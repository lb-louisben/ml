#!/usr/bin/env python3
"""Select homework for a server using non-cone Git sparse checkout.

Run ``list`` in any checkout. Run ``set`` only in a fresh ``--no-checkout``
clone or an existing sparse checkout; a full local checkout is protected.
This changes the working tree only. Clone with ``--filter=blob:none`` and
``--depth 1`` to also reduce downloads and history.
"""

import argparse
from dataclasses import dataclass
import json
from pathlib import Path
import re
import subprocess
import sys
from typing import Dict, Iterable, List, Optional, Tuple


CONFIG_PATH = "config/checkout-profiles.json"
PROFILE_CONFIG_KEY = "codex.serverProfile"


class CheckoutError(RuntimeError):
    """A configuration or repository cannot safely be used."""


@dataclass(frozen=True)
class Profile:
    description: str
    paths: Tuple[str, ...]
    files: Tuple[str, ...]


@dataclass(frozen=True)
class Catalog:
    base_files: Tuple[str, ...]
    profiles: Dict[str, Profile]


def git(repo: Path, *args: str, input_text: Optional[str] = None,
        check: bool = True) -> subprocess.CompletedProcess:
    """Run Git without a shell; only ``apply_profile`` issues writes."""
    try:
        result = subprocess.run(
            ["git", "-C", str(repo), *args],
            input=input_text,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
    except OSError as error:
        raise CheckoutError("无法运行 Git：{}".format(error)) from error
    if check and result.returncode:
        detail = result.stderr.strip() or "退出码 {}".format(result.returncode)
        raise CheckoutError("git {} 失败：{}".format(" ".join(args), detail))
    return result


def repository_root(directory: Path) -> Path:
    result = git(directory, "rev-parse", "--is-inside-work-tree", check=False)
    if result.returncode or result.stdout.strip() != "true":
        raise CheckoutError("目标必须是 Git 工作树；请先 clone 仓库。")
    root = git(directory, "rev-parse", "--show-toplevel").stdout.strip()
    if not root:
        raise CheckoutError("无法确定 Git 工作树根目录。")
    return Path(root).resolve()


def validate_path(value: object) -> str:
    """Require literal, canonical repository-relative POSIX paths."""
    if not isinstance(value, str) or not value or value != value.strip():
        raise CheckoutError("检出路径必须是非空字符串且不能有首尾空白。")
    components = value.split("/")
    if (value.startswith("/") or re.match(r"^[A-Za-z]:", value)
            or any(part in ("", ".", "..") for part in components)
            or any(character in value for character in "*?[]\\")
            or any(ord(character) < 32 for character in value)
            or components[0] == ".git"):
        raise CheckoutError("不安全的检出路径：{!r}".format(value))
    return value


def paths_from_json(value: object, field: str) -> Tuple[str, ...]:
    if not isinstance(value, list):
        raise CheckoutError("{} 必须是路径列表。".format(field))
    return tuple(dict.fromkeys(validate_path(path) for path in value))


def parse_catalog(data: object) -> Catalog:
    if not isinstance(data, dict) or data.get("version") != 1:
        raise CheckoutError("检出配置必须使用 version: 1。")
    base_files = paths_from_json(data.get("base_files"), "base_files")
    if ".gitignore" not in base_files:
        raise CheckoutError("base_files 必须包含 .gitignore，以保留运行产物隔离规则。")
    definitions = data.get("profiles")
    if not isinstance(definitions, dict) or not definitions:
        raise CheckoutError("profiles 必须是非空配置映射。")
    profiles = {}
    for name, definition in definitions.items():
        if not isinstance(name, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
            raise CheckoutError("无效的 profile 名称：{!r}".format(name))
        if not isinstance(definition, dict):
            raise CheckoutError("profile {} 必须是配置对象。".format(name))
        description = definition.get("description", "")
        if not isinstance(description, str):
            raise CheckoutError("profile {} 的 description 必须是字符串。".format(name))
        paths = paths_from_json(definition.get("paths"), "{}.paths".format(name))
        # A whole work/course directory would also include personal lectures.
        if any(not path.startswith(("assignments/", "work/"))
               or (path.startswith("work/") and len(path.split("/")) < 3)
               for path in paths):
            raise CheckoutError("profile {} 只能选作业及对应的个人作业目录。".format(name))
        files = paths_from_json(definition.get("files", []), "{}.files".format(name))
        profiles[name] = Profile(description, paths, files)
    if "all-exercises" not in profiles:
        raise CheckoutError("配置缺少默认 profile：all-exercises。")
    return Catalog(base_files, profiles)


def load_catalog(repo: Path) -> Catalog:
    source = repo / CONFIG_PATH
    try:
        if source.is_file():
            content = source.read_text(encoding="utf-8")
        else:
            # Bootstrap a --no-checkout clone without materializing any library.
            content = git(repo, "show", "HEAD:" + CONFIG_PATH).stdout
        return parse_catalog(json.loads(content))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise CheckoutError("无法读取检出配置：{}".format(error)) from error


def selected_profiles(catalog: Catalog, names: Iterable[str]) -> List[str]:
    selected = list(dict.fromkeys(names))
    if not selected:
        selected = ["all-exercises"]
    unknown = [name for name in selected if name not in catalog.profiles]
    if unknown:
        raise CheckoutError("未知 profile：{}；使用 list 查看可选项。".format(", ".join(unknown)))
    return selected


def build_patterns(catalog: Catalog, names: Iterable[str]) -> List[str]:
    selected = selected_profiles(catalog, names)
    patterns = ["/" + path for path in catalog.base_files]
    for name in selected:
        profile = catalog.profiles[name]
        patterns.extend("/" + path for path in profile.files)
        patterns.extend("/" + path + "/" for path in profile.paths)
    return list(dict.fromkeys(patterns))


def ensure_safe_checkout(repo: Path) -> bool:
    """Refuse a full checkout; return whether an empty index needs bootstrap."""
    sparse = git(repo, "config", "--bool", "core.sparseCheckout", check=False)
    # A fresh clone --no-checkout contains only .git and has no Git index.
    # An emptied full checkout still has an index, and must remain protected.
    if not any(path.name != ".git" for path in repo.iterdir()):
        index = Path(git(repo, "rev-parse", "--git-path", "index").stdout.strip())
        if not index.is_absolute():
            index = repo / index
        if not index.exists():
            return True
    if sparse.returncode == 0 and sparse.stdout.strip() == "true":
        return False
    status = git(repo, "status", "--porcelain=v1", "--untracked-files=all").stdout
    if status:
        raise CheckoutError(
            "完整工作树含有本地修改或未跟踪文件，已拒绝修改检出范围。"
            "请使用单独的新 clone --no-checkout 或已有 sparse 目录；不要在主项目执行 set。"
        )
    raise CheckoutError(
        "已拒绝修改完整本机工作树。请使用单独的新 clone --no-checkout "
        "或已有 sparse 目录；不要在主项目执行 set。"
    )


def apply_profile(repo: Path, catalog: Catalog, names: Iterable[str],
                  dry_run: bool = False) -> List[str]:
    selected = selected_profiles(catalog, names)
    patterns = build_patterns(catalog, selected)
    if dry_run:
        return patterns
    fresh_no_checkout = ensure_safe_checkout(repo)
    git(repo, "sparse-checkout", "set", "--no-cone", "--stdin",
        input_text="\n".join(patterns) + "\n")
    if fresh_no_checkout:
        # sparse-checkout set writes the patterns, but an absent index has no
        # HEAD entries to populate. Initialize it only after the patterns are
        # in place, so lecture/reference blobs are never checked out first.
        git(repo, "read-tree", "-mu", "HEAD")
    git(repo, "config", "--replace-all", PROFILE_CONFIG_KEY, selected[0])
    for name in selected[1:]:
        git(repo, "config", "--add", PROFILE_CONFIG_KEY, name)
    return patterns


def argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, help="目标 Git 工作树目录；默认当前目录")
    commands = parser.add_subparsers(dest="command", required=True)
    listing = commands.add_parser("list", help="查看所有作业 profile；不修改仓库")
    setting = commands.add_parser("set", help="在服务器 clone 中设置作业检出范围")
    for command in (listing, setting):
        command.add_argument("--repo-root", type=Path, default=argparse.SUPPRESS,
                             help=argparse.SUPPRESS)
    setting.add_argument("profile", nargs="?", default="all-exercises")
    setting.add_argument("--add", action="append", default=[], metavar="PROFILE",
                         help="在本次选择中加入另一个 profile；可重复使用")
    setting.add_argument("--dry-run", action="store_true", help="仅打印检出模式，不修改 Git")
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    args = argument_parser().parse_args(argv)
    try:
        repo = repository_root((args.repo_root or Path.cwd()).resolve())
        catalog = load_catalog(repo)
        if args.command == "list":
            for name, profile in catalog.profiles.items():
                print("{}\t{}".format(name, profile.description))
            return 0
        names = selected_profiles(catalog, [args.profile, *args.add])
        patterns = apply_profile(repo, catalog, names, dry_run=args.dry_run)
        if args.dry_run:
            print("\n".join(patterns))
        else:
            print("已设置服务器作业范围：{}".format(", ".join(names)))
            print("这是工作树选择。减少下载量还需在 clone 时使用 --filter=blob:none --depth 1。")
        return 0
    except CheckoutError as error:
        print("错误：{}".format(error), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
