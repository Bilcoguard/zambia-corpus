"""Integrity checks for batch 0248. CHECK1a-CHECK6. Mirror of batch 0247."""
import os, json, hashlib, glob

BATCH_RESULTS = sorted(glob.glob('_work/batch_0248_one_*.json'))
results = []
for r in BATCH_RESULTS:
    d = json.load(open(r))
    if d.get('status') == 'ok' and 'record' in d:
        results.append(d)

batch_records = [d['record'] for d in results]

# CHECK1a: batch unique IDs
check1a = len(set(r['id'] for r in batch_records)) == len(batch_records)

# CHECK1b: corpus presence on disk (each record JSON exists where expected)
check1b = all(os.path.exists(d['record_path']) for d in results)

# CHECK2/3: amended_by, repealed_by references resolve in entire corpus
all_ids = set()
for f in glob.glob('records/sis/**/*.json', recursive=True):
    try:
        all_ids.add(json.load(open(f))['id'])
    except:
        pass
for f in glob.glob('records/acts/**/*.json', recursive=True):
    try:
        all_ids.add(json.load(open(f))['id'])
    except:
        pass
unresolved_amend = []
unresolved_repeal = []
for r in batch_records:
    for ref in r.get('amended_by', []):
        if ref not in all_ids:
            unresolved_amend.append((r['id'], ref))
    for ref in r.get('repealed_by', []):
        if ref not in all_ids:
            unresolved_repeal.append((r['id'], ref))
check2 = len(unresolved_amend) == 0
check3 = len(unresolved_repeal) == 0

# CHECK4: source_hash matches raw file on disk
sha_mismatches = []
for r in batch_records:
    yr = r['year']
    rid = r['id']
    pdf_path = f"raw/zambialii/si/{yr}/{rid}.pdf"
    html_path = f"raw/zambialii/si/{yr}/{rid}.html"
    if os.path.exists(pdf_path):
        actual = hashlib.sha256(open(pdf_path,'rb').read()).hexdigest()
        if actual != r['source_hash']:
            sha_mismatches.append((r['id'], 'pdf', actual[:16], r['source_hash'][:16]))
    elif os.path.exists(html_path):
        actual = hashlib.sha256(open(html_path,'rb').read()).hexdigest()
        if actual != r['source_hash']:
            sha_mismatches.append((r['id'], 'html', actual[:16], r['source_hash'][:16]))
    else:
        sha_mismatches.append((r['id'], 'no_raw_file', '', ''))
check4 = len(sha_mismatches) == 0

# CHECK5: required fields present
required = ['id','type','jurisdiction','title','source_url','source_hash',
            'fetched_at','parser_version','year','number']
field_misses = []
for r in batch_records:
    for f in required:
        if f not in r or r[f] in (None, ''):
            field_misses.append((r['id'], f))
check5 = len(field_misses) == 0

# CHECK6: cited_authorities resolve
unresolved_cite = []
for r in batch_records:
    for ref in r.get('cited_authorities', []):
        if ref not in all_ids:
            unresolved_cite.append((r['id'], ref))
check6 = len(unresolved_cite) == 0

result = {
    'batch': '0248',
    'records_count': len(batch_records),
    'CHECK1a_unique': check1a,
    'CHECK1b_disk_presence': check1b,
    'CHECK2_amended_by_resolves': check2,
    'CHECK3_repealed_by_resolves': check3,
    'CHECK4_sha256_matches': check4,
    'CHECK5_required_fields': check5,
    'CHECK6_cited_authorities_resolve': check6,
    'unresolved_amend': unresolved_amend,
    'unresolved_repeal': unresolved_repeal,
    'sha_mismatches': sha_mismatches,
    'field_misses': field_misses,
    'unresolved_cite': unresolved_cite,
    'all_pass': all([check1a, check1b, check2, check3, check4, check5, check6]),
}
with open('_work/batch_0248_integrity.json','w') as f:
    json.dump(result, f, indent=2)
print(json.dumps(result, indent=2))
