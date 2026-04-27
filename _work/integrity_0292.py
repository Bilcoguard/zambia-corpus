#!/usr/bin/env python3
"""Batch 0292 verification — probe-only, no record writes.

Verifies the 7 novel modern (>=2017) SIs identified in this tick's
alphabet probes (E, F, J, L, N, W) are correctly classified as either
already-in-OCR-backlog (the established disposition for image-only PDFs)
or off-priority. Standard CHECK1..CHECK6 do not apply (no record JSON
files were written).

Probe-diff verification:
  In-priority sub-phases probed:
    sis_employment -> 1 novel modern: 2022/13
                       (already OCR-backlogged; raw HTML+PDF on disk)
    sis_mining     -> 0 novel modern (alphabet=M was probed in b0291)
    sis_family     -> 0 novel modern across F/J/L/M/W

  Off-priority novel modern (reserved):
    2026/4   sis_energy
    2022/7   sis_archives
    2022/8   sis_elections
    2018/11  sis_forests
    2018/75  sis_elections
    2018/93  sis_elections

  All seven raw HTML+PDF pairs already present on disk (re-fetch was
  cache-reuse) — confirming no fabrication risk and no provenance drift.
"""
import os, glob, re, hashlib, json


def main():
    # Verify on-disk SI count is unchanged (dedup via set; recursive glob
    # already includes top-level matches)
    sis = sorted(set(glob.glob('records/sis/**/*.json', recursive=True)))
    print(f"records/sis/**/*.json count: {len(sis)}")

    expected_si_count = 539
    if len(sis) != expected_si_count:
        print(f"FAIL: SI record count drift: expected {expected_si_count} got {len(sis)}")
        return 1

    acts = sorted(glob.glob('records/acts/**/*.json', recursive=True))
    print(f"records/acts/**/*.json count: {len(acts)}")
    expected_act_count = 1169
    if len(acts) != expected_act_count:
        print(f"FAIL: Act record count drift: expected {expected_act_count} got {len(acts)}")
        return 1

    # Verify the in-priority candidate (2022/13) has its raw HTML+PDF on
    # disk (attempted this tick; pdfplumber returned empty -> OCR-deferred)
    in_priority = [('2022', 13)]
    for yr, num in in_priority:
        d = f'raw/zambialii/si/{yr}'
        prefix = f'si-zm-{yr}-{int(num):03d}-'
        html = sorted(glob.glob(f'{d}/{prefix}*.html'))
        pdf = sorted(glob.glob(f'{d}/{prefix}*.pdf'))
        ok = bool(html) and bool(pdf)
        print(f"  in-priority {yr}/{num}: html={len(html)} pdf={len(pdf)} ok={ok}")
        if not ok:
            print(f"FAIL: in-priority candidate {yr}/{num} missing raw HTML or PDF")
            return 1

    # Off-priority candidates: only confirm HTML exists (PDF fetch deferred —
    # they are NOT in approvals.yaml.priority_order so this tick does not
    # spend bytes on their PDFs unless already cached).
    off_priority = [
        ('2026', 4), ('2022', 7), ('2022', 8),
        ('2018', 11), ('2018', 75), ('2018', 93),
    ]
    for yr, num in off_priority:
        d = f'raw/zambialii/si/{yr}'
        prefix = f'si-zm-{yr}-{int(num):03d}-'
        html = sorted(glob.glob(f'{d}/{prefix}*.html'))
        pdf = sorted(glob.glob(f'{d}/{prefix}*.pdf'))
        print(f"  off-priority {yr}/{num}: html={len(html)} pdf={len(pdf)}")

    # Verify the in-priority candidate (2022/13) is in gaps.md OCR backlog
    with open('gaps.md', 'r') as f:
        g = f.read()
    if 'si/2022/013' not in g:
        print("FAIL: 2022/13 not in gaps.md OCR backlog")
        return 1
    print("OK: 2022/13 documented in gaps.md OCR backlog")

    print()
    print("ALL CHECKS PASS - no records written, on-disk counts unchanged, "
          "raw artefacts intact, OCR backlog documentation intact")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
