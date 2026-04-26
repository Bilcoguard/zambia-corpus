import json, os, re, hashlib, sys

BATCH = "0266"
PICKS = [
    ("1952","5","victoria-memorial-institute-repeal-act-1952"),
    ("1950","45","zambia-police-reserve-act-1950"),
    ("1967","28","war-graves-and-memorials-act-1967"),
    ("1972","26","termination-of-pregnancy-act-1972"),
    ("1972","37","technical-education-and-vocational-training-act-1972"),
    ("1973","49","trades-charges-act-1973"),
    ("1987","20","university-of-zambia-act-1987"),
    ("1992","26","university-act-1992"),
]

REQUIRED = ["id","type","jurisdiction","title","citation","enacted_date","commencement_date",
            "in_force","amended_by","repealed_by","cited_authorities","sections",
            "source_url","source_hash","fetched_at","parser_version"]

errors = []
ids_in_batch = []
records = []

for yr, num, slug in PICKS:
    rid = f"act-zm-{yr}-{int(num):03d}-{slug}"
    p = f"records/acts/{yr}/{rid}.json"
    if not os.path.exists(p):
        errors.append(f"CHECK1b miss: {p}"); continue
    with open(p) as f:
        rec = json.load(f)
    records.append(rec)
    ids_in_batch.append(rec["id"])

# CHECK1a: unique IDs in batch
dupes = [x for x in set(ids_in_batch) if ids_in_batch.count(x) > 1]
if dupes:
    errors.append(f"CHECK1a duplicates in batch: {dupes}")

# CHECK1b: each on disk - already done
# CHECK2/3: amended_by + repealed_by references resolve
all_existing_ids = set()
for root, dirs, files in os.walk("records"):
    for fn in files:
        if fn.endswith(".json"):
            all_existing_ids.add(fn[:-5])
abr = 0; rbr = 0
for rec in records:
    for ref in rec.get("amended_by") or []:
        abr += 1
        if ref not in all_existing_ids:
            errors.append(f"CHECK2 amended_by unresolved: {rec['id']} -> {ref}")
    if rec.get("repealed_by"):
        rbr += 1
        if rec["repealed_by"] not in all_existing_ids:
            errors.append(f"CHECK3 repealed_by unresolved: {rec['id']} -> {rec['repealed_by']}")

# CHECK4: source_hash matches on-disk raw
sha_ok = 0
for rec in records:
    yr_match = re.match(r"act-zm-(\d+)-(\d+)-", rec["id"])
    if not yr_match:
        errors.append(f"CHECK4 cannot parse id: {rec['id']}"); continue
    yr = yr_match.group(1); num = int(yr_match.group(2))
    raw_path = f"raw/zambialii/act/{yr}/{yr}-{num:03d}.html"
    if not os.path.exists(raw_path):
        errors.append(f"CHECK4 raw missing: {raw_path}"); continue
    with open(raw_path, "rb") as f:
        on_disk = hashlib.sha256(f.read()).hexdigest()
    expected = rec["source_hash"].replace("sha256:","")
    if on_disk != expected:
        errors.append(f"CHECK4 hash mismatch: {rec['id']} disk={on_disk[:16]} rec={expected[:16]}")
    else:
        sha_ok += 1

# CHECK5: required fields present
field_misses = 0
for rec in records:
    for fld in REQUIRED:
        if fld not in rec:
            errors.append(f"CHECK5 missing {fld} in {rec['id']}"); field_misses += 1

# CHECK6: cited_authorities references resolve
ca_count = 0
for rec in records:
    for ref in rec.get("cited_authorities") or []:
        ca_count += 1
        if ref not in all_existing_ids:
            errors.append(f"CHECK6 cited_authorities unresolved: {rec['id']} -> {ref}")

summary = {
    "batch": BATCH,
    "records_checked": len(records),
    "CHECK1a_unique_in_batch": len(set(ids_in_batch)) == len(ids_in_batch),
    "CHECK1b_all_on_disk": all(os.path.exists(f"records/acts/{yr}/act-zm-{yr}-{int(num):03d}-{slug}.json") for yr,num,slug in PICKS),
    "CHECK2_amended_by_refs": abr,
    "CHECK3_repealed_by_refs": rbr,
    "CHECK4_sha256_verified": sha_ok,
    "CHECK5_required_field_misses": field_misses,
    "CHECK6_cited_authorities_refs": ca_count,
    "errors": errors,
}
print(json.dumps(summary, indent=2))
sys.exit(0 if not errors else 1)
