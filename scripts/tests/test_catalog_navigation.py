"""Offline checks that catalog regeneration keeps independently managed courses."""

from contextlib import redirect_stdout
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from scripts import build_library_catalog, download_courses


class CatalogNavigationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.library = self.root / "library"
        (self.root / "course").mkdir()
        for name in build_library_catalog.NAMES:
            (self.library / name).mkdir(parents=True)
        self.nju = self.library / "nju-llm-2026"
        self.nju.mkdir()
        self.nju_readme = b"NJU locally maintained index\n"
        (self.nju / "README.md").write_bytes(self.nju_readme)
        (self.nju / "LECTURES.md").write_text("NJU lectures\n")
        (self.library / "manifest.json").write_text(json.dumps({
            "retrieved_at": "offline fixture", "resources": [],
        }))

    def assert_nju_navigation(self):
        catalog = (self.library / "README.md").read_text()
        self.assertIn("## 单独同步的课程", catalog)
        self.assertIn("(nju-llm-2026/README.md)", catalog)
        self.assertIn("(nju-llm-2026/LECTURES.md)", catalog)
        self.assertIn("(../work/nju-llm-2026/README.md)", catalog)
        self.assertIn("python3 scripts/sync_nju.py lectures", catalog)
        self.assertEqual((self.nju / "README.md").read_bytes(), self.nju_readme)

    def test_download_catalog_preserves_nju_without_network(self):
        def offline_result(item):
            return dict(item, status="failed", error="offline fixture")

        with patch.object(download_courses, "ROOT", self.library), \
                patch.object(download_courses, "collect", return_value=[]), \
                patch.object(download_courses, "download", side_effect=offline_result), \
                patch.object(download_courses, "fetch", side_effect=AssertionError("No network")), \
                redirect_stdout(io.StringIO()):
            download_courses.main()
        self.assert_nju_navigation()
        resources = json.loads((self.library / "manifest.json").read_text())["resources"]
        self.assertFalse(any(item["course"] == "nju-llm-2026" for item in resources))

    def test_rebuild_catalog_preserves_nju_outside_archive_totals(self):
        with patch.multiple(build_library_catalog, ROOT=self.root, LIB=self.library), \
                redirect_stdout(io.StringIO()):
            build_library_catalog.main()
        self.assert_nju_navigation()
        self.assertIn("已归档 **0 个官方文件，0.0 MiB**", (self.library / "README.md").read_text())
        self.assertEqual(json.loads((self.library / "manifest.json").read_text())["resources"], [])


if __name__ == "__main__":
    unittest.main()
