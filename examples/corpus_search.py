#!/usr/bin/env python3
"""examples/corpus_search.py — Phase 7 deliverable #2 example #1.

Full-text search over the Zambian Authorities Corpus with type / court /
year filters. Wraps :func:`query_corpus.search` with a thin CLI so a
specialist can do quick case-law lookups without writing Python.

Read-only — uses the same ``mode=ro&immutable=1`` access pattern as the
underlying query API. Never writes to ``corpus.sqlite``.

Usage:
    python examples/corpus_search.py "shareholder" --type judgment --limit 5
    python examples/corpus_search.py "electoral" --type si --year-from 2020
    python examples/corpus_search.py "companies act"

Output is a compact one-line-per-hit table by default; pass --json for the
raw API output (suitable for piping to ``jq``).
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys

# Make the corpus query API importable regardless of where this script is run
# from. ``query_corpus.py`` lives in ``scripts/`` next to this folder.
HERE = pathlib.Path(__file__).resolve().parent
WORKSPACE = HERE.parent
sys.path.insert(0, str(WORKSPACE / "scripts"))
import query_corpus as q  # noqa: E402


def _format_row(rec: dict) -> str:
    """One-line summary of a record for the table view."""
    rid = rec.get("id", "?")
    rtype = rec.get("type", "?")
    title = rec.get("case_name") or rec.get("title") or ""
    extra = ""
    if rtype == "judgment":
        court = rec.get("court") or ""
        outcome = rec.get("outcome") or "(unspecified)"
        date = rec.get("date_decided") or ""
        extra = f" [{court} | {outcome} | {date}]"
    elif rtype == "act":
        cite = rec.get("citation") or ""
        extra = f" [{cite}]"
    elif rtype == "si":
        cite = rec.get("citation") or ""
        extra = f" [{cite}]"
    return f"  {rid:<70} | {rtype:<8} | {title[:80]}{extra}"


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        description=(
            "Full-text search over the Zambian Authorities Corpus "
            "(query_corpus.search wrapper)."
        )
    )
    p.add_argument("query", help="FTS5 query string")
    p.add_argument(
        "--type",
        choices=["act", "si", "judgment"],
        default=None,
        help="Restrict to one record type",
    )
    p.add_argument(
        "--court",
        default=None,
        help="Case-insensitive substring filter (judgments only)",
    )
    p.add_argument("--year-from", dest="year_from", type=int, default=None)
    p.add_argument("--year-to", dest="year_to", type=int, default=None)
    p.add_argument("--limit", type=int, default=10)
    p.add_argument(
        "--json",
        action="store_true",
        dest="as_json",
        help="Emit the raw API output as JSON instead of a table",
    )
    args = p.parse_args(argv)

    results = q.search(
        args.query,
        type=args.type,
        court=args.court,
        year_from=args.year_from,
        year_to=args.year_to,
        limit=args.limit,
    )

    if args.as_json:
        json.dump(results, sys.stdout, ensure_ascii=False, indent=2, sort_keys=True)
        sys.stdout.write("\n")
        return 0

    print(f"# query: {args.query!r}")
    print(f"# filters: type={args.type} court={args.court} "
          f"year_from={args.year_from} year_to={args.year_to} limit={args.limit}")
    print(f"# {len(results)} result(s)")
    if not results:
        return 0
    for rec in results:
        print(_format_row(rec))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
