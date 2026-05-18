"""batch_0698_jiw_insert.py — Insertion phase for JIW b0698 tick.

Writes 8 ZMCC 2024 records to records/judgments/zmcc/2024/*.json AND inserts
into corpus.sqlite (records + records_fts) atomically. Direct in-place
mutation per b0696 methodology (PRAGMA journal_mode=MEMORY; synchronous=OFF).
"""
from __future__ import annotations

import datetime as dt
import json
import shutil
import sqlite3
import sys
from pathlib import Path

REPO = Path("/sessions/keen-pensive-davinci/mnt/corpus")
PARSED = REPO / "scripts/_b0698_jiw_parsed.json"
DB_PATH = REPO / "corpus.sqlite"
OUT_DIR = REPO / "records/judgments/zmcc/2024"

BATCH_ID = "b0698-jiw"
NOW = "2026-05-18T14:05:00Z"


def main():
    data = json.loads(PARSED.read_text())
    records = data["records"]
    deferred = data["deferred"]
    if not records:
        print("No records to insert.")
        return

    # Backup DB before mutation
    snapshot = DB_PATH.with_suffix(
        f".sqlite.bak.{BATCH_ID}-pre-"
        + dt.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    )
    shutil.copy2(DB_PATH, snapshot)
    print(f"DB snapshot: {snapshot.name}")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    written = []
    for r in records:
        # Strip internal underscore fields and write canonical JSON record
        clean = {k: v for k, v in r.items() if not k.startswith("_")}
        out_file = OUT_DIR / f"{r['id']}.json"
        out_file.write_text(json.dumps(clean, indent=2, ensure_ascii=False))
        written.append((r, out_file))
        print(f"WROTE {out_file.relative_to(REPO)}")

    # Insert into sqlite — records table + records_fts (FTS5 external content)
    con = sqlite3.connect(str(DB_PATH))
    con.execute("PRAGMA journal_mode=MEMORY;")
    con.execute("PRAGMA synchronous=OFF;")
    cur = con.cursor()

    for r, out_file in written:
        # Build the body field — composite searchable text:
        # case_name, citation, judges, outcome_detail, issue_tags, key statutes,
        # and the original PDF excerpts so FTS can match operative wording.
        body_parts = [
            r.get("title", ""),
            r.get("case_name", ""),
            r.get("citation", ""),
            r.get("court", ""),
            f"Case number: {r.get('case_number','')}",
            f"Date decided: {r.get('date_decided','')}",
            "Judges: " + "; ".join(j.get("name", "") for j in r.get("judges", [])),
            "Issue tags: " + "; ".join(r.get("issue_tags") or []),
            f"Outcome: {r.get('outcome','')}",
            r.get("outcome_detail", ""),
            r.get("_body_excerpt_first", ""),
            r.get("_body_excerpt_last", ""),
        ]
        body = "\n\n".join(p for p in body_parts if p)

        on_disk_path = str(out_file.relative_to(REPO))

        cur.execute(
            """INSERT INTO records (
                id, type, jurisdiction, title, citation, in_force,
                source_url, source_hash, fetched_at, parser_version,
                on_disk_path, body
            ) VALUES (?, ?, ?, ?, ?, NULL, ?, ?, ?, ?, ?, ?)""",
            (
                r["id"],
                r["type"],
                r["jurisdiction"],
                r["title"],
                r["citation"],
                r["source_url"],
                r["source_hash"],
                r["fetched_at"],
                r["parser_version"],
                on_disk_path,
                body,
            ),
        )
        # FTS5 with external content syncs via rowid; insert rowid->id mapping
        rowid = cur.lastrowid
        cur.execute(
            """INSERT INTO records_fts (rowid, id, title, body, citation, type)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (rowid, r["id"], r["title"], body, r["citation"], r["type"]),
        )
        print(f"  INSERT rowid={rowid} id={r['id']}")

    con.commit()
    # Integrity self-check
    rc = cur.execute("SELECT COUNT(*) FROM records").fetchone()[0]
    fc = cur.execute("SELECT COUNT(*) FROM records_fts").fetchone()[0]
    qc = cur.execute("PRAGMA quick_check;").fetchone()[0]
    ic = cur.execute("PRAGMA integrity_check;").fetchone()[0]
    print(f"\nDB after insert: records={rc} records_fts={fc} quick_check={qc} integrity_check={ic}")
    con.close()

    print(
        f"\nINSERT_COMPLETE batch={BATCH_ID} records={len(written)} deferred={len(deferred)} time={NOW}"
    )


if __name__ == "__main__":
    main()
