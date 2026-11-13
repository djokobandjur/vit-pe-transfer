# TRANSREP B4 token × depth — external pre-evaluation lock
Date: 2026-11-13. Research branch only. Does not alter published v1.2.0.

## Protocol
Cohort C, 12 already trained FINAL ViT-B models (RoPE 42 epochs; Learned 200 epochs), six fixed seeds per family. Five frozen downstream tasks. All 13 post-block/final-LN depths × two token readouts are extracted in FP32 from a single forward pass, no training. Primary readout-change statistic: for each model, `d = test_score(final_norm patch mean) - test_score(final_norm CLS)`; compare the six RoPE and six Learned model-level d values using Welch 95% intervals and a two-sided exact 6-vs-6 label permutation (924 allocations) with Holm over five tasks. Block 10: separately labeled secondary five-task family. Other depths: exploratory; preserve all. Selected C on validation only, one non-test refit, per-image test predictions retained. Original Step07 final-LN CLS features and scores are verified, without changing original artifacts. Cohort L bracket extension is a separately executed later phase.

All checksums below are SHA-256 of the exact files within the corresponding distributed B4 runner ZIP; this commit cryptographically timestamps their contents. The executable ZIP contains the actual bytes. No GPU evaluation results existed at lock time.

## SHA-256 immutable source commitments

```
c9d7e019c864c57bf4773001500982e12abbca6ce9a44d5c490b9e58d69ba84b  protocol/B4_PROTOCOL_PRELOCK.json
3400d0dc9740e7ea4b4397f6c59242973b82d973bd623b0164c6901f7d32a63c  protocol/V0846_THREE_CORRECTIONS_PROPOSED.md
8e79438e59ee27a42b7995774546d70050d28d14d21d4b03cf7c6c66a3cb1c95  scripts/common.py
ec237badb7195856bc24d3875ee7daf551c57d5fe5b77eed619ed31683200da3  scripts/extract_one.py
01d15f53527665f5533d62298b54226cf2cace26c0ef56216b9d797929f60204  scripts/probe_one.py
b66d43efd98cfc0c5c4059efafbef01214fe85b01a916e5197f95045520fe3c7  scripts/runner.py
cdeae56ccd0a4f3cd211d68ae4b58b68c81e4615d13ee91ca487cf989d6fc05c  start_slot.sh
10ea8e3fefe2960a767ecd4381fcea93c601254901d716f6cc2022a6efce4ccc  methods/08_extract_final_features_original.py
1afc994c8a0ed356dce33d6880d87c2ef3054a2bba9247e97ba3978c8a0ce99f  methods/09_revised_linear_probe_original.py
87a85ac1c20c7ee3590040cc612551025d85ec69de1591faa2adf12dd600fe7b  methods/09_revised_linear_probe_newseeds.py
9145d111cb54c512ff6fb5887db5583705accd4d050abcc38aa8607c9f9c1779  configs/downstream_selection_splits.npz
8d066c2fb30d7368445fbf31c14daed0f0c4f3607b53a8814a7700df9ce5917f  configs/model_manifest.csv
dc043ce3c14a2f1f2fd17cdc4955e99505efba3aeab28f1147f578b615853a8f  README_START_HERE.md
91f7e3b9375a8d5fa7eafe5d8f780e54ae51e2c0ac177dfd3a09d19b9bcd261c  SCIENTIFIC_CHANGELOG.md
```

Guard: remote runner refuses to run unless every locked file matches this manifest and records this commit SHA. Output is isolated under the B4 path; original Step06/Step07 are read-only. Research-branch source commitment is not a Zenodo release or independently preregistered confirmation.
