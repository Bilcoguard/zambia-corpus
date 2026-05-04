#!/usr/bin/env python3
"""Batch 0516 ZMSC parser — judgment-ingestion-worker tick.

Wraps b0506 parser: reads targets from _work/b0516/targets.json
(or argv[1]), writes records to records/judgments/zmsc/{year}/.
Outputs parse_summary.json under _work/b0516/.
"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
ROOT = HERE.parent

import batch_0506_zmsc_parse as p
WORK = ROOT / "_work" / "b0516"
WORK.mkdir(parents=True, exist_ok=True)

# patch
p.WORK = WORK
p.TARGETS_JSON = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else (WORK / "targets.json")

if __name__ == "__main__":
    p.main()
