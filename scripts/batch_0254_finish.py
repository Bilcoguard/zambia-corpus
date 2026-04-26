#!/usr/bin/env python3
"""Continuation of batch_0254.py — ingest the single remaining pick that
was preempted by a bash wall-clock timeout. Reuses ingest_one() from the
parent script so parser_version, hashing, and provenance writes stay
identical.
"""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from batch_0254 import ingest_one, BATCH_NUM

PICK = {
    "yr": "1981", "num": "3",
    "title": "Central Committee Act, 1981",
    "slug": "central-committee-act-1981",
    "sub_phase": "acts_in_force", "alpha": "C",
}


def main():
    rec, status = ingest_one(PICK)
    print(f"{PICK['yr']}/{PICK['num']} -> {status}")
    summary_path = f"_work/batch_{BATCH_NUM}_summary.json"
    if os.path.exists(summary_path):
        with open(summary_path) as f:
            results = json.load(f)
    else:
        results = []
    results.append({
        "yr": PICK["yr"], "num": PICK["num"], "title": PICK["title"],
        "status": status, "id": (rec["id"] if rec else None),
    })
    os.makedirs("_work", exist_ok=True)
    with open(summary_path, "w") as f:
        json.dump(results, f, indent=2)


if __name__ == "__main__":
    main()
