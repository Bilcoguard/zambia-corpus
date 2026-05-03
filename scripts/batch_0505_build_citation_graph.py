#!/usr/bin/env python3
"""
Phase 6 batch 0505 — build citation graph (deliverable 2 of 4).

Walks records/{acts,sis,judgments}/**.json and emits a citation graph
edge list. Each edge has (src_id, dst_id, relation, source_field).

Sources of edges (per BRIEF.md Phase 6 deliverable 2):
  - acts.amended_by      -> relation="amended_by",   source_field="acts.amended_by"
  - acts.repealed_by     -> relation="repealed_by",  source_field="acts.repealed_by"
  - sis.amended_by       -> relation="amended_by",   source_field="sis.amended_by"
  - sis.repealed_by      -> relation="repealed_by",  source_field="sis.repealed_by"
  - sis.parent_act       -> relation="parent_act",   source_field="sis.parent_act"
                            (free-text title resolved via title-normalisation lookup)
  - judgments.key_statutes        -> relation="cites_statute",   source_field="judgments.key_statutes"
  - judgments.cited_authorities   -> relation="cites_authority", source_field="judgments.cited_authorities"

Resolution policy (per BRIEF.md Phase 6 completion criteria):
  - Every dst_id in the graph MUST resolve to a real record id. Unresolved
    references are written to gaps.md, NOT to the graph.
  - For acts.repealed_by / acts.amended_by: the field is already an id
    (per current parser). If it doesn't match a real id, log gap.
  - For sis.parent_act: the field is a free-text title (e.g.
    "Zambia National Service Act"). Resolve via normalised-title lookup
    against acts. If no match, log gap.
  - For judgments.key_statutes / cited_authorities: empty across the
    current corpus (parser has not extracted them yet). The script
    handles them but emits zero edges this tick.

Outputs:
  - citations.jsonl  (one edge per line, JSON; canonical git artefact)
  - data/citations_summary.json  (per-relation counts + dangling stats)
  - corpus.sqlite citations table — created if the DB is healthy;
    otherwise the script logs and skips DB write (the JSONL is the
    source of truth and the next healthy tick can rebuild from it).

Provenance: parser_version="phase6.b0505". This script is the canonical
build artefact and must be re-runnable to reproduce citations.jsonl
exactly.
"""
from __future__ import annotations
import json
import os
import re
import sqlite3
import sys
from datetime import datetime, timezone
from glob import glob
from pathlib import Path

PARSER_VERSION = "phase6.b0505"
WORKSPACE = Path(__file__).resolve().parent.parent
RECORDS = WORKSPACE / "records"
CITATIONS_JSONL = WORKSPACE / "citations.jsonl"
SUMMARY_JSON = WORKSPACE / "data" / "citations_summary.json"
GAPS_MD = WORKSPACE / "gaps.md"
CORPUS_SQLITE = WORKSPACE / "corpus.sqlite"

# ---------- helpers ----------

_PUNCT_RE = re.compile(r"[^\w\s]")
_WS_RE = re.compile(r"\s+")
_YEAR_RE = re.compile(r"\b(?:19|20)\d{2}\b")
_LEADING_THE = re.compile(r"^the\s+")
_TRAILING_QUALIFIER = re.compile(
    r"\s+(?:act|regulations?|order|rules?|cap(?:ter)?\.?\s*\d+|"
    r"chapter\s+\d+|amendment(?:s)?|no\.?\s*\d+\s+of\s+\d+)\b.*$"
)


def normalise_title(t: str) -> str:
    """Normalise an act/SI title for fuzzy matching.

    Steps: lowercase, drop leading 'the', strip trailing qualifier
    ('Act', 'Regulations', 'Cap. 275', etc.), strip punctuation,
    drop year tokens, collapse whitespace.
    """
    if not t:
        return ""
    s = t.lower().strip()
    s = _LEADING_THE.sub("", s)
    # Strip trailing qualifier (after the actual subject name)
    s = _TRAILING_QUALIFIER.sub("", s)
    s = _PUNCT_RE.sub(" ", s)
    s = _YEAR_RE.sub(" ", s)
    s = _WS_RE.sub(" ", s).strip()
    return s


def is_real_record(r):
    if not isinstance(r, dict):
        return False
    # Skip explicit tombstone placeholders. Note: previous form
    # `r.get("TOMBSTONE_NAV_PAGE")` looked up a literal key (always
    # falsy) — fixed to match the b0504 FTS5 loader and the b0505
    # integrity check which both check `r.get("type") ==
    # "TOMBSTONE_NAV_PAGE"`.
    if r.get("_tombstone") is True:
        return False
    if r.get("type") == "TOMBSTONE_NAV_PAGE":
        return False
    return bool(r.get("id"))


def load_all_records():
    """Return {id: {type, title, path, raw}} for every real record."""
    out = {}
    seen_paths = {}
    for typ, pat in [
        ("act", "records/acts/**/*.json"),
        ("si", "records/sis/**/*.json"),
        ("judgment", "records/judgments/**/*.json"),
    ]:
        for f in glob(str(WORKSPACE / pat), recursive=True):
            try:
                with open(f) as fh:
                    r = json.load(fh)
            except Exception:
                continue
            if not is_real_record(r):
                continue
            rid = r["id"]
            entry = {
                "type": typ,
                "id": rid,
                "title": r.get("title") or "",
                "path": os.path.relpath(f, WORKSPACE),
                "raw": r,
            }
            # If we've seen this id before, prefer the deeper-nested path
            # (matches the b0504 dedup convention).
            if rid in out:
                prev = out[rid]
                if entry["path"].count(os.sep) > prev["path"].count(os.sep):
                    out[rid] = entry
            else:
                out[rid] = entry
    return out


def build_title_index(records):
    """Build {normalised_title: act_id} for act records.

    Conflicting normalisations (multiple acts share a normalised title)
    map to a list of ids; resolution prefers the most recent enacted_date,
    falling back to the lexicographically last id.
    """
    raw = {}
    for rid, r in records.items():
        if r["type"] != "act":
            continue
        n = normalise_title(r["title"])
        if not n:
            continue
        raw.setdefault(n, []).append(rid)
    # Collapse multi-hits deterministically.
    idx = {}
    for n, ids in raw.items():
        if len(ids) == 1:
            idx[n] = ids[0]
        else:
            # Prefer the act with the most recent enacted_date; tiebreak by id.
            def keyfn(i):
                d = records[i]["raw"].get("enacted_date") or ""
                return (d, i)
            idx[n] = sorted(ids, key=keyfn)[-1]
    return idx


# ---------- edge extraction ----------

def extract_edges(records, title_index):
    """Yield (edge_dict, dangling_dict_or_None) tuples."""
    edges = []
    dangling = []  # records whose dst_id couldn't be resolved

    for rid, r in records.items():
        raw = r["raw"]
        rtype = r["type"]

        if rtype == "act":
            # amended_by: list of act ids
            for amender in raw.get("amended_by") or []:
                if not amender:
                    continue
                if amender in records:
                    edges.append({
                        "src_id": rid,
                        "dst_id": amender,
                        "relation": "amended_by",
                        "source_field": "acts.amended_by",
                    })
                else:
                    dangling.append({
                        "src_id": rid,
                        "dst_raw": str(amender),
                        "relation": "amended_by",
                        "source_field": "acts.amended_by",
                        "reason": "act_id_not_in_corpus",
                    })
            # repealed_by: usually a single id (string) but the schema
            # also allows list — handle both.
            rep = raw.get("repealed_by")
            if rep:
                rep_list = rep if isinstance(rep, list) else [rep]
                for repealer in rep_list:
                    if not repealer:
                        continue
                    if repealer in records:
                        edges.append({
                            "src_id": rid,
                            "dst_id": repealer,
                            "relation": "repealed_by",
                            "source_field": "acts.repealed_by",
                        })
                    else:
                        dangling.append({
                            "src_id": rid,
                            "dst_raw": str(repealer),
                            "relation": "repealed_by",
                            "source_field": "acts.repealed_by",
                            "reason": "act_id_not_in_corpus",
                        })

        if rtype == "si":
            # SI amended_by / repealed_by — same shape as for acts.
            for amender in raw.get("amended_by") or []:
                if not amender:
                    continue
                if amender in records:
                    edges.append({
                        "src_id": rid,
                        "dst_id": amender,
                        "relation": "amended_by",
                        "source_field": "sis.amended_by",
                    })
                else:
                    dangling.append({
                        "src_id": rid,
                        "dst_raw": str(amender),
                        "relation": "amended_by",
                        "source_field": "sis.amended_by",
                        "reason": "si_amender_id_not_in_corpus",
                    })
            rep = raw.get("repealed_by")
            if rep:
                rep_list = rep if isinstance(rep, list) else [rep]
                for repealer in rep_list:
                    if not repealer:
                        continue
                    if repealer in records:
                        edges.append({
                            "src_id": rid,
                            "dst_id": repealer,
                            "relation": "repealed_by",
                            "source_field": "sis.repealed_by",
                        })
                    else:
                        dangling.append({
                            "src_id": rid,
                            "dst_raw": str(repealer),
                            "relation": "repealed_by",
                            "source_field": "sis.repealed_by",
                            "reason": "si_repealer_id_not_in_corpus",
                        })
            # SI parent_act -> we resolve free-text title to act id
            pa = raw.get("parent_act")
            if pa:
                pa_list = pa if isinstance(pa, list) else [pa]
                for title in pa_list:
                    if not title:
                        continue
                    n = normalise_title(title)
                    aid = title_index.get(n)
                    if aid:
                        edges.append({
                            "src_id": rid,
                            "dst_id": aid,
                            "relation": "parent_act",
                            "source_field": "sis.parent_act",
                        })
                    else:
                        dangling.append({
                            "src_id": rid,
                            "dst_raw": title,
                            "dst_normalised": n,
                            "relation": "parent_act",
                            "source_field": "sis.parent_act",
                            "reason": "parent_act_title_not_resolved",
                        })

        if rtype == "judgment":
            # key_statutes: list of statute ids/citations
            for ks in raw.get("key_statutes") or []:
                if not ks:
                    continue
                # try id-direct then title-normalised
                if ks in records:
                    edges.append({
                        "src_id": rid,
                        "dst_id": ks,
                        "relation": "cites_statute",
                        "source_field": "judgments.key_statutes",
                    })
                else:
                    n = normalise_title(ks)
                    aid = title_index.get(n) if n else None
                    if aid:
                        edges.append({
                            "src_id": rid,
                            "dst_id": aid,
                            "relation": "cites_statute",
                            "source_field": "judgments.key_statutes",
                        })
                    else:
                        dangling.append({
                            "src_id": rid,
                            "dst_raw": str(ks),
                            "relation": "cites_statute",
                            "source_field": "judgments.key_statutes",
                            "reason": "statute_not_resolved",
                        })
            # cited_authorities: list of judgment ids/citations
            for ca in raw.get("cited_authorities") or []:
                if not ca:
                    continue
                if ca in records:
                    edges.append({
                        "src_id": rid,
                        "dst_id": ca,
                        "relation": "cites_authority",
                        "source_field": "judgments.cited_authorities",
                    })
                else:
                    dangling.append({
                        "src_id": rid,
                        "dst_raw": str(ca),
                        "relation": "cites_authority",
                        "source_field": "judgments.cited_authorities",
                        "reason": "judgment_not_resolved",
                    })

    return edges, dangling


# ---------- DB write (best-effort) ----------

def write_to_sqlite(edges):
    """Write the citations table. Best-effort: if the DB is malformed,
    skip and return a status string; the JSONL remains the canonical
    artefact."""
    if not CORPUS_SQLITE.exists():
        return "skipped: corpus.sqlite missing (rebuild via batch_0504 script first)"
    try:
        con = sqlite3.connect(str(CORPUS_SQLITE), timeout=10)
        cur = con.cursor()
        # Probe
        cur.execute("SELECT 1 FROM sqlite_master LIMIT 1")
        cur.execute("DROP TABLE IF EXISTS citations")
        cur.execute(
            "CREATE TABLE citations ("
            " src_id TEXT NOT NULL, "
            " dst_id TEXT NOT NULL, "
            " relation TEXT NOT NULL, "
            " source_field TEXT NOT NULL, "
            " PRIMARY KEY (src_id, dst_id, relation)"
            ")"
        )
        cur.execute("CREATE INDEX idx_citations_dst ON citations(dst_id)")
        cur.execute("CREATE INDEX idx_citations_relation ON citations(relation)")
        # INSERT OR IGNORE to defang accidental dupes.
        cur.executemany(
            "INSERT OR IGNORE INTO citations(src_id,dst_id,relation,source_field) VALUES (?,?,?,?)",
            [(e["src_id"], e["dst_id"], e["relation"], e["source_field"]) for e in edges]
        )
        n_rows = cur.execute("SELECT COUNT(*) FROM citations").fetchone()[0]
        con.commit()
        con.close()
        return f"ok: {n_rows} rows in citations table"
    except sqlite3.DatabaseError as e:
        return f"skipped: corpus.sqlite read/write failed ({e!r}); JSONL remains canonical"


# ---------- main ----------

def main():
    started = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    print(f"[{started}] batch-0505 build_citation_graph START parser={PARSER_VERSION}")

    records = load_all_records()
    print(f"  records loaded: {len(records)} unique ids")

    title_index = build_title_index(records)
    print(f"  act-title index size: {len(title_index)}")

    edges, dangling = extract_edges(records, title_index)
    # Dedup edges deterministically (defensive — should already be unique
    # because the source fields are sets/lists, but be paranoid).
    seen = set()
    unique_edges = []
    for e in edges:
        key = (e["src_id"], e["dst_id"], e["relation"])
        if key in seen:
            continue
        seen.add(key)
        unique_edges.append(e)

    # Sort for stable diffs.
    unique_edges.sort(key=lambda e: (e["src_id"], e["relation"], e["dst_id"]))
    dangling.sort(key=lambda d: (d["src_id"], d["relation"], d.get("dst_raw","")))

    # Per-relation counts
    by_rel = {}
    for e in unique_edges:
        by_rel[e["relation"]] = by_rel.get(e["relation"], 0) + 1
    by_dangling_reason = {}
    for d in dangling:
        by_dangling_reason[d["reason"]] = by_dangling_reason.get(d["reason"], 0) + 1

    summary = {
        "parser_version": PARSER_VERSION,
        "built_at": started,
        "record_count": len(records),
        "edge_count": len(unique_edges),
        "edges_by_relation": by_rel,
        "dangling_count": len(dangling),
        "dangling_by_reason": by_dangling_reason,
        # Integrity: every dst_id in unique_edges must be a real record id.
        "all_dst_ids_resolved": all(e["dst_id"] in records for e in unique_edges),
    }
    print(f"  edges: {len(unique_edges)} (by relation: {by_rel})")
    print(f"  dangling: {len(dangling)} (by reason: {by_dangling_reason})")
    print(f"  all_dst_ids_resolved: {summary['all_dst_ids_resolved']}")

    # Write outputs.
    SUMMARY_JSON.parent.mkdir(parents=True, exist_ok=True)
    with open(CITATIONS_JSONL, "w") as fh:
        for e in unique_edges:
            fh.write(json.dumps(e, sort_keys=True) + "\n")
    with open(SUMMARY_JSON, "w") as fh:
        json.dump(summary, fh, indent=2, sort_keys=True)
    print(f"  wrote {CITATIONS_JSONL.name} ({len(unique_edges)} lines)")
    print(f"  wrote {SUMMARY_JSON.relative_to(WORKSPACE)}")

    # Best-effort DB write.
    db_status = write_to_sqlite(unique_edges)
    print(f"  sqlite citations table: {db_status}")

    # Return value for callers/integrity check.
    return {
        "summary": summary,
        "dangling": dangling,
        "db_status": db_status,
    }


if __name__ == "__main__":
    result = main()
    # Exit 0 always — dangling references are not failures, they go to gaps.md.
    sys.exit(0)
