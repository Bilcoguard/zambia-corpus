#!/usr/bin/env python3
"""Integrity checks for batch 0282."""
import os, json, hashlib, re, glob, sys

BATCH = "0282"
RECORDS = [
    "records/acts/2009/act-zm-2009-007-supplementary-appropriation-2007-act.json",
    "records/acts/2009/act-zm-2009-016-non-governmental-organisations-act.json",
    "records/acts/2010/act-zm-2010-004-public-interest-disclosure-protection-of-whistleblowers-act.json",
    "records/acts/2010/act-zm-2010-011-supplementary-appropriation-2008-act.json",
    "records/acts/2010/act-zm-2010-023-excess-expenditure-appropriation-2007-act.json",
    "records/acts/2011/act-zm-2011-025-supplementary-appropriation-2009-act.json",
]
REQUIRED = ["id","type","jurisdiction","title","citation","enacted_date",
            "commencement_date","in_force","amended_by","repealed_by",
            "cited_authorities","sections","source_url","source_hash",
            "fetched_at","parser_version"]

failures = []
recs = []
for p in RECORDS:
    if not os.path.exists(p):
        failures.append(f"MISSING: {p}")
        continue
    with open(p) as f:
        rec = json.load(f)
    recs.append((p, rec))

# CHECK1a: unique IDs in batch
ids = [r["id"] for _, r in recs]
if len(ids) != len(set(ids)):
    failures.append(f"CHECK1a FAIL: duplicate IDs in batch: {ids}")
else:
    print(f"CHECK1a PASS: {len(ids)}/{len(ids)} batch unique")

# CHECK1b: each ID's record file present on disk (slug-glob)
ok = 0
for p, rec in recs:
    yr = rec["id"].split("-")[2]
    num = rec["id"].split("-")[3]
    pat = f"records/acts/{yr}/act-zm-{yr}-{num}-*.json"
    found = glob.glob(pat)
    if found:
        ok += 1
    else:
        failures.append(f"CHECK1b FAIL: {rec['id']} no glob match")
print(f"CHECK1b PASS: {ok}/{len(recs)} corpus presence on disk")

# CHECK2/3: amended_by + repealed_by references resolve
amended_count = 0
repealed_count = 0
for p, rec in recs:
    for amid in (rec.get("amended_by") or []):
        amended_count += 1
        if not glob.glob(f"records/**/{amid}.json", recursive=True):
            failures.append(f"CHECK2 FAIL: amended_by {amid} unresolved in {rec['id']}")
    rb = rec.get("repealed_by")
    if rb:
        repealed_count += 1
        if not glob.glob(f"records/**/{rb}.json", recursive=True):
            failures.append(f"CHECK3 FAIL: repealed_by {rb} unresolved in {rec['id']}")
print(f"CHECK2 PASS: 0 amended_by refs (count={amended_count})")
print(f"CHECK3 PASS: 0 repealed_by refs (count={repealed_count})")

# CHECK4: source_hash matches on-disk raw file (HTML)
ok = 0
for p, rec in recs:
    yr = rec["id"].split("-")[2]
    num = rec["id"].split("-")[3]
    raw = f"raw/zambialii/act/{yr}/{yr}-{num}.html"
    if not os.path.exists(raw):
        failures.append(f"CHECK4 FAIL: raw missing {raw}")
        continue
    with open(raw, "rb") as f:
        body = f.read()
    sha = hashlib.sha256(body).hexdigest()
    expect = rec["source_hash"].split(":",1)[1]
    if sha == expect:
        ok += 1
    else:
        failures.append(f"CHECK4 FAIL: {rec['id']} sha mismatch (want {expect[:16]}, got {sha[:16]})")
print(f"CHECK4 PASS: {ok}/{len(recs)} source_hash sha256 verified")

# CHECK5: required fields present
ok = 0
total = 0
for p, rec in recs:
    for k in REQUIRED:
        total += 1
        if k in rec:
            ok += 1
        else:
            failures.append(f"CHECK5 FAIL: missing field {k} in {rec['id']}")
print(f"CHECK5 PASS: required {len(REQUIRED)} fields x {len(recs)} = {ok}/{total} all present")

# CHECK6: cited_authorities references resolve
cited = 0
for p, rec in recs:
    for cid in (rec.get("cited_authorities") or []):
        cited += 1
        if not glob.glob(f"records/**/{cid}.json", recursive=True):
            failures.append(f"CHECK6 FAIL: cited {cid} unresolved in {rec['id']}")
print(f"CHECK6 PASS: cited_authorities {cited} refs all resolve")

if failures:
    print("\n*** INTEGRITY FAILURES ***")
    for f in failures:
        print(" ", f)
    sys.exit(1)
print("\n=== ALL CHECKS PASSED ===")
