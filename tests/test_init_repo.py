import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("init_repo", ROOT / "scripts/init_repo.py")
init = importlib.util.module_from_spec(spec)
spec.loader.exec_module(init)


class InstallationTests(unittest.TestCase):
    def test_presets_initialize_and_build_offline(self):
        for topic in ("rsi", "harness"):
            with self.subTest(topic=topic), tempfile.TemporaryDirectory() as temp:
                root = Path(temp).resolve() / topic
                self.assertGreater(init.initialize(root, topic), 0)
                self.assertEqual(init.initialize(root, topic), 0)
                self.assertTrue((root / "tests/test_build.py").is_file())
                subprocess.run([sys.executable, "-B", "update.py", "--offline",
                                "--site-url", "https://example.github.io/research/"],
                               cwd=root, check=True, capture_output=True)
                self.assertTrue(ET.parse(root / "public/feed.xml").findall(".//item"))
                if topic == "rsi":
                    catalog = json.loads((root / "catalog/rsi.json").read_text())
                    self.assertEqual(len({r["group"] for r in catalog}), 11)
                    self.assertEqual(len({r["topic"] for r in catalog}), 36)

    def test_existing_documents_and_custom_topic_are_preserved(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp).resolve()
            for name in ("README.md", "AGENTS.md", ".gitignore"):
                (root / name).write_text("user content\n")
            init.initialize(root, "new-topic", "New topic", "Research scope")
            for name in ("README.md", "AGENTS.md", ".gitignore"):
                self.assertEqual((root / name).read_text(), "user content\n")
            self.assertTrue((root / "RESEARCH-FEED.md").exists())
            self.assertEqual(json.loads((root / "catalog/new-topic.json").read_text()), [])
            (root / "build.py").write_text("user modified\n")
            before = {p.relative_to(root): p.read_bytes() for p in root.rglob("*") if p.is_file()}
            with self.assertRaisesRegex(ValueError, "differs"):
                init.initialize(root, "new-topic")
            self.assertEqual(before, {p.relative_to(root): p.read_bytes() for p in root.rglob("*") if p.is_file()})

    def test_incomplete_install_is_reported_before_writes(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp).resolve()
            with patch.object(init, "TEMPLATE", init.SKILL / "missing-template"):
                with self.assertRaisesRegex(ValueError, "Incomplete skill installation"):
                    init.initialize(root / "destination", "rsi")
            self.assertFalse((root / "destination").exists())
