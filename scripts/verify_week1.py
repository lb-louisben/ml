"""Execute only the newly authored lessons; never overwrite source notebooks."""
from pathlib import Path
import os
import sys
import nbformat
from nbclient import NotebookClient

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "week1/outputs/verified"
OUTPUT.mkdir(parents=True, exist_ok=True)
for key, folder in {
    "MPLCONFIGDIR": ROOT / ".cache/matplotlib",
    "IPYTHONDIR": ROOT / ".cache/ipython",
    "JUPYTER_CONFIG_DIR": ROOT / ".jupyter",
    "JUPYTER_DATA_DIR": ROOT / ".jupyter/data",
    "JUPYTER_RUNTIME_DIR": ROOT / ".jupyter/runtime",
}.items():
    folder.mkdir(parents=True, exist_ok=True)
    os.environ.setdefault(key, str(folder))

FILES = [
    "day1/01_Python_depth_breadth_bonus.ipynb",
    "day2/02_NumPy_depth_breadth_bonus.ipynb",
    "day3/03_Pandas_data_cleaning.ipynb",
    "day4/04_Visualization_EDA.ipynb",
    "day5/05_ML_workflow_and_splits.ipynb",
    "day6/06_Linear_regression.ipynb",
    "day7/07_Metrics_and_final_evaluation.ipynb",
    "project/08_Student_performance_project.ipynb",
]

failed = []
for relative in FILES:
    path = ROOT / "week1" / relative
    try:
        notebook = nbformat.read(path, as_version=4)
        nbformat.validate(notebook)
        client = NotebookClient(notebook, timeout=180, kernel_name="python3",
                                resources={"metadata": {"path": str(path.parent)}})
        # Force the current project Python rather than an unrelated user kernel.
        from jupyter_client import KernelManager
        manager = KernelManager(kernel_name="python3")
        manager.kernel_spec.argv = [sys.executable, "-m", "ipykernel_launcher", "-f", "{connection_file}"]
        client.km = manager
        try:
            client.execute()
        finally:
            if manager.has_kernel:
                manager.shutdown_kernel(now=True)
        nbformat.write(notebook, OUTPUT / path.name)
        print("PASS", relative, flush=True)
    except Exception as exc:
        failed.append(relative)
        print("FAIL", relative, str(exc), flush=True)

print(f"Verified {len(FILES)-len(failed)}/{len(FILES)} notebooks", flush=True)
if failed:
    raise SystemExit(1)
