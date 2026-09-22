"""Migrate learning files into their canonical locations; safe to rerun."""
from pathlib import Path
from urllib.parse import urlsplit, unquote
import json
import os
import re

ROOT = Path(__file__).resolve().parents[1]
MOVES = {
    "curriculum": "course",
    "week1": "course/bootcamp/week1",
    "week2": "course/bootcamp/week2",
    "week3": "course/bootcamp/week3",
    "GIT_GUIDE.md": "docs/GIT_GUIDE.md",
    "环境使用说明.md": "docs/setup/README.md",
    "docs/环境使用说明.md": "docs/setup/README.md",
    "00_环境测试.ipynb": "docs/setup/00_环境测试.ipynb",
}
active = {old: new for old, new in MOVES.items() if (ROOT / old).exists()}
if not active:
    raise SystemExit("Layout already current; nothing changed")

# Check all destinations before any mutation.
for old, new in active.items():
    if (ROOT / new).exists():
        raise RuntimeError(f"Destination already exists: {new}")
if len(set(active.values())) != len(active):
    raise RuntimeError("Multiple sources have the same destination")


def relocated(path):
    rel = path.relative_to(ROOT).as_posix()
    for old, new in active.items():
        if rel == old or rel.startswith(old + "/"):
            return ROOT / (new + rel[len(old):])
    return path


paths = [ROOT / "README.md", ROOT / "GIT_GUIDE.md", ROOT / "环境使用说明.md"]
for folder in ("curriculum", "course", "docs", "week1", "week2", "week3"):
    paths.extend((ROOT / folder).rglob("*.md"))
updates = {}
for path in paths:
    if not path.is_file():
        continue
    content = path.read_text()

    def replace(match):
        url = match.group(2)
        if urlsplit(url).scheme or url.startswith("#"):
            return match.group(0)
        target, sep, fragment = url.partition("#")
        resolved = (path.parent / unquote(target)).resolve()
        if not resolved.is_relative_to(ROOT):
            return match.group(0)
        new = os.path.relpath(relocated(resolved), relocated(path).parent)
        return match.group(1) + new + (sep + fragment if sep else "") + ")"

    updated = re.sub(r"(\[[^\]]*\]\()([^\)]+)\)", replace, content)
    if updated != content:
        updates[relocated(path)] = updated

# Update only source strings, preserving notebook outputs, metadata and formatting.
if "week1" in active:
    for path in (ROOT / "week1").rglob("*.ipynb"):
        if "outputs" in path.parts or ".ipynb_checkpoints" in path.parts:
            continue
        content = path.read_text()
        notebook = json.loads(content)
        for cell in notebook["cells"]:
            lines = cell.get("source", [])
            if isinstance(lines, str):
                lines = [lines]
            for line in lines:
                updated = line.replace("week1/data/", "course/bootcamp/week1/data/")
                updated = updated.replace("week1/outputs", "course/bootcamp/week1/outputs")
                if updated != line:
                    content = content.replace(json.dumps(line, ensure_ascii=False),
                                              json.dumps(updated, ensure_ascii=False))
        updates[relocated(path)] = content

for old, new in active.items():
    destination = ROOT / new
    destination.parent.mkdir(parents=True, exist_ok=True)
    (ROOT / old).rename(destination)
    print(f"Moved {old} -> {new}")
for path, content in updates.items():
    path.write_text(content)
print(f"Updated {len(updates)} documents/notebooks")
