#!/usr/bin/env python3
"""Integrity check for batch 0278 - 7 committed records (2000/11 deferred to gaps).

CHECK1a: batch unique IDs
CHECK1b: corpus presence on disk
CHECK2/3: amended_by / repealed_by reference resolution
CHECK4: source_hash sha256 verified against raw HTML on disk
CHECK5: required 16 fields present
CHECK6: cited_authorities reference resolution
"""
import json, hashlib, glob, sys, os

COMMITTED = [
    ("1992","16","supplementary-appropriation-1990-act"),
    ("1993","29","supplementary-appropriation-1991-act"),
    ("1994","40","supplementary-appropriation-1992-act"),
    # 1995/33 quarantined to _stale_locks/ for OCR section-spurious ('95' from "No. 33 of 1995" garble)
    ("1997","23","supplementary-appropriation-1994-act"),
    ("1997","29","supplementary-appropriation-1995-act"),
    ("2001","5","supplementary-appropriation-1998-act"),
]

REQUIRED = ["id","type","jurisdiction","title","citation","enacted_date",
            "commencement_date","in_force","amended_by","repealed_by",
            "cited_authorities","sections","source_url","source_hash",
            "fetched_at","parser_version"]

errors = []
ids_seen = set()

# Build corpus id index for cross-reference resolution
corpus_ids = set()
for p in glob.glob("records/**/*.json", recursive=True):
    try:
        with open(p) as f:
            d = json.load(f)
        if "id" in d:
            corpus_ids.add(d["id"])
    except Exception as e:
        pass

print(f"corpus index: {len(corpus_ids)} ids")

ok = 0
for yr, num, slug in COMMITTED:
    rid = f"act-zm-{yr}-{int(num):03d}-{slug}"
    path = f"records/acts/{yr}/{rid}.json"
    if not os.path.exists(path):
        errors.append(f"CHECK1b FAIL {rid}: file missing")
        continue
    with open(path) as f:
        rec = json.load(f)

    # CHECK1a unique within batch
    if rec["id"] in ids_seen:
        errors.append(f"CHECK1a FAIL {rid}: duplicate batch id")
    ids_seen.add(rec["id"])

    # CHECK5 required fields
    for fld in REQUIRED:
        if fld not in rec:
            errors.append(f"CHECK5 FAIL {rid}: missing {fld}")

    # CHECK2 amended_by resolution
    for ref in rec.get("amended_by", []) or []:
        if isinstance(ref, str) and ref not in corpus_ids:
            errors.append(f"CHECK2 FAIL {rid}: amended_by '{ref}' not in corpus")

    # CHECK3 repealed_by resolution
    rb = rec.get("repealed_by")
    if isinstance(rb, str) and rb not in corpus_ids:
        errors.append(f"CHECK3 FAIL {rid}: repealed_by '{rb}' not in corpus")

    # CHECK6 cited_authorities resolution
    for ref in rec.get("cited_authorities", []) or []:
        if isinstance(ref, str) and ref not in corpus_ids:
            errors.append(f"CHECK6 FAIL {rid}: cited '{ref}' not in corpus")

    # CHECK4 source_hash
    raw_html = f"raw/zambialii/act/{yr}/{yr}-{int(num):03d}.html"
    if not os.path.exists(raw_html):
        errors.append(f"CHECK4 FAIL {rid}: raw html missing at {raw_html}")
        continue
    with open(raw_html, "rb") as f:
        on_disk_sha = hashlib.sha256(f.read()).hexdigest()
    if rec["source_hash"] != f"sha256:{on_disk_sha}":
        errors.append(f"CHECK4 FAIL {rid}: stored {rec['source_hash']} vs on-disk sha256:{on_disk_sha}")

    ok += 1

print(f"records checked: {ok}/{len(COMMITTED)}")
if errors:
    print(f"FAIL: {len(errors)} errors")
    for e in errors:
        print(f"  {e}")
    sys.exit(1)
print("ALL INTEGRITY CHECKS PASS")
