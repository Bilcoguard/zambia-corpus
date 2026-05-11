#!/usr/bin/env python3
"""Batch 0579 — judgment-ingestion-worker fetch phase.

Priority (c) ZMSC 2020 upper-band GET-fetch (post-95 cohort).
b0579 HEAD probe (head_probe_zmcc_2018.py) confirmed:
  ZMSC 2020 upper-band sweep {95,100,105,110,115,120,130,150,175}: 9 OK + zmsc/2020/200 = 404.
  → ZMSC 2020 upper boundary localised between 175 and 200; tick GET-fetches the lower 8 of the 9 newly-confirmed nums.

GET-fetch nums {95,100,105,110,115,120,130,150} (MAX_BATCH_SIZE=8) — newly confirmed published nums in upper band.
Wrapper around scripts/batch_0506_zmsc_fetch.py:fetch_one.
"""
import json, pathlib, sys
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import batch_0506_zmsc_fetch as f
ROOT = HERE.parent
WORK = ROOT / "_work" / "b0579"
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
