# B4-C full token-depth MAP analysis sidecar — source commitment (2026-11-15)

**Scope:** Post-completion, read-only exploratory aggregation. All 60 extractions, 240 CORE probes and 1320 MAP probes had finished, and the independent full MAP scan reported 330/330 complete, clean missing 0, PROBLEMS 0 on S1–S4, before this tool was run on the real results.

This commit is **not a retrospective statistical pre-registration**. The pre-specified B4 primary final_norm and secondary block_10 analyses remain in B4's original locked protocol and CORE aggregate. The new script produces per-depth exploratory summaries without making confirmatory claims about the other layers.

## SHA-256 source commitment
```
9e9066276e69e25dc7adf8ac1f63aa9053252bccade2c35159f51cbc6a838dbe  TRANSREP_B4C_MAP_READONLY_AGGREGATOR_2026-11-15.py
e48c75246c9da120df3a0265fbd613aec9ef79e45b104d63d277224ce2162464  README_START_HERE.md
9a4d01b7c142684ec96969ff2afbab8468bed5a44e21ae5d0717c3c0720d1771  TRANSREP_B4C_MAP_ANALYSIS_SIDECAR_2026-11-15.zip
```

Original immutable REPLAY128 source lock: `ff3dc423c85e21046bec3c16685234e59ff252b4`.

**Validation of sidecar on synthetic fixture** (not real MAP results): 1560/1560 result pairs enumerated and hashed, 10/10 CORE D/p/CI anchors reproduced using supplied genuine CORE aggregates, all output products written only into a separate directory, original B4 tree untouched. Real MAP results have NOT yet been inspected with this sidecar.

The script checks source-file SHA-256, four extract/core exit pairs, two recovered MAP exits, two regular MAP exits, result and prediction SHA-256, source commitment, feature metadata SHA-256, CLS Step07 replay, and exactly 10 CORE anchor outcomes before writing a new analysis directory OUTSIDE the original experiment.

Outputs include 1560 per-seed readout rows, 260 group means, 65 depth-wise token-change contrasts, and 130 direct PE-by-readout contrasts (all additional depth p-values unadjusted and exploratory). No change to model weights, features, predictions, original probe/scoring code, C search, seeds, test data or scientific protocol. PE vs duration confounding (RoPE 42e, Learned 200e) remains a limitation.
