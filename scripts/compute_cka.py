"""
CKA (Centered Kernel Alignment) computation and analysis.

Loads per-layer features extracted by extract_cka_features.py and computes:
  1. Within-PE consistency: CKA across seeds within same PE family (per layer)
  2. Cross-PE similarity: CKA across PE families (mean across seeds, per layer)
  3. Cross-layer similarity: CKA between different layers of same model

Output: NPZ files and CSV summary, plus printed tables.

Usage:
    python -m scripts.compute_cka \\
        --cka_features_dir "/content/drive/MyDrive/pe_transfer_experiment/cka_features" \\
        --output_dir "/content/drive/MyDrive/pe_transfer_experiment/cka_analysis"
"""

import argparse
import os
import json
import numpy as np
from tqdm import tqdm
from itertools import combinations

from models import PE_TYPES, SEEDS


# ----------------------------------------------------------------------
# Linear CKA implementation
# ----------------------------------------------------------------------

def gram_linear(x):
    """Linear Gram matrix: x @ x.T"""
    return x @ x.T


def center_gram(gram):
    """Double-centered Gram matrix (subtract row+col means, add overall mean)."""
    n = gram.shape[0]
    means = gram.mean(axis=0, keepdims=True)
    means -= means.mean() / 2
    return gram - means - means.T


def cka(x, y):
    """
    Linear CKA between two feature matrices.

    Args:
        x: [N, d1] feature matrix
        y: [N, d2] feature matrix (same N as x)

    Returns:
        Scalar in [0, 1] (or sometimes slightly above 1 due to numerical issues; clip)
    """
    gx = center_gram(gram_linear(x.astype(np.float64)))
    gy = center_gram(gram_linear(y.astype(np.float64)))
    hsic_xy = (gx * gy).sum()
    hsic_xx = (gx * gx).sum()
    hsic_yy = (gy * gy).sum()
    denom = np.sqrt(hsic_xx * hsic_yy)
    if denom < 1e-12:
        return 0.0
    return float(hsic_xy / denom)


# ----------------------------------------------------------------------
# Analysis functions
# ----------------------------------------------------------------------

def load_model_features(features_dir, pe_type, seed):
    """Load all 12 layers for one model."""
    path = os.path.join(features_dir, f"{pe_type}_seed{seed}_cka_features.npz")
    if not os.path.exists(path):
        return None
    data = np.load(path)
    return [data[f"layer_{i}"] for i in range(12)]


def within_pe_consistency(features_dir):
    """
    For each PE family, compute pairwise CKA across seeds (per layer).

    Returns: dict {pe_type: [mean_cka_layer_0, mean_cka_layer_1, ..., mean_cka_layer_11]}
    """
    print("\n[1/3] WITHIN-PE consistency (seed pairs within each PE family)")
    print("-" * 60)
    results = {}
    for pe in tqdm(PE_TYPES, desc="PE families"):
        model_features = {}
        for seed in SEEDS:
            feats = load_model_features(features_dir, pe, seed)
            if feats is None:
                print(f"  [SKIP] {pe}_seed{seed} missing")
                continue
            model_features[seed] = feats
        if len(model_features) < 2:
            continue

        seeds_present = sorted(model_features.keys())
        layer_means = []
        for layer_idx in range(12):
            pair_ckas = []
            for s1, s2 in combinations(seeds_present, 2):
                pair_ckas.append(cka(model_features[s1][layer_idx],
                                      model_features[s2][layer_idx]))
            layer_means.append(np.mean(pair_ckas))
        results[pe] = layer_means
    return results


def cross_pe_similarity(features_dir):
    """
    For each pair of PE families, compute mean CKA across all seed combinations (per layer).

    Returns: dict {(pe1, pe2): [mean_cka_layer_0, ..., mean_cka_layer_11]}
    """
    print("\n[2/3] CROSS-PE similarity (PE family pairs, mean over seed combinations)")
    print("-" * 60)
    # Load all model features
    all_features = {}
    for pe in PE_TYPES:
        for seed in SEEDS:
            feats = load_model_features(features_dir, pe, seed)
            if feats is not None:
                all_features[(pe, seed)] = feats

    results = {}
    for pe1, pe2 in tqdm(list(combinations(PE_TYPES, 2)) + [(p, p) for p in PE_TYPES],
                         desc="PE pairs"):
        seeds1 = [s for (p, s) in all_features.keys() if p == pe1]
        seeds2 = [s for (p, s) in all_features.keys() if p == pe2]
        layer_means = []
        for layer_idx in range(12):
            pair_ckas = []
            for s1 in seeds1:
                for s2 in seeds2:
                    if pe1 == pe2 and s1 >= s2:
                        continue  # skip self-pairs and duplicates
                    pair_ckas.append(cka(all_features[(pe1, s1)][layer_idx],
                                          all_features[(pe2, s2)][layer_idx]))
            if pair_ckas:
                layer_means.append(np.mean(pair_ckas))
            else:
                layer_means.append(np.nan)
        results[(pe1, pe2)] = layer_means
    return results


def cross_layer_within_model(features_dir, pe_type, seed):
    """
    Compute 12x12 layer-vs-layer CKA matrix for a single model.

    Returns: [12, 12] array (symmetric, diag=1).
    """
    feats = load_model_features(features_dir, pe_type, seed)
    if feats is None:
        return None
    mat = np.zeros((12, 12))
    for i in range(12):
        for j in range(i, 12):
            val = cka(feats[i], feats[j])
            mat[i, j] = val
            mat[j, i] = val
    return mat


# ----------------------------------------------------------------------
# Print helpers
# ----------------------------------------------------------------------

def print_within_pe(results):
    print("\n" + "=" * 80)
    print("WITHIN-PE seed consistency (mean CKA across seed pairs, per layer)")
    print("=" * 80)
    print(f"{'Layer':<8}" + ''.join(f'{pe:>13}' for pe in PE_TYPES))
    print('-' * 60)
    for layer in range(12):
        row = f'{layer:<8}'
        for pe in PE_TYPES:
            val = results.get(pe, [np.nan]*12)[layer]
            row += f'{val:>13.4f}'
        print(row)

    print('-' * 60)
    row = f"{'Mean':<8}"
    for pe in PE_TYPES:
        vals = results.get(pe, [])
        row += f'{np.mean(vals):>13.4f}' if vals else f'{"--":>13}'
    print(row)


def print_cross_pe_at_layer(results, layer_idx):
    print(f"\nCross-PE CKA at layer {layer_idx}:")
    print(f"{'':<13}" + ''.join(f'{pe:>13}' for pe in PE_TYPES))
    print('-' * 65)
    for pe1 in PE_TYPES:
        row = f'{pe1:<13}'
        for pe2 in PE_TYPES:
            # Get value (handle both orderings)
            val = results.get((pe1, pe2), results.get((pe2, pe1), [np.nan]*12))[layer_idx]
            row += f'{val:>13.4f}'
        print(row)


def print_cross_pe_summary(results):
    """For each PE pair, mean across all layers."""
    print("\n" + "=" * 80)
    print("CROSS-PE similarity (mean CKA across all 12 layers)")
    print("=" * 80)
    print(f"{'':<13}" + ''.join(f'{pe:>13}' for pe in PE_TYPES))
    print('-' * 65)
    for pe1 in PE_TYPES:
        row = f'{pe1:<13}'
        for pe2 in PE_TYPES:
            vals = results.get((pe1, pe2), results.get((pe2, pe1), []))
            row += f'{np.mean(vals):>13.4f}' if vals else f'{"--":>13}'
        print(row)


def print_cross_pe_by_layer(results):
    """Show how cross-PE similarity changes across layers."""
    print("\n" + "=" * 80)
    print("CROSS-PE similarity per layer (off-diagonal pairs only)")
    print("=" * 80)
    pe_pairs = list(combinations(PE_TYPES, 2))
    header = f"{'Layer':<8}" + ''.join(f'{p1[:4]}-{p2[:4]:<8}' for p1, p2 in pe_pairs)
    print(header)
    print('-' * len(header))
    for layer in range(12):
        row = f'{layer:<8}'
        for p1, p2 in pe_pairs:
            val = results.get((p1, p2), results.get((p2, p1), [np.nan]*12))[layer]
            row += f'{val:>13.4f}'
        print(row)


# ----------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cka_features_dir", required=True)
    parser.add_argument("--output_dir", required=True)
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    print("=" * 80)
    print("CKA ANALYSIS")
    print("=" * 80)

    # 1. Within-PE consistency
    within = within_pe_consistency(args.cka_features_dir)
    print_within_pe(within)

    # 2. Cross-PE similarity
    cross = cross_pe_similarity(args.cka_features_dir)
    print_cross_pe_summary(cross)
    print_cross_pe_by_layer(cross)
    # Key layers
    print_cross_pe_at_layer(cross, 0)
    print_cross_pe_at_layer(cross, 6)
    print_cross_pe_at_layer(cross, 11)

    # 3. Cross-layer within-model (just one representative per PE family)
    print("\n" + "=" * 80)
    print("CROSS-LAYER similarity within representative models (seed=42)")
    print("=" * 80)
    cross_layer_matrices = {}
    for pe in PE_TYPES:
        mat = cross_layer_within_model(args.cka_features_dir, pe, SEEDS[0])
        if mat is not None:
            cross_layer_matrices[pe] = mat
            # Print summary: similarity of layer 0 to other layers
            print(f"\n{pe} (seed={SEEDS[0]}), layer 0 vs other layers:")
            for j in range(12):
                print(f"  L0 vs L{j:2d}: {mat[0, j]:.4f}")

    # Save all results
    np.savez_compressed(
        os.path.join(args.output_dir, "cka_results.npz"),
        within_pe=within,
        cross_pe={f"{p1}_{p2}": v for (p1, p2), v in cross.items()},
        cross_layer={pe: mat for pe, mat in cross_layer_matrices.items()},
    )

    # CSV summary
    csv_path = os.path.join(args.output_dir, "cka_summary.csv")
    with open(csv_path, "w") as f:
        f.write("analysis,layer,key1,key2,cka\n")
        for pe, vals in within.items():
            for l, v in enumerate(vals):
                f.write(f"within_pe,{l},{pe},{pe},{v:.6f}\n")
        for (p1, p2), vals in cross.items():
            for l, v in enumerate(vals):
                f.write(f"cross_pe,{l},{p1},{p2},{v:.6f}\n")

    print(f"\n[SAVED] Results: {args.output_dir}/cka_results.npz")
    print(f"[SAVED] CSV summary: {csv_path}")


if __name__ == "__main__":
    main()
