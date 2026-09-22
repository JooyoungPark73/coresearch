"""Offline regression checks for parent-selected Codex model and effort."""
import copy
import importlib.util
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('harness', Path(__file__).with_name('harness.py'))
harness = importlib.util.module_from_spec(spec)
spec.loader.exec_module(harness)


class EffortPolicyTests(unittest.TestCase):
    def test_native_roles_allow_assignment_effort(self):
        self.assertEqual(harness.validate_source_roles(), [])
        for role in harness.roles():
            self.assertEqual(role['providers']['codex']['effort'], 'assignment')
            native = harness.parse_role_definition(
                harness.ROOT / 'agents/codex' / (role['name'] + '.toml'), 'codex')
            self.assertNotIn('model_reasoning_effort', native)
            self.assertNotIn('model', native)
            self.assertEqual(role['providers']['codex']['model'], 'assignment')

    def test_installed_fixed_effort_is_drift(self):
        name = 'coresearch-reader'
        text = (harness.ROOT / 'agents/codex' / (name + '.toml')).read_text()
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / (name + '.toml')
            path.write_text(text)
            row = next(row for row in harness.role_status(Path(tmp), 'codex') if row.startswith(name + ':'))
            self.assertNotIn('CONFIG-MISMATCH', row)
            for key in ('model', 'model_reasoning_effort'):
                for value in ('"gpt-6-astra"', "'medium'", '3', '""'):
                    path.write_text(key + ' = ' + value + '\n' + text)
                    row = next(row for row in harness.role_status(Path(tmp), 'codex') if row.startswith(name + ':'))
                    self.assertIn('CONFIG-MISMATCH', row)

    def test_source_overrides_are_drift(self):
        original = harness.parse_role_definition
        for key in ('model', 'model_reasoning_effort'):
            for value in ('gpt-6-astra', '<unparsed>', ''):
                def with_override(path, provider):
                    config = original(path, provider)
                    if provider == 'codex':
                        config[key] = value
                    return config
                with patch.object(harness, 'parse_role_definition', side_effect=with_override):
                    self.assertTrue(harness.validate_source_roles())

    def probe(self, effort, observed_effort, model='gpt-6-astra', observed_model='requested'):
        manifest = copy.deepcopy(harness.agent_manifest())
        manifest['codex_effort_policy']['probe_effort'] = effort
        output = {
            'agent_type': 'coresearch-reader',
            'text': 'CORESEARCH_ROLE_PROBE coresearch-reader',
        }
        if observed_model is not None:
            output['model'] = model if observed_model == 'requested' else observed_model
        if observed_effort is not None:
            output['model_reasoning_effort'] = observed_effort
        import json
        with patch.object(harness, 'agent_manifest', return_value=manifest), \
             patch.object(harness.shutil, 'which', return_value='/fixture/codex'), \
             patch.object(harness, '_is_git_worktree', return_value=True), \
             patch.object(harness.subprocess, 'run', return_value=subprocess.CompletedProcess(
                 [], 0, json.dumps(output))) as run:
            reports, failures = harness.probe_role_routing(
                ['codex'], {'codex': Path('/fixture')}, harness.ROOT, 'coresearch-reader', model)
        command = run.call_args.args[0]
        self.assertIn(f'model={model}', command[-1])
        self.assertIn(f'reasoning_effort={effort}', command[-1])
        self.assertIn('fork_turns=none', command[-1])
        self.assertIn(f'requested_model={model}', command[-1])
        self.assertIn(f'requested_effort={effort}', command[-1])
        self.assertIn('primary_skill=coresearch', command[-1])
        self.assertIn('no writes or network', command[-1])
        self.assertIn('stop after the marker reply', command[-1])
        self.assertNotIn('--model', command)
        return reports, failures

    def test_same_role_accepts_each_requested_effort(self):
        for effort in ('low', 'medium', 'high', 'xhigh'):
            with self.subTest(effort=effort):
                reports, failures = self.probe(effort, effort)
                self.assertEqual(failures, [])
                self.assertIn('status=verified', reports[0])

    def test_same_role_accepts_all_model_effort_combinations(self):
        for model in ('gpt-6-astra', 'gpt-5.6-sol', 'gpt-5.6-terra', 'gpt-5.6-luna'):
            for effort in ('low', 'medium', 'high', 'xhigh'):
                with self.subTest(model=model, effort=effort):
                    reports, failures = self.probe(effort, effort, model)
                    self.assertEqual(failures, [])
                    self.assertIn('status=verified', reports[0])

    def test_model_mismatch_and_missing_metadata(self):
        for observed, status in (('gpt-5.6-sol', 'mismatch'), (None, 'static-only')):
            reports, failures = self.probe('low', 'low', observed_model=observed)
            self.assertTrue(failures)
            self.assertIn('status=' + status, reports[0])

    def test_disallowed_model_never_runs(self):
        with patch.object(harness.subprocess, 'run') as run:
            reports, failures = harness.probe_role_routing(
                ['codex'], {'codex': Path('/fixture')}, harness.ROOT,
                'coresearch-reader', 'unapproved-model')
            self.assertTrue(failures)
            run.assert_not_called()

    def test_failed_static_preflight_never_probes(self):
        import contextlib
        import io
        args = harness.build_parser().parse_args([
            'doctor', '--strict', '--probe-models', '--surface', 'codex'])
        for policy in (None, {}, {'allowed': []}):
            manifest = copy.deepcopy(harness.agent_manifest())
            manifest['codex_model_policy'] = policy
            with patch.object(harness, 'agent_manifest', return_value=manifest), \
                 patch.object(harness, 'probe_role_routing') as probe, \
                 contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(harness.cmd_doctor(args), 1)
                probe.assert_not_called()
        with patch.object(harness, 'role_status', return_value=['fixture CONFIG-MISMATCH']), \
             patch.object(harness, 'probe_role_routing') as probe, \
             contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(harness.cmd_doctor(args), 1)
            probe.assert_not_called()

    def test_invalid_model_policies(self):
        for key, value in (
            ('allowed', ['gpt-6-astra']), ('default_model', 'unknown'),
            ('fallback_model', 'unknown'), ('default_model', 'gpt-5.6-sol'),
            ('fallback_model', 'gpt-5.6-sol'), ('probe_model', 'unknown'),
            ('selection', {}), ('selection', {'gpt-6-astra': ''}),
        ):
            manifest = copy.deepcopy(harness.agent_manifest())
            manifest.setdefault('codex_model_policy', {})[key] = value
            with patch.object(harness, 'agent_manifest', return_value=manifest):
                self.assertTrue(harness.validate_source_roles(), key)

    def test_different_effort_fails(self):
        reports, failures = self.probe('medium', 'high')
        self.assertTrue(failures)
        self.assertIn('status=mismatch', reports[0])

    def test_missing_effort_is_static_only(self):
        reports, failures = self.probe('medium', None)
        self.assertTrue(failures)
        self.assertIn('status=static-only', reports[0])

    def test_invalid_policy_fails_source_validation(self):
        manifest = copy.deepcopy(harness.agent_manifest())
        manifest['codex_effort_policy']['probe_effort'] = 'automatic'
        with patch.object(harness, 'agent_manifest', return_value=manifest):
            self.assertTrue(harness.validate_source_roles())


if __name__ == '__main__':
    unittest.main()
