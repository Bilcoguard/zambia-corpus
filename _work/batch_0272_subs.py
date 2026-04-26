#!/usr/bin/env python3
"""Batch 0272 substitutes after 2000/8 and 2000/16 returned no_sections (scanned PDFs).
Substituting with the 2 carryover residuals: E 2004/4 and N 2005/17.
Reuses ingest_one() from scripts/batch_0272.py."""
import os, sys, json
sys.path.insert(0, "scripts")
from batch_0272 import ingest_one, BATCH_NUM

SUBS = [
    {"yr":"2004","num":"4","title":"Excess Expenditure Appropriation (1999) Act, 2004",
     "slug":"excess-expenditure-appropriation-1999-act-2004","sub_phase":"acts_in_force","alpha":"E"},
    {"yr":"2005","num":"17","title":"National Health Services (Repeal) Act, 2005",
     "slug":"national-health-services-repeal-act-2005","sub_phase":"acts_in_force","alpha":"N"},
]

results = []
for idx, pick in enumerate(SUBS):
    rec, status = ingest_one(pick)
    results.append({
        "idx": idx,
        "yr": pick["yr"], "num": pick["num"], "title": pick["title"],
        "alpha": pick["alpha"],
        "status": status, "id": (rec["id"] if rec else None),
        "sections": (len(rec["sections"]) if rec else 0),
        "source_hash": (rec["source_hash"] if rec else None),
        "source_url": (rec["source_url"] if rec else None),
    })
    print(f"  sub[{idx}] {pick['yr']}/{pick['num']} -> {status}", flush=True)

os.makedirs("_work", exist_ok=True)
with open(f"_work/batch_{BATCH_NUM}_subs.json", "w") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)
