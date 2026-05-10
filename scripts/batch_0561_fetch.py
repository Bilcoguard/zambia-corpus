#!/usr/bin/env python3
"""Batch 0561 — judgment-ingestion-worker fetch phase.

Priority (c) ZMCC NEW YEARS sweep — continuation of b0560.
b0560 sparse-sampled ZMCC 2019 at {1,5,10,15,20,25} → 4 OK + 2 404.
b0561 HEAD-probe (head_probe_zmcc_2019.py) confirmed:
  Upper sentinel: nums 26,27,28 OK; 29..35 all 404 (7 consecutive 404s)
  → ZMCC 2019 upper boundary = num 28.
  Low-slice internal gaps: nums 3,4,6 OK; 2,7,8,9 404.

Combined known-OK published nums for ZMCC 2019:
  {1, 3, 4, 5, 6, 20, 25, 26, 27, 28} (10 OK seen so far)
Internal-gap 404s: {2, 7, 8, 9, 10, 15} (six confirmed)
Unknown (un-probed): {11..14, 16..19, 21..24}

This batch GET-fetches 8 nums (MAX_BATCH_SIZE=8):
  {1, 3, 4, 5, 6, 20, 25, 26}.
The remaining known-OK {27, 28} plus the un-probed range will be
swept next tick.

Wrapper around scripts/batch_0506_zmsc_fetch.py:fetch_one — same
generic URL pattern works for both ZMSC and ZMCC.
"""
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import batch_0506_zmsc_fetch as f  # noqa: E402

ROOT = HERE.parent
WORK = ROOT / "_work" / "b0561"
WORK.mkdir(parents=True, exist_ok=True)


def main():
    targets_path = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else (WORK / "targets.json")
    targets = json.loads(targets_path.read_text())
    results = []
    for t in targets:
        r = f.fetch_one(t["court"], int(t["year"]), int(t["num"]))
        results.append(r)
        print(json.dumps({
            "court": t["court"], "year": t["year"], "num": t["num"],
            "status": r["status"], "code": r.get("code"),
            "date": r.get("date"), "html_bytes": r.get("html_bytes"),
            "pdf_bytes": r.get("pdf_bytes"),
        }))
    (WORK / "fetch_results.json").write_text(json.dumps(results, indent=2))
    ok = sum(1 for r in results if r["status"] in ("ok", "skip-already"))
    print(f"SUMMARY: ok/skip={ok}/{len(results)}")


if __name__ == "__main__":
    main()
