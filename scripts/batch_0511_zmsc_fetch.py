#!/usr/bin/env python3
"""Batch 0511 — judgment-ingestion-worker dedicated tick.

Reuses the b0506 fetch implementation. Accepts targets file as argv[1].
"""
import json
import pathlib
import sys
import time

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import batch_0506_zmsc_fetch as f

ROOT = HERE.parent
WORK = ROOT / "_work" / "b0511"
WORK.mkdir(parents=True, exist_ok=True)

def main():
    if len(sys.argv) > 1:
        targets_path = pathlib.Path(sys.argv[1])
    else:
        targets_path = WORK / "targets.json"
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
        }), flush=True)
    out = WORK / (targets_path.stem.replace("targets", "fetch_results") + ".json")
    out.write_text(json.dumps(results, indent=2))
    ok = sum(1 for r in results if r["status"] in ("ok", "skip-already"))
    print(f"SUMMARY: ok/skip={ok}/{len(results)}")

if __name__ == "__main__":
    main()
