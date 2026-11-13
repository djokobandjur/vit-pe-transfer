# B4 locked-runner hash correction (supersedes one line of previous lock)

This amendment is recorded **before any B4 GPU extraction or probing**. The initial lock commit is `f88c938383a42dcdb5599a51f874d115c578d2ac`.

One operational bug was caught by local offline testing: `runner.py offline-check` depended on a remote Step07 directory. `verify_step07()` was moved from `offline()` into the H200 `preflight()` only. No change to hypotheses, data, feature extraction, C-selection, test inference, statistical analysis, or the 13×2 readout definition.

The single superseding exact source hash is:

```
09d4dfe6b553eb57ff4412f2fa2c62169329ad02200c238287eb08f3874bd105  scripts/runner.py
```

All 13 other SHA256 lines in `research/B4_TOKEN_DEPTH_SHA256_LOCK_2026-11-13.md` remain unchanged. The **final branch head commit** containing both documents is the effective external time anchor; its exact SHA is recorded in the distributed `protocol/B4_CODE_LOCK.json`. The runner checks every hash against its local list and fails closed on mismatch.

Local tests before this correction: both RoPE and Learned 12-block random-weight ViTs passed a numerical equality check between B4 final_norm CLS manual-forward and original `model.forward(return_features=True)[:,0]` (max absolute deviation zero), and the exact 6-vs-6 permutation enumeration produced 2/924 for separated groups.
