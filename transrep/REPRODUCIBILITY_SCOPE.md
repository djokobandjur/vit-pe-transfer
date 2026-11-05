# Reproducibility scope — numerical v1.2.0

Published Zenodo version: https://doi.org/10.5281/zenodo.23986036; all-versions DOI: https://doi.org/10.5281/zenodo.20368592.

The released ZIP supports independently verifying file checksums, reaggregating saved individual model predictions and downstream metrics, reconstructing figures, and checking stored training-history metadata, without source images or GPUs.

**Included:** observations for 24 ImageNet-100 ViT-B endpoints, six-pair endpoint matching (30 individual downstream values), 360 H200 longitudinal upstream measurements, 805 downstream probes, twelve complete 300-epoch H200 training histories and twelve checkpoint audit records, six historical RoPE training histories, original 120 k-NN results, nine public-model downstream prediction sets (45 model–task records), 3,588 CKA pairwise similarities, 78 depth/CKA aggregates, and exploratory 12-model DeiT–Swin records. Supplementary sensitivity summaries and figure reconstruction programs are included.

**Not included:** source datasets and original ImageNet images, full endpoint/longitudinal checkpoint weight binaries, full CKA activation matrices, journal manuscript, supplementary article, or an authenticated machine-by-machine historical execution snapshot. Model identities and recorded checkpoint SHA-256 hashes are supplied where available.

The first-crossing matched-upstream analysis uses **interpolation of downstream scalar scores** between evaluated checkpoint endpoints, not interpolation or retraining of weights. Reused numeric seed names are not randomized pairing blocks. Image-bootstrap intervals for fixed public checkpoints measure test-image sampling variability, not run-to-run training variability. The exploratory DeiT–Swin comparison concerns full model systems.

The six historical RoPE histories originate from earlier experiments; two have five missing logged entries each, which have **not been imputed**. The original endpoints and separate H200 longitudinal models are different training cohorts. Any further re-training or inference requires external dependencies and files not contained in the numerical ZIP.
