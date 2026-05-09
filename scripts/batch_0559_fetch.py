#!/usr/bin/env python3
"""Batch 0559 — judgment-ingestion-worker fetch phase.

Priority (c) ZMCC NEW YEARS sweep — continuation of b0558 (which
fetched ZMCC 2020 nums {1..8}). b0559 head-probe confirmed
nums {16, 17, 18} OK and num 19 = 404, so ZMCC 2020 upper boundary
is num 18. This batch GET-fetches ZMCC 2020 nums {9..16}
(MAX_BATCH_SIZE=8). Remaining nums {17, 18} carried to next tick.

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
WORK = ROOT / "_work" / "b0559"
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
