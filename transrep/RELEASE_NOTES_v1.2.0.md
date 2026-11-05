# Numerical reproducibility v1.2.0 — notes for a new Zenodo version

**Published 5 November 2026:** [Zenodo numerical archive v1.2.0](https://doi.org/10.5281/zenodo.23986036) (version DOI `10.5281/zenodo.23986036`; all-versions DOI `10.5281/zenodo.20368592`).

The numerical ZIP supersedes v1.1.0 **for offline reaggregation of the extended analysis**, preserving the historical release.

### Added evidence

- Seed-level exploratory endpoint matching: selection record, six pairs and 30 original task-level results, plus reaggregation script.
- Twelve complete H200 longitudinal histories and twelve 30-checkpoint audit records; six original RoPE endpoint training histories (two with documented gaps, not filled).
- Original 120 k-NN model–task results and numerical checks.
- Full last-crossing and conditional bracketing sensitivity tables and replay scripts.
- Source class index, checkpoint identity metadata, method provenance, figure-generation and additional QA checks.

### Verification

Run `python scripts/verify_release.py` and `python scripts/verify_training_histories.py` inside the extracted ZIP. Checks: **2,962 payload files**, **44 figure files**, **3,600 LR values**, **360 checkpoint SHA-256 identifiers**, and the saved numerical results. No scientific measurements or trained model weights were modified in preparing the public ZIP.

### Scope and citation

Only numerical evidence and analysis code are distributed, without source images, model weight binaries, manuscript or supplement. This numerical ZIP was published as a new version of the existing Zenodo deposit. Cite the version DOI **10.5281/zenodo.23986036** for v1.2.0; the concept DOI remains https://doi.org/10.5281/zenodo.20368592. The previous v1.1.0 version DOI identifies only that earlier release.
