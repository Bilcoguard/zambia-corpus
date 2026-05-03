#!/usr/bin/env python3
"""examples/citation_chain.py — Phase 7 deliverable #2 example #5.

Trace the citation network from a single record both forward (records the
input record cites — outbound, via :func:`query_corpus.cited_by`) and
backward (records that cite the input record — inbound, via
:func:`query_corpus.citations_of`). Optionally walks a second hop on
either side.

Read-only — uses the same ``mode=ro&immutable=1`` access pattern as the
underlying query API. Never writes to ``corpus.sqlite``.

Usage:
    python examples/citation_chain.py act-zm-1994-026-companies-act-1994
    python examples/citation_chain.py act-zm-2017-010-companies --depth 2
    python examples/citation_chain.py jud-zmsc-2025-005 --json

Default record id is the 1994 Companies Act, which produces a non-empty
chain on the current corpus (3 SI children naming it as parent + 1 Act
repealing it). Phase 7 BRIEF.md asks for a *judgment*-rooted example;
the current Phase 5 parser does not populate ``key_statutes`` or
``cited_authorities`` for any judgment, so judgment-rooted chains are
*expected to be empty under parser_v0.3.2* — see the [Limitations]
section of INTEGRATION.md and the 2026-05-03 entries in gaps.md. The
script handles that case explicitly (it prints a "(empty under current
parser coverage)" stub instead of a row table).
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

DEFAULT_RECORD_ID = "act-zm-1994-026-companies-act-1994"


def _row(rec: dict) -> dict:
    """Compact dict for one node on a chain."""
    return {
        "id": rec.get("id"),
        "type": rec.get("type"),
        "title": rec.get("case_name") or rec.get("title"),
        "citation": rec.get("citation"),
        "relation": rec.get("relation"),
        "source_field": rec.get("source_field"),
    }


def trace_chain(record_id: str, depth: int = 1) -> dict:
    """Build a forward + backward citation chain rooted at ``record_id``.

    Args:
        record_id: Any record id (act/si/judgment).
        depth: 1 for direct neighbours only; 2 walks one extra hop in
            both directions (de-duped against already-visited ids).

    Returns:
        ``{"root": ..., "outbound": [...], "inbound": [...],
           "outbound_hop2": [...], "inbound_hop2": [...]}``.
        Hop-2 lists are empty when ``depth < 2``.
    """
    depth = max(1, int(depth))
    root_rec = q.get_by_id(record_id) or {}
    outbound = [_row(r) for r in q.cited_by(record_id)]
    inbound = [_row(r) for r in q.citations_of(record_id)]

    visited = {record_id}
    visited.update(r["id"] for r in outbound if r.get("id"))
    visited.update(r["id"] for r in inbound if r.get("id"))

    outbound_hop2: list[dict] = []
    inbound_hop2: list[dict] = []
    if depth >= 2:
        for r in outbound:
            rid = r.get("id")
            if not rid:
                continue
            for r2 in q.cited_by(rid):
                if r2.get("id") in visited:
                    continue
                visited.add(r2.get("id"))
                row = _row(r2)
                row["via"] = rid
                outbound_hop2.append(row)
        for r in inbound:
            rid = r.get("id")
            if not rid:
                continue
            for r2 in q.citations_of(rid):
                if r2.get("id") in visited:
                    continue
                visited.add(r2.get("id"))
                row = _row(r2)
                row["via"] = rid
                inbound_hop2.append(row)

    return {
        "root": {
            "id": record_id,
            "found": bool(root_rec),
            "type": root_rec.get("type"),
            "title": root_rec.get("case_name") or root_rec.get("title"),
            "citation": root_rec.get("citation"),
        },
        "depth": depth,
        "outbound": outbound,
        "inbound": inbound,
        "outbound_hop2": outbound_hop2,
        "inbound_hop2": inbound_hop2,
    }


def _format_section(label: str, rows: list[dict]) -> list[str]:
    out: list[str] = []
    out.append(f"## {label} ({len(rows)})")
    if not rows:
        out.append("  (empty under current parser coverage — see "
                   "INTEGRATION.md Limitations)")
        return out
    for r in rows:
        rel = r.get("relation") or ""
        title = r.get("title") or ""
        via = f"  via={r.get('via')}" if r.get("via") else ""
        out.append(f"  {r.get('id'):<60} | {rel:<14} | {title[:70]}{via}")
    return out


def _format(chain: dict) -> str:
    root = chain["root"]
    lines: list[str] = []
    lines.append(f"# Root: {root.get('id')}")
    if not root.get("found"):
        lines.append("# (root not found in corpus)")
    else:
        lines.append(f"# Type:    {root.get('type')}")
        lines.append(f"# Title:   {root.get('title') or '(none)'}")
        lines.append(f"# Citation:{root.get('citation') or '(none)'}")
    lines.append(f"# Depth:   {chain.get('depth')}")
    lines.append("")
    lines.extend(_format_section("Outbound (records cited by root)", chain["outbound"]))
    lines.append("")
    lines.extend(_format_section("Inbound (records that cite root)", chain["inbound"]))
    if chain.get("outbound_hop2") or chain.get("inbound_hop2"):
        lines.append("")
        lines.extend(_format_section(
            "Outbound hop-2", chain.get("outbound_hop2", []),
        ))
        lines.append("")
        lines.extend(_format_section(
            "Inbound hop-2", chain.get("inbound_hop2", []),
        ))
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        description=(
            "Trace the citation network from a single record (forward + "
            "backward; optional 2-hop walk)."
        )
    )
    p.add_argument(
        "record_id",
        nargs="?",
        default=DEFAULT_RECORD_ID,
        help=(
            "Any record id (act/si/judgment). Default: "
            "act-zm-1994-026-companies-act-1994 (non-empty under current "
            "corpus coverage)."
        ),
    )
    p.add_argument(
        "--depth",
        type=int,
        default=1,
        help="1 = direct neighbours only (default); 2 = walk one extra hop.",
    )
    p.add_argument(
        "--json",
        action="store_true",
        dest="as_json",
        help="Emit the raw chain dict as JSON instead of the human view.",
    )
    args = p.parse_args(argv)

    chain = trace_chain(args.record_id, depth=args.depth)
    if args.as_json:
        json.dump(chain, sys.stdout, ensure_ascii=False, indent=2, sort_keys=True)
        sys.stdout.write("\n")
        return 0
    print(_format(chain))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
