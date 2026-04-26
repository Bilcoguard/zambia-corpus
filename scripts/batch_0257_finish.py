#!/usr/bin/env python3
"""Batch 0257 FINISH - completes the remaining 3 picks after the main run was
killed mid-execution by the host bash timeout. Reuses ingest_one() from
batch_0257.py.

Remaining picks:
  I 1965/53 International Development Association Act, 1965
  I 1965/52 International Finance Corporation Act, 1965
  I 1964/60 Interpretation and General Provisions Act, 1964
"""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from batch_0257 import ingest_one, BATCH_NUM

REMAINING = [
    {"yr":"1965","num":"53","title":"International Development Association Act, 1965",
     "slug":"international-development-association-act-1965","sub_phase":"acts_in_force","alpha":"I"},
    {"yr":"1965","num":"52","title":"International Finance Corporation Act, 1965",
     "slug":"international-finance-corporation-act-1965","sub_phase":"acts_in_force","alpha":"I"},
    {"yr":"1964","num":"60","title":"Interpretation and General Provisions Act, 1964",
     "slug":"interpretation-and-general-provisions-act-1964","sub_phase":"acts_in_force","alpha":"I"},
]

def main():
    results = []
    for pick in REMAINING:
        rec, status = ingest_one(pick)
        results.append({
            "yr": pick["yr"], "num": pick["num"], "title": pick["title"],
            "alpha": pick["alpha"],
            "status": status, "id": (rec["id"] if rec else None),
            "sections": (len(rec["sections"]) if rec else 0),
            "source_hash": (rec["source_hash"] if rec else None),
            "source_url": (rec["source_url"] if rec else None),
        })
        print(f"  {pick['yr']}/{pick['num']} -> {status}")
    with open(f"_work/batch_{BATCH_NUM}_summary_finish.json", "w") as f:
        json.dump(results, f, indent=2)
    print("FINISH DONE")
    print(json.dumps([r["status"] for r in results]))

if __name__ == "__main__":
    main()
