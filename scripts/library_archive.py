#!/usr/bin/env python3
"""Archive reference materials on GitHub Releases without making clones heavy.

Only ``publish``, ``restore`` and ``fetch`` invoke GitHub CLI. ``pack`` and its
unpacked-copy audit are offline. Existing local files are never overwritten.
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import re
import shutil
import stat
import subprocess
import tarfile
import tempfile
from pathlib import Path, PurePosixPath
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TAG = "materials-2026-10-12"
DEFAULT_REPOSITORY = "lb-louisben/ml"
COURSES = (
    "berkeley-cs182-sp21",
    "berkeley-cs189-sp25",
    "berkeley-data100-sp25",
    "mit-1806sc-f11",
    "stanford-cs224n-w25",
    "stanford-cs229-see",
    "stanford-cs231n-2025",
)
EXCLUDED_PARTS = {
    "unpacked", "runtime", "__pycache__", ".DS_Store", ".git", ".cache",
    ".venv", ".venv-dl", "venv", ".ipynb_checkpoints", "outputs",
    "checkpoints", "wandb", "runs", "node_modules", "__MACOSX",
}
EXCLUDED_SUFFIXES = {".pyc", ".pyo", ".incomplete", ".safetensors", ".ckpt", ".pem", ".key"}
MANIFEST_ASSET = "archive-manifest.json"
SOURCE_ASSET = "library-source-manifest.json"


class ArchiveError(ValueError):
    """An archive cannot be trusted or would replace local work."""


def sha256(path: Path) -> str:
    with path.open("rb") as stream:
        return stream_sha256(stream)


def stream_sha256(stream) -> str:
    digest = hashlib.sha256()
    for chunk in iter(lambda: stream.read(1024 * 1024), b""):
        digest.update(chunk)
    return digest.hexdigest()


def excluded(path: PurePosixPath) -> bool:
    return (
        any(part in EXCLUDED_PARTS or part.startswith("._") for part in path.parts)
        or path.suffix.lower() in EXCLUDED_SUFFIXES
        or path.name == ".env" or path.name.startswith(".env.")
    )


def safe_relative(value: str) -> PurePosixPath:
    path = PurePosixPath(value)
    if (
        not value or path.is_absolute() or ".." in path.parts or "\\" in value
        or path.as_posix() != value or any(ord(c) < 32 for c in value)
    ):
        raise ArchiveError(f"Unsafe relative path: {value!r}")
    return path


def safe_destination(root: Path, relative: str) -> Path:
    path = safe_relative(relative)
    target = root.joinpath(*path.parts)
    current = root
    for part in path.parts:
        current = current / part
        if current.is_symlink():
            raise ArchiveError(f"Refusing symlink destination: {current}")
    if not target.resolve().is_relative_to(root.resolve()):
        raise ArchiveError(f"Destination escapes project: {relative}")
    return target


def validate_tag(tag: str) -> None:
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", tag):
        raise ArchiveError("Tag must contain only letters, digits, dots, dashes or underscores")


def validate_repository(repository: str) -> None:
    if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repository):
        raise ArchiveError("Repository must be OWNER/REPOSITORY")


def file_record(root: Path, path: Path, course: str | None, asset: str, member: str | None) -> dict:
    if path.is_symlink() or not path.is_file():
        raise ArchiveError(f"Only regular files can be archived: {path}")
    return {
        "path": path.relative_to(root).as_posix(), "course": course,
        "size": path.stat().st_size, "sha256": sha256(path),
        "asset": asset, "member": member,
    }


def verify_file(path: Path, expected: dict) -> None:
    if path.is_symlink() or not path.is_file():
        raise ArchiveError(f"Missing regular file: {path}")
    if path.stat().st_size != expected["size"] or sha256(path) != expected["sha256"]:
        raise ArchiveError(f"Size/SHA256 mismatch: {path}")


def audit_unpacked(root: Path, courses: tuple[str, ...] = COURSES) -> dict:
    """Compare extracted originals, ignoring generated caches and archive markers."""
    checked = 0
    changes = []
    for course in courses:
        unpacked = root / "library" / course / "unpacked"
        if not unpacked.exists():
            continue
        for directory in sorted(unpacked.iterdir()):
            if not directory.is_dir() or directory.is_symlink():
                changes.append({"path": directory.relative_to(root).as_posix(), "reason": "unexpected unpacked entry"})
                continue
            archive = unpacked.parent / (directory.name + ".zip")
            if not archive.is_file():
                changes.append({"path": directory.relative_to(root).as_posix(), "reason": "no original ZIP"})
                continue
            expected = set()
            with ZipFile(archive) as bundle:
                for info in bundle.infolist():
                    relative = safe_relative(info.filename.rstrip("/"))
                    if (info.is_dir() or "__MACOSX" in relative.parts
                            or relative.name.startswith("._")
                            or stat.S_ISLNK(info.external_attr >> 16)):
                        continue
                    expected.add(relative.as_posix())
                    target = safe_destination(directory, relative.as_posix())
                    if not target.is_file():
                        changes.append({"path": target.relative_to(root).as_posix(), "reason": "missing"})
                        continue
                    with bundle.open(info) as source:
                        original = stream_sha256(source)
                    checked += 1
                    if original != sha256(target):
                        changes.append({"path": target.relative_to(root).as_posix(), "reason": "modified"})
            for target in sorted(directory.rglob("*")):
                relative = PurePosixPath(target.relative_to(directory).as_posix())
                if target.is_file() and relative.as_posix() not in expected and not excluded(relative) and target.name != ".archive-sha256":
                    changes.append({"path": target.relative_to(root).as_posix(), "reason": "extra"})
    return {"files_checked": checked, "changes": changes}


def write_tar(root: Path, target: Path, records: list[dict]) -> None:
    """Produce a deterministic archive so retrying pack keeps the same digest."""
    with target.open("wb") as output:
        with gzip.GzipFile(filename="", mode="wb", fileobj=output, mtime=0) as compressed:
            with tarfile.open(fileobj=compressed, mode="w", format=tarfile.GNU_FORMAT) as bundle:
                for record in records:
                    source = root / record["path"]
                    verify_file(source, record)
                    info = tarfile.TarInfo(record["member"])
                    info.size = record["size"]
                    info.mode = 0o644
                    info.mtime = 0
                    with source.open("rb") as stream:
                        bundle.addfile(info, stream)


def pack(root: Path = ROOT, tag: str = DEFAULT_TAG, repository: str = DEFAULT_REPOSITORY,
         cache: Path | None = None, manifest_path: Path | None = None,
         courses: tuple[str, ...] = COURSES) -> dict:
    validate_tag(tag)
    validate_repository(repository)
    cache = cache or root / ".cache" / "github-archive" / tag
    manifest_path = manifest_path or root / "config" / "archive-manifest.json"
    audit = audit_unpacked(root, courses)
    if audit["changes"]:
        raise ArchiveError("Unpacked copies contain changes; preserve them in work/ before packing:\n" + json.dumps(audit, ensure_ascii=False, indent=2))
    cache.mkdir(parents=True, exist_ok=True)
    records = []
    assets = []
    for course in courses:
        folder = root / "library" / course
        if not folder.is_dir() or folder.is_symlink():
            raise ArchiveError(f"Missing course directory: {folder}")
        course_records = []
        for source in sorted(folder.rglob("*")):
            relative = PurePosixPath(source.relative_to(folder).as_posix())
            if excluded(relative):
                continue
            if source.is_symlink():
                raise ArchiveError(f"Refusing source symlink: {source}")
            if not source.is_file():
                continue
            if source.suffix.lower() == ".zip":
                name = course + "--" + relative.as_posix().replace("/", "--")
                record = file_record(root, source, course, name, None)
                destination = cache / name
                if destination.exists():
                    verify_file(destination, record)
                else:
                    shutil.copyfile(source, destination)
                    verify_file(destination, record)
                assets.append({"name": name, "kind": "zip", "course": course,
                               "size": record["size"], "sha256": record["sha256"]})
            else:
                name = course + "--materials.tar.gz"
                record = file_record(root, source, course, name, source.relative_to(root).as_posix())
                course_records.append(record)
            records.append(record)
        if course_records:
            target = cache / (course + "--materials.tar.gz")
            with tempfile.TemporaryDirectory(dir=cache, prefix=".pack-") as temporary:
                prepared = Path(temporary) / target.name
                write_tar(root, prepared, course_records)
                metadata = {"name": target.name, "kind": "tar.gz", "course": course,
                            "size": prepared.stat().st_size, "sha256": sha256(prepared)}
                if target.exists():
                    verify_file(target, metadata)
                else:
                    shutil.copyfile(prepared, target)
            assets.append(metadata)
    source = root / "library" / "manifest.json"
    record = file_record(root, source, None, SOURCE_ASSET, None)
    target = cache / SOURCE_ASSET
    if target.exists():
        verify_file(target, record)
    else:
        shutil.copyfile(source, target)
    records.append(record)
    assets.append({"name": SOURCE_ASSET, "kind": "source-manifest", "course": None,
                   "size": record["size"], "sha256": record["sha256"]})
    manifest = {"schema_version": 1, "tag": tag, "repository": repository,
                "courses": list(courses), "files": records, "assets": assets,
                "unpacked_audit": audit}
    validate_manifest(manifest)
    encoded = json.dumps(manifest, ensure_ascii=False, indent=2) + "\n"
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(encoded)
    (cache / MANIFEST_ASSET).write_text(encoded)
    return manifest


def validate_manifest(manifest: dict) -> None:
    if manifest.get("schema_version") != 1:
        raise ArchiveError("Unsupported archive manifest schema")
    validate_tag(manifest["tag"])
    validate_repository(manifest["repository"])
    if not manifest["courses"] or len(set(manifest["courses"])) != len(manifest["courses"]):
        raise ArchiveError("Duplicate or empty course list")
    if any(course not in COURSES for course in manifest["courses"]):
        raise ArchiveError("Manifest contains an unknown course")
    names = set()
    for asset in manifest["assets"]:
        name = asset["name"]
        if safe_relative(name).name != name or name in names or name == MANIFEST_ASSET:
            raise ArchiveError(f"Invalid or duplicate asset: {name}")
        names.add(name)
        if asset["kind"] not in {"zip", "tar.gz", "source-manifest"}:
            raise ArchiveError(f"Unsupported asset kind: {asset['kind']}")
        if asset["course"] is not None and asset["course"] not in manifest["courses"]:
            raise ArchiveError(f"Unknown asset course: {name}")
        if asset["kind"] == "source-manifest" and (name != SOURCE_ASSET or asset["course"] is not None):
            raise ArchiveError("Invalid source manifest asset")
        if not isinstance(asset["size"], int) or asset["size"] < 0 or asset["size"] >= 2 * 1024**3:
            raise ArchiveError(f"Asset exceeds GitHub Release size limit: {name}")
        if not re.fullmatch(r"[0-9a-f]{64}", asset["sha256"]):
            raise ArchiveError(f"Invalid asset digest: {name}")
    paths = set()
    assets = {asset["name"]: asset for asset in manifest["assets"]}
    for record in manifest["files"]:
        path = safe_relative(record["path"])
        if record["path"] in paths or path.parts[0] != "library":
            raise ArchiveError(f"Invalid or duplicate archived path: {path}")
        paths.add(record["path"])
        course = record["course"]
        if course is None:
            if record["path"] != "library/manifest.json" or record["asset"] != SOURCE_ASSET:
                raise ArchiveError("Only the source manifest may live outside a course")
        elif course not in manifest["courses"] or len(path.parts) < 3 or path.parts[1] != course or excluded(PurePosixPath(*path.parts[2:])):
            raise ArchiveError(f"Invalid course file: {path}")
        if record["asset"] not in assets:
            raise ArchiveError(f"Unknown asset for file: {path}")
        asset = assets[record["asset"]]
        if asset["course"] != course:
            raise ArchiveError(f"Asset/course mismatch: {path}")
        if not isinstance(record["size"], int) or record["size"] < 0 or not re.fullmatch(r"[0-9a-f]{64}", record["sha256"]):
            raise ArchiveError(f"Invalid file metadata: {path}")
        if asset["kind"] == "tar.gz":
            if record["member"] != record["path"]:
                raise ArchiveError(f"Invalid tar member: {path}")
        elif record["member"] is not None or asset["size"] != record["size"] or asset["sha256"] != record["sha256"]:
            raise ArchiveError(f"Invalid standalone asset: {path}")
    for asset in manifest["assets"]:
        members = [record for record in manifest["files"] if record["asset"] == asset["name"]]
        if not members or (asset["kind"] != "tar.gz" and len(members) != 1):
            raise ArchiveError(f"Invalid asset file mapping: {asset['name']}")
        if asset["kind"] == "zip" and not members[0]["path"].lower().endswith(".zip"):
            raise ArchiveError(f"ZIP asset maps to a non-ZIP file: {asset['name']}")


def load_manifest(path: Path) -> dict:
    manifest = json.loads(path.read_text())
    validate_manifest(manifest)
    return manifest


def run_gh(arguments: list[str], check: bool = True) -> subprocess.CompletedProcess:
    try:
        result = subprocess.run(["gh", *arguments], capture_output=True, text=True)
    except FileNotFoundError as error:
        raise ArchiveError("GitHub CLI is required; install gh and authenticate with gh auth login") from error
    if check and result.returncode:
        raise ArchiveError("GitHub CLI failed: " + redact_error(result.stderr))
    return result


def redact_error(value: str) -> str:
    value = re.sub(r"(?:gh[pousr]_[A-Za-z0-9_]+|github_pat_[A-Za-z0-9_]+)", "[REDACTED]", value)
    value = re.sub(r"(?i)(?:bearer|token)\s+\S+", "[REDACTED]", value)
    return value.strip()


def release_info(manifest: dict) -> dict | None:
    # The by-tag endpoint is documented for published releases. Listing also
    # returns authenticated drafts, so interrupted uploads can be resumed.
    page = 1
    while True:
        endpoint = f"repos/{manifest['repository']}/releases?per_page=100&page={page}"
        result = run_gh(["api", endpoint], check=False)
        if result.returncode:
            raise ArchiveError("Cannot inspect releases: " + redact_error(result.stderr))
        releases = json.loads(result.stdout)
        if not isinstance(releases, list):
            raise ArchiveError("GitHub returned an unexpected release listing")
        for release in releases:
            if release.get("tag_name") == manifest["tag"]:
                release["assets"] = release_assets(manifest, release["id"])
                return release
        if len(releases) < 100:
            return None
        page += 1


def release_assets(manifest: dict, release_id: int) -> list[dict]:
    """Read all attachments, rather than trusting the embedded asset preview."""
    assets = []
    page = 1
    while True:
        endpoint = f"repos/{manifest['repository']}/releases/{release_id}/assets?per_page=100&page={page}"
        result = run_gh(["api", endpoint])
        batch = json.loads(result.stdout)
        if not isinstance(batch, list):
            raise ArchiveError("GitHub returned an unexpected asset listing")
        assets.extend(batch)
        if len(batch) < 100:
            return assets
        page += 1


def verify_remote_asset(remote: dict, expected: dict) -> None:
    if (remote.get("size") != expected["size"]
            or remote.get("digest") != "sha256:" + expected["sha256"]
            or remote.get("state") != "uploaded"):
        raise ArchiveError(f"Remote asset size/digest differs or upload incomplete: {expected['name']}; refusing to overwrite")


def publish(manifest_path: Path, cache: Path, target: str | None = None, tag: str | None = None) -> dict:
    manifest = load_manifest(manifest_path)
    if tag is not None and tag != manifest["tag"]:
        raise ArchiveError("Requested publication tag differs from archive-manifest.json; run pack first")
    expected = [*manifest["assets"], {
        "name": MANIFEST_ASSET, "size": manifest_path.stat().st_size, "sha256": sha256(manifest_path),
    }]
    for asset in manifest["assets"]:
        verify_file(cache / asset["name"], asset)
    metadata = cache / MANIFEST_ASSET
    if metadata.exists():
        verify_file(metadata, expected[-1])
    else:
        shutil.copyfile(manifest_path, metadata)
    release = release_info(manifest)
    if release is None:
        args = ["release", "create", manifest["tag"], "--repo", manifest["repository"],
                "--draft", "--title", "Course materials archive — " + manifest["tag"],
                "--notes", "Original course resources, source URLs and SHA256 checksums. ZIP starter bundles can be downloaded separately."]
        if target:
            args.extend(["--target", target])
        run_gh(args)
        release = release_info(manifest)
        if release is None:
            raise ArchiveError("Release was created but cannot be inspected")
    remote = {asset["name"]: asset for asset in release.get("assets", [])}
    expected_names = {asset["name"] for asset in expected}
    if set(remote) - expected_names:
        raise ArchiveError("Release contains unexpected assets; refusing to publish a mixed archive")
    # Inspect every existing asset before making any uploads.
    for asset in expected:
        if asset["name"] in remote:
            verify_remote_asset(remote[asset["name"]], asset)
    missing = [asset for asset in expected if asset["name"] not in remote]
    if missing and not release.get("draft"):
        raise ArchiveError("Published release is incomplete; create a new tag instead of changing it")
    completed = len(expected) - len(missing)
    for asset in missing:
        print(f"[{completed + 1}/{len(expected)}] Uploading {asset['name']} ({asset['size'] / 1024**2:.2f} MiB)", flush=True)
        run_gh(["release", "upload", manifest["tag"], str(cache / asset["name"]),
                "--repo", manifest["repository"]])
        completed += 1
    release = release_info(manifest)
    if release is None:
        raise ArchiveError("Cannot verify uploaded release")
    remote = {asset["name"]: asset for asset in release.get("assets", [])}
    if set(remote) != expected_names:
        raise ArchiveError("Uploaded release asset list differs from the manifest")
    for asset in expected:
        if asset["name"] not in remote:
            raise ArchiveError("Missing uploaded asset: " + asset["name"])
        verify_remote_asset(remote[asset["name"]], asset)
    if release.get("draft"):
        run_gh(["release", "edit", manifest["tag"], "--repo", manifest["repository"], "--draft=false"])
        release = release_info(manifest)
        if release is None or release.get("draft"):
            raise ArchiveError("Upload verified but release publication could not be confirmed")
    return {"tag": manifest["tag"], "repository": manifest["repository"], "verified_assets": len(expected)}


def cached_asset(manifest: dict, asset: dict, cache: Path) -> Path:
    cache.mkdir(parents=True, exist_ok=True)
    destination = cache / asset["name"]
    if destination.exists():
        verify_file(destination, asset)
        return destination
    with tempfile.TemporaryDirectory(dir=cache, prefix=".download-") as temporary:
        folder = Path(temporary)
        run_gh(["release", "download", manifest["tag"], "--repo", manifest["repository"],
                "--pattern", asset["name"], "--dir", str(folder)])
        prepared = folder / asset["name"]
        verify_file(prepared, asset)
        shutil.copyfile(prepared, destination)
    return destination


def check_local(root: Path, record: dict) -> bool:
    destination = safe_destination(root, record["path"])
    if destination.exists():
        verify_file(destination, record)
        return True
    return False


def copy_missing(root: Path, source: Path, record: dict) -> None:
    if check_local(root, record):
        return
    destination = safe_destination(root, record["path"])
    destination.parent.mkdir(parents=True, exist_ok=True)
    # Exclusive creation prevents an existing local file from being overwritten.
    with destination.open("xb") as output, source.open("rb") as incoming:
        shutil.copyfileobj(incoming, output)
    verify_file(destination, record)


def restore_tar(root: Path, archive: Path, records: list[dict]) -> None:
    expected = {record["member"]: record for record in records}
    with tempfile.TemporaryDirectory(prefix="ml-materials-restore-") as temporary:
        staging = Path(temporary)
        with tarfile.open(archive, "r:gz") as bundle:
            seen = set()
            for member in bundle:
                safe_relative(member.name)
                if not member.isfile() or member.name not in expected or member.name in seen:
                    raise ArchiveError(f"Unexpected, duplicate or non-regular tar member: {member.name}")
                seen.add(member.name)
                record = expected[member.name]
                if member.size != record["size"]:
                    raise ArchiveError(f"Tar member size mismatch: {member.name}")
                destination = safe_destination(staging, member.name)
                destination.parent.mkdir(parents=True, exist_ok=True)
                incoming = bundle.extractfile(member)
                if incoming is None:
                    raise ArchiveError(f"Cannot read tar member: {member.name}")
                with incoming, destination.open("xb") as output:
                    shutil.copyfileobj(incoming, output)
                verify_file(destination, record)
            if seen != set(expected):
                raise ArchiveError("Archive is missing declared files")
        # Validate every member and local destination before copying any files.
        for record in records:
            check_local(root, record)
        for record in records:
            copy_missing(root, staging / record["path"], record)


def restore(root: Path, manifest: dict, cache: Path, courses: list[str] | None = None) -> dict:
    validate_manifest(manifest)
    selected = set(courses if courses is not None else manifest["courses"])
    if not selected or not selected.issubset(manifest["courses"]):
        raise ArchiveError("Select a known course or use --all")
    records = [record for record in manifest["files"] if record["course"] in selected or record["course"] is None]
    for record in records:
        check_local(root, record)
    asset_map = {asset["name"]: asset for asset in manifest["assets"]}
    restored_assets = []
    for name in sorted({record["asset"] for record in records}):
        group = [record for record in records if record["asset"] == name]
        if all(check_local(root, record) for record in group):
            continue
        asset = asset_map[name]
        source = cached_asset(manifest, asset, cache)
        if asset["kind"] == "tar.gz":
            restore_tar(root, source, group)
        else:
            if len(group) != 1:
                raise ArchiveError("Standalone asset maps to multiple files")
            copy_missing(root, source, group[0])
        restored_assets.append(name)
    return {"courses": sorted(selected), "verified_files": len(records), "restored_assets": restored_assets}


def fetch(root: Path, manifest: dict, cache: Path, filename: str) -> dict:
    validate_manifest(manifest)
    relative = safe_relative(filename)
    path = "library/" + relative.as_posix()
    candidates = [record for record in manifest["files"] if record["path"] == path]
    if len(candidates) != 1:
        raise ArchiveError("File is not in the archive manifest: " + filename)
    record = candidates[0]
    asset = next(asset for asset in manifest["assets"] if asset["name"] == record["asset"])
    if asset["kind"] != "zip":
        raise ArchiveError("fetch only accepts an original ZIP starter bundle")
    if not check_local(root, record):
        source = cached_asset(manifest, asset, cache)
        copy_missing(root, source, record)
    return {"file": record["path"], "asset": asset["name"], "sha256": record["sha256"]}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    for name in ("pack", "publish", "restore", "fetch"):
        command = commands.add_parser(name)
        command.add_argument("--root", type=Path, default=ROOT)
        command.add_argument("--manifest", type=Path)
        command.add_argument("--cache", type=Path, help="Reuse verified assets in this cache directory")
        if name == "pack":
            command.add_argument("--tag", default=DEFAULT_TAG)
            command.add_argument("--repository", default=DEFAULT_REPOSITORY)
        elif name == "publish":
            command.add_argument("--target", help="Committed branch or SHA to use when creating the release tag")
            command.add_argument("--tag", help="Must match the snapshot tag stored in archive-manifest.json")
        elif name == "restore":
            selection = command.add_mutually_exclusive_group(required=True)
            selection.add_argument("--course", action="append", choices=COURSES)
            selection.add_argument("--all", action="store_true")
        elif name == "fetch":
            command.add_argument("--file", required=True, help="COURSE/ORIGINAL_FILENAME.zip")
    args = parser.parse_args()
    root = args.root.resolve()
    manifest_path = args.manifest or root / "config" / "archive-manifest.json"
    try:
        if args.command == "pack":
            cache = args.cache or root / ".cache" / "github-archive" / args.tag
            manifest = pack(root, args.tag, args.repository, cache, manifest_path)
            result = {"manifest": str(manifest_path), "cache": str(cache),
                      "files": len(manifest["files"]), "assets": len(manifest["assets"]) + 1,
                      "asset_MiB": round(sum(asset["size"] for asset in manifest["assets"]) / 1024**2, 2),
                      "unpacked_audit": manifest["unpacked_audit"]}
        else:
            manifest = load_manifest(manifest_path)
            cache = args.cache or root / ".cache" / "github-archive" / manifest["tag"]
            if args.command == "publish":
                result = publish(manifest_path, cache, args.target, args.tag)
            elif args.command == "restore":
                result = restore(root, manifest, cache, args.course)
            else:
                result = fetch(root, manifest, cache, args.file)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except (ArchiveError, OSError, json.JSONDecodeError, tarfile.TarError) as error:
        parser.exit(1, f"Archive error: {error}\n")


if __name__ == "__main__":
    main()
