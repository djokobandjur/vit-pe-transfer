"""
k-Nearest Neighbors evaluation on cached features.

For each (pe_type, seed, dataset) combination:
  1. Load cached features
  2. L2-normalize (for cosine similarity)
  3. kNN classification with k in {1, 5, 10, 20, 50}
  4. Report test accuracy for each k

Output: JSON file with all (pe_type, seed, dataset) -> accuracy + metadata.

kNN measures "raw" feature quality (no training, no parameters to fit).
Useful complement to linear probe — if both agree, signal is robust.

Usage:
    python -m scripts.knn_eval \\
        --features_dir /content/drive/MyDrive/pe_transfer_experiment/features \\
        --output_path /content/drive/MyDrive/pe_transfer_experiment/results/knn.json
"""

import argparse
import json
import os
import time
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
from tqdm import tqdm

from models import PE_TYPES, SEEDS
from data import DATASETS, DATASET_INFO


K_VALUES = [1, 5, 10, 20, 50]


def l2_normalize(x, eps=1e-8):
    """L2-normalize along last dimension."""
    norm = np.linalg.norm(x, axis=-1, keepdims=True)
    return x / (norm + eps)


def evaluate_knn(features_train, labels_train, features_test, labels_test,
                  k_values=K_VALUES, metric="cosine"):
    """
    kNN evaluation across multiple k values.

    Returns:
        dict: {k: {"test_acc": float, "elapsed_sec": float}}
    """
    if metric == "cosine":
        # Use L2-normalized features with euclidean distance, equivalent to cosine
        features_train = l2_normalize(features_train)
        features_test = l2_normalize(features_test)
        sklearn_metric = "cosine"
    else:
        sklearn_metric = metric

    results = {}
    max_k = max(k_values)

    # Fit once with max_k, then query with different k
    knn = KNeighborsClassifier(
        n_neighbors=max_k,
        metric=sklearn_metric,
        algorithm="brute",
        n_jobs=-1,
    )
    knn.fit(features_train, labels_train)

    # Get distances and indices for max_k neighbors (single query)
    t0 = time.time()
    distances, indices = knn.kneighbors(features_test, n_neighbors=max_k)
    query_time = time.time() - t0

    # Compute accuracy at each k from these indices
    for k in k_values:
        t0 = time.time()
        # Majority vote from first k neighbors
        nearest_labels = labels_train[indices[:, :k]]  # [N_test, k]
        # Mode along axis 1
        preds = np.array([np.bincount(row).argmax() for row in nearest_labels])
        test_acc = accuracy_score(labels_test, preds)
        elapsed = time.time() - t0

        results[k] = {
            "test_acc": float(test_acc),
            "elapsed_sec": elapsed,
        }

    results["_query_time_sec"] = query_time
    return results


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--features_dir", required=True)
    parser.add_argument("--output_path", required=True)
    parser.add_argument("--pe_types", nargs="+", default=PE_TYPES)
    parser.add_argument("--seeds", nargs="+", type=int, default=SEEDS)
    parser.add_argument("--datasets", nargs="+", default=DATASETS)
    parser.add_argument("--k_values", nargs="+", type=int, default=K_VALUES)
    parser.add_argument("--metric", default="cosine", choices=["cosine", "euclidean"])
    args = parser.parse_args()

    os.makedirs(os.path.dirname(args.output_path), exist_ok=True)

    results = {
        "metadata": {
            "k_values": args.k_values,
            "metric": args.metric,
            "pe_types": args.pe_types,
            "seeds": args.seeds,
            "datasets": args.datasets,
        },
        "per_combination": {},
    }

    total = len(args.pe_types) * len(args.seeds) * len(args.datasets)
    print(f"[INFO] kNN eval on {total} (pe_type, seed, dataset) combinations")
    print(f"[INFO] k values: {args.k_values}, metric: {args.metric}")

    pbar = tqdm(total=total)
    total_start = time.time()

    for pe_type in args.pe_types:
        for seed in args.seeds:
            for dataset_name in args.datasets:
                key = f"{pe_type}_seed{seed}_{dataset_name}"
                feat_path = os.path.join(args.features_dir, f"{key}.npz")

                if not os.path.exists(feat_path):
                    print(f"  [SKIP] {key} (features missing)")
                    pbar.update(1)
                    continue

                data = np.load(feat_path)
                features_train = data["features_train"]
                labels_train = data["labels_train"]
                features_test = data["features_test"]
                labels_test = data["labels_test"]

                result = evaluate_knn(
                    features_train, labels_train,
                    features_test, labels_test,
                    k_values=args.k_values, metric=args.metric,
                )
                result["num_classes"] = DATASET_INFO[dataset_name]["num_classes"]
                result["chance"] = 1.0 / result["num_classes"]

                results["per_combination"][key] = result

                # Show k=20 progress (standard reference)
                k20_acc = result.get(20, {}).get("test_acc", 0.0)
                pbar.set_postfix({
                    "dataset": dataset_name,
                    "k20_acc": f"{k20_acc:.3f}",
                })
                pbar.update(1)

    pbar.close()
    total_elapsed = time.time() - total_start
    results["metadata"]["total_elapsed_sec"] = total_elapsed

    with open(args.output_path, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\n[DONE] Total time: {total_elapsed / 60:.1f} min")
    print(f"[DONE] Results saved to: {args.output_path}")
    print(f"[DONE] Combinations completed: {len(results['per_combination'])}")


if __name__ == "__main__":
    main()
