"""Isolated uninstall checks; never touch the user's installed entries."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SKILLS = [row['name'] for row in json.loads((ROOT / 'skills/manifest.json').read_text())['owned']]
ROLES = [row['name'] for row in json.loads((ROOT / 'agents/manifest.json').read_text())['roles']]


class UninstallTests(unittest.TestCase):
    def run_cli(self, *args, code=0):
        result = subprocess.run([sys.executable, str(ROOT / 'scripts/harness.py'), *args],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, code, result.stdout + result.stderr)
        return result.stdout + result.stderr

    def test_scope_mode_and_surface(self):
        for scope in ('user', 'project'):
            for mode in ('copy', 'symlink'):
                with self.subTest(scope=scope, mode=mode), tempfile.TemporaryDirectory() as tmp:
                    base = Path(tmp)
                    if scope == 'user':
                        roots = [base / 'skills', base / 'codex/agents', base / 'claude/skills', base / 'claude/agents']
                        args = ['--scope', scope, '--codex-skills-root', str(roots[0]),
                                '--codex-home', str(base / 'codex'), '--claude-home', str(base / 'claude')]
                    else:
                        roots = [base / '.agents/skills', base / '.codex/agents', base / '.claude/skills', base / '.claude/agents']
                        args = ['--scope', scope, '--project-dir', tmp]
                    self.run_cli('install', *args, '--surface', 'both', '--mode', mode)
                    prompt = base / 'AGENTS.md'
                    prompt.write_text('Keep my prompt')
                    sentinel = roots[0] / 'unrelated'
                    sentinel.mkdir()
                    self.run_cli('uninstall', *args, '--surface', 'both', '--dry-run')
                    self.assertTrue((roots[0] / 'coresearch/SKILL.md').is_file())
                    self.run_cli('uninstall', *args, '--surface', 'codex')
                    for root, names, suffix in ((roots[0], SKILLS, ''), (roots[1], ROLES, '.toml')):
                        for name in names:
                            self.assertFalse((root / (name + suffix)).exists())
                            self.assertFalse((root / (name + suffix)).is_symlink())
                    self.assertTrue((roots[2] / 'coresearch/SKILL.md').is_file())
                    self.run_cli('uninstall', *args, '--surface', 'both')
                    self.run_cli('uninstall', *args, '--surface', 'both')
                    self.assertTrue(sentinel.is_dir())
                    self.assertEqual(prompt.read_text(), 'Keep my prompt')
                    self.assertTrue((ROOT / 'skills/coresearch/SKILL.md').is_file())
                    self.assertFalse(any(roots[3].iterdir()))
                    self.assertFalse(any(roots[2].iterdir()))

    def test_unrelated_entries_and_broken_owned_link(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            skills = base / '.agents/skills'
            roles = base / '.codex/agents'
            skills.mkdir(parents=True)
            roles.mkdir(parents=True)
            (skills / 'coresearch').mkdir()
            (skills / 'research-design').symlink_to(base / 'unrelated-missing')
            (skills / 'research-survey').symlink_to(ROOT / 'skills/missing-owned-target')
            role = roles / 'coresearch-reader.toml'
            role.write_text('unrelated')
            output = self.run_cli('uninstall', '--scope', 'project', '--project-dir', tmp, code=3)
            self.assertIn('unrelated', output)
            self.assertTrue((skills / 'coresearch').is_dir())
            self.assertTrue((skills / 'research-design').is_symlink())
            self.assertFalse((skills / 'research-survey').is_symlink())
            self.assertEqual(role.read_text(), 'unrelated')

    def test_source_root_refused(self):
        self.run_cli('uninstall', '--scope', 'user', '--codex-skills-root', str(ROOT / 'skills'), code=2)


if __name__ == '__main__':
    unittest.main()
