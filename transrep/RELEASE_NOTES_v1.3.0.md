# TRANSREP numerical reproducibility v1.3.0 — GitHub documentation update

**Published on Zenodo:** 17 November 2026

- **Version-specific DOI:** https://doi.org/10.5281/zenodo.24325778
- **All-versions DOI:** https://doi.org/10.5281/zenodo.20368592
- **Prior v1.2.0 DOI:** https://doi.org/10.5281/zenodo.23986036
- **Download location:** Zenodo v1.3.0 record; the full numerical ZIP is **not reuploaded to this GitHub source repository**.

## Added to the Zenodo v1.3.0 numerical evidence

- Cohort C completed schedules and their original archived source probes and aggregate tables.
- Cohort C B4-C analysis: 1,560 model-level depth/token scores, 65 D token-readout interaction contrasts and 130 direct PE contrasts, plus independent CSV-only reaggregation.
- Cohort L Oxford-IIIT Pets depth extension, including 288 refitted probes and K(75)/K(78) numerical calculations.
- Cohort E FINAL300 readout records (240 selected probes), plus its 12-model upstream top-1 **CSV** and derived summary.
- Cross-cohort C/L/E summaries and exploratory H and paired L75→L78 analyses.
- Five-stage CPU numerical verification entry point, `requirements-numerical.txt`, file-integrity checks and provenance information in the ZIP.

## Scope

Portable numerical verification does not re-execute training, GPU feature extraction or fitting of probes, and it does not redistribute original images, checkpoint weights or the complete REPLAY128 runtime tree. The E300 upstream CSV checker verifies arithmetic from the published table, not full source-log/checkpoint identity.

The v1.2.0 numerical release remains available under its own DOI. Historic GitHub source directories and published tags remain unchanged.
