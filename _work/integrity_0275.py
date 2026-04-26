#!/usr/bin/env python3
"""Integrity check for batch 0275 - mirrors batch_0274 integrity checks."""
import os, json, hashlib, sys, glob

BATCH_NUM = "0275"
PICKS = [
    ("1996","13","appropriation-act-1996"),
    ("1997","13","appropriation-act-1997"),
    ("1998","3","appropriation-act-1998"),
    ("1999","3","appropriation-act-1999"),
]
REQUIRED = ["id","type","jurisdiction","title","citation","enacted_date","commencement_date",
            "in_force","amended_by","repealed_by","cited_authorities","sections",
            "source_url","source_hash","fetched_at","parser_version"]

records = []
for yr,num,slug in PICKS:
    p = f"records/acts/{yr}/act-zm-{yr}-{int(num):03d}-{slug}.json"
    with open(p) as f:
        records.append((p,json.load(f)))

# CHECK1a - duplicate IDs in batch
ids = [r["id"] for _,r in records]
if len(set(ids)) != len(ids):
    print("FAIL CHECK1a - duplicates within batch:", ids)
    sys.exit(1)
print(f"PASS CHECK1a - {len(ids)} unique IDs in batch")

# CHECK1b - corpus presence
corpus_ids = set()
for fp in glob.glob("records/acts/**/*.json", recursive=True):
    try:
        with open(fp) as f:
            corpus_ids.add(json.load(f)["id"])
    except Exception:
        pass
missing = [i for i in ids if i not in corpus_ids]
if missing:
    print("FAIL CHECK1b - missing from corpus:", missing)
    sys.exit(1)
print(f"PASS CHECK1b - {len(ids)}/{len(ids)} present in corpus")

# CHECK2/3 - amended_by/repealed_by resolve
unresolved = []
for p,r in records:
    for ref in (r.get("amended_by") or []):
        if ref not in corpus_ids:
            unresolved.append(("amended_by",r["id"],ref))
    rb = r.get("repealed_by")
    if rb and rb not in corpus_ids:
        unresolved.append(("repealed_by",r["id"],rb))
if unresolved:
    print("FAIL CHECK2/3 - unresolved refs:", unresolved)
    sys.exit(1)
print("PASS CHECK2/3 - amended_by/repealed_by 0 refs to resolve")

# CHECK4 - source_hash matches raw HTML on disk
fail4 = []
for yr,num,slug in PICKS:
    raw = f"raw/zambialii/act/{yr}/{yr}-{int(num):03d}.html"
    with open(raw,"rb") as f:
        sha = "sha256:" + hashlib.sha256(f.read()).hexdigest()
    rec = next(r for _,r in records if r["id"] == f"act-zm-{yr}-{int(num):03d}-{slug}")
    if rec["source_hash"] != sha:
        fail4.append((rec["id"], rec["source_hash"], sha))
if fail4:
    print("FAIL CHECK4 - sha256 mismatch:", fail4)
    sys.exit(1)
print(f"PASS CHECK4 - sha256 verified {len(PICKS)}/{len(PICKS)} against raw HTML")

# CHECK5 - required fields
fail5 = []
for p,r in records:
    for k in REQUIRED:
        if k not in r:
            fail5.append((r["id"],k))
if fail5:
    print("FAIL CHECK5 - missing fields:", fail5)
    sys.exit(1)
print(f"PASS CHECK5 - 16x{len(records)}={16*len(records)} required fields present")

# CHECK6 - cited_authorities resolve
fail6 = []
for p,r in records:
    for c in (r.get("cited_authorities") or []):
        cid = c.get("id") if isinstance(c, dict) else c
        if cid and cid not in corpus_ids:
            fail6.append((r["id"], cid))
if fail6:
    print("FAIL CHECK6 - unresolved cited_authorities:", fail6)
    sys.exit(1)
print("PASS CHECK6 - cited_authorities 0 refs")

print("ALL CHECKS PASS")
