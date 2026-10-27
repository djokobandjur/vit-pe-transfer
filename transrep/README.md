# Transferable Representations — experimental reproducibility

This directory indexes **experimental results and reproducibility code only** for *Interpreting Frozen-Feature Transfer in Vision Transformers: Positional Encoding and Checkpoint Alignment* (Đoko Banđur, Miloš Banđur and Aleksandar Mićić). No manuscript, supplementary article, cover letter, or internal editorial document is included.

**Zenodo all-versions DOI:** https://doi.org/10.5281/zenodo.20368592

**Published numerical archive (Zenodo v1.1.0):** [`TRANSREP_EXPERIMENTAL_REPRODUCIBILITY_v1.1_2026-10-27.zip`](https://zenodo.org/records/23696781). **Version DOI:** https://doi.org/10.5281/zenodo.23696781. The archive's displayed MD5 (`c5e221cf58aa1aec971ced849cdd8598`) matches the locally verified release ZIP.

## Evidence

- **Endpoint ImageNet-100:** four PE families × six ViT-Base models = 24 endpoints. Three seeds per family originate in the prior TPAMI study, and three further seeds per family extend the cohort under the same recipe.
- **Longitudinal ImageNet-100:** six Learned and six RoPE training runs, 360 upstream measurements, 805 frozen-feature downstream records and 90 run-level primary comparisons at aligned accuracy.
- **External ImageNet-1k:** nine fixed public DeiT-III model variants (Small/Base/Large × APE/Axial/Mixed 2D RoPE); 45 downstream prediction records.
- **Layerwise/CKA:** 24 models, 13 readouts, 3,588 stored pairwise CKA values and 78 excess-divergence aggregates.
- **Exploratory DeiT–Swin model systems:** 12 common-cache upstream prediction arrays (50,000 images each) and 60 downstream model-task prediction arrays. This is not an isolated positional-encoding test.

The source figure package generates five main and one supplementary scientific plot from saved numeric records.

## Replay

After downloading and extracting the published v1.1 **Zenodo ZIP**, run:

```bash
cd TRANSREP_experimental_reproducibility_v1.1
python -m pip install numpy==2.3.5
python scripts/verify_release.py
```

The published ZIP contains **2,760 verified payload files** and a full `SHA256SUMS` manifest. For figure reproduction see `figures/README.md` and its pinned `requirements.txt`. No source images or model weights are required for numerical reaggregation.

The exploratory checkpoint-matching analysis in Section 4.2 has **task-level summaries**, but the original 30 per-pair records are not included. Large source CKA activation arrays, datasets and full trained-model weights are also excluded; relevant identities are in metadata. See [REPRODUCIBILITY_SCOPE.md](REPRODUCIBILITY_SCOPE.md).

The existing [repository root README](../README.md) documents the earlier three-seed study, which is preserved unchanged in scope. Original historical authorship and licensing remain in force for that material.
