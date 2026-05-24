# How Positional Encoding Shapes Transferable Representations in Vision Transformers

[![Paper Status](https://img.shields.io/badge/paper-under%20submission-orange)](#paper-and-citation)
[![Code License: MIT](https://img.shields.io/badge/Code%20License-MIT-yellow.svg)](LICENSE)
[![Data License: CC BY 4.0](https://img.shields.io/badge/Data%20License-CC%20BY%204.0-blue.svg)](https://creativecommons.org/licenses/by/4.0/)

Code, trained models, and reproducibility scripts for the paper
*"How Positional Encoding Shapes Transferable Representations in Vision Transformers"*
(manuscript under submission).

---

## What is this repository?

Vision Transformers use a *positional encoding* (PE) to inject spatial
structure into a permutation-invariant attention mechanism. This work asks
whether the choice of PE has consequences that survive transfer — i.e.
whether features learned with different PEs on the same pretraining task
transfer differently to downstream tasks.

Twelve ViT-Base models (4 PE families × 3 seeds) are pretrained on
ImageNet-100 and evaluated on five fine-grained downstream datasets
(Food-101, Oxford-IIIT Pets, FGVC Aircraft, Oxford Flowers-102, DTD)
under two probing protocols (linear probe, k-NN). Representational
similarity between PE-variant models is then analysed layer by layer
using linear CKA.

The two main findings are:

| Claim | One-line summary |
| --- | --- |
| **C1 (primary)** | **RoPE consistently leads and Learned consistently trails** across all five downstream datasets and both probing protocols (linear probe and k-NN); the mean ordering is **RoPE > Sinusoidal > ALiBi > Learned**, with the relative position of the two middle families varying between protocols. Largest gap: +8.6 p.p. on Oxford Pets (RoPE vs Learned). |
| **C2 (supporting)** | Cross-PE representational divergence is **not monotone in depth**: it peaks at transformer block 9 of 12 (CKA ≈ 0.69–0.72), then partially rebounds at the final block. The peak layer is invariant to the choice of stimulus image set. |

The two findings together are consistent with a depth-dependent
representational specialization story: PE choice influences the
middle-to-late layers most, and the resulting feature differences are what
the linear probe / k-NN classifier sees at transfer time.

---

## Repository layout

This repository contains the **code** and **small reproducibility artefacts**
(summary tables, paired tests, heatmap figure). Large binary artefacts —
pretrained checkpoints (~3.8 GB), downstream features (~4 GB), and per-layer
CKA features — are hosted on Google Drive; the Zenodo deposit archives this
code repository together with the Google Drive link (see *Trained models*
below).

```
vit-pe-transfer/
├── README.md                       # this file
├── LICENSE                         # MIT (code) + CC BY 4.0 (results, figures) — see License section
├── .gitignore
│
├── data/
│   ├── datasets.py                 # downstream dataset loaders (Food101, Pets, ...)
│   ├── imagenet100_classes.txt     # 100 class IDs used for pretraining
│   └── val_labels.txt              # ImageNet-1k val → class mapping
├── models/
│   ├── vit_architecture.py         # ViT-Base + 4 PE variants (Learned, Sinusoidal, RoPE, ALiBi)
│   └── model_loader.py             # loads .pth checkpoints into the right PE variant
├── notebooks/
│   ├── 01_sanity_check.ipynb       # loads one checkpoint, verifies it runs
│   └── 02_main_workflow.ipynb      # end-to-end pipeline, Colab-friendly
├── scripts/
│   ├── setup_imagenet100_val.py    # build ImageNet-100 val/ from ILSVRC2012 tar
│   ├── extract_features.py         # CLS features for downstream eval
│   ├── linear_probe.py             # linear-probe accuracy → results/linear_probe.json
│   ├── knn_eval.py                 # k-NN accuracy → results/knn.json
│   ├── extract_cka_features.py    # CLS features for cross-PE CKA
│   ├── compute_cka.py              # cross-PE linear CKA → cka_analysis/cka_summary.csv
│   ├── plot_cka_heatmap.py         # cka_summary.csv → cka_heatmap.{pdf,png}
│   └── analyze_results.py          # paper tables + paired tests from results/
│
├── cka_analysis/                   # small CKA summary (seed 0, primary)
│   ├── cka_summary.csv             # within-PE + cross-PE CKA per layer (long format)
│   ├── cka_results.npz             # raw within-PE + cross-PE + cross-layer matrices
│   ├── cka_heatmap.pdf             # Appendix A.3 figure (PDF)
│   └── cka_heatmap.png             # Appendix A.3 figure (PNG)
├── cka_analysis_seed1/             # small CKA summary (seed 1, replication, Appendix A.1)
│   ├── cka_summary.csv
│   └── cka_results.npz
└── results/                        # downstream evaluation outputs
    ├── linear_probe.json           # linear-probe accuracy (5 datasets × 12 models)
    ├── knn.json                    # k-NN accuracy for k ∈ {1, 5, 10, 20, 50}
    └── analysis/
        └── summary.csv             # per-PE × per-dataset means, paired tests
```

**Not in this repository** (download separately):

- `<checkpoint_root>/` — 12 ViT-Base `.pth` checkpoints trained by the authors (~3.8 GB; Google Drive link in *Trained models* below)
- `features/<pe>_seed<s>_<dataset>.npz` — 60 downstream feature files (~4 GB; produced by `extract_features.py`)
- `cka_features/<pe>_seed<s>_cka_features.npz` — 12 per-layer CKA feature files (one per model; produced by `extract_cka_features.py`)
- `cka_features_seed1/...` — same, second stimulus seed (Appendix A.1 replication)

### Script-to-output mapping

| Script | Purpose | Output |
| --- | --- | --- |
| `setup_imagenet100_val.py` | Extracts the 100 selected classes from the ILSVRC2012 validation tar into an ImageFolder-compatible `val/` directory (50 images per class). | `<output_dir>/val/<class>/` |
| `extract_features.py` | Per (model, downstream dataset): forwards images through the frozen backbone and saves the CLS features for the linear-probe and k-NN classifiers. | `<DATA_HOME>/features/<pe>_seed<s>_<dataset>.npz` (60 files, ~4 GB total) |
| `linear_probe.py` | Trains a multinomial logistic-regression head on top of frozen features for each (model, dataset). | `results/linear_probe.json` |
| `knn_eval.py` | Cosine-distance k-NN over the same frozen features for k ∈ {1, 5, 10, 20, 50}. | `results/knn.json` |
| `extract_cka_features.py` | For each model: forwards a fixed stimulus subset (2000 ImageNet-100 val images) through the model and saves the CLS-token activations after every transformer block in a single `.npz` per model. | `<DATA_HOME>/cka_features/<pe>_seed<s>_cka_features.npz` |
| `compute_cka.py` | Computes linear CKA both within each PE family (across seeds) and between every PE pair, at every transformer block; also computes cross-layer CKA for one representative model per PE family. | `cka_analysis/cka_summary.csv`, `cka_analysis/cka_results.npz` |
| `plot_cka_heatmap.py` | Renders the 6 cross-PE pairs × 12 layers heatmap (Appendix A.3) with the peak-divergence column highlighted. | `cka_analysis/cka_heatmap.{pdf,png}` |
| `analyze_results.py` | Aggregates `linear_probe.json` and `knn.json` into the per-dataset tables in the paper, computes paired tests, and writes a per-PE summary table. | `results/analysis/summary.csv` |

---

## Trained models

Twelve ViT-Base checkpoints were trained by the authors as part of this
study (4 PE families × 3 seeds, all trained from scratch on ImageNet-100
for 300 epochs at 224×224 with an identical recipe; the only thing that
differs between checkpoints is the positional-encoding implementation
and the random seed). The full set (~3.8 GB) is hosted on Google Drive:

- **Our ImageNet-100 ViT-Base models:** [drive.google.com/.../1WRhjaR3WZHIi2fTi9xcrIBJkBXZddMM9](https://drive.google.com/drive/folders/1WRhjaR3WZHIi2fTi9xcrIBJkBXZddMM9)

The folder layout expected by `model_loader.py` is:

```
<models_dir>/
├── learned_seed42/best_model.pth
├── learned_seed123/best_model.pth
├── learned_seed456/best_model.pth
├── sinusoidal_seed42/best_model.pth
├── ...
└── alibi_seed456/best_model.pth
```

The Zenodo deposit (DOI TBA on acceptance) archives this code repository
together with the Google Drive link above, providing a stable, citable
record of the artifacts used in this paper. The checkpoint files
themselves remain on Google Drive due to size (~3.8 GB).

---

## Prerequisites

Before running the notebook or the CLI workflow, anyone reproducing these
results needs to obtain three things and set one path. Result folders
(`features/`, `results/`, `cka_features/`, `cka_analysis/`, …) are created
automatically on first run — no manual `mkdir` needed.

**1. Our trained ViT-Base checkpoints (required)**

The twelve ViT-Base models used in this study were trained by the authors
on ImageNet-100, with identical training recipe across PE families, as
described in the paper. The resulting checkpoints are hosted on Google
Drive — see the *Trained models* section above for the link. Place the
unpacked folder anywhere with enough disk space (~3.8 GB) and use that
path as `<CHECKPOINT_ROOT>` (CLI) or `CHECKPOINT_ROOT` (notebook). The
expected internal layout is documented in *Trained models*.

**2. ImageNet-1k validation tar (required for CKA and pretraining only)**

The CKA experiments use a fixed 2000-image subset of the ImageNet-100
validation split. Building that subset needs the original
`ILSVRC2012_img_val.tar` from
[image-net.org](https://www.image-net.org/download.php) — the file is not
redistributed here for licensing reasons.

The class list (`data/imagenet100_classes.txt`) and the val-image →
class-id mapping (`data/val_labels.txt`) are shipped in this repository,
so the only path you need to set is where the tar lives. In the notebook
this is the `IMAGENET_TAR` variable in the section-6 setup cell; on the
CLI it is `--tar_path` to `setup_imagenet100_val.py`.

The downstream-transfer half of the pipeline (linear probe + k-NN, steps
1 – 5 of the notebook) does **not** require this tar. If you only want
to reproduce Table 1 and skip the CKA mechanism analysis, you can ignore
this step entirely.

**3. Downstream datasets (automatic)**

Food-101, Oxford-IIIT Pets, FGVC Aircraft, Oxford Flowers-102 and DTD
are auto-downloaded by `torchvision` on first use; the cache location is
the `--data_root` argument (CLI) or `DATA_ROOT` (notebook), and a few GB
of free space is enough. No manual download required.

**4. One path decision: `<DATA_HOME>`**

Pick one persistent directory where the generated features, intermediate
results, and aggregated tables will be written. In Colab this is
typically your Google Drive (the default path in the notebook is
`/content/drive/MyDrive/pe_transfer_experiment`); for local execution
it can be any folder with enough disk space (~10 GB to be comfortable
once everything is generated). The notebook reads this from the
`DATA_HOME` variable in the 1.4 path-constants cell. The CLI uses
explicit `--output_dir` flags per step — see *Recommended data layout*
under the Manual CLI workflow.

---

## Reproducing the results

### Quick start (notebook)

The fastest path for the downstream-transfer half of the pipeline is
[`notebooks/02_main_workflow.ipynb`](notebooks/02_main_workflow.ipynb).
It clones this repo, mounts Drive for checkpoint and dataset access, and
walks through:

1. Feature extraction (12 models × 5 downstream datasets = 60 `.npz` files)
2. Linear probe evaluation (C-grid search, LBFGS)
3. k-NN evaluation (k ∈ {1, 5, 10, 20, 50}, cosine)
4. Result analysis (per-PE tables, Spearman cross-dataset consistency,
   LP vs k-NN agreement)
5. CKA pipeline (validation-set setup, per-layer feature extraction,
   within-PE + cross-PE CKA)

For a minimal smoke test that only loads one checkpoint and verifies the
environment, use
[`notebooks/01_sanity_check.ipynb`](notebooks/01_sanity_check.ipynb).

Both notebooks have a header section titled **🔧 Configuration required**
that lists the small number of paths (`CHECKPOINT_ROOT`, `DATA_HOME`,
`IMAGENET_TAR`) you must edit before running. Cells that require editing
are flagged inline with `>>> USER CONFIGURATION REQUIRED <<<` banners; all
other cells use derived paths or ephemeral `/content/` storage and need
no changes.

### Manual CLI workflow

The notebook is a thin wrapper over CLI commands. All scripts are invoked
as Python modules from the repository root; run `python -m scripts.<name> --help`
for the per-script flags. The command sequence below reproduces all files
shipped under `results/` and `cka_analysis/`. Replace
`<CHECKPOINT_ROOT>`, `<DATA_HOME>`, and `<IMAGENET_VAL_ROOT>` with paths
on your machine — see *Recommended data layout* below.

**1. Prepare ImageNet-100 validation set**

```bash
python -m scripts.setup_imagenet100_val \
    --tar_path     "/path/to/ILSVRC2012_img_val.tar" \
    --labels_path  "data/val_labels.txt" \
    --classes_path "data/imagenet100_classes.txt" \
    --output_dir   "<IMAGENET_VAL_ROOT>"
```

The 100 class IDs and the ImageNet-1k val → class mapping are shipped in
`data/`. The ILSVRC2012 validation tar is **not** redistributed in this
repository — obtain it from
[image-net.org](https://www.image-net.org/download.php) under the
ImageNet terms of access.

**2. Extract downstream features**

```bash
python -m scripts.extract_features \
    --checkpoint_root "<CHECKPOINT_ROOT>" \
    --data_root       "<DATA_HOME>/datasets" \
    --output_dir      "<DATA_HOME>/features" \
    --batch_size 128 \
    --num_workers 4 \
    --skip_existing
```

Downstream datasets (Food-101, Oxford-IIIT Pets, FGVC Aircraft, Oxford
Flowers-102, DTD) are auto-downloaded by `torchvision` on first run and
cached under `--data_root`. The `--skip_existing` flag lets the script
resume safely if interrupted: 12 models × 5 datasets = 60 `.npz` files
are produced (~4 GB total).

**3. Linear probe and k-NN evaluation**

```bash
python -m scripts.linear_probe \
    --features_dir "<DATA_HOME>/features" \
    --output_path  "results/linear_probe.json"

python -m scripts.knn_eval \
    --features_dir "<DATA_HOME>/features" \
    --output_path  "results/knn.json"
```

Linear probe uses logistic regression with a C-grid search
(C ∈ {0.1, 1.0, 10.0}, LBFGS solver). k-NN uses cosine distance with
L2-normalised features for k ∈ {1, 5, 10, 20, 50}.

**4. CKA feature extraction + computation**

```bash
python -m scripts.extract_cka_features \
    --checkpoint_root    "<CHECKPOINT_ROOT>" \
    --imagenet_val_root  "<IMAGENET_VAL_ROOT>" \
    --output_dir         "<DATA_HOME>/cka_features" \
    --n_stimuli      2000 \
    --stimulus_seed  0 \
    --skip_existing

python -m scripts.compute_cka \
    --cka_features_dir "<DATA_HOME>/cka_features" \
    --output_dir       "cka_analysis"
```

`extract_cka_features.py` selects a fixed 2000-image stimulus subset from
the ImageNet-100 validation set (deterministic for a given
`--stimulus_seed`) and saves CLS-token activations after every
transformer block in a single `.npz` per model
(`<pe>_seed<s>_cka_features.npz` with keys `layer_0` … `layer_11`).

`compute_cka.py` writes both a binary results bundle and a long-format
CSV:

- `cka_analysis/cka_results.npz` — within-PE, cross-PE, and cross-layer matrices
- `cka_analysis/cka_summary.csv` — `analysis, layer, key1, key2, cka` rows
  (both `within_pe` and `cross_pe` analyses)

To reproduce the stimulus-replication result reported in Appendix A.1,
re-run step 4 with `--stimulus_seed 1`, `--output_dir <DATA_HOME>/cka_features_seed1`,
and `--output_dir cka_analysis_seed1` for the two steps respectively.

**5. CKA heatmap (Appendix A.3 figure)**

```bash
python -m scripts.plot_cka_heatmap \
    --cka_analysis_dir cka_analysis
```

The script reads `<cka_analysis_dir>/cka_summary.csv` and writes
`cka_heatmap.{pdf,png}` to the same directory. With no arguments it
defaults to the `cka_analysis/` directory at the repository root. For
the seed-1 replication, pass `--cka_analysis_dir cka_analysis_seed1`.

**6. Paper tables and paired tests**

```bash
python -m scripts.analyze_results \
    --linear_probe "results/linear_probe.json" \
    --knn          "results/knn.json" \
    --output_dir   "results/analysis"
```

### Recommended data layout

Because the pretrained checkpoints and feature files are large (several
GB combined), it is convenient to keep them outside the Git working tree.
A natural layout is:

```
<DATA_HOME>/                        # any location with sufficient disk space
├── Trained models_ImageNet100/    # 12 checkpoints (downloaded — see Trained models)
├── datasets/                       # torchvision auto-download cache
├── features/                       # produced by extract_features.py
├── cka_features/                   # produced by extract_cka_features.py
└── cka_features_seed1/             # second stimulus seed

vit-pe-transfer/                    # this Git repository (kept small)
└── (code + small results)
```

In the Colab notebooks `<DATA_HOME>` is your Google Drive
(`/content/drive/MyDrive/pe_transfer_experiment/`). For local execution
it can be any directory.

---

## Notes on local execution

All scripts accept their input and output paths as CLI arguments, so no
code changes are needed to relocate the pipeline. A few practical points
beyond what is covered in *Prerequisites*:

- **ImageNet-100 dataset structure** required by the feature-extraction
  and CKA scripts is the standard ImageFolder layout: one subdirectory
  per class, with image files inside. Pass the path to the parent of the
  class subdirectories as `--imagenet_val_root` (for CKA) or
  `--val_dir` (where applicable).

- **GPU memory.** Feature extraction is the only step that benefits from
  a high-memory GPU. Linear probe, k-NN, and CKA computation are
  CPU-friendly. If you hit out-of-memory on your card, reduce
  `--batch_size` (default 128).

- **Hardware reported in the paper.** Pretraining used a mixed pool of
  H100 and A100 sessions. Downstream evaluation and CKA analysis used a
  single NVIDIA RTX PRO 6000 Blackwell Server Edition (102 GB).

---

## Key results

### Linear-probe accuracy (mean ± std over 3 seeds, %)

| PE         | Food-101     | Pets         | Aircraft     | Flowers      | DTD          | **Mean**  |
| ---------- | ------------ | ------------ | ------------ | ------------ | ------------ | --------- |
| Learned    | 57.76 ± 0.26 | 67.60 ± 0.42 | 33.71 ± 0.45 | 64.84 ± 0.93 | 47.94 ± 1.03 | 54.37     |
| Sinusoidal | 58.43 ± 0.36 | 70.66 ± 0.23 | 35.79 ± 0.47 | 67.09 ± 0.38 | 49.84 ± 0.66 | 56.36     |
| ALiBi      | 57.35 ± 0.24 | 70.48 ± 0.66 | 35.56 ± 0.54 | 64.41 ± 0.50 | 47.54 ± 0.37 | 55.07     |
| **RoPE**   | **60.14 ± 0.13** | **76.20 ± 0.46** | **40.02 ± 0.31** | **67.96 ± 0.41** | **50.90 ± 0.41** | **59.04** |

Differences are significant at p < 0.01 on 4 of 5 datasets (paired t-test
across seeds; see `results/analysis/`). The k-NN ranking is identical and
is reported in full in Appendix A.2.

### Cross-PE CKA (peak divergence, all 6 PE pairs)

| Layer | Range across 6 pairs |
| ----: | -------------------- |
|  0    | 0.91 – 0.97          |
|  **9** | **0.69 – 0.72** (peak) |
| 11    | 0.74 – 0.79 (rebound) |

The peak layer is **9 for all six PE pairs under both stimulus seeds**;
the max absolute CKA difference between stimulus seeds is 0.0023 (Appendix A.1).

Full per-layer tables and the heatmap rendering are produced by
`compute_cka.py` and `plot_cka_heatmap.py` respectively.

---

## Paper and citation

The paper is currently under submission. Citation details will be added
once the submission status is finalized. In the meantime, please reference
this repository directly if you build on the code or use the results.

```bibtex
@misc{bandjur2026petransfer,
  title  = {How Positional Encoding Shapes Transferable Representations in Vision Transformers},
  author = {Bandjur, Djoko and Bandjur, Milos and Micic, Aleksandar},
  year   = {2026},
  note   = {Manuscript under submission.
            Code: \url{https://github.com/djokobandjur/vit-pe-transfer}}
}
```

---

## License

This repository uses a dual-licensing scheme that reflects the different
nature of its contents:

- **Source code** (all `.py` files, both notebooks under `notebooks/`)
  is released under the **MIT License** — see [`LICENSE`](LICENSE).

- **Result files and documentation** (the JSON and CSV files under
  `results/` and `cka_analysis/`, the generated figures under
  `cka_analysis/`, this README, and the Zenodo deposit of this repository)
  are released under the **Creative Commons Attribution 4.0 International
  License** (CC BY 4.0). Full text:
  [creativecommons.org/licenses/by/4.0/](https://creativecommons.org/licenses/by/4.0/).

- **Trained model checkpoints** (hosted on Google Drive; see *Trained models*
  above) are released under **CC BY 4.0 for research purposes**. The
  ImageNet-100 models are derivative artifacts of the ImageNet-1k dataset
  and remain subject to the
  [ImageNet terms of access](https://www.image-net.org/download.php) for
  any redistribution or commercial use.

- **The ImageNet-1k validation images** required to reproduce the
  ImageNet-100 experiments are governed by the
  [ImageNet terms of access](https://www.image-net.org/download.php) and
  are not redistributed in this repository.

If you use the code, cite the repository under MIT terms. If you use the
results, figures, or trained models in a derivative work, cite under
CC BY 4.0 terms (attribution required).
