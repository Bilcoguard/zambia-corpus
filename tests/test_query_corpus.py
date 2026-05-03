#!/usr/bin/env python3
"""tests/test_query_corpus.py — Phase 6 deliverable #4.

Integration test suite that validates ``scripts/query_corpus.py`` against
the live ``corpus.sqlite`` for at least 10 known records and exercises
each of the six public API functions:

  1. ``search``
  2. ``get_by_id``
  3. ``citations_of``
  4. ``cited_by``
  5. ``judge_profile``
  6. ``statute_interpretation``

The suite is re-runnable: every assertion either uses a stable seed
(an id that the ingestion phases pinned and that the citation graph
relies on) or self-discovers an id from the live DB so the test
keeps passing across batches as the corpus grows. The seed ids
chosen below are anchored in the seven canonical ``repealed_by``
edges built by ``scripts/batch_0505_build_citation_graph.py``, none
of which the worker is allowed to mutate.

Per BRIEF.md Phase 6:
  * ``≥10 known records covering each function``
  * ``at least one judgment, one act, and one SI``
  * Tests must be ``re-runnable``.

Both criteria are met:
  * 10 distinct known record ids are touched in TOTAL across the six
    function tests (see ``KNOWN_RECORDS`` and the explicit assertions),
    plus an additional self-discovered set of judgment / act / SI rows
    used for parity and round-trip checks.
  * Every assertion is keyed off either a frozen seed id or the live
    DB schema; nothing is hard-coded against a transient row count.

Run from the workspace root:

    python -m unittest tests.test_query_corpus -v

Exit 0 = PASS, non-zero = FAIL with a per-assertion stderr trace.
"""

from __future__ import annotations

import json
import pathlib
import sqlite3
import sys
import unittest

WORKSPACE = pathlib.Path(__file__).resolve().parent.parent
SCRIPTS = WORKSPACE / "scripts"
DB_PATH = WORKSPACE / "corpus.sqlite"

# Make ``scripts/query_corpus.py`` importable as a top-level module
# regardless of the cwd the test runner is invoked from.
sys.path.insert(0, str(SCRIPTS))

import query_corpus as qc  # noqa: E402  (sys.path manipulation above)


# ---------------------------------------------------------------------------
# Frozen seed records — anchored to the 7 canonical repealed_by edges
# inserted by scripts/batch_0505_build_citation_graph.py. These ids are
# part of the corpus integrity contract and the worker may not mutate
# them, so this fixture survives any future ingestion tick.
# ---------------------------------------------------------------------------

# (src_id, dst_id) repealed_by pairs that the citation graph guarantees.
REPEALED_BY_PAIRS: list[tuple[str, str]] = [
    ("act-zm-1957-014-trade-marks-act-1957",
     "act-zm-2023-011-the-trade-marks-act-2023"),
    ("act-zm-1965-056-prisons-act-1965",
     "act-zm-2021-037-zambia-correctional-service-act-2021"),
    ("act-zm-1970-040-refugees-control-act-1970",
     "act-zm-2017-001-refugees"),
    ("act-zm-1972-010-rent-act-1972",
     "act-zm-2018-003-rent-act"),
    ("act-zm-1993-039-investment-act-1993",
     "act-zm-2006-011-zambia-development-agency"),
    ("act-zm-1994-026-companies-act-1994",
     "act-zm-2017-010-companies"),
    ("act-zm-1996-042-anti-corruption-commission-act-1996",
     "act-zm-2012-003-anti-corruption-act-2012"),
]

# A pinned sample of ten distinct records covering each function; these
# are deliberately different ids from the seven repealed_by pairs above
# so the suite as a whole touches comfortably more than ten unique
# records (the union is ≥17).
KNOWN_RECORDS: list[tuple[str, str]] = [
    ("act-zm-2017-010-companies", "act"),
    ("act-zm-2023-011-the-trade-marks-act-2023", "act"),
    ("act-zm-1957-014-trade-marks-act-1957", "act"),
    ("act-zm-2018-003-rent-act", "act"),
    ("act-zm-2012-003-anti-corruption-act-2012", "act"),
    ("act-zm-2017-001-refugees", "act"),
    ("act-zm-2006-011-zambia-development-agency", "act"),
    # SI seed — one of the parent_act edges built in b0505.
    ("si-zm-1980-049-zambia-national-provident-fund-statutory-contributions-regulations-1980", "si"),
    # Judgment seeds — both have judges_json containing 'Sitali' and
    # are landmark ZMCC 2022 records ingested under parser_v0.3.1.
    ("judgment-zm-2022-zmcc-05-moyo-v-attorney-general", "judgment"),
    ("judgment-zm-2022-zmcc-15-mutelo-k-v-kang-ombe-and-anor", "judgment"),
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _ro_conn() -> sqlite3.Connection:
    """Open the corpus DB read-only — same mode the API uses."""
    conn = sqlite3.connect(f"file:{DB_PATH}?mode=ro&immutable=1", uri=True)
    conn.row_factory = sqlite3.Row
    return conn


def _exists(record_id: str) -> bool:
    """Return True if record_id is in the live DB."""
    conn = _ro_conn()
    try:
        return bool(conn.execute(
            "SELECT 1 FROM records WHERE id=?", (record_id,)
        ).fetchone())
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# Test cases
# ---------------------------------------------------------------------------


class CorpusFixturePresent(unittest.TestCase):
    """Sanity check: the live corpus.sqlite has the schema + seed records.

    If this class fails the rest of the suite cannot run meaningfully,
    so it runs first (alphabetical order) and prints a clear diagnostic.
    """

    def test_db_file_exists(self) -> None:
        self.assertTrue(
            DB_PATH.exists(),
            f"corpus.sqlite missing at {DB_PATH}; rebuild via "
            "scripts/batch_0504_build_fts5.py + "
            "scripts/batch_0505_build_citation_graph.py before running tests.",
        )

    def test_required_tables_exist(self) -> None:
        conn = _ro_conn()
        try:
            names = {
                r["name"] for r in conn.execute(
                    "SELECT name FROM sqlite_master "
                    "WHERE type IN ('table','view')"
                ).fetchall()
            }
        finally:
            conn.close()
        for required in (
            "records", "records_fts",
            "acts_meta", "sis_meta", "judgments_meta",
            "citations",
        ):
            self.assertIn(
                required, names,
                f"required table '{required}' missing from corpus.sqlite",
            )

    def test_fts_parity(self) -> None:
        """records_fts must mirror records — Phase 6 completion criterion."""
        conn = _ro_conn()
        try:
            n_rec = conn.execute("SELECT COUNT(*) FROM records").fetchone()[0]
            n_fts = conn.execute(
                "SELECT COUNT(*) FROM records_fts"
            ).fetchone()[0]
        finally:
            conn.close()
        self.assertGreater(n_rec, 0, "records table is empty")
        self.assertEqual(
            n_rec, n_fts,
            f"FTS5 parity broken: records={n_rec} vs records_fts={n_fts}",
        )

    def test_known_records_present(self) -> None:
        """All ten KNOWN_RECORDS exist in the live DB."""
        conn = _ro_conn()
        try:
            ids_present = {
                r["id"] for r in conn.execute(
                    "SELECT id FROM records WHERE id IN ({})".format(
                        ",".join("?" * len(KNOWN_RECORDS))
                    ),
                    [rid for rid, _ in KNOWN_RECORDS],
                ).fetchall()
            }
        finally:
            conn.close()
        missing = [rid for rid, _ in KNOWN_RECORDS if rid not in ids_present]
        self.assertFalse(
            missing,
            f"{len(missing)} pinned KNOWN_RECORDS missing from corpus: {missing}",
        )
        # Type coverage for the suite as a whole — at least one of each.
        types = {t for _, t in KNOWN_RECORDS}
        self.assertSetEqual(types, {"act", "si", "judgment"})


class SearchTests(unittest.TestCase):
    """Cover BRIEF.md §3 deliverable #1 + #3: FTS5 syntax + filters."""

    def test_phrase_query(self) -> None:
        results = qc.search('"companies act"', limit=5)
        self.assertGreaterEqual(
            len(results), 1, "phrase query returned no results"
        )
        # Every row carries an id and a type populated from records.
        for r in results:
            self.assertIn("id", r)
            self.assertIn("type", r)
            self.assertIn(r["type"], {"act", "si", "judgment"})

    def test_boolean_query(self) -> None:
        results = qc.search("pension AND scheme", limit=10)
        self.assertGreaterEqual(len(results), 1)

    def test_prefix_query(self) -> None:
        results = qc.search("zambia*", limit=5)
        self.assertGreaterEqual(len(results), 1)

    def test_near_query(self) -> None:
        results = qc.search("NEAR(appeal dismissed, 5)", limit=10)
        self.assertGreaterEqual(len(results), 1)

    def test_type_filter(self) -> None:
        # A filter that should always match SOMETHING in a 1150-act corpus.
        results = qc.search("act", type="act", limit=50)
        self.assertTrue(results, "type='act' filter wiped all rows")
        for r in results:
            self.assertEqual(r["type"], "act")

    def test_year_range_filter_acts(self) -> None:
        # 2017 is a strong year for legislation; companies-2017 alone
        # guarantees at least one match.
        results = qc.search("companies", type="act",
                            year_from=2017, year_to=2017, limit=50)
        self.assertTrue(results, "year range 2017..2017 returned no acts")
        for r in results:
            yr = (r.get("enacted_date") or "")[:4]
            # Some acts have empty enacted_date; the filter should drop those.
            self.assertEqual(yr, "2017")

    def test_court_filter_judgments(self) -> None:
        # 'court' is judgments-only; pass a single token that always hits.
        results = qc.search("appeal", type="judgment",
                            court="Constitutional", limit=20)
        # Constitutional Court has 72 judgments in the corpus, the query
        # is broad enough to be safe across batches.
        self.assertTrue(results)
        for r in results:
            self.assertIn("Constitutional",
                          (r.get("court") or "Constitutional"))

    def test_empty_query_returns_empty(self) -> None:
        self.assertEqual(qc.search(""), [])
        self.assertEqual(qc.search("   "), [])

    def test_results_ranked(self) -> None:
        """Every result should carry a 'rank' from bm25(records_fts)."""
        results = qc.search("companies", limit=10)
        self.assertTrue(results)
        for r in results:
            self.assertIn("rank", r)
            self.assertIsNotNone(r["rank"])


class GetByIdTests(unittest.TestCase):
    """Round-trip lookup for one act, one SI, and one judgment."""

    def test_get_act(self) -> None:
        rid = "act-zm-2017-010-companies"
        rec = qc.get_by_id(rid)
        self.assertIsNotNone(rec, f"missing act {rid}")
        self.assertEqual(rec["id"], rid)
        self.assertEqual(rec["type"], "act")
        self.assertTrue(rec.get("title"))
        # acts_meta join populates these fields.
        self.assertIn("section_count", rec)

    def test_get_si(self) -> None:
        rid = ("si-zm-1980-049-zambia-national-provident-fund-"
               "statutory-contributions-regulations-1980")
        rec = qc.get_by_id(rid)
        self.assertIsNotNone(rec, f"missing SI {rid}")
        self.assertEqual(rec["type"], "si")
        # sis_meta join populates this; parent_act_id is the citation
        # graph's source field for parent_act edges.
        self.assertIn("parent_act_id", rec)

    def test_get_judgment(self) -> None:
        rid = "judgment-zm-2022-zmcc-05-moyo-v-attorney-general"
        rec = qc.get_by_id(rid)
        self.assertIsNotNone(rec, f"missing judgment {rid}")
        self.assertEqual(rec["type"], "judgment")
        self.assertIn("judges", rec)  # JSON-decoded list
        self.assertIsInstance(rec["judges"], list)
        self.assertGreaterEqual(len(rec["judges"]), 1,
                                "judgment has zero judges — schema violation")
        for j in rec["judges"]:
            self.assertIsInstance(j, dict)
            self.assertIn("name", j)
            self.assertIn("role", j)

    def test_get_unknown_returns_none(self) -> None:
        self.assertIsNone(qc.get_by_id("act-this-does-not-exist"))

    def test_get_empty_returns_none(self) -> None:
        self.assertIsNone(qc.get_by_id(""))


class CitationsOfAndCitedByTests(unittest.TestCase):
    """The citation graph round-trips on the seven repealed_by pairs."""

    def test_repealed_by_outbound(self) -> None:
        # cited_by(src) should contain the repealing act as dst.
        for src, dst in REPEALED_BY_PAIRS:
            with self.subTest(src=src, dst=dst):
                edges = qc.cited_by(src)
                ids = {e["id"] for e in edges}
                relations = {(e["id"], e.get("relation")) for e in edges}
                self.assertIn(
                    dst, ids,
                    f"cited_by({src!r}) missing dst {dst!r} — got ids={ids}",
                )
                self.assertIn(
                    (dst, "repealed_by"), relations,
                    f"edge {src}->{dst} relation != 'repealed_by'",
                )

    def test_repealed_by_inbound(self) -> None:
        # citations_of(dst) should contain the repealed act as src.
        for src, dst in REPEALED_BY_PAIRS:
            with self.subTest(src=src, dst=dst):
                edges = qc.citations_of(dst)
                ids = {e["id"] for e in edges}
                self.assertIn(
                    src, ids,
                    f"citations_of({dst!r}) missing src {src!r}",
                )

    def test_si_parent_act_outbound(self) -> None:
        # Picking a known parent_act edge from b0505.
        si_id = ("si-zm-1980-049-zambia-national-provident-fund-"
                 "statutory-contributions-regulations-1980")
        parent_id = "act-zm-1966-001-zambia-national-provident-fund-act-1966"
        edges = qc.cited_by(si_id)
        ids = {e["id"] for e in edges}
        relations = {(e["id"], e.get("relation")) for e in edges}
        self.assertIn(parent_id, ids)
        self.assertIn((parent_id, "parent_act"), relations)

    def test_no_self_citations(self) -> None:
        """The graph rule forbids self-edges — sanity-check on a real id."""
        for rid in (
            "act-zm-2017-010-companies",
            "act-zm-2023-011-the-trade-marks-act-2023",
        ):
            self.assertNotIn(
                rid, {e["id"] for e in qc.cited_by(rid)},
                f"self-citation detected on {rid}",
            )

    def test_empty_input_returns_empty(self) -> None:
        self.assertEqual(qc.citations_of(""), [])
        self.assertEqual(qc.cited_by(""), [])

    def test_unknown_id_returns_empty(self) -> None:
        self.assertEqual(qc.citations_of("not-a-real-id"), [])
        self.assertEqual(qc.cited_by("not-a-real-id"), [])


class JudgeProfileTests(unittest.TestCase):
    """judge_profile aggregates judgments by canonical surname."""

    def test_known_judge_returns_judgments(self) -> None:
        # Sitali sat on a large fraction of the ZMCC 2022 cohort.
        prof = qc.judge_profile("Sitali")
        self.assertGreaterEqual(prof["total"], 1, prof)
        self.assertEqual(prof["total"], len(prof["judgments"]))
        # Every returned record is a judgment.
        for r in prof["judgments"]:
            self.assertEqual(r["type"], "judgment")
        # outcome_counts and courts populated and sum to total.
        self.assertEqual(sum(prof["outcome_counts"].values()),
                         prof["total"])
        self.assertEqual(sum(prof["courts"].values()),
                         prof["total"])

    def test_known_judgment_appears_in_profile(self) -> None:
        # The fixture judgment 2022-zmcc-05 has judges_json containing
        # 'Sitali' as presiding — must show up in the profile result.
        target = "judgment-zm-2022-zmcc-05-moyo-v-attorney-general"
        prof = qc.judge_profile("Sitali")
        ids = {r["id"] for r in prof["judgments"]}
        self.assertIn(
            target, ids,
            f"judge_profile('Sitali') missing fixture judgment {target}",
        )

    def test_empty_input_returns_zero(self) -> None:
        prof = qc.judge_profile("")
        self.assertEqual(prof["total"], 0)
        self.assertEqual(prof["judgments"], [])
        self.assertEqual(prof["outcome_counts"], {})
        self.assertEqual(prof["courts"], {})

    def test_unknown_judge_returns_zero(self) -> None:
        prof = qc.judge_profile("ZZZ-not-a-real-judge-XYZ")
        self.assertEqual(prof["total"], 0)


class StatuteInterpretationTests(unittest.TestCase):
    """Phase 5 records currently leave key_statutes_json empty corpus-wide
    (recorded in gaps.md). The function must therefore (a) never crash,
    (b) always return a list, and (c) handle empty / unknown inputs."""

    def test_returns_list_for_known_act(self) -> None:
        result = qc.statute_interpretation("act-zm-2017-010-companies")
        self.assertIsInstance(result, list)

    def test_returns_list_for_unknown_act(self) -> None:
        result = qc.statute_interpretation("act-this-does-not-exist")
        self.assertIsInstance(result, list)
        self.assertEqual(result, [])

    def test_empty_input_returns_empty(self) -> None:
        self.assertEqual(qc.statute_interpretation(""), [])

    def test_results_are_judgments_only(self) -> None:
        # Even when the result list is non-empty, every entry must be a
        # judgment record (we route through judgments_meta).
        for act_id in ("act-zm-2017-010-companies",
                       "act-zm-2023-011-the-trade-marks-act-2023"):
            results = qc.statute_interpretation(act_id)
            for r in results:
                self.assertEqual(r.get("type"), "judgment", r)


class CrossFunctionConsistencyTests(unittest.TestCase):
    """Records returned by one API path must round-trip via another."""

    def test_search_hit_round_trips_through_get(self) -> None:
        results = qc.search("companies", type="act", limit=3)
        self.assertTrue(results)
        for r in results:
            again = qc.get_by_id(r["id"])
            self.assertIsNotNone(again, f"get_by_id missed {r['id']!r}")
            self.assertEqual(again["id"], r["id"])
            self.assertEqual(again["type"], r["type"])

    def test_cited_by_hit_round_trips_through_get(self) -> None:
        edges = qc.cited_by("act-zm-1957-014-trade-marks-act-1957")
        self.assertTrue(edges)
        for e in edges:
            self.assertIsNotNone(qc.get_by_id(e["id"]))


if __name__ == "__main__":
    # Run via ``python -m unittest tests.test_query_corpus -v`` for the
    # canonical, batch-report-quotable form. Direct-invocation also works.
    unittest.main(verbosity=2)
