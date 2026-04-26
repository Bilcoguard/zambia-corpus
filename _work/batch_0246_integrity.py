"""Batch 0246 integrity checks.
CHECK1a: batch unique ids
CHECK1b: corpus presence on disk
CHECK2: amended_by refs resolve
CHECK3: repealed_by refs resolve
CHECK4: source_hash sha256 matches on-disk raw file
CHECK5: required fields present
CHECK6: cited_authorities refs resolve
"""
import json, os, hashlib, glob, sys

REQUIRED = ['id','type','jurisdiction','year','number','title','source_url','source_hash','fetched_at','parser_version']

def main():
    results = {}
    one_files = sorted(glob.glob('_work/batch_0246_one_*.json'))
    ok_records = []
    for f in one_files:
        r = json.load(open(f))
        if r.get('status') == 'ok':
            ok_records.append(r)
    print(f'OK records: {len(ok_records)}')

    # CHECK1a batch unique ids
    ids = [r['record']['id'] for r in ok_records]
    dup = [i for i in set(ids) if ids.count(i) > 1]
    check1a = not dup
    results['check1a_batch_unique'] = {'pass': check1a, 'count': len(ids), 'duplicates': dup}

    # CHECK1b corpus presence on disk
    missing = []
    for r in ok_records:
        rp = r['record_path']
        if not os.path.exists(rp):
            missing.append(rp)
    check1b = not missing
    results['check1b_corpus_presence'] = {'pass': check1b, 'count': len(ok_records), 'missing': missing}

    # Build corpus index for ref checks
    all_records = {}
    for f in glob.glob('records/**/*.json', recursive=True):
        try:
            r = json.load(open(f))
            if 'id' in r:
                all_records[r['id']] = f
        except Exception:
            pass

    # CHECK2 amended_by refs
    amended_unresolved = []
    for r in ok_records:
        for ref in r['record'].get('amended_by', []):
            if ref and ref not in all_records:
                amended_unresolved.append((r['record']['id'], ref))
    check2 = not amended_unresolved
    results['check2_amended_by'] = {'pass': check2, 'unresolved': amended_unresolved, 'refs_total': sum(len(r['record'].get('amended_by',[])) for r in ok_records)}

    # CHECK3 repealed_by refs
    repealed_unresolved = []
    for r in ok_records:
        for ref in r['record'].get('repealed_by', []):
            if ref and ref not in all_records:
                repealed_unresolved.append((r['record']['id'], ref))
    check3 = not repealed_unresolved
    results['check3_repealed_by'] = {'pass': check3, 'unresolved': repealed_unresolved, 'refs_total': sum(len(r['record'].get('repealed_by',[])) for r in ok_records)}

    # CHECK4 source_hash matches on-disk raw file
    hash_mismatches = []
    for r in ok_records:
        rec = r['record']
        # Find the PDF (or HTML) on disk that should match source_hash
        # Build expected paths
        yr = rec['year']; num = rec['number']
        # Search for the matching raw file - prefer PDF
        candidate_paths = sorted(glob.glob(f"raw/zambialii/si/{yr}/si-zm-{yr}-{num:03d}-*.pdf"))
        if not candidate_paths:
            candidate_paths = sorted(glob.glob(f"raw/zambialii/si/{yr}/si-zm-{yr}-{num:03d}-*.html"))
        matched = False
        for p in candidate_paths:
            with open(p,'rb') as fh:
                disk_sha = hashlib.sha256(fh.read()).hexdigest()
            if disk_sha == rec['source_hash']:
                matched = True; break
        if not matched:
            hash_mismatches.append({'id': rec['id'], 'expected': rec['source_hash'], 'candidates': candidate_paths})
    check4 = not hash_mismatches
    results['check4_source_hash'] = {'pass': check4, 'count': len(ok_records), 'mismatches': hash_mismatches}

    # CHECK5 required fields
    field_missing = []
    for r in ok_records:
        rec = r['record']
        miss = [f for f in REQUIRED if f not in rec or rec[f] in (None, '')]
        if miss:
            field_missing.append({'id': rec['id'], 'missing': miss})
    check5 = not field_missing
    results['check5_required_fields'] = {'pass': check5, 'count': len(ok_records), 'missing': field_missing}

    # CHECK6 cited_authorities
    cited_unresolved = []
    for r in ok_records:
        for ref in r['record'].get('cited_authorities', []):
            if ref and ref not in all_records:
                cited_unresolved.append((r['record']['id'], ref))
    check6 = not cited_unresolved
    results['check6_cited_authorities'] = {'pass': check6, 'unresolved': cited_unresolved, 'refs_total': sum(len(r['record'].get('cited_authorities',[])) for r in ok_records)}

    all_pass = check1a and check1b and check2 and check3 and check4 and check5 and check6
    results['ALL_PASS'] = all_pass
    json.dump(results, open('_work/batch_0246_integrity.json','w'), indent=2)
    print(json.dumps({k: v if isinstance(v, bool) else (v.get('pass') if isinstance(v, dict) else v) for k,v in results.items()}, indent=2))
    if not all_pass:
        print('FAIL details:')
        print(json.dumps(results, indent=2, default=str))
        sys.exit(1)

if __name__ == '__main__':
    main()
