"""
Aggregate linear probe + kNN results into summary tables.

Produces:
  1. Per-PE × per-dataset table (mean over seeds, with std)
  2. Per-PE ranking by dataset
  3. Cross-dataset ranking consistency (Spearman correlation)
  4. Linear probe vs kNN agreement

Output: prints to stdout + saves as text + CSV.

Usage:
    python -m scripts.analyze_results \\
        --linear_probe /content/drive/MyDrive/pe_transfer_experiment/results/linear_probe.json \\
        --knn /content/drive/MyDrive/pe_transfer_experiment/results/knn.json \\
        --output_dir /content/drive/MyDrive/pe_transfer_experiment/results/analysis
"""

import argparse
import json
import os
import numpy as np
from collections import defaultdict
from scipy.stats import spearmanr

from models import PE_TYPES, SEEDS
from data import DATASETS, DATASET_INFO


def aggregate_by_pe_dataset(per_combination, score_key="best_test_acc"):
    """
    Aggregate (pe_type, seed, dataset) results -> {(pe_type, dataset): [seed_accuracies]}.
    """
    aggregated = defaultdict(list)
    for key, result in per_combination.items():
        # Parse key: "{pe_type}_seed{seed}_{dataset_name}"
        # PE types and dataset names contain underscores, so split carefully
        for pe in PE_TYPES:
            if key.startswith(f"{pe}_seed"):
                # Remaining: "{seed}_{dataset_name}"
                remainder = key[len(f"{pe}_seed"):]
                # Find seed (numeric prefix until underscore)
                for i, c in enumerate(remainder):
                    if not c.isdigit():
                        break
                seed = int(remainder[:i])
                dataset_name = remainder[i + 1:]  # skip underscore
                if score_key in result:
                    aggregated[(pe, dataset_name)].append(result[score_key])
                break
    return aggregated


def print_mean_std_table(aggregated, datasets, title=""):
    """Print PE × dataset table with mean ± std."""
    print(f"\n{'=' * 80}")
    print(f"{title}")
    print(f"{'=' * 80}")

    # Header
    header = f"{'PE Type':<14}"
    for ds in datasets:
        header += f"{ds:>18}"
    print(header)
    print("-" * len(header))

    # Rows
    for pe in PE_TYPES:
        row = f"{pe:<14}"
        for ds in datasets:
            scores = aggregated.get((pe, ds), [])
            if scores:
                mean = np.mean(scores)
                std = np.std(scores)
                n = len(scores)
                row += f"{mean:>10.4f} ± {std:.4f}" if n > 1 else f"{mean:>18.4f}"
            else:
                row += f"{'--':>18}"
        print(row)


def compute_rankings(aggregated, datasets):
    """For each dataset, rank PE types by mean accuracy."""
    rankings = {}
    for ds in datasets:
        pe_means = {}
        for pe in PE_TYPES:
            scores = aggregated.get((pe, ds), [])
            if scores:
                pe_means[pe] = np.mean(scores)
        # Sort by mean accuracy descending
        ranked = sorted(pe_means.items(), key=lambda x: -x[1])
        rankings[ds] = [pe for pe, _ in ranked]
    return rankings


def print_rankings(rankings, title=""):
    """Print per-dataset rankings."""
    print(f"\n{'=' * 80}")
    print(f"{title}")
    print(f"{'=' * 80}")
    print(f"{'Dataset':<20} {'1st':<14} {'2nd':<14} {'3rd':<14} {'4th':<14}")
    print("-" * 80)
    for ds, ranking in rankings.items():
        ranked_str = ""
        for pe in ranking:
            ranked_str += f"{pe:<14}"
        print(f"{ds:<20} {ranked_str}")


def cross_dataset_consistency(rankings):
    """Compute pairwise Spearman correlation between dataset rankings."""
    datasets = list(rankings.keys())
    n = len(datasets)
    print(f"\n{'=' * 80}")
    print(f"Cross-dataset Ranking Consistency (Spearman ρ)")
    print(f"{'=' * 80}")

    # Build rank vectors
    rank_vectors = {}
    for ds, ranking in rankings.items():
        # rank_vectors[ds][pe] = rank (1 = best, 4 = worst)
        rank_vectors[ds] = {pe: rank + 1 for rank, pe in enumerate(ranking)}

    # Pairwise correlations
    header = f"{'':14}"
    for ds in datasets:
        header += f"{ds[:12]:>14}"
    print(header)
    print("-" * len(header))

    for ds1 in datasets:
        row = f"{ds1[:12]:<14}"
        for ds2 in datasets:
            r1 = [rank_vectors[ds1][pe] for pe in PE_TYPES]
            r2 = [rank_vectors[ds2][pe] for pe in PE_TYPES]
            rho, _ = spearmanr(r1, r2)
            row += f"{rho:>14.3f}"
        print(row)


def linear_vs_knn_agreement(lp_rankings, knn_rankings):
    """For each dataset, compute Spearman correlation between LP and kNN rankings."""
    print(f"\n{'=' * 80}")
    print(f"Linear Probe vs kNN Ranking Agreement (Spearman ρ per dataset)")
    print(f"{'=' * 80}")
    print(f"{'Dataset':<20} {'Spearman ρ':<14}")
    print("-" * 40)

    for ds in lp_rankings:
        if ds not in knn_rankings:
            continue
        lp_rank = {pe: rank for rank, pe in enumerate(lp_rankings[ds])}
        knn_rank = {pe: rank for rank, pe in enumerate(knn_rankings[ds])}
        r1 = [lp_rank[pe] for pe in PE_TYPES]
        r2 = [knn_rank[pe] for pe in PE_TYPES]
        rho, _ = spearmanr(r1, r2)
        print(f"{ds:<20} {rho:<14.3f}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--linear_probe", required=True,
                        help="Path to linear_probe.json")
    parser.add_argument("--knn", required=True,
                        help="Path to knn.json")
    parser.add_argument("--knn_k", type=int, default=20,
                        help="Which k to use for kNN analysis (default 20)")
    parser.add_argument("--output_dir", required=True)
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    # Load
    with open(args.linear_probe) as f:
        lp_data = json.load(f)
    with open(args.knn) as f:
        knn_data = json.load(f)

    lp_combinations = lp_data["per_combination"]
    knn_combinations = knn_data["per_combination"]

    # Aggregate linear probe
    lp_aggregated = aggregate_by_pe_dataset(lp_combinations, score_key="best_test_acc")

    # Aggregate kNN at chosen k
    # The kNN result keys are integers in the per-combination dict
    # but JSON serializes ints as strings; handle both
    knn_aggregated = defaultdict(list)
    k_str = str(args.knn_k)
    for key, result in knn_combinations.items():
        for pe in PE_TYPES:
            if key.startswith(f"{pe}_seed"):
                remainder = key[len(f"{pe}_seed"):]
                for i, c in enumerate(remainder):
                    if not c.isdigit():
                        break
                seed = int(remainder[:i])
                dataset_name = remainder[i + 1:]
                # kNN result has integer k keys
                k_result = result.get(k_str) or result.get(args.knn_k)
                if k_result and "test_acc" in k_result:
                    knn_aggregated[(pe, dataset_name)].append(k_result["test_acc"])
                break

    # Compute rankings
    lp_rankings = compute_rankings(lp_aggregated, DATASETS)
    knn_rankings = compute_rankings(knn_aggregated, DATASETS)

    # Print
    print_mean_std_table(lp_aggregated, DATASETS,
                          title="Linear Probe Accuracy (Test, mean ± std across seeds)")
    print_mean_std_table(knn_aggregated, DATASETS,
                          title=f"kNN (k={args.knn_k}) Accuracy (Test, mean ± std across seeds)")

    print_rankings(lp_rankings, title="Linear Probe: PE Ranking per Dataset (1st = best)")
    print_rankings(knn_rankings, title=f"kNN (k={args.knn_k}): PE Ranking per Dataset (1st = best)")

    cross_dataset_consistency(lp_rankings)
    cross_dataset_consistency(knn_rankings)

    linear_vs_knn_agreement(lp_rankings, knn_rankings)

    # Save as CSV
    csv_path = os.path.join(args.output_dir, "summary.csv")
    with open(csv_path, "w") as f:
        f.write("metric,pe_type,dataset,mean,std,n_seeds\n")
        for (pe, ds), scores in lp_aggregated.items():
            f.write(f"linear_probe,{pe},{ds},{np.mean(scores):.4f},{np.std(scores):.4f},{len(scores)}\n")
        for (pe, ds), scores in knn_aggregated.items():
            f.write(f"knn_k{args.knn_k},{pe},{ds},{np.mean(scores):.4f},{np.std(scores):.4f},{len(scores)}\n")
    print(f"\n[SAVED] Summary CSV: {csv_path}")


if __name__ == "__main__":
    main()
