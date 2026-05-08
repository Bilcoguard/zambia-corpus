#!/usr/bin/env python3
"""Batch 0539 — judgment-ingestion-worker dedicated tick.

Wraps b0506 fetcher; reads targets from _work/b0539/targets.json.
Continues ZMSC 2021 most-recent-first DESC sweep nums {27..20} per
b0536 next-tick recommendation. Heavy scan-PDF ratio observed in
b0536 (6 of 7 OK fetches were image-only PDFs deferred to OCR).
Renumbered from b0538 -> b0539 mid-tick because the main corpus
worker already claimed b0538 for Phase 8 nightly reverify
(2026-05-08T07:18Z) before this judgment-ingestion tick committed.
"""
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import batch_0506_zmsc_fetch as f

ROOT = HERE.parent
WORK = ROOT / "_work" / "b0539"
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
