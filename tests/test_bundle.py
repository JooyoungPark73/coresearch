"""Bundle integrity and an installed, offline research-artifact workflow."""
import ast
import importlib.util
import json
import re
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

from test_install import installer
from test_sources import PDF, Response

ROOT = Path(__file__).resolve().parents[1]


class BundleTests(unittest.TestCase):
    def test_single_skill_and_routing_metadata(self):
        paths = list((ROOT / "skills").glob("*/SKILL.md"))
        self.assertEqual(paths, [ROOT / "skills/coresearch/SKILL.md"])
        metadata = paths[0].read_text().split("---", 2)[1]
        self.assertEqual(set(re.findall(r"^(\w+):", metadata, re.M)), {"name", "description"})
        self.assertIn("name: coresearch", metadata)
        self.assertLess(len(metadata.split("description:")[1].strip()), 160)
        plugin = json.loads((ROOT / ".codex-plugin/plugin.json").read_text())
        self.assertEqual(plugin["name"], "coresearch")
        self.assertTrue((ROOT / plugin["skills"]).is_dir())

    def test_markdown_local_links_exist(self):
        for file in ROOT.rglob("*.md"):
            for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", file.read_text(encoding="utf-8")):
                if "://" in target or target.startswith("#"):
                    continue
                with self.subTest(file=file, target=target):
                    self.assertTrue((file.parent / target.split("#")[0]).exists())

    def test_persistent_context_stays_small_and_no_legacy_runtime(self):
        self.assertLess(len((ROOT / "AGENTS.md").read_text().split()), 150)
        self.assertLess(len((ROOT / "skills/coresearch/SKILL.md").read_text().split()), 400)
        for path in ("harness", "bin", "templates", "skills/manifest.json", "scripts/harness.py", "scripts/install.sh"):
            self.assertFalse((ROOT / path).exists(), path)

    def test_runtime_imports_are_standard_library_only(self):
        for path in (ROOT / "scripts/coresearch.py", ROOT / "skills/coresearch/scripts/fetch_sources.py"):
            for node in ast.walk(ast.parse(path.read_text())):
                if isinstance(node, ast.Import):
                    names = [alias.name.split(".")[0] for alias in node.names]
                elif isinstance(node, ast.ImportFrom):
                    names = [node.module.split(".")[0]]
                else:
                    continue
                self.assertTrue(set(names) <= sys.stdlib_module_names, (path, names))

    def test_installed_artifact_workflow(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            project = root / "research project"
            project.mkdir()
            (project / "AGENTS.md").write_text("Local project constraints.\n")
            installer.install(root / "host skills")
            installer.initialize(project, question="Which explanation matches the evidence?")
            payload = root / "host skills/coresearch"
            spec = importlib.util.spec_from_file_location("installed_sources", payload / "scripts/fetch_sources.py")
            installed = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(installed)
            manifest = project / "sources.json"
            manifest.write_text(json.dumps([{"id": "fixture", "title": "Synthetic transport fixture", "url": "https://example.org/fixture.pdf", "access": "open"}]))
            connection = MagicMock()
            connection.getresponse.return_value = Response()
            output = project / "research/pdfs"
            with patch.object(installed, "PublicHTTPSConnection", return_value=connection):
                self.assertEqual(installed.main([str(manifest), "--output", str(output)]), 0)
            report = json.loads((output / "report.json").read_text())
            self.assertEqual(report["sources"][0]["status"], "downloaded")
            self.assertEqual((output / "fixture.pdf").read_bytes(), PDF)
            self.assertEqual((project / "AGENTS.md").read_text(), "Local project constraints.\n")
            self.assertFalse((project / "CLAUDE.md").exists())
            self.assertTrue((project / "research/brief.md").is_file())
            self.assertEqual(len(list(payload.rglob("SKILL.md"))), 1)


if __name__ == "__main__":
    unittest.main()
