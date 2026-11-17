# Scientific result → published numerical v1.3.0 source map

**Published version DOI:** https://doi.org/10.5281/zenodo.24325778  
**All-versions DOI:** https://doi.org/10.5281/zenodo.20368592

**Path convention:** all paths below are **inside** the extracted `TRANSREP_NUMERICAL_REPRODUCIBILITY_v1.3.0/` folder of the Zenodo ZIP, **not** paths in this GitHub repository. Historical subdirectory names are retained for traceability, even where they contain older local working-version labels.

| Evidence / analysis | Location inside v1.3.0 ZIP | Reproducibility boundary |
| --- | --- | --- |
| Earlier E endpoint transfer, upstream, k-NN and CKA | `reproducibility/01_core_numerical_v1.2.0_WORKING/data/regime1/`, `data/cka/` and `outputs/` | Earlier numerical records; source archive is a historical working extension, not identical to the published v1.2.0 ZIP. |
| Longitudinal L upstream checkpoint scores and transfer | `reproducibility/01_core_numerical_v1.2.0_WORKING/data/regime2/` | Saved checkpoint-level and transfer observations; prior verification scripts retained in nested archive. |
| Public DeiT-III ImageNet-1k panel P | `reproducibility/01_core_numerical_v1.2.0_WORKING/data/regime3/` | Fixed public-checkpoint scores and available prediction records. |
| Completed-schedule cohort C | `reproducibility/02_cohort_C/` | Source Step 08 probe records, aggregates and provenance. |
| Cohort C readout/depth B4-C | `reproducibility/03_B4C_CORE_MAP/B4_MAP_1560_seed_level.csv` | 1,560 model-level scores; score-level reaggregation only. |
| C token-readout D and direct PE contrasts | `reproducibility/03_B4C_CORE_MAP/recompute_b4c_from_seed_csv.py` | Recomputes 65 D and 130 PE contrasts and checks archived CSVs; original REPLAY128 raw replay requires external records. |
| L Oxford-IIIT Pets depth readouts, K | `reproducibility/04_L_READOUT/` | 288 refitted depth probes and available run-level results. |
| E FINAL300 readout D/K | `reproducibility/05_B4E_FINAL300/` | 240 archived probe records across selected depths/readouts. |
| C/L/E derived comparisons | `reproducibility/06_synthesis_and_derived/` | Saved numerical cross-cohort analysis; exploratory comparisons are not longitudinal tracking of identical models. |
| Protocol and execution provenance | `reproducibility/07_protocols_and_execution/` | Selected recorded source methods and metadata; full original runtime tree not redistributed. |
| E FINAL300 upstream validation | `reproducibility/08_E300_UPSTREAM_VALIDATION/` | Twelve-row published model-level CSV and statistical arithmetic; original full histories kept by authors. |
| Exploratory H and paired L75→L78 | `reproducibility/09_v0857_exploratory/` | Post hoc, clearly distinguished from primary locked analyses. |

## Unified verification

In the extracted Zenodo ZIP:

```bash
python -m pip install -r requirements-numerical.txt
bash verify_release_all.sh /tmp/transrep-v13-check
```

The root `SHA256SUMS.txt` covers **3,511 files**; the ZIP contains **3,512 members** including the manifest itself. For the full supported scope, see [REPRODUCIBILITY_SCOPE.md](REPRODUCIBILITY_SCOPE.md). No weight files, raw benchmark images or large original feature arrays are redistributed.
