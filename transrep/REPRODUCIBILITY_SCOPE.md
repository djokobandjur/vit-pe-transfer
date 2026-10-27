# Numerical reproduction and limitations

This experimental package allows independent checksum verification and selected metric reconstruction without access to source images, checkpoint weights or GPUs.

**Included**: 24 endpoint upstream observations, 360 longitudinal upstream measurements, 805 downstream evaluation records, 90 run-level target contrasts, 45 public DeiT-III downstream prediction records, 3,588 CKA similarities and 78 family/readout aggregates, 12 shared ImageNet-1k DeiT/Swin prediction arrays, 60 supplementary DeiT/Swin downstream prediction arrays, and data and scripts for six figures.

**Not included**: `matched_30_pairs.csv` and `matching_lock.json` for the exploratory endpoint matching analysis (Section 4.2). The available analysis there is only task-summary-level. Source datasets, complete trained checkpoint weights, and the 24 very large CKA source activation arrays are not redistributed; the latter have SHA-256 metadata. Some training modules have external execution dependencies.

The longitudinal aligned-accuracy analysis is based on **interpolation of recorded test scores**, not retrained intermediate model weights. Seed numbers reused across PE families do not make the models randomized paired blocks. Bootstrap intervals on public models describe evaluation-image sampling variability, not retraining variability. The exploratory DeiT–Swin comparison compares complete model systems.

Publication manuscripts and supplementary article files are expressly excluded from this repository/deposit.
