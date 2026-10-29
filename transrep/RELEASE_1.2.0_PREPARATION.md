# TRANSREP numerical reproducibility v1.2.0 — publication preparation

**Status:** release artifact prepared and verified, **not yet deposited on Zenodo**. This file is a publication checklist, not a substitute for the research article.

## Distribution

- Intended file: `TRANSREP_EXPERIMENTAL_REPRODUCIBILITY_v1.2.0_RELEASE_READY_2026-10-29.zip`
- ZIP bytes: `17139017` (17.14 MB)
- SHA-256: `df56bc0b5fafed4c2198fcb63782153be9376422a22cf9dcecdf1412ea559fd5`
- MD5: `7c5a46ddbf09b8657d64361b515ed69c`
- Verified payload: **2,916 files** plus the `SHA256SUMS` index. No cached Python `.pyc` files or journal manuscript documents.
- Command from extracted archive root: `python -B scripts/verify_release.py`. The preparatory run passed the SHA-256 manifest, numeric-record count checks, CKA, M4, G5, k-NN, and saved-prediction checks. Additional reproducibility scripts and their inputs are documented in the archive README.

## Changes from v1.1.0

- `data/regime1/matching/matching_lock.json` and `matched_30_pairs.csv`: six locked checkpoint pairs and 30 downstream contrasts for article §4.2, with `scripts/reaggregate_regime1_matching.py`.
- Pets diagnostic: independent Welch intervals for Supplementary Table S7, derived from six per-run source JSON files per encoding, with reaggregation script.
- Longitudinal sensitivity: 15/15 S2d conditional betweenness records and 15/15 last-crossing task/target contrasts, with independent source-derived reaggregations.
- Figure 3d and S2: verified K1 dagger classification and source-derived graphics; the S2 code is a reproducible reconstruction, not a recovered original script.
- k-NN Table S4: 120 original model/task JSONs, 120 model rows, 20 family rows, original computation/aggregation scripts, and offline verifier.
- Internal Python bytecode files excluded from the integrity manifest.

## Zenodo deposition

Create a **new version of the existing record**, not a new unrelated deposit and not a replacement of the old v1.1.0 file. Starting record: https://zenodo.org/records/23696781. The current **concept DOI** is `10.5281/zenodo.20368592`. Zenodo will assign a **new version-specific DOI** after publishing v1.2.0; do not fabricate it or use the v1.1.0 DOI as if it identified v1.2.0.

Recommended metadata to review in the authenticated Zenodo form:
- **Title:** *vit-pe-transfer: Positional Encoding and Checkpoint Alignment — Numerical Reproducibility (TRANSREP v1.2)*
- **Version:** `1.2.0`
- **Creators, in order:** Banđur, Đoko; Banđur, Miloš; Mićić, Aleksandar.
- **Type:** software and experimental numerical data (retain the existing record's type if the deposit system permits only one).
- **Description:** Numerical records, saved predictions, provenance metadata and source-level reaggregation/figure-generation code supporting *Interpreting Frozen-Feature Transfer in Vision Transformers: Positional Encoding and Checkpoint Alignment*. The v1.2 update completes the article §4.2 checkpoint matching and k-NN S4 source records and adds G4/G5 sensitivity reaggregations and K1 figure-source corrections. Neither journal manuscript nor supplementary article, model checkpoint weights nor source image datasets are included.
- **Rights:** authors' source code under MIT, generated numerical records and figures under CC BY 4.0; these terms do not grant licenses to third-party source images/model weights.
- **Related works:** https://github.com/djokobandjur/vit-pe-transfer (then the exact GitHub v1.2.0 tag once created).

**Before clicking Publish:** inspect the three creator entries, visibility, file name, ZIP size and uploaded file checksum. After publication, record the actual new DOI, public link, publication date and any Zenodo-reported checksum in the repository release metadata.

## Follow-up on GitHub

Once Zenodo has supplied the new version DOI: update the repository root README and `transrep/README.md`; replace the historical §4.2-only map in `transrep/RESULTS_MAP.md` with the v1.2 map; update `transrep/RELEASE_MANIFEST.json` and the citation metadata; then create a v1.2.0 GitHub release/tag if desired. Published v1.1.0 and v1.0.1 tags remain untouched.

This file deliberately does **not** claim that v1.2.0 has been published.
