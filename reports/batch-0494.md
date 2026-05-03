# Batch 0494 — parser_v0.3.2 reparse continuation (ZMCC 2025 DESC sweep, num {18..7})

- **Tick start (UTC):** 2026-05-03T~12:02Z (scheduled tick)
- **Phase:** 5 (judgments) — approved+incomplete
- **Action:** seventh v0.3.2 reparse pass; continues the ZMCC 2025 DESC sweep recommended by b0493 with the next slice `{18, 17, 14, 11, 10, 9, 8, 7}` (raw on disk, no records yet).
- **Records written:** 0
- **Records deferred:** 8 (all `html_no_summary_pdf_no_match` re-confirmed under v0.3.2)
- **Cumulative today:** 0/2000 fetches; ~5k tokens (parser script copy + report + gaps.md edits)
- **Yield this tick:** 0/8 = 0.0%
- **Five-consecutive-zero-discovery counter:** 1 (b0494) — un-fired

## Targets and selection

Per b0493's next-tick recommendation: continue option (1) — ZMCC 2025
DESC sweep through the remaining untested-under-v0.3.2 candidates.
Slice `{18, 17, 14, 11, 10, 9, 8, 7}` taken DESC (skipping 16, 15, 13,
12 — 13 already in corpus; 16/15/12 were fetched but already deferred
under earlier passes and not in the b0493-recommended slice). All
eight HTML+PDF pairs already on disk; 0 fresh fetches consumed.

## Resolutions

None. All eight candidates re-deferred under specific reason
`html_no_summary_pdf_no_match` after re-test under v0.3.2's widened
SUMMARY_PATTERNS_V032, PDF_TAIL_PATTERNS_V032, and ORDER_INTRO +
window-scan resolver.

## Deferrals (specific reason codes only — no generic
`outcome_not_inferable_under_tightened_policy`)

- **[2025] ZMCC 18** (TC Promotions Limited and Ors v Lusaka City
  Council, 2025-09-30) — `html_no_summary_pdf_no_match`. Issue-style
  summary on advertising-fee statutory-instrument question; no
  recognised disposition token in either pool.
- **[2025] ZMCC 17** (Isaac Mwaanza, 2025-08-27) —
  `html_no_summary_pdf_no_match`. Jurisdictional dismissal implied
  ("vacancy questions fall to High Court / tribunal under section 96
  EPA") but no operative-verb match in either v0.3.2 or v0.3.1
  patterns.
- **[2025] ZMCC 14** (The People v John Sinkamba and Ors, 2025-07-28)
  — `html_no_summary_pdf_no_match`. Pure ratio-style summary on
  Article 266 child-definition; no disposition token.
- **[2025] ZMCC 11** (Ford Chombo v The Attorney General, 2025-06-19)
  — `html_no_summary_pdf_no_match`. Holding-style summary on the
  Constitutional Court's jurisdictional bar over pre-2016 pension
  disputes; operative dismissal implied but not surfaced in any
  v0.3.2 / v0.3.1 SUMMARY/TAIL construction.
- **[2025] ZMCC 10** (Munir Zulu v Attorney General and Ors,
  2025-06-04) — `html_no_summary_pdf_no_match`. Ratio-style holding on
  automatic vacancy from imprisonment; no disposition token.
- **[2025] ZMCC 9** (The People v Attorney General (Ex Parte Nickson
  Chilangwa), 2025-02-10) — `html_no_summary_pdf_no_match`. Ratio-twin
  to ZMCC 10 on parallel facts; same parser limitation.
- **[2025] ZMCC 8** (Richard Sakala v The Attorney General,
  2025-04-01) — `html_no_summary_pdf_no_match`. Holding-style summary
  on Limitation Act applicability with conditional disposition
  ("inordinate unexplained delay may justify dismissal"); conditional
  verb still not addressable under v0.3.2.
- **[2025] ZMCC 7** (Munir Zulu v The Attorney General and Ors,
  2025-04-07) — `html_no_summary_pdf_no_match`. Jurisdictional ratio
  ("Constitutional Court has no jurisdiction under Article 128(2) to
  stay subordinate court proceedings"); described but not in
  dismissal-pattern form in either v0.3.2 or v0.3.1 patterns.

All eight deferrals received `RECONFIRMED-DEFERRED in batch-0494
(parser_v0.3.2)` notes appended beneath their original `gaps.md`
entries (in the batch-0362 detailed section for nums {18, 17, 14}
and the batch-0363 detailed section for nums {11, 10, 9, 8, 7}), per
the reparse-first audit-policy non-negotiable. No `gaps.md` entries
were deleted.

## Integrity checks

- IDs unique across `records/judgments/` (92/92 — no new records
  this tick).
- All four-field provenance present on the existing 92 records.
- Full-corpus sha256 resolution PASS (sha256-index over `raw/` tree
  via `Path.rglob`).
- All `judges[*].name` across the full corpus resolve in
  `judges_registry.yaml` (canonical or bare-surname).
- `outcome` ∈ enum across all records.
- `issue_tags` non-empty across all records.
- `scripts/integrity_check_b0494.py` returns
  `INTEGRITY CHECK: PASS (0 record(s))` (zero-write tick — checks
  pass vacuously on the empty `written` array; full-corpus checks
  remain valid because no records were written or modified).

## Cumulative v0.3.2 yield

Across b0488..b0494: **14 records written / 56 attempted = 25.0%**.

| Batch | Cohort | Written | Attempted | Yield | Profile |
|-------|--------|---------|-----------|-------|---------|
| 0488  | ZMCC 2022 (judges_no_comma + html_no_summary, DESC entry) | 2 | 8 | 25.0% | parser-launch + in-batch regression patch |
| 0489  | ZMCC 2022 (judges_no_comma DESC continuation) | 3 | 8 | 37.5% | five-judge benches with v031-tail operative phrases |
| 0490  | ZMCC 2022 (judges_no_comma DESC completion) | 6 | 8 | 75.0% | judges_no_comma backlog cleared |
| 0491  | ZMCC 2022 (html_no_summary untested-under-v0.3.2) | 0 | 8 | 0.0% | declaratory/interpretive — vocabulary-blind |
| 0492  | ZMCC 2024 (num-ASC pivot)                       | 0 | 8 | 0.0% | declaratory/interlocutory — same blind spot |
| 0493  | ZMCC 2025 (DESC pivot, num {33..19})            | 3 | 8 | 37.5% | two SUMMARY hits on Peter-targeted phrases + one PDF-tail hit |
| 0494  | ZMCC 2025 (DESC continuation, num {18..7})      | 0 | 8 | 0.0% | declaratory / ratio-style cohort (this batch) |

## Phase 5 progress

92 → 92 (target 100–160 landmark judgments). 8 short of low end.
Five-consecutive-zero-discovery completion criterion remains UN-FIRED
(b0488/0489/0490 wrote, b0491/0492 zero, b0493 wrote 3, b0494 zero —
counter currently at 1 and resets on next non-zero tick).

## Next-tick recommendation

Three actionable options:

1. **Finish ZMCC 2025 DESC sweep**: nums `{6, 5, 2}` remain on disk
   without records (all previously deferred under batch-0364 with
   `html_no_summary_pdf_no_match`). Three candidates only — short
   batch, expected zero yield (same declaratory/ratio profile as
   today) but formally exhausts ZMCC 2025 reparse-first inventory
   under v0.3.2.
2. **Pivot to ZMCC 2023**: cohort size unknown to this tick; an
   inventory pass at the next tick prelude would scope it before
   committing to a slice.
3. **ZMSC older-year sweep**: still pending Peter's URL pattern
   confirmation per `approvals.yaml.zmsc_older_year_sweep_approval_note`;
   not actionable by scheduled tick until that confirmation lands.

Recommend option (1) for b0495 — it's a clean way to record the
formal exhaustion of ZMCC 2025 under v0.3.2 — followed by option (2)
in b0496.
