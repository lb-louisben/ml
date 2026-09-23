"""Execute the local lecture 1/4 study notebooks with real weights, offline."""

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import sys

import nbformat
from nbclient import NotebookClient
from jupyter_client import KernelManager

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--only", choices=("1", "4"), help="Only run one lecture")
    args = parser.parse_args()
    model = ROOT / ".cache/llm-course/qwen3-tokenizer"
    if not (model / "model.safetensors").is_file():
        parser.exit(1, "请先运行 .venv/bin/python scripts/download_nju_model.py\n")
    for key, relative in {"MPLCONFIGDIR": ".cache/matplotlib", "IPYTHONDIR": ".cache/ipython",
                          "JUPYTER_RUNTIME_DIR": ".jupyter/runtime"}.items():
        path = ROOT / relative
        path.mkdir(parents=True, exist_ok=True)
        os.environ[key] = str(path)
    os.environ["HF_HUB_OFFLINE"] = "1"
    os.environ["TRANSFORMERS_OFFLINE"] = "1"
    records = []
    for number in ([args.only] if args.only else ["1", "4"]):
        source = ROOT / f"work/nju-llm-2026/lecture{number}.ipynb"
        folder = ROOT / f".cache/nju-validation/lecture{number}"
        folder.mkdir(parents=True, exist_ok=True)
        notebook = nbformat.read(source, as_version=4)
        manager = KernelManager(kernel_name="python3")
        manager.kernel_spec.argv = [sys.executable, "-m", "ipykernel_launcher", "-f", "{connection_file}"]
        client = NotebookClient(notebook, timeout=600, resources={"metadata": {"path": str(folder)}})
        client.km = manager
        print(f"Running lecture {number} with local weights...", flush=True)
        try:
            client.execute()
        finally:
            if manager.has_kernel:
                manager.shutdown_kernel(now=True)
        nbformat.write(notebook, folder / source.name)
        cells = sum(cell.cell_type == "code" for cell in notebook.cells)
        records.append(dict(lecture=number, code_cells=cells, status="passed",
                            source=str(source.relative_to(ROOT))))
        print(f"PASS lecture {number}: {cells} code cells", flush=True)
    report = dict(verified_at=datetime.now(timezone.utc).isoformat(), python=sys.executable,
                  model="Qwen/Qwen3-0.6B", offline=True, notebooks=records)
    dest = ROOT / ".cache/nju-validation/model-verification.json"
    dest.write_text(json.dumps(report, indent=2) + "\n")
    print(f"PASS real model verification: {dest.relative_to(ROOT)}", flush=True)


if __name__ == "__main__":
    main()
