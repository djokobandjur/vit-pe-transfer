"""
Per-layer feature extraction for CKA analysis.

For each model, extract features after every transformer block (12 layers)
on a fixed stimulus set (ImageNet-100 validation subset, 2000 images).

Output: one .npz per model with features at each of 12 layers.
    {pe_type}_seed{seed}_cka_features.npz containing:
        layer_0, layer_1, ..., layer_11  : each [N_stimuli, embed_dim]
        labels                            : [N_stimuli]
        stimulus_indices                  : [N_stimuli] (which val images used)

Stimulus set is FIXED (same images for every model) so CKA comparisons
are well-defined.

Usage:
    python -m scripts.extract_cka_features \\
        --checkpoint_root "/content/drive/MyDrive/Trained models_ImageNet100" \\
        --imagenet_val_root "/content/drive/MyDrive/ImageNet100/val" \\
        --output_dir "/content/drive/MyDrive/pe_transfer_experiment/cka_features" \\
        --n_stimuli 2000 \\
        --stimulus_seed 0
"""

import argparse
import os
import time
import numpy as np
import torch
import torch.nn.functional as F
from torch.utils.data import DataLoader, Subset
from torchvision import datasets, transforms
from tqdm import tqdm

from models import load_pretrained_model, PE_TYPES, SEEDS


def get_stimulus_indices(n_total, n_stimuli, seed=0):
    """Deterministic random subset of stimulus indices."""
    rng = np.random.RandomState(seed)
    return np.sort(rng.choice(n_total, size=n_stimuli, replace=False))


@torch.no_grad()
def extract_per_layer_features(model, loader, device):
    """
    Run forward pass through all 12 transformer blocks, capturing
    CLS token features after each block.

    Returns:
        per_layer_features: list of 12 arrays, each [N, embed_dim]
        labels: array [N]
    """
    n_layers = len(model.blocks)
    per_layer_feats = [[] for _ in range(n_layers)]
    labels_list = []

    for imgs, labels in tqdm(loader, leave=False):
        imgs = imgs.to(device, non_blocking=True)
        B = imgs.shape[0]

        # Manual forward pass capturing per-block CLS token
        x = model.patch_embed(imgs)
        x = torch.cat([model.cls_token.expand(B, -1, -1), x], dim=1)
        if hasattr(model, "pos_encoding"):
            x = model.pos_encoding(x)
        x = model.dropout(x)

        for i, block in enumerate(model.blocks):
            x = block(x)
            # Capture CLS token after this block
            per_layer_feats[i].append(x[:, 0].cpu().numpy())

        labels_list.append(labels.numpy())

    per_layer_feats = [np.concatenate(layer_feats, axis=0)
                       for layer_feats in per_layer_feats]
    labels = np.concatenate(labels_list, axis=0)
    return per_layer_feats, labels


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--checkpoint_root", required=True)
    parser.add_argument("--imagenet_val_root", required=True,
                        help="Path to ImageNet-100 validation set (ImageFolder structure)")
    parser.add_argument("--output_dir", required=True)
    parser.add_argument("--n_stimuli", type=int, default=2000,
                        help="Number of stimulus images (default 2000)")
    parser.add_argument("--stimulus_seed", type=int, default=0,
                        help="Seed for stimulus subset selection (fixed for all models)")
    parser.add_argument("--pe_types", nargs="+", default=PE_TYPES)
    parser.add_argument("--seeds", nargs="+", type=int, default=SEEDS)
    parser.add_argument("--batch_size", type=int, default=64)
    parser.add_argument("--num_workers", type=int, default=4)
    parser.add_argument("--img_size", type=int, default=224)
    parser.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    parser.add_argument("--skip_existing", action="store_true")
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    # Standard ImageNet preprocessing
    transform = transforms.Compose([
        transforms.Resize(int(args.img_size * 256 / 224)),
        transforms.CenterCrop(args.img_size),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])

    # Load full ImageNet-100 validation set, select fixed stimulus subset
    full_val = datasets.ImageFolder(args.imagenet_val_root, transform=transform)
    print(f"[INFO] Full ImageNet-100 val size: {len(full_val)}")

    stim_indices = get_stimulus_indices(len(full_val), args.n_stimuli, args.stimulus_seed)
    stim_subset = Subset(full_val, stim_indices)
    loader = DataLoader(stim_subset, batch_size=args.batch_size,
                        shuffle=False, num_workers=args.num_workers,
                        pin_memory=True)
    print(f"[INFO] Stimulus subset: {args.n_stimuli} images (seed={args.stimulus_seed})")
    print(f"[INFO] PE types: {args.pe_types}")
    print(f"[INFO] Seeds: {args.seeds}")
    print(f"[INFO] Total models: {len(args.pe_types) * len(args.seeds)}")

    total_start = time.time()

    for pe_type in args.pe_types:
        for seed in args.seeds:
            output_path = os.path.join(args.output_dir,
                                        f"{pe_type}_seed{seed}_cka_features.npz")
            if args.skip_existing and os.path.exists(output_path):
                print(f"[SKIP] {pe_type}_seed{seed} (cached)")
                continue

            print(f"\n[MODEL] {pe_type}, seed={seed}")
            model = load_pretrained_model(args.checkpoint_root, pe_type, seed,
                                           num_classes=100, device=args.device)
            if model is None:
                continue

            t0 = time.time()
            per_layer_feats, labels = extract_per_layer_features(model, loader, args.device)
            elapsed = time.time() - t0

            # Save with per-layer keys: layer_0, layer_1, ..., layer_11
            save_dict = {
                f"layer_{i}": feats.astype(np.float32)
                for i, feats in enumerate(per_layer_feats)
            }
            save_dict["labels"] = labels
            save_dict["stimulus_indices"] = stim_indices

            np.savez_compressed(output_path, **save_dict)

            shape0 = per_layer_feats[0].shape
            print(f"  [DONE] {len(per_layer_feats)} layers x {shape0}, "
                  f"elapsed={elapsed:.1f}s -> {output_path}")

            del model
            torch.cuda.empty_cache()

    total_elapsed = time.time() - total_start
    print(f"\n[ALL DONE] Total time: {total_elapsed / 60:.1f} min")


if __name__ == "__main__":
    main()
