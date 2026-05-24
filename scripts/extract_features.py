"""
Feature extraction for transfer learning experiments.

For each (pe_type, seed, dataset) combination:
  1. Load pretrained model
  2. Run forward_features on full train and test splits
  3. Save features as .npz with keys: features_train, labels_train,
                                      features_test, labels_test

Cached features are then reused by linear probe and kNN scripts.

Usage:
    python -m scripts.extract_features \\
        --checkpoint_root "/content/drive/MyDrive/Trained models_ImageNet100" \\
        --data_root /content/datasets \\
        --output_dir /content/drive/MyDrive/pe_transfer_experiment/features \\
        --datasets food101 oxford_pets fgvc_aircraft oxford_flowers dtd \\
        --batch_size 128
"""

import argparse
import os
import time
import numpy as np
import torch
from tqdm import tqdm

from models import load_pretrained_model, PE_TYPES, SEEDS
from data import get_dataloader, DATASETS


@torch.no_grad()
def extract_features(model, loader, device):
    """Run forward_features over a loader; return (features, labels) numpy arrays."""
    features_list, labels_list = [], []
    for imgs, labels in tqdm(loader, leave=False):
        imgs = imgs.to(device, non_blocking=True)
        feats = model.forward_features(imgs)  # [B, embed_dim]
        features_list.append(feats.cpu().numpy())
        labels_list.append(labels.numpy())
    features = np.concatenate(features_list, axis=0)
    labels = np.concatenate(labels_list, axis=0)
    return features, labels


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--checkpoint_root", required=True,
                        help="Root path containing {pe_type}_seed{seed}/best_model.pth")
    parser.add_argument("--data_root", required=True,
                        help="Root path for downstream datasets (torchvision downloads here)")
    parser.add_argument("--output_dir", required=True,
                        help="Where to save extracted feature .npz files")
    parser.add_argument("--datasets", nargs="+", default=DATASETS,
                        help=f"Datasets to extract. Default: all {DATASETS}")
    parser.add_argument("--pe_types", nargs="+", default=PE_TYPES,
                        help="PE types to process")
    parser.add_argument("--seeds", nargs="+", type=int, default=SEEDS,
                        help="Seeds to process")
    parser.add_argument("--batch_size", type=int, default=128)
    parser.add_argument("--num_workers", type=int, default=4)
    parser.add_argument("--img_size", type=int, default=224)
    parser.add_argument("--num_classes_pretrain", type=int, default=100,
                        help="Number of classes the checkpoint was trained on")
    parser.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    parser.add_argument("--skip_existing", action="store_true",
                        help="Skip combinations where output .npz already exists")
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)
    print(f"[INFO] Device: {args.device}")
    print(f"[INFO] PE types: {args.pe_types}")
    print(f"[INFO] Seeds: {args.seeds}")
    print(f"[INFO] Datasets: {args.datasets}")
    print(f"[INFO] Total combinations: {len(args.pe_types) * len(args.seeds) * len(args.datasets)}")

    total_start = time.time()

    for pe_type in args.pe_types:
        for seed in args.seeds:
            # Load model once per (pe_type, seed); reuse across datasets
            print(f"\n[MODEL] {pe_type}, seed={seed}")
            model = load_pretrained_model(
                args.checkpoint_root, pe_type, seed,
                num_classes=args.num_classes_pretrain,
                device=args.device,
            )
            if model is None:
                print(f"  [SKIP] checkpoint missing")
                continue

            for dataset_name in args.datasets:
                output_path = os.path.join(
                    args.output_dir,
                    f"{pe_type}_seed{seed}_{dataset_name}.npz"
                )
                if args.skip_existing and os.path.exists(output_path):
                    print(f"  [SKIP] {dataset_name} (cached)")
                    continue

                print(f"  [EXTRACT] {dataset_name}")
                t0 = time.time()

                train_loader = get_dataloader(
                    dataset_name, args.data_root,
                    split="train", batch_size=args.batch_size,
                    num_workers=args.num_workers, img_size=args.img_size,
                    augment=False, shuffle=False,
                )
                test_loader = get_dataloader(
                    dataset_name, args.data_root,
                    split="test", batch_size=args.batch_size,
                    num_workers=args.num_workers, img_size=args.img_size,
                    augment=False, shuffle=False,
                )

                feats_train, labels_train = extract_features(model, train_loader, args.device)
                feats_test, labels_test = extract_features(model, test_loader, args.device)

                np.savez_compressed(
                    output_path,
                    features_train=feats_train.astype(np.float32),
                    labels_train=labels_train,
                    features_test=feats_test.astype(np.float32),
                    labels_test=labels_test,
                )
                elapsed = time.time() - t0
                print(f"    [DONE] train={feats_train.shape}, test={feats_test.shape}, "
                      f"elapsed={elapsed:.1f}s -> {output_path}")

            del model
            torch.cuda.empty_cache()

    total_elapsed = time.time() - total_start
    print(f"\n[ALL DONE] Total time: {total_elapsed / 60:.1f} min")


if __name__ == "__main__":
    main()
