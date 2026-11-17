# TRANSREP — published numerical-reproducibility index

**Current published archive:** [Zenodo v1.3.0](https://doi.org/10.5281/zenodo.24325778), 17 November 2026.

- **All-versions DOI:** https://doi.org/10.5281/zenodo.20368592
- **This exact release:** https://doi.org/10.5281/zenodo.24325778
- **Prior published v1.2.0:** https://doi.org/10.5281/zenodo.23986036

This directory is a **GitHub documentation index** for the full **Zenodo numerical ZIP**; it is not the full v1.3.0 archive itself. The top-level GitHub files remain primarily historical earlier-study code and data.

- [Results and archive paths](RESULTS_MAP.md)
- [Supported and unsupported reproduction](REPRODUCIBILITY_SCOPE.md)
- [v1.3.0 release metadata and checksum](RELEASE_MANIFEST_v1.3.0.json)
- [v1.3.0 release notes](RELEASE_NOTES_v1.3.0.md)
- [Historical v1.2.0 manifest](RELEASE_MANIFEST.json) and [release notes](RELEASE_NOTES_v1.2.0.md)
- [Licensing and source rights](LICENSE.md)

## Reproduce score-level analyses

Download and extract the [Zenodo v1.3.0 ZIP](https://doi.org/10.5281/zenodo.24325778), then from its top-level extracted directory run:

```bash
python -m pip install -r requirements-numerical.txt
bash verify_release_all.sh /tmp/transrep-v13-check
```

Supply a new output path outside the archive. This checks file integrity, the inherited core numerical release, L/B4-E/synthesis and exploratory calculations, the E300 upstream twelve-row CSV, and 65 + 130 B4-C CSV-derived contrasts. These are **CPU-only numerical verifications**, not original training or GPU-extraction replays.

The archived v1.3.0 distribution omits model weights, source images, large feature arrays and the full original execution tree. The E FINAL300 additional upstream measurements are supplied as a CSV, and the checker recomputes its statistics rather than independently verifying their original history-to-checkpoint provenance.

The [v1.0.1 historical source snapshot](https://github.com/djokobandjur/vit-pe-transfer/tree/v1.0.1) remains accessible; historical permissions are unchanged.
