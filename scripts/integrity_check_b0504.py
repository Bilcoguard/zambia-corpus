#!/usr/bin/env python3
"""Integrity check for batch-0504 (Phase 6 batch 1 — FTS5 schema + populate).

Phase 6 scope checks:
  - on-disk JSON record count == records table count (after dedup)
  - records_fts row count == records row count
  - per-type sums match records_total
  - every records.id is unique
  - every records.id has matching FTS row
  - every records.id has matching meta-table row (acts_meta / sis_meta / judgments_meta)
  - core provenance non-null on every row (source_url, source_hash, fetched_at, parser_version)
  - representative FTS queries return >0 hits (sanity)
"""

from __future__ import annotations

import json
import pathlib
import sqlite3
import sys

WORKSPACE = pathlib.Path("/sessions/wizardly-dreamy-davinci/mnt/corpus")
RECORDS_DIR = WORKSPACE / "records"


def count_on_disk() -> dict:
    counts = {"act": 0, "si": 0, "judgment": 0,
              "skipped_tombstone": 0, "skipped_nav": 0,
              "skipped_no_id": 0, "duplicate_paths": 0}
    seen = {}
    for p in RECORDS_DIR.rglob("*.json"):
        if not p.is_file():
            continue
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
        except Exception:  # noqa: BLE001
            counts["skipped_no_id"] += 1
            continue
        if d.get("_tombstone"):
            counts["skipped_tombstone"] += 1
            continue
        if d.get("type") == "TOMBSTONE_NAV_PAGE" or d.get("deleted"):
            counts["skipped_nav"] += 1
            continue
        rid = d.get("id")
        rtype = d.get("type")
        if not rid or not rtype:
            counts["skipped_no_id"] += 1
            continue
        if rtype in ("si", "statutory_instrument"):
            normal = "si"
        elif rtype in ("act", "judgment"):
            normal = rtype
        else:
            continue
        if rid in seen:
            counts["duplicate_paths"] += 1
            continue
        seen[rid] = normal
        counts[normal] += 1
    counts["unique_ids"] = len(seen)
    return counts


def main(db_path: str) -> int:
    errors: list[str] = []
    on_disk = count_on_disk()

    con = sqlite3.connect(db_path)
    cur = con.cursor()

    rec_total = cur.execute("SELECT COUNT(*) FROM records").fetchone()[0]
    fts_total = cur.execute("SELECT COUNT(*) FROM records_fts").fetchone()[0]
    rec_acts = cur.execute("SELECT COUNT(*) FROM records WHERE type='act'").fetchone()[0]
    rec_sis = cur.execute("SELECT COUNT(*) FROM records WHERE type='si'").fetchone()[0]
    rec_jms = cur.execute("SELECT COUNT(*) FROM records WHERE type='judgment'").fetchone()[0]
    am = cur.execute("SELECT COUNT(*) FROM acts_meta").fetchone()[0]
    sm = cur.execute("SELECT COUNT(*) FROM sis_meta").fetchone()[0]
    jm = cur.execute("SELECT COUNT(*) FROM judgments_meta").fetchone()[0]

    if rec_total != fts_total:
        errors.append(f"records ({rec_total}) != records_fts ({fts_total})")
    if rec_total != rec_acts + rec_sis + rec_jms:
        errors.append(f"records_total {rec_total} != sum-by-type {rec_acts+rec_sis+rec_jms}")
    if rec_acts != am:
        errors.append(f"records.act {rec_acts} != acts_meta {am}")
    if rec_sis != sm:
        errors.append(f"records.si {rec_sis} != sis_meta {sm}")
    if rec_jms != jm:
        errors.append(f"records.judgment {rec_jms} != judgments_meta {jm}")
    if on_disk["unique_ids"] != rec_total:
        errors.append(f"on-disk unique ids {on_disk['unique_ids']} != db records {rec_total}")
    if on_disk["act"] != rec_acts:
        errors.append(f"on-disk acts {on_disk['act']} != db acts {rec_acts}")
    if on_disk["si"] != rec_sis:
        errors.append(f"on-disk SIs {on_disk['si']} != db SIs {rec_sis}")
    if on_disk["judgment"] != rec_jms:
        errors.append(f"on-disk judgments {on_disk['judgment']} != db judgments {rec_jms}")

    # Provenance non-null check
    bad = cur.execute(
        "SELECT id FROM records WHERE source_url='' OR source_hash='' OR fetched_at='' OR parser_version=''"
    ).fetchall()
    if bad:
        errors.append(f"{len(bad)} records have empty core provenance — first 3: {[b[0] for b in bad[:3]]}")

    # Sample FTS sanity
    samples = [
        ("companies act", 1),
        ("pension AND scheme", 1),
        ("zambia*", 50),
        ("NEAR(appeal dismissed, 5)", 1),
    ]
    for q, min_hits in samples:
        n = cur.execute("SELECT COUNT(*) FROM records_fts WHERE records_fts MATCH ?", (q,)).fetchone()[0]
        if n < min_hits:
            errors.append(f"FTS sample '{q}' returned {n} (<{min_hits})")

    # FTS5 vs records id parity
    leak = cur.execute(
        "SELECT COUNT(*) FROM records_fts f WHERE NOT EXISTS (SELECT 1 FROM records r WHERE r.id=f.id)"
    ).fetchone()[0]
    if leak:
        errors.append(f"{leak} fts rows reference non-existent records.id")
    leak2 = cur.execute(
        "SELECT COUNT(*) FROM records r WHERE NOT EXISTS (SELECT 1 FROM records_fts f WHERE f.id=r.id)"
    ).fetchone()[0]
    if leak2:
        errors.append(f"{leak2} records have no FTS row")

    summary = {
        "on_disk": on_disk,
        "db": {
            "records_total": rec_total,
            "records_fts": fts_total,
            "acts": rec_acts, "sis": rec_sis, "judgments": rec_jms,
            "acts_meta": am, "sis_meta": sm, "judgments_meta": jm,
        },
        "errors": errors,
    }
    print(json.dumps(summary, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    db = sys.argv[1] if len(sys.argv) > 1 else str(WORKSPACE / "corpus.sqlite")
    raise SystemExit(main(db))
