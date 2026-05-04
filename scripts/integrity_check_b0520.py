#!/usr/bin/env python3
"""Integrity check b0520 — judgment-ingestion-worker tick.

Validates the 2 ZMSC 2023 records written this tick (nums 14, 11)
pass the seven required checks from the SKILL.md non-negotiables:
  1. Every judgment has at least one judge
  2. issue_tags non-empty
  3. outcome from allowed enum
  4. All judges[].name resolve in judges_registry.yaml
  5. No duplicate IDs in corpus
  6. raw_sha256 matches on-disk file
  7. Required schema fields all present

Plus identity/format checks: id, type, court, source_url shape.
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
    "judgment-zm-2023-zmsc-14-k-v-wheels-and-construction-ltd-v-investrust-bank",
    "judgment-zm-2023-zmsc-11-kakunda-and-ors-v-the-people",
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

    # Corpus-wide duplicate-id check
    all_ids = []
    for jp in (ROOT / "records" / "judgments").rglob("*.json"):
        try:
            rj = json.loads(jp.read_text())
            all_ids.append(rj["id"])
        except Exception:
            pass
    check(
        len(all_ids) == len(set(all_ids)),
        f"corpus-wide: no duplicate judgment IDs (n={len(all_ids)} ids, "
        f"{len(set(all_ids))} unique)",
    )

    print(f"PASSED: {passed}")
    print(f"FAILED: {failed}")
    if errors:
        print("ERRORS:")
        for e in errors:
            print(f"  - {e}")
    print(f"Total judgment records on disk: {len(all_ids)}")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
