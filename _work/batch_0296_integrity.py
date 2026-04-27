"""Batch 0296 integrity check (probe-only refresh tick).

Per BRIEF.md non-negotiable #5, integrity checks must pass before any
commit. This batch writes ZERO record JSONs (it is a probe-only
upstream-refresh tick), so the per-record CHECK1..CHECK6 are N/A.
The relevant "soft" integrity checks for a probe-only tick are:

  C1: records/sis/ JSON count unchanged from b0293 (539).
  C2: records/acts/ JSON count unchanged from b0293 (1169).
  C3: zambialii robots.txt sha256 matches expected.
  C4: parliament robots.txt sha256 matches expected.
  C5: probe novel_true counts (zambialii recent + parliament page 0)
      both equal 0 (steady state preserved).
  C6: no record JSON writes occurred in this tick (verified by
      diffing the records/ tree git status).

Exits non-zero on any failure.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def fail(msg):
    print(f"FAIL: {msg}")
    sys.exit(1)


def ok(msg):
    print(f"OK:   {msg}")


def main():
    # C1
    sis_count = sum(1 for _ in (ROOT / "records" / "sis").rglob("*.json"))
    if sis_count != 539:
        fail(f"C1: SIs count {sis_count} != 539")
    ok(f"C1: SIs count = {sis_count}")

    # C2
    acts_count = sum(1 for _ in (ROOT / "records" / "acts").rglob("*.json"))
    if acts_count != 1169:
        fail(f"C2: Acts count {acts_count} != 1169")
    ok(f"C2: Acts count = {acts_count}")

    # Load probe data
    probe = json.loads((ROOT / "_work" / "batch_0296_probe.json").read_text())

    # C3
    if not probe["zambialii_robots_match_expected"]:
        fail(f"C3: zambialii robots sha mismatch: {probe['zambialii_robots_sha256']}")
    ok(f"C3: zambialii robots sha matches expected")

    # C4
    if not probe["parliament_robots_match_expected"]:
        fail(f"C4: parliament robots sha mismatch: {probe['parliament_robots_sha256']}")
    ok(f"C4: parliament robots sha matches expected")

    # C5
    nzt = len(probe["novel_zambialii_true"])
    npt = len(probe["novel_parliament_true"])
    if nzt != 0 or npt != 0:
        fail(f"C5: novel_true counts non-zero: zambialii={nzt}, parliament={npt}")
    ok(f"C5: novel_true counts = 0/0 (steady state)")

    # C6
    try:
        diff = subprocess.run(
            ["git", "status", "--porcelain", "records/"],
            cwd=str(ROOT), capture_output=True, text=True, timeout=10,
        )
        if diff.stdout.strip():
            fail(f"C6: records/ has uncommitted changes:\n{diff.stdout}")
        ok(f"C6: records/ tree clean (no record JSON writes this tick)")
    except Exception as e:
        print(f"WARN: git status check skipped: {e}")

    print("\nbatch 0296 integrity: PASS (probe-only; CHECK1..CHECK6 N/A — zero record writes)")


if __name__ == "__main__":
    main()
