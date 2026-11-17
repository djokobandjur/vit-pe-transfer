# Reproducibility scope — published numerical v1.3.0

**Exact archived release:** https://doi.org/10.5281/zenodo.24325778  
**Latest-version entry point:** https://doi.org/10.5281/zenodo.20368592

This repository holds historical source code and a **documentation index**. The reproducibility distribution is the **Zenodo ZIP**; it is not fully checked out in GitHub.

## Supported without training or GPUs

From the extracted Zenodo v1.3.0 archive, `bash verify_release_all.sh /path/to/new/output` checks:

1. Root and nested core SHA-256 inventories.
2. Historical core stored-record calculations, available prediction-level analyses and selected training/provenance summaries.
3. Longitudinal L, cohort E FINAL300 readouts, C/L/E synthesis and exploratory H and paired L75→L78 calculations.
4. E FINAL300 upstream 12-row CSV statistical consistency and family contrasts.
5. Cohort C B4-C 1,560-score CSV aggregation: **65 D**, **130 direct PE contrasts**, and associated group means, compared with stored tables.

Install the archive-root `requirements-numerical.txt` first. Generated files/logs belong outside the extracted release tree. A verification PASS indicates agreement of **the specific supplied numerical records and computations**, not an independent retraining or authentication of full experimental origin.

## Not supplied by the portable ZIP

- Raw ImageNet or downstream benchmark images, checkpoint weights, full extracted features or CKA activations.
- The complete external B4-C REPLAY128 source tree and its original raw MAP execution environment.
- End-to-end training, feature extraction, refitting of probes, or exact regeneration of every historical figure.
- All original cohort-E training history JSONs. The additional FINAL300 upstream result is a **CSV-only publication** whose statistical summary can be recomputed; original histories remain in the authors' project records. Inherited earlier RoPE histories in the core archive are not a full 12-model E300 history set.

## Interpretation and attribution

The L matched-upstream analysis uses scalar-score interpolation across evaluated checkpoints; no weights are interpolated. The same numeric seed labels across PE families do not establish an experimental pairing block. Public fixed-model image-bootstrap intervals reflect image sampling, not training-run variation. Post hoc H and cross-cohort C/E comparisons are exploratory; C and E are **separate training cohorts**, not time points of the same models.

The archive and GitHub repository are subject to their recorded **MIT** software / **CC BY 4.0** generated-record notices and separate third-party/data rights. Historic material is preserved rather than rewritten.
