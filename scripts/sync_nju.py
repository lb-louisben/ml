#!/usr/bin/env python3
"""Update 2026 NJU lectures; keep the one-time assignment archive unchanged."""

import argparse
import base64
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path, PurePosixPath
import posixpath
import re
import subprocess
import tempfile
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "library/nju-llm-2026"
REPO = "https://github.com/NJUDeepEngine/llm-course-lecture"
API = "https://api.github.com/repos/NJUDeepEngine/llm-course-lecture"


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def blob_sha(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def local_path(base, relative):
    path = PurePosixPath(relative)
    if path.is_absolute() or ".." in path.parts or not path.parts:
        raise ValueError(f"Unsafe source path: {relative}")
    target = base / path
    if not target.resolve().is_relative_to(base.resolve()):
        raise ValueError(f"Path escapes destination: {relative}")
    return target


class Fetcher:
    def __init__(self, direct=False):
        self.direct = direct

    def __call__(self, url):
        command = ["curl", "--fail", "--location", "--silent", "--show-error",
                   "--connect-timeout", "15", "--max-time", "180", "--retry", "2",
                   "--proto", "=https", "--proto-redir", "=https",
                   "--user-agent", "NJU-course-personal-sync"]
        if self.direct:
            command += ["--noproxy", "*"]
        return subprocess.check_output(command + [url])


def publish(folder, files, metadata, manifest_name="manifest.json"):
    """Preflight every replacement; interrupted downloads never touch local files."""
    manifest = folder / manifest_name
    previous = json.loads(manifest.read_text()) if manifest.exists() else {}
    known = {r["file"]: r["sha256"] for r in previous.get("resources", [])}
    conflicts = []
    for name, data in files.items():
        target = local_path(folder, name)
        if target.exists():
            actual = sha256(target.read_bytes())
            if actual != sha256(data) and actual != known.get(name):
                conflicts.append(str(target.relative_to(ROOT)))
    if conflicts:
        raise RuntimeError("本地文件已修改，同步未写入。请先备份并移走以下文件到 work/（不是 cd work），再从项目根目录重试：\n" +
                           "\n".join(conflicts))
    # Stage all files on the same filesystem, then atomically replace each file.
    cache = ROOT / ".cache/nju-sync"
    cache.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=cache) as temp:
        staged = Path(temp)
        for name, data in files.items():
            path = local_path(staged, name)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
        stage_manifest = staged / manifest_name
        stage_manifest.write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n")
        folder.mkdir(parents=True, exist_ok=True)
        changed = 0
        for name, data in files.items():
            path = local_path(folder, name)
            if path.exists() and path.read_bytes() == data:
                continue
            path.parent.mkdir(parents=True, exist_ok=True)
            local_path(staged, name).replace(path)
            changed += 1
        stage_manifest.replace(manifest)
    print(f"{folder.relative_to(ROOT)}: {len(files)} files, {changed} updated", flush=True)


def local_images(name, data):
    if name.endswith(".ipynb"):
        notebook = json.loads(data)
        content = "\n".join("".join(cell["source"]) for cell in notebook["cells"]
                            if cell["cell_type"] == "markdown")
    elif name.endswith(".md"):
        content = data.decode("utf-8")
    else:
        return set()
    content = re.sub(r"<!--.*?-->", "", content, flags=re.S)
    refs = re.findall(r'''!\[[^\]]*\]\(([^)]+)\)|<img[^>]*src=["']([^"']+)''', content)
    paths = set()
    for pair in refs:
        ref = next(value for value in pair if value).strip()
        if urlsplit(ref).scheme or ref.startswith(("//", "#")):
            continue
        paths.add(posixpath.normpath(posixpath.join(posixpath.dirname(name), ref)))
    return paths


def sync_lectures(fetch):
    ref = json.loads(fetch(API + "/git/ref/heads/main"))
    commit = ref["object"]["sha"]
    tree = json.loads(fetch(API + f"/git/trees/{commit}?recursive=1"))
    if tree.get("truncated"):
        raise RuntimeError("GitHub 文件清单被截断，未进行同步。")
    entries = {item["path"]: item for item in tree["tree"] if item["type"] == "blob"}
    names = sorted(name for name in entries if name.startswith("2026/"))
    if not names:
        raise RuntimeError("官方仓库未返回 2026 年文件，未进行同步。")

    def retrieve(name):
        item = entries[name]
        if item.get("mode") == "120000":
            raise ValueError(f"Unsupported upstream symlink: {name}")
        target = local_path(DEST, name)
        if target.is_file() and blob_sha(target.read_bytes()) == item["sha"]:
            return name, target.read_bytes()
        response = json.loads(fetch(API + "/git/blobs/" + item["sha"]))
        if response.get("encoding") != "base64":
            raise ValueError(f"Unexpected GitHub encoding: {name}")
        data = base64.b64decode(response["content"])
        if blob_sha(data) != item["sha"]:
            raise ValueError(f"Git blob checksum mismatch: {name}")
        return name, data

    with ThreadPoolExecutor(max_workers=4) as pool:
        files = dict(pool.map(retrieve, names))
        images = set().union(*(local_images(name, data) for name, data in files.items()))
        missing = images - entries.keys()
        if missing:
            raise RuntimeError(f"官方讲义引用了不存在的配图：{sorted(missing)}")
        files.update(pool.map(retrieve, sorted(images - files.keys())))
    resources = [dict(file=name, url=f"{REPO}/blob/{commit}/{name}",
                      bytes=len(data), sha256=sha256(data), git_blob_sha=entries[name]["sha"])
                 for name, data in sorted(files.items())]
    index = ["# 当前同步的 2026 年讲义", "", "[课程入口](README.md)", "",
             f"来源快照：[{commit[:12]}]({REPO}/tree/{commit}/2026)", ""]
    index += [f"- [{name}](<{name}>)" for name in names]
    files["LECTURES.md"] = ("\n".join(index) + "\n").encode()
    resources.append(dict(file="LECTURES.md", sha256=sha256(files["LECTURES.md"]),
                          bytes=len(files["LECTURES.md"]), generated=True))
    # Add new upstream files only. Existing teaching files may contain personal work.
    existing = {name for name in files if local_path(DEST, name).exists()}
    additions = {name: data for name, data in files.items() if name not in existing}
    # Refresh the generated navigation only while it still matches our last version.
    previous = json.loads((DEST / "manifest.json").read_text()) if (DEST / "manifest.json").exists() else {}
    known = {r["file"]: r["sha256"] for r in previous.get("resources", [])}
    index = DEST / "LECTURES.md"
    if index.exists() and sha256(index.read_bytes()) == known.get("LECTURES.md"):
        additions["LECTURES.md"] = files["LECTURES.md"]
    elif index.exists():
        for record in resources:
            if record["file"] == "LECTURES.md":
                record.update(sha256=known.get("LECTURES.md", "user-managed"))
    publish(DEST, additions, dict(retrieved_at=datetime.now(timezone.utc).isoformat(),
                                  repository=REPO, commit=commit, tree=tree["sha"],
                                  policy="add-only; preserve existing course files", resources=resources))
    print(f"增量同步：保留 {len(existing - {'LECTURES.md'})} 个已有资料文件，仅补充新增文件。")


def sync_assignments(fetch):
    """Compatibility command: assignments are a fixed, versioned snapshot."""
    manifest = ROOT / "assignments/nju-llm-2026/SOURCES.json"
    if not manifest.is_file():
        raise RuntimeError("作业固定快照缺失，请从自己的 ML 仓库恢复 assignments 目录。")
    print("作业已一次性归档：跳过联网与更新。见 library/nju-llm-2026/README.md#作业")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", choices=("lectures", "assignments", "all"))
    parser.add_argument("--direct", action="store_true", help="直接联网，绕过本机代理")
    args = parser.parse_args()
    fetch = Fetcher(args.direct)
    try:
        if args.source in ("lectures", "all"):
            sync_lectures(fetch)
        if args.source in ("assignments", "all"):
            sync_assignments(fetch)
    except subprocess.SubprocessError as exc:
        parser.exit(1, f"下载失败：{exc}\n若本机代理不可用，可添加 --direct 重试。\n")
    except (ValueError, RuntimeError, OSError) as exc:
        parser.exit(1, f"同步失败：{exc}\n")


if __name__ == "__main__":
    main()
