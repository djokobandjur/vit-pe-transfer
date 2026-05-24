#!/usr/bin/env python3
"""
Regenerate the cross-PE CKA heatmap (Appendix A.3) from cka_summary.csv.

This script reads the CKA summary produced by `compute_cka.py` and produces
`cka_heatmap.pdf` and `cka_heatmap.png` identical to the figure included in
the paper. A red rectangle highlights the peak-divergence column (layer 9).

Usage
-----
From the `code/` directory (consistent with the other scripts in this repo):

    python -m scripts.plot_cka_heatmap \
        --cka_analysis_dir ../cka_analysis

Or with no arguments — defaults resolve to the repository's
`cka_analysis/` directory relative to this script's location.

Inputs
------
`<cka_analysis_dir>/cka_summary.csv` with columns:
    analysis, layer, key1, key2, cka

Only rows with `analysis == 'cross_pe'` and `key1 != key2` are plotted
(6 unordered PE pairs across the 12 transformer blocks of ViT-Base).

Outputs
-------
    <cka_analysis_dir>/cka_heatmap.pdf
    <cka_analysis_dir>/cka_heatmap.png
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import pandas as pd


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

# Row order of PE pairs in the heatmap (top to bottom).
# Tuples are (key1, key2) as they appear in cka_summary.csv.
PE_PAIRS: list[tuple[str, str]] = [
    ("learned", "sinusoidal"),
    ("learned", "rope"),
    ("learned", "alibi"),
    ("sinusoidal", "rope"),
    ("sinusoidal", "alibi"),
    ("rope", "alibi"),
]

# Pretty labels for y-axis tick labels.
PE_DISPLAY = {
    "learned": "Learned",
    "sinusoidal": "Sinusoidal",
    "rope": "RoPE",
    "alibi": "ALiBi",
}

# Layer 0..11 for ViT-Base (12 transformer blocks).
NUM_LAYERS = 12

# Column to highlight (peak cross-PE divergence reported in the paper).
PEAK_LAYER = 9

# Colormap bounds. vmin tracks the minimum observed cross-PE CKA (~0.69);
# vmax = 1.0 because CKA is bounded above by 1.
CMAP = "viridis_r"
VMIN = 0.69
VMAX = 1.00

# Text-color threshold: cells with CKA >= this get white text (dark purple/blue
# cells under viridis_r), everything below gets black text (green/yellow cells).
# Tuned so the layer-9 column (peak divergence, ~0.69-0.72, light yellow) keeps
# black text for readability.
TEXT_WHITE_THRESHOLD = 0.88


# ---------------------------------------------------------------------------
# Core logic
# ---------------------------------------------------------------------------

def build_matrix(df: pd.DataFrame) -> np.ndarray:
    """Build a (6, 12) matrix of cross-PE CKA values in the canonical row order."""
    cross = df[df["analysis"] == "cross_pe"].copy()

    matrix = np.full((len(PE_PAIRS), NUM_LAYERS), np.nan, dtype=float)
    for row_idx, (a, b) in enumerate(PE_PAIRS):
        # Accept either ordering of the pair in the CSV.
        mask = (
            ((cross["key1"] == a) & (cross["key2"] == b))
            | ((cross["key1"] == b) & (cross["key2"] == a))
        )
        sub = cross[mask]
        if sub.empty:
            raise ValueError(f"No cross_pe rows found for pair ({a}, {b}).")
        for _, r in sub.iterrows():
            layer = int(r["layer"])
            if 0 <= layer < NUM_LAYERS:
                matrix[row_idx, layer] = float(r["cka"])

    if np.isnan(matrix).any():
        missing = np.argwhere(np.isnan(matrix))
        raise ValueError(f"Missing CKA entries at (row, layer) positions: {missing.tolist()}")

    return matrix


def plot_heatmap(matrix: np.ndarray, out_dir: Path) -> tuple[Path, Path]:
    """Render the heatmap and write PDF + PNG to ``out_dir``."""
    out_dir.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(10, 4.2))

    im = ax.imshow(
        matrix,
        cmap=CMAP,
        vmin=VMIN,
        vmax=VMAX,
        aspect="auto",
    )

    # Axis ticks and labels.
    ax.set_xticks(np.arange(NUM_LAYERS))
    ax.set_xticklabels([str(i) for i in range(NUM_LAYERS)])
    ax.set_yticks(np.arange(len(PE_PAIRS)))
    ax.set_yticklabels(
        [f"{PE_DISPLAY[a]}\u2013{PE_DISPLAY[b]}" for a, b in PE_PAIRS]
    )
    ax.set_xlabel("Transformer block (layer)")

    # Annotate every cell.
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            value = matrix[i, j]
            color = "white" if value >= TEXT_WHITE_THRESHOLD else "black"
            ax.text(
                j, i, f"{value:.2f}",
                ha="center", va="center",
                color=color,
                fontweight="bold",
                fontsize=10,
            )

    # Highlight peak-divergence column.
    rect = mpatches.Rectangle(
        (PEAK_LAYER - 0.5, -0.5),
        width=1.0,
        height=len(PE_PAIRS),
        linewidth=2.5,
        edgecolor="red",
        facecolor="none",
        zorder=5,
    )
    ax.add_patch(rect)

    # Colorbar.
    cbar = fig.colorbar(im, ax=ax, fraction=0.025, pad=0.02)
    cbar.set_label("Cross-PE CKA")

    # Clean borders.
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.tick_params(top=False, bottom=True, left=False, right=False)

    fig.tight_layout()

    pdf_path = out_dir / "cka_heatmap.pdf"
    png_path = out_dir / "cka_heatmap.png"
    fig.savefig(pdf_path, bbox_inches="tight")
    fig.savefig(png_path, bbox_inches="tight", dpi=200)
    plt.close(fig)

    return pdf_path, png_path


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Regenerate the cross-PE CKA heatmap from cka_summary.csv."
    )
    # Default resolves to the repository's cka_analysis/ directory regardless
    # of the current working directory. The script lives at
    # <repo>/code/scripts/plot_cka_heatmap.py, so the repo root is two levels up.
    repo_root = Path(__file__).resolve().parent.parent.parent
    parser.add_argument(
        "--cka_analysis_dir",
        type=Path,
        default=repo_root / "cka_analysis",
        help="Directory containing cka_summary.csv. The heatmap files "
             "cka_heatmap.{pdf,png} are written to the same directory. "
             "Default: <repo>/cka_analysis/.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    csv_path = args.cka_analysis_dir / "cka_summary.csv"
    if not csv_path.is_file():
        raise FileNotFoundError(f"Input CSV not found: {csv_path}")

    df = pd.read_csv(csv_path)
    required_cols = {"analysis", "layer", "key1", "key2", "cka"}
    missing = required_cols - set(df.columns)
    if missing:
        raise ValueError(f"Input CSV is missing required columns: {sorted(missing)}")

    matrix = build_matrix(df)
    pdf_path, png_path = plot_heatmap(matrix, args.cka_analysis_dir)

    print(f"Wrote {pdf_path}")
    print(f"Wrote {png_path}")


if __name__ == "__main__":
    main()
