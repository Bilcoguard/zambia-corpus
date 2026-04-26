"""Integrity checks for batch 0244.
CHECK1a: batch unique IDs
CHECK1b: every record on disk
CHECK2/3: amended_by/repealed_by refs resolve
CHECK4: source_hash matches on-disk raw file
CHECK5: required fields all present
CHECK6: cited_authorities refs resolve
"""
import os, json, hashlib, glob, sys

REQUIRED = ['id','type','jurisdiction','year','number','title',
            'source_url','source_hash','fetched_at','parser_version']

# Load all batch 0244 ok records
ok_records = []
nonok = []
for i in range(7):
    fp = f'_work/batch_0244_one_{i}.json'
    if not os.path.exists(fp):
        print(f'MISSING {fp}')
        sys.exit(2)
    d = json.load(open(fp))
    if d.get('status') != 'ok':
        nonok.append((i, d.get('status'), d.get('pick',{}).get('yr_num','')))
        continue
    ok_records.append(d['record'])
print(f'Non-ok records: {len(nonok)} -> {nonok}')

ids = [r['id'] for r in ok_records]
assert len(set(ids)) == len(ids), 'CHECK1a duplicate IDs in batch'
print(f'CHECK1a unique ids: {len(ids)}/{len(ids)} PASS')

# CHECK1b: every record on disk
for r in ok_records:
    yr = r['year']
    p = f'records/sis/{yr}/{r["id"]}.json'
    assert os.path.exists(p), f'missing on disk: {p}'
print(f'CHECK1b on-disk presence: {len(ok_records)}/{len(ok_records)} PASS')

# CHECK2/3 amended_by/repealed_by refs resolve
all_existing = set()
for fp in glob.glob('records/**/*.json', recursive=True):
    try:
        d = json.load(open(fp))
        if isinstance(d, dict) and 'id' in d:
            all_existing.add(d['id'])
    except: pass

unresolved2 = unresolved3 = 0
for r in ok_records:
    for ref in r.get('amended_by',[]):
        if ref not in all_existing: unresolved2 += 1
    for ref in r.get('repealed_by',[]):
        if ref not in all_existing: unresolved3 += 1
print(f'CHECK2 amended_by unresolved: {unresolved2}')
print(f'CHECK3 repealed_by unresolved: {unresolved3}')
assert unresolved2 == 0 and unresolved3 == 0

# CHECK4 source_hash matches on-disk raw file
mismatch = 0
for r in ok_records:
    yr = r['year']
    pdf_path = f'raw/zambialii/si/{yr}/{r["id"]}.pdf'
    if not os.path.exists(pdf_path):
        print(f'MISSING raw PDF: {pdf_path}')
        mismatch += 1
        continue
    pdf_bytes = open(pdf_path,'rb').read()
    sha = hashlib.sha256(pdf_bytes).hexdigest()
    if sha != r['source_hash']:
        print(f'SHA MISMATCH for {r["id"]}: disk={sha[:16]} record={r["source_hash"][:16]}')
        mismatch += 1
print(f'CHECK4 source_hash match: {len(ok_records)-mismatch}/{len(ok_records)} {"PASS" if mismatch==0 else "FAIL"}')
assert mismatch == 0

# CHECK5 required fields
missing = 0
for r in ok_records:
    for k in REQUIRED:
        if k not in r or r[k] in (None,'',[]):
            print(f'MISSING field {k} in {r["id"]}')
            missing += 1
print(f'CHECK5 required fields: {len(REQUIRED)*len(ok_records)-missing}/{len(REQUIRED)*len(ok_records)} {"PASS" if missing==0 else "FAIL"}')
assert missing == 0

# CHECK6 cited_authorities refs
unresolved6 = 0
for r in ok_records:
    for ref in r.get('cited_authorities',[]):
        if ref not in all_existing: unresolved6 += 1
print(f'CHECK6 cited_authorities unresolved: {unresolved6}')
assert unresolved6 == 0

print('\n=== ALL INTEGRITY CHECKS PASS ===')
import json as _j
out = {
    'batch':'0244',
    'records_count': len(ok_records),
    'check1a_unique_ids': True,
    'check1b_on_disk': True,
    'check2_amended_by_unresolved': unresolved2,
    'check3_repealed_by_unresolved': unresolved3,
    'check4_source_hash_mismatch': mismatch,
    'check5_required_fields_missing': missing,
    'check6_cited_authorities_unresolved': unresolved6,
    'status': 'PASS',
}
with open('_work/batch_0244_integrity.json','w') as f:
    _j.dump(out, f, indent=2)
print("wrote _work/batch_0244_integrity.json")
