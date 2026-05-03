#!/usr/bin/env python3
"""integrity_check_b0508.py — Phase 6 batch 0508 (query_corpus.py landing).

Validates Phase 6 deliverable #3 (``scripts/query_corpus.py``) without
touching the on-disk source-of-truth:

  1. Module imports clean (no syntax errors, no missing names).
  2. ``query_corpus.search`` returns ≥1 result for each of 4 known seeds
     covering phrase / boolean / prefix / NEAR FTS5 syntaxes.
  3. ``get_by_id`` returns a complete record for one known act, one SI,
     and one judgment (each merging in its type-specific meta), and
     returns ``None`` for an unknown id.
  4. ``cited_by`` returns the expected ``repealed_by`` edge for the
     Trade Marks 1957 -> 2023 pair, and ``citations_of`` returns the
     same edge inbound.
  5. ``judge_profile`` returns ≥1 judgment for a judge known to be in
     the corpus (Sitali) and 0 for an empty input.
  6. ``statute_interpretation`` returns a list (empty is acceptable
     because Phase 5 records currently have empty key_statutes_json
     across the corpus — see gaps.md / batch-0505 report).
  7. No regression on records / records_fts row counts (must equal the
     baseline reported by batch-0506: records=1791, records_fts=1791).
  8. citations table row count >= the b0505 follow-up baseline (221).
  9. Empty / malformed inputs don't raise — all API functions return a
     well-typed empty value.

Exit 0 on PASS; exit 1 with a stderr diagnostic on FAIL.
"""

from __future__ import annotations

import pathlib
import sqlite3
import sys
import traceback

WORKSPACE = pathlib.Path(__file__).resolve().parent.parent
DB_PATH = WORKSPACE / "corpus.sqlite"
SCRIPTS = WORKSPACE / "scripts"

# Allow integrity check to import query_corpus.
sys.path.insert(0, str(SCRIPTS))


BASELINE = {
    "records": 1791,
    "records_fts": 1791,
    "citations_min": 221,  # post-b0505 follow-up canonical
}


def _expect(condition: bool, label: str, detail: str = "") -> None:
    """Assert ``condition`` is truthy; raise AssertionError if not."""
    if not condition:
        msg = f"INTEGRITY FAIL [{label}]"
        if detail:
            msg += f": {detail}"
        raise AssertionError(msg)


def main() -> int:
    checks_run = 0
    try:
        # 1. Import
        import query_corpus as qc  # noqa: WPS433
        checks_run += 1

        # 2. FTS5 syntax variants
        seeds = [
            ('"companies act"', "phrase"),
            ("pension AND scheme", "boolean"),
            ("zambia*", "prefix"),
            ("NEAR(appeal dismissed, 5)", "NEAR"),
        ]
        for q, label in seeds:
            res = qc.search(q, limit=5)
            _expect(len(res) >= 1, f"search.{label}", f"q={q!r} got {len(res)}")
            checks_run += 1

        # 3. get_by_id round trips
        # Find one of each type from the DB so the test self-discovers ids.
        conn = sqlite3.connect(f"file:{DB_PATH}?mode=ro&immutable=1", uri=True)
        conn.row_factory = sqlite3.Row
        try:
            act_row = conn.execute(
                "SELECT id FROM records WHERE type='act' LIMIT 1"
            ).fetchone()
            si_row = conn.execute(
                "SELECT id FROM records WHERE type='si' LIMIT 1"
            ).fetchone()
            j_row = conn.execute(
                "SELECT id FROM records WHERE type='judgment' LIMIT 1"
            ).fetchone()
        finally:
            conn.close()
        for r, t, label in (
            (act_row, "act", "get_by_id.act"),
            (si_row, "si", "get_by_id.si"),
            (j_row, "judgment", "get_by_id.judgment"),
        ):
            _expect(r is not None, label, "no row of this type in records")
            rec = qc.get_by_id(r["id"])
            _expect(rec is not None, label, f"id={r['id']!r}")
            _expect(rec.get("type") == t, label, f"wrong type: {rec.get('type')}")
            _expect(bool(rec.get("title")), label, "title empty")
            checks_run += 1
        _expect(qc.get_by_id("nope-not-real") is None, "get_by_id.unknown")
        checks_run += 1

        # 4. citations_of + cited_by on a known edge
        src = "act-zm-1957-014-trade-marks-act-1957"
        dst = "act-zm-2023-011-the-trade-marks-act-2023"
        out = qc.cited_by(src)
        _expect(any(r["id"] == dst and r.get("relation") == "repealed_by" for r in out),
                "cited_by.trade_marks", f"got {len(out)} edges")
        checks_run += 1
        inb = qc.citations_of(dst)
        _expect(any(r["id"] == src and r.get("relation") == "repealed_by" for r in inb),
                "citations_of.trade_marks", f"got {len(inb)} edges")
        checks_run += 1

        # 5. judge_profile sanity
        prof = qc.judge_profile("Sitali")
        _expect(prof["total"] >= 1, "judge_profile.sitali",
                f"got total={prof['total']}")
        checks_run += 1
        empty = qc.judge_profile("")
        _expect(empty["total"] == 0 and empty["judgments"] == [],
                "judge_profile.empty")
        checks_run += 1

        # 6. statute_interpretation does not crash; type is list[dict]
        si = qc.statute_interpretation("act-zm-2017-010-companies-act-2017")
        _expect(isinstance(si, list), "statute_interpretation.type",
                f"got {type(si).__name__}")
        checks_run += 1

        # 7. No regression on records / records_fts
        conn = sqlite3.connect(f"file:{DB_PATH}?mode=ro&immutable=1", uri=True)
        try:
            n_rec = conn.execute("SELECT COUNT(*) FROM records").fetchone()[0]
            n_fts = conn.execute("SELECT COUNT(*) FROM records_fts").fetchone()[0]
            n_cit = conn.execute("SELECT COUNT(*) FROM citations").fetchone()[0]
        finally:
            conn.close()
        _expect(n_rec == BASELINE["records"], "records.count",
                f"got {n_rec} expected {BASELINE['records']}")
        _expect(n_fts == BASELINE["records_fts"], "records_fts.count",
                f"got {n_fts} expected {BASELINE['records_fts']}")
        _expect(n_rec == n_fts, "records.fts_parity")
        _expect(n_cit >= BASELINE["citations_min"], "citations.count",
                f"got {n_cit} min {BASELINE['citations_min']}")
        checks_run += 4

        # 8. Empty inputs are well-handled.
        _expect(qc.search("") == [], "search.empty")
        _expect(qc.get_by_id("") is None, "get_by_id.empty")
        _expect(qc.citations_of("") == [], "citations_of.empty")
        _expect(qc.cited_by("") == [], "cited_by.empty")
        _expect(qc.statute_interpretation("") == [], "statute_interpretation.empty")
        checks_run += 5
    except Exception:  # noqa: BLE001
        sys.stderr.write("INTEGRITY CHECK FAIL\n")
        traceback.print_exc()
        return 1

    print(f"INTEGRITY CHECK PASS — {checks_run} assertions over query_corpus.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
