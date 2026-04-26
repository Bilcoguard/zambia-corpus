#!/usr/bin/env python3
"""Single-record runner for batch 0256. Usage: batch_0256_one.py <index>"""
import sys, json
sys.path.insert(0, "scripts")
import batch_0256 as bm

idx = int(sys.argv[1])
pick = bm.PICKS[idx]
rec, status = bm.ingest_one(pick)
out = {
    "idx": idx, "yr": pick["yr"], "num": pick["num"], "title": pick["title"],
    "alpha": pick["alpha"], "status": status,
    "id": (rec["id"] if rec else None),
    "sections": (len(rec["sections"]) if rec else 0),
    "source_hash": (rec["source_hash"] if rec else None),
    "source_url": (rec["source_url"] if rec else None),
}
import os
os.makedirs("_work", exist_ok=True)
with open(f"_work/batch_0256_one_{idx}.json","w") as f:
    json.dump(out, f, indent=2)
print(f"  {pick['yr']}/{pick['num']} -> {status}")
