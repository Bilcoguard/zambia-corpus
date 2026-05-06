#!/usr/bin/env python3
"""Batch 0529 — judgment-ingestion-worker dedicated tick (parse phase).

Thin wrapper around scripts/batch_0506_zmsc_parse.py. Re-points the work
directory and TARGETS_JSON at _work/b0529/, then re-runs the existing
parser_v0.3.2 pipeline. No parser changes.
"""
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

# Override WORK before importing main parser module so its module-level
# constants pick up the b0529 paths.
import batch_0506_zmsc_parse as p

ROOT = HERE.parent
WORK = ROOT / "_work" / "b0529"
WORK.mkdir(parents=True, exist_ok=True)
TARGETS = WORK / "targets.json"

# Patch parser module pointers
p.WORK = WORK
p.TARGETS_JSON = TARGETS


if __name__ == "__main__":
    p.main()
