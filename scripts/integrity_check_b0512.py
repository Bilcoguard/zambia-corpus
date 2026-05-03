#!/usr/bin/env python3
"""integrity_check_b0512.py — Phase 7 batch 1 integrity check.

Phase 7 deliverables this batch:
  - INTEGRATION.md (initial draft: header, ToC, Data Coverage Summary,
    full API reference, stub sections for the rest)
  - examples/corpus_search.py
  - examples/statute_interpretations.py

Integrity rules (per BRIEF.md Phase 7 §107):
  * No regression on existing tables (records / records_fts / citations).
  * Example scripts that exist run without error and produce non-empty
    output for at least one realistic example.
  * Data-coverage figures cited in INTEGRATION.md reproduce when
    re-computed against corpus.sqlite.
  * No fabricated function names, parameters, or example outputs — every
    example block in INTEGRATION.md must reference a real function in
    scripts/query_corpus.py with parameters that actually exist.

Exits 0 on success, non-zero with a diagnostic on the first failed assertion.
"""
from __future__ import annotations

import inspect
import pathlib
import re
import shutil
import sqlite3
import subprocess
import sys
import tempfile

WORKSPACE = pathlib.Path(__file__).resolve().parent.parent
DB_PATH = WORKSPACE / "corpus.sqlite"
INTEGRATION_MD = WORKSPACE / "INTEGRATION.md"
QUERY_CORPUS = WORKSPACE / "scripts" / "query_corpus.py"
EXAMPLES_DIR = WORKSPACE / "examples"


def _fail(msg: str) -> None:
    print(f"INTEGRITY CHECK FAIL: {msg}", file=sys.stderr)
    sys.exit(2)


def _open_ro_db() -> sqlite3.Connection:
    """Open the DB read-only. Copies to a temp file when the live DB has
    been opened by an external writer (FUSE mount path), to avoid the
    "attempt to write a readonly database" error on journal recovery."""
    if not DB_PATH.exists():
        _fail(f"corpus.sqlite missing at {DB_PATH}")
    # Always copy to a sandbox-writable temp path so SQLite's auto-journal
    # recovery has somewhere to land.
    tmp_dir = pathlib.Path(tempfile.mkdtemp(prefix="b0512_check_"))
    tmp_db = tmp_dir / "corpus.sqlite"
    shutil.copy(DB_PATH, tmp_db)
    return sqlite3.connect(f"file:{tmp_db}?mode=ro&immutable=1", uri=True)


def main() -> int:
    asserts: list[str] = []

    # 1. Files exist
    for p in (INTEGRATION_MD, EXAMPLES_DIR, QUERY_CORPUS):
        if not p.exists():
            _fail(f"required path missing: {p}")
        asserts.append(f"exists: {p.relative_to(WORKSPACE)}")

    # 2. INTEGRATION.md basic shape — required headings present
    md = INTEGRATION_MD.read_text(encoding="utf-8")
    required_headings = [
        "## Quick start",
        "## Data coverage summary",
        "## API reference",
        "### `search`",
        "### `get_by_id`",
        "### `citations_of`",
        "### `cited_by`",
        "### `judge_profile`",
        "### `statute_interpretation`",
        "## Limitations",
        "## Example scripts",
    ]
    for h in required_headings:
        if h not in md:
            _fail(f"INTEGRATION.md missing required heading: {h!r}")
        asserts.append(f"heading present: {h}")

    # 3. Every API function name documented in INTEGRATION.md must
    #    actually exist in scripts/query_corpus.py with the documented
    #    parameter set.
    sys.path.insert(0, str(WORKSPACE / "scripts"))
    import query_corpus as q

    expected_api = {
        "search": {"query", "type", "court", "year_from", "year_to", "limit", "db_path"},
        "get_by_id": {"record_id", "db_path"},
        "citations_of": {"record_id", "db_path"},
        "cited_by": {"record_id", "db_path"},
        "judge_profile": {"judge_name", "db_path"},
        "statute_interpretation": {"act_id", "db_path"},
    }
    for fn_name, expected_params in expected_api.items():
        if not hasattr(q, fn_name):
            _fail(f"query_corpus has no function '{fn_name}'")
        sig = inspect.signature(getattr(q, fn_name))
        actual = set(sig.parameters.keys())
        missing = expected_params - actual
        if missing:
            _fail(
                f"query_corpus.{fn_name} is missing parameters {sorted(missing)} "
                f"(actual: {sorted(actual)})"
            )
        asserts.append(f"{fn_name}{tuple(sorted(actual))}")

    # 4. Live-counts reproduce.
    conn = _open_ro_db()
    counts = {
        "total_records": conn.execute("SELECT COUNT(*) FROM records").fetchone()[0],
        "fts_rows":      conn.execute("SELECT COUNT(*) FROM records_fts").fetchone()[0],
        "act":           conn.execute("SELECT COUNT(*) FROM records WHERE type='act'").fetchone()[0],
        "si":            conn.execute("SELECT COUNT(*) FROM records WHERE type='si'").fetchone()[0],
        "judgment":      conn.execute("SELECT COUNT(*) FROM records WHERE type='judgment'").fetchone()[0],
        "citations":     conn.execute("SELECT COUNT(*) FROM citations").fetchone()[0],
        "parent_act":    conn.execute("SELECT COUNT(*) FROM citations WHERE relation='parent_act'").fetchone()[0],
        "repealed_by":   conn.execute("SELECT COUNT(*) FROM citations WHERE relation='repealed_by'").fetchone()[0],
        "concourt":      conn.execute("SELECT COUNT(*) FROM judgments_meta WHERE court='Constitutional Court of Zambia'").fetchone()[0],
        "scz":           conn.execute("SELECT COUNT(*) FROM judgments_meta WHERE court='Supreme Court of Zambia'").fetchone()[0],
    }
    md_must_contain = {
        f"Acts (`type='act'`) | {counts['act']:,}":      counts['act'],
        f"Statutory Instruments (`type='si'`) | {counts['si']:,}": counts['si'],
        f"Judgments (`type='judgment'`) | {counts['judgment']:,}": counts['judgment'],
        f"**Total** | **{counts['total_records']:,}**":  counts['total_records'],
        f"`records_fts` row count = {counts['fts_rows']:,}": counts['fts_rows'],
        f"Constitutional Court of Zambia | {counts['concourt']:,}": counts['concourt'],
        f"Supreme Court of Zambia | {counts['scz']:,}": counts['scz'],
        f"`parent_act` (SI → Act) | {counts['parent_act']:,}": counts['parent_act'],
        f"`repealed_by` (Act → Act) | {counts['repealed_by']:,}": counts['repealed_by'],
    }
    for needle, val in md_must_contain.items():
        if needle not in md:
            _fail(
                f"INTEGRATION.md does not contain expected coverage line "
                f"(value={val}): {needle!r}"
            )
        asserts.append(f"live count reproduces: {needle}")

    # 5. No regression on row counts vs Phase 6 baselines.
    #    Phase 6 b0509 baseline: records=1791, records_fts=1791, citations=221.
    #    Phase 7 may grow these (judgment-ingestion-worker can add records),
    #    so we assert ">=" not "==".
    if counts["total_records"] < 1791:
        _fail(f"records regression: {counts['total_records']} < 1791")
    if counts["fts_rows"] < 1791:
        _fail(f"records_fts regression: {counts['fts_rows']} < 1791")
    if counts["citations"] < 221:
        _fail(f"citations regression: {counts['citations']} < 221")
    asserts.append(f"records>={1791}: {counts['total_records']}")
    asserts.append(f"records_fts>={1791}: {counts['fts_rows']}")
    asserts.append(f"citations>={221}: {counts['citations']}")

    # 6. Example scripts run without error and produce non-empty output.
    example_runs = [
        ([sys.executable, str(EXAMPLES_DIR / "corpus_search.py"),
          "shareholder", "--type", "judgment", "--limit", "3"], "search-judgment"),
        ([sys.executable, str(EXAMPLES_DIR / "corpus_search.py"),
          "electoral", "--type", "si", "--limit", "3"], "search-si"),
        ([sys.executable, str(EXAMPLES_DIR / "statute_interpretations.py"),
          "act-zm-2017-010-companies", "--limit", "5"], "stat-companies"),
    ]
    for argv, label in example_runs:
        try:
            res = subprocess.run(
                argv, capture_output=True, text=True, timeout=60, cwd=str(WORKSPACE),
            )
        except subprocess.TimeoutExpired:
            _fail(f"example {label!r} timed out")
        if res.returncode != 0:
            _fail(
                f"example {label!r} exited with {res.returncode}; "
                f"stderr: {res.stderr[:400]!r}"
            )
        if not res.stdout.strip():
            _fail(f"example {label!r} produced empty stdout")
        asserts.append(f"example runs cleanly: {label} ({len(res.stdout)} chars stdout)")

    # 7. Spot-check: no fabricated id in INTEGRATION.md examples.
    #    Pull every record-id-shaped token from the markdown and confirm
    #    it resolves in the corpus.
    id_pattern = re.compile(r"\b(act|si|judgment)-zm-[a-z0-9-]{6,}", re.IGNORECASE)
    candidates = set(id_pattern.findall(md))  # captures only the prefix word
    # Re-run to capture full ids:
    candidates = set(re.findall(r"(?:act|si|judgment)-zm-[a-z0-9-]+", md, re.IGNORECASE))
    # Strip trailing punctuation
    candidates = {c.rstrip("`).,;:") for c in candidates}
    if not candidates:
        _fail("INTEGRATION.md contains no example record ids — suspicious")
    cur = conn.execute("SELECT id FROM records")
    real_ids = {r[0] for r in cur.fetchall()}
    bogus = [c for c in sorted(candidates) if c not in real_ids]
    if bogus:
        _fail(
            "INTEGRATION.md cites record ids not found in corpus.sqlite: "
            f"{bogus}"
        )
    asserts.append(f"all {len(candidates)} cited record ids resolve in corpus")

    print(f"INTEGRITY CHECK PASS — {len(asserts)} assertions over Phase 7 batch 1")
    for a in asserts:
        print(f"  ok: {a}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
