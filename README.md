# Positional Encoding and Checkpoint Alignment — TRANSREP Reproducibility

**Software and experimental numerical evidence — not the manuscript repository.**

Research by **Đoko Banđur, Miloš Banđur and Aleksandar Mićić** accompanying *Same Accuracy, Different Features: Checkpoint Alignment Changes Positional-Encoding Transfer Rankings in Vision Transformers*.

## Published numerical reproducibility: v1.3.0

- **Latest published version:** [TRANSREP numerical reproducibility v1.3.0](https://doi.org/10.5281/zenodo.24325778), 17 November 2026.
- **All-versions DOI:** https://doi.org/10.5281/zenodo.20368592 (resolves to the latest published Zenodo version).
- **Version-specific DOI for this study's archived evidence:** https://doi.org/10.5281/zenodo.24325778 (identifies the exact v1.3.0 release).
- **Prior version:** [Zenodo v1.2.0](https://doi.org/10.5281/zenodo.23986036) · [GitHub v1.2.0](https://github.com/djokobandjur/vit-pe-transfer/releases/tag/v1.2.0).
- **Release index:** [Result-to-file map](transrep/RESULTS_MAP.md) · [Reproducibility scope](transrep/REPRODUCIBILITY_SCOPE.md) · [v1.3.0 release notes](transrep/RELEASE_NOTES_v1.3.0.md) · [Archive manifest](transrep/RELEASE_MANIFEST_v1.3.0.json).

The **complete portable numerical package is the ZIP on Zenodo**. It is not duplicated in this GitHub repository. The top-level historical `data/`, `models/`, `scripts/`, `notebooks/`, `cka_analysis/`, and `results/` directories largely originate from an earlier three-seed study; they should **not** be interpreted as a complete checkout of the v1.3.0 extended analysis.

## Scientific coverage

| Research component | Archived evidence |
| --- | --- |
| Endpoint cohort E | 24 ImageNet-100 ViT-Base models, four PE configurations, five downstream tasks; original endpoint and frozen-feature results. |
| Longitudinal cohort L | Six independently trained Learned and six RoPE runs; checkpoint comparisons by epoch or upstream accuracy, and Oxford-IIIT Pets depth-resolved analysis. |
| Completed-schedule cohort C | Six Learned and six RoPE models trained under distinct completed schedules; five-task transfer and 26 depth/token readouts. |
| C depth/token analysis | 1,560 model-level scores, with 65 token-readout interaction contrasts D and 130 direct PE contrasts recomputable from archived CSVs. |
| Cohort E at epoch 300 | Twelve E FINAL300 upstream top-1 observations supplied as a model-level CSV; selected readout contrasts based on separate frozen-feature probes. |
| External panel P | Nine fixed public ImageNet-1k DeiT-III checkpoints: APE versus axial and mixed 2D RoPE. No task–size cell meets the specified shared-positive criterion across both rotary variants. |
| Supplementary analyses | CKA, exploratory H depth-dependence, paired L75→L78 change, and exploratory DeiT/Swin whole-system comparisons. |

These are defined training/configuration comparisons; the cross-cohort contrasts do not isolate a direct PE effect independent of optimization history.

## Verify the published v1.3.0 numerical archive

Download `TRANSREP_NUMERICAL_REPRODUCIBILITY_v1.3.0_ZENODO_UPLOAD_READY_2026-11-17.zip` from [Zenodo v1.3.0](https://doi.org/10.5281/zenodo.24325778), extract it, and enter the extracted directory `TRANSREP_NUMERICAL_REPRODUCIBILITY_v1.3.0/`:

```bash
python -m pip install -r requirements-numerical.txt
bash verify_release_all.sh /tmp/transrep-v13-verification
```

Choose a **new output directory outside the extracted release tree**. The unified CPU-only checker verifies the root and inherited manifests, supported core score-level analyses, L/B4-E and cross-cohort aggregates, the E300 upstream CSV arithmetic, and B4-C 65 D / 130 PE contrasts. It does **not** retrain models, re-extract features, fit new probes, or certify the complete original experimental execution.

Trained checkpoint binaries, raw datasets, large feature/activation arrays and the full B4-C REPLAY128 execution tree are not redistributed. See [scope](transrep/REPRODUCIBILITY_SCOPE.md) and the Zenodo archive's root README.

## Historical materials, rights and citation

Original software: **MIT**; original numerical outputs, figures and documentation: **CC BY 4.0**, subject to provenance and third-party rights. Separately hosted checkpoint weights and benchmark images are not relicensed by these notices. See [LICENSE](LICENSE) and [license notes](transrep/LICENSE.md).

The original [v1.0.1 GitHub tag](https://github.com/djokobandjur/vit-pe-transfer/tree/v1.0.1) and [Zenodo v1.0.1](https://doi.org/10.5281/zenodo.20368593) preserve earlier three-seed materials and their attribution.

For the **exact archived numerical evidence** supporting the current manuscript, cite **10.5281/zenodo.24325778**. The **all-versions DOI** `10.5281/zenodo.20368592` is also provided as the persistent project address. The journal manuscript and supplement are separate outputs and are not part of this repository.
