# Batch 0376 — Phase 5 reparse-first INVENTORY AUDIT (no parser write)

**Date:** 2026-04-30T22:05:00Z
**Phase:** phase_5_judgments (approved: true, complete: false)
**Parser:** parser_v0.3.1 (frozen baseline `scripts/batch_0360_parse.py`)
**Mode:** AUDIT — confirms b0375 finding; no fresh fetches; no parse output commit
**Slice attempted:** none (audit only)

## Result: NO COMMIT OF PARSE OUTPUT — v0.3.1-addressable reparse inventory remains exhausted

This tick re-verified the b0375 finding from a clean audit, using a court+year+number
key match across `raw/zambialii/judgments/{zmcc,zmsc}/` against `records/judgments/`
(rather than relying on full-stem string equality, which produced spurious mismatches
on ZMSC short-form record filenames).

### Inventory snapshot (2026-04-30T22:05Z)

| Court | Years on disk | Raw HTML+PDF pairs | Records written | Missing (raw, no record) |
|-------|---------------|--------------------|-----------------|--------------------------|
| ZMCC  | 2021–2026     | 142                | 53              | 89                       |
| ZMSC  | 2025–2026     | 24                 | 24              | 0                        |
| **Total** | —          | **166**            | **77**          | **89**                   |

(One additional record under `records/judgments/judgment-zm-2026-scz-09-konkola-v-ag.json`
sits at the root from earlier work and is not split by court directory; total records on
disk = 78. Phase 5 progress: 78 / 100–160.)

### All 89 missing candidates are already deferred in `gaps.md`

Cross-checked by court+year+number against every mention of `[YYYY] ZMCC N`,
`zmcc/YYYY/N`, and `judgment-zm-YYYY-zmcc-N` in `gaps.md`. Result: 89/89 missing
candidates appear in `gaps.md`. None are unaddressed.

Deferral reason distribution across `gaps.md` (after counting all per-record entries
including duplicate b0344 legacy + b0362/b0363 reparse cross-references):

- `html_no_summary_pdf_no_match` — 115 mentions
- `parser_v0.3.1_judges_no_comma_unhandled` — 14 mentions
- `pdf_extraction_empty_likely_scanned` — 10 mentions
- `multi_judge_separate_opinions_no_clear_majority_disposition` — 2 mentions
- `outcome_inferred_but_detail_unsafe` — 0 mentions
- legacy `outcome_not_inferable_under_tightened_policy` — 49 mentions (all from
  pre-v0.3.1 batches; every one has a follow-up reparse entry under b0362/b0363/
  b0365/b0366/b0368–0374 with a v0.3.1 specific reason code)

### Why a v0.3.1 reparse this tick would be wasted work

- All four v0.3.1 specific reason codes (`html_no_summary_pdf_no_match`,
  `parser_v0.3.1_judges_no_comma_unhandled`, `pdf_extraction_empty_likely_scanned`,
  `multi_judge_separate_opinions_no_clear_majority_disposition`) are by definition
  not addressable by parser_v0.3.1 itself — they were assigned BECAUSE v0.3.1 could
  not produce a safe outcome for the candidate.
- The legacy 49 `outcome_not_inferable_under_tightened_policy` entries have
  documented v0.3.1 follow-ups in later gaps.md sections; spot-checked
  zmcc/2024/{4,5} (b0344 legacy + b0354 v0.3.1 reparse → both `html_no_summary_pdf_no_match`).
- ZMSC has zero raw-on-disk no-record candidates.
- A fresh DESC sweep into older ZMSC years would consume fetch budget without
  changing the parser disposition-extraction yield rate; per `reparse_first_note`
  fresh sweeps are permitted now (no v0.3.1-addressable inventory remains), but
  given that ~85% of the ZMCC backlog produced `html_no_summary_pdf_no_match`,
  a ZMSC pre-2025 sweep would likely reproduce the same pattern under v0.3.1.

## Action taken this tick

- Cleared stale `.git/*.lock` and `.git/*.lock.bak` files (per task instruction step 1).
- `git pull --ff-only` ⇒ Already up to date.
- Read `approvals.yaml`. Phase 5 is approved+incomplete; reparse_first: true.
- Verified ZMCC + ZMSC raw-vs-records inventory under court+year+number keying.
- Cross-checked all 89 missing candidates against `gaps.md` ⇒ 89/89 already deferred.
- Confirmed all v0.3.1-specific reason codes are by definition not v0.3.1-addressable.
- Confirmed legacy `outcome_not_inferable_under_tightened_policy` mentions all have
  documented v0.3.1 follow-ups in later gaps.md sections.
- No parse run executed (would have produced 0 / 0 / 0).
- No new fetch issued (0 bytes; cumulative_today still ~22/2000 carried from yesterday).
- No `gaps.md`, `provenance.log`, `corpus.sqlite`, or `records/*.json` writes.

## Recommendation

`parser_v0.3.2 vocabulary widening` (declaratory operative verbs;
judges-no-comma format; procedural-refusal patterns; "discontinuance allowed",
"challenge … dismissed for lack", "application … dismissed for failing",
"declaratory relief was academic", "single-judge declined", etc.) and
`OCR pipeline` (for the 4 `pdf_extraction_empty_likely_scanned` candidates)
remain the dominant unblocks. Both are subject to Peter's approval per
BRIEF.md non-negotiable on parser changes.

Until either parser_v0.3.2 or OCR is approved in `approvals.yaml`, the worker
will continue producing audit-only ticks. The next tick should default to the
same audit-only output unless `approvals.yaml` shows a new approval.

**Suggested next-tick action:** log "idle — awaiting parser_v0.3.2 approval
(no v0.3.1-addressable reparse inventory remaining)" and stop.

## Logs

- `worker.log` updated with the audit confirmation and the recommendation above.
- `costs.log` updated with `audit-no-write` event (0 bytes, written=0, deferred=0).
- `provenance.log` not updated (no records written).
- `gaps.md` not updated (no new deferrals; existing cross-references stand).
- B2 sync deferred to host (rclone not in sandbox).
- SQLite ingestion deferred to host (corpus.sqlite FTS5 malformed-disk-image carry-forward).
