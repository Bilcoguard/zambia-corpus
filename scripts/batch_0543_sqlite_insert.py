#!/usr/bin/env python3
"""Batch 0543 — insert this tick's 3 ZMSC 2020 records into corpus.sqlite.

Idempotent: uses INSERT OR REPLACE so re-runs are safe.
Updates `records` and `judgments_meta`. records_fts left to host-side rebuild
(scripts/batch_0504_build_fts5.py) per b0517 precedent.

Reuses the b0531 TMPDIR-routed atomic copy pattern via b0540's import.
"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import batch_0531_sqlite_insert as ins  # noqa: E402

# Override the IDs to insert this tick's records.
ins.NEW_IDS = [
    "judgment-zm-2020-zmsc-51-richard-h-chama-213-other-v-national-pension-schem",
    "judgment-zm-2020-zmsc-60-matias-chitigwa-mugogo-v-the-people",
    "judgment-zm-2020-zmsc-65-jackson-kamanga-others-v-the-people",
]


if __name__ == "__main__":
    ins.main()
