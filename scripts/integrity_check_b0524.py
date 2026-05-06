#!/usr/bin/env python3
"""Integrity check for batch 0524 (Phase 8 nightly re-verification, first
batch). Read-only against records/ and reports/.

The Phase-8 batch did NOT write any records, so the usual ingestion
integrity battery (duplicate IDs, raw_sha256-on-disk, registry resolution,
etc.) does not apply. This script validates the Phase-8-specific
guarantees instead.
"""

from __future__ import annotations

import json
import os
import sys

WORKSPACE = "/sessions/lucid-upbeat-dirac/mnt/corpus"
SUMMARY = os.path.join(WORKSPACE, "reports", "batch-0524-reverify.json")
REPORT = os.path.join(WORKSPACE, "reports", "batch-0524-report.md")
GAPS = os.path.join(WORKSPACE, "gaps.md")

MAX_BATCH = 8


def main() -> int:
    failures: list[str] = []

    if not os.path.exists(SUMMARY):
        failures.append(f"missing summary JSON at {SUMMARY}")
        for f in failures:
            print("FAIL:", f)
        return 1

    with open(SUMMARY, "r", encoding="utf-8") as fh:
        d = json.load(fh)

    # Check 1: batch number
    if d.get("batch") != "0524":
        failures.append(f"summary batch is {d.get('batch')!r}, expected '0524'")

    # Check 2: phase tag
    if d.get("phase") != "phase_8_nightly_reverify":
        failures.append(f"summary phase is {d.get('phase')!r}, "
                        "expected 'phase_8_nightly_reverify'")

    # Check 3: sample size <= MAX_BATCH
    if d.get("sample_size", 0) > MAX_BATCH:
        failures.append(f"sample_size {d['sample_size']} > MAX_BATCH {MAX_BATCH}")

    # Check 4: sample_size matches results length
    if d.get("sample_size") != len(d.get("results", [])):
        failures.append("sample_size != len(results)")

    # Check 5: every result has a verdict
    for r in d.get("results", []):
        if r.get("verdict") not in ("match", "drift", "fetch_error"):
            failures.append(f"unknown verdict for {r.get('id')}: {r.get('verdict')!r}")

    # Check 6: counts add up
    counts = {"match": 0, "drift": 0, "fetch_error": 0}
    for r in d.get("results", []):
        v = r.get("verdict")
        if v in counts:
            counts[v] += 1
    if counts["match"] != d.get("match_count", -1):
        failures.append(
            f"match_count {d.get('match_count')} != observed {counts['match']}")
    if counts["drift"] != d.get("drift_count", -1):
        failures.append(
            f"drift_count {d.get('drift_count')} != observed {counts['drift']}")
    if counts["fetch_error"] != d.get("fetch_error_count", -1):
        failures.append(
            f"fetch_error_count {d.get('fetch_error_count')} != "
            f"observed {counts['fetch_error']}")

    # Check 7: each non-error result has matching hash semantics
    for r in d.get("results", []):
        if r.get("verdict") == "match":
            if r.get("stored_sha256") != r.get("fetched_sha256"):
                failures.append(
                    f"verdict 'match' but hashes differ for {r.get('id')}")
        elif r.get("verdict") == "drift":
            if r.get("stored_sha256") == r.get("fetched_sha256"):
                failures.append(
                    f"verdict 'drift' but hashes equal for {r.get('id')}")

    # Check 8: gaps.md contains the b0524 section
    with open(GAPS, "r", encoding="utf-8") as fh:
        gaps = fh.read()
    if "Phase 8 — Nightly re-verification, batch 0524" not in gaps:
        failures.append("gaps.md missing 'Phase 8 — Nightly re-verification, "
                        "batch 0524' section")
    # Each drift id should appear in gaps.md
    for r in d.get("results", []):
        if r.get("verdict") == "drift":
            if r.get("id") not in gaps:
                failures.append(f"gaps.md missing drift entry for {r.get('id')}")

    # Check 9: report exists
    if not os.path.exists(REPORT):
        failures.append(f"missing batch report at {REPORT}")

    # Check 10: results contain hex-only sha256 strings (where present)
    import re
    HEX = re.compile(r"^[0-9a-f]+$")
    for r in d.get("results", []):
        for k in ("stored_sha256", "fetched_sha256"):
            v = r.get(k)
            if v is not None and not HEX.match(v):
                failures.append(f"non-hex {k} for {r.get('id')}: {v!r}")

    if failures:
        print("INTEGRITY FAILED:")
        for f in failures:
            print("  -", f)
        return 1

    print(f"INTEGRITY PASS — 10/10 Phase-8 checks (batch=0524, "
          f"sample={d.get('sample_size')}, match={counts['match']}, "
          f"drift={counts['drift']}, fetch_error={counts['fetch_error']})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
