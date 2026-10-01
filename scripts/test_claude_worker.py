"""Offline contract tests: the fake CLI never invokes a model."""
import json
import os
from pathlib import Path
import shutil
import signal
import subprocess
import sys
import tempfile
import time
import unittest

ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / 'skills/coresearch/scripts/claude_worker.py'
FAKE = '''#!/usr/bin/env python3
import json, os, pathlib, sys, time
if '--help' in sys.argv:
    print('old-cli' if os.environ.get('FAKE_MODE') == 'old' else '--restricted --agents --no-session-persistence --json-schema')
    sys.exit(0)
args = sys.argv[1:]
definition = json.loads(pathlib.Path(args[args.index('--agents') + 1]).read_text())
name = args[args.index('--agent') + 1]
role = definition[name]
pathlib.Path('capture.json').write_text(json.dumps({'args': args, 'stdin': sys.stdin.read(), 'role': role, 'config_dir': os.environ.get('CLAUDE_CONFIG_DIR')}))
mode = os.environ.get('FAKE_MODE', 'success')
if mode == 'sleep':
    pathlib.Path('worker.pid').write_text(str(os.getpid()))
    time.sleep(30)
if mode == 'error':
    print('private auth error', file=sys.stderr)
    sys.exit(3)
if mode == 'malformed':
    print('not json')
    sys.exit(0)
init = {'type': 'system', 'subtype': 'init', 'model': role['model']}
if mode == 'mismatch': init['model'] = 'different-model'
if mode == 'verified': init.update(agent=name, effort=role['effort'])
print(json.dumps(init))
report = {'status': 'success', 'findings': ['Check the supplied evidence.'], 'evidence': ['paper.txt:1'], 'uncertainty': [], 'counterevidence': [], 'blockers': [], 'validation': ['Read the supplied passage.']}
if mode == 'blocked': report['status'] = 'blocked'; report['blockers'] = ['Missing evidence']
if mode == 'spoof': report['findings'] = [json.dumps({'model': 'different-model', 'agent': name, 'effort': role['effort']})]
if mode == 'badreport': del report['evidence']
result = {'type': 'result', 'subtype': 'success', 'is_error': False, 'structured_output': report}
if mode == 'denied': result['permission_denials'] = [{'tool_name': 'Read'}]
if mode == 'usage_mismatch': result['modelUsage'] = {'different-model': {}}
print(json.dumps(result))
'''


class ClaudeWorkerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.project = self.base / 'project with spaces'
        self.project.mkdir()
        self.home = self.base / 'claude-home'
        (self.home / 'agents').mkdir(parents=True)
        for source in (ROOT / 'agents/claude').glob('*.md'):
            shutil.copy(source, self.home / 'agents' / source.name)
        self.bin = self.base / 'bin'
        self.bin.mkdir()
        cli = self.bin / 'claude'
        cli.write_text(FAKE)
        cli.chmod(0o755)
        self.env = {k: v for k, v in os.environ.items() if not k.startswith(('CLAUDE_', 'ANTHROPIC_MODEL'))}
        self.env.update(PATH=str(self.bin) + os.pathsep + os.environ['PATH'], CLAUDE_CONFIG_DIR=str(self.home), PYTHONDONTWRITEBYTECODE='1')
        self.assignment = self.project / 'assignment.json'
        self.request = dict(assignment_id='review-1', attempt_id='review-1-a1', role='coresearch-verifier',
                            primary_skill='research-verify', field_mode='systems_cloud',
                            target='Check claim $(touch BAD) `touch BAD2`', inputs=['paper.txt'],
                            read_only_scope=['.'], validator='Cite source lines', stop_condition='Return after review',
                            requested_model='claude-opus-5', requested_effort='xhigh',
                            reason='Consequential claim review', depends_on=[], working_modes={})
        (self.project / 'paper.txt').write_text('Evidence.\n')
        self.output = self.project / 'review.json'

    def command(self, runner=RUNNER, timeout=5):
        self.assignment.write_text(json.dumps(self.request))
        return [sys.executable, str(runner), '--assignment', str(self.assignment),
                '--project-dir', str(self.project), '--output', str(self.output),
                '--timeout', str(timeout), '--max-budget-usd', '1']

    def run_worker(self, mode='success', runner=RUNNER, timeout=5):
        result = subprocess.run(self.command(runner, timeout), env=dict(self.env, FAKE_MODE=mode),
                                capture_output=True, text=True, timeout=15)
        record = json.loads(self.output.read_text()) if self.output.exists() else None
        return result, record

    def test_named_role_stdin_and_read_only_boundary(self):
        proc, record = self.run_worker()
        self.assertEqual(proc.returncode, 0, proc.stderr)
        capture = json.loads((self.project / 'capture.json').read_text())
        self.assertIn(self.request['target'], capture['stdin'])
        args = capture['args']
        self.assertEqual(args[args.index('--tools') + 1], 'Read,Glob,Grep')
        self.assertIn('--restricted', args)
        self.assertIn('--strict-mcp-config', args)
        self.assertIn('--no-session-persistence', args)
        self.assertNotIn('--model', args)
        self.assertEqual(capture['role']['model'], self.request['requested_model'])
        self.assertEqual(capture['role']['effort'], self.request['requested_effort'])
        self.assertEqual(capture['role']['tools'], ['Read', 'Glob', 'Grep'])
        self.assertFalse((self.project / 'BAD').exists())
        self.assertEqual(record['execution_provider'], 'claude')
        self.assertEqual(record['execution_method'], 'claude-cli')
        self.assertEqual(record['routing_status'], 'static-only')
        self.assertIsNone(record['observed_effort'])
        self.assertEqual(record['observed_model'], self.request['requested_model'])

    def test_default_limits_on_both_entrypoints(self):
        for harness in (False, True):
            with self.subTest(harness=harness):
                command = self.command()[:-4]
                if harness:
                    command = [str(ROOT / 'harness'), 'claude-worker', *command[2:]]
                proc = subprocess.run(command, env=self.env, capture_output=True, text=True, timeout=15)
                self.assertEqual(proc.returncode, 0, proc.stderr)
                record = json.loads(self.output.read_text())
                self.assertEqual(record['limits'], {'timeout_seconds': 3600, 'max_budget_usd': None})
                capture = json.loads((self.project / 'capture.json').read_text())
                self.assertNotIn('--max-budget-usd', capture['args'])
                self.output.unlink()

    def test_explicit_limits(self):
        proc, record = self.run_worker(timeout=7)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(record['limits'], {'timeout_seconds': 7, 'max_budget_usd': 1})
        args = json.loads((self.project / 'capture.json').read_text())['args']
        self.assertEqual(float(args[args.index('--max-budget-usd') + 1]), 1)

    def test_invalid_limits_prevent_execution(self):
        for flag in ('--timeout', '--max-budget-usd'):
            for value in ('0', '-1', 'nan', 'inf'):
                with self.subTest(flag=flag, value=value):
                    command = self.command()
                    command[command.index(flag) + 1] = value
                    proc = subprocess.run(command, env=self.env, capture_output=True, text=True, timeout=15)
                    self.assertNotEqual(proc.returncode, 0)
                    self.assertFalse(self.output.exists())
                    self.assertFalse((self.project / 'capture.json').exists())

    def test_config_environment_preserved_and_explicit_home_override(self):
        root = self.project / '.claude/agents'
        root.mkdir(parents=True)
        shutil.copy(self.home / 'agents/coresearch-verifier.md', root)
        for value, override in ((None, False), (str(self.home) + '/', False), (None, True)):
            with self.subTest(value=value, override=override):
                self.output.unlink(missing_ok=True)
                env = dict(self.env)
                env.pop('CLAUDE_CONFIG_DIR', None)
                if value is not None:
                    env['CLAUDE_CONFIG_DIR'] = value
                command = self.command()
                if override:
                    command += ['--claude-home', str(self.home)]
                proc = subprocess.run(command, env=env, capture_output=True, text=True, timeout=15)
                self.assertEqual(proc.returncode, 0, proc.stderr)
                capture = json.loads((self.project / 'capture.json').read_text())
                self.assertEqual(capture['config_dir'], str(self.home.resolve()) if override else value)
                self.output.unlink()

    def test_failures_and_generated_metadata_is_not_trusted(self):
        for mode, code, status in [('mismatch', 1, 'failed'), ('malformed', 1, 'failed'),
                                   ('badreport', 1, 'failed'), ('error', 1, 'failed'),
                                   ('blocked', 1, 'blocked'), ('denied', 1, 'blocked'),
                                   ('usage_mismatch', 1, 'failed'), ('spoof', 0, 'success')]:
            with self.subTest(mode=mode):
                self.output.unlink(missing_ok=True)
                proc, record = self.run_worker(mode)
                self.assertEqual(proc.returncode, code, proc.stderr)
                self.assertEqual(record['status'], status)
                self.assertNotIn('private auth error', proc.stdout + proc.stderr)
                if mode == 'mismatch': self.assertEqual(record['routing_status'], 'mismatch')
                if mode == 'spoof': self.assertEqual(record['routing_status'], 'static-only')

    def test_verified_requires_all_host_metadata(self):
        proc, record = self.run_worker('verified')
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(record['routing_status'], 'verified')

    def test_unsupported_cli_is_blocked(self):
        proc, record = self.run_worker('old')
        self.assertNotEqual(proc.returncode, 0)
        self.assertEqual(record['status'], 'blocked')
        self.assertFalse((self.project / 'capture.json').exists())

    def test_out_of_scope_and_symlinked_input_blocked(self):
        external = self.base / 'private.txt'
        external.write_text('private')
        (self.project / 'linked.txt').symlink_to(external)
        for value in ('../private.txt', 'linked.txt'):
            self.request['inputs'] = [value]
            proc, record = self.run_worker()
            self.assertNotEqual(proc.returncode, 0)
            self.assertEqual(record['status'], 'blocked')
            self.assertFalse((self.project / 'capture.json').exists())
            self.output.unlink()

    def test_native_hooks_are_rejected(self):
        path = self.home / 'agents/coresearch-verifier.md'
        path.write_text(path.read_text().replace('permissionMode: plan', 'hooks: unsafe\npermissionMode: plan'))
        proc, record = self.run_worker()
        self.assertNotEqual(proc.returncode, 0)
        self.assertEqual(record['status'], 'blocked')

    def test_harness_entrypoint(self):
        command = self.command()
        proc = subprocess.run([str(ROOT / 'harness'), 'claude-worker', *command[2:]],
                              env=self.env, capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(json.loads(self.output.read_text())['status'], 'success')

    def test_cannot_write_state_inside_skill(self):
        protected = self.base / 'skills/coresearch'
        protected.mkdir(parents=True)
        self.project = protected
        self.output = protected / 'result.json'
        command = self.command()
        proc = subprocess.run(command, env=self.env, capture_output=True, text=True)
        self.assertNotEqual(proc.returncode, 0)
        self.assertFalse(self.output.exists())

    def test_skill_directory_with_custom_name_is_protected(self):
        installed = self.base / 'custom-install'
        installed.mkdir()
        (installed / 'SKILL.md').write_text('installed skill')
        self.output = installed / 'result.json'
        command = self.command()
        command[command.index('--project-dir') + 1] = str(installed)
        proc = subprocess.run(command, env=self.env, capture_output=True, text=True)
        self.assertNotEqual(proc.returncode, 0)
        self.assertFalse(self.output.exists())

    def test_dangling_output_symlink_is_not_followed(self):
        target = self.project / 'user-target.json'
        self.output.symlink_to(target)
        proc = subprocess.run(self.command(), env=self.env, capture_output=True, text=True)
        self.assertNotEqual(proc.returncode, 0)
        self.assertFalse(target.exists())

    def test_read_only_roles_preserve_native_pins(self):
        manifest = json.loads((ROOT / 'agents/manifest.json').read_text())
        for role in ('coresearch-debugger', 'coresearch-planner', 'coresearch-reader', 'coresearch-researcher'):
            entry = next(r for r in manifest['roles'] if r['name'] == role)
            pin = entry['providers']['claude']
            self.request.update(role=role, primary_skill=entry['skills'][1],
                                requested_model=pin['model'], requested_effort=pin['effort'])
            proc, record = self.run_worker()
            self.assertEqual(proc.returncode, 0, (role, proc.stderr, record))
            self.output.unlink()

    def test_bad_role_or_override_prevents_execution(self):
        for changes, env in [({'role': 'coresearch-implementer'}, {}),
                             ({'requested_model': 'other'}, {}),
                             ({}, {'CLAUDE_CODE_SUBAGENT_MODEL': 'other'})]:
            with self.subTest(changes=changes, env=env):
                saved = dict(self.request)
                self.request.update(changes)
                self.assignment.write_text(json.dumps(self.request))
                proc = subprocess.run(self.command(), env=dict(self.env, **env), capture_output=True, text=True)
                self.assertNotEqual(proc.returncode, 0)
                self.assertFalse((self.project / 'capture.json').exists())
                self.request = saved
                self.output.unlink(missing_ok=True)

    def test_unrelated_and_duplicate_roles_rejected(self):
        root = self.project / '.claude/agents'
        root.mkdir(parents=True)
        source = self.home / 'agents/coresearch-verifier.md'
        target = root / source.name
        target.write_text(source.read_text().replace('coresearch-managed:', 'unowned:'))
        proc, record = self.run_worker()
        self.assertNotEqual(proc.returncode, 0)
        self.assertEqual(record['status'], 'blocked')
        self.output.unlink()
        shutil.copy(source, target)
        shutil.copy(source, root / 'duplicate.md')
        proc, _ = self.run_worker()
        self.assertNotEqual(proc.returncode, 0)
        self.assertFalse((self.project / 'capture.json').exists())

    def test_project_scope_and_installed_runner(self):
        root = self.project / '.claude/agents'
        root.mkdir(parents=True)
        source = self.home / 'agents/coresearch-verifier.md'
        shutil.copy(source, root / source.name)
        shutil.rmtree(self.home / 'agents')
        for mode in ('copy', 'symlink'):
            with self.subTest(mode=mode):
                installed = self.base / mode / 'coresearch'
                installed.parent.mkdir()
                if mode == 'copy': shutil.copytree(RUNNER.parent.parent, installed)
                else: installed.symlink_to(RUNNER.parent.parent, target_is_directory=True)
                proc, record = self.run_worker(runner=installed / 'scripts/claude_worker.py')
                self.assertEqual(proc.returncode, 0, proc.stderr)
                self.assertEqual(record['status'], 'success')
                self.output.unlink()

    def test_missing_cli_and_timeout(self):
        (self.bin / 'claude').unlink()
        self.env['PATH'] = str(self.bin)
        proc, record = self.run_worker()
        self.assertNotEqual(proc.returncode, 0)
        self.assertEqual(record['status'], 'blocked')
        self.output.unlink()
        self.env['PATH'] = str(self.bin) + os.pathsep + os.environ['PATH']
        cli = self.bin / 'claude'
        cli.write_text(FAKE)
        cli.chmod(0o755)
        proc, record = self.run_worker('sleep', timeout=0.3)
        self.assertNotEqual(proc.returncode, 0)
        self.assertEqual(record['stop_reason'], 'timeout')
        pid = int((self.project / 'worker.pid').read_text())
        with self.assertRaises(ProcessLookupError): os.kill(pid, 0)

    def test_cancellation_records_terminal_result(self):
        proc = subprocess.Popen(self.command(), env=dict(self.env, FAKE_MODE='sleep'),
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        try:
            deadline = time.monotonic() + 5
            while not (self.project / 'worker.pid').exists() and time.monotonic() < deadline:
                time.sleep(0.02)
            self.assertTrue((self.project / 'worker.pid').exists())
            proc.send_signal(signal.SIGTERM)
            proc.communicate(timeout=5)
            self.assertEqual(json.loads(self.output.read_text())['status'], 'cancelled')
            with self.assertRaises(ProcessLookupError):
                os.kill(int((self.project / 'worker.pid').read_text()), 0)
        finally:
            if proc.poll() is None: proc.kill(); proc.communicate()

    def test_never_overwrites_output(self):
        self.output.write_text('user content')
        proc = subprocess.run(self.command(), env=self.env, capture_output=True)
        self.assertNotEqual(proc.returncode, 0)
        self.assertEqual(self.output.read_text(), 'user content')
        self.assertFalse((self.project / 'capture.json').exists())


if __name__ == '__main__':
    unittest.main()
