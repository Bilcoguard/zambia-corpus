#!/usr/bin/env python3
"""Integrity check for batch-0372 (Phase 5 ZMCC ingestion).

Validates the records written by batch_0372_parse.py (driven from
_work/b0372/parse_summary.json):
  - All 20 required fields present
  - id matches /^judgment-zm-[a-z0-9-]+$/
  - date_decided YYYY-MM-DD
  - outcome ∈ enum
  - court ∈ enum
  - judges[*].role ∈ enum
  - all judges resolve in judges_registry.yaml (canonical or bare-surname)
  - ≥1 issue_tag
  - source_hash matches raw HTML on disk
  - raw_sha256 matches raw PDF on disk
  - id is globally unique within records/judgments/
  - outcome_detail safety: no blacklisted substrings, ≥12 alphabetic chars,
    no leading lowercase mid-word fragment.
"""

import hashlib
import json
import pathlib
import re
import sys
import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
SUMMARY = ROOT / "_work/b0372/parse_summary.json"

REQUIRED = [
    "id", "type", "jurisdiction", "title", "citation", "court", "case_name",
    "case_number", "date_decided", "judges", "issue_tags", "outcome",
    "outcome_detail", "reasoning_tags", "key_statutes", "raw_sha256",
    "source_url", "source_hash", "fetched_at", "parser_version",
]
OUTCOMES = {"dismissed", "allowed", "withdrawn", "struck-out", "remitted",
            "upheld", "overturned"}
COURTS = {"Constitutional Court of Zambia", "Supreme Court of Zambia",
          "Court of Appeal of Zambia", "High Court of Zambia",
          "Industrial Relations Court", "Subordinate Court", "Local Court"}
ROLES = {"presiding", "concurring", "dissenting", "partial-concurring",
         "partial-dissenting"}
DETAIL_BLACKLIST = ["case supra", " supra", "another v ",
                    "Generall4l", "Generall4]", "Mulonda"]


def find_record_path(rec_id):
    for p in (ROOT / "records/judgments").rglob("*.json"):
        if p.stem == rec_id:
            return p
    return None


def main():
    summary = json.loads(SUMMARY.read_text())
    written = summary["written"]
    errors = []

    reg = yaml.safe_load((ROOT / "judges_registry.yaml").read_text())
    canonicals = {j["canonical_name"] for j in reg["judges"]}

    # global uniqueness
    ids = {}
    for p in (ROOT / "records/judgments").rglob("*.json"):
        try:
            r = json.loads(p.read_text())
        except Exception:
            continue
        rid = r.get("id")
        if not rid:
            continue
        ids.setdefault(rid, []).append(str(p))
    dups = {k: v for k, v in ids.items() if len(v) > 1}
    if dups:
        errors.append(f"duplicate ids in judgments: {list(dups)[:3]}")

    for w in written:
        rid = w["id"]
        rec_path = find_record_path(rid)
        if rec_path is None:
            errors.append(f"{rid}: record JSON not found on disk")
            continue
        rec = json.loads(rec_path.read_text())

        missing = [k for k in REQUIRED if k not in rec]
        if missing:
            errors.append(f"{rid}: missing fields: {missing}")

        if not re.match(r"^judgment-zm-[a-z0-9-]+$", rec["id"]):
            errors.append(f"{rid}: bad id pattern: {rec['id']}")

        if not re.match(r"^\d{4}-\d{2}-\d{2}$", rec["date_decided"] or ""):
            errors.append(f"{rid}: bad date_decided: {rec['date_decided']}")

        if rec["outcome"] not in OUTCOMES:
            errors.append(f"{rid}: bad outcome: {rec['outcome']}")

        if rec["court"] not in COURTS:
            errors.append(f"{rid}: bad court: {rec['court']}")

        if not rec["judges"]:
            errors.append(f"{rid}: no judges")
        for j in rec["judges"]:
            if j.get("role") not in ROLES:
                errors.append(f"{rid}: bad judge role: {j}")
            name = j["name"]
            if name in canonicals:
                continue
            if any(cn.split()[0] == name for cn in canonicals):
                continue
            errors.append(f"{rid}: unresolved judge: {name}")

        if not rec["issue_tags"]:
            errors.append(f"{rid}: issue_tags empty")

        # source_hash + raw_sha256 against raw files on disk
        html_path = pathlib.Path(w["html_path"])
        pdf_path = pathlib.Path(w["pdf_path"])
        if not html_path.exists():
            errors.append(f"{rid}: raw HTML missing: {html_path}")
        else:
            h = "sha256:" + hashlib.sha256(html_path.read_bytes()).hexdigest()
            if rec["source_hash"] != h:
                errors.append(f"{rid}: source_hash mismatch rec={rec['source_hash']} disk={h}")
        if not pdf_path.exists():
            errors.append(f"{rid}: raw PDF missing: {pdf_path}")
        else:
            p = hashlib.sha256(pdf_path.read_bytes()).hexdigest()
            if rec["raw_sha256"] != p:
                errors.append(f"{rid}: raw_sha256 mismatch rec={rec['raw_sha256']} disk={p}")

        detail = rec["outcome_detail"] or ""
        for bad in DETAIL_BLACKLIST:
            if bad in detail:
                errors.append(f"{rid}: outcome_detail contains blacklist substr: {bad}")
        if len(re.sub(r"[^A-Za-z]", "", detail)) < 12:
            errors.append(f"{rid}: outcome_detail too short")
        if re.match(r"^[a-z](?:\s|$)", detail):
            errors.append(f"{rid}: outcome_detail starts mid-word")

    if errors:
        print("INTEGRITY CHECK: FAIL")
        for e in errors:
            print("  -", e)
        sys.exit(1)
    print(f"INTEGRITY CHECK: PASS ({len(written)} record(s))")


if __name__ == "__main__":
    main()
