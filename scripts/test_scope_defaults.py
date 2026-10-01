"""Offline checks for project-default installation and diagnostics."""
import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('harness', ROOT / 'scripts/harness.py')
harness = importlib.util.module_from_spec(spec)
spec.loader.exec_module(harness)


class ScopeDefaultTests(unittest.TestCase):
    def test_project_default_and_explicit_user_scope(self):
        parser = harness.build_parser()
        for command in ('install', 'link', 'uninstall', 'doctor', 'repair', 'update'):
            with self.subTest(command=command):
                self.assertEqual(parser.parse_args([command]).scope, 'project')
                self.assertEqual(parser.parse_args([command, '--scope', 'user']).scope, 'user')

    def test_install_and_doctor_use_current_project_without_touching_user_roots(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            project = base / 'project'
            project.mkdir()
            prompt = project / 'AGENTS.md'
            prompt.write_text('Preserve this project prompt\n')
            home_args = ['--codex-home', str(base / 'user-codex'),
                         '--codex-skills-root', str(base / 'user-skills'),
                         '--claude-home', str(base / 'user-claude')]
            for command in (['install'], ['doctor', '--strict']):
                result = subprocess.run(
                    [sys.executable, str(ROOT / 'scripts/harness.py'), *command,
                     '--surface', 'both', *home_args], cwd=project, capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertTrue((project / '.agents/skills/coresearch/SKILL.md').is_file())
            self.assertTrue((project / '.codex/agents/coresearch-planner.toml').is_file())
            self.assertTrue((project / '.claude/skills/coresearch/SKILL.md').is_file())
            self.assertTrue((project / '.claude/agents/coresearch-planner.md').is_file())
            for name in ('user-codex', 'user-skills', 'user-claude'):
                self.assertFalse((base / name).exists(), name)
            self.assertEqual(prompt.read_text(), 'Preserve this project prompt\n')

    def test_link_keeps_selected_scope(self):
        for scope in ('project', 'user'):
            args = harness.build_parser().parse_args(['link', '--scope', scope])
            with patch.object(harness, 'cmd_install', return_value=0) as install:
                self.assertEqual(harness.cmd_link(args), 0)
                self.assertEqual(install.call_args.args[0].scope, scope)
                self.assertEqual(install.call_args.args[0].mode, 'symlink')


if __name__ == '__main__':
    unittest.main()
