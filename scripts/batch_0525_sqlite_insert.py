#!/usr/bin/env python3
"""Batch 0525 — insert this tick's 4 ZMSC 2022 records into corpus.sqlite.

Idempotent: uses INSERT OR REPLACE so re-runs are safe.
Updates `records` and `judgments_meta`. records_fts left to host-side rebuild
(scripts/batch_0504_build_fts5.py) per b0517 precedent.
"""
import json
import pathlib
import shutil
import sqlite3
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent

NEW_IDS = [
    "judgment-zm-2022-zmsc-45-abel-chipemba-v-the-people",
    "judgment-zm-2022-zmsc-42-chimanga-changa-ltd-v-export-trading-ltd",
    "judgment-zm-2022-zmsc-40-zambian-breweries-plc-v-maritime-freight-and-forwa",
    "judgment-zm-2022-zmsc-39-teal-minerals-barbados-incorporated-v-zambia-reven",
]


def insert_into_db(db_path):
    conn = sqlite3.connect(str(db_path))
    cur = conn.cursor()

    n_records_before = cur.execute("SELECT count(*) FROM records").fetchone()[0]
    n_meta_before = cur.execute("SELECT count(*) FROM judgments_meta").fetchone()[0]

    inserted = 0
    for rec_id in NEW_IDS:
        parts = rec_id.split("-")
        year = parts[2]
        court = parts[3]
        json_path = ROOT / "records" / "judgments" / court / year / f"{rec_id}.json"
        rec = json.loads(json_path.read_text())

        cur.execute(
            """INSERT OR REPLACE INTO records
               (id, type, jurisdiction, title, citation, in_force,
                source_url, source_hash, fetched_at, parser_version,
                on_disk_path, body)
               VALUES (?, ?, ?, ?, ?, NULL, ?, ?, ?, ?, ?, NULL)""",
            (
                rec["id"], rec["type"], rec["jurisdiction"], rec["title"],
                rec["citation"], rec["source_url"], rec["source_hash"],
                rec["fetched_at"], rec["parser_version"],
                f"records/judgments/{court}/{year}/{rec_id}.json",
            ),
        )
        cur.execute(
            """INSERT OR REPLACE INTO judgments_meta
               (id, court, case_name, case_number, date_decided,
                outcome, outcome_detail, judges_json, issue_tags_json,
                reasoning_tags_json, key_statutes_json,
                cited_authorities_json, paragraph_count)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, NULL)""",
            (
                rec["id"], rec["court"], rec["case_name"],
                rec["case_number"], rec["date_decided"],
                rec["outcome"], rec["outcome_detail"],
                json.dumps(rec["judges"]),
                json.dumps(rec["issue_tags"]),
                json.dumps(rec.get("reasoning_tags", [])),
                json.dumps(rec.get("key_statutes", [])),
                json.dumps([]),
            ),
        )
        inserted += 1
        print(f"INSERT: {rec_id}")

    conn.commit()
    n_records_after = cur.execute("SELECT count(*) FROM records").fetchone()[0]
    n_meta_after = cur.execute("SELECT count(*) FROM judgments_meta").fetchone()[0]
    conn.close()

    print(f"records: {n_records_before} -> {n_records_after} (+{n_records_after - n_records_before})")
    print(f"judgments_meta: {n_meta_before} -> {n_meta_after} (+{n_meta_after - n_meta_before})")
    print(f"inserted/replaced this run: {inserted}")
    return n_records_before, n_records_after, n_meta_before, n_meta_after


def main():
    """Use TMPDIR-routed atomic copy pattern (b0519/b0520/b0521/b0522/b0523
    precedent) to avoid FUSE journal cleanup errors when writing to in-place
    corpus.sqlite on the FUSE-mount. Steps:
      1. copy corpus.sqlite -> tmp_db
      2. open tmp_db, do INSERT OR REPLACE writes, commit
      3. close, then atomic copy tmp_db back -> corpus.sqlite
    """
    src = ROOT / "corpus.sqlite"
    with tempfile.TemporaryDirectory(prefix="b0525_sqlite_") as tmp:
        tmp_db = pathlib.Path(tmp) / "corpus.sqlite"
        shutil.copy2(src, tmp_db)
        n_rb, n_ra, n_mb, n_ma = insert_into_db(tmp_db)
        # atomic copy back
        shutil.copy2(tmp_db, src)
    print("DB sync complete via TMPDIR-routed atomic copy")
    return n_rb, n_ra, n_mb, n_ma


if __name__ == "__main__":
    main()
