# Batch 0377 — Phase 5 reparse-first INVENTORY AUDIT (no parser write)

**Date:** 2026-04-30T22:35:00Z
**Phase:** phase_5_judgments (approved: true, complete: false)
**Parser:** parser_v0.3.1 (frozen baseline `scripts/batch_0360_parse.py`)
**Mode:** AUDIT — re-confirms b0375/b0376 finding; no fresh fetches; no parse output commit
**Slice attempted:** none (audit only)

## Result: NO COMMIT OF PARSE OUTPUT — v0.3.1-addressable reparse inventory remains exhausted

This tick re-verified the b0375/b0376 finding. `approvals.yaml` is unchanged since
2026-04-30 03:23Z (parser_v0.3.2 / OCR approvals not yet landed). No new raw bytes
have been written to `raw/zambialii/judgments/` since b0376; the 89-candidate
ZMCC backlog is identical to b0376's snapshot.

### Inventory snapshot (2026-04-30T22:35Z)

| Court | Years on disk | Raw HTML+PDF pairs | Records written | Missing (raw, no record) |
|-------|---------------|--------------------|-----------------|--------------------------|
| ZMCC  | 2021–2026     | 142                | 53              | 89                       |
| ZMSC  | 2025–2026     | 24                 | 24              | 0                        |
| **Total** | —          | **166**            | **77**          | **89**                   |

(One additional record at the records-tree root —
`judgment-zm-2026-scz-09-konkola-v-ag.json` — brings on-disk total to 78. Phase 5
progress: **78 / 100–160**, unchanged from b0376.)

#### ZMCC missing-by-year (court+year+number keying)

- 2021: 5 — {12, 14, 15, 18, 21}
- 2022: 29 — {1–11, 13–18, 20–25, 27, 30–34}
- 2023: 17 — {3–6, 8, 12, 14, 16–21, 23, 25–27}
- 2024: 15 — {2, 4–8, 10, 13, 15, 17, 20, 22, 23, 25, 27}
- 2025: 22 — {2, 5–12, 14–19, 21, 22, 24, 25, 28, 32, 33}
- 2026: 1 — {1}

### All 89 missing candidates are already deferred in `gaps.md`

Programmatic cross-check this tick (court+year+number key match against any of:
`zmcc/{year}/{n}`, `[{year}] ZMCC {n}`, `judgment-zm-{year}-zmcc-{n}-`) ⇒
**89 / 89 missing candidates appear in `gaps.md`** under at least one v0.3.1
specific reason code. None are unaddressed. Result identical to b0376 audit.

### Why a v0.3.1 reparse this tick would (still) be wasted work

- All four v0.3.1 specific reason codes (`html_no_summary_pdf_no_match`,
  `parser_v0.3.1_judges_no_comma_unhandled`, `pdf_extraction_empty_likely_scanned`,
  `multi_judge_separate_opinions_no_clear_majority_disposition`) are by definition
  not addressable by parser_v0.3.1 itself.
- The legacy 49 `outcome_not_inferable_under_tightened_policy` entries all have
  documented v0.3.1 follow-ups recorded in later `gaps.md` sections.
- ZMSC has zero raw-on-disk no-record candidates; nothing to re-parse there.

### Why NOT a fresh DESC sweep this tick

`approvals.yaml` `reparse_first` flag is satisfied (no v0.3.1-addressable
inventory remaining), so a fresh DESC sweep into ZMSC pre-2025 (or ZMCC 2020 and
earlier) is technically permitted. b0376 explicitly considered and recommended
against this on the grounds that ~85% of the existing ZMCC backlog defers as
`html_no_summary_pdf_no_match` — a parser-vocabulary limitation that a fresh
sweep into older judgments would simply reproduce, while consuming fetch budget
that parser_v0.3.2 will be far more efficient with once approved.

This tick continues that recommendation. **Cost of waiting:** none — fresh fetch
budget rolls over daily, and the missing 89 + any future fresh-sweep candidates
will all be amenable to a single high-yield reparse pass once parser_v0.3.2
ships. **Cost of acting:** likely 6–7/8 candidates deferring under the same
parser-vocabulary blocker, plus eight rows of avoidable `gaps.md` churn.

## Action taken this tick

- Cleared stale `.git/*.lock` and `.git/*.lock.bak` files (per task step 1).
- `git pull --ff-only` ⇒ Already up to date.
- Read `approvals.yaml`. Phase 5 is approved+incomplete; reparse_first: true;
  parser_v0.3.2 / OCR not yet approved.
- Verified `costs.log` shows 0 events for 2026-05-01 (date boundary). No budget
  consumed today.
- Re-ran the b0376 court+year+number audit script: ZMCC raw 142 / records 53 /
  missing 89; ZMSC raw 24 / records 24 / missing 0; +1 root record.
- Cross-checked all 89 missing candidates against `gaps.md` with three needle
  shapes per candidate. **89 / 89 found** — zero uncatalogued candidates.
- No parse run executed (would have produced 0 / 0 / 0).
- No new fetch issued (0 bytes).
- No `gaps.md`, `provenance.log`, `corpus.sqlite`, `judges_registry.yaml`, or
  `records/*.json` writes.

## Recommendation (unchanged from b0375/b0376)

**parser_v0.3.2 vocabulary widening** + **OCR pipeline** remain the dominant
unblocks. Both are subject to Peter's approval per BRIEF.md non-negotiable on
parser changes.

Until either approval lands in `approvals.yaml`, the worker will continue
producing audit-only ticks. Each audit-only tick costs ~0 budget and simply
re-confirms the b0376 / b0377 inventory state.

**Suggested next-tick action:** continue the audit-only pattern unless
`approvals.yaml` shows a new approval; if no change after, say, three more
ticks, consider escalating an explicit notification to Peter via `worker.log`
so he is aware the worker is in a sustained idle-by-design state.

## Logs

- `worker.log` updated with the b0377 audit confirmation.
- `costs.log` updated with `audit-no-write` event (0 bytes, written=0, deferred=0).
- `provenance.log` not updated (no records written).
- `gaps.md` not updated (no new deferrals; existing entries stand).
- B2 sync deferred to host (rclone not in sandbox).
- SQLite ingestion deferred to host (corpus.sqlite FTS5 malformed-disk-image
  carry-forward; canonical source-of-truth remains `records/*.json`).
