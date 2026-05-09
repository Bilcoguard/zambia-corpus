#!/usr/bin/env python3
"""Batch 0553 integrity check.

Verifies:
- Each new record file unique by ID
- type == 'judgment', outcome in allowed enum
- issue_tags non-empty, judges non-empty
- All judge canonical names resolve in judges_registry.yaml
- raw_sha256 matches on-disk PDF
- corpus.sqlite contains the record in `records` and `judgments_meta`
- No duplicate IDs across full corpus
- For deferred records: raw HTML+PDF still on disk
"""
import hashlib
import json
import pathlib
import shutil
import sqlite3
import sys
import tempfile

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent

NEW_IDS = [
    "judgment-zm-2025-zmsc-04-minimart-development-corporation-company-limited-v",
    "judgment-zm-2025-zmsc-32-shaba-mulengela-and-anor-v-frank-mumba",
]

# Deferred raw-on-disk files this tick (no record written, but raw must exist).
DEFERRED = [
    {"court": "zmsc", "year": 2025, "num": 31},
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

    # Deferred raw-on-disk verification
    for d in DEFERRED:
        court = d["court"]; year = d["year"]; num = d["num"]
        rdir = ROOT / "raw" / "zambialii" / "judgments" / court / str(year)
        htmls = list(rdir.glob(f"judgment-zm-{year}-{court}-{num:02d}-*.html"))
        pdfs = list(rdir.glob(f"judgment-zm-{year}-{court}-{num:02d}-*.pdf"))
        if len(htmls) != 1:
            failures.append((f"{court}/{year}/{num}", f"deferred html count {len(htmls)}"))
        if len(pdfs) != 1:
            failures.append((f"{court}/{year}/{num}", f"deferred pdf count {len(pdfs)}"))

    all_ids = []
    for fp in (ROOT / "records" / "judgments").rglob("*.json"):
        all_ids.append(json.loads(fp.read_text())["id"])
    if len(all_ids) != len(set(all_ids)):
        failures.append(("corpus", "duplicate IDs detected"))

    # TMPDIR-routed atomic copy (b0519+ precedent) — read corpus.sqlite from
    # an off-FUSE temp copy to avoid sporadic FUSE I/O errors mid-tick.
    src = ROOT / "corpus.sqlite"
    with tempfile.TemporaryDirectory(prefix="b0553_check_") as tmp:
        tmp_db = pathlib.Path(tmp) / "corpus.sqlite"
        shutil.copy2(src, tmp_db)
        con = sqlite3.connect(str(tmp_db))
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
    print(f"INTEGRITY PASS: {len(NEW_IDS)} records + {len(DEFERRED)} deferred raw verified; corpus IDs unique ({len(all_ids)}).")


if __name__ == "__main__":
    main()
