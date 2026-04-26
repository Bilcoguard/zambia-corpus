#!/usr/bin/env python3
"""Integrity checks for batch 0280.

Per BRIEF tick step 6:
  CHECK1a: no duplicate IDs within the batch
  CHECK1b: each new record exists on disk
  CHECK2:  every amended_by reference resolves
  CHECK3:  every repealed_by reference resolves
  CHECK4:  every source_hash matches the on-disk raw file
  CHECK5:  required schema fields all present
  CHECK6:  every cited_authorities reference resolves
"""
import json, glob, hashlib, os, sys

REQUIRED_FIELDS = [
    "id","type","jurisdiction","title","citation","enacted_date",
    "commencement_date","in_force","amended_by","repealed_by",
    "cited_authorities","sections","source_url","source_hash",
    "fetched_at","parser_version",
]


def load_summary():
    with open("_work/batch_0280_summary.json") as f:
        return json.load(f)


def load_committed():
    s = load_summary()
    return [r for r in s if r["status"] == "ok"]


def all_corpus_ids():
    ids = set()
    for fname in glob.glob("records/**/*.json", recursive=True):
        try:
            with open(fname) as f:
                j = json.load(f)
            ids.add(j["id"])
        except Exception:
            pass
    return ids


def main():
    committed = load_committed()
    fail = []

    # CHECK1a
    ids = [r["id"] for r in committed]
    if len(ids) != len(set(ids)):
        fail.append(("CHECK1a", "duplicate IDs in batch", ids))
    else:
        print(f"CHECK1a: PASS ({len(ids)} unique batch IDs)")

    # CHECK1b
    missing = []
    for r in committed:
        rid = r["id"]; yr = r["yr"]
        path = f"records/acts/{yr}/{rid}.json"
        if not os.path.exists(path):
            missing.append(path)
    if missing:
        fail.append(("CHECK1b", "missing record files", missing))
    else:
        print(f"CHECK1b: PASS ({len(committed)} records on disk)")

    # Load full record JSONs for further checks
    recs = []
    for r in committed:
        path = f"records/acts/{r['yr']}/{r['id']}.json"
        with open(path) as f:
            recs.append(json.load(f))

    corpus_ids = all_corpus_ids()

    # CHECK2: amended_by refs resolve
    bad2 = []
    n2 = 0
    for rec in recs:
        for ref in (rec.get("amended_by") or []):
            n2 += 1
            if ref not in corpus_ids:
                bad2.append((rec["id"], ref))
    if bad2:
        fail.append(("CHECK2", "unresolved amended_by", bad2))
    else:
        print(f"CHECK2: PASS ({n2} amended_by refs all resolved)")

    # CHECK3: repealed_by refs resolve
    bad3 = []
    n3 = 0
    for rec in recs:
        ref = rec.get("repealed_by")
        if ref:
            n3 += 1
            if ref not in corpus_ids:
                bad3.append((rec["id"], ref))
    if bad3:
        fail.append(("CHECK3", "unresolved repealed_by", bad3))
    else:
        print(f"CHECK3: PASS ({n3} repealed_by refs all resolved)")

    # CHECK4: source_hash matches raw file
    bad4 = []
    for rec in recs:
        sh = rec.get("source_hash", "").replace("sha256:", "")
        # raw HTML path encodes yr / num
        m = rec["id"].split("-")
        # id: act-zm-<yr>-<num>-<slug...>
        yr = m[2]; num = int(m[3])
        raw_path = f"raw/zambialii/act/{yr}/{yr}-{num:03d}.html"
        if not os.path.exists(raw_path):
            bad4.append((rec["id"], "raw missing", raw_path))
            continue
        with open(raw_path, "rb") as f:
            disk_sha = hashlib.sha256(f.read()).hexdigest()
        if disk_sha != sh:
            bad4.append((rec["id"], disk_sha, sh))
    if bad4:
        fail.append(("CHECK4", "source_hash mismatch", bad4))
    else:
        print(f"CHECK4: PASS ({len(recs)} source_hash sha256 verified)")

    # CHECK5: required fields present
    bad5 = []
    for rec in recs:
        for k in REQUIRED_FIELDS:
            if k not in rec:
                bad5.append((rec["id"], k))
    if bad5:
        fail.append(("CHECK5", "missing fields", bad5))
    else:
        print(f"CHECK5: PASS ({len(REQUIRED_FIELDS)}x{len(recs)}={len(REQUIRED_FIELDS)*len(recs)} fields)")

    # CHECK6: cited_authorities refs resolve
    bad6 = []
    n6 = 0
    for rec in recs:
        for ref in (rec.get("cited_authorities") or []):
            n6 += 1
            if ref not in corpus_ids:
                bad6.append((rec["id"], ref))
    if bad6:
        fail.append(("CHECK6", "unresolved cited_authorities", bad6))
    else:
        print(f"CHECK6: PASS ({n6} cited_authorities refs all resolved)")

    if fail:
        print("INTEGRITY: FAIL")
        for tag, msg, det in fail:
            print(f"  {tag}: {msg}")
            for d in det[:5]:
                print(f"    {d}")
        sys.exit(1)
    print("INTEGRITY: PASS (all 6 checks)")


if __name__ == "__main__":
    main()
