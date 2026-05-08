#!/usr/bin/env python3
"""Integrity check b0539 — judgment-ingestion-worker tick.

This tick wrote 0 new records (all 8 ZMSC 2021 nums {27..20} candidates
deferred under `pdf_extraction_empty_likely_scanned`). Therefore the
seven required per-record checks from SKILL.md are trivially N/A. This
check still validates two corpus-wide invariants that are independent
of the tick:

  1. No duplicate IDs across records/judgments/**/*.json
  2. The 8 deferred raw HTML+PDF files are on disk (one matching pair
     each in raw/zambialii/judgments/zmsc/2021/).
"""
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

DEFERRED = [
    ("zmsc", 2021, 27),
    ("zmsc", 2021, 26),
    ("zmsc", 2021, 25),
    ("zmsc", 2021, 24),
    ("zmsc", 2021, 23),
    ("zmsc", 2021, 22),
    ("zmsc", 2021, 21),
    ("zmsc", 2021, 20),
]

passed = 0
failed = 0
errors = []


def check(cond, msg):
    global passed, failed
    if cond:
        passed += 1
    else:
        failed += 1
        errors.append(msg)


def main():
    # 1. Corpus-wide duplicate-ID check
    all_records_dir = ROOT / "records" / "judgments"
    all_ids = []
    for p in all_records_dir.rglob("*.json"):
        try:
            r = json.loads(p.read_text())
            all_ids.append(r["id"])
        except Exception:
            pass
    check(
        len(all_ids) == len(set(all_ids)),
        f"no duplicate ids in corpus (n={len(all_ids)}, uniq={len(set(all_ids))})",
    )

    # 2. Deferred raw files on disk (HTML + PDF pair) for each candidate
    raw_year = ROOT / "raw" / "zambialii" / "judgments" / "zmsc" / "2021"
    for (court, year, num) in DEFERRED:
        htmls = list(raw_year.glob(f"judgment-zm-{year}-{court}-{num:02d}-*.html"))
        pdfs = list(raw_year.glob(f"judgment-zm-{year}-{court}-{num:02d}-*.pdf"))
        check(len(htmls) == 1, f"{court}/{year}/{num}: exactly one raw HTML on disk (got {len(htmls)})")
        check(len(pdfs) == 1, f"{court}/{year}/{num}: exactly one raw PDF on disk (got {len(pdfs)})")

    print(f"Integrity check b0539: {passed} passed / {failed} failed")
    if errors:
        for e in errors:
            print(f"  FAIL: {e}")
        sys.exit(1)
    print(f"Total records on disk: {len(all_ids)} unique IDs")


if __name__ == "__main__":
    main()
