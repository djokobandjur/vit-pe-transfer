# B4-C map continuation utility — operational sidecar (2026-11-14)

**HOLD WHILE ORIGINAL SLOTS ARE ACTIVE.** This sidecar exists solely to continue *unfinished* exploratory MAP probes after FMLE compute sessions expire. It is not a change to B4's scientific protocol, feature extraction, regularization grid, solver, checkpoint, seeds, train/test split, or statistical tests.

### Why needed

The immutable original `scripts/runner.py` has first-run guards, and its `_run_one()` refuses to start a job if the original log already exists. It cannot directly resume a partially executed `map` stage. `scripts/probe_one.py` writes each result pair independently (per-readout JSON and prediction NPZ) onto persistent shared Lustre.

### Sidecar hashes and authority

```
40fa184cd99907949c7bbbd01b04b25438d91f75eb8f2da118a01172d9b4d5d8  b4_map_resume.py
aa908bf4171a57f255a7e70894795e2c2c59c37dfeec6397f8b149d69066eede  start_map_resume.sh
```

Original B4-C REPLAY128 source Git SHA `ff3dc423c85e21046bec3c16685234e59ff252b4` remains unchanged.

### Controls
1. `scan` is read-only: counts 330 MAP readouts per slot; validates **both** output files, per-prediction SHA-256, identity, source commit and per-feature-metadata SHA-256. One-sided/orphan or invalid results trigger STOP rather than deletion or overwriting.
2. `resume-slot` explicitly requires operator confirmation that the **original slot's session/workers have ENDED**. Remote FMLE process liveness is NOT reliably visible across session namespaces. Never run concurrently with an original or second resume worker for the same slot.
3. Uses original locked `scripts/probe_one.py` verbatim, same task order and 22 non-core readouts; each complete verified output is skipped; no `core` jobs ever submitted.
4. Preserves original `logs/...`, `locks/...`, `provenance/...` untouched; creates distinctly named `logs/map_resume_Sx_Rnn/`, `locks/map_resume_Sx_Rnn.guard`, `provenance/map_resume_Sx_Rnn_exit.txt`. No deletion or overwrite.
5. Newly computed probe results remain in the same original `probes/<model-task>/` tree and are written only if both target files are absent. Optional time budget stops **between** tasks (exit 75); a long task can still be interrupted externally and would require a separate forensic check.
6. The sidecar only resumes jobs; it does not aggregate exploratory MAP or alter original test families. `runner.py status` shows completed output counts, but not sidecar exit status; inspect the separate sidecar supervisor log/exit code.
7. For future H200 or CPU-only sessions, ensure the original Python / numpy / scikit-learn versions remain matched before a resume run. The frozen-feature probe script uses CPU scikit-learn; extracting ViT features already finished.

This is a preparatory external operational commitment, **not authorization to restart currently running S1–S4**.
