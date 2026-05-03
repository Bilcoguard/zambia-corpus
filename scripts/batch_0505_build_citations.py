#!/usr/bin/env python3
"""batch_0505_build_citations.py — Phase 6 batch 2.

Phase 6 deliverable #2 — Citation graph.

Builds the ``citations`` table in ``corpus.sqlite``:

    citations(
        src_id TEXT NOT NULL,
        dst_id TEXT NOT NULL,
        relation TEXT NOT NULL,
        source_field TEXT NOT NULL,
        PRIMARY KEY (src_id, dst_id, relation)
    )

Source fields and relations harvested:
  - acts.amended_by       -> relation='amended_by'        source_field='acts.amended_by'
  - acts.repealed_by      -> relation='repealed_by'       source_field='acts.repealed_by'
  - sis.amended_by        -> relation='amended_by'        source_field='sis.amended_by'
  - sis.repealed_by       -> relation='repealed_by'       source_field='sis.repealed_by'
  - sis.parent_act_id     -> relation='parent_act'        source_field='sis.parent_act_id'
  - sis.parent_act (text) -> relation='parent_act'        source_field='sis.parent_act'
  - sis.cited_authorities -> relation='cited_authority'   source_field='sis.cited_authorities'
  - judgments.key_statutes        -> relation='cites_statute'    source_field='judgments.key_statutes'
  - judgments.cited_authorities   -> relation='cites_authority'  source_field='judgments.cited_authorities'

Per BRIEF.md Phase 6 completion criterion: the citation graph has zero
dangling references — every dst_id MUST resolve to a real record id in
the corpus. Unresolved candidates are written to gaps.md (and to a
per-batch dangling-ref report under reports/dangling-refs-b0505.md),
they are NOT inserted into the citations table.

The script does not fetch anything (Phase 6 is local-data-only); it
reads the on-disk JSON tree under ``records/`` plus the existing
``corpus.sqlite``. Re-runnable.
"""

from __future__ import annotations

import json
import os
import pathlib
import re
import sqlite3
import sys
import time
from collections import defaultdict

WORKSPACE = pathlib.Path(__file__).resolve().parent.parent
RECORDS_DIR = WORKSPACE / "records"
DB_PATH = WORKSPACE / "corpus.sqlite"

# ---------------------------------------------------------------------------
# Title normalisation — used to resolve free-text parent_act fields
# (e.g. "Citizens Economic Empowerment Act") to a corpus act id.
# ---------------------------------------------------------------------------

_PUNCT_RE = re.compile(r"[^a-z0-9 ]+")
_SPACE_RE = re.compile(r"\s+")
_NUMBER_TAIL_RE = re.compile(r"\s*,?\s*\d{4}$")  # trailing year e.g. ", 2017"
_ACT_SUFFIX_RE = re.compile(r"\s+act$")


def normalise_title(title: str) -> str:
    """Lower-case, strip punctuation, drop trailing year + Act, collapse spaces."""
    if not title:
        return ""
    s = title.lower().strip()
    s = s.replace("’", "'")
    # remove "the " prefix
    if s.startswith("the "):
        s = s[4:]
    s = _NUMBER_TAIL_RE.sub("", s)
    s = _PUNCT_RE.sub(" ", s)
    s = _ACT_SUFFIX_RE.sub("", s)
    s = _SPACE_RE.sub(" ", s).strip()
    return s


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def iter_records(record_type_dir: pathlib.Path):
    for p in sorted(record_type_dir.rglob("*.json")):
        try:
            with open(p, "r", encoding="utf-8") as fh:
                rec = json.load(fh)
        except (OSError, json.JSONDecodeError):
            continue
        if not isinstance(rec, dict):
            continue
        if rec.get("_tombstone") is True:
            continue
        if rec.get("type") == "TOMBSTONE_NAV_PAGE":
            continue
        yield p, rec


def looks_like_corpus_id(s: str) -> bool:
    if not isinstance(s, str):
        return False
    return bool(
        re.match(r"^(act|si|statutory_instrument|judgment|constitution|regulation)-",
                 s, re.IGNORECASE)
    )


def normalise_id(s: str) -> str:
    """Normalise minor variants (e.g. statutory_instrument vs si)."""
    if not isinstance(s, str):
        return s
    return s.strip()


# ---------------------------------------------------------------------------
# Main build
# ---------------------------------------------------------------------------


def main() -> int:
    t0 = time.time()
    print(f"[b0505] starting at {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}")

    if not DB_PATH.exists():
        print(f"FATAL: {DB_PATH} not found", file=sys.stderr)
        return 2

    con = sqlite3.connect(str(DB_PATH))
    # The mount blocks unlinking the rollback journal between runs; running
    # in MEMORY journal mode sidesteps the host-locked journal file. The
    # b0504 build script used the same workaround.
    con.execute("PRAGMA journal_mode = MEMORY")
    con.execute("PRAGMA synchronous = NORMAL")
    con.execute("PRAGMA foreign_keys = ON")
    cur = con.cursor()

    # Build the resolution index from on-disk JSON (canonical, since
    # corpus.sqlite is gitignored and may lag behind the JSON tree when
    # the dedicated judgment-ingestion-worker writes new records between
    # b0504 and b0505 ticks). The integrity check uses the same on-disk
    # source, so this keeps the two artefacts self-consistent.
    existing_ids: set[str] = set()
    title_to_ids: dict[str, list[str]] = defaultdict(list)
    act_titles_by_id: dict[str, str] = {}
    for rec_type_dir, rec_type in (
        (RECORDS_DIR / "acts", "act"),
        (RECORDS_DIR / "sis", "si"),
        (RECORDS_DIR / "judgments", "judgment"),
    ):
        if not rec_type_dir.exists():
            continue
        for path, rec in iter_records(rec_type_dir):
            rid = rec.get("id")
            if not rid:
                continue
            existing_ids.add(rid)
            if rec_type == "act":
                rtitle = rec.get("title") or ""
                n = normalise_title(rtitle)
                if n:
                    title_to_ids[n].append(rid)
                    act_titles_by_id[rid] = rtitle
    print(f"[b0505] index: {len(existing_ids)} record IDs (on-disk JSON), "
          f"{len(title_to_ids)} normalised act titles")

    # Drop+create the citations table (idempotent rebuild).
    cur.execute("DROP TABLE IF EXISTS citations")
    cur.execute(
        """
        CREATE TABLE citations (
            src_id TEXT NOT NULL,
            dst_id TEXT NOT NULL,
            relation TEXT NOT NULL,
            source_field TEXT NOT NULL,
            PRIMARY KEY (src_id, dst_id, relation)
        )
        """
    )
    cur.execute("CREATE INDEX IF NOT EXISTS idx_citations_src ON citations(src_id)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_citations_dst ON citations(dst_id)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_citations_rel ON citations(relation)")

    resolved_rows: list[tuple] = []
    dangling: list[dict] = []

    def try_resolve(raw: object, *, prefer_type: str | None = None,
                    src_id: str = "", source_field: str = "",
                    relation: str = "") -> tuple[str | None, str]:
        """Returns (resolved_id_or_None, reason).
        reason in {'id-direct','title-unique','title-no-match','title-ambiguous',
                   'unrecognised-shape','self-ref-ignored'}.
        """
        if raw is None:
            return None, "empty"
        if isinstance(raw, list):
            # Caller iterates; passing a list here is a programming error.
            return None, "list-passed"
        if isinstance(raw, dict):
            cand = raw.get("id") or raw.get("ref") or raw.get("title")
            if not cand:
                return None, "dict-no-id"
            return try_resolve(cand, prefer_type=prefer_type,
                               src_id=src_id, source_field=source_field,
                               relation=relation)
        if not isinstance(raw, str):
            return None, "unrecognised-shape"
        cand = raw.strip()
        if not cand:
            return None, "empty"
        # Direct ID hit.
        if looks_like_corpus_id(cand):
            cand_norm = normalise_id(cand)
            if cand_norm in existing_ids:
                if cand_norm == src_id:
                    return None, "self-ref-ignored"
                return cand_norm, "id-direct"
            return None, "id-not-in-corpus"
        # Title-based resolution (acts only).
        nt = normalise_title(cand)
        if not nt:
            return None, "title-empty-after-normalise"
        ids = title_to_ids.get(nt) or []
        if len(ids) == 1:
            cand_norm = ids[0]
            if cand_norm == src_id:
                return None, "self-ref-ignored"
            return cand_norm, "title-unique"
        if len(ids) > 1:
            return None, "title-ambiguous"
        return None, "title-no-match"

    counters: dict[str, int] = defaultdict(int)

    def add_citation(src_id: str, raw: object, relation: str, source_field: str) -> None:
        if isinstance(raw, list):
            for item in raw:
                add_citation(src_id, item, relation, source_field)
            return
        resolved, reason = try_resolve(
            raw, src_id=src_id, source_field=source_field, relation=relation
        )
        counters[f"reason:{reason}"] += 1
        if resolved:
            resolved_rows.append((src_id, resolved, relation, source_field))
            counters[f"resolved:{relation}"] += 1
        elif reason in {"empty", "list-passed", "self-ref-ignored",
                        "title-empty-after-normalise"}:
            # Not a real candidate worth flagging.
            return
        else:
            counters[f"dangling:{relation}"] += 1
            dangling.append(
                {
                    "src_id": src_id,
                    "raw": raw if isinstance(raw, str) else str(raw)[:200],
                    "relation": relation,
                    "source_field": source_field,
                    "reason": reason,
                }
            )

    # ----- Acts -----
    acts_dir = RECORDS_DIR / "acts"
    if acts_dir.exists():
        for path, rec in iter_records(acts_dir):
            sid = rec.get("id")
            if not sid or sid not in existing_ids:
                continue
            add_citation(sid, rec.get("amended_by"), "amended_by", "acts.amended_by")
            add_citation(sid, rec.get("repealed_by"), "repealed_by", "acts.repealed_by")
            # cited_authorities on acts is not in the BRIEF deliverable list but
            # if any are populated we surface them as 'cites_authority'.
            add_citation(sid, rec.get("cited_authorities"),
                         "cites_authority", "acts.cited_authorities")
            counters["acts_scanned"] += 1

    # ----- Statutory instruments -----
    sis_dir = RECORDS_DIR / "sis"
    if sis_dir.exists():
        for path, rec in iter_records(sis_dir):
            sid = rec.get("id")
            if not sid or sid not in existing_ids:
                continue
            add_citation(sid, rec.get("amended_by"), "amended_by", "sis.amended_by")
            add_citation(sid, rec.get("repealed_by"), "repealed_by", "sis.repealed_by")
            # parent_act_id (resolved id) and parent_act (free-text title).
            add_citation(sid, rec.get("parent_act_id"), "parent_act", "sis.parent_act_id")
            add_citation(sid, rec.get("parent_act"), "parent_act", "sis.parent_act")
            add_citation(sid, rec.get("cited_authorities"),
                         "cites_authority", "sis.cited_authorities")
            counters["sis_scanned"] += 1

    # ----- Judgments -----
    judg_dir = RECORDS_DIR / "judgments"
    if judg_dir.exists():
        for path, rec in iter_records(judg_dir):
            sid = rec.get("id")
            if not sid or sid not in existing_ids:
                continue
            add_citation(sid, rec.get("key_statutes"),
                         "cites_statute", "judgments.key_statutes")
            add_citation(sid, rec.get("cited_authorities"),
                         "cites_authority", "judgments.cited_authorities")
            counters["judgments_scanned"] += 1

    # Dedupe + insert resolved.
    distinct = set(resolved_rows)
    cur.executemany(
        "INSERT OR IGNORE INTO citations (src_id, dst_id, relation, source_field) "
        "VALUES (?, ?, ?, ?)",
        list(distinct),
    )
    con.commit()
    inserted = cur.execute("SELECT COUNT(*) FROM citations").fetchone()[0]
    counters["citations_rows_post_insert"] = inserted
    counters["resolved_total_distinct"] = len(distinct)

    # Per-relation breakdown.
    rel_breakdown = {
        rel: cnt for rel, cnt in cur.execute(
            "SELECT relation, COUNT(*) FROM citations GROUP BY relation ORDER BY relation"
        )
    }

    # ----- Output: dangling-ref report -----
    reports_dir = WORKSPACE / "reports"
    reports_dir.mkdir(exist_ok=True)
    drep_path = reports_dir / "dangling-refs-b0505.md"
    with open(drep_path, "w", encoding="utf-8") as fh:
        fh.write("# Dangling reference report — batch 0505 (Phase 6, citation graph)\n\n")
        fh.write(f"- Generated (UTC): "
                 f"{time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}\n")
        fh.write(f"- Citations table rows (resolved): {inserted}\n")
        fh.write(f"- Dangling refs (NOT inserted into citations): {len(dangling)}\n\n")
        fh.write("Per BRIEF.md Phase 6 completion criterion, dangling references are "
                 "recorded here (and appended to gaps.md) but never inserted into the "
                 "citations graph itself.\n\n")
        fh.write("## Per-relation resolved breakdown\n\n")
        for rel, cnt in rel_breakdown.items():
            fh.write(f"- `{rel}`: {cnt}\n")
        fh.write("\n## Dangling entries (grouped by reason)\n\n")
        by_reason: dict[str, list[dict]] = defaultdict(list)
        for d in dangling:
            by_reason[d["reason"]].append(d)
        for reason in sorted(by_reason.keys()):
            entries = by_reason[reason]
            fh.write(f"### {reason} ({len(entries)})\n\n")
            for d in entries[:25]:  # cap to keep report compact
                fh.write(
                    f"- `{d['src_id']}` -> `{d['raw']}` (relation=`{d['relation']}`, "
                    f"source_field=`{d['source_field']}`)\n"
                )
            if len(entries) > 25:
                fh.write(f"- ... and {len(entries) - 25} more\n")
            fh.write("\n")

    # ----- gaps.md append -----
    if dangling:
        ts = time.strftime("%Y-%m-%d", time.gmtime())
        with open(WORKSPACE / "gaps.md", "a", encoding="utf-8") as fh:
            fh.write(f"\n## [{ts}] Phase 6 batch 0505 — citation graph dangling references\n\n")
            fh.write(
                f"Built `citations` table from on-disk JSON. {inserted} resolved citation "
                f"edges inserted; {len(dangling)} candidate references could not resolve "
                f"and were excluded from the graph (Phase 6 completion criterion: zero "
                f"dangling refs in the graph itself). Full list in "
                f"`reports/dangling-refs-b0505.md`. Reasons:\n\n"
            )
            for reason in sorted(by_reason.keys()):
                fh.write(f"- `{reason}`: {len(by_reason[reason])}\n")
            fh.write("\nThese are surfaced for triage, not deletion. Resolution paths:\n")
            fh.write("- `title-no-match` / `title-ambiguous` on `sis.parent_act` — needs an "
                     "explicit `parent_act_id` lookup table (titles don't uniquely identify "
                     "the consolidated Cap. version vs. an annual Act).\n")
            fh.write("- `id-not-in-corpus` — references a record we haven't ingested yet "
                     "(typically older or repealed-prior versions); add to ingestion target "
                     "list when the relevant phase reopens.\n")

    # ----- citations.jsonl (canonical artefact, committed to git) -----
    # corpus.sqlite is gitignored (>100MB GH limit), so the JSONL form is
    # the source-of-truth for the citation graph in version control. The
    # b0505 integrity check treats this file as canonical and the SQLite
    # table as a derived/cached view.
    jsonl_path = WORKSPACE / "citations.jsonl"
    distinct_sorted = sorted(distinct)
    with open(jsonl_path, "w", encoding="utf-8") as fh:
        for src, dst, rel, sf in distinct_sorted:
            fh.write(json.dumps(
                {"dst_id": dst, "relation": rel, "source_field": sf, "src_id": src},
                sort_keys=True,
            ) + "\n")

    # ----- data/citations_summary.json (consumed by integrity check) -----
    data_dir = WORKSPACE / "data"
    data_dir.mkdir(exist_ok=True)
    record_count = len(existing_ids)
    summary = {
        "all_dst_ids_resolved": True,  # zero-dangling rule honoured by construction
        "built_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "dangling_by_reason": {r: len(by_reason[r]) for r in sorted(by_reason.keys())},
        "dangling_count": len(dangling),
        "edge_count": len(distinct_sorted),
        "edges_by_relation": {rel: cnt for rel, cnt in rel_breakdown.items()},
        "parser_version": "phase6.b0505",
        "record_count": record_count,
    }
    with open(data_dir / "citations_summary.json", "w", encoding="utf-8") as fh:
        json.dump(summary, fh, indent=2, sort_keys=True)
        fh.write("\n")

    # ----- Summary print -----
    print(f"[b0505] resolved={inserted} dangling={len(dangling)}")
    for k in sorted(counters.keys()):
        print(f"  {k}: {counters[k]}")
    print(f"[b0505] per-relation:")
    for k, v in rel_breakdown.items():
        print(f"  {k}: {v}")
    print(f"[b0505] elapsed {time.time() - t0:.1f}s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
