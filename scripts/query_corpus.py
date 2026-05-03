#!/usr/bin/env python3
"""query_corpus.py — Phase 6 deliverable #3: Retrieval API.

A read-only Python module + CLI for querying the Zambian Authorities Corpus
built by Phases 4-5 of the worker. All data is sourced from
``corpus.sqlite`` (FTS5 index built in batch 0504; citations table built in
batch 0505). The DB is rebuildable from on-disk JSON records (the
canonical source-of-truth) plus ``citations.jsonl`` — see
``scripts/batch_0504_build_fts5.py`` and
``scripts/batch_0505_build_citations.py``.

Public API (per BRIEF.md Phase 6 deliverable #3):

* ``search(query, type=None, court=None, year_from=None, year_to=None,
            limit=50)`` -> ``list[dict]``
    Full-text search via the ``records_fts`` FTS5 virtual table. Supports
    SQLite FTS5 syntax (phrase quotes, AND/OR/NOT, NEAR(), prefix*).

* ``get_by_id(record_id)`` -> ``dict | None``
    Full record (base + type-specific meta merged). None when no match.

* ``citations_of(record_id)`` -> ``list[dict]``
    Records that CITE the given record (i.e. rows where
    ``citations.dst_id == record_id``).

* ``cited_by(record_id)`` -> ``list[dict]``
    Records that the given record CITES (i.e. rows where
    ``citations.src_id == record_id``).

* ``judge_profile(judge_name)`` -> ``dict``
    All judgments where ``judges_meta.judges_json`` mentions
    ``judge_name`` (case-insensitive substring match against the canonical
    ``name`` field of each entry). Returns ``judgments`` (list[dict]),
    ``outcome_counts`` (dict[str,int]) and ``total`` (int).

* ``statute_interpretation(act_id)`` -> ``list[dict]``
    All judgments whose ``judgments_meta.key_statutes_json`` references
    the given ``act_id``. The Phase 5 parser frequently leaves
    ``key_statutes`` empty — when that's the case for the whole corpus
    this function returns an empty list cleanly.

CLI usage:

    python scripts/query_corpus.py search "companies act"
    python scripts/query_corpus.py search "pension AND scheme" --type act
    python scripts/query_corpus.py get act-zm-2017-010-companies
    python scripts/query_corpus.py citations-of act-zm-2017-010-companies
    python scripts/query_corpus.py cited-by jud-...
    python scripts/query_corpus.py judge "Mwanamwambwa"
    python scripts/query_corpus.py statute-interpretation act-zm-2017-010-companies

Output is JSON on stdout (one document per call) so downstream
consumers can pipe into ``jq``. ``--limit`` caps result lists; the
default of 50 mirrors a typical legal-research result page.

Phase 6 is local-data-only: this module never makes a network call.
"""

from __future__ import annotations

import argparse
import json
import os
import pathlib
import sqlite3
import sys
from typing import Any, Iterable, Optional

WORKSPACE = pathlib.Path(__file__).resolve().parent.parent
DB_PATH = WORKSPACE / "corpus.sqlite"

PARSER_VERSION = "query_corpus.v1.0"
DEFAULT_LIMIT = 50

# ---------------------------------------------------------------------------
# Connection helpers
# ---------------------------------------------------------------------------


def _connect(db_path: Optional[pathlib.Path] = None) -> sqlite3.Connection:
    """Open the corpus DB read-only.

    Uses ``mode=ro&immutable=1`` so concurrent writers (e.g. an active
    judgment-ingestion-worker tick) cannot corrupt this query session, and
    so we never accidentally mutate the source-of-truth.
    """
    p = db_path if db_path is not None else DB_PATH
    if not p.exists():
        raise FileNotFoundError(
            f"corpus.sqlite not found at {p}. Rebuild via "
            "`python scripts/batch_0504_build_fts5.py` then "
            "`python scripts/batch_0505_build_citations.py`."
        )
    uri = f"file:{p}?mode=ro&immutable=1"
    conn = sqlite3.connect(uri, uri=True)
    conn.row_factory = sqlite3.Row
    return conn


def _row_to_dict(row: sqlite3.Row) -> dict:
    """Convert a sqlite3.Row to a plain dict."""
    return {k: row[k] for k in row.keys()}


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _records_by_ids(
    conn: sqlite3.Connection, ids: Iterable[str]
) -> list[dict]:
    """Look up base ``records`` rows for the given ids, preserving order."""
    ids = list(ids)
    if not ids:
        return []
    # Build placeholders. SQLite handles ~999 max; we chunk if needed.
    out: dict[str, dict] = {}
    chunk = 500
    for i in range(0, len(ids), chunk):
        sl = ids[i : i + chunk]
        placeholders = ",".join("?" for _ in sl)
        cur = conn.execute(
            "SELECT id, type, jurisdiction, title, citation, in_force, "
            "source_url, source_hash, fetched_at, parser_version, on_disk_path "
            f"FROM records WHERE id IN ({placeholders})",
            sl,
        )
        for r in cur.fetchall():
            out[r["id"]] = _row_to_dict(r)
    # Preserve incoming ID order
    return [out[i] for i in ids if i in out]


def _attach_meta(conn: sqlite3.Connection, rec: dict) -> dict:
    """Attach type-specific meta fields (acts_meta / sis_meta / judgments_meta)."""
    rid = rec["id"]
    t = rec["type"]
    if t == "act":
        m = conn.execute(
            "SELECT enacted_date, commencement_date, amended_by, repealed_by, "
            "section_count FROM acts_meta WHERE id=?",
            (rid,),
        ).fetchone()
        if m:
            rec.update(_row_to_dict(m))
    elif t == "si":
        m = conn.execute(
            "SELECT si_number, si_year, parent_act_id, section_count "
            "FROM sis_meta WHERE id=?",
            (rid,),
        ).fetchone()
        if m:
            rec.update(_row_to_dict(m))
    elif t == "judgment":
        m = conn.execute(
            "SELECT court, case_name, case_number, date_decided, outcome, "
            "outcome_detail, judges_json, issue_tags_json, reasoning_tags_json, "
            "key_statutes_json, cited_authorities_json, paragraph_count "
            "FROM judgments_meta WHERE id=?",
            (rid,),
        ).fetchone()
        if m:
            d = _row_to_dict(m)
            # Decode the JSON-encoded list fields for convenience.
            for k in (
                "judges_json",
                "issue_tags_json",
                "reasoning_tags_json",
                "key_statutes_json",
                "cited_authorities_json",
            ):
                v = d.pop(k)
                key = k[: -len("_json")]  # strip suffix
                try:
                    d[key] = json.loads(v) if v else []
                except (ValueError, TypeError):
                    d[key] = []
            rec.update(d)
    return rec


def _date_year(date_str: Optional[str]) -> Optional[int]:
    """Return the year from a YYYY-MM-DD style string, else None."""
    if not date_str:
        return None
    try:
        return int(str(date_str)[:4])
    except (ValueError, TypeError):
        return None


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def search(
    query: str,
    type: Optional[str] = None,
    court: Optional[str] = None,
    year_from: Optional[int] = None,
    year_to: Optional[int] = None,
    limit: int = DEFAULT_LIMIT,
    *,
    db_path: Optional[pathlib.Path] = None,
) -> list[dict]:
    """Full-text search the corpus via the FTS5 ``records_fts`` table.

    Args:
        query: An FTS5 query string (phrase quotes, AND/OR/NOT, NEAR(), *
            prefix all supported).
        type: Optional record type filter — one of {"act", "si", "judgment"}.
        court: Optional court filter (judgments only) — substring match,
            case-insensitive.
        year_from: Optional inclusive lower bound on the record's effective
            year (acts: enacted_date, sis: si_year, judgments: date_decided).
        year_to: Optional inclusive upper bound on the same effective year.
        limit: Maximum number of results.

    Returns:
        A list of result dicts, each containing the base ``records`` row
        plus the type-specific meta fields and an ``rank`` score.
        Results are ordered by FTS5 ``bm25(records_fts)``.
    """
    if not query or not str(query).strip():
        return []
    conn = _connect(db_path)
    try:
        # FTS5 returns rowid (==records.id via the UNINDEXED 'id' column)
        # so we join back to records on records_fts.id.
        sql = (
            "SELECT records_fts.id AS id, bm25(records_fts) AS rank "
            "FROM records_fts WHERE records_fts MATCH ? "
            "ORDER BY rank LIMIT ?"
        )
        # Pull a generous candidate pool then post-filter; FTS5 doesn't let us
        # join on type/year inside the MATCH expression cheaply.
        candidate_pool = max(int(limit) * 10, int(limit), 200)
        rows = conn.execute(sql, (query, candidate_pool)).fetchall()
        ids = [r["id"] for r in rows]
        rank_by_id = {r["id"]: r["rank"] for r in rows}
        recs = _records_by_ids(conn, ids)
        out: list[dict] = []
        for rec in recs:
            if type and rec.get("type") != type:
                continue
            rec = _attach_meta(conn, rec)
            if court and rec.get("type") == "judgment":
                c = (rec.get("court") or "").lower()
                if court.lower() not in c:
                    continue
            yr = None
            if rec.get("type") == "act":
                yr = _date_year(rec.get("enacted_date"))
            elif rec.get("type") == "si":
                yr = rec.get("si_year")
                if yr is None:
                    yr = _date_year(rec.get("citation"))
            elif rec.get("type") == "judgment":
                yr = _date_year(rec.get("date_decided"))
            if year_from is not None and (yr is None or yr < year_from):
                continue
            if year_to is not None and (yr is None or yr > year_to):
                continue
            rec["rank"] = rank_by_id.get(rec["id"])
            out.append(rec)
            if len(out) >= int(limit):
                break
        return out
    finally:
        conn.close()


def get_by_id(record_id: str, *, db_path: Optional[pathlib.Path] = None) -> Optional[dict]:
    """Look up a single record by id; merge in its type-specific meta.

    Returns ``None`` if the id does not exist in the corpus.
    """
    if not record_id:
        return None
    conn = _connect(db_path)
    try:
        recs = _records_by_ids(conn, [record_id])
        if not recs:
            return None
        return _attach_meta(conn, recs[0])
    finally:
        conn.close()


def citations_of(record_id: str, *, db_path: Optional[pathlib.Path] = None) -> list[dict]:
    """Records that cite ``record_id`` (i.e. inbound edges).

    Returns each citing record (full base + meta) plus an extra
    ``relation`` key indicating the edge label.
    """
    if not record_id:
        return []
    conn = _connect(db_path)
    try:
        rows = conn.execute(
            "SELECT src_id, relation, source_field FROM citations "
            "WHERE dst_id=? ORDER BY relation, src_id",
            (record_id,),
        ).fetchall()
        if not rows:
            return []
        ids = [r["src_id"] for r in rows]
        relation_by = {(r["src_id"], r["relation"]): r["relation"] for r in rows}
        recs = _records_by_ids(conn, ids)
        out: list[dict] = []
        for rec in recs:
            rec = _attach_meta(conn, rec)
            # Attach the first matching relation; a record may appear with multiple.
            for r in rows:
                if r["src_id"] == rec["id"]:
                    rec["relation"] = r["relation"]
                    rec["source_field"] = r["source_field"]
                    break
            out.append(rec)
        return out
    finally:
        conn.close()


def cited_by(record_id: str, *, db_path: Optional[pathlib.Path] = None) -> list[dict]:
    """Records that ``record_id`` cites (i.e. outbound edges).

    Returns each cited record (full base + meta) plus ``relation`` /
    ``source_field`` keys describing how the edge was harvested.
    """
    if not record_id:
        return []
    conn = _connect(db_path)
    try:
        rows = conn.execute(
            "SELECT dst_id, relation, source_field FROM citations "
            "WHERE src_id=? ORDER BY relation, dst_id",
            (record_id,),
        ).fetchall()
        if not rows:
            return []
        ids = [r["dst_id"] for r in rows]
        recs = _records_by_ids(conn, ids)
        out: list[dict] = []
        for rec in recs:
            rec = _attach_meta(conn, rec)
            for r in rows:
                if r["dst_id"] == rec["id"]:
                    rec["relation"] = r["relation"]
                    rec["source_field"] = r["source_field"]
                    break
            out.append(rec)
        return out
    finally:
        conn.close()


def judge_profile(judge_name: str, *, db_path: Optional[pathlib.Path] = None) -> dict:
    """Profile a judge across all their judgments.

    Match strategy: case-insensitive substring against the canonical
    ``name`` field of each entry in ``judges_meta.judges_json``. We
    deliberately use substring matching (not registry lookup) so callers
    can pass either a full canonical form ("Sitali J") or just a surname
    ("Sitali") — both Phase 5 records and the registry are normalised
    with surnames first, so substring is well-behaved.

    Returns a dict with:
        ``judge_name``: the input string,
        ``total``: int — number of judgments matched,
        ``judgments``: list[dict] — each judgment record (base+meta),
        ``outcome_counts``: dict[str,int] — outcome -> count,
        ``courts``: dict[str,int] — court -> count.
    """
    needle = (judge_name or "").strip().lower()
    if not needle:
        return {
            "judge_name": judge_name,
            "total": 0,
            "judgments": [],
            "outcome_counts": {},
            "courts": {},
        }
    conn = _connect(db_path)
    try:
        rows = conn.execute(
            "SELECT id, judges_json FROM judgments_meta "
            "WHERE judges_json IS NOT NULL AND judges_json != '' AND judges_json != '[]'"
        ).fetchall()
        matched_ids: list[str] = []
        for r in rows:
            try:
                judges = json.loads(r["judges_json"]) or []
            except (ValueError, TypeError):
                judges = []
            for j in judges:
                if not isinstance(j, dict):
                    continue
                name = (j.get("name") or "").lower()
                if needle in name:
                    matched_ids.append(r["id"])
                    break
        recs = _records_by_ids(conn, matched_ids)
        full = [_attach_meta(conn, rec) for rec in recs]
        outcomes: dict[str, int] = {}
        courts: dict[str, int] = {}
        for j in full:
            o = j.get("outcome") or "(unspecified)"
            outcomes[o] = outcomes.get(o, 0) + 1
            c = j.get("court") or "(unspecified)"
            courts[c] = courts.get(c, 0) + 1
        full.sort(key=lambda r: (r.get("date_decided") or "", r.get("id") or ""))
        return {
            "judge_name": judge_name,
            "total": len(full),
            "judgments": full,
            "outcome_counts": outcomes,
            "courts": courts,
        }
    finally:
        conn.close()


def statute_interpretation(
    act_id: str, *, db_path: Optional[pathlib.Path] = None
) -> list[dict]:
    """All judgments that interpret a given statute.

    Three resolution paths, evaluated in order, deduped by judgment id:

    1. ``citations`` table edges where ``relation='cites_statute'`` and
       ``dst_id == act_id`` — the canonical, integrity-checked path.
    2. ``judgments_meta.key_statutes_json`` containing the act_id literally.
    3. ``judgments_meta.key_statutes_json`` mentioning the statute's
       title or citation (from ``records.title`` / ``records.citation``)
       as a free-text fallback for records the parser left unstructured.
    """
    if not act_id:
        return []
    conn = _connect(db_path)
    try:
        ids: list[str] = []
        seen: set[str] = set()

        # Path 1: citations edges
        rows = conn.execute(
            "SELECT src_id FROM citations "
            "WHERE relation='cites_statute' AND dst_id=? ORDER BY src_id",
            (act_id,),
        ).fetchall()
        for r in rows:
            if r["src_id"] not in seen:
                seen.add(r["src_id"])
                ids.append(r["src_id"])

        # Look up the statute's title + citation for the free-text path.
        s = conn.execute(
            "SELECT title, citation FROM records WHERE id=?", (act_id,)
        ).fetchone()
        title = (s["title"] if s else "") or ""
        cite = (s["citation"] if s else "") or ""

        # Path 2 + 3: scan judgments_meta.key_statutes_json
        rows = conn.execute(
            "SELECT id, key_statutes_json FROM judgments_meta "
            "WHERE key_statutes_json IS NOT NULL "
            "AND key_statutes_json != '' AND key_statutes_json != '[]'"
        ).fetchall()
        for r in rows:
            blob = r["key_statutes_json"] or ""
            hit = act_id and act_id in blob
            if not hit and title:
                hit = title.lower() in blob.lower()
            if not hit and cite:
                hit = cite.lower() in blob.lower()
            if hit and r["id"] not in seen:
                seen.add(r["id"])
                ids.append(r["id"])

        recs = _records_by_ids(conn, ids)
        return [_attach_meta(conn, rec) for rec in recs]
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def _print_json(obj: Any) -> None:
    """Print obj as JSON with stable, deterministic key ordering."""
    sys.stdout.write(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True))
    sys.stdout.write("\n")


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="query_corpus — Phase 6 retrieval API for the Zambian Authorities Corpus"
    )
    p.add_argument(
        "--db",
        default=None,
        help=f"Path to corpus.sqlite (default: {DB_PATH})",
    )
    sub = p.add_subparsers(dest="command", required=True)

    s = sub.add_parser("search", help="FTS5 full-text search")
    s.add_argument("query")
    s.add_argument("--type", default=None, choices=["act", "si", "judgment"])
    s.add_argument("--court", default=None)
    s.add_argument("--year-from", type=int, default=None, dest="year_from")
    s.add_argument("--year-to", type=int, default=None, dest="year_to")
    s.add_argument("--limit", type=int, default=DEFAULT_LIMIT)

    g = sub.add_parser("get", help="Look up a single record by id")
    g.add_argument("record_id")

    co = sub.add_parser("citations-of", help="Records citing the given record")
    co.add_argument("record_id")

    cb = sub.add_parser("cited-by", help="Records cited by the given record")
    cb.add_argument("record_id")

    j = sub.add_parser("judge", help="Profile of a judge")
    j.add_argument("judge_name")

    si = sub.add_parser(
        "statute-interpretation", help="Judgments interpreting a statute"
    )
    si.add_argument("act_id")

    return p


def main(argv: Optional[list[str]] = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    db_path = pathlib.Path(args.db) if args.db else None
    if args.command == "search":
        out = search(
            args.query,
            type=args.type,
            court=args.court,
            year_from=args.year_from,
            year_to=args.year_to,
            limit=args.limit,
            db_path=db_path,
        )
    elif args.command == "get":
        out = get_by_id(args.record_id, db_path=db_path)
    elif args.command == "citations-of":
        out = citations_of(args.record_id, db_path=db_path)
    elif args.command == "cited-by":
        out = cited_by(args.record_id, db_path=db_path)
    elif args.command == "judge":
        out = judge_profile(args.judge_name, db_path=db_path)
    elif args.command == "statute-interpretation":
        out = statute_interpretation(args.act_id, db_path=db_path)
    else:
        parser.print_help()
        return 2
    _print_json(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
