#!/usr/bin/env python3
"""Integrity check for batch-0346 (Phase 5 ZMCC ingestion).

Validates the 1 record written by batch_0346_parse.py:
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
NEW = ROOT / "records/judgments/zmcc/2025/judgment-zm-2025-zmcc-13-issac-mwanza-and-anor-v-the-attorney-general-and-o.json"

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
ROLES = {"presiding", "concurring", "dissenting"}
DETAIL_BLACKLIST = ["case supra", " supra", "another v ",
                    "Generall4l", "Generall4]", "Mulonda"]


def main():
    rec = json.loads(NEW.read_text())
    errors = []

    missing = [k for k in REQUIRED if k not in rec]
    if missing:
        errors.append(f"missing fields: {missing}")

    if not re.match(r"^judgment-zm-[a-z0-9-]+$", rec["id"]):
        errors.append(f"bad id pattern: {rec['id']}")

    if not re.match(r"^\d{4}-\d{2}-\d{2}$", rec["date_decided"]):
        errors.append(f"bad date_decided: {rec['date_decided']}")

    if rec["outcome"] not in OUTCOMES:
        errors.append(f"bad outcome: {rec['outcome']}")

    if rec["court"] not in COURTS:
        errors.append(f"bad court: {rec['court']}")

    for j in rec["judges"]:
        if j.get("role") not in ROLES:
            errors.append(f"bad judge role: {j}")

    reg = yaml.safe_load((ROOT / "judges_registry.yaml").read_text())
    canonicals = {j["canonical_name"] for j in reg["judges"]}
    for j in rec["judges"]:
        name = j["name"]
        if name in canonicals:
            continue
        if any(cn.split()[0] == name for cn in canonicals):
            continue
        errors.append(f"unresolved judge: {name}")

    if not rec["issue_tags"]:
        errors.append("issue_tags empty")

    raw_dir = ROOT / "raw/zambialii/judgments/zmcc/2025"
    htmls = list(raw_dir.glob("judgment-zm-2025-zmcc-13-*.html"))
    pdfs = list(raw_dir.glob("judgment-zm-2025-zmcc-13-*.pdf"))
    if not htmls or not pdfs:
        errors.append("raw HTML or PDF missing on disk for zmcc-13")
    else:
        h = "sha256:" + hashlib.sha256(htmls[0].read_bytes()).hexdigest()
        p = hashlib.sha256(pdfs[0].read_bytes()).hexdigest()
        if rec["source_hash"] != h:
            errors.append(f"source_hash mismatch: rec={rec['source_hash']} disk={h}")
        if rec["raw_sha256"] != p:
            errors.append(f"raw_sha256 mismatch: rec={rec['raw_sha256']} disk={p}")

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

    detail = rec["outcome_detail"] or ""
    for bad in DETAIL_BLACKLIST:
        if bad in detail:
            errors.append(f"outcome_detail contains blacklist substr: {bad}")
    if len(re.sub(r"[^A-Za-z]", "", detail)) < 12:
        errors.append("outcome_detail too short")
    if re.match(r"^[a-z](?:\s|$)", detail):
        errors.append("outcome_detail starts mid-word")

    if errors:
        print("INTEGRITY CHECK: FAIL")
        for e in errors:
            print("  -", e)
        sys.exit(1)
    print("INTEGRITY CHECK: PASS (1 record)")


if __name__ == "__main__":
    main()
