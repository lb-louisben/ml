"""Offline regression checks for source isolation and local-file protection."""

import base64
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import sync_nju as sync


class SyncTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.dest = self.root / "library/nju-llm-2026"
        self.patches = patch.multiple(sync, ROOT=self.root, DEST=self.dest)
        self.patches.start()
        self.addCleanup(self.patches.stop)

    def test_local_edits_block_entire_publish(self):
        self.dest.mkdir(parents=True)
        (self.dest / "notes.md").write_bytes(b"my notes")
        metadata = {"resources": [{"file": "notes.md", "sha256": sync.sha256(b"original")}]}
        (self.dest / "manifest.json").write_text(json.dumps(metadata))
        before = (self.dest / "manifest.json").read_bytes()
        with self.assertRaisesRegex(RuntimeError, "本地文件已修改"):
            sync.publish(self.dest, {"new.md": b"new", "notes.md": b"teacher update"}, {})
        self.assertFalse((self.dest / "new.md").exists())
        self.assertEqual((self.dest / "notes.md").read_bytes(), b"my notes")
        self.assertEqual((self.dest / "manifest.json").read_bytes(), before)

    def test_lectures_scope_cache_and_download_failure(self):
        sources = {"2026/lecture1.md": b"![figure](../images/2026/a.png)",
                   "images/2026/a.png": b"image", "2025/lecture1.md": b"old course"}
        entries = [dict(path=name, sha=sync.blob_sha(data), type="blob", mode="100644")
                   for name, data in sources.items()]
        calls = []

        def fetch(url):
            calls.append(url)
            if "/git/ref/" in url:
                return json.dumps({"object": {"sha": "commit-snapshot"}}).encode()
            if "/git/trees/" in url:
                return json.dumps(dict(sha="snapshot", tree=entries)).encode()
            for data in sources.values():
                if url.endswith(sync.blob_sha(data)):
                    return json.dumps(dict(encoding="base64", content=base64.b64encode(data).decode())).encode()
            raise AssertionError(url)

        assignment = self.dest / "assignments/personal.txt"
        assignment.parent.mkdir(parents=True)
        assignment.write_bytes(b"untouched")
        sync.sync_lectures(fetch)
        self.assertFalse((self.dest / "2025").exists())
        self.assertEqual(assignment.read_bytes(), b"untouched")
        self.assertEqual((self.dest / "images/2026/a.png").read_bytes(), b"image")
        calls.clear()
        sync.sync_lectures(fetch)
        self.assertEqual(len(calls), 2, "Unchanged files only need ref and tree requests")
        manifest = json.loads((self.dest / "manifest.json").read_text())
        self.assertEqual(manifest["commit"], "commit-snapshot")
        self.assertEqual(manifest["tree"], "snapshot")
        self.assertIn("/blob/commit-snapshot/", manifest["resources"][0]["url"])
        before = (self.dest / "manifest.json").read_bytes()
        entries.append(dict(path="2026/new.md", sha="unavailable", type="blob", mode="100644"))

        def failing(url):
            if url.endswith("unavailable"):
                raise OSError("network failure")
            return fetch(url)

        with self.assertRaises(OSError):
            sync.sync_lectures(failing)
        self.assertEqual((self.dest / "manifest.json").read_bytes(), before)
        self.assertFalse((self.dest / "2026/new.md").exists())

    def test_assignments_never_fetch_or_write(self):
        folder = self.dest / "assignments"
        folder.mkdir(parents=True)
        marker = folder / "repository-manifest.json"
        marker.write_bytes(b'{"fixed": true}')
        def forbidden_fetch(url):
            raise AssertionError("Assignment command must not access network")
        sync.sync_assignments(forbidden_fetch)
        self.assertEqual(marker.read_bytes(), b'{"fixed": true}')
        marker.unlink()
        with self.assertRaisesRegex(RuntimeError, "固定快照缺失"):
            sync.sync_assignments(forbidden_fetch)

    def test_paths_cannot_escape_destination(self):
        for name in ("../personal.md", "/tmp/personal.md"):
            with self.assertRaises(ValueError):
                sync.local_path(self.dest, name)


if __name__ == "__main__":
    unittest.main()
