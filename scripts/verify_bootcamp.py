"""Run the guided Week 2/3 notebooks in fresh kernels without altering sources.

Run from the project root: .venv/bin/python scripts/verify_bootcamp.py
Use --only classification, --only numpy, or --only pytorch for a single lesson.
"""
from pathlib import Path
import argparse
import os
import sys

import nbformat
from nbclient import NotebookClient
from jupyter_client import KernelManager

ROOT = Path(__file__).resolve().parents[1]
LESSONS = {
    "classification": (
        "course/bootcamp/week2/classification_walkthrough.ipynb", ".venv/bin/python"
    ),
    "numpy": (
        "course/bootcamp/week3/01_numpy_network_walkthrough.ipynb", ".venv/bin/python"
    ),
    "pytorch": (
        "course/bootcamp/week3/02_pytorch_training_walkthrough.ipynb", ".venv/bin/python"
    ),
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--only", choices=LESSONS, help="Run one tutorial")
    args = parser.parse_args()
    selected = [args.only] if args.only else list(LESSONS)
    for key, relative in {
        "MPLCONFIGDIR": ".cache/matplotlib",
        "IPYTHONDIR": ".cache/ipython",
        "JUPYTER_CONFIG_DIR": ".jupyter",
        "JUPYTER_DATA_DIR": ".jupyter/data",
        "JUPYTER_RUNTIME_DIR": ".jupyter/runtime",
    }.items():
        folder = ROOT / relative
        folder.mkdir(parents=True, exist_ok=True)
        os.environ.setdefault(key, str(folder))
    # CPU examples need no GPU or external data downloads.
    os.environ.setdefault("OMP_NUM_THREADS", "1")
    os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
    failures = []
    for name in selected:
        relative, interpreter = LESSONS[name]
        source = ROOT / relative
        python = ROOT / interpreter
        try:
            if not python.is_file():
                raise RuntimeError(
                    f"Missing {interpreter}; follow docs/setup/DEEP_LEARNING.md "
                    "for PyTorch or docs/setup/README.md for the core environment."
                )
            notebook = nbformat.read(source, as_version=4)
            nbformat.validate(notebook)
            manager = KernelManager(kernel_name="python3")
            manager.kernel_spec.argv = [
                str(python), "-m", "ipykernel_launcher", "-f", "{connection_file}"
            ]
            client = NotebookClient(
                notebook, timeout=300, kernel_name="python3",
                resources={"metadata": {"path": str(source.parent)}},
            )
            client.km = manager
            try:
                client.execute()
            finally:
                if manager.has_kernel:
                    manager.shutdown_kernel(now=True)
            output = source.parent / "outputs/verified" / source.name
            output.parent.mkdir(parents=True, exist_ok=True)
            nbformat.write(notebook, output)
            count = sum(cell.cell_type == "code" for cell in notebook.cells)
            print(f"PASS {name}: {count} code cells; {output.relative_to(ROOT)}", flush=True)
        except Exception as exc:
            failures.append(name)
            print(f"FAIL {name}: {exc}", flush=True)
    print(f"Verified {len(selected) - len(failures)}/{len(selected)} tutorials", flush=True)
    return bool(failures)


if __name__ == "__main__":
    sys.exit(main())
