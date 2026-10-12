"""Check maintained document links, notebook JSON and project Python syntax offline.

Run from any directory: python3 /path/to/project/scripts/check_structure.py
Downloaded materials from other schools are optional; --strict-library requires them.
Teacher source files, notebook outputs and runtime directories are not scanned.
"""

import argparse
import ast
import json
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
SKIP = {"outputs", ".ipynb_checkpoints", "__pycache__"}
LINK = re.compile(r'!?\[[^\]\n]*\]\(\s*(?:<([^>\n]+)>|([^\s)]+))(?:\s+[\"\'][^\n]*?[\"\'])?\s*\)')


def markdown_links(text):
    """Yield link line numbers and destinations, ignoring fenced code examples."""
    fence = None
    for number, line in enumerate(text.splitlines(), 1):
        marker = re.match(r"^\s*(`{3,}|~{3,})", line)
        if marker:
            token = marker.group(1)
            if fence is None:
                fence = token
            elif token[0] == fence[0] and len(token) >= len(fence):
                fence = None
            continue
        if fence is None:
            for match in LINK.finditer(line):
                yield number, match.group(1) or match.group(2)


def optional_library_file(root, target):
    try:
        parts = target.relative_to(root / "library").parts
    except ValueError:
        return False
    return len(parts) >= 2 and parts[0] != "nju-llm-2026" and parts[1:] != ("README.md",)


def check_project(root, strict_library=False):
    root = root.resolve()
    errors, optional = [], set()
    documents = [root / "README.md", root / "library/README.md"]
    documents.extend((root / "library").glob("*/README.md"))
    documents.append(root / "library/nju-llm-2026/LECTURES.md")
    notebooks = []
    for name in ("assignments", "course", "docs", "work", "scripts"):
        for path in (root / name).rglob("*"):
            if SKIP.intersection(path.relative_to(root).parts):
                continue
            # NJU a0-a5 are preserved upstream assignment packages, like the
            # teacher files in library/. Check their maintained entry page,
            # while keeping original task links and notebook contents intact.
            parts = path.relative_to(root / name).parts
            if (name == "assignments" and len(parts) > 1
                    and parts[0] == "nju-llm-2026"
                    and parts[1] in {f"a{number}" for number in range(6)}):
                continue
            if path.suffix == ".md":
                documents.append(path)
            elif path.suffix == ".ipynb":
                notebooks.append(path)

    def check_links(path, text, cell=""):
        for line, destination in markdown_links(text):
            url = urlsplit(destination)
            if url.scheme or url.netloc or not url.path:
                continue
            target = (path.parent / unquote(url.path)).resolve()
            if target.exists():
                continue
            if not strict_library and optional_library_file(root, target):
                optional.add(target.relative_to(root).as_posix())
                continue
            errors.append(f"{path.relative_to(root)}{cell}:{line}: missing {destination}")

    for path in sorted(set(documents)):
        if not path.is_file():
            errors.append(f"missing document: {path.relative_to(root)}")
            continue
        check_links(path, path.read_text(encoding="utf-8"))
    for path in sorted(notebooks):
        try:
            notebook = json.loads(path.read_text(encoding="utf-8"))
            if notebook.get("nbformat") != 4 or not isinstance(notebook.get("cells"), list):
                raise ValueError("expected nbformat 4 and cells list")
            for number, cell in enumerate(notebook["cells"], 1):
                if cell.get("cell_type") == "markdown":
                    source = cell.get("source", [])
                    check_links(path, "".join(source), f" [cell {number}]")
        except (ValueError, TypeError, AttributeError) as exc:
            errors.append(f"{path.relative_to(root)}: invalid notebook: {exc}")

    sources = sorted((root / "scripts").rglob("*.py"))
    sources += sorted((root / "docs/archive").glob("*.py"))
    sources += sorted((root / "assignments/bootcamp").rglob("*.py"))
    for path in sources:
        if SKIP.intersection(path.relative_to(root).parts):
            continue
        try:
            ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except SyntaxError as exc:
            errors.append(f"{path.relative_to(root)}:{exc.lineno}: {exc.msg}")
    json_settings = root / ".vscode/settings.json"
    if json_settings.exists():
        try:
            json.loads(json_settings.read_text(encoding="utf-8"))
        except ValueError as exc:
            errors.append(f".vscode/settings.json: {exc}")
    return errors, optional, len(set(documents)), len(notebooks), len(sources)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--strict-library", action="store_true", help="Require locally downloaded school files too")
    args = parser.parse_args()
    errors, optional, docs, notebooks, sources = check_project(ROOT, args.strict_library)
    for error in errors:
        print(f"FAIL {error}")
    if optional:
        print(f"SKIP {len(optional)} absent optional school files; download them or use --strict-library")
    print(f"{'FAIL' if errors else 'PASS'} structure: {docs} documents, {notebooks} notebooks, {sources} Python files; {len(errors)} errors")
    return bool(errors)


if __name__ == "__main__":
    raise SystemExit(main())
