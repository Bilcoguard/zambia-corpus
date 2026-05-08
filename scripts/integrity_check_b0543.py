#!/usr/bin/env python3
"""Batch 0543 integrity check.

Verifies:
- Each new record file unique by ID
- type == 'judgment', outcome in allowed enum
- issue_tags non-empty, judges non-empty
- All judge canonical names resolve in judges_registry.yaml
- raw_sha256 matches on-disk PDF
- corpus.sqlite contains the record in `records` and `judgments_meta`
- No duplicate IDs across full corpus
"""
import hashlib
import json
import pathlib
import sqlite3
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent

NEW_IDS = [
    "judgment-zm-2020-zmsc-51-richard-h-chama-213-other-v-national-pension-schem",
    "judgment-zm-2020-zmsc-60-matias-chitigwa-mugogo-v-the-people",
    "judgment-zm-2020-zmsc-65-jackson-kamanga-others-v-the-people",
]

ALLOWED_OUTCOMES = {
    "allowed", "dismissed", "upheld", "overturned", "remitted",
    "struck-out", "withdrawn", "granted", "refused", "set-aside",
    "quashed", "other",
}


def main():
    reg = yaml.safe_load((ROOT / "judges_registry.yaml").read_text())
    canonical_names = {j["canonical_name"] for j in reg["judges"]}

    failures = []
    for rid in NEW_IDS:
        fps = list((ROOT / "records" / "judgments").rglob(f"{rid}.json"))
        if len(fps) != 1:
            failures.append((rid, f"unique-id check failed: {len(fps)} files"))
            continue
        rec = json.loads(fps[0].read_text())
        if rec["type"] != "judgment":
            failures.append((rid, f"bad type {rec['type']}"))
        if rec["outcome"] not in ALLOWED_OUTCOMES:
            failures.append((rid, f"bad outcome {rec['outcome']}"))
        if not rec["issue_tags"]:
            failures.append((rid, "empty issue_tags"))
        if not rec["judges"]:
            failures.append((rid, "no judges"))
        for j in rec["judges"]:
            if j["name"] not in canonical_names:
                failures.append((rid, f"judge {j['name']} not in registry"))
        pdfs = list((ROOT / "raw" / "zambialii" / "judgments").rglob(f"{rid}.pdf"))
        if len(pdfs) != 1:
            failures.append((rid, f"on-disk pdf check failed: {len(pdfs)} files"))
            continue
        actual_sha = hashlib.sha256(pdfs[0].read_bytes()).hexdigest()
        if actual_sha != rec["raw_sha256"]:
            failures.append((rid, f"raw_sha256 mismatch: {actual_sha} vs {rec['raw_sha256']}"))

    all_ids = []
    for fp in (ROOT / "records" / "judgments").rglob("*.json"):
        all_ids.append(json.loads(fp.read_text())["id"])
    if len(all_ids) != len(set(all_ids)):
        failures.append(("corpus", "duplicate IDs detected"))

    con = sqlite3.connect(str(ROOT / "corpus.sqlite"))
    cur = con.cursor()
    for rid in NEW_IDS:
        if not cur.execute("SELECT id FROM records WHERE id=?", (rid,)).fetchone():
            failures.append((rid, "missing in records"))
        if not cur.execute("SELECT id FROM judgments_meta WHERE id=?", (rid,)).fetchone():
            failures.append((rid, "missing in judgments_meta"))
    con.close()

    if failures:
        print("INTEGRITY FAIL:")
        for rid, msg in failures:
            print(f"  {rid}: {msg}")
        sys.exit(1)
    print(f"INTEGRITY PASS: {len(NEW_IDS)} records examined; corpus IDs unique ({len(all_ids)}).")


if __name__ == "__main__":
    main()
