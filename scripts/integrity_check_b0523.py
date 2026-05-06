#!/usr/bin/env python3
"""Integrity check b0523 — judgment-ingestion-worker tick.

Validates the 4 ZMSC 2022 records written this tick (nums 50, 49, 48, 47)
pass the seven required checks from the SKILL.md non-negotiables.
"""
import hashlib
import json
import pathlib
import re
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent

ALLOWED_OUTCOMES = {
    "allowed", "dismissed", "upheld", "overturned", "remitted",
    "struck-out", "withdrawn", "granted", "refused", "set-aside",
    "quashed", "other",
}

NEW_IDS = [
    "judgment-zm-2022-zmsc-50-banda-v-people",
    "judgment-zm-2022-zmsc-49-nkonde-and-ors-v-attorney-general",
    "judgment-zm-2022-zmsc-48-mbazima-v-tobacco-association-of-zambia",
    "judgment-zm-2022-zmsc-47-mwandila-v-phiri",
]

REQUIRED_FIELDS = [
    "id", "type", "court", "citation", "case_name", "case_number",
    "date_decided", "judges", "issue_tags", "outcome", "outcome_detail",
    "reasoning_tags", "key_statutes", "raw_sha256", "source_url",
]

ID_PAT = re.compile(r"^judgment-zm-(\d{4})-(zmsc|zmcc|zmhc|zmca)-(\d+)-")

passed = 0
failed = 0
errors = []


def check(cond, msg):
    global passed, failed
    if cond:
        passed += 1
    else:
        failed += 1
        errors.append(msg)


def main():
    reg_data = yaml.safe_load((ROOT / "judges_registry.yaml").read_text())
    canonical_names = {j["canonical_name"] for j in reg_data.get("judges", [])}

    for rec_id in NEW_IDS:
        m = ID_PAT.match(rec_id)
        assert m, f"bad id format: {rec_id}"
        year = int(m.group(1))
        court_code = m.group(2)
        num = int(m.group(3))

        json_path = ROOT / "records" / "judgments" / court_code / str(year) / f"{rec_id}.json"
        check(json_path.exists(), f"{rec_id}: file exists")
        if not json_path.exists():
            continue

        rec = json.loads(json_path.read_text())

        for f in REQUIRED_FIELDS:
            check(f in rec, f"{rec_id}: required field '{f}' present")

        check(rec["id"] == rec_id, f"{rec_id}: id matches filename")
        check(rec["type"] == "judgment", f"{rec_id}: type=judgment")
        check(rec["court"] == "Supreme Court of Zambia", f"{rec_id}: court is SCZ")
        check(len(rec["judges"]) >= 1, f"{rec_id}: at least one judge")
        for j in rec["judges"]:
            check(
                j["name"] in canonical_names,
                f"{rec_id}: judge '{j['name']}' resolves in canonical registry",
            )
        check(
            isinstance(rec["issue_tags"], list) and len(rec["issue_tags"]) >= 1,
            f"{rec_id}: issue_tags non-empty",
        )
        check(
            rec["outcome"] in ALLOWED_OUTCOMES,
            f"{rec_id}: outcome '{rec['outcome']}' in allowed enum",
        )
        check(
            rec["outcome_detail"] and len(rec["outcome_detail"]) > 0,
            f"{rec_id}: outcome_detail non-empty",
        )

        raw_year = ROOT / "raw" / "zambialii" / "judgments" / court_code / str(year)
        matching = list(
            raw_year.glob(f"judgment-zm-{year}-{court_code}-{num:02d}-*.pdf"),
        )
        check(
            len(matching) == 1,
            f"{rec_id}: exactly one matching raw PDF on disk (got {len(matching)})",
        )
        if len(matching) == 1:
            actual_sha = hashlib.sha256(matching[0].read_bytes()).hexdigest()
            check(
                rec["raw_sha256"] == actual_sha,
                f"{rec_id}: raw_sha256 matches on-disk PDF",
            )

        check(
            rec["source_url"].startswith("https://zambialii.org/akn/zm/judgment/zmsc/"),
            f"{rec_id}: source_url is ZambiaLII canonical",
        )

    # Duplicate-id check across whole corpus
    all_records_dir = ROOT / "records" / "judgments"
    all_ids = []
    for p in all_records_dir.rglob("*.json"):
        try:
            r = json.loads(p.read_text())
            all_ids.append(r["id"])
        except Exception:
            pass
    check(len(all_ids) == len(set(all_ids)),
          f"no duplicate ids in corpus (n={len(all_ids)}, uniq={len(set(all_ids))})")

    print(f"Integrity check b0523: {passed} passed / {failed} failed")
    if errors:
        for e in errors:
            print(f"  FAIL: {e}")
        sys.exit(1)
    print(f"Total records on disk: {len(all_ids)} unique IDs")


if __name__ == "__main__":
    main()
