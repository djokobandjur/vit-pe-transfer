"""
Setup ImageNet-100 validation set from ILSVRC2012_img_val.tar.

The full ImageNet-1k validation tar contains 50,000 images in a flat
directory. This script:
  1. Reads the list of 100 ImageNet-100 class WordNet IDs
  2. Reads validation labels (one WordNet ID per image, 50000 lines)
  3. Extracts only the 5,000 images belonging to the 100 classes
  4. Organizes them in ImageFolder structure: val/{synset_id}/*.JPEG

Prerequisites (on Google Drive or local):
  - ILSVRC2012_img_val.tar : ImageNet-1k validation tar
    (obtain from https://image-net.org, requires academic registration)
  - imagenet100_classes.txt: one WordNet ID per line, 100 lines total
  - val_labels.txt         : one WordNet ID per line, 50000 lines
    (auto-downloaded from tensorflow/models if not present)

Output structure (5,000 images, 100 classes, 50 images each):
  output_dir/val/
  ├── n01558993/
  │   ├── ILSVRC2012_val_00000293.JPEG
  │   └── ... (50 images)
  ├── n01692333/
  └── ... (100 classes)

ImageNet-100 split reference:
  Tian, Y., Krishnan, D., Isola, P.
  "Contrastive Multiview Coding", ECCV 2020.

Usage:
    python -m scripts.setup_imagenet100_val \\
        --tar_path "/content/drive/MyDrive/pe_experiment/imagenet/ILSVRC2012_img_val.tar" \\
        --classes_path "/content/drive/MyDrive/pe_experiment/imagenet100_classes.txt" \\
        --labels_path "/content/drive/MyDrive/pe_experiment/val_labels.txt" \\
        --output_dir /content/imagenet100
"""

import os
import tarfile
import argparse
import urllib.request
from pathlib import Path
from tqdm import tqdm


VAL_LABELS_URL = (
    "https://raw.githubusercontent.com/tensorflow/models/"
    "master/research/slim/datasets/"
    "imagenet_2012_validation_synset_labels.txt"
)


def main():
    parser = argparse.ArgumentParser(
        description="Prepare ImageNet-100 validation set from ILSVRC2012 tar"
    )
    parser.add_argument("--tar_path", required=True,
                        help="Path to ILSVRC2012_img_val.tar")
    parser.add_argument("--classes_path", default=None,
                        help="Path to imagenet100_classes.txt (100 WordNet IDs). "
                             "Defaults to repo's data/imagenet100_classes.txt")
    parser.add_argument("--labels_path", default=None,
                        help="Path to val_labels.txt (50000 WordNet IDs, "
                             "one per ImageNet-1k val image). "
                             "Defaults to repo's data/val_labels.txt. "
                             "Auto-downloaded if missing.")
    parser.add_argument("--output_dir", required=True,
                        help="Output directory (val/ subfolder will be created inside)")
    args, _ = parser.parse_known_args()

    # Defaults to repo-relative paths
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if args.classes_path is None:
        args.classes_path = os.path.join(repo_root, "data", "imagenet100_classes.txt")
        print(f"[INFO] Using default classes file: {args.classes_path}")
    if args.labels_path is None:
        args.labels_path = os.path.join(repo_root, "data", "val_labels.txt")
        print(f"[INFO] Using default labels file: {args.labels_path}")

    print("=" * 60)
    print("ImageNet-100 Validation Set Setup")
    print("=" * 60)

    # Verify required inputs
    for path, name in [(args.tar_path, "ILSVRC2012_img_val.tar"),
                        (args.classes_path, "imagenet100_classes.txt")]:
        if not os.path.exists(path):
            raise FileNotFoundError(
                f"\n[ERROR] {name} not found at:\n  {path}\n"
                f"Please verify the path and re-run."
            )
        print(f"  Found: {name}")

    # Auto-download val_labels.txt if missing
    if not os.path.exists(args.labels_path):
        print(f"  val_labels.txt not found at {args.labels_path}")
        print(f"  Downloading from TensorFlow Models repository...")
        os.makedirs(os.path.dirname(args.labels_path), exist_ok=True)
        urllib.request.urlretrieve(VAL_LABELS_URL, args.labels_path)
        print(f"  Downloaded: {args.labels_path}")
    else:
        print(f"  Found: val_labels.txt")

    # Load class split
    with open(args.classes_path) as f:
        classes = set(line.strip() for line in f if line.strip())
    print(f"\nImageNet-100 classes: {len(classes)}")
    assert len(classes) == 100, f"Expected 100 classes, got {len(classes)}"

    # Load val labels
    with open(args.labels_path) as f:
        val_labels = [line.strip() for line in f.readlines()]
    print(f"Val labels loaded: {len(val_labels)} entries")
    assert len(val_labels) == 50000, \
        f"Expected 50,000 val labels, got {len(val_labels)}"

    # Create output directories
    val_dir = os.path.join(args.output_dir, "val")
    for synset in classes:
        os.makedirs(os.path.join(val_dir, synset), exist_ok=True)
    print(f"Output directory: {val_dir}")
    print(f"Created {len(classes)} class folders")

    # Extract relevant images
    print(f"\nExtracting from: {args.tar_path}")
    print("(This may take 5-10 minutes depending on Drive speed...)\n")

    extracted = 0
    skipped = 0

    with tarfile.open(args.tar_path, "r") as tar:
        members = tar.getmembers()
        print(f"Total images in tar: {len(members):,}")

        for member in tqdm(members, desc="Filtering", unit="img"):
            stem = Path(member.name).stem  # e.g. ILSVRC2012_val_00000001
            try:
                idx = int(stem.split("_")[-1]) - 1  # 0-indexed
            except ValueError:
                skipped += 1
                continue
            if idx >= len(val_labels):
                skipped += 1
                continue

            synset = val_labels[idx]
            if synset not in classes:
                skipped += 1
                continue

            dst_path = os.path.join(val_dir, synset, member.name)
            fobj = tar.extractfile(member)
            if fobj is not None:
                with open(dst_path, "wb") as out:
                    out.write(fobj.read())
                extracted += 1

    # Verification
    print(f"\n{'=' * 60}")
    print(f"Extraction complete!")
    print(f"  Images extracted: {extracted:,}")
    print(f"  Images skipped:   {skipped:,}")
    print(f"  Expected:         5,000")

    if extracted != 5000:
        print(f"\n[WARNING] Expected 5,000 images but got {extracted}.")
        print("  Check that val_labels.txt matches ILSVRC2012 val set.")
    else:
        print(f"\n  All 5,000 images extracted successfully.")

    # Per-class verification
    print(f"\nPer-class image count (first 5):")
    class_counts = {}
    for synset in sorted(classes):
        folder = os.path.join(val_dir, synset)
        count = len(os.listdir(folder))
        class_counts[synset] = count
    for synset, count in list(class_counts.items())[:5]:
        print(f"  {synset}: {count} images")

    min_count = min(class_counts.values())
    max_count = max(class_counts.values())
    print(f"\n  Min images per class: {min_count}")
    print(f"  Max images per class: {max_count}")
    if min_count == max_count == 50:
        print(f"All classes have exactly 50 images.")
    else:
        print(f"  [WARNING] Unequal class sizes — check val_labels.txt")

    print(f"\nDataset ready at: {val_dir}")


if __name__ == "__main__":
    main()
