"""
Linear probing on cached features.

For each (pe_type, seed, dataset) combination:
  1. Load cached features from extract_features.py output
  2. Standardize features (zero mean, unit variance per dim) based on train set
  3. Train a multinomial logistic regression with LBFGS
  4. Search over a small LR / regularization grid (3 values)
  5. Report best test accuracy and metadata

Output: JSON file with all (pe_type, seed, dataset) -> accuracy + metadata.

Usage:
    python -m scripts.linear_probe \\
        --features_dir /content/drive/MyDrive/pe_transfer_experiment/features \\
        --output_path /content/drive/MyDrive/pe_transfer_experiment/results/linear_probe.json
"""

import argparse
import json
import os
import time
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
from tqdm import tqdm

from models import PE_TYPES, SEEDS
from data import DATASETS, DATASET_INFO


# Standard regularization grid (Kornblith et al. ICML 2019 used similar)
# C in scikit-learn = inverse of L2 regularization strength
C_GRID = [0.1, 1.0, 10.0]


def train_linear_probe(features_train, labels_train, features_test, labels_test,
                        c_grid=C_GRID, max_iter=1000, verbose=False):
    """
    Train logistic regression with C-grid search.

    Returns:
        dict with keys:
            best_c, best_test_acc, best_train_acc,
            all_results (list of {c, train_acc, test_acc})
    """
    # Standardize (fit on train, apply to both)
    scaler = StandardScaler()
    features_train_s = scaler.fit_transform(features_train)
    features_test_s = scaler.transform(features_test)

    all_results = []
    best = {"best_test_acc": -1.0}

    for c in c_grid:
        clf = LogisticRegression(
            C=c,
            solver="lbfgs",
            max_iter=max_iter,
            multi_class="multinomial",
            n_jobs=-1,
        )
        clf.fit(features_train_s, labels_train)

        train_pred = clf.predict(features_train_s)
        test_pred = clf.predict(features_test_s)
        train_acc = accuracy_score(labels_train, train_pred)
        test_acc = accuracy_score(labels_test, test_pred)

        all_results.append({"c": c, "train_acc": float(train_acc), "test_acc": float(test_acc)})

        if verbose:
            print(f"    C={c}: train={train_acc:.4f}, test={test_acc:.4f}")

        if test_acc > best["best_test_acc"]:
            best = {
                "best_c": c,
                "best_test_acc": float(test_acc),
                "best_train_acc": float(train_acc),
            }

    best["all_results"] = all_results
    return best


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--features_dir", required=True,
                        help="Directory containing extract_features.py .npz outputs")
    parser.add_argument("--output_path", required=True,
                        help="Path to save results JSON")
    parser.add_argument("--pe_types", nargs="+", default=PE_TYPES)
    parser.add_argument("--seeds", nargs="+", type=int, default=SEEDS)
    parser.add_argument("--datasets", nargs="+", default=DATASETS)
    parser.add_argument("--c_grid", nargs="+", type=float, default=C_GRID,
                        help=f"Regularization C values to search. Default: {C_GRID}")
    parser.add_argument("--max_iter", type=int, default=1000)
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    os.makedirs(os.path.dirname(args.output_path), exist_ok=True)

    results = {
        "metadata": {
            "c_grid": args.c_grid,
            "max_iter": args.max_iter,
            "pe_types": args.pe_types,
            "seeds": args.seeds,
            "datasets": args.datasets,
        },
        "per_combination": {},
    }

    total = len(args.pe_types) * len(args.seeds) * len(args.datasets)
    print(f"[INFO] Linear probe on {total} (pe_type, seed, dataset) combinations")
    print(f"[INFO] C grid: {args.c_grid}")

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

                t0 = time.time()
                result = train_linear_probe(
                    features_train, labels_train,
                    features_test, labels_test,
                    c_grid=args.c_grid, max_iter=args.max_iter,
                    verbose=args.verbose,
                )
                elapsed = time.time() - t0

                result["elapsed_sec"] = elapsed
                result["num_classes"] = DATASET_INFO[dataset_name]["num_classes"]
                result["chance"] = 1.0 / result["num_classes"]
                results["per_combination"][key] = result

                pbar.set_postfix({
                    "dataset": dataset_name,
                    "test_acc": f"{result['best_test_acc']:.3f}",
                    "C": result["best_c"],
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
