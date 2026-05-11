#!/usr/bin/env python3
"""Batch 0579 — judgment-ingestion-worker dedicated tick (parse phase).

Thin wrapper around scripts/batch_0506_zmsc_parse.py. Re-points the work
directory and TARGETS_JSON at _work/b0579/, then re-runs the existing
parser_v0.3.2 pipeline (Supreme Court of Zambia variant). No parser
changes.

Targets are the 8 newly-fetched ZMSC 2020 upper-band records (nums
{95, 100, 105, 110, 115, 120, 130, 150}).
"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import batch_0506_zmsc_parse as p  # noqa: E402

ROOT = HERE.parent
WORK = ROOT / "_work" / "b0579"
WORK.mkdir(parents=True, exist_ok=True)
TARGETS = WORK / "targets.json"

p.WORK = WORK
p.TARGETS_JSON = TARGETS


if __name__ == "__main__":
    p.main()
