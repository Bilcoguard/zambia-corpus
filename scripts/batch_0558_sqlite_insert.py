#!/usr/bin/env python3
"""Batch 0558 — insert this tick's 2 ZMCC 2020 records into corpus.sqlite.

Updates `records`, `judgments_meta`, AND `records_fts` (per b0557 strict
assertion: records == records_fts). Uses TMPDIR-routed atomic copy
(b0531 pattern) and PRAGMA journal_mode=TRUNCATE (b0557 workaround for
virtiofs unlink restriction).

Idempotent: INSERT OR REPLACE on records/judgments_meta; for records_fts
we DELETE WHERE id=? then INSERT (FTS5 doesn't support REPLACE).
"""
import json
import pathlib
import shutil
import sqlite3
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent

NEW_IDS = [
    "judgment-zm-2020-zmcc-02-kambwili-v-attorney-general",
    "judgment-zm-2020-zmcc-03-dean-masule-v-kangombe",
]


def insert_into_db(db_path):
    conn = sqlite3.connect(str(db_path))
    cur = conn.cursor()
    # b0557 workaround for virtiofs DELETE journal unlink failure
    cur.execute("PRAGMA journal_mode = TRUNCATE")

    n_records_before = cur.execute("SELECT count(*) FROM records").fetchone()[0]
    n_meta_before = cur.execute("SELECT count(*) FROM judgments_meta").fetchone()[0]
    n_fts_before = cur.execute("SELECT count(*) FROM records_fts").fetchone()[0]

    inserted = 0
    for rec_id in NEW_IDS:
        parts = rec_id.split("-")
        # parts: judgment-zm-{year}-{court}-{num:02d}-{slug...}
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
        # records_fts: delete-then-insert (FTS5 lacks REPLACE)
        cur.execute("DELETE FROM records_fts WHERE id = ?", (rec_id,))
        cur.execute(
            """INSERT INTO records_fts (id, type, title, citation, case_name, outcome_detail, body)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (
                rec["id"], rec["type"], rec["title"], rec["citation"],
                rec["case_name"], rec["outcome_detail"], None,
            ),
        )
        # Per-record commit (b0557 belt-and-braces precaution for virtiofs)
        conn.commit()
        inserted += 1
        print(f"INSERT: {rec_id}")

    n_records_after = cur.execute("SELECT count(*) FROM records").fetchone()[0]
    n_meta_after = cur.execute("SELECT count(*) FROM judgments_meta").fetchone()[0]
    n_fts_after = cur.execute("SELECT count(*) FROM records_fts").fetchone()[0]
    integ = cur.execute("PRAGMA integrity_check").fetchone()[0]
    print(f"records: {n_records_before} -> {n_records_after} (+{n_records_after - n_records_before})")
    print(f"judgments_meta: {n_meta_before} -> {n_meta_after} (+{n_meta_after - n_meta_before})")
    print(f"records_fts: {n_fts_before} -> {n_fts_after} (+{n_fts_after - n_fts_before})")
    print(f"integrity_check: {integ}")
    conn.close()
    return {
        "records_before": n_records_before, "records_after": n_records_after,
        "meta_before": n_meta_before, "meta_after": n_meta_after,
        "fts_before": n_fts_before, "fts_after": n_fts_after,
        "integrity": integ, "inserted": inserted,
    }


def main():
    src = ROOT / "corpus.sqlite"
    with tempfile.TemporaryDirectory(prefix="b0558_sqlite_") as tmp:
        tmp_db = pathlib.Path(tmp) / "corpus.sqlite"
        shutil.copy2(src, tmp_db)
        result = insert_into_db(tmp_db)
        shutil.copy2(tmp_db, src)
    print("DB sync complete via TMPDIR-routed atomic copy")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
