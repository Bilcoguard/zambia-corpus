"""Integrity check for batch 0270 - mirrors checks performed inline at tick.
Re-run with: python3 _work/integrity_0270.py
"""
import json, hashlib, os, sys
PICKS = [
    ("1983","10","supplementary-appropriation-1981-act-1983"),
    ("1984","5","excess-expenditure-appropriation-1981-act-1984"),
    ("1984","6","supplementary-appropriation-1982-act-1984"),
    ("1985","8","excess-expenditure-appropriation-1982-act-1985"),
    ("1985","9","supplementary-appropriation-1983-act-1985"),
    ("1986","9","supplementary-appropriation-1984-act-1986"),
    ("1986","10","excess-expenditure-appropriation-1983-act-1986"),
    ("1987","12","supplementary-appropriation-1985-act-1987"),
]
required=["id","type","jurisdiction","title","citation","enacted_date","commencement_date",
          "in_force","amended_by","repealed_by","cited_authorities","sections","source_url",
          "source_hash","fetched_at","parser_version"]
ok=True
ids=set()
for yr,num,slug in PICKS:
    rid=f"act-zm-{yr}-{int(num):03d}-{slug}"
    rp=f"records/acts/{yr}/{rid}.json"
    raw=f"raw/zambialii/act/{yr}/{yr}-{int(num):03d}.html"
    if not os.path.exists(rp): print("MISSING",rp); ok=False; continue
    with open(rp) as f: r=json.load(f)
    # CHECK1a unique within batch
    if r["id"] in ids: print("DUP_ID",r["id"]); ok=False
    ids.add(r["id"])
    # CHECK5 required fields
    for k in required:
        if k not in r: print("MISSING_FIELD",rid,k); ok=False
    # CHECK4 sha verify
    if not os.path.exists(raw): print("MISSING_RAW",raw); ok=False; continue
    expected=r["source_hash"].split(":")[1]
    actual=hashlib.sha256(open(raw,"rb").read()).hexdigest()
    if expected!=actual: print("SHA_MISMATCH",rid,expected,actual); ok=False
    # CHECK2/3 amended_by/repealed_by refs (none expected this batch)
    if r["amended_by"]:
        for ref in r["amended_by"]:
            import glob
            if not glob.glob(f"records/**/{ref}.json", recursive=True):
                print("UNRESOLVED_AMENDED_BY",rid,ref); ok=False
    if r["repealed_by"]:
        import glob
        if not glob.glob(f"records/**/{r['repealed_by']}.json", recursive=True):
            print("UNRESOLVED_REPEALED_BY",rid,r["repealed_by"]); ok=False
    # CHECK6 cited_authorities
    for ref in r["cited_authorities"]:
        import glob
        if not glob.glob(f"records/**/{ref}.json", recursive=True):
            print("UNRESOLVED_CITED",rid,ref); ok=False
    print(f"  {rid}: OK ({len(r['sections'])} sections, sha={expected[:16]}...)")
print("PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
