#!/usr/bin/env python3
"""Batch 0558 — judgment-ingestion-worker fetch phase.

Priority (c) ZMCC NEW YEARS sweep — older years not yet covered.
b0558 HEAD probe (zmcc/2020/{1,5,10,15,20,25}) returned 4 OK + 2 404,
confirming ZambiaLII publishes ZMCC 2020. This batch GET-fetches
ZMCC 2020 nums {1..8} (MAX_BATCH_SIZE=8). 404s are recorded as
http-error and skipped by the parser via raw_bytes_not_on_disk.

Wrapper around scripts/batch_0506_zmsc_fetch.py:fetch_one — same
generic URL pattern works for both ZMSC and ZMCC. The slug regex
in fetch_one strips "[YYYY] ZMSC NN" but not "[YYYY] ZMCC NN", so we
post-process the slug after fetch to strip ZMCC if present.
"""
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import batch_0506_zmsc_fetch as f  # noqa: E402

ROOT = HERE.parent
WORK = ROOT / "_work" / "b0558"
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
