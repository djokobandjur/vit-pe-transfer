# Positional Encoding and Checkpoint Alignment — TRANSREP Reproducibility

**Experimental evidence and reproducibility software**, not a manuscript repository.

This repository now indexes the numerical records for **“Interpreting Frozen-Feature Transfer in Vision Transformers: Positional Encoding and Checkpoint Alignment”** by **Đoko Banđur, Miloš Banđur and Aleksandar Mićić**. The new experiments extend an earlier four-encoding, three-seed ViT-Base study. The scientific reporting for the extended TRANSREP analysis is in the separate journal submission; neither its manuscript nor its supplementary article is included here.

- **Exact numerical release:** [Zenodo v1.1.0 — 10.5281/zenodo.23696781](https://doi.org/10.5281/zenodo.23696781)
- **All-versions DOI:** [10.5281/zenodo.20368592](https://doi.org/10.5281/zenodo.20368592)
- **GitHub release:** [v1.1.0](https://github.com/djokobandjur/vit-pe-transfer/releases/tag/v1.1.0)
- **Reproduction scope:** [`transrep/README.md`](transrep/README.md) · [results-to-files map](transrep/RESULTS_MAP.md) · [integrity manifest](transrep/RELEASE_MANIFEST.json)

## What the experiments show

| Evidence | Models / design | Main observation |
| --- | --- | --- |
| Endpoint frozen-feature benchmark | Four positional-encoding families, six runs each (24 ViT-B ImageNet-100 endpoints), five downstream datasets | RoPE has higher upstream accuracy than the other families and leads Learned on endpoint transfer for all five tasks; the upstream accuracy ranges do not overlap, so endpoint contrasts alone cannot separate encoding from upstream performance. |
| Longitudinal checkpoints | Six independently trained Learned + six RoPE models, with snapshots across training | At equal epochs RoPE leads in all 50 task–epoch cells. At the **same measured upstream accuracy** (70%, 75%, 78%), the direction depends on task: RoPE favors Pets (+4.9 to +6.0 percentage points), while Learned favors Food-101 (RoPE minus Learned −1.2 to −2.1 points). |
| External ImageNet-1k evaluation | Nine public DeiT-III APE, Axial 2D RoPE and Mixed 2D RoPE checkpoints across Small/Base/Large | **0/15** size–task cells satisfy the prespecified criterion for a positive frozen-transfer advantage shared by both rotary geometries. |
| Layerwise frozen transfer and CKA | 24 endpoint models; 13 readouts and seed-referenced CKA | Largest RoPE–Learned transfer gaps occur in later blocks. A raw-similarity dip around block 9 occurs in all PE families; **Learned–RoPE excess divergence peaks at block 10**, not block 9. |
| Exploratory DeiT–Swin systems | Six DeiT-Base and six Swin-Base independently trained models | Whole-model-system comparison; not an intervention isolating positional encoding. |

These observations describe the specific evaluated model cohorts and comparison rules. Detailed definitions of metrics, seed labels, uncertainty and reproducibility boundaries appear in the archived numerical records.

## Find the numerical evidence

Download `TRANSREP_EXPERIMENTAL_REPRODUCIBILITY_v1.1_2026-10-27.zip` from the [Zenodo version record](https://zenodo.org/records/23696781). The ZIP includes archived observations, model identities and checksums, reaggregation scripts, and data/code for five scientific figures plus one supplemental figure. The ZIP contains neither journal manuscript nor supplementary article.

[**Open the section/figure/table → file map**](transrep/RESULTS_MAP.md).

The top-level `data/`, `scripts/`, `models/`, `notebooks/`, `cka_analysis/` and `results/` directories in GitHub remain **historical three-seed materials**. They do not by themselves reproduce the full six-seed TRANSREP analysis; use the Zenodo v1.1.0 ZIP for that.

### Reproduce the numeric release

From the extracted Zenodo archive directory:

```bash
python -m pip install numpy==2.3.5
python scripts/verify_release.py
```

See `figures/README.md` inside the archive for plotting requirements and scripts. The release contains 2,760 SHA-256–checked payload files. Recomputing selected numerical summaries does not require GPU, source images, or checkpoint weights. Training the models or regenerating the original activation arrays is a separate undertaking.

**Coverage boundary:** Exploratory endpoint matching (manuscript §4.2) is documented at the task-summary level; the original 30 individual matched-pair rows and matching-lock metadata are not distributed in v1.1.0.

## Historical three-seed study (v1.0.1)

The prior study used 12 ImageNet-100 ViT-Base models (four PE families × three seeds) and reported descriptive endpoint probe and raw CKA patterns. Its original material and wording are preserved at the immutable historical [v1.0.1 tag](https://github.com/djokobandjur/vit-pe-transfer/tree/v1.0.1) and [Zenodo v1.0.1](https://doi.org/10.5281/zenodo.20368593).

**Interpretive distinction:** The historical endpoint ordering and raw block-9 CKA dip are **not** the conclusions of the expanded, checkpoint-aligned analysis. In particular, the four-family order is not invariant across datasets or alignment rules, and a common raw CKA dip does not establish PE-specific excess divergence.

Historical scripts and instructions remain accessible under the original `models/`, `scripts/`, `notebooks/`, `results/` and `cka_analysis/` directories on the current branch. The twelve original ViT-B checkpoints are **linked** from the historical release and hosted externally on [Google Drive](https://drive.google.com/drive/folders/1WRhjaR3WZHIi2fTi9xcrIBJkBXZddMM9); the weights are **not** included in GitHub or the Zenodo numerical ZIP. The other trained checkpoint weights are not supplied through these releases. Source ImageNet images are not distributed.

## Licenses and access conditions

- Authors' repository code: **MIT**.
- Authors' experimental numeric records, documentation and generated plots: **CC BY 4.0**.
- The historical trained checkpoints are available via a separately hosted link, **not included in the licensed numerical archive**. The older README and LICENSE described their terms as “CC BY 4.0 for research purposes,” which was inconsistent: CC BY itself permits commercial use. This README makes **no new or retroactive rights determination** for those weights. Users must examine the [original ImageNet access agreement](https://image-net.org/accessagreement), the historical checkpoint notices and any relevant permissions before redistributing or using the weights. A change to CC BY-NC cannot retroactively withdraw earlier CC BY permissions.
- NAVER AI public DeiT-III model weights and source images are not redistributed here; their identifiers and provenance are recorded in the Zenodo package.

See [LICENSE](LICENSE) and [TRANSREP attribution notes](transrep/LICENSE.md) for the scope of the included software and numerical data. Historical licenses and author attribution are preserved through prior version tags.

## Citation

When using the **extended numerical results**, cite the deposited version with **all three creators**:

> Banđur, Đ., Banđur, M., & Mićić, A. (2026). *vit-pe-transfer: Positional Encoding and Checkpoint Alignment — Numerical Reproducibility (TRANSREP v1.1)* (Version 1.1.0) [Computer software and numerical data]. Zenodo. https://doi.org/10.5281/zenodo.23696781

The all-versions DOI is `10.5281/zenodo.20368592`. For historical three-seed work, cite the separately tagged earlier record.

**Repository note:** The GitHub v1.1.0 tag marks the code/documentation at release time; this `main` README incorporates subsequent published-DOI and interpretation clarifications. No published tag or Zenodo archive has been silently altered.
