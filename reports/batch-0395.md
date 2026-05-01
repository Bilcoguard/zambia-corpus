# Batch 0395 — Phase 5 audit-only (20th consecutive substantive idle tick)

- **Timestamp (UTC):** 2026-05-01T08:03Z
- **Phase:** phase_5_judgments (approved+incomplete)
- **Yield:** 0 records written / 0 deferred
- **Fetches this tick:** 0
- **Cumulative today:** 0 / 2000 fetches
- **Wall-clock:** under 5 minutes (well under 20-min budget)

## Tick summary

Pre-flight cleanup ran clean (`find .git -name "*.lock" / -name
"*.lock.bak" -delete` — no in-`.git` matches; pre-existing
`_stale_locks_b03**_*.lock.bak` quarantine residue at the repo root
persists harmlessly — see Housekeeping below). `git pull --ff-only`
reports "Already up to date" with the carry-forward
`.git/objects/maintenance.lock` "Operation not permitted" warning that
has been benign across the full b0375 → b0394 idle stretch.

`approvals.yaml` is unchanged since 2026-04-30T15:36:40Z (commit
`b24a938` — "Lock in parser_v0.3.1 + reparse-first policy across
BRIEF.md and approvals.yaml") — ~16h 26m at tick start (per
`git log -1 --format %cI -- approvals.yaml`). `phase_5_judgments`
remains `approved: true / complete: false`. The three Peter-only
unblocks (parser_v0.3.2 vocabulary widening, OCR pipeline for scanned
PDFs, ZMSC fresh-DESC sweep into 2024/2023) are all still pending.

## Reparse-first inventory (BRIEF.md Phase 5 policy: reparse before fetch)

| Court | Raw HTML | Raw PDF | Records on disk | Missing |
|-------|---------:|--------:|----------------:|--------:|
| ZMCC  | 142 | 141 | 53 | **89** |
| ZMSC  |  25 |  24 | 24 |   0 (1 HTML stem outside the canonical pattern; non-blocking) |
| SCZ   |   — |   — |  1 |   —   |
| **Total** | | | **78** | **89** |

**Verdict:** v0.3.1 reparse inventory remains **FULLY EXHAUSTED**.
Every one of the 89 ZMCC raw-but-no-record candidates carries a
deferral reason that v0.3.1 cannot address without one of the three
Peter-only unblocks. Inventory identical to b0378 → b0394 (17
consecutive ticks of unchanged inventory).

## gaps.md cross-check (line-frequency, grep -c)

Reason-code frequencies — identical to b0386 → b0394:

- 114 lines `html_no_summary_pdf_no_match`
- 14 lines `parser_v0.3.1_judges_no_comma_unhandled`
- 10 lines `pdf_extraction_empty_likely_scanned`
- 2 lines `multi_judge_separate_opinions_no_clear_majority_disposition`
- 49 lines `outcome_not_inferable_under_tightened_policy` (legacy
  v0.3.0 generic, retained historical — banned for new deferrals)

`gaps.md` mtime 2026-04-30T21:39:41Z (commit `61d666e`) — unchanged
since b0379.

## Fresh DESC sweep deferral (carried from b0376–b0394)

Two non-overlapping reasons preserve current deferral:

1. **ZMCC backlog dominated by parser-vocabulary limitations.**
   ~85% of the existing 89-record ZMCC backlog is gated on
   `html_no_summary_pdf_no_match` — a parser-vocabulary limit that a
   fresh DESC sweep would only reproduce while consuming finite fetch
   budget that parser_v0.3.2 can use far more efficiently in a single
   re-parse pass.
2. **ZMSC schema-mixing hazard.** The 24 existing ZMSC records use
   parser_v0.5.0 schema; a v0.3.1 sweep would mix two schemas in the
   same court directory. Integrity checks in the current codebase do
   not detect schema-mixing — silent drift would be possible. Needs
   explicit Peter approval before any v0.3.1 ZMSC sweep proceeds.

## Escalation (20th consecutive substantive idle tick)

Three non-overlapping unblocks remain on Peter's plate, ranked by
expected yield:

1. **parser_v0.3.2 vocabulary widening** — highest yield against the
   existing ZMCC backlog (~70 / 89 deferred candidates would clear).
   Subject to Peter approval per BRIEF.md non-negotiable on parser
   changes.
2. **OCR pipeline** for the 4 scanned-PDF candidates
   (`zmcc/2021/{14,15}`, `zmcc/2022/16`, `zmcc/2025/19`). Subject to
   Peter approval (new dependency surface).
3. **ZMSC fresh DESC sweep** into 2024/2023 — schema-mixing hazard;
   needs explicit approval.

Recommended ordering: (1) → (2) → (3).

The 20-tick threshold (≈10 wall-clock hours of idle ticks at the
30-minute cadence) crystallises the prior recommendation: any one of
the three unblocks would convert the next tick from audit-only to
substantive yield.

## Integrity check

Trivial PASS — no records written or deleted; schema/registry/hash/
cited_authorities clauses not exercised. Spot-check on the last 3
ZMCC + last 3 ZMSC record JSONs confirms required provenance fields
(`source_url`, `source_hash`, `fetched_at`, `parser_version`) all
present and JSON parses clean. ZMCC samples report parser_version
0.2.0; ZMSC samples report parser_version 0.5.0 — confirming the
schema-mixing hazard called out above.

## Housekeeping (carry-forward from b0391–b0394)

The `_stale_locks_b03**_*.lock.bak` quarantine residue at the repo
root continues to grow (~30+ files visible). Harmless to git
operations and worker logic; suggested host-side single-line cleanup
at a convenient maintenance window:

```
rm -f ~/KateWestonCorpus/corpus/_stale_locks_*
```

Worker has not attempted in-sandbox cleanup because every prior
`unlink` attempt hits "Operation not permitted" (same condition
driving the `mv`-based lock workaround during commits).

## Phase 5 completion criterion

The "appears complete, awaiting human confirmation" criterion fired
in batch-0379 and has been re-affirmed every substantive tick since.
The worker does not flip the `complete: false` flag — that is a Peter
action per BRIEF.md.

## B2 sync / SQLite ingestion

- **B2 sync:** deferred to host (rclone not in sandbox).
- **SQLite ingestion:** deferred to host (corpus.sqlite FTS5
  malformed-disk-image carry-forward; canonical source remains
  `records/*.json`).
