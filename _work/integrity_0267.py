"""Integrity check for batch 0267 - mirrors checks performed inline at 12:50Z tick.
Re-run with: python3 _work/integrity_0267.py
"""
import json, hashlib, os, sys
PICKS = [
    ("1964","39","zambia-youth-service-act-1964"),
    ("1966","1","zambia-national-provident-fund-act-1966"),
    ("1966","9","zambia-red-cross-society-act-1966"),
    ("1966","32","zambia-national-commission-for-unesco-act-1966"),
    ("1966","50","zambian-mines-local-pension-fund-dissolution-act-1966"),
    ("1967","18","zambia-tanzania-pipeline-act-1967"),
    ("1973","43","zambia-security-intelligence-service-act-1973"),
    ("1982","30","zambia-national-tender-board-act-1982"),
]
required=["id","type","jurisdiction","title","citation","enacted_date","commencement_date",
          "in_force","amended_by","repealed_by","cited_authorities","sections","source_url",
          "source_hash","fetched_at","parser_version"]
ok=True
for yr,num,slug in PICKS:
    rid=f"act-zm-{yr}-{int(num):03d}-{slug}"
    rp=f"records/acts/{yr}/{rid}.json"
    raw=f"raw/zambialii/act/{yr}/{yr}-{int(num):03d}.html"
    if not os.path.exists(rp): print("MISSING",rp); ok=False; continue
    with open(rp) as f: r=json.load(f)
    for k in required:
        if k not in r: print("MISSING_FIELD",rid,k); ok=False
    if not os.path.exists(raw): print("MISSING_RAW",raw); ok=False; continue
    expected=r["source_hash"].split(":")[1]
    actual=hashlib.sha256(open(raw,"rb").read()).hexdigest()
    if expected!=actual: print("SHA_MISMATCH",rid); ok=False
print("PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
