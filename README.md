# Positional Encoding and Checkpoint Alignment — TRANSREP Reproducibility

**Experimental numerical evidence and analysis code, not a manuscript repository.** Research by **Đoko Banđur, Miloš Banđur and Aleksandar Mićić** for *Interpreting Frozen-Feature Transfer in Vision Transformers: Positional Encoding and Checkpoint Alignment*.

> **Release preparation:** Numerical v1.2.0 is verified and prepared for upload as a new version of the existing Zenodo record. The version-specific v1.2.0 DOI has **not yet been issued**. Until that publication, the currently published Zenodo/GitHub release remains **v1.1.0**. This is a staging branch; do not merge into `main` until the new Zenodo version is published and its DOI added.

- **Existing all-versions DOI:** https://doi.org/10.5281/zenodo.20368592
- **Previous published release:** [Zenodo v1.1.0](https://doi.org/10.5281/zenodo.23696781) · [GitHub v1.1.0](https://github.com/djokobandjur/vit-pe-transfer/releases/tag/v1.1.0)
- **v1.2.0 numerical archive filename:** `TRANSREP_EXPERIMENTAL_REPRODUCIBILITY_v1.2.0_PUBLIC_RELEASE_2026-11-05.zip`
- **v1.2.0 archive SHA-256:** `3f7c4b8ce21df74a78f685dbcdd2827a3976d2c7bbf8f20a485e7df85d9f3404`
- **Release documentation:** [Data map](transrep/RESULTS_MAP.md) · [Coverage and limitations](transrep/REPRODUCIBILITY_SCOPE.md) · [Manifest](transrep/RELEASE_MANIFEST.json) · [Release notes](transrep/RELEASE_NOTES_v1.2.0.md)

## Scientific evidence

| Analysis | Design and observation |
| --- | --- |
| Endpoint ViT-B/ImageNet-100 | Four positional-encoding implementations × six independently trained models, evaluated on five downstream tasks. One-dimensional RoPE has higher upstream accuracy and higher endpoint transfer, but upstream accuracy ranges do not overlap. |
| Longitudinal checkpoint comparison | Six Learned and six RoPE runs, 360 measured upstream checkpoint scores and 805 downstream checkpoint–task probes. RoPE leads all 50 equal-epoch mean task cells; at matched upstream accuracy the observed direction differs between Pets and Food-101. |
| Public ImageNet-1k | Nine fixed DeiT-III APE/Axial/Mixed models (Small, Base, Large). In the evaluated panel, 0/15 size–task cells satisfy the joint positive-advantage criterion for both 2D RoPE variants. |
| Depth and CKA | Thirteen readouts across 24 endpoint models; Learned–RoPE excess CKA divergence peaks at Block 10 while the raw-similarity dip around Block 9 is shared across families. |
| Exploratory DeiT–Swin | Independent whole-model-system comparison; not a controlled positional-encoding intervention. |

These results concern the tested configurations and comparison rules, not a causal isolation of positional encoding.

## v1.2.0 numerical reproducibility

The v1.2.0 ZIP contains the original 30 task-level endpoint-matching observations and selection record, 120 k-NN model–task results, full archived longitudinal sensitivity tables, twelve H200 training histories and checkpoint audit records, six earlier RoPE training histories, per-image predictions, recorded model/checkpoint identities, and scripts to reaggregate numerical findings and build figures.

After publication, download the v1.2.0 ZIP from its **version-specific Zenodo record**. Extract it and run:

```bash
cd TRANSREP_experimental_reproducibility_v1.2.0
python -m pip install numpy==2.3.5
python scripts/verify_release.py
python scripts/verify_training_histories.py
```

The current candidate contains **2,962 SHA-256–checked payload files** and an independent 44-entry figure manifest. No source images, trained weights or full CKA activation arrays are included. Offline metric reaggregation does not imply that retraining or full feature extraction can be rerun using only this numerical ZIP.

The top-level historical `data/`, `scripts/`, `models/`, `notebooks/`, `cka_analysis/` and `results/` directories in this GitHub repository are largely materials from the earlier three-seed study; **the v1.2.0 ZIP on Zenodo** is the numerical archive for the extended analysis.

## Historical materials and rights

The immutable [v1.0.1 GitHub tag](https://github.com/djokobandjur/vit-pe-transfer/tree/v1.0.1) and [Zenodo v1.0.1](https://doi.org/10.5281/zenodo.20368593) retain the earlier three-seed study. The original twelve checkpoint weights are linked externally in that historical release; new checkpoint weights are not distributed.

Authors' original code is under **MIT**; included numerical records and generated figures under **CC BY 4.0**, subject to underlying data and third-party rights. Neither these notices nor this release rescind historical permissions or grant rights over separately hosted weights, original ImageNet images or public third-party model binaries. See [LICENSE](LICENSE) and [scope notes](transrep/LICENSE.md).

## Citation

For the expanded numerical archive, cite the **specific v1.2.0 Zenodo version DOI once published**, naming all three creators. The all-versions DOI remains `10.5281/zenodo.20368592`. Until then, the available fixed version is [v1.1.0](https://doi.org/10.5281/zenodo.23696781).

The journal manuscript and supplementary article are separate research outputs; neither is placed in this reproducibility repository.
