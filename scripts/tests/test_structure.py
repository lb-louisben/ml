"""Regression checks for links broken by document moves and offline clones."""

import json
from pathlib import Path
import tempfile
import unittest

from scripts import check_structure


class StructureTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        for name in ("README.md",):
            self.write(name, "# Fixture\n")

    def write(self, name, content):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def test_angle_paths_and_code_examples(self):
        self.write("docs/my notes.md", "# Notes\n")
        self.write("README.md", '[notes](<docs/my notes.md>)\n[notes](docs/my%20notes.md#notes)\n```md\n[example](absent.md)\n```\n')
        errors, *_ = check_structure.check_project(self.root)
        self.assertEqual(errors, [])

    def test_broken_notebook_image_is_checked_without_execution(self):
        notebook = {"nbformat": 4, "cells": [
            {"cell_type": "markdown", "source": ["![figure](images/figure.png)\n"]},
            {"cell_type": "code", "source": ["raise RuntimeError('must not execute')"]},
        ]}
        self.write("work/lesson.ipynb", json.dumps(notebook))
        errors, *_ = check_structure.check_project(self.root)
        self.assertEqual(len(errors), 1)
        self.assertIn("[cell 1]:1: missing images/figure.png", errors[0])
        self.write("work/images/figure.png", "fixture")
        errors, *_ = check_structure.check_project(self.root)
        self.assertEqual(errors, [])

    def test_retired_material_links_fail_without_optional_exemptions(self):
        self.write("README.md", '[old notes](library/stanford-cs229-see/notes.pdf)\n[old lecture](library/nju-llm-2026/2026/lecture1.md)\n')
        errors, optional, *_ = check_structure.check_project(self.root)
        self.assertEqual(len(errors), 2)
        self.assertEqual(optional, set())


if __name__ == "__main__":
    unittest.main()
