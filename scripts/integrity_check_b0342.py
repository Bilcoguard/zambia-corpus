#!/usr/bin/env python3
"""Integrity check for batch 0342 — the 3 new ZMCC judgment records."""

import hashlib
import json
import pathlib
import sys
import yaml

ROOT = pathlib.Path("/sessions/friendly-brave-mendel/mnt/corpus")
RECORDS_DIR = ROOT / "records" / "judgments" / "zmcc" / "2026"

# IDs added in this batch
NEW_IDS = {
    "judgment-zm-2026-zmcc-02-morgan-ng-ona-suing-as-secretary-general-of-the-pa",
    "judgment-zm-2026-zmcc-06-munir-zulu-v-attorney-general-and-anor",
    "judgment-zm-2026-zmcc-07-climate-action-professionals-zambia-v-attorney-gen",
}

OUTCOME_ENUM = {"allowed", "dismissed", "upheld", "overturned", "remitted", "struck-out", "withdrawn"}
ROLE_ENUM = {"presiding", "concurring", "dissenting", "partial-concurring", "partial-dissenting"}
REQUIRED = {"id","type","jurisdiction","title","citation","court","case_name","case_number",
            "date_decided","judges","issue_tags","outcome","outcome_detail","reasoning_tags",
            "key_statutes","raw_sha256","source_url","source_hash","fetched_at","parser_version"}

failures = []
results = {}

# Load judges registry
reg = yaml.safe_load((ROOT / "judges_registry.yaml").read_text())
canonical = {j["canonical_name"] for j in reg["judges"]}

# Load all existing judgment IDs to check for duplicates across the corpus
all_ids = set()
for p in (ROOT / "records").glob("**/*.json"):
    try:
        d = json.loads(p.read_text())
        if "id" in d:
            if d["id"] in all_ids:
                failures.append(f"DUPLICATE ID: {d['id']} (in {p})")
            all_ids.add(d["id"])
    except Exception as e:
        pass

for rid in sorted(NEW_IDS):
    matches = list(RECORDS_DIR.glob(f"{rid}.json"))
    if not matches:
        failures.append(f"MISSING: {rid}")
        continue
    f = matches[0]
    rec = json.loads(f.read_text())
    rec_failures = []

    # Required fields
    missing = REQUIRED - set(rec.keys())
    if missing:
        rec_failures.append(f"missing fields: {sorted(missing)}")

    # Outcome enum
    if rec.get("outcome") not in OUTCOME_ENUM:
        rec_failures.append(f"outcome '{rec.get('outcome')}' not in enum")

    # ≥1 judge, role enum, name resolves
    if not rec.get("judges"):
        rec_failures.append("no judges")
    else:
        for j in rec["judges"]:
            if j.get("role") not in ROLE_ENUM:
                rec_failures.append(f"judge role '{j.get('role')}' not in enum (judge {j.get('name')})")
            if j.get("name") not in canonical:
                rec_failures.append(f"judge name '{j.get('name')}' does not resolve in registry")

    # ≥1 issue_tag
    if not rec.get("issue_tags"):
        rec_failures.append("no issue_tags")

    # source_hash matches HTML on disk
    raw_html = ROOT / "raw" / "zambialii" / "judgments" / "zmcc" / "2026" / f"{rid}.html"
    if raw_html.exists():
        actual = "sha256:" + hashlib.sha256(raw_html.read_bytes()).hexdigest()
        if actual != rec.get("source_hash"):
            rec_failures.append(f"source_hash mismatch: rec={rec.get('source_hash')[:30]}.. raw={actual[:30]}..")
    else:
        rec_failures.append(f"raw HTML not on disk: {raw_html}")

    # raw_sha256 matches PDF on disk
    raw_pdf = ROOT / "raw" / "zambialii" / "judgments" / "zmcc" / "2026" / f"{rid}.pdf"
    if raw_pdf.exists():
        actual = hashlib.sha256(raw_pdf.read_bytes()).hexdigest()
        if actual != rec.get("raw_sha256"):
            rec_failures.append(f"raw_sha256 mismatch: rec={rec.get('raw_sha256','')[:20]}.. pdf={actual[:20]}..")
    else:
        rec_failures.append(f"raw PDF not on disk: {raw_pdf}")

    # ID format
    if rec["id"] != rid:
        rec_failures.append(f"id mismatch in record vs filename")

    if rec_failures:
        failures.append((rid, rec_failures))
    else:
        results[rid] = "PASS"

print(json.dumps({
    "checked": len(NEW_IDS),
    "pass": len(results),
    "fail": len(failures),
    "failures": failures,
    "passes": list(results.keys()),
}, indent=2, default=str))

if failures:
    sys.exit(2)
