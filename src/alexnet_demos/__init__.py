"""Execute the demo notebooks end to end and write the populated `*.results.ipynb` copies.

Each run is expensive (the EOT-style optimization section alone takes roughly
1-3 hours per notebook on CPU) and overwrites that notebook's `.results.ipynb`
copy, which is tracked via git-lfs. The source notebooks themselves
(`alexnet_demo.ipynb`, `efficientnet_demo.ipynb`) are kept output-free in git.
"""

from pathlib import Path

import nbformat
from nbclient import NotebookClient

REPO_ROOT = Path(__file__).resolve().parents[2]
NOTEBOOKS = ("alexnet_demo.ipynb", "efficientnet_demo.ipynb")


def run_notebook(name: str) -> Path:
    """Execute `name` and write the populated notebook to `<stem>.results.ipynb`."""
    src = REPO_ROOT / name
    dst = REPO_ROOT / f"{src.stem}.results.ipynb"

    nb = nbformat.read(src, as_version=4)
    client = NotebookClient(
        nb, timeout=-1, kernel_name="python3", resources={"metadata": {"path": str(REPO_ROOT)}}
    )
    client.execute()
    nbformat.write(nb, dst)
    return dst


def main() -> None:
    for name in NOTEBOOKS:
        print(f"executing {name} ...")
        dst = run_notebook(name)
        print(f"  -> wrote {dst.name}")
