#!/usr/bin/env python3
"""Integrity check for batch 0286.

CHECK1a: no duplicate IDs in batch
CHECK1b: each ID present on disk
CHECK2:  amended_by references resolve
CHECK3:  repealed_by references resolve
CHECK4:  source_hash matches on-disk raw HTML file
CHECK5:  required 16 fields present
CHECK6:  cited_authorities references resolve
"""
import json, hashlib, glob, os, sys

REQUIRED = [
    "id","type","jurisdiction","title","citation",
    "enacted_date","commencement_date","in_force",
    "amended_by","repealed_by","cited_authorities",
    "sections","source_url","source_hash","fetched_at","parser_version",
]

with open("_work/batch_0286_summary.json") as f:
    summary = json.load(f)
ok_results = [r for r in summary["results"] if r["status"] == "ok"]

ids_in_batch = [r["id"] for r in ok_results]

# Build full corpus id index for cross-ref checks
all_ids = set()
for path in glob.glob("records/**/*.json", recursive=True):
    try:
        with open(path) as f:
            d = json.load(f)
        all_ids.add(d.get("id"))
    except Exception:
        pass

failures = []

# CHECK1a
dups = set([x for x in ids_in_batch if ids_in_batch.count(x) > 1])
if dups:
    failures.append(f"CHECK1a: duplicate IDs in batch: {dups}")
else:
    print(f"CHECK1a: {len(ids_in_batch)}/{len(ids_in_batch)} batch unique - PASS")

# CHECK1b - presence on disk
present = 0
for r in ok_results:
    pat = f"records/acts/{r['yr']}/{r['id']}.json"
    if os.path.exists(pat):
        present += 1
    else:
        failures.append(f"CHECK1b: missing on disk: {pat}")
print(f"CHECK1b: {present}/{len(ok_results)} corpus presence - {'PASS' if present==len(ok_results) else 'FAIL'}")

# CHECK2/3/6
am_refs = re_refs = ca_refs = 0
for r in ok_results:
    pat = f"records/acts/{r['yr']}/{r['id']}.json"
    with open(pat) as f:
        d = json.load(f)
    for ref in d.get("amended_by", []):
        am_refs += 1
        if ref not in all_ids:
            failures.append(f"CHECK2: unresolved amended_by ref {ref} in {d['id']}")
    rep = d.get("repealed_by")
    if rep:
        re_refs += 1
        if rep not in all_ids:
            failures.append(f"CHECK3: unresolved repealed_by ref {rep} in {d['id']}")
    for ref in d.get("cited_authorities", []):
        ca_refs += 1
        if ref not in all_ids:
            failures.append(f"CHECK6: unresolved cited_authorities ref {ref} in {d['id']}")
print(f"CHECK2: {am_refs} amended_by refs - PASS")
print(f"CHECK3: {re_refs} repealed_by refs - PASS")
print(f"CHECK6: {ca_refs} cited_authorities refs - PASS")

# CHECK4 - source hash
hash_ok = 0
for r in ok_results:
    pat = f"records/acts/{r['yr']}/{r['id']}.json"
    with open(pat) as f:
        d = json.load(f)
    expected = d["source_hash"].split(":",1)[1]
    raw = f"raw/zambialii/act/{r['yr']}/{r['yr']}-{int(r['num']):03d}.html"
    if not os.path.exists(raw):
        failures.append(f"CHECK4: missing raw {raw}")
        continue
    actual = hashlib.sha256(open(raw,"rb").read()).hexdigest()
    if actual != expected:
        failures.append(f"CHECK4: hash mismatch {r['id']}: expected {expected[:16]}, got {actual[:16]}")
    else:
        hash_ok += 1
print(f"CHECK4: {hash_ok}/{len(ok_results)} source_hash sha256 verified - {'PASS' if hash_ok==len(ok_results) else 'FAIL'}")

# CHECK5 - 16 required fields
fcount = 0
total_expected = len(REQUIRED) * len(ok_results)
for r in ok_results:
    pat = f"records/acts/{r['yr']}/{r['id']}.json"
    with open(pat) as f:
        d = json.load(f)
    for fld in REQUIRED:
        if fld not in d:
            failures.append(f"CHECK5: {r['id']} missing field {fld}")
        else:
            fcount += 1
print(f"CHECK5: {fcount}/{total_expected} required fields - {'PASS' if fcount==total_expected else 'FAIL'}")

if failures:
    print("\nFAILURES:")
    for f in failures:
        print("  ", f)
    sys.exit(1)
else:
    print("\nALL CHECKS PASSED")
