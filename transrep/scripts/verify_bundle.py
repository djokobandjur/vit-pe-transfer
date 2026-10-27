#!/usr/bin/env python3
"""Validate the integrity of a TRANSREP numerical-release ZIP (standard library)."""
import hashlib
import sys
import zipfile
from pathlib import PurePosixPath

def check(path):
    with zipfile.ZipFile(path) as z:
        assert z.testzip() is None, "Corrupt ZIP member"
        top = "TRANSREP_experimental_reproducibility_v1.1/"
        sha_path = top + "SHA256SUMS"
        assert sha_path in z.namelist(), "No SHA256SUMS"
        checks = z.read(sha_path).decode("utf-8").splitlines()
        for entry in checks:
            expected, relative = entry.split("  ", 1)
            assert not PurePosixPath(relative).is_absolute()
            member = top + relative
            observed = hashlib.sha256(z.read(member)).hexdigest()
            assert observed == expected, relative
        assert len(checks) == 2759, f"Unexpected release size: {len(checks)}"
        forbidden = ("manuscript_", "cover_letter", "supplement_v", "internal_")
        assert not any(any(t in name.lower() for t in forbidden) for name in z.namelist())
        print(f"PASS: {len(checks)} members, ZIP CRC, SHA-256 and publication-file exclusion")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python transrep/scripts/verify_bundle.py /path/to/release_v1.1.zip")
    check(sys.argv[1])
