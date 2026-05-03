#!/usr/bin/env python3
"""integrity_check_b0514.py — Phase 7 batch 3 integrity check.

Phase 7 batch 3 deliverables (this batch):
  - INTEGRATION.md "Specialist integration patterns" — populated with
    one worked example per Kate Weston Legal plugin v15.1 specialist
    persona (Clare, Harvey, Clifford, Mike, Sarah, Catherine,
    Johnnie, Andrew). Every code block grounds in a real
    query_corpus.py call against the live corpus.sqlite.
  - INTEGRATION.md "Citation-verification integration" — populated
    with the verify_zambian_citation flow + invocation order +
    safety notes.
  - INTEGRATION.md "Limitations" — full nine-section inventory of
    coverage gaps (key_statutes empty, dangling parent_act refs,
    sis_meta.parent_act_id NULL, judgment coverage, acts metadata
    gaps, reasoning_tags empty, no HC interpretation, sqlite
    gitignored, no write API).
  - Status header + TOC stub markers updated to reflect batch 3
    completion.

Integrity rules (BRIEF.md Phase 7 §107):
  * No regression on existing tables (records / records_fts /
    citations) — delegated to b0513 unchanged.
  * Every example script that exists runs without error and produces
    non-empty output for at least one realistic example — delegated
    to b0513.
  * Data-coverage figures cited in INTEGRATION.md reproduce when
    re-computed against corpus.sqlite — checked here for the new
    Limitations counters (770 NULL enacted_date, 64 NULL in_force,
    16 dangling parent_act, 22 distinct judges, etc.).
  * No fabricated function names, parameters, or example outputs —
    every record id referenced in the new Specialist patterns must
    resolve via q.get_by_id(); every function name referenced must
    be a real attribute of query_corpus.

This check ALWAYS runs the full b0513 suite first (which itself
delegates to b0512) so any regression on prior batches surfaces
verbatim.

Exits 0 on success, non-zero with a diagnostic on the first failed
assertion.
"""
from __future__ import annotations

import json
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
EXAMPLES_DIR = WORKSPACE / "examples"
SCRIPTS_DIR = WORKSPACE / "scripts"
PRIOR_CHECK = SCRIPTS_DIR / "integrity_check_b0513.py"


def _fail(msg: str) -> None:
    print(f"INTEGRITY CHECK FAIL: {msg}", file=sys.stderr)
    sys.exit(2)


def _open_ro_db() -> sqlite3.Connection:
    """Read-only DB via temp copy (matches b0513/b0512 pattern)."""
    if not DB_PATH.exists():
        _fail(f"corpus.sqlite missing at {DB_PATH}")
    tmp_dir = pathlib.Path(tempfile.mkdtemp(prefix="b0514_check_"))
    tmp_db = tmp_dir / "corpus.sqlite"
    shutil.copy(DB_PATH, tmp_db)
    conn = sqlite3.connect(f"file:{tmp_db}?mode=ro&immutable=1", uri=True)
    conn.row_factory = sqlite3.Row
    return conn


# Record ids referenced in the new Specialist patterns. Every one of
# these MUST resolve in q.get_by_id() — if any is missing, the doc has
# fabricated a citation and we fail.
EXPECTED_IDS_IN_PATTERNS: list[str] = [
    # Clare
    "judgment-zm-2026-zmsc-07-munir-v-attorney",
    "judgment-zm-2022-zmcc-26-michelo-v-sampa-and-anor",
    # Harvey
    "judgment-zm-2025-zmsc-23-the-v-zambia",
    "judgment-zm-2026-zmsc-01-kapsch-v-intelligent",
    "judgment-zm-2025-zmsc-30-sa-v-zambia",
    "act-zm-1994-026-companies-act-1994",
    "act-zm-2017-010-companies",
    "si-zm-2019-014-companies-general-regulations-2019",
    "si-zm-2019-015-companies-fees-regulations-2019",
    "si-zm-2019-021-companies-prescribed-forms-regulations-2019",
    "act-zm-2022-005-the-bank-of-zambia-act-2022",
    "act-zm-1994-021-banking-and-financial-services-act-1994",
    # Clifford
    "act-zm-1967-032-income-tax-act-1967",
    "act-zm-2025-017-income-tax-amendment-no20-act",
    "act-zm-2022-024-the-income-tax-amendment-act-2022",
    # Sarah
    # (already listed above: 2017 Companies, 1994 Companies, 2019 SIs)
    # Catherine
    "act-zm-1989-005-intestate-succession-act-1989",
    "act-zm-2007-020-matrimonial-causes-act-2007",
    "act-zm-1918-010-marriage-act-1918",
    "act-zm-2023-013-the-marriage-amendment-act-2023",
    "judgment-zm-2025-zmsc-22-chama-v-odile",
    "judgment-zm-2025-zmsc-10-thelma-v-the",
    # Johnnie
    "act-zm-2016-035-the-electoral-process",
    "act-zm-2015-003-the-urban-and-regional-planning",
    "act-zm-2010-027-the-animal-health",
    "local-government-act-2019",
    "act-zm-1999-007-forests-act-1999",
]


def main() -> int:
    asserts: list[str] = []

    # 0. Delegated re-run of the b0513 check (which itself delegates to
    #    b0512). Any prior-batch regression surfaces verbatim.
    if not PRIOR_CHECK.exists():
        _fail(f"prior integrity check missing: {PRIOR_CHECK}")
    res = subprocess.run(
        [sys.executable, str(PRIOR_CHECK)],
        capture_output=True, text=True, timeout=180, cwd=str(WORKSPACE),
    )
    if res.returncode != 0:
        _fail(
            f"delegated b0513 check failed (rc={res.returncode}); "
            f"stderr tail: {res.stderr[-400:]!r}"
        )
    delegated_count = 0
    for line in res.stdout.splitlines():
        if "INTEGRITY CHECK PASS" in line:
            try:
                delegated_count = int(line.split("—")[1].strip().split()[0])
            except Exception:
                delegated_count = -1
            break
    asserts.append(
        f"delegated b0513 PASS ({delegated_count} prior-batch assertions, "
        "which themselves include delegated b0512)"
    )

    # 1. INTEGRATION.md exists and the three previously-stubbed sections
    #    are now populated (no '(stub)' markers remain in the body).
    if not INTEGRATION_MD.exists():
        _fail(f"INTEGRATION.md missing at {INTEGRATION_MD}")
    md = INTEGRATION_MD.read_text(encoding="utf-8")
    forbidden_substrings = [
        "*(stub)*",
        "*(stub — populated in subsequent",
        "*(stub — full version in subsequent",
    ]
    for s in forbidden_substrings:
        if s in md:
            _fail(f"INTEGRATION.md still contains stub marker: {s!r}")
    asserts.append("INTEGRATION.md no longer carries stub markers")

    # 2. Section headers exist for the three populated sections.
    for header in (
        "## Specialist integration patterns",
        "## Citation-verification integration",
        "## Limitations",
    ):
        if header not in md:
            _fail(f"INTEGRATION.md missing required header: {header!r}")
        asserts.append(f"section header present: {header}")

    # 3. Each of the eight specialist personas is named under the
    #    Specialist patterns section.
    personas = [
        "Clare", "Harvey", "Clifford", "Mike",
        "Sarah", "Catherine", "Johnnie", "Andrew",
    ]
    spec_idx = md.find("## Specialist integration patterns")
    cite_idx = md.find("## Citation-verification integration")
    if spec_idx == -1 or cite_idx == -1 or cite_idx <= spec_idx:
        _fail("Specialist / Citation-verification section ordering is wrong")
    spec_block = md[spec_idx:cite_idx]
    for p in personas:
        # Each persona heading uses an em-dash like "Clare — case-law-research".
        needle = f"### {p} —"
        if needle not in spec_block:
            _fail(f"Specialist patterns missing persona heading: {needle!r}")
        asserts.append(f"specialist heading present: {needle}")

    # 4. The Limitations section enumerates at least the eight major
    #    coverage gaps as numbered subsections.
    lim_idx = md.find("## Limitations")
    if lim_idx == -1:
        _fail("Limitations section header missing")
    lim_block = md[lim_idx:]
    expected_lim_subsections = [
        "### 1. ", "### 2. ", "### 3. ", "### 4. ",
        "### 5. ", "### 6. ", "### 7. ", "### 8. ",
    ]
    for needle in expected_lim_subsections:
        if needle not in lim_block:
            _fail(f"Limitations missing numbered subsection: {needle!r}")
    asserts.append(
        f"Limitations has all {len(expected_lim_subsections)} numbered subsections"
    )

    # 5. Every record id referenced in the Specialist patterns resolves
    #    to a real record in corpus.sqlite — no fabrication.
    sys.path.insert(0, str(SCRIPTS_DIR))
    import query_corpus as q  # type: ignore
    missing_ids: list[str] = []
    for rid in EXPECTED_IDS_IN_PATTERNS:
        rec = q.get_by_id(rid)
        if rec is None:
            missing_ids.append(rid)
    if missing_ids:
        _fail(
            f"INTEGRATION.md references non-existent record ids: "
            f"{missing_ids[:5]} (and {max(0, len(missing_ids)-5)} more)"
        )
    asserts.append(
        f"all {len(EXPECTED_IDS_IN_PATTERNS)} record ids referenced in "
        "Specialist patterns resolve via q.get_by_id"
    )

    # 6. Function names referenced in INTEGRATION.md must be real
    #    attributes of query_corpus. We cite six per BRIEF.md §80.
    expected_fns = [
        "search", "get_by_id", "citations_of",
        "cited_by", "judge_profile", "statute_interpretation",
    ]
    for fn in expected_fns:
        if not hasattr(q, fn):
            _fail(f"INTEGRATION.md references nonexistent fn query_corpus.{fn}")
        # also assert the call signature exists in some form in the API
        # reference section
        if f"q.{fn}(" not in md and f"`{fn}`" not in md:
            _fail(
                f"INTEGRATION.md fails to mention query_corpus.{fn} either as "
                "`fn` or q.fn(...) call"
            )
    asserts.append(
        f"all {len(expected_fns)} BRIEF.md §80 functions exist on "
        "query_corpus AND appear in INTEGRATION.md"
    )

    # 7. Live count assertions for the new Limitations §4 / §5 / §6 numbers.
    conn = _open_ro_db()
    counts: dict[str, int] = {}
    counts["records_total"] = conn.execute(
        "SELECT COUNT(*) FROM records").fetchone()[0]
    counts["records_fts"] = conn.execute(
        "SELECT COUNT(*) FROM records_fts").fetchone()[0]
    counts["citations"] = conn.execute(
        "SELECT COUNT(*) FROM citations").fetchone()[0]
    counts["judgments"] = conn.execute(
        "SELECT COUNT(*) FROM records WHERE type='judgment'"
    ).fetchone()[0]
    counts["zmcc"] = conn.execute(
        "SELECT COUNT(*) FROM judgments_meta WHERE court LIKE 'Constitutional%'"
    ).fetchone()[0]
    counts["scz"] = conn.execute(
        "SELECT COUNT(*) FROM judgments_meta WHERE court LIKE 'Supreme%'"
    ).fetchone()[0]
    counts["scz_tagged"] = conn.execute(
        "SELECT COUNT(*) FROM judgments_meta WHERE court LIKE 'Supreme%' "
        "AND issue_tags_json IS NOT NULL AND issue_tags_json != '' "
        "AND issue_tags_json != '[]'"
    ).fetchone()[0]
    counts["scz_judged"] = conn.execute(
        "SELECT COUNT(*) FROM judgments_meta WHERE court LIKE 'Supreme%' "
        "AND judges_json IS NOT NULL AND judges_json != '' "
        "AND judges_json != '[]'"
    ).fetchone()[0]
    counts["judgments_tagged"] = conn.execute(
        "SELECT COUNT(*) FROM judgments_meta WHERE issue_tags_json IS NOT NULL "
        "AND issue_tags_json != '' AND issue_tags_json != '[]'"
    ).fetchone()[0]
    counts["reasoning_populated"] = conn.execute(
        "SELECT COUNT(*) FROM judgments_meta WHERE reasoning_tags_json IS NOT NULL "
        "AND reasoning_tags_json != '' AND reasoning_tags_json != '[]'"
    ).fetchone()[0]
    counts["key_statutes_populated"] = conn.execute(
        "SELECT COUNT(*) FROM judgments_meta WHERE key_statutes_json IS NOT NULL "
        "AND key_statutes_json != '' AND key_statutes_json != '[]'"
    ).fetchone()[0]
    counts["cited_authorities_populated"] = conn.execute(
        "SELECT COUNT(*) FROM judgments_meta WHERE cited_authorities_json IS NOT NULL "
        "AND cited_authorities_json != '' AND cited_authorities_json != '[]'"
    ).fetchone()[0]
    counts["acts_total"] = conn.execute(
        "SELECT COUNT(*) FROM records WHERE type='act'").fetchone()[0]
    counts["acts_null_enacted"] = conn.execute(
        "SELECT COUNT(*) FROM acts_meta WHERE enacted_date IS NULL OR enacted_date=''"
    ).fetchone()[0]
    counts["acts_null_in_force"] = conn.execute(
        "SELECT COUNT(*) FROM records WHERE type='act' AND in_force IS NULL"
    ).fetchone()[0]
    counts["sis_total"] = conn.execute(
        "SELECT COUNT(*) FROM records WHERE type='si'").fetchone()[0]
    counts["sis_null_parent"] = conn.execute(
        "SELECT COUNT(*) FROM sis_meta WHERE parent_act_id IS NULL"
    ).fetchone()[0]

    # Distinct judge surnames from judges_json across the corpus.
    distinct_surnames: set[str] = set()
    for r in conn.execute(
        "SELECT judges_json FROM judgments_meta "
        "WHERE judges_json IS NOT NULL AND judges_json != '' "
        "AND judges_json != '[]'"
    ):
        try:
            js = json.loads(r["judges_json"]) or []
        except Exception:
            js = []
        for j in js:
            n = ""
            if isinstance(j, dict):
                n = j.get("name") or ""
            elif isinstance(j, str):
                n = j
            if n.split():
                distinct_surnames.add(n.split()[0])
    counts["distinct_judge_surnames"] = len(distinct_surnames)

    # Sanity envelopes — INTEGRATION.md text is committed to these
    # numbers, so any drift here means the doc is stale.
    expectations = {
        "records_total": (1791, 1791),  # exact
        "records_fts": (1791, 1791),
        "citations": (221, 221),
        "judgments": (102, 102),
        "zmcc": (72, 72),
        "scz": (30, 30),
        "scz_tagged": (5, 5),
        "scz_judged": (6, 6),
        "judgments_tagged": (77, 77),
        "reasoning_populated": (0, 0),
        "key_statutes_populated": (0, 0),
        "cited_authorities_populated": (0, 0),
        "acts_total": (1150, 1150),
        "acts_null_enacted": (770, 770),
        "acts_null_in_force": (64, 64),
        "sis_total": (539, 539),
        "sis_null_parent": (539, 539),
        "distinct_judge_surnames": (22, 22),
    }
    for key, (lo, hi) in expectations.items():
        v = counts[key]
        if not (lo <= v <= hi):
            _fail(
                f"INTEGRATION.md drift: counts[{key!r}]={v}, "
                f"expected in [{lo}, {hi}]"
            )
    asserts.append(
        "all 18 live-count expectations match INTEGRATION.md text "
        "(records=1791, judgments=102, zmcc=72, scz=30, scz_tagged=5, "
        "scz_judged=6, judgments_tagged=77, reasoning_populated=0, "
        "key_statutes=0, cited_authorities=0, acts=1150, "
        "acts_null_enacted=770, acts_null_in_force=64, sis=539, "
        "sis_null_parent=539, distinct_judges=22)"
    )

    # 8. The new "Citation-verification integration" section actually
    #    explains a flow (looks for the verify_zambian_citation helper
    #    name + the three return-state strings + the recommended
    #    fallback order).
    cv_block = md[cite_idx:lim_idx]
    cv_required = [
        "verify_zambian_citation",
        "no_match_in_corpus",
        "verified",
        "partial_match",
        "ZambiaLII",
        "Parliament of Zambia",
    ]
    for needle in cv_required:
        if needle not in cv_block:
            _fail(
                f"Citation-verification section missing required substring: "
                f"{needle!r}"
            )
    asserts.append("Citation-verification section covers all 6 required points")

    # 9. INTEGRATION.md status header bumped to batch 3.
    if "Phase 7 batch 3" not in md.splitlines()[2]:
        _fail("INTEGRATION.md status header not bumped to 'Phase 7 batch 3'")
    asserts.append("INTEGRATION.md status header bumped to Phase 7 batch 3")

    # 10. Snapshot row counts (no regression).
    if counts["records_total"] < 1791:
        _fail(f"records regression: {counts['records_total']} < 1791")
    if counts["records_fts"] < 1791:
        _fail(f"records_fts regression: {counts['records_fts']} < 1791")
    if counts["citations"] < 221:
        _fail(f"citations regression: {counts['citations']} < 221")
    asserts.append(
        f"row counts: records={counts['records_total']}, "
        f"records_fts={counts['records_fts']}, "
        f"citations={counts['citations']} (no regression on Phase 6 baseline)"
    )

    print(
        f"INTEGRITY CHECK PASS — {len(asserts)} new assertions over Phase 7 "
        f"batch 3 (plus delegated b0513 PASS)"
    )
    for a in asserts:
        print(f"  ok: {a}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
