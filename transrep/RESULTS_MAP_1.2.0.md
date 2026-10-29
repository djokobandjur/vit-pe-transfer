# TRANSREP v1.2.0 numerical evidence map (prepared archive)

**Status:** v1.2.0 archive prepared and hash-verified; **version-specific Zenodo DOI pending publication**. The published v1.1.0 scientific-results map remains at [RESULTS_MAP.md](RESULTS_MAP.md).

All paths below are **inside** `TRANSREP_EXPERIMENTAL_REPRODUCIBILITY_v1.2.0_RELEASE_READY_2026-10-29.zip`, relative to its single extracted root `TRANSREP_experimental_reproducibility_v1.2.0/`. The manuscript and supplementary article are **not** inside this data archive.

| Article result | v1.2.0 source / replay path | Boundary |
| --- | --- | --- |
| §4.1 endpoint benchmarks, Figure 2 | `data/regime1/upstream_accuracy.csv`, `data/regime1/upstream_downstream_joined.csv`, `data/regime1/linear_probe/`; `figures/build_figures.py` | 24 checkpoints across 4 PE families × 6 seeds, five downstream tasks |
| §4.2 exploratory endpoint matching | `data/regime1/matching/matching_lock.json`, `data/regime1/matching/matched_30_pairs.csv`; `scripts/reaggregate_regime1_matching.py` | 6 upstream-locked pairs, 30 original task–seed contrasts; matches upstream top-1 rather than isolating causal PE effect |
| §4.3 matched-upstream trajectories, Figure 3 | `data/regime2/upstream_360.csv`, `data/regime2/all_805_scores.csv`, `data/regime2/primary_fixed3_seed_pairs_90.csv`; `figures/build_figures.py` | 90 seed-level primary contrasts, 15 task/target summaries |
| §4.4 equal-epoch trajectories, Figure 3e | `data/regime2/secondary_same_epoch_seed_pairs_300.csv`, `data/regime2/secondary_same_epoch_summary_50.csv` | 50 task–epoch cells |
| §4.5 public DeiT-III panel, Figure 4 | `data/regime3/analysis/` and `data/regime3/*.test_predictions.npz`; `figures/build_figures_4_5.py` | 9 fixed public models, 45 downstream predictions, 15 group tests |
| §4.6 depth and CKA, Figure 5 | `data/depth/`, `data/cka/cka_pairs.csv`, `data/cka/cka_excess_divergence.csv`; `figures/build_figures_4_5.py` | Archived CKA scalar records are complete; large original activation matrices excluded |
| DeiT–Swin exploratory comparison | `data/step9/` | 12 trained whole-model systems; no isolated PE inference |
| Supplementary Table S2b and †, Figure 3d / Supplementary Figure S2 | `data/regime2/primary_fixed3_seed_pairs_90.csv`, `figures/k1_readout_inference.py`, `figures/verify_k1_symbols.py`, `figures/build_figure_s2_k1.py` | S2 plotting script is a reproducible reconstruction, not recovered original code |
| Supplementary Table S2d | `data/regime2/sensitivity/conditional_betweenness_S2d_15.csv`; `scripts/reaggregate_s2d_betweenness.py` | 15 conditional betweenness cells; not inferential confidence intervals |
| Supplementary Note 12 last crossing | `data/regime2/sensitivity/last_upward_crossing_summary_15.csv`; `scripts/reaggregate_last_crossing.py` | 15 task–target contrasts; downstream scores interpolate between evaluated checkpoints |
| Supplementary Table S4 k-NN | `outputs/knn/*.json`, `outputs/knn/revised_knn_model_results.csv`, `outputs/knn/revised_knn_family_summary.csv`; `scripts/13_revised_knn.py`, `scripts/14_aggregate_knn.py`, `scripts/verify_knn_s4.py` | 120 original recorded results (primary k=20 and sensitivity), 20 family aggregates; feature arrays/CUDA not distributed |
| Supplementary Table S7 Pets | `data/diagnostics/pets/`; `scripts/reaggregate_pets_s7_welch.py` | Independent Welch nominal exploratory intervals from archived per-model scores |

## Verification and licensing

- `SHA256SUMS`: 2,916 checksummed payload files.
- `scripts/verify_release.py`: offline integrity and numeric checks.
- `metadata/release_scope.json`: included and omitted evidence.
- Code MIT; original numerical records and generated figures CC BY 4.0. Checkpoint weights and source images are not redistributed.

**Integrity:** v1.2.0 release ZIP SHA-256 `df56bc0b5fafed4c2198fcb63782153be9376422a22cf9dcecdf1412ea559fd5`. See [release preparation metadata](RELEASE_1.2.0_PREPARATION.md) before publishing.
