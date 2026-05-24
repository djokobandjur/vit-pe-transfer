"""
Pretrained model loader for ViT-Base checkpoints.

Expected checkpoint layout:
    {checkpoint_root}/{pe_type}_seed{seed}/best_model.pth

Where:
    pe_type in {learned, sinusoidal, rope, alibi}
    seed    in {42, 123, 456}

Auto-detects architecture from state_dict shapes (patch_size, img_size).
"""

import os
import torch

from .vit_architecture import VisionTransformer


PE_TYPES = ["learned", "sinusoidal", "rope", "alibi"]
SEEDS = [42, 123, 456]


def detect_architecture(state_dict):
    """Infer patch_size, img_size, num_patches from checkpoint shapes."""
    pw = state_dict["patch_embed.proj.weight"]
    patch_size = pw.shape[-1]

    pe_shape = None
    # Possible PE buffer/parameter names across training-time conventions
    for key in ["pos_encoding.pos_embed", "pos_encoding.pe", "pos_embed"]:
        if key in state_dict:
            pe_shape = state_dict[key].shape
            break

    if pe_shape is not None:
        n_tokens = pe_shape[1]
        candidate = n_tokens - 1  # subtract CLS
        # if (n - 1) is a perfect square, it's (n-1) patches
        if candidate > 0 and int(candidate ** 0.5) ** 2 == candidate:
            num_patches = candidate
        else:
            num_patches = n_tokens
        img_size = int(num_patches ** 0.5) * patch_size
    else:
        # RoPE / ALiBi: no pos_embed in state_dict; fall back to convention
        img_size = 32 if patch_size == 4 else 224

    return patch_size, img_size


def load_pretrained_model(checkpoint_root, pe_type, seed,
                           num_classes=100, device="cuda"):
    """
    Load a pretrained ViT-Base checkpoint.

    Args:
        checkpoint_root : path to root folder containing {pe_type}_seed{seed}/ subfolders
        pe_type         : one of PE_TYPES
        seed            : integer seed
        num_classes     : number of output classes the checkpoint was trained with
                          (default 100 for ImageNet-100; ignored for feature extraction)
        device          : torch device

    Returns:
        model : VisionTransformer in eval mode, loaded with checkpoint weights
                None if checkpoint missing.
    """
    if pe_type not in PE_TYPES:
        raise ValueError(f"pe_type must be one of {PE_TYPES}, got {pe_type}")

    path = os.path.join(checkpoint_root, f"{pe_type}_seed{seed}", "best_model.pth")
    if not os.path.exists(path):
        print(f"[MISSING] {path}")
        return None

    state = torch.load(path, map_location=device, weights_only=True)
    # Strip torch.compile() prefix if present
    state = {k.replace("_orig_mod.", ""): v for k, v in state.items()}

    patch_size, img_size = detect_architecture(state)

    torch.manual_seed(seed)
    model = VisionTransformer(
        img_size=img_size,
        patch_size=patch_size,
        num_classes=num_classes,
        embed_dim=768,
        depth=12,
        num_heads=12,
        mlp_ratio=4.0,
        dropout=0.1,
        pe_type=pe_type,
    ).to(device)

    # Drop checkpoint buffers whose shape differs from the current architecture.
    # RoPE cos_cached/sin_cached in some checkpoints have an extra
    # (1, 1, seq, dim) batch/head broadcast prefix from older training code.
    # We let the model regenerate them deterministically from inv_freq.
    keys_to_delete = [k for k in state.keys()
                      if "rope.cos_cached" in k or "rope.sin_cached" in k]
    for k in keys_to_delete:
        del state[k]

    # Load with strict=False to tolerate minor buffer-name differences
    # (e.g., inv_freq absent in some checkpoints, or extra params from training infra)
    missing, unexpected = model.load_state_dict(state, strict=False)
    if missing:
        # Filter to learnable parameters only (buffers can be regenerated)
        learnable_missing = [k for k in missing
                              if not any(s in k for s in ['inv_freq', 'cos_cached', 'sin_cached',
                                                           'rel_dist', 'slopes', 'pe'])]
        if learnable_missing:
            raise RuntimeError(f"Missing learnable parameters: {learnable_missing}")
        print(f"  [INFO] Skipped {len(missing)} buffer keys (regenerated from architecture)")
    if unexpected:
        print(f"  [INFO] Ignored {len(unexpected)} unexpected keys: {unexpected[:3]}{'...' if len(unexpected) > 3 else ''}")

    model.eval()
    return model


def list_available_checkpoints(checkpoint_root):
    """Return list of (pe_type, seed) tuples for available checkpoints."""
    available = []
    for pe_type in PE_TYPES:
        for seed in SEEDS:
            path = os.path.join(checkpoint_root, f"{pe_type}_seed{seed}", "best_model.pth")
            if os.path.exists(path):
                available.append((pe_type, seed))
    return available
