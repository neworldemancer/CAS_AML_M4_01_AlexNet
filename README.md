# AlexNet / EfficientNet ImageNet demos

Two parallel Jupyter notebooks exercising pretrained ImageNet classifiers
(`alexnet_demo.ipynb` with torchvision's AlexNet, `efficientnet_demo.ipynb`
with EfficientNet-B0) on the same set of internet test images, with identical
structure throughout:

1. **Inference** on a curated set of Wikimedia Commons images, each paired
   with a known ground-truth ImageNet class.
2. **Robustness sweeps** — scale, brightness, and contrast perturbed on a log
   scale around identity, tracking how P(true class) responds.
3. **Input optimization toward the true class** for every misclassified
   image: gradient ascent directly on the input pixels (model and weights
   fixed), visualized over the course of 1000 steps, with before/after diff
   maps.
4. **The same optimization, EOT-regularized**: each step's gradient is
   averaged over 32 randomly augmented views of the current image (random
   scale/rotation/brightness/contrast/saturation/hue), rather than computed
   on a single view — see `prompts.md` session 2 for why a single sample per
   step produces a near-random walk instead of a directed one.

> **Just here to look, not to run anything?** Open
> `alexnet_demo.results.ipynb` / `efficientnet_demo.results.ipynb` — no
> setup needed, every figure and printed output from the last full run is
> already baked in. See **Running** below.

## Setup

```
uv sync
```

Requires Python ≥3.11 and pulls in `torch`/`torchvision` (CPU by default on
this platform), `jupyter`, `matplotlib`, etc. — see `pyproject.toml`.

## Running

**Just want to look at the results?** No setup needed — open
`alexnet_demo.results.ipynb` / `efficientnet_demo.results.ipynb` directly;
they already have every figure and printed output from the last full run
baked in.

To run it yourself: open either source notebook (`alexnet_demo.ipynb` /
`efficientnet_demo.ipynb`) in Jupyter/VS Code and run all cells, or
regenerate both end to end from the command line:

```
uv run run_all
```

This executes `alexnet_demo.ipynb` and `efficientnet_demo.ipynb` in clean
kernels and writes the populated results to `alexnet_demo.results.ipynb` /
`efficientnet_demo.results.ipynb` (see **Notebook layout** below). It's
expensive — on CPU, the EOT-regularized optimization section alone takes
roughly 1–3 hours per notebook (1000 steps × 32 augmented samples/step ×
~4–5 misclassified images).

## Notebook layout

- `alexnet_demo.ipynb`, `efficientnet_demo.ipynb` — the source notebooks,
  kept **output-free** in git so diffs stay readable.
- `alexnet_demo.results.ipynb`, `efficientnet_demo.results.ipynb` — the same
  notebooks *with* their last full execution's outputs baked in (figures,
  printed probabilities, etc.), so results can be reviewed without rerunning
  anything. These are large (tens of MB, mostly embedded PNGs) and tracked
  via **git-lfs** (`*.results.ipynb`, see `.gitattributes`) — run
  `git lfs install` once after cloning.
- `images/` — downloaded test images and generated study artifacts
  (`images/opt_study/`); gitignored, regenerated on demand by the notebooks.

## Other files

- `prompts.md` — the full prompt history behind these notebooks (across two
  sessions), kept for reproducibility and as a record of *why* things are
  the way they are (e.g. the `N_AUG_SAMPLES = 32` choice).
- `src/alexnet_demos/` — the `run_all` console script (see Running,
  above).
