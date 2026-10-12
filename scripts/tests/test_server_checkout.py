"""Offline checks for homework scope and full-checkout protection."""

from contextlib import redirect_stderr, redirect_stdout
import io
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from scripts import server_checkout as checkout


PROJECT_ROOT = Path(__file__).resolve().parents[2]
CONFIG_DATA = json.loads((PROJECT_ROOT / checkout.CONFIG_PATH).read_text(encoding="utf-8"))


class FakeGit:
    """Record subprocess calls; never invoke Git or a network."""

    def __init__(self, root, sparse=False, status="", inside=True):
        self.root = root
        self.sparse = sparse
        self.status = status
        self.inside = inside
        self.calls = []

    def __call__(self, command, **kwargs):
        self.calls.append((command, kwargs))
        self.assert_safe_arguments(command, kwargs)
        args = command[3:]
        code, output = 0, ""
        if args == ["rev-parse", "--is-inside-work-tree"]:
            code, output = (0, "true\n") if self.inside else (128, "")
        elif args == ["rev-parse", "--show-toplevel"]:
            output = str(self.root) + "\n"
        elif args == ["rev-parse", "--git-path", "index"]:
            output = str(self.root / ".git/index") + "\n"
        elif args == ["config", "--bool", "core.sparseCheckout"]:
            code, output = (0, "true\n") if self.sparse else (1, "")
        elif args == ["status", "--porcelain=v1", "--untracked-files=all"]:
            output = self.status
        elif args == ["show", "HEAD:" + checkout.CONFIG_PATH]:
            output = json.dumps(CONFIG_DATA)
        elif args[:2] not in (["sparse-checkout", "set"], ["read-tree", "-mu"],
                             ["config", "--replace-all"], ["config", "--add"]):
            raise AssertionError("Unexpected Git command: {}".format(args))
        return subprocess.CompletedProcess(command, code, output, "fixture error" if code else "")

    @staticmethod
    def assert_safe_arguments(command, kwargs):
        if command[:2] != ["git", "-C"] or kwargs.get("shell"):
            raise AssertionError("Commands must use Git directly, without a shell")
        if not kwargs.get("text") or kwargs.get("check") is not False:
            raise AssertionError("Unexpected subprocess configuration")

    def mutating_calls(self):
        return [call for call in self.calls
                if call[0][3:5] in (["sparse-checkout", "set"],
                                   ["read-tree", "-mu"],
                                   ["config", "--replace-all"], ["config", "--add"])]


class CheckoutTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name).resolve()
        (self.root / ".git").mkdir()
        self.catalog = checkout.parse_catalog(CONFIG_DATA)

    def test_catalog_profiles_select_only_corresponding_homework(self):
        expected = {"all-exercises", "bootcamp", "week1", "week2", "week3", "core", "nju"}
        expected.update("core-a{:02}".format(number) for number in range(1, 9))
        expected.update("nju-a{}".format(number) for number in range(6))
        self.assertEqual(set(self.catalog.profiles), expected)
        for profile in self.catalog.profiles.values():
            for path in profile.paths:
                self.assertTrue(path.startswith(("assignments/", "work/")))
                self.assertNotIn("lecture", path)
                self.assertNotIn("library", path)
                if path.startswith("work/"):
                    self.assertEqual(len(path.split("/")), 3)
        week = checkout.build_patterns(self.catalog, ["week1"])
        self.assertIn("/assignments/bootcamp/week1/", week)
        self.assertNotIn("/assignments/bootcamp/week2/", week)
        self.assertNotIn("/assignments/core/A01/", week)
        nju = checkout.build_patterns(self.catalog, ["nju-a0"])
        self.assertIn("/work/nju-llm-2026/a0/", nju)
        self.assertIn("/assignments/nju-llm-2026/SOURCES.json", nju)
        self.assertNotIn("/work/nju-llm-2026/", nju)
        self.assertNotIn("/assignments/nju-llm-2026/a1/", nju)

    def test_patterns_are_literal_files_and_directories_without_sibling_expansion(self):
        patterns = checkout.build_patterns(self.catalog, ["core-a01", "nju-a0", "core-a01"])
        self.assertEqual(len(patterns), len(set(patterns)))
        self.assertIn("/.gitignore", patterns)
        self.assertIn("/docs/SERVER_GUIDE.md", patterns)
        self.assertNotIn("/docs/", patterns)
        self.assertIn("/work/assignments/A01/", patterns)
        self.assertNotIn("/work/assignments/", patterns)
        self.assertNotIn("/assignments/core/A02/", patterns)
        self.assertTrue(all(pattern.startswith("/") for pattern in patterns))

    def test_invalid_paths_and_unknown_profiles_fail_before_git_writes(self):
        invalid = ("../README.md", "/tmp/README.md", "a/../b", "a/./b", "a//b",
                   "C:/tmp/file", r"C:\tmp\file", "a/*.pdf", "a/?.pdf", "a/[ab]",
                   ".git/config", "a\n/library/", "a/", " README.md")
        for path in invalid:
            with self.subTest(path=path), self.assertRaises(checkout.CheckoutError):
                checkout.validate_path(path)
        fake = FakeGit(self.root, sparse=True)
        with patch.object(checkout.subprocess, "run", fake):
            with self.assertRaisesRegex(checkout.CheckoutError, "未知 profile"):
                checkout.apply_profile(self.root, self.catalog, ["missing"])
        self.assertEqual(fake.calls, [])

    def test_catalog_rejects_whole_personal_course_or_library_directories(self):
        for path in ("work/nju-llm-2026", "library/nju-llm-2026", "course"):
            data = {"version": 1, "base_files": [".gitignore"], "profiles": {
                "all-exercises": {"paths": [path]}}}
            with self.subTest(path=path), self.assertRaises(checkout.CheckoutError):
                checkout.parse_catalog(data)

    def test_list_and_dry_run_have_no_side_effects_even_in_full_checkout(self):
        (self.root / "README.md").write_text("local full checkout")
        fake = FakeGit(self.root, status=" M README.md\n")
        for arguments in (["list"], ["set", "week1", "--add", "nju-a0", "--dry-run"]):
            output = io.StringIO()
            with patch.object(checkout.subprocess, "run", fake), redirect_stdout(output):
                result = checkout.main(["--repo-root", str(self.root), *arguments])
            self.assertEqual(result, 0)
            self.assertIn("all-exercises" if arguments == ["list"] else "/assignments/bootcamp/week1/",
                          output.getvalue())
        self.assertEqual(fake.mutating_calls(), [])
        self.assertEqual((self.root / "README.md").read_text(), "local full checkout")

    def test_full_local_checkout_is_refused_clean_or_dirty(self):
        (self.root / "README.md").write_text("personal work")
        for status in ("", " M README.md\n", "?? personal.py\n"):
            fake = FakeGit(self.root, status=status)
            with patch.object(checkout.subprocess, "run", fake):
                with self.assertRaisesRegex(checkout.CheckoutError, "不要在主项目执行 set"):
                    checkout.apply_profile(self.root, self.catalog, ["week1"])
            self.assertEqual(fake.mutating_calls(), [])
        self.assertEqual((self.root / "README.md").read_text(), "personal work")

    def test_empty_but_previously_checked_out_repository_is_also_refused(self):
        (self.root / ".git/index").write_bytes(b"existing index")
        fake = FakeGit(self.root, status=" D README.md\n")
        with patch.object(checkout.subprocess, "run", fake):
            with self.assertRaisesRegex(checkout.CheckoutError, "本地修改"):
                checkout.apply_profile(self.root, self.catalog, ["week1"])
        self.assertEqual(fake.mutating_calls(), [])

    def test_fresh_no_checkout_clone_bootstraps_config_and_uses_non_cone(self):
        fake = FakeGit(self.root)
        output = io.StringIO()
        with patch.object(checkout.subprocess, "run", fake), redirect_stdout(output):
            result = checkout.main(["set", "week1", "--add", "nju-a0", "--repo-root", str(self.root)])
        self.assertEqual(result, 0)
        self.assertTrue(any(command[3:] == ["show", "HEAD:" + checkout.CONFIG_PATH]
                            for command, _ in fake.calls))
        writes = fake.mutating_calls()
        self.assertEqual(writes[0][0][3:], ["sparse-checkout", "set", "--no-cone", "--stdin"])
        stdin = writes[0][1]["input"]
        self.assertIn("/assignments/bootcamp/week1/\n", stdin)
        self.assertIn("/assignments/nju-llm-2026/a0/\n", stdin)
        self.assertIn("/.gitignore\n", stdin)
        self.assertNotIn("/library/", stdin)
        self.assertNotIn("/work/nju-llm-2026/\n", stdin)
        self.assertEqual(writes[1][0][3:], ["read-tree", "-mu", "HEAD"])
        self.assertEqual(writes[2][0][3:], ["config", "--replace-all", checkout.PROFILE_CONFIG_KEY, "week1"])
        self.assertEqual(writes[3][0][3:], ["config", "--add", checkout.PROFILE_CONFIG_KEY, "nju-a0"])

    def test_existing_sparse_checkout_can_switch_profiles_and_default_is_all(self):
        (self.root / "README.md").write_text("sparse checkout")
        fake = FakeGit(self.root, sparse=True)
        with patch.object(checkout.subprocess, "run", fake), redirect_stdout(io.StringIO()):
            self.assertEqual(checkout.main(["--repo-root", str(self.root), "set"]), 0)
        self.assertEqual(fake.mutating_calls()[1][0][-1], "all-exercises")
        self.assertNotIn("/library/", fake.mutating_calls()[0][1]["input"])
        self.assertFalse(any(command[3] == "read-tree" for command, _ in fake.calls))

    def test_retry_after_patterns_were_written_still_bootstraps_missing_index(self):
        fake = FakeGit(self.root, sparse=True)
        with patch.object(checkout.subprocess, "run", fake):
            checkout.apply_profile(self.root, self.catalog, ["nju-a0"])
        self.assertEqual(fake.mutating_calls()[1][0][3:], ["read-tree", "-mu", "HEAD"])

    def test_real_no_checkout_clone_materializes_only_selected_files_and_stays_clean(self):
        # All Git operations use temporary local repositories. No remote, main
        # checkout, model downloads, or network connection is involved.
        source = self.root / "source"
        source.mkdir()

        def run_git(repo, *arguments):
            return subprocess.run(["git", "-C", str(repo), *arguments],
                                  text=True, capture_output=True, check=True)

        run_git(source, "init", "--quiet")
        fixtures = {
            "README.md": "fixture\n",
            ".gitignore": "__pycache__/\n",
            checkout.CONFIG_PATH: json.dumps(CONFIG_DATA),
            "assignments/nju-llm-2026/a0/train.py": "print('exercise')\n",
            "assignments/nju-llm-2026/SOURCES.json": "{}\n",
            "work/nju-llm-2026/a0/personal.py": "print('personal')\n",
            "work/nju-llm-2026/lecture1.md": "personal lecture notes\n",
            "assignments/nju-llm-2026/a1/train.py": "other exercise\n",
            "assignments/bootcamp/week1/train.py": "bootcamp exercise\n",
            "work/bootcamp/week1/personal.py": "bootcamp implementation\n",
            "library/nju-llm-2026/lecture.pdf": "lecture fixture\n",
            "library/reference-book.pdf": "reference book fixture\n",
        }
        for name, content in fixtures.items():
            path = source / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
        run_git(source, "add", ".")
        run_git(source, "-c", "user.name=Checkout fixture", "-c",
                "user.email=fixture@example.invalid", "commit", "--quiet", "-m", "Fixture")
        clone = self.root / "clone"
        run_git(self.root, "clone", "--quiet", "--no-checkout", str(source), str(clone))
        self.assertFalse((clone / ".git/index").exists())
        self.assertEqual({path.name for path in clone.iterdir()}, {".git"})

        with redirect_stdout(io.StringIO()):
            result = checkout.main(["--repo-root", str(clone), "set", "nju-a0"])
        self.assertEqual(result, 0)
        self.assertTrue((clone / "assignments/nju-llm-2026/a0/train.py").is_file())
        self.assertTrue((clone / "work/nju-llm-2026/a0/personal.py").is_file())
        self.assertTrue((clone / "assignments/nju-llm-2026/SOURCES.json").is_file())
        self.assertTrue((clone / "README.md").is_file())
        self.assertTrue((clone / ".gitignore").is_file())
        self.assertFalse((clone / "library").exists())
        self.assertFalse((clone / "work/nju-llm-2026/lecture1.md").exists())
        self.assertFalse((clone / "assignments/nju-llm-2026/a1").exists())
        self.assertEqual(run_git(clone, "status", "--porcelain=v1").stdout, "")
        self.assertEqual(run_git(clone, "config", "--get-all", checkout.PROFILE_CONFIG_KEY).stdout,
                         "nju-a0\n")

        # Switching an initialized sparse checkout must retain local changes
        # in an exercise that remains selected; read-tree would overwrite it.
        personal = clone / "work/nju-llm-2026/a0/personal.py"
        personal.write_text("my unfinished homework\n", encoding="utf-8")
        with redirect_stdout(io.StringIO()):
            self.assertEqual(checkout.main(["--repo-root", str(clone), "set", "nju-a0",
                                           "--add", "week1"]), 0)
        self.assertEqual(personal.read_text(encoding="utf-8"), "my unfinished homework\n")
        self.assertTrue((clone / "assignments/bootcamp/week1/train.py").is_file())
        self.assertTrue((clone / "work/bootcamp/week1/personal.py").is_file())
        self.assertFalse((clone / "library").exists())

    def test_non_repository_is_refused_before_reading_config_or_writing(self):
        fake = FakeGit(self.root, inside=False)
        errors = io.StringIO()
        with patch.object(checkout.subprocess, "run", fake), redirect_stderr(errors):
            result = checkout.main(["--repo-root", str(self.root), "set", "week1"])
        self.assertEqual(result, 2)
        self.assertIn("Git 工作树", errors.getvalue())
        self.assertEqual(len(fake.calls), 1)
        self.assertEqual(fake.mutating_calls(), [])


if __name__ == "__main__":
    unittest.main()
