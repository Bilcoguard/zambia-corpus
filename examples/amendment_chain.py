#!/usr/bin/env python3
"""examples/amendment_chain.py — Phase 7 deliverable #2 example #3.

Trace the amendment / repeal chain for a specific Act. Wraps
:func:`query_corpus.cited_by` and :func:`query_corpus.citations_of` plus a
direct ``acts_meta.amended_by`` lookup so a specialist can answer
"what supersedes / was superseded by this Act?" without writing Python.

Read-only — uses the same ``mode=ro&immutable=1`` access pattern as the
underlying query API. Never writes to ``corpus.sqlite``.

Usage:
    python examples/amendment_chain.py act-zm-1994-026-companies-act-1994
    python examples/amendment_chain.py act-zm-2017-010-companies --json

Defaults to the 1994 Companies Act when no id is supplied — that record is
the canonical worked example because it carries a ``repealed_by`` edge to
the 2017 Companies Act AND is the parent of three pre-2018 SIs that are
still on the books.

Output groups:
  * ``repealed_by``    — Acts that repealed THIS Act (forward chain).
  * ``repeals``        — Acts that THIS Act repealed (backward chain).
  * ``amended_by``     — raw value of ``acts_meta.amended_by``
                         (Phase 2/4 parsers leave this JSON-encoded
                         empty list `[]` for the bulk of the corpus —
                         flagged where present).
  * ``has_subsidiary`` — SIs that name this Act as their parent.
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

DEFAULT_ACT_ID = "act-zm-1994-026-companies-act-1994"


def amendment_chain(act_id: str) -> dict:
    """Build the amendment / repeal / parent-of chain dict for an Act.

    Pure data — no I/O beyond query_corpus's read-only DB connection.
    """
    rec = q.get_by_id(act_id) or {}
    if not rec:
        return {
            "id": act_id,
            "found": False,
            "title": None,
            "repealed_by": [],
            "repeals": [],
            "amended_by_raw": None,
            "has_subsidiary": [],
        }

    # repealed_by: outbound edges with relation='repealed_by'
    outbound = q.cited_by(act_id)
    repealed_by = [
        {"id": r["id"], "title": r.get("title"), "citation": r.get("citation")}
        for r in outbound
        if r.get("relation") == "repealed_by"
    ]

    # repeals: inbound edges with relation='repealed_by'
    inbound = q.citations_of(act_id)
    repeals = [
        {"id": r["id"], "title": r.get("title"), "citation": r.get("citation")}
        for r in inbound
        if r.get("relation") == "repealed_by"
    ]

    # has_subsidiary: inbound parent_act edges (SIs naming this Act)
    has_subsidiary = [
        {
            "id": r["id"],
            "title": r.get("title"),
            "citation": r.get("citation"),
            "si_year": r.get("si_year"),
        }
        for r in inbound
        if r.get("relation") == "parent_act"
    ]

    return {
        "id": rec.get("id", act_id),
        "found": True,
        "title": rec.get("title"),
        "citation": rec.get("citation"),
        "enacted_date": rec.get("enacted_date"),
        "repealed_by": repealed_by,
        "repeals": repeals,
        # acts_meta.amended_by is a JSON-encoded string in the schema; expose
        # the raw value here, the consumer should treat None as "unknown".
        "amended_by_raw": rec.get("amended_by"),
        "has_subsidiary": has_subsidiary,
    }


def _format(chain: dict) -> str:
    lines: list[str] = []
    lines.append(f"# Act: {chain.get('id')}")
    if not chain.get("found"):
        lines.append("# (not found in corpus)")
        return "\n".join(lines)
    lines.append(f"# Title:    {chain.get('title') or '(none)'}")
    lines.append(f"# Citation: {chain.get('citation') or '(none)'}")
    lines.append(f"# Enacted:  {chain.get('enacted_date') or '(none)'}")
    lines.append("")
    lines.append(f"## Repealed by ({len(chain['repealed_by'])})")
    for r in chain["repealed_by"]:
        lines.append(f"  -> {r['id']:<60} {r.get('title') or ''}")
    lines.append("")
    lines.append(f"## Repeals ({len(chain['repeals'])})")
    for r in chain["repeals"]:
        lines.append(f"  <- {r['id']:<60} {r.get('title') or ''}")
    lines.append("")
    lines.append(f"## amended_by raw value (acts_meta.amended_by)")
    lines.append(f"  {chain.get('amended_by_raw')!r}")
    lines.append(
        "  (Phase 2/4 parsers leave this empty for most acts; treat None or "
        "'[]' as 'unknown', not 'never amended'.)"
    )
    lines.append("")
    lines.append(f"## Subsidiary SIs (parent_act inbound edges) "
                 f"({len(chain['has_subsidiary'])})")
    for r in chain["has_subsidiary"]:
        lines.append(f"  +  {r['id']:<60} {r.get('title') or ''}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        description=(
            "Trace the amendment / repeal / subsidiary chain for one Act."
        )
    )
    p.add_argument(
        "act_id",
        nargs="?",
        default=DEFAULT_ACT_ID,
        help=(
            "Record id of the Act (default: 1994 Companies Act, the "
            "canonical worked example with non-empty chain)."
        ),
    )
    p.add_argument(
        "--json",
        action="store_true",
        dest="as_json",
        help="Emit the raw chain dict as JSON instead of a human table",
    )
    args = p.parse_args(argv)

    chain = amendment_chain(args.act_id)
    if args.as_json:
        json.dump(chain, sys.stdout, ensure_ascii=False, indent=2, sort_keys=True)
        sys.stdout.write("\n")
        return 0
    print(_format(chain))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
