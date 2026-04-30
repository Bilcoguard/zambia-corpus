# Batch 0362 — Phase 5 reparse-first triage continuation

- Tick start: 2026-04-30T16:00:00Z
- Sandbox session: wonderful-sweet-bohr
- Phase: phase_5_judgments (approved + incomplete)
- Parser version: 0.3.1 (frozen baseline `scripts/batch_0360_parse.py`,
  copied via `scripts/batch_0361_parse.py` to `scripts/batch_0362_parse.py`
  with only TARGETS slice + `_work` directory + version-bump comments;
  the b0361 specific-reason-code refinement is preserved unchanged)
- Mode: REPARSE-FIRST (zero fresh fetch budget consumed)

## Slice

Continuation of the b0361 reparse-first sweep (next eight raw
HTML+PDF pairs already on disk, year-DESC then num-DESC after the
b0361 set):

| # | Court/Year/# | Date       | Source URL |
|---|--------------|------------|------------|
| 1 | zmcc/2025/22 | 2025-11-27 | https://zambialii.org/akn/zm/judgment/zmcc/2025/22/eng@2025-11-27 |
| 2 | zmcc/2025/21 | 2025-11-25 | https://zambialii.org/akn/zm/judgment/zmcc/2025/21/eng@2025-11-25 |
| 3 | zmcc/2025/19 | 2025-09-30 | https://zambialii.org/akn/zm/judgment/zmcc/2025/19/eng@2025-09-30 |
| 4 | zmcc/2025/18 | 2025-09-30 | https://zambialii.org/akn/zm/judgment/zmcc/2025/18/eng@2025-09-30 |
| 5 | zmcc/2025/17 | 2025-08-27 | https://zambialii.org/akn/zm/judgment/zmcc/2025/17/eng@2025-08-27 |
| 6 | zmcc/2025/16 | 2025-08-25 | https://zambialii.org/akn/zm/judgment/zmcc/2025/16/eng@2025-08-25 |
| 7 | zmcc/2025/15 | 2025-07-23 | https://zambialii.org/akn/zm/judgment/zmcc/2025/15/eng@2025-07-23 |
| 8 | zmcc/2025/14 | 2025-07-28 | https://zambialii.org/akn/zm/judgment/zmcc/2025/14/eng@2025-07-28 |

## Yield

- Records written: **0 / 8**
- Records deferred: **8 / 8** (specific reason codes, no banned generic)
- Outcome-source breakdown: n/a (no records written this tick)
- Fresh fetches this tick: **0** (all raw bytes already on disk —
  reparse-first compliance)

### Written

(none)

### Deferred

All eight classified with specific codes from `approvals.yaml`
`deferral_reasons_locked`; the banned generic
`outcome_not_inferable_under_tightened_policy` was NOT used. Raw
HTML+PDF retained on disk for a future widened-vocabulary or
OCR-augmented re-parse.

| Court/Year/# | Reason |
|--------------|--------|
| zmcc/2025/22 | html_no_summary_pdf_no_match |
| zmcc/2025/21 | html_no_summary_pdf_no_match |
| zmcc/2025/19 | pdf_extraction_empty_likely_scanned |
| zmcc/2025/18 | html_no_summary_pdf_no_match |
| zmcc/2025/17 | html_no_summary_pdf_no_match |
| zmcc/2025/16 | html_no_summary_pdf_no_match |
| zmcc/2025/15 | html_no_summary_pdf_no_match |
| zmcc/2025/14 | html_no_summary_pdf_no_match |

See gaps.md "Batch 0362" section for per-record summary heads and
deferral rationale.

## Integrity

`scripts/integrity_check_b0362.py` PASS (0 records). With zero
records written this tick the check is structurally vacuous, but
the script still ran to confirm no schema regression in the
parse_summary contract and no unexpected partial-write artefacts
under `records/judgments/zmcc/2025/`.

## Budget impact

- Fresh fetches: 0 (reparse-pass: zero-cost)
- Cumulative today: ~15 -> ~15 / 2000 (~0.75%)
- Tokens: not separately metered this tick
- B2 sync: deferred to host (rclone not available in sandbox)

## Phase 5 progress

- Before tick: 37 / 100-160 target
- After tick:  **37 / 100-160** target (zero net change; high-quality
  no-fabrication outcome)

## Discovery / completion-criterion accounting

Two consecutive low-yield reparse ticks (b0361: 2 written / 6
deferred; b0362: 0 written / 8 deferred). Neither tick performed a
fresh DESC sweep, so the BRIEF.md "five consecutive zero-discovery
ticks" completion criterion does NOT apply here — the reparse-first
pass is bounded above by the existing on-disk backlog (~96 candidates
remaining after this tick) and is not a discovery probe. When the
reparse queue is exhausted we resume fresh DESC sweeps; only then
does the zero-discovery counter apply.

## Next tick

Two viable paths:

1. **Continue reparse-first sweep** (recommended for one more tick):
   target zmcc/2025/{12,11,10,9,8,7,6,5} — eight more raw-on-disk
   candidates with no record. Zero fetch cost. Likely yield is again
   low (most 2025 ZMCC summaries are holding-style rather than
   disposition-style), but it clears the queue ahead of any future
   parser-vocabulary widening.

2. **Pivot to parser-vocabulary widening** (recommended after one
   more reparse tick): the dominant deferral reason is
   `html_no_summary_pdf_no_match` driven by holding-style summaries
   and PDFs that bury the operative paragraph in passive voice. A
   parser_v0.3.2 bump that adds (a) a "denied | refused | granted in
   part | declaratory relief refused" SUMMARY_PATTERNS extension and
   (b) a passive-voice operative-paragraph extractor would likely
   resolve a sizeable fraction of the current deferred backlog.
   That parser bump requires Peter's approval; logging the
   recommendation here for the next human review.

3. **OCR pass on scanned PDFs**: `zmcc/2021/{15,14}` (b0360) and
   `zmcc/2025/19` (this tick) are deferred under
   `pdf_extraction_empty_likely_scanned`. A small Tesseract-driven
   OCR pass would unblock these specifically.

`phase_5_judgments` remains approved + incomplete; worker does not
flip approval flags. Next tick continues the reparse-first sweep.
