"""Download and verify the official Qwen3 model used by NJU lectures 1 and 4."""

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODEL_DIR = ROOT / ".cache/llm-course/qwen3-tokenizer"
REPOSITORY = "Qwen/Qwen3-0.6B"
REVISION = "c1899de289a04d12100db370d81485cdf75e47ca"
PATTERNS = ["*.json", "*.txt", "*.safetensors", "*.jinja", "README.md", "LICENSE"]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--revision", default=REVISION, help="Official model revision; defaults to the verified snapshot")
    parser.add_argument("--direct", action="store_true", help="Bypass the current proxy if direct access works")
    args = parser.parse_args()
    os.environ.setdefault("HF_HOME", str(ROOT / ".cache/huggingface"))
    os.environ.setdefault("HF_HUB_DISABLE_XET", "1")
    os.environ.setdefault("HF_HUB_DOWNLOAD_TIMEOUT", "60")
    os.environ.setdefault("HF_HUB_ETAG_TIMEOUT", "20")
    if args.direct:
        for key in ("HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "http_proxy", "https_proxy", "all_proxy"):
            os.environ.pop(key, None)
        os.environ["NO_PROXY"] = "*"
    from huggingface_hub import HfApi, snapshot_download
    from fnmatch import fnmatch

    info = HfApi().model_info(REPOSITORY, revision=args.revision, files_metadata=True, timeout=20)
    files = [item for item in info.siblings if any(fnmatch(item.rfilename, pattern) for pattern in PATTERNS)]
    print(f"Downloading {REPOSITORY} @ {info.sha} ({sum(item.size or 0 for item in files):,} bytes)", flush=True)
    snapshot_download(repo_id=REPOSITORY, revision=info.sha, local_dir=MODEL_DIR,
                      allow_patterns=PATTERNS, max_workers=4)
    records = []
    for item in files:
        path = MODEL_DIR / item.rfilename
        if item.size is not None and path.stat().st_size != item.size:
            raise ValueError(f"Size mismatch: {item.rfilename}")
        digest = hashlib.sha256()
        with path.open("rb") as stream:
            for chunk in iter(lambda: stream.read(8 * 1024 * 1024), b""):
                digest.update(chunk)
        actual = digest.hexdigest()
        if item.lfs and actual != item.lfs.sha256:
            raise ValueError(f"Official LFS SHA256 mismatch: {item.rfilename}")
        records.append(dict(file=item.rfilename, bytes=path.stat().st_size, sha256=actual))
    manifest = dict(repository=REPOSITORY, revision=info.sha,
                    verified_at=datetime.now(timezone.utc).isoformat(), files=records)
    (MODEL_DIR / "download-source.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"PASS: {len(records)} files verified at {MODEL_DIR}", flush=True)


if __name__ == "__main__":
    main()
