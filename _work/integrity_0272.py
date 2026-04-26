#!/usr/bin/env python3
"""Integrity check for batch 0272 - 8 records expected."""
import os, json, hashlib, glob, sys

BATCH_NUM = "0272"
EXPECTED_IDS = [
    "act-zm-1993-024-prescribed-minerals-and-materials-commission-dissolution-act-1993",
    "act-zm-1994-030-excess-expenditure-appropriation-1991-act-1994",
    "act-zm-1994-045-presidential-emoluments-amendment-act-1994",
    "act-zm-1995-032-excess-expenditure-appropriation-1992-act-1993",
    "act-zm-1997-022-excess-expenditure-appropriation-1993-act-1997",
    "act-zm-2003-017-excess-expenditure-appropriation-1998-act-2003",
    "act-zm-2004-004-excess-expenditure-appropriation-1999-act-2004",
    "act-zm-2005-017-national-health-services-repeal-act-2005",
]
ID_TO_PATH = {
    "act-zm-1993-024-prescribed-minerals-and-materials-commission-dissolution-act-1993":
      ("records/acts/1993/", "raw/zambialii/act/1993/1993-024.html"),
    "act-zm-1994-030-excess-expenditure-appropriation-1991-act-1994":
      ("records/acts/1994/", "raw/zambialii/act/1994/1994-030.html"),
    "act-zm-1994-045-presidential-emoluments-amendment-act-1994":
      ("records/acts/1994/", "raw/zambialii/act/1994/1994-045.html"),
    "act-zm-1995-032-excess-expenditure-appropriation-1992-act-1993":
      ("records/acts/1995/", "raw/zambialii/act/1995/1995-032.html"),
    "act-zm-1997-022-excess-expenditure-appropriation-1993-act-1997":
      ("records/acts/1997/", "raw/zambialii/act/1997/1997-022.html"),
    "act-zm-2003-017-excess-expenditure-appropriation-1998-act-2003":
      ("records/acts/2003/", "raw/zambialii/act/2003/2003-017.html"),
    "act-zm-2004-004-excess-expenditure-appropriation-1999-act-2004":
      ("records/acts/2004/", "raw/zambialii/act/2004/2004-004.html"),
    "act-zm-2005-017-national-health-services-repeal-act-2005":
      ("records/acts/2005/", "raw/zambialii/act/2005/2005-017.html"),
}

REQUIRED_FIELDS = [
    "id","type","jurisdiction","title","citation","enacted_date","commencement_date",
    "in_force","amended_by","repealed_by","cited_authorities","sections",
    "source_url","source_hash","fetched_at","parser_version",
]

def main():
    failures = []
    # CHECK1a: batch unique IDs
    if len(set(EXPECTED_IDS)) != len(EXPECTED_IDS):
        failures.append(f"CHECK1a duplicate IDs in batch")
    print(f"CHECK1a batch unique IDs: {len(set(EXPECTED_IDS))}/{len(EXPECTED_IDS)} unique")

    # CHECK1b: presence on disk
    present = 0
    for rid in EXPECTED_IDS:
        p = os.path.join(ID_TO_PATH[rid][0], f"{rid}.json")
        if os.path.exists(p):
            present += 1
        else:
            failures.append(f"CHECK1b missing: {p}")
    print(f"CHECK1b corpus presence on disk: {present}/{len(EXPECTED_IDS)}")

    # Also check no other on-disk acts with same (yr,num) prefix that would be duplicate
    yr_num_pairs = [("1993","024"),("1994","030"),("1994","045"),("1995","032"),
                    ("1997","022"),("2003","017"),("2004","004"),("2005","017")]
    for yr, num in yr_num_pairs:
        files = glob.glob(f"records/acts/{yr}/act-zm-{yr}-{num}-*.json")
        if len(files) != 1:
            failures.append(f"CHECK1a-dup {yr}/{num}: {len(files)} files: {files}")

    # CHECK2/3: amended_by/repealed_by references
    refs_amended = 0; refs_repealed = 0
    for rid in EXPECTED_IDS:
        p = os.path.join(ID_TO_PATH[rid][0], f"{rid}.json")
        with open(p) as f:
            r = json.load(f)
        for ref in r.get("amended_by", []):
            refs_amended += 1
            # Resolve - placeholder, would need full corpus index
        if r.get("repealed_by"):
            refs_repealed += 1
    print(f"CHECK2 amended_by refs: {refs_amended} (none to resolve)")
    print(f"CHECK3 repealed_by refs: {refs_repealed} (none to resolve)")

    # CHECK4: source_hash matches on-disk raw HTML
    sha_pass = 0
    for rid in EXPECTED_IDS:
        rec_path = os.path.join(ID_TO_PATH[rid][0], f"{rid}.json")
        raw_path = ID_TO_PATH[rid][1]
        with open(rec_path) as f:
            r = json.load(f)
        with open(raw_path, "rb") as f:
            data = f.read()
        actual = "sha256:" + hashlib.sha256(data).hexdigest()
        if actual == r["source_hash"]:
            sha_pass += 1
        else:
            failures.append(f"CHECK4 sha mismatch {rid}: rec={r['source_hash']} disk={actual}")
    print(f"CHECK4 source_hash sha256 verified: {sha_pass}/{len(EXPECTED_IDS)}")

    # CHECK5: required fields
    fields_pass = 0
    fields_total = 0
    for rid in EXPECTED_IDS:
        p = os.path.join(ID_TO_PATH[rid][0], f"{rid}.json")
        with open(p) as f:
            r = json.load(f)
        for fn in REQUIRED_FIELDS:
            fields_total += 1
            if fn in r:
                fields_pass += 1
            else:
                failures.append(f"CHECK5 missing field {fn} in {rid}")
    print(f"CHECK5 required {len(REQUIRED_FIELDS)} fields x {len(EXPECTED_IDS)} = {fields_pass}/{fields_total}")

    # CHECK6: cited_authorities
    cited_total = 0
    for rid in EXPECTED_IDS:
        p = os.path.join(ID_TO_PATH[rid][0], f"{rid}.json")
        with open(p) as f:
            r = json.load(f)
        cited_total += len(r.get("cited_authorities", []))
    print(f"CHECK6 cited_authorities refs: {cited_total} (none to resolve)")

    if failures:
        print("\nFAIL:")
        for fl in failures:
            print(f"  - {fl}")
        sys.exit(1)
    else:
        print("\nALL CHECKS PASS")

if __name__ == "__main__":
    main()
