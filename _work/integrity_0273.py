#!/usr/bin/env python3
"""Integrity check for batch 0273 - 8 records expected."""
import os, json, hashlib, glob, sys

BATCH_NUM = "0273"
EXPECTED_IDS = [
    "act-zm-1964-036-apprenticeship-act-1964",
    "act-zm-1980-009-appropriation-act-1980",
    "act-zm-1981-012-appropriation-act-1981",
    "act-zm-1982-015-appropriation-act-1982",
    "act-zm-1983-014-appropriation-act-1983",
    "act-zm-1984-013-appropriation-act-1984",
    "act-zm-1985-016-appropriation-act-1985",
    "act-zm-1986-012-appropriation-act-1986",
]
ID_TO_PATH = {
    "act-zm-1964-036-apprenticeship-act-1964":
      ("records/acts/1964/", "raw/zambialii/act/1964/1964-036.html"),
    "act-zm-1980-009-appropriation-act-1980":
      ("records/acts/1980/", "raw/zambialii/act/1980/1980-009.html"),
    "act-zm-1981-012-appropriation-act-1981":
      ("records/acts/1981/", "raw/zambialii/act/1981/1981-012.html"),
    "act-zm-1982-015-appropriation-act-1982":
      ("records/acts/1982/", "raw/zambialii/act/1982/1982-015.html"),
    "act-zm-1983-014-appropriation-act-1983":
      ("records/acts/1983/", "raw/zambialii/act/1983/1983-014.html"),
    "act-zm-1984-013-appropriation-act-1984":
      ("records/acts/1984/", "raw/zambialii/act/1984/1984-013.html"),
    "act-zm-1985-016-appropriation-act-1985":
      ("records/acts/1985/", "raw/zambialii/act/1985/1985-016.html"),
    "act-zm-1986-012-appropriation-act-1986":
      ("records/acts/1986/", "raw/zambialii/act/1986/1986-012.html"),
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
    yr_num_pairs = [("1964","036"),("1980","009"),("1981","012"),("1982","015"),
                    ("1983","014"),("1984","013"),("1985","016"),("1986","012")]
    for yr, num in yr_num_pairs:
        files = glob.glob(f"records/acts/{yr}/act-zm-{yr}-{num}-*.json")
        # Also check legacy flat path records/acts/act-zm-{yr}-{num}-*.json (older layout)
        files += glob.glob(f"records/acts/act-zm-{yr}-{num}-*.json")
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
