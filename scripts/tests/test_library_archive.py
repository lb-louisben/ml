"""Offline archive round trips and safety checks; GitHub CLI is always mocked."""
import copy
from contextlib import redirect_stdout
import io
import json
from pathlib import Path
import shutil
import subprocess
import tarfile
import tempfile
import unittest
from unittest.mock import patch
from zipfile import ZipFile

from scripts import library_archive as archive


class LibraryArchiveTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name) / "source"
        self.destination = Path(self.temporary.name) / "destination"
        self.course = archive.COURSES[0]
        self.cache = self.root / ".cache" / "github-archive" / archive.DEFAULT_TAG
        self.manifest_path = self.root / "config" / "archive-manifest.json"
        for course in archive.COURSES:
            folder = self.root / "library" / course
            folder.mkdir(parents=True)
            (folder / "README.md").write_text(f"Index of {course}\n")
            (folder / "notes.pdf").write_bytes(b"%PDF-offline fixture\n" + course.encode())
            (folder / "source-pages").mkdir()
            (folder / "source-pages" / "page.html").write_text("Official resource page snapshot")
        self.filename = self.course + "/12345678-hw1.zip"
        self.zip_path = self.root / "library" / self.filename
        with ZipFile(self.zip_path, "w") as bundle:
            bundle.writestr("starter/exercise.py", "answer = None\n")
            bundle.writestr("starter/README.md", "Finish the exercise\n")
        self.other_zip = self.root / "library" / archive.COURSES[1] / "abcd1234-hw2.zip"
        with ZipFile(self.other_zip, "w") as bundle:
            bundle.writestr("second.py", "other = None\n")
        (self.root / "library" / "manifest.json").write_text(json.dumps({"resources": []}))
        self.calls = []

    def build(self):
        return archive.pack(self.root)

    def download_cli(self, arguments, check=True):
        self.calls.append(arguments)
        self.assertEqual(arguments[:2], ["release", "download"])
        name = arguments[arguments.index("--pattern") + 1]
        folder = Path(arguments[arguments.index("--dir") + 1])
        shutil.copyfile(self.cache / name, folder / name)
        return subprocess.CompletedProcess(arguments, 0, "", "")

    def publish_cli(self, state):
        def run(arguments, check=True):
            self.calls.append(arguments)
            if arguments[0] == "api":
                if "/assets?" in arguments[1]:
                    return subprocess.CompletedProcess(arguments, 0, json.dumps(state["release"]["assets"]), "")
                if state["release"] is None:
                    return subprocess.CompletedProcess(arguments, 0, "[]", "")
                release = dict(state["release"], tag_name=archive.DEFAULT_TAG, id=123)
                release["assets"] = release["assets"][:30]
                return subprocess.CompletedProcess(arguments, 0, json.dumps([release]), "")
            if arguments[:2] == ["release", "create"]:
                self.assertIn("--draft", arguments)
                state["release"] = {"draft": True, "assets": []}
            elif arguments[:2] == ["release", "upload"]:
                path = Path(arguments[3])
                state["release"]["assets"].append({
                    "name": path.name, "size": path.stat().st_size,
                    "digest": "sha256:" + archive.sha256(path), "state": "uploaded",
                })
                if state.get("corrupt_upload"):
                    state["release"]["assets"][-1]["digest"] = "sha256:" + "0" * 64
            elif arguments[:2] == ["release", "edit"]:
                self.assertIn("--draft=false", arguments)
                state["release"]["draft"] = False
            else:
                self.fail("Unexpected GitHub CLI operation: " + repr(arguments))
            return subprocess.CompletedProcess(arguments, 0, "", "")
        return run

    def test_pack_full_inventory_excludes_generated_and_private_files(self):
        folder = self.root / "library" / self.course
        for relative in ["runtime/model.safetensors", "outputs/result.log", "__pycache__/a.pyc", ".env", ".DS_Store"]:
            path = folder / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(b"excluded fixture")
        nju = self.root / "library" / "nju-llm-2026"
        nju.mkdir()
        (nju / "lecture.md").write_text("already in Git")
        with patch.object(archive, "run_gh", side_effect=AssertionError("No network")):
            manifest = self.build()
            repeated = self.build()
        self.assertEqual(manifest, repeated)
        expected = {
            f"library/{course}/{filename}"
            for course in archive.COURSES
            for filename in ["README.md", "notes.pdf", "source-pages/page.html"]
        } | {"library/manifest.json", "library/" + self.filename,
             "library/" + self.other_zip.relative_to(self.root / "library").as_posix()}
        self.assertEqual({record["path"] for record in manifest["files"]}, expected)
        self.assertEqual(len(manifest["assets"]), len(archive.COURSES) + 3)
        for asset in manifest["assets"]:
            archive.verify_file(self.cache / asset["name"], asset)
        for record in manifest["files"]:
            archive.verify_file(self.root / record["path"], record)
        self.assertEqual(archive.load_manifest(self.manifest_path), manifest)

    def test_modified_unpacked_copy_blocks_pack_without_losing_work(self):
        extracted = self.zip_path.parent / "unpacked" / self.zip_path.stem
        with ZipFile(self.zip_path) as bundle:
            bundle.extractall(extracted)
        (extracted / ".archive-sha256").write_text(archive.sha256(self.zip_path) + "\n")
        self.assertEqual(archive.audit_unpacked(self.root)["changes"], [])
        exercise = extracted / "starter" / "exercise.py"
        exercise.write_text("answer = 42\n")
        with self.assertRaisesRegex(archive.ArchiveError, "Unpacked copies contain changes"):
            self.build()
        self.assertEqual(exercise.read_text(), "answer = 42\n")
        self.assertFalse(self.manifest_path.exists())

    def test_same_tag_different_source_refuses_cache_overwrite(self):
        self.build()
        original_metadata = self.manifest_path.read_bytes()
        (self.zip_path.parent / "notes.pdf").write_bytes(b"updated notes")
        with self.assertRaisesRegex(archive.ArchiveError, "mismatch"):
            self.build()
        self.assertEqual(self.manifest_path.read_bytes(), original_metadata)

    def test_restore_roundtrip_verified_assets_and_cache_reuse(self):
        manifest = self.build()
        download_cache = self.destination / ".cache" / "materials"
        with patch.object(archive, "run_gh", side_effect=self.download_cli):
            result = archive.restore(self.destination, manifest, download_cache)
            for record in manifest["files"]:
                archive.verify_file(self.destination / record["path"], record)
            first_downloads = len(self.calls)
            repeated = archive.restore(self.destination, manifest, download_cache)
        self.assertEqual(result["verified_files"], len(manifest["files"]))
        self.assertEqual(first_downloads, len(manifest["assets"]))
        self.assertEqual(len(self.calls), first_downloads)
        self.assertEqual(repeated["restored_assets"], [])

    def test_fetch_downloads_only_requested_zip_then_reuses_existing_file(self):
        manifest = self.build()
        download_cache = self.destination / ".cache" / "materials"
        with patch.object(archive, "run_gh", side_effect=self.download_cli):
            result = archive.fetch(self.destination, manifest, download_cache, self.filename)
            archive.fetch(self.destination, manifest, download_cache, self.filename)
        self.assertEqual(len(self.calls), 1)
        self.assertEqual(self.calls[0][self.calls[0].index("--pattern") + 1], result["asset"])
        self.assertEqual((self.destination / "library" / self.filename).read_bytes(), self.zip_path.read_bytes())
        self.assertFalse((self.destination / "library" / self.course / "notes.pdf").exists())
        self.assertFalse((self.destination / "library" / "manifest.json").exists())
        self.assertFalse((self.destination / "library" / archive.COURSES[1]).exists())

    def test_fetch_rejects_non_zip_and_traversal_before_download(self):
        manifest = self.build()
        with patch.object(archive, "run_gh", side_effect=AssertionError("No network")):
            for filename in [self.course + "/notes.pdf", "../outside.zip", "/absolute.zip"]:
                with self.subTest(filename=filename), self.assertRaises(archive.ArchiveError):
                    archive.fetch(self.destination, manifest, self.destination / ".cache", filename)

    def test_restore_and_fetch_preserve_modified_local_files(self):
        manifest = self.build()
        local = self.destination / "library" / self.filename
        local.parent.mkdir(parents=True)
        local.write_bytes(b"local homework")
        with patch.object(archive, "run_gh", side_effect=AssertionError("No download before conflict check")):
            with self.assertRaises(archive.ArchiveError):
                archive.fetch(self.destination, manifest, self.destination / ".cache", self.filename)
            with self.assertRaises(archive.ArchiveError):
                archive.restore(self.destination, manifest, self.destination / ".cache")
        self.assertEqual(local.read_bytes(), b"local homework")

    def test_restore_only_selected_course(self):
        manifest = self.build()
        with patch.object(archive, "run_gh", side_effect=self.download_cli):
            archive.restore(self.destination, manifest, self.destination / ".cache", [self.course])
        self.assertEqual(len(self.calls), 3)  # Selected ZIP, selected readings and source manifest.
        self.assertTrue((self.destination / "library" / self.course / "notes.pdf").exists())
        self.assertFalse((self.destination / "library" / archive.COURSES[1]).exists())

    def test_corrupt_download_never_creates_original_destination(self):
        manifest = self.build()
        def corrupt(arguments, check=True):
            folder = Path(arguments[arguments.index("--dir") + 1])
            name = arguments[arguments.index("--pattern") + 1]
            (folder / name).write_bytes(b"corrupt")
            return subprocess.CompletedProcess(arguments, 0, "", "")
        with patch.object(archive, "run_gh", side_effect=corrupt), self.assertRaises(archive.ArchiveError):
            archive.fetch(self.destination, manifest, self.destination / ".cache", self.filename)
        self.assertFalse((self.destination / "library" / self.filename).exists())

    def test_tar_rejects_traversal_absolute_links_duplicate_and_missing_members(self):
        manifest = self.build()
        records = [record for record in manifest["files"]
                   if record["course"] == self.course and record["member"] is not None]
        for case in ["traversal", "absolute", "symlink", "hardlink", "duplicate", "missing", "wrong-hash"]:
            with self.subTest(case=case):
                path = self.root / (case + ".tar.gz")
                with tarfile.open(path, "w:gz") as bundle:
                    if case != "missing":
                        record = records[0]
                        name = {"traversal": "../escape", "absolute": "/escape"}.get(case, record["member"])
                        member = tarfile.TarInfo(name)
                        payload = (self.root / record["path"]).read_bytes()
                        if case in {"symlink", "hardlink"}:
                            member.type = tarfile.SYMTYPE if case == "symlink" else tarfile.LNKTYPE
                            member.linkname = "../escape"
                            bundle.addfile(member)
                        else:
                            member.size = len(payload)
                            bundle.addfile(member, io.BytesIO(b"x" * len(payload) if case == "wrong-hash" else payload))
                            if case == "duplicate":
                                bundle.addfile(member, io.BytesIO(payload))
                with self.assertRaises(archive.ArchiveError):
                    archive.restore_tar(self.destination, path, records)
                self.assertFalse((self.destination / "library").exists())

    def test_restore_rejects_destination_symlink(self):
        manifest = self.build()
        outside = Path(self.temporary.name) / "outside"
        outside.mkdir()
        self.destination.mkdir()
        (self.destination / "library").symlink_to(outside, target_is_directory=True)
        with patch.object(archive, "run_gh", side_effect=AssertionError("No network")), self.assertRaisesRegex(archive.ArchiveError, "symlink"):
            archive.restore(self.destination, manifest, self.destination / ".cache")
        self.assertEqual(list(outside.iterdir()), [])

    def test_manifest_rejects_cross_course_and_runtime_paths(self):
        manifest = self.build()
        for path in ["../escape", "library/unknown/a.pdf", f"library/{self.course}/runtime/a.pdf"]:
            invalid = copy.deepcopy(manifest)
            invalid["files"][0]["path"] = path
            with self.subTest(path=path), self.assertRaises(archive.ArchiveError):
                archive.validate_manifest(invalid)

    def test_publish_draft_upload_verify_then_publish_without_overwriting(self):
        manifest = self.build()
        state = {"release": None}
        output = io.StringIO()
        with patch.object(archive, "run_gh", side_effect=self.publish_cli(state)), redirect_stdout(output):
            result = archive.publish(self.manifest_path, self.cache, target="commit-sha", tag=manifest["tag"])
            call_count = len(self.calls)
            archive.publish(self.manifest_path, self.cache)
        self.assertFalse(state["release"]["draft"])
        self.assertEqual(result["verified_assets"], len(manifest["assets"]) + 1)
        self.assertIn("commit-sha", next(call for call in self.calls if call[:2] == ["release", "create"]))
        self.assertFalse(any("--clobber" in call for call in self.calls))
        self.assertEqual(len(self.calls) - call_count, 4)  # Release and complete assets, twice.
        self.assertIn("[1/", output.getvalue())
        self.assertIn("Uploading", output.getvalue())

    def test_publish_remote_conflict_blocks_all_uploads_and_publication(self):
        manifest = self.build()
        asset = manifest["assets"][0]
        state = {"release": {"draft": True, "assets": [{
            "name": asset["name"], "size": asset["size"], "digest": "sha256:" + "0" * 64, "state": "uploaded",
        }]}}
        with patch.object(archive, "run_gh", side_effect=self.publish_cli(state)), self.assertRaisesRegex(archive.ArchiveError, "refusing to overwrite"):
            archive.publish(self.manifest_path, self.cache)
        self.assertTrue(state["release"]["draft"])
        self.assertTrue(all(call[0] == "api" for call in self.calls))

    def test_new_draft_waits_for_release_listing_visibility(self):
        manifest = self.build()
        expected = {"id": 123, "tag_name": manifest["tag"], "draft": True}
        with patch.object(archive, "release_info", side_effect=[None, None, expected]) as lookup, \
                patch.object(archive.time, "sleep") as sleep:
            self.assertEqual(archive.created_release_info(manifest), expected)
        self.assertEqual(lookup.call_count, 3)
        self.assertEqual([call.args[0] for call in sleep.call_args_list], [1, 2])

    def test_publish_corrupt_api_digest_stays_draft(self):
        self.build()
        state = {"release": None, "corrupt_upload": True}
        with patch.object(archive, "run_gh", side_effect=self.publish_cli(state)), redirect_stdout(io.StringIO()), self.assertRaises(archive.ArchiveError):
            archive.publish(self.manifest_path, self.cache)
        self.assertTrue(state["release"]["draft"])
        self.assertFalse(any(call[:2] == ["release", "edit"] for call in self.calls))

    def test_publish_tag_mismatch_is_offline_and_safe(self):
        self.build()
        with patch.object(archive, "run_gh", side_effect=AssertionError("No network")), self.assertRaisesRegex(archive.ArchiveError, "differs"):
            archive.publish(self.manifest_path, self.cache, tag="materials-other-snapshot")

    def test_release_assets_pagination_does_not_trust_embedded_thirty_assets(self):
        manifest = self.build()
        all_assets = [{"name": f"fixture-{number}"} for number in range(101)]
        def paginated(arguments, check=True):
            self.calls.append(arguments)
            if "/assets?" in arguments[1]:
                batch = all_assets[:100] if arguments[1].endswith("&page=1") else all_assets[100:]
                return subprocess.CompletedProcess(arguments, 0, json.dumps(batch), "")
            release = {"id": 123, "tag_name": archive.DEFAULT_TAG, "draft": True, "assets": all_assets[:30]}
            return subprocess.CompletedProcess(arguments, 0, json.dumps([release]), "")
        with patch.object(archive, "run_gh", side_effect=paginated):
            release = archive.release_info(manifest)
        self.assertEqual(release["assets"], all_assets)
        self.assertEqual(len(self.calls), 3)


if __name__ == "__main__":
    unittest.main()
