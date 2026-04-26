"""Integrity checks for batch 0245.
CHECK1a: no duplicate IDs in batch.
CHECK1b: each record file is on disk.
CHECK2/3: amended_by/repealed_by references resolve (none expected).
CHECK4: source_hash matches sha256 of raw PDF on disk.
CHECK5: required fields present.
CHECK6: cited_authorities references resolve (none expected).
"""
import json, os, hashlib, glob, sys

BATCH_OK_INDICES = {'main':[5,6,7], 'sub':[1,2,3,4]}  # only ok results

records = []
for i in BATCH_OK_INDICES['main']:
    d = json.load(open(f'_work/batch_0245_one_{i}.json'))
    if d['status']=='ok':
        records.append(d)
for i in BATCH_OK_INDICES['sub']:
    p = f'_work/batch_0245_sub_{i}.json'
    if os.path.exists(p):
        d = json.load(open(p))
        if d['status']=='ok':
            records.append(d)

results = {'CHECK1a':None,'CHECK1b':None,'CHECK2':None,'CHECK3':None,
           'CHECK4':None,'CHECK5':None,'CHECK6':None,
           'records':[r['record']['id'] for r in records]}

# CHECK1a duplicate IDs
ids = [r['record']['id'] for r in records]
results['CHECK1a'] = 'PASS' if len(ids)==len(set(ids)) else 'FAIL'

# CHECK1b corpus presence on disk
missing=[]
for r in records:
    p = r['record_path']
    if not os.path.exists(p): missing.append(p)
results['CHECK1b'] = 'PASS' if not missing else f'FAIL missing={missing}'

# CHECK2/3 amended_by + repealed_by
unresolved=[]
for r in records:
    for ref in r['record'].get('amended_by',[]) + r['record'].get('repealed_by',[]):
        # any ref must resolve to a record id in records/
        found = False
        for root,_,files in os.walk('records'):
            if any(f.startswith(ref) for f in files):
                found=True; break
        if not found: unresolved.append(ref)
results['CHECK2'] = 'PASS' if not unresolved else f'FAIL {unresolved}'
results['CHECK3'] = results['CHECK2']  # same check

# CHECK4 source_hash matches PDF on disk
mismatches=[]
for r in records:
    rec = r['record']
    # find the PDF fetch
    pdf_path = None
    for f in r['fetches']:
        if f['path'].endswith('.pdf'): pdf_path = f['path']; break
    if pdf_path:
        with open(pdf_path,'rb') as fp:
            disk_sha = hashlib.sha256(fp.read()).hexdigest()
        if disk_sha != rec['source_hash']:
            mismatches.append((rec['id'], disk_sha, rec['source_hash']))
results['CHECK4'] = 'PASS' if not mismatches else f'FAIL {mismatches}'

# CHECK5 required fields
required = ['id','type','jurisdiction','title','source_url','source_hash',
            'fetched_at','parser_version','amended_by','repealed_by']
missing_fields=[]
for r in records:
    rec = r['record']
    for k in required:
        if k not in rec: missing_fields.append((rec['id'],k))
results['CHECK5'] = 'PASS' if not missing_fields else f'FAIL {missing_fields}'

# CHECK6 cited_authorities resolve
unresolved_cites=[]
for r in records:
    for ref in r['record'].get('cited_authorities',[]):
        found = False
        for root,_,files in os.walk('records'):
            if any(f.startswith(ref) for f in files):
                found=True; break
        if not found: unresolved_cites.append(ref)
results['CHECK6'] = 'PASS' if not unresolved_cites else f'FAIL {unresolved_cites}'

results['record_count'] = len(records)
results['all_pass'] = all(v=='PASS' or v.startswith('PASS') for k,v in results.items()
                          if k.startswith('CHECK'))

with open('_work/batch_0245_integrity.json','w') as f:
    json.dump(results, f, indent=2)
print(json.dumps(results, indent=2))
