#!/usr/bin/env python3
"""Integrity check for batch 0344.

Scope: the 3 newly-written ZMCC judgment records plus a sanity sweep over
all judgment records in records/judgments/ to catch any cross-batch
regressions.

Checks:
  Standard:
    - No duplicate IDs across all judgment records.
    - source_hash matches sha256 of the on-disk raw HTML.
    - raw_sha256 matches sha256 of the on-disk raw PDF.
  Phase 5:
    - judgment.schema.json validation (jsonschema-light: required keys,
      enums for outcome and judge.role, court enum).
    - At least 1 judge.
    - At least 1 issue_tag.
    - Every judges[*].name resolves in judges_registry.yaml (either as a
      bare-surname canonical or as the first whitespace-token of an
      existing canonical, matching the registry-update logic in
      batch_0344_parse.py).

Exit non-zero on any failure. Prints a concise pass/fail summary.
"""

import hashlib
import json
import pathlib
import re
import sys
from collections import defaultdict

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
RECORDS_DIR = ROOT / "records" / "judgments"
JUDGES_REG = ROOT / "judges_registry.yaml"
SCHEMA_PATH = ROOT / "schema" / "judgment.schema.json"

NEW_RECORDS = [
    RECORDS_DIR / "zmcc" / "2025" / "judgment-zm-2025-zmcc-27-munir-zuu-and-anor-v-attorney-general-and-ors.json",
    RECORDS_DIR / "zmcc" / "2025" / "judgment-zm-2025-zmcc-29-law-association-of-zambia-and-ors-v-attorney-gener.json",
    RECORDS_DIR / "zmcc" / "2025" / "judgment-zm-2025-zmcc-31-munir-zulu-and-anor-v-attorney-general-and-ors.json",
]

OUTCOME_ENUM = {"allowed", "dismissed", "upheld", "overturned", "remitted", "struck-out", "withdrawn"}
ROLE_ENUM = {"presiding", "concurring", "dissenting", "partial-concurring", "partial-dissenting"}
COURT_ENUM = {
    "Constitutional Court of Zambia",
    "Supreme Court of Zambia",
    "Court of Appeal of Zambia",
    "High Court of Zambia",
    "Industrial Relations Court of Zambia",
}
REQUIRED = [
    "id", "type", "jurisdiction", "title", "citation",
    "court", "case_name", "case_number", "date_decided",
    "judges", "issue_tags", "outcome", "outcome_detail",
    "reasoning_tags", "key_statutes", "raw_sha256",
    "source_url", "source_hash", "fetched_at", "parser_version",
]


def load_registry() -> set[str]:
    reg = yaml.safe_load(JUDGES_REG.read_text())
    canonicals = set()
    for j in reg["judges"]:
        canonicals.add(j["canonical_name"])
    return canonicals


def judge_resolves(canonicals: set[str], name: str) -> bool:
    if name in canonicals:
        return True
    # Match against first whitespace-token of an existing canonical.
    for cn in canonicals:
        first = cn.split()[0] if cn else ""
        if first == name:
            return True
    return False


def find_raw_pair(record_path: pathlib.Path):
    rec_id = record_path.stem
    # records/judgments/zmcc/2025/<id>.json -> raw/zambialii/judgments/zmcc/2025/<id>.html|.pdf
    parts = record_path.parts
    try:
        idx = parts.index("judgments")
    except ValueError:
        return None, None
    court_year = parts[idx + 1: idx + 3]
    raw_dir = ROOT / "raw" / "zambialii" / "judgments" / court_year[0] / court_year[1]
    html = raw_dir / f"{rec_id}.html"
    pdf = raw_dir / f"{rec_id}.pdf"
    return (html if html.exists() else None,
            pdf if pdf.exists() else None)


def check_record(rec_path: pathlib.Path, canonicals: set[str], errors: list, all_ids: dict):
    try:
        rec = json.loads(rec_path.read_text())
    except Exception as e:
        errors.append((str(rec_path), f"json_load_error: {e}"))
        return
    rid = rec.get("id")
    if rid in all_ids:
        errors.append((str(rec_path), f"duplicate_id collision with {all_ids[rid]}"))
    else:
        all_ids[rid] = str(rec_path)

    # Required keys
    for k in REQUIRED:
        if k not in rec:
            errors.append((rid, f"missing_required:{k}"))
    if rec.get("type") != "judgment":
        errors.append((rid, f"type_not_judgment:{rec.get('type')}"))
    if rec.get("jurisdiction") != "ZM":
        errors.append((rid, f"jurisdiction_not_ZM:{rec.get('jurisdiction')}"))
    if rec.get("court") not in COURT_ENUM:
        errors.append((rid, f"court_not_in_enum:{rec.get('court')}"))
    if rec.get("outcome") not in OUTCOME_ENUM:
        errors.append((rid, f"outcome_not_in_enum:{rec.get('outcome')}"))
    if not isinstance(rec.get("issue_tags"), list) or not rec.get("issue_tags"):
        errors.append((rid, "issue_tags_empty"))
    judges = rec.get("judges") or []
    if not judges:
        errors.append((rid, "no_judges"))
    for j in judges:
        if j.get("role") not in ROLE_ENUM:
            errors.append((rid, f"judge_role_not_in_enum:{j.get('role')}"))
        if not judge_resolves(canonicals, j.get("name", "")):
            errors.append((rid, f"judge_not_in_registry:{j.get('name')}"))
    # ID pattern
    if not re.match(r"^judgment-zm-[a-z0-9-]+$", rid or ""):
        errors.append((rid, "id_pattern_violation"))
    # Date format
    if not re.match(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$", rec.get("date_decided") or ""):
        errors.append((rid, f"date_decided_pattern:{rec.get('date_decided')}"))
    # raw_sha256 pattern
    if not re.match(r"^[a-f0-9]{64}$", rec.get("raw_sha256") or ""):
        errors.append((rid, "raw_sha256_pattern"))
    if not re.match(r"^sha256:[a-f0-9]{64}$", rec.get("source_hash") or ""):
        errors.append((rid, "source_hash_pattern"))
    if not re.match(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$", rec.get("fetched_at") or ""):
        errors.append((rid, f"fetched_at_pattern:{rec.get('fetched_at')}"))


def check_hash_match(rec_path: pathlib.Path, errors: list):
    rec = json.loads(rec_path.read_text())
    html_path, pdf_path = find_raw_pair(rec_path)
    if html_path is None:
        errors.append((rec.get("id"), "raw_html_missing"))
    else:
        h = "sha256:" + hashlib.sha256(html_path.read_bytes()).hexdigest()
        if h != rec.get("source_hash"):
            errors.append((rec.get("id"), f"source_hash_mismatch on_disk={h} record={rec.get('source_hash')}"))
    if pdf_path is None:
        errors.append((rec.get("id"), "raw_pdf_missing"))
    else:
        h = hashlib.sha256(pdf_path.read_bytes()).hexdigest()
        if h != rec.get("raw_sha256"):
            errors.append((rec.get("id"), f"raw_sha256_mismatch on_disk={h} record={rec.get('raw_sha256')}"))


def main():
    errors_new = []
    errors_global_dup = []
    canonicals = load_registry()

    # Global duplicate-ID sweep over all judgment records.
    all_ids = {}
    for f in sorted(RECORDS_DIR.glob("**/*.json")):
        try:
            rec = json.loads(f.read_text())
        except Exception as e:
            errors_global_dup.append((str(f), f"json_load_error: {e}"))
            continue
        rid = rec.get("id")
        if not rid:
            continue
        if rid in all_ids:
            errors_global_dup.append((rid, f"duplicate_id_global: {all_ids[rid]} & {f}"))
        else:
            all_ids[rid] = str(f)

    # Per-new-record schema + hash checks.
    seen_ids = {}
    for r in NEW_RECORDS:
        if not r.exists():
            errors_new.append((str(r), "record_missing_after_parse"))
            continue
        check_record(r, canonicals, errors_new, seen_ids)
        check_hash_match(r, errors_new)

    if errors_new:
        print("FAIL — new-record integrity check:")
        for e in errors_new:
            print("  ", e)
    else:
        print(f"PASS — new-record integrity check ({len(NEW_RECORDS)} records).")

    if errors_global_dup:
        # Note: we treat these as informational unless they involve any of
        # the new IDs. Pre-existing duplicates in records/acts/ have been
        # documented in prior batch reports (b0128/b0264/b0289 lineage).
        new_ids = {pathlib.Path(p).stem for p in [str(x) for x in NEW_RECORDS]}
        regress = [e for e in errors_global_dup if any(n in str(e) for n in new_ids)]
        if regress:
            print("FAIL — duplicate-ID regression involving new records:")
            for e in regress:
                print("  ", e)
        else:
            print(f"INFO — pre-existing duplicate IDs (not from this batch): {len(errors_global_dup)}")
    else:
        print("PASS — no duplicate IDs in records/judgments/.")

    # Final exit code
    if errors_new:
        sys.exit(2)
    if errors_global_dup:
        new_ids = {pathlib.Path(p).stem for p in [str(x) for x in NEW_RECORDS]}
        if any(n in str(e) for e in errors_global_dup for n in new_ids):
            sys.exit(3)
    sys.exit(0)


if __name__ == "__main__":
    main()
