"""Installer contracts, including writes through the real command-line entry point."""
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("installer", ROOT / "scripts/coresearch.py")
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)


class InstallTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.skills = self.root / "space ü" / "skills"

    def cli(self, *args):
        return subprocess.run([sys.executable, "-B", str(ROOT / "scripts/coresearch.py"), *map(str, args)],
                              cwd=self.root, input="", capture_output=True, text=True, timeout=10)

    def test_copy_install_is_complete_and_idempotent(self):
        result = self.cli("install", "--to", self.skills)
        self.assertEqual(result.returncode, 0, result.stderr)
        copied = self.skills / "coresearch"
        self.assertTrue(installer.identical(installer.payload(installer.SKILL), installer.payload(copied)))
        result = self.cli("install", "--to", self.skills)
        self.assertIn("Already installed", result.stdout)
        self.assertEqual(result.returncode, 0)

    def test_link_install_and_same_link_are_idempotent(self):
        installer.install(self.skills, link=True)
        destination = self.skills / "coresearch"
        self.assertTrue(destination.is_symlink())
        self.assertEqual(destination.resolve(), installer.SKILL)
        self.assertIn("Already linked", installer.install(self.skills, link=True))

    def test_foreign_destination_is_preserved(self):
        destination = self.skills / "coresearch"
        destination.mkdir(parents=True)
        (destination / "SKILL.md").write_text("User skill", encoding="utf-8")
        result = self.cli("install", "--to", self.skills)
        self.assertEqual(result.returncode, 2)
        self.assertIn("preserving", result.stderr)
        self.assertEqual((destination / "SKILL.md").read_text(), "User skill")

    def test_modified_copy_is_preserved(self):
        installer.install(self.skills)
        path = self.skills / "coresearch/references/analysis.md"
        path.write_text("local edits")
        with self.assertRaises(FileExistsError):
            installer.install(self.skills)
        self.assertEqual(path.read_text(), "local edits")

    def test_broken_link_is_preserved(self):
        self.skills.mkdir(parents=True)
        destination = self.skills / "coresearch"
        destination.symlink_to(self.root / "missing")
        with self.assertRaises(FileExistsError):
            installer.install(self.skills, link=True)
        self.assertTrue(destination.is_symlink())

    def test_copy_does_not_replace_a_link(self):
        installer.install(self.skills, link=True)
        with self.assertRaises(FileExistsError):
            installer.install(self.skills)

    def test_install_dry_run_has_no_writes(self):
        result = self.cli("install", "--to", self.skills, "--dry-run")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(self.skills.parent.exists())

    def test_recursive_destination_rejected(self):
        with self.assertRaises(ValueError):
            installer.install(installer.SKILL / "nested")
        with self.assertRaises(ValueError):
            installer.install(installer.SKILL.parent)

    def test_payload_rejects_symlinks(self):
        root = self.root / "source"
        root.mkdir()
        (root / "SKILL.md").write_text("skill")
        (root / "foreign").symlink_to(self.root / "missing")
        with self.assertRaises(ValueError):
            installer.payload(root)

    def test_copy_failure_cleans_partial_install(self):
        with patch.object(installer.shutil, "copy2", side_effect=OSError("disk full")):
            with self.assertRaises(OSError):
                installer.install(self.skills)
        self.assertFalse((self.skills / "coresearch").exists())

    def test_skill_metadata_published_last(self):
        original = installer.shutil.copy2
        copied = []

        def copy(source, target):
            copied.append(Path(target).name)
            return original(source, target)

        with patch.object(installer.shutil, "copy2", side_effect=copy):
            installer.install(self.skills)
        self.assertEqual(copied[-1], "SKILL.md")

    def test_init_is_noninteractive_and_preserves_host_prompts(self):
        for name in ("AGENTS.md", "CLAUDE.md"):
            (self.root / name).write_text(f"keep {name}\n")
        result = self.cli("init", self.root, "--question", "Does this control explain the effect?")
        self.assertEqual(result.returncode, 0, result.stderr)
        brief = self.root / "research/brief.md"
        self.assertIn("Does this control", brief.read_text())
        for name in ("AGENTS.md", "CLAUDE.md"):
            self.assertEqual((self.root / name).read_text(), f"keep {name}\n")
        before = brief.read_bytes()
        result = self.cli("init", self.root, "--question", "Different")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(brief.read_bytes(), before)

    def test_init_dry_run_is_write_free(self):
        result = self.cli("init", self.root, "--dry-run")
        self.assertEqual(result.returncode, 0)
        self.assertFalse((self.root / "research").exists())

    def test_init_does_not_write_through_research_directory_link(self):
        outside = self.root / "outside"
        outside.mkdir()
        (self.root / "research").symlink_to(outside, target_is_directory=True)
        with self.assertRaises(ValueError):
            installer.initialize(self.root)
        self.assertEqual(list(outside.iterdir()), [])

    def test_init_preserves_broken_brief_link(self):
        (self.root / "research").mkdir()
        brief = self.root / "research/brief.md"
        brief.symlink_to(self.root / "missing")
        self.assertIn("Preserved", installer.initialize(self.root))
        self.assertTrue(brief.is_symlink())

    def test_installed_script_runs_without_checkout_context(self):
        installer.install(self.skills)
        script = self.skills / "coresearch/scripts/fetch_sources.py"
        manifest = self.root / "sources.json"
        manifest.write_text(json.dumps([{"id": "x", "title": "Example", "url": "https://example.org/x.pdf", "access": "open"}]))
        output = self.root / "absent"
        result = subprocess.run([sys.executable, "-B", str(script), str(manifest), "--output", str(output), "--dry-run"],
                                cwd=self.root, capture_output=True, text=True, timeout=10)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main()
