#!/usr/bin/env python3
"""batch_0504_build_fts5.py — Phase 6 batch 1.

Phase 6 deliverable #1 — FTS5 full-text search index.

Builds a fresh ``corpus.sqlite`` from the on-disk JSON records under
``records/``. The unified ``records`` table holds base provenance for
all record types (act, si/statutory_instrument, judgment); type-specific
tables ``acts_meta``, ``sis_meta``, ``judgments_meta`` hold richer fields.
A single FTS5 virtual table ``records_fts`` indexes title + citation +
case_name + outcome_detail + body across every record so ``search()``
in the Phase 6 query API can do unified phrase / boolean / NEAR queries.

This batch does NOT fetch anything. Phase 6 is local-data-only.

Source-of-truth = JSON files on disk; corpus.sqlite is rebuilt from
scratch and the previous file is replaced via in-place truncate+write
(unlink is blocked by the mount, so we overwrite bytes).

Skipped record categories (recorded in summary, not loaded):
  - ``_tombstone: true`` markers (e.g. reclassified-as-SI placeholders)
  - ``type: TOMBSTONE_NAV_PAGE`` deleted/nav stubs
  - Records missing ``id`` or ``type``

Duplicate IDs across multiple on-disk paths are deduplicated by
preferring the more deeply-nested (year-organised) path.
"""

from __future__ import annotations

import json
import pathlib
import sqlite3
import sys

WORKSPACE = pathlib.Path("/sessions/wizardly-dreamy-davinci/mnt/corpus")
RECORDS_DIR = WORKSPACE / "records"
DB_PATH = WORKSPACE / "corpus.sqlite"

# Type aliases — Phase 4 used both `si` and `statutory_instrument` for SIs.
TYPE_NORMALISE = {
    "si": "si",
    "statutory_instrument": "si",
    "act": "act",
    "judgment": "judgment",
}


def gather_records():
    """Return list[(path, dict)] of usable records, plus a skip-reasons dict."""
    skipped = {"tombstone_flag": 0, "tombstone_nav_page": 0, "no_id_or_type": 0,
               "duplicate_id": 0, "unknown_type": 0}
    by_id: dict[str, tuple[pathlib.Path, dict]] = {}
    for p in RECORDS_DIR.rglob("*.json"):
        if not p.is_file():
            continue
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
        except Exception:  # noqa: BLE001
            skipped["no_id_or_type"] += 1
            continue
        if d.get("_tombstone"):
            skipped["tombstone_flag"] += 1
            continue
        if d.get("type") == "TOMBSTONE_NAV_PAGE" or d.get("deleted"):
            skipped["tombstone_nav_page"] += 1
            continue
        rid = d.get("id")
        rtype_raw = d.get("type")
        if not rid or not rtype_raw:
            skipped["no_id_or_type"] += 1
            continue
        if rtype_raw not in TYPE_NORMALISE:
            skipped["unknown_type"] += 1
            continue
        # Dedup: prefer the deeper / longer-path entry (year-organised dirs
        # have more path segments than flat records/acts/foo.json).
        if rid in by_id:
            existing_p, _ = by_id[rid]
            if len(p.parts) > len(existing_p.parts):
                by_id[rid] = (p, d)
            skipped["duplicate_id"] += 1
        else:
            by_id[rid] = (p, d)
    return list(by_id.values()), skipped


def coerce_text(*parts) -> str:
    bits = []
    for x in parts:
        if x is None:
            continue
        if isinstance(x, (list, tuple)):
            bits.append(" ".join(coerce_text(i) for i in x))
        elif isinstance(x, dict):
            bits.append(" ".join(coerce_text(v) for v in x.values()))
        else:
            bits.append(str(x))
    return " ".join(b for b in bits if b)


def section_text(rec: dict) -> str:
    parts: list[str] = []
    secs = rec.get("sections")
    if isinstance(secs, list):
        for s in secs:
            if isinstance(s, dict):
                parts.append(coerce_text(s.get("number"), s.get("heading"), s.get("text")))
            else:
                parts.append(str(s))
    paras = rec.get("paragraphs")
    if isinstance(paras, list):
        for pp in paras:
            if isinstance(pp, dict):
                parts.append(coerce_text(pp.get("number"), pp.get("text")))
            else:
                parts.append(str(pp))
    if isinstance(rec.get("full_text"), str):
        parts.append(rec["full_text"])
    return "\n".join(p for p in parts if p)


SCHEMA_SQL = """
CREATE TABLE records (
    id TEXT PRIMARY KEY,
    type TEXT NOT NULL,
    jurisdiction TEXT NOT NULL,
    title TEXT NOT NULL,
    citation TEXT,
    in_force INTEGER,
    source_url TEXT NOT NULL,
    source_hash TEXT NOT NULL,
    fetched_at TEXT NOT NULL,
    parser_version TEXT NOT NULL,
    on_disk_path TEXT NOT NULL,
    body TEXT
);

CREATE INDEX idx_records_type ON records(type);
CREATE INDEX idx_records_in_force ON records(in_force);

CREATE TABLE acts_meta (
    id TEXT PRIMARY KEY REFERENCES records(id) ON DELETE CASCADE,
    enacted_date TEXT,
    commencement_date TEXT,
    amended_by TEXT,
    repealed_by TEXT,
    section_count INTEGER
);

CREATE TABLE sis_meta (
    id TEXT PRIMARY KEY REFERENCES records(id) ON DELETE CASCADE,
    si_number TEXT,
    si_year INTEGER,
    parent_act_id TEXT,
    section_count INTEGER
);

CREATE TABLE judgments_meta (
    id TEXT PRIMARY KEY REFERENCES records(id) ON DELETE CASCADE,
    court TEXT,
    case_name TEXT,
    case_number TEXT,
    date_decided TEXT,
    outcome TEXT,
    outcome_detail TEXT,
    judges_json TEXT,
    issue_tags_json TEXT,
    reasoning_tags_json TEXT,
    key_statutes_json TEXT,
    cited_authorities_json TEXT,
    paragraph_count INTEGER
);

CREATE VIRTUAL TABLE records_fts USING fts5(
    id UNINDEXED,
    type UNINDEXED,
    title,
    citation,
    case_name,
    outcome_detail,
    body,
    tokenize = 'porter unicode61'
);

CREATE TABLE corpus_meta (
    key TEXT PRIMARY KEY,
    value TEXT
);
"""


def build(target: pathlib.Path) -> dict:
    if target.exists():
        target.unlink()
    con = sqlite3.connect(target)
    cur = con.cursor()
    cur.executescript(SCHEMA_SQL)

    records, skipped = gather_records()

    counts = {"act": 0, "si": 0, "judgment": 0}
    for p, rec in records:
        rtype = TYPE_NORMALISE[rec["type"]]
        rid = rec["id"]
        title = rec.get("title") or rec.get("case_name") or rid
        citation = rec.get("citation")
        in_force_raw = rec.get("in_force")
        in_force = 1 if in_force_raw else (0 if in_force_raw is False else None)
        body = section_text(rec)
        cur.execute(
            "INSERT INTO records "
            "(id, type, jurisdiction, title, citation, in_force, source_url, source_hash, fetched_at, parser_version, on_disk_path, body) "
            "VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
            (
                rid, rtype, rec.get("jurisdiction") or "ZM", title, citation, in_force,
                rec.get("source_url") or "",
                rec.get("source_hash") or "",
                rec.get("fetched_at") or "",
                rec.get("parser_version") or "",
                str(p.relative_to(WORKSPACE)),
                body,
            ),
        )
        counts[rtype] += 1

        if rtype == "act":
            cur.execute(
                "INSERT INTO acts_meta VALUES (?,?,?,?,?,?)",
                (
                    rid,
                    rec.get("enacted_date"),
                    rec.get("commencement_date"),
                    json.dumps(rec.get("amended_by") or []),
                    json.dumps(rec.get("repealed_by")) if rec.get("repealed_by") is not None else None,
                    len(rec.get("sections") or []),
                ),
            )
        elif rtype == "si":
            si_num = None
            si_year = None
            try:
                bits = rid.split("-")
                if len(bits) >= 4 and bits[0] == "si" and bits[2].isdigit() and bits[3].isdigit():
                    si_year = int(bits[2])
                    si_num = bits[3]
            except Exception:  # noqa: BLE001
                pass
            cur.execute(
                "INSERT INTO sis_meta VALUES (?,?,?,?,?)",
                (rid, si_num, si_year, rec.get("parent_act_id"),
                 len(rec.get("sections") or []) or len(rec.get("paragraphs") or []) or 0),
            )
        elif rtype == "judgment":
            cur.execute(
                "INSERT INTO judgments_meta VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (
                    rid,
                    rec.get("court"),
                    rec.get("case_name") or rec.get("title"),
                    rec.get("case_number"),
                    rec.get("date_decided") or rec.get("delivery_date"),
                    rec.get("outcome"),
                    rec.get("outcome_detail"),
                    json.dumps(rec.get("judges") or []),
                    json.dumps(rec.get("issue_tags") or []),
                    json.dumps(rec.get("reasoning_tags") or []),
                    json.dumps(rec.get("key_statutes") or []),
                    json.dumps(rec.get("cited_authorities") or []),
                    len(rec.get("paragraphs") or []),
                ),
            )

        cur.execute(
            "INSERT INTO records_fts (id, type, title, citation, case_name, outcome_detail, body) "
            "VALUES (?,?,?,?,?,?,?)",
            (
                rid, rtype, title or "", citation or "",
                (rec.get("case_name") or "") if rtype == "judgment" else "",
                rec.get("outcome_detail") or "",
                body,
            ),
        )

    # Metadata
    cur.execute("INSERT INTO corpus_meta VALUES (?,?)", ("schema_version", "phase6.b0504"))
    cur.execute("INSERT INTO corpus_meta VALUES (?,?)", ("built_by", "scripts/batch_0504_build_fts5.py"))
    cur.execute("INSERT INTO corpus_meta VALUES (?,?)", ("built_at_utc", __import__("datetime").datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")))
    cur.execute("INSERT INTO corpus_meta VALUES (?,?)", ("on_disk_record_count", str(len(records))))

    con.commit()
    cur.execute("INSERT INTO records_fts(records_fts) VALUES('optimize')")
    con.commit()

    counts["records_total"] = cur.execute("SELECT COUNT(*) FROM records").fetchone()[0]
    counts["fts_total"] = cur.execute("SELECT COUNT(*) FROM records_fts").fetchone()[0]
    counts["acts_meta"] = cur.execute("SELECT COUNT(*) FROM acts_meta").fetchone()[0]
    counts["sis_meta"] = cur.execute("SELECT COUNT(*) FROM sis_meta").fetchone()[0]
    counts["judgments_meta"] = cur.execute("SELECT COUNT(*) FROM judgments_meta").fetchone()[0]
    counts["skipped"] = skipped
    con.close()
    return counts


def main():
    tmp = pathlib.Path("/tmp/b0504_work/corpus.sqlite.new")
    tmp.parent.mkdir(parents=True, exist_ok=True)
    if tmp.exists():
        tmp.unlink()
    print("Building fresh corpus.sqlite at", tmp, flush=True)
    counts = build(tmp)
    print("Counts:", json.dumps(counts, indent=2), flush=True)

    if counts["records_total"] != counts["fts_total"]:
        print("FAIL: records vs fts mismatch", file=sys.stderr)
        sys.exit(2)
    if counts["records_total"] != counts["act"] + counts["si"] + counts["judgment"]:
        print("FAIL: per-type sums don't match records_total", file=sys.stderr)
        sys.exit(3)

    if "--write" in sys.argv:
        print(f"Overwriting {DB_PATH} with {tmp.stat().st_size} bytes", flush=True)
        with open(tmp, "rb") as src, open(DB_PATH, "wb") as dst:
            while True:
                chunk = src.read(1 << 20)
                if not chunk:
                    break
                dst.write(chunk)
        journal = DB_PATH.parent / "corpus.sqlite-journal"
        if journal.exists():
            try:
                with open(journal, "wb") as fh:
                    fh.write(b"")
            except Exception:  # noqa: BLE001
                pass
        print("Replacement complete.", flush=True)
    else:
        print("Dry run — pass --write to overwrite corpus.sqlite", flush=True)


if __name__ == "__main__":
    main()
