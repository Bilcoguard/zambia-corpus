#!/usr/bin/env python3
"""Run a slice of batch_0258 picks. Usage: python3 batch_0258_one.py <start> <end>."""
import sys, os, json
sys.path.insert(0, os.path.dirname(__file__))
import batch_0258 as b

def main():
    start = int(sys.argv[1]); end = int(sys.argv[2])
    results=[]
    for pick in b.PICKS[start:end]:
        rec, status = b.ingest_one(pick)
        results.append({
            "yr": pick["yr"], "num": pick["num"], "title": pick["title"],
            "alpha": pick["alpha"], "status": status,
            "id": (rec["id"] if rec else None),
            "sections": (len(rec["sections"]) if rec else 0),
            "source_hash": (rec["source_hash"] if rec else None),
            "source_url": (rec["source_url"] if rec else None),
        })
        print(f"  {pick['yr']}/{pick['num']} -> {status}", flush=True)
    os.makedirs("_work", exist_ok=True)
    with open(f"_work/batch_0258_one_{start}_{end}.json","w") as f:
        json.dump(results,f,indent=2)
    print("DONE")

if __name__ == "__main__":
    main()
