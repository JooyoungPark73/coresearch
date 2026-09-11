"""Offline regression checks for parent-selected Codex effort."""
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

    def test_installed_fixed_effort_is_drift(self):
        name = 'coresearch-reader'
        text = (harness.ROOT / 'agents/codex' / (name + '.toml')).read_text()
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / (name + '.toml')
            path.write_text(text)
            row = next(row for row in harness.role_status(Path(tmp), 'codex') if row.startswith(name + ':'))
            self.assertNotIn('CONFIG-MISMATCH', row)
            for value in ('"low"', "'medium'", '3', '""'):
                path.write_text('model_reasoning_effort = ' + value + '\n' + text)
                row = next(row for row in harness.role_status(Path(tmp), 'codex') if row.startswith(name + ':'))
                self.assertIn('CONFIG-MISMATCH', row)

    def probe(self, effort, observed_effort):
        manifest = copy.deepcopy(harness.agent_manifest())
        manifest['codex_effort_policy']['probe_effort'] = effort
        output = {
            'agent_type': 'coresearch-reader', 'model': 'gpt-6-astra',
            'text': 'CORESEARCH_ROLE_PROBE coresearch-reader',
        }
        if observed_effort is not None:
            output['model_reasoning_effort'] = observed_effort
        import json
        with patch.object(harness, 'agent_manifest', return_value=manifest), \
             patch.object(harness.shutil, 'which', return_value='/fixture/codex'), \
             patch.object(harness, '_is_git_worktree', return_value=True), \
             patch.object(harness.subprocess, 'run', return_value=subprocess.CompletedProcess(
                 [], 0, json.dumps(output))) as run:
            reports, failures = harness.probe_role_routing(
                ['codex'], {'codex': Path('/fixture')}, harness.ROOT, 'coresearch-reader')
        command = run.call_args.args[0]
        self.assertIn(f'reasoning_effort={effort}', command[-1])
        self.assertIn('fork_turns=none', command[-1])
        self.assertNotIn('--model', command)
        return reports, failures

    def test_same_role_accepts_each_requested_effort(self):
        for effort in ('low', 'medium', 'high', 'xhigh'):
            with self.subTest(effort=effort):
                reports, failures = self.probe(effort, effort)
                self.assertEqual(failures, [])
                self.assertIn('status=verified', reports[0])

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
