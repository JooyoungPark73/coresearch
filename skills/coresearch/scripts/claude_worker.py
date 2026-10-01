#!/usr/bin/env python3
"""Execute one read-only native Claude assignment; no scheduling or runtime manifest."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import re
import shutil
import signal
import subprocess
import sys
import tempfile
import time

# Execution eligibility, not another role/model registry. Pins come from the
# installed native definition and must match the parent's declared assignment.
SUPPORTED_ROLES = ('coresearch-verifier', 'coresearch-debugger', 'coresearch-planner',
                   'coresearch-reader', 'coresearch-researcher')
READ_TOOLS = ['Read', 'Glob', 'Grep']
REPORT_FIELDS = ('findings', 'evidence', 'uncertainty', 'counterevidence', 'blockers', 'validation')
REPORT_SCHEMA = {
    'type': 'object', 'additionalProperties': False,
    'required': ['status', *REPORT_FIELDS],
    'properties': {
        'status': {'type': 'string', 'enum': ['success', 'blocked']},
        **{key: {'type': 'array', 'maxItems': 32,
                 'items': {'type': 'string', 'maxLength': 4000}} for key in REPORT_FIELDS},
    },
}


class ContractError(ValueError):
    pass


class Cancelled(Exception):
    pass


def positive(value: str) -> float:
    number = float(value)
    if not math.isfinite(number) or number <= 0:
        raise argparse.ArgumentTypeError('must be a finite positive number')
    return number


def add_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument('--assignment', required=True, help='JSON assignment file')
    parser.add_argument('--project-dir', required=True, help='read-only working directory')
    parser.add_argument('--output', required=True, help='new terminal record inside project')
    parser.add_argument('--timeout', type=positive, default=3600, help='wall-clock seconds (default: 3600)')
    parser.add_argument('--max-budget-usd', type=positive, help='optional Claude API dollar cap (default: no cap)')
    parser.add_argument('--claude-home', help='override role/config root and credential context; default: preserve CLAUDE_CONFIG_DIR or use ~/.claude')


def native_definition(path: Path) -> tuple[dict, str, str]:
    """Parse only the flat scalar/list frontmatter emitted by Coresearch."""
    text = path.read_text()
    if not text.startswith('---\n') or '\n---\n' not in text[4:]:
        raise ContractError('invalid native role frontmatter')
    header, body = text[4:].split('\n---\n', 1)
    data: dict = {}
    key = None
    for line in header.splitlines():
        if line.startswith('  - ') and key and isinstance(data[key], list):
            data[key].append(line[4:])
        else:
            match = re.fullmatch(r'([A-Za-z]+):(?: (.+))?', line)
            if not match or match[1] in data:
                raise ContractError('unsupported or duplicate native role field')
            key = match[1]
            data[key] = match[2] if match[2] is not None else []
    allowed = {'name', 'description', 'model', 'effort', 'permissionMode', 'tools', 'skills'}
    if set(data) != allowed or '<!-- coresearch-managed: role-description-version=2 -->' not in body:
        raise ContractError('unowned or incompatible native role')
    if any(not isinstance(data[k], str) or not data[k] for k in allowed - {'tools', 'skills'}):
        raise ContractError('invalid native role scalar')
    if any(not isinstance(data[k], list) or not data[k] for k in ('tools', 'skills')):
        raise ContractError('invalid native role list')
    if data['permissionMode'] != 'plan' or not set(READ_TOOLS).issubset(data['tools']):
        raise ContractError('role must support read-only analysis')
    if {'Edit', 'Write', 'Agent', 'Task'} & set(data['tools']):
        raise ContractError('role grants incompatible tools')
    if data['effort'] not in ('low', 'medium', 'high', 'xhigh') or data['model'] == 'inherit':
        raise ContractError('role must pin model and effort')
    return data, body, hashlib.sha256(text.encode()).hexdigest()


def resolve_role(project: Path, home: Path, name: str) -> tuple[Path, dict, str, str]:
    # Snapshot the chosen native definition into --agents so host discovery of
    # ancestor/plugin roles cannot silently select a different definition.
    for root in (project / '.claude/agents', home / 'agents'):
        matches = []
        if root.exists():
            for path in root.rglob('*.md'):
                text = path.read_text()
                if path.name == name + '.md' or re.search(r'^name: [\"\']?' + re.escape(name) + r'[\"\']?\s*$', text, re.M):
                    matches.append(path)
        if len(matches) > 1:
            raise ContractError('ambiguous native role in one discovery scope')
        if matches:
            config, body, digest = native_definition(matches[0])
            if config['name'] != name:
                raise ContractError('native role name differs from assignment')
            return matches[0], config, body, digest
    raise ContractError('native Claude role is not installed at project or user scope')


def load_assignment(path: Path, project: Path) -> dict:
    if path.stat().st_size > 256_000:
        raise ContractError('assignment exceeds 256 KB')
    request = json.loads(path.read_text())
    if not isinstance(request, dict):
        raise ContractError('assignment must be an object')
    for key in ('assignment_id', 'attempt_id', 'role', 'primary_skill', 'field_mode', 'target',
                'validator', 'stop_condition', 'requested_model', 'requested_effort', 'reason'):
        if not isinstance(request.get(key), str) or not request[key].strip():
            raise ContractError('assignment requires nonempty ' + key)
    if request['role'] not in SUPPORTED_ROLES:
        raise ContractError('role is not eligible for this read-only Claude adapter')
    for key in ('inputs', 'read_only_scope', 'depends_on'):
        if not isinstance(request.get(key), list) or any(not isinstance(x, str) for x in request[key]):
            raise ContractError('assignment requires a string list: ' + key)
    if not request['read_only_scope']:
        raise ContractError('read_only_scope cannot be empty')
    for key in ('inputs', 'read_only_scope'):
        for value in request[key]:
            resolved = (project / value).resolve()
            if not resolved.is_relative_to(project) or not resolved.exists():
                raise ContractError('inputs and read_only_scope must exist inside project')
    scopes = [(project / value).resolve() for value in request['read_only_scope']]
    if any(not any((project / value).resolve().is_relative_to(scope) for scope in scopes)
           for value in request['inputs']):
        raise ContractError('input is outside declared read_only_scope')
    modes = request.get('working_modes')
    if not isinstance(modes, dict) or set(modes) - {'ponytail', 'caveman'} or any(v not in ('off', 'lite', 'full') for v in modes.values()):
        raise ContractError('invalid working_modes')
    return request


def interpret(stdout: Path, request: dict, record: dict) -> None:
    """Inspect host envelopes only; never search generated content for routing."""
    observed = {'model': set(), 'effort': set(), 'agent': set()}
    result = None
    with stdout.open() as stream:
        for line in stream:
            if len(line) > 2_000_000:
                raise ContractError('host event exceeds output limit')
            event = json.loads(line)
            if not isinstance(event, dict):
                raise ContractError('invalid host event')
            if event.get('type') == 'system' and event.get('subtype') == 'init':
                for key in observed:
                    if isinstance(event.get(key), str):
                        observed[key].add(event[key])
            if event.get('type') == 'result':
                if result is not None:
                    raise ContractError('multiple terminal host results')
                result = event
                usage = event.get('modelUsage', {})
                if isinstance(usage, dict):
                    observed['model'].update(k for k in usage if isinstance(k, str))
    for key, dest in [('model', 'observed_model'), ('effort', 'observed_effort'), ('agent', 'observed_role')]:
        record[dest] = next(iter(observed[key])) if len(observed[key]) == 1 else None
    expected = {'model': request['requested_model'], 'effort': request['requested_effort'], 'agent': request['role']}
    if any(values and values != {expected[key]} for key, values in observed.items()):
        record['routing_status'] = 'mismatch'
        raise ContractError('host routing differs from assignment')
    record['routing_status'] = 'verified' if all(observed.values()) else 'static-only'
    if not result or result.get('subtype') != 'success' or result.get('is_error') is not False:
        raise ContractError('host did not report successful completion; inspect raw logs')
    report = result.get('structured_output')
    if not isinstance(report, dict) or set(report) != {'status', *REPORT_FIELDS} or report['status'] not in ('success', 'blocked'):
        raise ContractError('invalid structured worker report')
    for key in REPORT_FIELDS:
        values = report[key]
        if not isinstance(values, list) or len(values) > 32 or any(not isinstance(v, str) or len(v) > 4000 for v in values):
            raise ContractError('invalid or oversized worker report field')
    if len(json.dumps(report)) > 64_000:
        raise ContractError('worker report exceeds 64 KB')
    record['report'] = report
    record['status'] = 'blocked' if report['status'] == 'blocked' or report['blockers'] or result.get('permission_denials') else 'success'
    record['stop_reason'] = 'worker blocked or permissions denied' if record['status'] == 'blocked' else 'assignment returned; parent validation required'


def stop_process(process: subprocess.Popen) -> None:
    try:
        os.killpg(process.pid, signal.SIGTERM)
    except ProcessLookupError:
        pass
    try:
        process.wait(timeout=2)
    except subprocess.TimeoutExpired:
        pass
    # The leader may have exited while a descendant ignored SIGTERM.
    try:
        os.killpg(process.pid, signal.SIGKILL)
    except ProcessLookupError:
        pass
    finally:
        process.wait()


def execute(args: argparse.Namespace) -> int:
    project = Path(args.project_dir).resolve()
    if Path(args.output).is_symlink():
        print('ERROR: output is an existing symlink; use a new output path', file=sys.stderr)
        return 1
    output = Path(args.output).resolve()
    protected = {'skills', 'agents', '.git', '.agents', '.codex', '.claude'}
    if (not project.is_dir() or not output.is_relative_to(project)
            or protected & set(output.parts)
            or any((parent / 'SKILL.md').is_file() for parent in output.parents)):
        print('ERROR: output must be inside project and outside skill/role/config directories', file=sys.stderr)
        return 1
    # Reserve the result before spending tokens; never replace user artifacts.
    output.parent.mkdir(parents=True, exist_ok=True)
    try:
        fd = os.open(output, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    except FileExistsError:
        print('ERROR: output already exists; use a new attempt and output path', file=sys.stderr)
        return 1
    record = dict(assignment_id=None, attempt_id=None, role=None, status='blocked',
                  execution_provider='claude', execution_method='claude-cli',
                  requested_model=None, requested_effort=None, observed_model=None,
                  observed_effort=None, observed_role=None, routing_status='mismatch',
                  artifacts=[], validators=[], stop_reason='', report=None)
    started = time.monotonic()
    process = None
    previous_handlers = {}
    def cancel(signum, frame):
        raise Cancelled()
    try:
        for sig in (signal.SIGTERM, signal.SIGINT):
            previous_handlers[sig] = signal.signal(sig, cancel)
        request = load_assignment(Path(args.assignment), project)
        for key in ('assignment_id', 'attempt_id', 'role', 'requested_model', 'requested_effort'):
            record[key] = request[key]
        home = Path(args.claude_home or os.environ.get('CLAUDE_CONFIG_DIR', '~/.claude')).expanduser().resolve()
        role_path, config, body, role_digest = resolve_role(project, home, request['role'])
        for key in ('model', 'effort'):
            if config[key] != request['requested_' + key]:
                raise ContractError('requested ' + key + ' differs from installed role pin')
        if request['primary_skill'] not in config['skills']:
            raise ContractError('primary_skill is not supported by installed role')
        overrides = ('CLAUDE_CODE_SUBAGENT_MODEL', 'ANTHROPIC_MODEL', 'CLAUDE_CODE_EFFORT_LEVEL',
                     *(key for key in os.environ if key.startswith('ANTHROPIC_DEFAULT_') and key.endswith('_MODEL')))
        if any(os.environ.get(key) for key in overrides):
            raise ContractError('model/effort environment override is set')
        executable = shutil.which('claude')
        if not executable:
            raise ContractError('Claude CLI is unavailable')
        scratch_root = project / '.tmp/claude-worker'
        if (not scratch_root.resolve().is_relative_to(project)
                or protected & set(scratch_root.resolve().parts)
                or any((parent / 'SKILL.md').is_file() for parent in scratch_root.resolve().parents)):
            raise ContractError('scratch must remain inside project')
        scratch_root.mkdir(parents=True, exist_ok=True)
        scratch = Path(tempfile.mkdtemp(prefix='attempt-', dir=scratch_root))
        record['logs'] = str(scratch)
        record['role_source'] = str(role_path)
        record['role_sha256'] = role_digest
        record['limits'] = {'timeout_seconds': args.timeout, 'max_budget_usd': args.max_budget_usd}
        env = os.environ.copy()
        # Even explicitly setting the default path can change macOS Keychain
        # lookup. Preserve the caller's exact credential context by default.
        if args.claude_home is not None:
            env['CLAUDE_CONFIG_DIR'] = str(home)
        help_result = subprocess.run([executable, '--help'], env=env, cwd=project, capture_output=True, text=True, timeout=min(10, args.timeout))
        (scratch / 'help.txt').write_text(help_result.stdout + help_result.stderr)
        if help_result.returncode or '--restricted' not in help_result.stdout:
            raise ContractError('Claude CLI with --restricted support is required')
        # CLI-defined snapshot takes precedence; restrict capabilities without
        # changing model, effort, skills, or the native role instructions.
        definition = {key: value for key, value in config.items() if key != 'name'}
        definition.update(prompt=body, tools=READ_TOOLS, permissionMode='dontAsk')
        snapshot = scratch / 'agent.json'
        snapshot.write_text(json.dumps({request['role']: definition}))
        command = [executable, '--agent', request['role'], '--agents', str(snapshot),
                   '--print', '--output-format', 'stream-json', '--verbose',
                   '--restricted', '--tools', ','.join(READ_TOOLS),
                   '--permission-mode', 'dontAsk', '--setting-sources', '',
                   '--settings', json.dumps({'disableAllHooks': True}),
                   '--strict-mcp-config', '--mcp-config', '{"mcpServers":{}}',
                   '--no-session-persistence',
                   '--json-schema', json.dumps(REPORT_SCHEMA)]
        if args.max_budget_usd is not None:
            command.extend(['--max-budget-usd', str(args.max_budget_usd)])
        prompt = ('Execute exactly this Coresearch assignment. Do not delegate, run commands, edit files, '
                  'or update the ledger. Read only the declared scope. Return structured findings with '
                  'source locators, uncertainty, counterevidence, validation and blockers. '
                  'Missing evidence is a blocker, not permission to widen scope.\n' + json.dumps(request))
        record['status'] = 'failed'
        stdout, stderr = scratch / 'stdout.jsonl', scratch / 'stderr.log'
        with stdout.open('w') as out, stderr.open('w') as err:
            process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=out, stderr=err,
                                       cwd=project, env=env, text=True, start_new_session=True)
            process.communicate(prompt, timeout=max(0.001, args.timeout - (time.monotonic() - started)))
        record['exit_code'] = process.returncode
        if process.returncode:
            raise ContractError('Claude exited unsuccessfully; inspect raw logs')
        interpret(stdout, request, record)
    except (Cancelled, KeyboardInterrupt):
        record.update(status='cancelled', stop_reason='cancelled')
    except subprocess.TimeoutExpired:
        record.update(status='failed', stop_reason='timeout')
    except (ContractError, OSError, ValueError) as exc:
        # Exception messages from JSON/filesystem can contain private content.
        record['stop_reason'] = str(exc) if isinstance(exc, ContractError) else 'invalid input/output or filesystem error; inspect local files'
    finally:
        for sig in previous_handlers:
            signal.signal(sig, signal.SIG_IGN)
        if process is not None:
            stop_process(process)
        if record['status'] != 'success':
            record['routing_status'] = 'mismatch'
        record['duration_seconds'] = round(time.monotonic() - started, 3)
        with os.fdopen(fd, 'w') as stream:
            json.dump(record, stream, indent=2)
            stream.write('\n')
        for sig, handler in previous_handlers.items():
            signal.signal(sig, handler)
    print(json.dumps({'status': record['status'], 'routing_status': record['routing_status'], 'output': str(output)}))
    return 0 if record['status'] == 'success' else 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    add_arguments(parser)
    return execute(parser.parse_args())


if __name__ == '__main__':
    raise SystemExit(main())
