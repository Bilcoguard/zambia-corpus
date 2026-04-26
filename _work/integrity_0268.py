"""Integrity check for batch 0268 - mirrors checks performed inline at 13:38Z tick.
Re-run with: python3 _work/integrity_0268.py
"""
import json, hashlib, os, sys
PICKS = [
    ("1989","1","zambia-centre-for-accountancy-studies-act-1989"),
    ("1993","25","zambia-iron-and-steel-authority-dissolution-act-1993"),
    ("1995","24","zambia-institute-of-diplomacy-and-international-studies-act-1995"),
    ("1995","36","zambia-institute-of-architects-act-1995"),
    ("1996","10","zambia-institute-of-advanced-legal-education-act-1996"),
    ("1996","11","zambia-law-development-commission-act-1996"),
    ("1996","19","zambia-institute-of-mass-communications-repeal-act-1996"),
    ("1997","11","zambia-institute-of-human-resources-management-act-1997"),
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
    # CHECK1b on disk (already verified above by os.path.exists)
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
            tgt = f"records/**/{ref}.json"
            import glob
            if not glob.glob(tgt, recursive=True):
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
print("PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
