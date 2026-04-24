#!/usr/bin/env python3
"""
Batch 0196 RESUMER — picks up after the initial run of batch_0196.py
was killed by the sandbox 45s bash timeout after writing 3/7 records
(sis_family 2013/14; sis_tax 2011/33, 2024/18). The discovery fetches
were already logged to costs.log/provenance.log in that first run
(fetches 1-5), and the 3 ingest pairs accounted for fetches 6-11.

This resumer re-uses the HTML/PDF/parse functions from batch_0196.py
and processes the remaining targets in small slices that fit inside
the bash timeout. It also writes the final summary / state file.

Takes --slice start:end (0-indexed into REMAINING targets) and
--fetch-start (so costs.log/provenance.log fetch_n values continue
monotonically across chunks).
"""
import argparse, json, os, sys
from datetime import datetime, timezone

# Make sibling module importable.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import batch_0196 as b  # type: ignore

REMAINING = [
    (2014, 69, "sis_tax"),
    (2014, 68, "sis_tax"),
    (2008, 14, "sis_tax"),
    (2007, 19, "sis_tax"),
]

def utc_now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--slice", default=f"0:{len(REMAINING)}")
    ap.add_argument("--fetch-start", type=int, required=True,
                    help="Starting fetch_n for monotonic logging.")
    ap.add_argument("--final", action="store_true",
                    help="If set, also write the final summary + state file.")
    args = ap.parse_args()
    start_idx, end_idx = [int(x) for x in args.slice.split(":")]
    slice_targets = REMAINING[start_idx:end_idx]

    # Re-read HEAD so already-written records block collisions.
    import re
    head_ids = set()
    head_slots = set()
    for root, dirs, files in os.walk(os.path.join(b.WORKSPACE, "records", "sis")):
        for fn in files:
            if fn.endswith(".json"):
                rid = fn[:-5]
                head_ids.add(rid)
                m = re.match(r"si-zm-(\d{4})-(\d+)-", rid)
                if m:
                    head_slots.add((int(m.group(1)), int(m.group(2))))
    print(f"HEAD SI records: {len(head_ids)}; slots: {len(head_slots)}")

    import requests
    session = requests.Session()
    session.headers["User-Agent"] = b.USER_AGENT

    last_fetch_t = [None]
    fetch_counter = [args.fetch_start]

    results = []
    for (year, number, sub_phase) in slice_targets:
        print(f"\n=== SI {year}/{number:03d}  [{sub_phase}] ===")
        status, rec, meta = b.process_target(
            session, year, number, sub_phase, head_ids, head_slots,
            last_fetch_t, fetch_counter)
        print(f"  status: {status}")
        entry = {"year": year, "number": number, "sub_phase": sub_phase,
                 "status": status}
        if rec is not None:
            entry.update({
                "record_id": rec["id"],
                "sections": meta["sections"],
                "title": meta["title"],
                "pdf_url": meta["pdf_url"],
                "pdf_hash": meta["pdf_hash"],
                "pdf_bytes": meta["pdf_bytes"],
                "raw_pdf": meta["raw_pdf"],
                "record_path": meta["record_path"],
            })
            head_ids.add(rec["id"])
        else:
            with open("gaps.md", "a") as f:
                f.write(f"- [{utc_now()}] si/{year}/{number:03d} status={status} "
                        f"url=https://zambialii.org/akn/zm/act/si/{year}/{number} "
                        f"batch={b.BATCH_NUM} sub_phase={sub_phase}\n")
        results.append(entry)

    # Append partial state so next chunk can pick up + final summary can find it.
    os.makedirs("_work", exist_ok=True)
    partial_path = f"_work/batch_{b.BATCH_NUM}_resume_slice_{start_idx}_{end_idx}.json"
    with open(partial_path, "w") as f:
        json.dump({
            "slice": [start_idx, end_idx],
            "fetch_start": args.fetch_start,
            "fetch_end": fetch_counter[0],
            "results": results,
            "completed_at": utc_now(),
        }, f, indent=2)
    print(f"  wrote {partial_path}; fetch_counter now {fetch_counter[0]}")
    print(f"  ok={sum(1 for r in results if r['status']=='ok')}/{len(results)}")

if __name__ == "__main__":
    sys.exit(main() or 0)
