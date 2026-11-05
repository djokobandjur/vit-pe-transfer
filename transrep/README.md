# TRANSREP — numerical reproducibility files

This folder indexes **numerical evidence, source code and reproducibility metadata** for *Interpreting Frozen-Feature Transfer in Vision Transformers: Positional Encoding and Checkpoint Alignment* by Đoko Banđur, Miloš Banđur and Aleksandar Mićić.

**Published numerical v1.2.0:** [10.5281/zenodo.23986036](https://doi.org/10.5281/zenodo.23986036) (5 November 2026). Prior numerical release: [v1.1.0](https://doi.org/10.5281/zenodo.23696781). All-versions DOI: https://doi.org/10.5281/zenodo.20368592.

The v1.2.0 ZIP on Zenodo, **not** the historical GitHub top-level result files, will contain the complete extended numerical evidence. See the [result-to-file map](RESULTS_MAP.md), [scope and limitations](REPRODUCIBILITY_SCOPE.md), [v1.2.0 manifest](RELEASE_MANIFEST.json), and [release notes](RELEASE_NOTES_v1.2.0.md).

## Numerical verification

After obtaining and extracting `TRANSREP_EXPERIMENTAL_REPRODUCIBILITY_v1.2.0_PUBLIC_RELEASE_2026-11-05.zip`:

```bash
cd TRANSREP_experimental_reproducibility_v1.2.0
python -m pip install numpy==2.3.5
python scripts/verify_release.py
python scripts/verify_training_histories.py
python scripts/reaggregate_regime1_matching.py
python scripts/reaggregate_last_crossing.py
```

The v1.2.0 release includes **2,962 checksum-inventoried files**, twelve complete H200 Learned/RoPE training histories, twelve checkpoint audit records, six historic original RoPE training histories, and the seed-level exploratory endpoint matching evidence. It does not include the full checkpoint weights, source images, full CKA source arrays, manuscript or supplementary article.

The prior three-seed study remains available at [v1.0.1](https://github.com/djokobandjur/vit-pe-transfer/tree/v1.0.1); its historical permissions are unchanged.
