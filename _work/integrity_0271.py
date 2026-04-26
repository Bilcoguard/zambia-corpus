"""Integrity check for batch 0271 - mirrors checks performed inline at tick.
Re-run with: python3 _work/integrity_0271.py
"""
import json, hashlib, os, sys
PICKS = [
    ("1987","13","excess-expenditure-appropriation-1984-act-1987"),
    ("1988","14","excess-expenditure-appropriation-1985-act-1988"),
    ("1988","15","supplementary-appropriation-1986-act-1988"),
    ("1988","30","excess-expenditure-appropriation-1986-act-1988"),
    ("1989","32","excess-expenditure-appropriation-1987-act-1989"),
    ("1990","38","excess-expenditure-appropriation-1988-act-1990"),
    ("1992","15","excess-expenditure-appropriation-1989-act-1992"),
    ("1993","20","prices-and-incomes-commission-dissolution-act-1993"),
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
    if r["id"] in ids: print("DUP_ID",r["id"]); ok=False
    ids.add(r["id"])
    for k in required:
        if k not in r: print("MISSING_FIELD",rid,k); ok=False
    if not os.path.exists(raw): print("MISSING_RAW",raw); ok=False; continue
    expected=r["source_hash"].split(":")[1]
    actual=hashlib.sha256(open(raw,"rb").read()).hexdigest()
    if expected!=actual: print("SHA_MISMATCH",rid,expected,actual); ok=False
    if r["amended_by"]:
        import glob
        for ref in r["amended_by"]:
            if not glob.glob(f"records/**/{ref}.json", recursive=True):
                print("UNRESOLVED_AMENDED_BY",rid,ref); ok=False
    if r["repealed_by"]:
        import glob
        if not glob.glob(f"records/**/{r['repealed_by']}.json", recursive=True):
            print("UNRESOLVED_REPEALED_BY",rid,r["repealed_by"]); ok=False
    for ref in r["cited_authorities"]:
        import glob
        if not glob.glob(f"records/**/{ref}.json", recursive=True):
            print("UNRESOLVED_CITED",rid,ref); ok=False
    print(f"  {rid}: OK ({len(r['sections'])} sections, sha={expected[:16]}...)")
print("PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
