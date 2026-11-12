# -*- coding: utf-8 -*-
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "build_zips.py"
sys.path.insert(0, str(SCRIPT.parent))

import build_zips as B  # noqa: E402


class BuildZips(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.out = Path(tempfile.mkdtemp())
        cls.built = B.build(ROOT, cls.out)

    def names(self, name):
        with zipfile.ZipFile(self.out / name) as z:
            return set(z.namelist())

    def test_builds_skill_and_plugin_zip_per_plugin(self):
        self.assertEqual(sorted(p.name for p in self.built), [
            "stakeholder-brief-plugin.zip", "stakeholder-brief-skill.zip",
            "stop-slop-vi-plugin.zip", "stop-slop-vi-skill.zip"])

    def test_skill_zip_has_skill_folder_at_root(self):
        names = self.names("stop-slop-vi-skill.zip")
        self.assertIn("stop-slop-vi/SKILL.md", names)
        self.assertIn("stop-slop-vi/references/vi-slop-patterns.md", names)
        self.assertIn("stop-slop-vi/scripts/slop_scan.py", names)
        self.assertTrue(all(n.startswith("stop-slop-vi/") for n in names))

    def test_plugin_zip_has_manifest_at_root(self):
        names = self.names("stop-slop-vi-plugin.zip")
        self.assertIn(".claude-plugin/plugin.json", names)
        self.assertIn("skills/stop-slop-vi/SKILL.md", names)
        self.assertIn("hooks/hooks.json", names)

    def test_no_cache_files(self):
        for p in self.built:
            with zipfile.ZipFile(p) as z:
                self.assertFalse([n for n in z.namelist() if "__pycache__" in n or n.endswith(".pyc")], p.name)

    def test_deterministic(self):
        again = Path(tempfile.mkdtemp())
        B.build(ROOT, again)
        for p in self.built:
            self.assertEqual(p.read_bytes(), (again / p.name).read_bytes(), p.name)

    def test_cli(self):
        out = Path(tempfile.mkdtemp())
        r = subprocess.run([sys.executable, str(SCRIPT), "--out", str(out)], capture_output=True)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(len(list(out.glob("*.zip"))), 4)


if __name__ == "__main__":
    unittest.main()
