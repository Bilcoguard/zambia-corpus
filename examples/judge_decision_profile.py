#!/usr/bin/env python3
"""examples/judge_decision_profile.py — Phase 7 deliverable #2 example #4.

Pull a judge's full decision history with an outcome and court breakdown.
Wraps :func:`query_corpus.judge_profile` with a thin CLI that's optimised
for trial-prep / panel-prediction work (Mike & Andrew specialists in the
Kate Weston Legal plugin).

Read-only — uses the same ``mode=ro&immutable=1`` access pattern as the
underlying query API. Never writes to ``corpus.sqlite``.

Usage:
    python examples/judge_decision_profile.py Sitali
    python examples/judge_decision_profile.py "Mulonga"  --json
    python examples/judge_decision_profile.py Munalula --limit 25

Default search is "Mulongoti" — the judge with the highest judgment
count in the current corpus (33 judgments under parser_v0.3.2 across
ZMSC and ZMCC). Pass any surname (or canonical 'Surname Title' form)
as a CLI arg to switch.

The judge name match is a case-insensitive substring against the
canonical ``name`` field in each ``judges_meta.judges_json`` entry, so
both ``"Sitali"`` and ``"Sitali J"`` work.
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

DEFAULT_JUDGE = "Mulongoti"


def _format_summary(profile: dict, limit: int) -> str:
    """Multi-line human summary of a judge_profile() result."""
    lines: list[str] = []
    judge = profile.get("judge_name", "(unknown)")
    total = profile.get("total", 0)
    lines.append(f"# Judge: {judge}")
    lines.append(f"# Total judgments: {total}")

    courts = profile.get("courts", {}) or {}
    if courts:
        lines.append("# By court:")
        for c, n in sorted(courts.items(), key=lambda kv: (-kv[1], kv[0])):
            lines.append(f"    {n:>4}  {c}")

    outcomes = profile.get("outcome_counts", {}) or {}
    if outcomes:
        lines.append("# By outcome:")
        for o, n in sorted(outcomes.items(), key=lambda kv: (-kv[1], kv[0])):
            lines.append(f"    {n:>4}  {o}")

    judgments = profile.get("judgments", []) or []
    if judgments:
        lines.append("")
        lines.append(f"## Judgments (first {min(limit, len(judgments))} of {len(judgments)}, "
                     f"chronological by date_decided)")
        for j in judgments[:limit]:
            jid = j.get("id", "?")
            court = j.get("court") or ""
            date = j.get("date_decided") or ""
            outcome = j.get("outcome") or "(unspecified)"
            case_name = j.get("case_name") or j.get("title") or ""
            lines.append(f"  {date:<10} | {court:<35} | {outcome:<14} | "
                         f"{jid:<55} | {case_name[:60]}")

    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        description=(
            "Show a judge's full decision history with outcome and court "
            "breakdown (query_corpus.judge_profile wrapper)."
        )
    )
    p.add_argument(
        "judge",
        nargs="?",
        default=DEFAULT_JUDGE,
        help=(
            "Surname or canonical 'Surname Title' form; case-insensitive "
            "substring match (default: Mulongoti, the highest-volume "
            "judge in the current corpus)."
        ),
    )
    p.add_argument(
        "--limit",
        type=int,
        default=15,
        help="Cap the number of judgments listed (default: 15).",
    )
    p.add_argument(
        "--json",
        action="store_true",
        dest="as_json",
        help="Emit the raw API output as JSON instead of a human summary.",
    )
    args = p.parse_args(argv)

    profile = q.judge_profile(args.judge)

    if args.as_json:
        # Trim long judgments lists for the JSON view too — caller can
        # re-run query_corpus directly for the full record set.
        out = dict(profile)
        out["judgments"] = (out.get("judgments") or [])[: args.limit]
        json.dump(out, sys.stdout, ensure_ascii=False, indent=2, sort_keys=True, default=str)
        sys.stdout.write("\n")
        return 0

    print(_format_summary(profile, args.limit))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
