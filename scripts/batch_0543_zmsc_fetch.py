#!/usr/bin/env python3
"""Batch 0543 — judgment-ingestion-worker dedicated tick (fetch phase).

ZMSC 2020 upper-boundary follow-up. b0543 first ran an inline HEAD-only
probe of nums {51, 55, 60, 65, 70, 75, 80, 90} (8 fetches; 7 OK, 1 404
at num=80) — boundary therefore extends to ≥90 with at least one
internal 404. This script GET-fetches the 7 confirmed-OK nums to
ingest. Wraps b0506 fetcher; reads targets from _work/b0543/targets.json.

No parser, fetcher, or wrapper logic changes — same configuration-only
pattern as b0539/b0540/b0541.
"""
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import batch_0506_zmsc_fetch as f  # noqa: E402

ROOT = HERE.parent
WORK = ROOT / "_work" / "b0543"
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
