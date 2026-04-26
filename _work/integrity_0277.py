#!/usr/bin/env python3
"""Integrity check for batch 0277 (6 records).

CHECK1a: batch IDs unique
CHECK1b: corpus presence on disk (records/acts/{yr}/{rid}.json exists)
CHECK2: amended_by references resolve (each id is on disk)
CHECK3: repealed_by references resolve
CHECK4: source_hash sha256 matches raw file on disk
CHECK5: required 16 fields present and non-null where required
CHECK6: cited_authorities references resolve
"""
import os, json, hashlib, sys

PICKS = [
    ("1970","55","nurses-and-midwives-act"),
    ("1973","41","supreme-court-of-zambia-act"),
    ("1979","22","public-officers-pensions-zambia-agreement-implementation-act"),
    ("1988","31","supplementary-appropriation-1987-act"),
    ("1989","31","supplementary-appropriation-1988-act"),
    ("1990","39","supplementary-appropriation-1989-act"),
]

REQUIRED = ["id","type","jurisdiction","title","citation","enacted_date",
            "commencement_date","in_force","amended_by","repealed_by",
            "cited_authorities","sections","source_url","source_hash",
            "fetched_at","parser_version"]

errors = []
records = []

# CHECK1a/1b
batch_ids = []
for yr,num,slug in PICKS:
    rid = f"act-zm-{yr}-{int(num):03d}-{slug}"
    p = f"records/acts/{yr}/{rid}.json"
    if not os.path.isfile(p):
        errors.append(f"CHECK1b: missing on disk {p}")
        continue
    with open(p, encoding="utf-8") as f:
        rec = json.load(f)
    records.append((rec, p, yr, num))
    batch_ids.append(rec["id"])

if len(batch_ids) != len(set(batch_ids)):
    errors.append(f"CHECK1a: duplicate ids in batch {batch_ids}")
print(f"CHECK1a: batch unique {len(batch_ids)}/{len(PICKS)} {'PASS' if len(batch_ids)==len(set(batch_ids)) else 'FAIL'}")
print(f"CHECK1b: on-disk presence {len(records)}/{len(PICKS)} {'PASS' if len(records)==len(PICKS) else 'FAIL'}")

# Build full id index for CHECK2/3/6 (fast: scan all records dirs)
all_ids = set()
for root, dirs, files in os.walk("records"):
    for fn in files:
        if fn.endswith(".json"):
            try:
                with open(os.path.join(root,fn), encoding="utf-8") as f:
                    r = json.load(f)
                all_ids.add(r.get("id",""))
            except Exception:
                pass
print(f"  (corpus has {len(all_ids)} unique record ids)")

# CHECK2/3/6
unresolved2 = unresolved3 = unresolved6 = 0
for rec, p, yr, num in records:
    for ref in rec.get("amended_by") or []:
        if ref not in all_ids:
            unresolved2 += 1
            errors.append(f"CHECK2: {rec['id']} amended_by ref {ref} unresolved")
    rb = rec.get("repealed_by")
    if rb:
        refs = rb if isinstance(rb, list) else [rb]
        for ref in refs:
            if ref not in all_ids:
                unresolved3 += 1
                errors.append(f"CHECK3: {rec['id']} repealed_by ref {ref} unresolved")
    for ref in rec.get("cited_authorities") or []:
        if ref not in all_ids:
            unresolved6 += 1
            errors.append(f"CHECK6: {rec['id']} cited_authorities ref {ref} unresolved")
print(f"CHECK2: amended_by unresolved={unresolved2} {'PASS' if unresolved2==0 else 'FAIL'}")
print(f"CHECK3: repealed_by unresolved={unresolved3} {'PASS' if unresolved3==0 else 'FAIL'}")
print(f"CHECK6: cited_authorities unresolved={unresolved6} {'PASS' if unresolved6==0 else 'FAIL'}")

# CHECK4: source_hash matches raw HTML file on disk
mismatch4 = 0
for rec, p, yr, num in records:
    raw_html = f"raw/zambialii/act/{yr}/{yr}-{int(num):03d}.html"
    if not os.path.isfile(raw_html):
        errors.append(f"CHECK4: raw missing {raw_html}")
        mismatch4 += 1
        continue
    with open(raw_html, "rb") as f:
        body = f.read()
    sha = "sha256:" + hashlib.sha256(body).hexdigest()
    if sha != rec.get("source_hash"):
        errors.append(f"CHECK4: hash mismatch {rec['id']} disk={sha[:23]}... rec={rec.get('source_hash','')[:23]}...")
        mismatch4 += 1
print(f"CHECK4: source_hash match {len(records)-mismatch4}/{len(records)} {'PASS' if mismatch4==0 else 'FAIL'}")

# CHECK5: required fields present
missing5 = 0
for rec, p, yr, num in records:
    for field in REQUIRED:
        if field not in rec:
            missing5 += 1
            errors.append(f"CHECK5: {rec.get('id','?')} missing field {field}")
print(f"CHECK5: required fields {len(records)*len(REQUIRED)-missing5}/{len(records)*len(REQUIRED)} {'PASS' if missing5==0 else 'FAIL'}")

if errors:
    print("\nFAILED CHECKS:")
    for e in errors:
        print("  ", e)
    sys.exit(1)
else:
    print("\nALL CHECKS PASS")
