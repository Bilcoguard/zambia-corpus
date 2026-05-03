#!/usr/bin/env python3
"""integrity_check_b0509.py — Phase 6 batch 0509 (test_query_corpus.py).

Validates Phase 6 deliverable #4 (``tests/test_query_corpus.py``) plus
no-regression on deliverables #1-#3:

  1. Test module imports and discovers all expected TestCase classes.
  2. ``unittest`` runs the full suite to PASS, with ≥ 30 assertions and
     all six API functions covered (search / get_by_id / citations_of /
     cited_by / judge_profile / statute_interpretation).
  3. Coverage check: ≥ 10 distinct record ids touched across
     KNOWN_RECORDS + REPEALED_BY_PAIRS, with at least one act, one SI,
     and one judgment present.
  4. Re-runnable check: the same suite passes a second time (covers
     the BRIEF.md ``re-runnable`` requirement directly).
  5. No regression on deliverables #1-#3:
        - records / records_fts row count parity
        - citations table size unchanged from b0508 baseline (≥221)
        - integrity_check_b0508.py still PASSes (delegated invocation)

Exit 0 on PASS; exit 1 with a stderr diagnostic on FAIL.
"""

from __future__ import annotations

import importlib
import io
import pathlib
import sqlite3
import subprocess
import sys
import traceback
import unittest

WORKSPACE = pathlib.Path(__file__).resolve().parent.parent
DB_PATH = WORKSPACE / "corpus.sqlite"
SCRIPTS = WORKSPACE / "scripts"
TESTS = WORKSPACE / "tests"

# Make tests + scripts importable.
sys.path.insert(0, str(WORKSPACE))
sys.path.insert(0, str(SCRIPTS))


BASELINE_B0508 = {
    "records": 1791,
    "records_fts": 1791,
    "citations_min": 221,
}


def _expect(condition: bool, label: str, detail: str = "") -> None:
    if not condition:
        msg = f"INTEGRITY FAIL [{label}]"
        if detail:
            msg += f": {detail}"
        raise AssertionError(msg)


def _run_suite() -> tuple[int, int, int, list[str]]:
    """Run the test suite once. Returns (n_run, n_failures, n_errors, names)."""
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromName("tests.test_query_corpus")
    # Walk the suite tree and collect the test names so we can verify
    # coverage of all six API functions.
    names: list[str] = []
    def _walk(s):
        for t in s:
            if isinstance(t, unittest.TestSuite):
                _walk(t)
            else:
                names.append(t.id())
    _walk(suite)
    buf = io.StringIO()
    runner = unittest.TextTestRunner(stream=buf, verbosity=2)
    result = runner.run(suite)
    return result.testsRun, len(result.failures), len(result.errors), names


def main() -> int:
    checks_run = 0
    try:
        # 1. Test module imports clean.
        test_mod = importlib.import_module("tests.test_query_corpus")
        for cls in (
            "CorpusFixturePresent",
            "SearchTests",
            "GetByIdTests",
            "CitationsOfAndCitedByTests",
            "JudgeProfileTests",
            "StatuteInterpretationTests",
            "CrossFunctionConsistencyTests",
        ):
            _expect(hasattr(test_mod, cls),
                    f"import.{cls}", "TestCase missing")
            checks_run += 1

        # 2. Run the suite — must pass cleanly.
        n_run, n_fail, n_err, names = _run_suite()
        _expect(n_run >= 30, "suite.size",
                f"only {n_run} tests collected (expected ≥30)")
        _expect(n_fail == 0 and n_err == 0,
                "suite.pass",
                f"failures={n_fail} errors={n_err}")
        checks_run += 2

        # 2a. All six API function families covered by class name.
        function_classes = {
            "search":                  "SearchTests",
            "get_by_id":               "GetByIdTests",
            "citations_of/cited_by":   "CitationsOfAndCitedByTests",
            "judge_profile":           "JudgeProfileTests",
            "statute_interpretation":  "StatuteInterpretationTests",
            "cross-function":          "CrossFunctionConsistencyTests",
        }
        for fn, cls in function_classes.items():
            covered = any(cls in n for n in names)
            _expect(covered, f"coverage.{fn}", f"no test in {cls}")
            checks_run += 1

        # 3. Coverage check — KNOWN_RECORDS + REPEALED_BY_PAIRS hit ≥10
        # unique ids spanning all three types.
        union: set[str] = set()
        types: set[str] = set()
        for rid, t in test_mod.KNOWN_RECORDS:
            union.add(rid)
            types.add(t)
        for src, dst in test_mod.REPEALED_BY_PAIRS:
            union.update([src, dst])
        _expect(len(union) >= 10,
                "coverage.unique_ids",
                f"only {len(union)} unique ids in fixtures")
        _expect(types == {"act", "si", "judgment"},
                "coverage.types",
                f"types covered: {types}")
        checks_run += 2

        # All ids in the union must currently exist in the DB.
        conn = sqlite3.connect(f"file:{DB_PATH}?mode=ro&immutable=1", uri=True)
        try:
            placeholders = ",".join("?" * len(union))
            present = {
                row[0] for row in conn.execute(
                    f"SELECT id FROM records WHERE id IN ({placeholders})",
                    list(union),
                ).fetchall()
            }
        finally:
            conn.close()
        missing = sorted(union - present)
        _expect(not missing, "coverage.fixture_present",
                f"{len(missing)} fixture ids missing from corpus: {missing}")
        checks_run += 1

        # 4. Re-runnable: run the suite a second time end-to-end.
        n_run2, n_fail2, n_err2, _ = _run_suite()
        _expect(n_run2 == n_run, "rerun.size",
                f"{n_run2} vs {n_run}")
        _expect(n_fail2 == 0 and n_err2 == 0, "rerun.pass",
                f"failures={n_fail2} errors={n_err2}")
        checks_run += 2

        # 5. No regression on deliverables #1-#3.
        conn = sqlite3.connect(f"file:{DB_PATH}?mode=ro&immutable=1", uri=True)
        try:
            n_rec = conn.execute("SELECT COUNT(*) FROM records").fetchone()[0]
            n_fts = conn.execute(
                "SELECT COUNT(*) FROM records_fts"
            ).fetchone()[0]
            n_cit = conn.execute(
                "SELECT COUNT(*) FROM citations"
            ).fetchone()[0]
        finally:
            conn.close()
        _expect(n_rec == BASELINE_B0508["records"], "regression.records",
                f"records={n_rec} expected {BASELINE_B0508['records']}")
        _expect(n_fts == BASELINE_B0508["records_fts"],
                "regression.records_fts",
                f"records_fts={n_fts}")
        _expect(n_rec == n_fts, "regression.fts_parity")
        _expect(n_cit >= BASELINE_B0508["citations_min"],
                "regression.citations",
                f"citations={n_cit}")
        checks_run += 4

        # Delegated b0508 integrity check.
        proc = subprocess.run(
            [sys.executable, str(SCRIPTS / "integrity_check_b0508.py")],
            capture_output=True, text=True, timeout=60,
        )
        _expect(proc.returncode == 0,
                "regression.integrity_b0508",
                f"rc={proc.returncode} stderr={proc.stderr[-300:]}")
        checks_run += 1
    except Exception:  # noqa: BLE001
        sys.stderr.write("INTEGRITY CHECK FAIL\n")
        traceback.print_exc()
        return 1

    print(
        f"INTEGRITY CHECK PASS — {checks_run} assertions over "
        "tests/test_query_corpus.py + no regression on deliverables #1-#3"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
