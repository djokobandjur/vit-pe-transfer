# B4-E dual-checkpoint token-readout study — protocol prelock v0.1 (2026-11-14)

**STATUS: DESIGN PRELOCK ONLY. NO NEW E EXTRACTIONS OR PROBES AUTHORIZED UNTIL 24 E EPOCH-300 FILES, THEIR SHA-256, THEIR TRAINING-EPOCH PROVENANCE, AND NUMERICAL REPLAY ARE VERIFIED.**

Motivation: planned AFTER B4-C results were known; B4-E is a prospectively specified (relative to E execution) robustness study, not a prospectively hypothesized result of the original manuscript. Cohort E = 24 original ImageNet-100 endpoint ViT-B/16 models: learned, rope, sinusoidal, raster ALiBi × six seeds 42, 123, 456, 789, 1011, 1213.

**Primary rule:** fixed epoch-300 FINAL checkpoint for each original E model, not an L-cohort epoch-300 weight. Main contrast between six RoPE and six Learned models: for each of five tasks, D=mean((pool−CLS)_RoPE)−mean((pool−CLS)_Learned), readout at final LN. Exact independent 6:6 permutation (924 allocations), unadjusted Welch 95% CI, five-task Holm.

**Secondary rule:** original best-validation endpoint checkpoint, same readouts and five-task analysis, as its own Holm family. Exploratory: best-versus-final checkpoint interaction computed within identical model runs, then between PE families; direct RoPE−Learned pool contrasts; block_10 token readout, Sinusoidal/ALiBi context and remaining depths. Independent model is the inferential unit, not image. Repeat-task and checkpoint selection correlations are explicitly acknowledged.

Preserve original Step07 selection/train/test splits, frozen feature extraction, 196 patch mean pool excluding CLS, 17-value C grid, StandardScaler, LBFGS up to 1000 iterations, no test-based selection. Record per-model and per-image predictions and provenance. Exact H200 batch/TF32 settings must be established against the original E best CLS model before E readout outputs are produced; do not assume B4-C replay settings also replay E.

## Cryptographic commitments

The following immutable files are distributed inside the separately named B4-E prelock bundle. All hash strings below are SHA-256 of exact file bytes:

```
a1b1f7a768c0c677b7e1c724812d5dad6761b6e5dc4708e8b757fcbe76ba59fe  B4_E_PROTOCOL_PRELOCK_v0.1.json
de7671ea77a99e7b8ecfbaf9f160d5edb1ecf405583d378dbec04391fc6a91d3  B4E_checkpoint_expected.csv
6cd9ace9cd607494283588ba5a25d29f1fa0bca8ab86d0116382029c37fdf402  prepare_inventory.py
```

The checkpoint manifest contains **24 separately archived FULL SHA-256 values for best_model.pth**, obtained from `TRANSREP_experimental_reproducibility_v1.2.0/metadata/checkpoints/CHECKPOINT_MANIFEST.csv`. The manifest's 24 final300 SHA fields are intentionally empty: **no original E final300 SHA found in local reproducibility archives**. Their identity is NOT verified. The inventory script hashes actual files, flags best-model mismatches, and records final candidates, but does not itself authenticate the epoch number or independently validate final hash provenance. A second external lock must commit those results and evidence before execution. **No invented or substituted hash values**.

This lock is on a research branch and leaves `main`, release `v1.2.0` and the earlier B4-C SHA commitments unchanged. It does not authorize E training or claim any E readout results.
