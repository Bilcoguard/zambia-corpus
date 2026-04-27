#!/usr/bin/env python3
"""Batch 0290 verification — probe-only, no record writes.

Verifies that every (year, num) tuple enumerated from the two upstream
listing probes is present in records/acts/**/*.json. Standard
CHECK1..CHECK6 do not apply (no records were written).
"""
import os, glob, re

def main():
    existing = set()
    for p in glob.glob('records/acts/**/*.json', recursive=True):
        fn = os.path.basename(p)
        m = re.match(r'act-zm-(\d{4})-(\d+)-', fn)
        if m:
            existing.add((m.group(1), int(m.group(2))))

    zambia_recent = [
        ("2025", 5), ("2025", 6), ("2025", 7), ("2025", 8), ("2025", 9),
        ("2025", 22), ("2025", 23), ("2025", 24), ("2025", 25),
        ("2025", 26), ("2025", 27), ("2025", 28), ("2025", 29),
    ]
    parl = (
        [("2026", n) for n in range(1, 12)]
        + [("2025", n) for n in range(1, 30)]
        + [("2024", n) for n in range(12, 31)]
    )

    miss_z = [k for k in zambia_recent if k not in existing]
    miss_p = [k for k in parl if k not in existing]

    print(f"PROBE-DIFF zambialii recent: {len(zambia_recent)} probed, missing: {miss_z}")
    print(f"PROBE-DIFF parliament listed: {len(parl)} probed, missing: {miss_p}")

    if not miss_z and not miss_p:
        print("ALL PROBES PASS - no upstream items missing from corpus")
        return 0
    print("FAIL - upstream items missing from corpus")
    return 1

if __name__ == "__main__":
    raise SystemExit(main())
