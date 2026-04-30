# Batch 0363 — Phase 5 reparse-first triage continuation

- Tick start: 2026-04-30T16:30:00Z
- Sandbox session: determined-youthful-cannon
- Phase: phase_5_judgments (approved + incomplete)
- Parser version: 0.3.1 (frozen baseline `scripts/batch_0360_parse.py`,
  copied via `scripts/batch_0362_parse.py` to `scripts/batch_0363_parse.py`
  with only TARGETS slice + `_work` directory + version-bump comments;
  the b0361 specific-reason-code refinement is preserved unchanged)
- Mode: REPARSE-FIRST (zero fresh fetch budget consumed)

## Slice

Continuation of the b0362 reparse-first sweep (next eight raw
HTML+PDF pairs already on disk, year-DESC then num-DESC after the
b0362 set):

| # | Court/Year/# | Date       | Source URL |
|---|--------------|------------|------------|
| 1 | zmcc/2025/12 | 2025-06-27 | https://zambialii.org/akn/zm/judgment/zmcc/2025/12/eng@2025-06-27 |
| 2 | zmcc/2025/11 | 2025-06-19 | https://zambialii.org/akn/zm/judgment/zmcc/2025/11/eng@2025-06-19 |
| 3 | zmcc/2025/10 | 2025-06-04 | https://zambialii.org/akn/zm/judgment/zmcc/2025/10/eng@2025-06-04 |
| 4 | zmcc/2025/09 | 2025-02-10 | https://zambialii.org/akn/zm/judgment/zmcc/2025/9/eng@2025-02-10 |
| 5 | zmcc/2025/08 | 2025-04-01 | https://zambialii.org/akn/zm/judgment/zmcc/2025/8/eng@2025-04-01 |
| 6 | zmcc/2025/07 | 2025-04-07 | https://zambialii.org/akn/zm/judgment/zmcc/2025/7/eng@2025-04-07 |
| 7 | zmcc/2025/06 | 2025-03-24 | https://zambialii.org/akn/zm/judgment/zmcc/2025/6/eng@2025-03-24 |
| 8 | zmcc/2025/05 | 2025-03-24 | https://zambialii.org/akn/zm/judgment/zmcc/2025/5/eng@2025-03-24 |

## Yield

- Records written: **0 / 8**
- Records deferred: **8 / 8** (specific reason codes, no banned generic)
- Outcome-source breakdown: n/a (no records written this tick)
- Fresh fetches this tick: **0** (all raw bytes already on disk —
  reparse-first compliance)

### Written

(none)

### Deferred

All eight classified with the specific code
`html_no_summary_pdf_no_match` from `approvals.yaml`
`deferral_reasons_locked`; the banned generic
`outcome_not_inferable_under_tightened_policy` was NOT used. Raw
HTML+PDF retained on disk for a future widened-vocabulary or
OCR-augmented re-parse.

| Court/Year/# | Reason |
|--------------|--------|
| zmcc/2025/12 | html_no_summary_pdf_no_match |
| zmcc/2025/11 | html_no_summary_pdf_no_match |
| zmcc/2025/10 | html_no_summary_pdf_no_match |
| zmcc/2025/09 | html_no_summary_pdf_no_match |
| zmcc/2025/08 | html_no_summary_pdf_no_match |
| zmcc/2025/07 | html_no_summary_pdf_no_match |
| zmcc/2025/06 | html_no_summary_pdf_no_match |
| zmcc/2025/05 | html_no_summary_pdf_no_match |

See gaps.md "Batch 0363" section for per-record case names,
case numbers, summary heads, and deferral rationale.

## Integrity

`scripts/integrity_check_b0363.py` PASS (0 records). With zero
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

Three consecutive low-yield reparse ticks (b0361: 2 written / 6
deferred; b0362: 0 written / 8 deferred; b0363: 0 written / 8
deferred). None of these performed a fresh DESC sweep, so the
BRIEF.md "five consecutive zero-discovery ticks" completion
criterion does NOT apply — the reparse-first pass is bounded above
by the existing on-disk backlog (~88 candidates remaining after
this tick) and is not a discovery probe. When the reparse queue is
exhausted we resume fresh DESC sweeps; only then does the
zero-discovery counter apply.

## Pattern observation (b0361 → b0362 → b0363)

Across these three reparse ticks the parser_v0.3.1 yield trends
sharply downward as the slice descends through the 2025 backlog
(2 → 0 → 0). The deferral profile is overwhelmingly
`html_no_summary_pdf_no_match` driven by ZambiaLII's editorial
preference for a ratio-style holding head ("Court holds…", "A
pre-2016 pension dispute is…", "Imprisonment automatically vacates
…") rather than a disposition-style closer ("Petition dismissed").
PDF tails confirm the operative paragraph exists but in voicing
the parser does not recognise. This is the strongest signal yet
that further reparse ticks under the same parser will continue to
return zero, and that closure of this segment of the queue requires
a parser_v0.3.2 vocabulary widening (subject to Peter's approval).

## Next tick

Two viable paths:

1. **Continue reparse-first sweep** (mechanical, low yield expected):
   target zmcc/2025/{04,03,02,01} + zmcc/2024/{n…} — the next
   eight raw-on-disk candidates with no record. Zero fetch cost.
   Likely yield is again low for the same ratio-style-summary
   reason, but it clears the queue ahead of any future
   parser-vocabulary widening.

2. **Pivot to parser-vocabulary widening** (recommended after one
   more confirmatory reparse tick): a parser_v0.3.2 bump that adds
   (a) "denied | refused | granted in part | declaratory relief
   refused | improperly filed" to SUMMARY_PATTERNS and (b) a
   passive-voice operative-paragraph extractor would likely resolve
   a sizeable fraction of the current deferred backlog (3 of 3
   reparse ticks now point in the same direction). That parser bump
   requires Peter's approval; the recommendation is logged here for
   the next human review.

3. **OCR pass on scanned PDFs**: `zmcc/2021/{15,14}` (b0360) and
   `zmcc/2025/19` (b0362) remain deferred under
   `pdf_extraction_empty_likely_scanned`. A small Tesseract-driven
   OCR pass would unblock these specifically.

`phase_5_judgments` remains approved + incomplete; worker does not
flip approval flags. Next tick continues the reparse-first sweep.
