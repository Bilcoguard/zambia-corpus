#!/usr/bin/env python3
"""Batch 0558 — judgment-ingestion-worker parse phase.

Thin wrapper around scripts/batch_0498_parse.py (parser_v0.3.2 baseline,
which has the build_record_v032() that already handles ZMCC court_full
and citation correctly). Re-points WORK / TARGETS_JSON to _work/b0558.

Priority (c) ZMCC NEW YEARS — parses 8 ZMCC 2020 records freshly fetched
by scripts/batch_0558_fetch.py.
"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import batch_0498_parse as p  # noqa: E402

ROOT = HERE.parent
WORK = ROOT / "_work" / "b0558"
WORK.mkdir(parents=True, exist_ok=True)
TARGETS = WORK / "targets.json"

p.WORK = WORK
p.TARGETS_JSON = TARGETS


if __name__ == "__main__":
    p.main()
