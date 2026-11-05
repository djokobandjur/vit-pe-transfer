# Scientific results → numerical v1.2.0 archive

**Published archive:** [Zenodo v1.2.0](https://doi.org/10.5281/zenodo.23986036), version DOI `10.5281/zenodo.23986036`. Existing Zenodo concept DOI: https://doi.org/10.5281/zenodo.20368592. The paths below are **inside** the extracted `TRANSREP_experimental_reproducibility_v1.2.0/` directory, not GitHub paths.

| Evidence in article | Source in the numerical ZIP | Scope |
| --- | --- | --- |
| Endpoint ImageNet-100, Figure 2 | `data/regime1/upstream_accuracy.csv`, `data/regime1/upstream_downstream_joined.csv`, `data/regime1/linear_probe/` | 24 models × 5 downstream tasks |
| Exploratory six-seed endpoint matching (§4.2) | `data/regime1/matching/matching_lock.json`, `data/regime1/matching/matched_30_pairs.csv`; `scripts/reaggregate_regime1_matching.py` | Six selected RoPE snapshots and 30 individual task metrics |
| Longitudinal matched accuracy, Figure 3(a–d) | `data/regime2/upstream_360.csv`, `data/regime2/all_805_scores.csv`, `data/regime2/primary_fixed3_seed_pairs_90.csv`; `scripts/verify_release.py` | 360 upstream scores, 805 probes, 90 target–task–seed comparisons |
| Equal-epoch transfer, Figure 3(e) | `data/regime2/secondary_same_epoch_seed_pairs_300.csv`, `data/regime2/secondary_same_epoch_summary_50.csv` | 50 task–epoch mean comparisons |
| Longitudinal training histories and audits | `data/regime2/training_runs/`, `metadata/training_audits/`; `scripts/verify_training_histories.py` | Twelve 300-epoch histories, 360 recorded checkpoint SHA-256 identifiers |
| Earlier original RoPE training histories | `data/regime1/historical_rope_histories/` | Six supplied histories; ten total logged entries missing in two runs, not reconstructed |
| Upstream-alignment sensitivity | `data/regime2/sensitivity/`; `scripts/reaggregate_last_crossing.py`, `scripts/reaggregate_s2d_betweenness.py` | First/last crossing and conditional bracketing checks |
| Original cosine k-NN | `outputs/knn/`; `scripts/verify_knn_s4.py` | 120 original model–task records |
| Public DeiT-III panel, Figure 4 | `data/regime3/`, `data/regime3/analysis/` | Nine models, 45 model–task prediction files |
| Layerwise transfer and CKA, Figure 5 | `data/depth/`, `data/cka/`; `metadata/external_cka_feature_manifest.json` | Thirteen readouts, 3,588 CKA pairs and 78 aggregates |
| Exploratory DeiT–Swin | `data/step9/` | Twelve whole-model system records; no isolated PE interpretation |
| Main/Supplementary figure reconstruction | `figures/figure_data/`, `figures/build_figures.py`, `figures/build_figures_4_5.py`, `figures/build_supplement_figure.py`, `figures/build_figure_s2_k1.py` | Five main figures and Supplementary Figures S1/S2 |

## Verification and boundaries

`SHA256SUMS`: 2,962 payload files; `figures/SHA256SUMS.txt`: 44 figure-subdirectory files. `scripts/verify_release.py` and `scripts/verify_training_histories.py` verify saved numerical records and selected recomputations **without GPU**. The ZIP does not include datasets, model weight binaries or the full CKA feature arrays; not all model training and feature extraction can be independently rerun from its contents.
