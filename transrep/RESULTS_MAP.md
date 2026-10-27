# TRANSREP scientific results → public numerical release paths

Versioned archive: [Zenodo v1.1.0](https://doi.org/10.5281/zenodo.23696781) (all-versions DOI: [10.5281/zenodo.20368592](https://doi.org/10.5281/zenodo.20368592)).

All paths in the table are **relative to the root of the extracted ZIP directory** `TRANSREP_experimental_reproducibility_v1.1/`. Paths in this document index the published archive and are **not GitHub repository files**, except for the separately linked source `transrep/` instructions and historical 12-model code.

| Results section / illustration | Primary source file(s) in the ZIP | Purpose and scope |
| --- | --- | --- |
| §4.1, Figure 2: 24-model upstream scores and frozen endpoint transfer | `data/regime1/upstream_accuracy.csv`, `data/regime1/upstream_downstream_joined.csv`, `data/regime1/linear_probe/revised_probe_family_summary.csv`; individual probe JSONs under `data/regime1/linear_probe/` | Six seeds per PE family, upstream top-1 and five downstream task metrics. |
| §4.2: exploratory endpoint matching | **No individual matched-pair source file in this release** | This analysis is reported at task-summary level in the article. Original `matched_30_pairs.csv` and `matching_lock.json` are not distributed; do not claim pair-level replay. |
| §4.3, Figure 3(a–d), transfer at matched upstream accuracy | `data/regime2/upstream_360.csv`, `data/regime2/all_805_scores.csv`, `data/regime2/primary_fixed3_seed_pairs_90.csv`, `data/regime2/primary_fixed3_summary_15.csv`, `data/regime2/method_lock.json` | Upstream measurements, individual probe records, 90 run-task-target comparisons and 15 aggregated task-target contrasts. |
| §4.4, Figure 3(e): equal-epoch analysis | `data/regime2/secondary_same_epoch_seed_pairs_300.csv`, `data/regime2/secondary_same_epoch_summary_50.csv` | 300 seed-level values and 50 task-by-epoch summaries; upstream trajectory in `data/regime2/upstream_360.csv`. |
| §4.5, Figure 4: nine public DeiT-III models | `data/regime3/analysis/TRANSREP_G7_primary_IUT_15cells_v1.csv`, `data/regime3/analysis/TRANSREP_G7_model_metrics_v1.csv`, `data/regime3/analysis/TRANSREP_G7_all_contrasts_v1.csv`; `data/regime3/*.test_predictions.npz`; `metadata/checkpoints/TRANSREP_NAVER_AI_HF_model_identity_manifest_v0.1_2026-10-24.csv` | 15 size–task tests, 45 model–task predictions, fixed public model identities and image-sampling bootstrap outputs. |
| §4.6, Figure 5: depth and CKA | `data/depth/layerwise/revised_layerwise_family_summary.csv`, `data/depth/inference/rope_learned_all_13_layers.csv`, `data/cka/cka_pairs.csv`, `data/cka/cka_within_family.csv`, `data/cka/cka_excess_divergence.csv`, `data/cka/cka_between_family.csv` | Layerwise transfer and seed-referenced CKA; per-model readout JSONs under `data/depth/layerwise/`; feature-array hashes in `metadata/external_cka_feature_manifest.json`. |
| §4.7: exploratory DeiT–Swin | `data/step9/summary/STEP9_UNPAIRED_PERM924_EXPLORATORY_v1.csv`, `data/step9/summary/STEP9_G6_60_INDIVIDUAL_SCORES.csv`, `data/step9/summary/STEP9_S7_12_UPSTREAM_TOP1.csv`, `data/step9/g6/*.test_predictions.npz`, `data/step9/s7/*.npz` | Six whole-model systems per architecture, saved upstream predictions, 60 downstream evaluations and exact exploratory inference. |
| Figure 1: research workflow | `figures/figures/Figure_1_argument_flow.pdf`; `figures/build_figures.py` | Diagram of analysis design; not a new experiment. |
| Figure 2: endpoint transfer | `figures/figures/Figure_2_endpoint_transfer.pdf`; `figures/figure_data/regime1_upstream_downstream_joined.csv` | Plot-ready endpoint data. |
| Figure 3: trajectories, matched accuracy and equal epochs | `figures/figures/Figure_3_longitudinal_comparison.pdf`; `figures/figure_data/primary_fixed3_seed_pairs_90.csv`, `figures/figure_data/regime2_secondary_same_epoch_summary_50.csv`, `figures/figure_data/upstream_360.csv` | Plot-ready run-level interpolation and same-epoch summaries. |
| Figure 4: public-model evaluation | `figures/figures/Figure_4_external_public_validation.pdf`; `figures/figure_data/regime3_primary_IUT_15cells.csv`, `figures/figure_data/regime3_upstream_9.csv` | Shared-positive-rule contrasts and upstream relative to APE. |
| Figure 5: depth and representational similarity | `figures/figures/Figure_5_depth_and_cka.pdf`; `figures/figure_data/depth_layerwise_summary.csv`, `figures/figure_data/cka_excess_divergence.csv` | Plot-ready layerwise/CKA inputs. |
| Supplementary Figure S1 | `figures/figures/Supplementary_Figure_S1_remaining_trajectories.pdf`; `figures/build_supplement_figure.py` | Individual longitudinal plots for remaining downstream tasks. |

## Integrity and numerical reproducibility

- `SHA256SUMS` — 2,760 individual payload checksums.
- `scripts/verify_release.py` — GPU-free numerical/integrity verification.
- `metadata/release_scope.json` — packaged evidence scope and documented omissions.
- `metadata/checkpoints/CHECKPOINT_MANIFEST.csv` — recorded training/model identities.
- `figures/README.md` and `figures/requirements.txt` — figure generation and pinned Python library versions.

The archived plots are **research figures only**. The numerical ZIP does not contain a manuscript or supplementary article. The public `v1.1.0` GitHub release snapshots documentation and code, while the separate Zenodo ZIP contains full numerical evidence.
