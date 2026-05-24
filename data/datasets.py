"""
Downstream dataset loaders for transfer learning experiments.

Five datasets:
  - Food-101         : 101 classes, general food images
  - Oxford Pets      : 37 classes, fine-grained natural (cats/dogs breeds)
  - FGVC Aircraft    : 100 classes, fine-grained, less texture-driven
  - Oxford 102 Flowers : 102 classes, fine-grained, texture-rich
  - DTD              : 47 classes, pure texture (no semantic content)

Standard ImageNet preprocessing (224x224, ImageNet mean/std).
Minimal augmentation (linear probe / kNN benefit from raw features).
"""

import os
import torch
from torchvision import datasets, transforms
from torch.utils.data import DataLoader


IMAGENET_MEAN = [0.485, 0.456, 0.406]
IMAGENET_STD = [0.229, 0.224, 0.225]


def get_eval_transform(img_size=224):
    """Standard evaluation transform: resize + center crop + normalize."""
    return transforms.Compose([
        transforms.Resize(int(img_size * 256 / 224)),
        transforms.CenterCrop(img_size),
        transforms.ToTensor(),
        transforms.Normalize(mean=IMAGENET_MEAN, std=IMAGENET_STD),
    ])


def get_train_transform(img_size=224, augment=False):
    """Training transform: optional light augmentation."""
    if augment:
        return transforms.Compose([
            transforms.RandomResizedCrop(img_size, scale=(0.8, 1.0)),
            transforms.RandomHorizontalFlip(),
            transforms.ToTensor(),
            transforms.Normalize(mean=IMAGENET_MEAN, std=IMAGENET_STD),
        ])
    # Linear probe / kNN: no augmentation, want raw features
    return get_eval_transform(img_size)


# ----------------------------------------------------------------------
# Dataset registry
# ----------------------------------------------------------------------

DATASET_INFO = {
    "food101": {
        "num_classes": 101,
        "torchvision_class": "Food101",
        "split_train": "train",
        "split_test": "test",
    },
    "oxford_pets": {
        "num_classes": 37,
        "torchvision_class": "OxfordIIITPet",
        "split_train": "trainval",
        "split_test": "test",
    },
    "fgvc_aircraft": {
        "num_classes": 100,
        "torchvision_class": "FGVCAircraft",
        "split_train": "trainval",
        "split_test": "test",
    },
    "oxford_flowers": {
        "num_classes": 102,
        "torchvision_class": "Flowers102",
        "split_train": "train",
        "split_test": "test",
    },
    "dtd": {
        "num_classes": 47,
        "torchvision_class": "DTD",
        "split_train": "train",
        "split_test": "test",
    },
}


def get_dataset(name, data_root, split="train", img_size=224, augment=False, download=True):
    """
    Load a downstream dataset.

    Args:
        name      : one of DATASET_INFO keys
        data_root : path to dataset root (will be created/used by torchvision)
        split     : 'train' or 'test'
        img_size  : input image size (default 224)
        augment   : if True and split=='train', apply light augmentation
        download  : if True, download dataset if not present

    Returns:
        torchvision Dataset
    """
    if name not in DATASET_INFO:
        raise ValueError(f"Unknown dataset: {name}. Available: {list(DATASET_INFO)}")

    info = DATASET_INFO[name]
    transform = get_train_transform(img_size, augment) if split == "train" \
        else get_eval_transform(img_size)

    split_key = info["split_train"] if split == "train" else info["split_test"]

    dataset_class = getattr(datasets, info["torchvision_class"])
    dataset = dataset_class(
        root=data_root,
        split=split_key,
        transform=transform,
        download=download,
    )
    return dataset


def get_dataloader(name, data_root, split="train", batch_size=128, num_workers=4,
                   img_size=224, augment=False, download=True, shuffle=None):
    """Convenience wrapper around get_dataset returning a DataLoader."""
    if shuffle is None:
        shuffle = (split == "train")

    dataset = get_dataset(name, data_root, split, img_size, augment, download)
    loader = DataLoader(
        dataset,
        batch_size=batch_size,
        shuffle=shuffle,
        num_workers=num_workers,
        pin_memory=True,
        persistent_workers=(num_workers > 0),
    )
    return loader


DATASETS = list(DATASET_INFO.keys())
