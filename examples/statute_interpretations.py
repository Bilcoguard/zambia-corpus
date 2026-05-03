#!/usr/bin/env python3
"""examples/statute_interpretations.py — Phase 7 deliverable #2 example #4.

For a given Act id, list every judgment that interprets that statute.

Wraps :func:`query_corpus.statute_interpretation` and adds a graceful
fallback when the parser hasn't yet populated ``key_statutes_json`` for a
given record (which is currently the case across the entire corpus —
see INTEGRATION.md "Limitations").

The fallback path performs a free-text FTS5 search over judgments using
the act's title and citation as the query, so a specialist still gets a
reasonable answer until the parser is upgraded to populate the structured
field. Records that surface only via the fallback are clearly marked.

Read-only — uses the same access pattern as ``query_corpus``.

Usage:
    python examples/statute_interpretations.py act-zm-2017-010-companies
    python examples/statute_interpretations.py act-zm-2016-035-the-electoral-process --json

Exit code is 0 on success (including when no judgments are found — that
is a legitimate "we know of none" answer).
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
WORKSPACE = HERE.parent
sys.path.insert(0, str(WORKSPACE / "scripts"))
import query_corpus as q  # noqa: E402


def _free_text_fallback(act: dict, limit: int) -> list[dict]:
    """Run an FTS5 fallback search over judgments using the act's title.

    This is *not* the same as :func:`query_corpus.statute_interpretation`
    (which only inspects structured fields). It supplements that path
    while ``key_statutes_json`` is uniformly empty in the corpus.
    """
    title = (act.get("title") or "").strip()
    if not title:
        return []
    # FTS5 phrase quote the title to keep multi-word matches together.
    fts_query = f'"{title}"'
    try:
        return q.search(fts_query, type="judgment", limit=limit)
    except Exception:
        return []


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        description=(
            "List every judgment that interprets a given Act. "
            "Falls back to a free-text title search when the structured "
            "key_statutes field is unpopulated."
        )
    )
    p.add_argument("act_id", help="Corpus id of the Act, e.g. act-zm-2017-010-companies")
    p.add_argument("--limit", type=int, default=20)
    p.add_argument(
        "--no-fallback",
        action="store_true",
        help="Skip the FTS5 free-text fallback (structured-only)",
    )
    p.add_argument(
        "--json",
        action="store_true",
        dest="as_json",
        help="Emit JSON instead of the human-readable table",
    )
    args = p.parse_args(argv)

    act = q.get_by_id(args.act_id)
    if act is None:
        print(
            f"ERROR: act_id {args.act_id!r} not found in corpus.sqlite",
            file=sys.stderr,
        )
        return 2
    if act.get("type") != "act":
        print(
            f"ERROR: id {args.act_id!r} is type={act.get('type')!r}, expected 'act'",
            file=sys.stderr,
        )
        return 2

    structured = q.statute_interpretation(args.act_id, db_path=None)
    structured_ids = {r["id"] for r in structured}

    fallback: list[dict] = []
    if not args.no_fallback:
        fallback = [
            r for r in _free_text_fallback(act, args.limit)
            if r["id"] not in structured_ids
        ]

    if args.as_json:
        out = {
            "act_id": args.act_id,
            "act_title": act.get("title"),
            "act_citation": act.get("citation"),
            "structured_matches": structured,
            "fallback_matches": fallback,
        }
        json.dump(out, sys.stdout, ensure_ascii=False, indent=2, sort_keys=True)
        sys.stdout.write("\n")
        return 0

    print(f"# act: {act.get('title')!r}  ({act.get('citation')})")
    print(f"# id : {args.act_id}")
    print()
    print(f"## Structured (key_statutes_json) — {len(structured)} hit(s)")
    if not structured:
        print("  (none — key_statutes_json is uniformly empty across the corpus;")
        print("   see INTEGRATION.md Limitations.)")
    for r in structured:
        cn = r.get("case_name") or r.get("title") or ""
        print(f"  {r['id']:<70} | {r.get('outcome') or '(unspecified)':<13} | {cn[:60]}")

    if not args.no_fallback:
        print()
        print(f"## Free-text title fallback — {len(fallback)} additional hit(s)")
        for r in fallback:
            cn = r.get("case_name") or r.get("title") or ""
            print(f"  {r['id']:<70} | {r.get('outcome') or '(unspecified)':<13} | {cn[:60]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
