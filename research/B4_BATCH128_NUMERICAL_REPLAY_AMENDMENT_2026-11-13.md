# TRANSREP B4 — second post-failure numerical replay amendment: enforce Step07 batch size 128 (2026-11-13)

**Status:** Explicit operational correction after the SECOND failed S1 extraction; source code and all scientific analysis commitments are unchanged apart from matching the original numeric batch shape. This is NOT presented as an original prelock. **No new B4 GPU result existed when this correction was prepared.**

- Original immutable B4 scientific prelock: SHA256 `c9d7e019c864c57bf4773001500982e12abbca6ce9a44d5c490b9e58d69ba84b`.
- Original source lock: commit `ce4506ace0f20f0789c6fbfa12286caabe013997`.
- First post-failure TF32 amendment: commit `834ba8995b45d5c300bb36ff5e7890529555666a`; its original source and protocol remain present, including its then-valid choice of batch 64.
- Under TF32=True the second S1 run failed at exactly one Food-101 train batch (75,750 images; max abs CLS discrepancy **0.0037404894828796387**), leaving its own `.partial` and error log.
- A subsequent **read-only H200 last-batch diagnosis** proved the cause: Step07's final batch size **102** (train indices 75,648:75,750) gives exactly the archived CLS (max abs 0) with either standard or B4 manual forward; B4's 64+38 partition differs only on its final **38** (max abs **0.00374048948**), even with the standard Step07 forward. The first 64 rows agree exactly. Diagnosis ended `DIAGNOSIS LAST-BATCH-SHAPE CONFIRMED`.
- Recovery: use **batch size 128**, with **CUDA matmul and cuDNN TF32 both True**, exact Step07 recipe. Extractor *refuses* batch size !=128, and launcher explicitly passes `--batch-size 128`. This preserves the stringent `rtol=atol=3e-5` feature gate for every split of all 60 extractions.
- New archive root: `TRANSREP_B4_COHORT_C_TOKEN_DEPTH_REPLAY128_2026-11-13` (new outputs only). **Do not delete/modify** either earlier original or TF32FIX partial, guard, log, checkpoint or provenance.
- No change to model weights, upstream matching, PE families, seeds, task partitions, transforms, 13×2 readouts, pooling definition, FP32 stored data, probe protocol, primary/secondary test families, or exploratory status. No training.
- Validation scope: the **read-only last-batch** H200 diagnostic passed. A complete 75,750-image train, validation and test replication in this new package **has not yet been run**. Stop at the existing strict numerical gate if anything differs; S2–S4 only after one full first extraction passes.
- Operational nature: because the original `B4_PROTOCOL_PRELOCK.json` asserted "no TF32" and the first post-failure amendment justified batch size 64 on a 128-image diagnostic, the ordered external chain of post-failure amendments explicitly supersedes both execution settings. No retrospective relabeling.

## SHA-256 source/document commitments
Exact bytes of files inside the new archive:

```
56dade4a8bc2748b04fe7e88aa83f6a444ca467b29543d2de755b70f255fb3c8  scripts/extract_one.py
5ca9e4e78fd17c2cad32eb3c5bf6d772aad325b9ea5663fad0a2605f3a79ed47  scripts/runner.py
08c975f3d17672a0954a54bd4f5a2b9f97c19d0ac588f7973b8aaee90d2fc760  README_START_HERE.md
8035e708fb745750b1404375997054f75ac9ac1532aceaab7fb98e88cbb8fca4  RECOVERY_NOTE_LAST_BATCH.md
b19e089b2ba9dd1d5c31debd62d844ba414b7833f2ba2c4a916dc992f2c6226f  SCIENTIFIC_CHANGELOG.md
18b906b9de51576d1eaba64818885b1426bd34f218fef20ffd344f9db20095dd  protocol/B4_BATCH_REPLAY_AMENDMENT.json
```

Unchanged preexisting locked files retain their earlier hashes from `research/B4_TOKEN_DEPTH_SHA256_LOCK_2026-11-13.md`, `research/B4_LOCK_AMENDMENT_2026-11-13.md` and `research/B4_TF32_NUMERICAL_REPLAY_AMENDMENT_2026-11-13.md`. The commit containing this file is the new external timestamp anchor to store in the `B4_CODE_LOCK.json` of the new archive, and is not a release or deposition.
