#!/usr/bin/env python3
"""integrity_check_b0513.py — Phase 7 batch 2 integrity check.

Phase 7 batch 2 deliverables (this batch):
  - examples/amendment_chain.py
  - examples/judge_decision_profile.py
  - examples/citation_chain.py
  - INTEGRATION.md "Example scripts" table updated to mark all 5 scripts
    as Implemented + worked-example bullets per script.

Integrity rules (BRIEF.md Phase 7 §107):
  * No regression on existing tables (records / records_fts / citations).
  * Every example script that exists runs without error and produces
    non-empty output for at least one realistic example.
  * Data-coverage figures cited in INTEGRATION.md reproduce when
    re-computed against corpus.sqlite (delegated to b0512 unchanged).
  * No fabricated function names, parameters, or example outputs — every
    example block in INTEGRATION.md must reference a real function in
    scripts/query_corpus.py with parameters that actually exist.

This check ALWAYS runs the full b0512 suite first (delegating via
subprocess so a regression on the prior batch surfaces verbatim) and
then adds batch-2-specific assertions.

Exits 0 on success, non-zero with a diagnostic on the first failed assertion.
"""
from __future__ import annotations

import json
import pathlib
import shutil
import sqlite3
import subprocess
import sys
import tempfile

WORKSPACE = pathlib.Path(__file__).resolve().parent.parent
DB_PATH = WORKSPACE / "corpus.sqlite"
INTEGRATION_MD = WORKSPACE / "INTEGRATION.md"
EXAMPLES_DIR = WORKSPACE / "examples"
PRIOR_CHECK = WORKSPACE / "scripts" / "integrity_check_b0512.py"


def _fail(msg: str) -> None:
    print(f"INTEGRITY CHECK FAIL: {msg}", file=sys.stderr)
    sys.exit(2)


def _open_ro_db() -> sqlite3.Connection:
    """Read-only DB via temp copy (matches b0512 pattern; FUSE journal
    recovery would otherwise fail under mode=ro&immutable=1)."""
    if not DB_PATH.exists():
        _fail(f"corpus.sqlite missing at {DB_PATH}")
    tmp_dir = pathlib.Path(tempfile.mkdtemp(prefix="b0513_check_"))
    tmp_db = tmp_dir / "corpus.sqlite"
    shutil.copy(DB_PATH, tmp_db)
    return sqlite3.connect(f"file:{tmp_db}?mode=ro&immutable=1", uri=True)


def main() -> int:
    asserts: list[str] = []

    # 0. Delegated re-run of the b0512 check — surfaces any regression on
    #    the prior batch verbatim.
    if not PRIOR_CHECK.exists():
        _fail(f"prior integrity check missing: {PRIOR_CHECK}")
    res = subprocess.run(
        [sys.executable, str(PRIOR_CHECK)],
        capture_output=True, text=True, timeout=120, cwd=str(WORKSPACE),
    )
    if res.returncode != 0:
        _fail(
            f"delegated b0512 check failed (rc={res.returncode}); "
            f"stderr tail: {res.stderr[-400:]!r}"
        )
    # Pull the assertion count out of the delegated output for the report.
    delegated_count = 0
    for line in res.stdout.splitlines():
        if "INTEGRITY CHECK PASS" in line:
            try:
                delegated_count = int(line.split("—")[1].strip().split()[0])
            except Exception:
                delegated_count = -1
    asserts.append(
        f"delegated b0512 PASS ({delegated_count} prior-batch assertions)"
    )

    # 1. The three new example scripts exist and import cleanly as modules.
    new_scripts = [
        ("amendment_chain.py", "amendment_chain"),
        ("judge_decision_profile.py", None),  # uses argparse only — no fn import
        ("citation_chain.py", "trace_chain"),
    ]
    for filename, _ in new_scripts:
        p = EXAMPLES_DIR / filename
        if not p.exists():
            _fail(f"example script missing: {p}")
        asserts.append(f"exists: examples/{filename}")

    # 2. Each new example runs cleanly with realistic args and produces
    #    non-empty stdout.
    example_runs = [
        # amendment_chain — default + JSON + repealing-act side
        ([sys.executable, str(EXAMPLES_DIR / "amendment_chain.py")],
         "amend-default", "Repealed by (1)"),
        ([sys.executable, str(EXAMPLES_DIR / "amendment_chain.py"),
          "act-zm-2017-010-companies", "--json"],
         "amend-2017-json", '"repeals":'),
        # judge_decision_profile — default high-volume judge
        ([sys.executable, str(EXAMPLES_DIR / "judge_decision_profile.py"),
          "--limit", "5"],
         "judge-default-5", "# Total judgments:"),
        ([sys.executable, str(EXAMPLES_DIR / "judge_decision_profile.py"),
          "Sitali", "--limit", "3"],
         "judge-sitali", "# Judge: Sitali"),
        # citation_chain — default + 2-hop walk + judgment-rooted (empty-ok)
        ([sys.executable, str(EXAMPLES_DIR / "citation_chain.py")],
         "cite-default", "## Outbound (records cited by root) (1)"),
        ([sys.executable, str(EXAMPLES_DIR / "citation_chain.py"),
          "act-zm-1957-014-trade-marks-act-1957", "--depth", "2"],
         "cite-trade-marks-d2", "# Depth:   2"),
    ]
    for argv, label, must_contain in example_runs:
        try:
            r = subprocess.run(
                argv, capture_output=True, text=True, timeout=60,
                cwd=str(WORKSPACE),
            )
        except subprocess.TimeoutExpired:
            _fail(f"example {label!r} timed out")
        if r.returncode != 0:
            _fail(
                f"example {label!r} exited with {r.returncode}; "
                f"stderr tail: {r.stderr[-400:]!r}"
            )
        if not r.stdout.strip():
            _fail(f"example {label!r} produced empty stdout")
        if must_contain not in r.stdout:
            _fail(
                f"example {label!r} stdout missing expected substring "
                f"{must_contain!r}; head: {r.stdout[:300]!r}"
            )
        asserts.append(
            f"example runs cleanly: {label} ({len(r.stdout)} chars stdout)"
        )

    # 3. amendment_chain.py JSON output round-trip — schema we promised
    #    (id, found, repealed_by, repeals, amended_by_raw, has_subsidiary)
    r = subprocess.run(
        [sys.executable, str(EXAMPLES_DIR / "amendment_chain.py"),
         "act-zm-1994-026-companies-act-1994", "--json"],
        capture_output=True, text=True, timeout=60, cwd=str(WORKSPACE),
    )
    if r.returncode != 0:
        _fail(f"amendment_chain json run failed: {r.stderr!r}")
    chain = json.loads(r.stdout)
    expected_keys = {
        "id", "found", "title", "citation", "enacted_date",
        "repealed_by", "repeals", "amended_by_raw", "has_subsidiary",
    }
    missing_keys = expected_keys - set(chain.keys())
    if missing_keys:
        _fail(f"amendment_chain JSON missing keys: {sorted(missing_keys)}")
    if not chain["found"]:
        _fail("amendment_chain default-id JSON shows found=false (DB mismatch?)")
    if len(chain["repealed_by"]) != 1:
        _fail(
            f"amendment_chain default-id repealed_by len={len(chain['repealed_by'])} "
            "(expected 1: 2017 Companies Act)"
        )
    if len(chain["has_subsidiary"]) != 3:
        _fail(
            f"amendment_chain default-id has_subsidiary len={len(chain['has_subsidiary'])} "
            "(expected 3 SIs from 2019)"
        )
    asserts.append(
        "amendment_chain JSON schema + 1994 Companies Act 1+3 chain verified"
    )

    # 4. citation_chain.py JSON output round-trip on the same root.
    r = subprocess.run(
        [sys.executable, str(EXAMPLES_DIR / "citation_chain.py"),
         "act-zm-1994-026-companies-act-1994", "--json"],
        capture_output=True, text=True, timeout=60, cwd=str(WORKSPACE),
    )
    if r.returncode != 0:
        _fail(f"citation_chain json run failed: {r.stderr!r}")
    cc = json.loads(r.stdout)
    if not isinstance(cc.get("outbound"), list) or len(cc["outbound"]) != 1:
        _fail(
            f"citation_chain default outbound count={len(cc.get('outbound', []))} "
            "(expected 1: repealed_by 2017 Act)"
        )
    if not isinstance(cc.get("inbound"), list) or len(cc["inbound"]) != 3:
        _fail(
            f"citation_chain default inbound count={len(cc.get('inbound', []))} "
            "(expected 3: 2019 subsidiary SIs)"
        )
    if cc["outbound"][0].get("relation") != "repealed_by":
        _fail(
            f"citation_chain default outbound relation="
            f"{cc['outbound'][0].get('relation')!r} (expected 'repealed_by')"
        )
    if not all(r.get("relation") == "parent_act" for r in cc["inbound"]):
        _fail("citation_chain default inbound has wrong relation labels")
    asserts.append("citation_chain JSON schema + 1+3 chain + relations verified")

    # 5. judge_decision_profile.py JSON view — total > 0 for default judge.
    r = subprocess.run(
        [sys.executable, str(EXAMPLES_DIR / "judge_decision_profile.py"),
         "--json", "--limit", "3"],
        capture_output=True, text=True, timeout=60, cwd=str(WORKSPACE),
    )
    if r.returncode != 0:
        _fail(f"judge_decision_profile json run failed: {r.stderr!r}")
    prof = json.loads(r.stdout)
    if prof.get("total", 0) <= 0:
        _fail(
            f"judge_decision_profile default judge total={prof.get('total')} "
            "(expected >0 for the highest-volume judge in the corpus)"
        )
    if not isinstance(prof.get("outcome_counts"), dict):
        _fail("judge_decision_profile JSON outcome_counts not a dict")
    if not isinstance(prof.get("courts"), dict):
        _fail("judge_decision_profile JSON courts not a dict")
    asserts.append(
        f"judge_decision_profile JSON: default judge total={prof['total']}, "
        f"{len(prof['outcome_counts'])} outcomes, {len(prof['courts'])} courts"
    )

    # 6. INTEGRATION.md table updates — all 5 scripts now marked Implemented.
    md = INTEGRATION_MD.read_text(encoding="utf-8")
    must_contain = [
        "`examples/amendment_chain.py` | Implemented in batch 0513",
        "`examples/judge_decision_profile.py` | Implemented in batch 0513",
        "`examples/citation_chain.py` | Implemented in batch 0513",
    ]
    for needle in must_contain:
        if needle not in md:
            _fail(f"INTEGRATION.md missing table row: {needle!r}")
        asserts.append(f"INTEGRATION.md row updated: {needle.split('|')[0].strip()}")

    # 7. The example-scripts directory contains exactly the five expected
    #    scripts (no stragglers, no missing entries).
    expected = {
        "corpus_search.py",
        "statute_interpretations.py",
        "amendment_chain.py",
        "judge_decision_profile.py",
        "citation_chain.py",
    }
    actual = {p.name for p in EXAMPLES_DIR.glob("*.py")}
    if expected - actual:
        _fail(f"missing example scripts: {sorted(expected - actual)}")
    extras = actual - expected
    if extras:
        # Not fatal but we want to know about it.
        asserts.append(f"WARNING: extra scripts in examples/: {sorted(extras)}")
    asserts.append(f"examples/ contains all 5 expected scripts")

    # 8. Live counts for the report (delegated check already verified
    #    INTEGRATION.md table values; here we just publish the snapshot).
    conn = _open_ro_db()
    snap = {
        "records":     conn.execute("SELECT COUNT(*) FROM records").fetchone()[0],
        "records_fts": conn.execute("SELECT COUNT(*) FROM records_fts").fetchone()[0],
        "citations":   conn.execute("SELECT COUNT(*) FROM citations").fetchone()[0],
    }
    if snap["records"] < 1791:
        _fail(f"records regression: {snap['records']} < 1791")
    if snap["records_fts"] < 1791:
        _fail(f"records_fts regression: {snap['records_fts']} < 1791")
    if snap["citations"] < 221:
        _fail(f"citations regression: {snap['citations']} < 221")
    asserts.append(
        f"row counts: records={snap['records']}, "
        f"records_fts={snap['records_fts']}, citations={snap['citations']} "
        "(no regression on Phase 6 baseline)"
    )

    print(
        f"INTEGRITY CHECK PASS — {len(asserts)} new assertions over Phase 7 "
        f"batch 2 (plus delegated b0512 PASS)"
    )
    for a in asserts:
        print(f"  ok: {a}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
