# Batch 0365 — Phase 5 reparse-first triage continuation

- Tick start: 2026-04-30T17:00:00Z
- Sandbox session: vigilant-confident-ramanujan
- Phase: phase_5_judgments (approved + incomplete)
- Parser version: 0.3.1 (frozen baseline `scripts/batch_0360_parse.py`,
  copied via `scripts/batch_0364_parse.py` to `scripts/batch_0365_parse.py`
  with only TARGETS slice + `_work` directory + version-bump comments;
  the b0361 specific-reason-code refinement is preserved unchanged)
- Mode: REPARSE-FIRST (zero fresh fetch budget consumed)

## Slice

Continuation of the b0364 reparse-first sweep (next eight raw
HTML+PDF pairs already on disk, year-DESC then num-DESC after the
b0364 set; zmcc/2023/22 already in records/ and correctly skipped
by the SKIP-existing guard at parse time):

| # | Court/Year/# | Date       | Source URL |
|---|--------------|------------|------------|
| 1 | zmcc/2024/03 | 2024-02-09 | https://zambialii.org/akn/zm/judgment/zmcc/2024/3/eng@2024-02-09 |
| 2 | zmcc/2024/02 | 2024-01-17 | https://zambialii.org/akn/zm/judgment/zmcc/2024/2/eng@2024-01-17 |
| 3 | zmcc/2024/01 | 2024-01-25 | https://zambialii.org/akn/zm/judgment/zmcc/2024/1/eng@2024-01-25 |
| 4 | zmcc/2023/27 | 2023-08-03 | https://zambialii.org/akn/zm/judgment/zmcc/2023/27/eng@2023-08-03 |
| 5 | zmcc/2023/26 | 2023-12-16 | https://zambialii.org/akn/zm/judgment/zmcc/2023/26/eng@2023-12-16 |
| 6 | zmcc/2023/25 | 2023-12-08 | https://zambialii.org/akn/zm/judgment/zmcc/2023/25/eng@2023-12-08 |
| 7 | zmcc/2023/24 | 2023-12-01 | https://zambialii.org/akn/zm/judgment/zmcc/2023/24/eng@2023-12-01 |
| 8 | zmcc/2023/23 | 2023-11-07 | https://zambialii.org/akn/zm/judgment/zmcc/2023/23/eng@2023-11-07 |

## Yield

- Records written: **3 / 8**
- Records deferred: **5 / 8** (specific reason codes, no banned generic)
- Outcome-source breakdown: 3/3 via `pdf-tail-2pages` fallback
- Fresh fetches this tick: **0** (all raw bytes already on disk —
  reparse-first compliance)

### Written

| Record ID | Outcome | Source | Detail (truncated) |
|-----------|---------|--------|--------------------|
| `judgment-zm-2024-zmcc-03-hastings-mwila-v-local-authorities-superannuation` | dismissed | pdf-tail-2pages | "[90] We thus find no merit in the Petitioner's case and we dismiss it" |
| `judgment-zm-2024-zmcc-01-bowman-chilosha-lusambo-v-bernard-kanengo-and-ors` | dismissed | pdf-tail-2pages | "1] Our conclusion is that all grounds of appeal fail and are hereby" |
| `judgment-zm-2023-zmcc-24-fredson-kango-yamba-v-the-principal-resident-magis` | dismissed | pdf-tail-2pages | "[44] Accordingly, the Petition fails and is hereby dismissed" |

### Deferred

All five classified with the specific code
`html_no_summary_pdf_no_match` from `approvals.yaml`
`deferral_reasons_locked`; the banned generic
`outcome_not_inferable_under_tightened_policy` was NOT used. Raw
HTML+PDF retained on disk for a future widened-vocabulary or
OCR-augmented re-parse.

| Court/Year/# | Reason |
|--------------|--------|
| zmcc/2024/02 | html_no_summary_pdf_no_match |
| zmcc/2023/27 | html_no_summary_pdf_no_match |
| zmcc/2023/26 | html_no_summary_pdf_no_match |
| zmcc/2023/25 | html_no_summary_pdf_no_match |
| zmcc/2023/23 | html_no_summary_pdf_no_match |

See gaps.md "Batch 0365" section for per-record case names,
case numbers, summary heads, and deferral rationale.

## Integrity

`scripts/integrity_check_b0365.py` PASS (3 records). All required
fields present, source_hash and raw_sha256 match raw HTML/PDF on
disk, judges resolve in `judges_registry.yaml`, outcome enum +
court enum + role enum all valid, outcome_detail safety checks
green (12+ alphabetic chars; no blacklisted substrings; no
mid-word-fragment leading char), no duplicate IDs.

## Budget impact

- Fresh fetches: 0 (reparse-pass: zero-cost)
- Cumulative today: ~15 -> ~15 / 2000 (~0.75%) — pre-tick fetch counter
  unchanged because no new HTTP requests issued.
- Tokens: not separately metered this tick
- B2 sync: deferred to host (rclone not available in sandbox)
- SQLite ingestion: deferred to host (corpus.sqlite FTS5 index
  reports `database disk image is malformed` on read — consistent
  with the b0360–b0364 pattern of skipping in-tick SQLite writes;
  records JSON files are the source of truth on disk and will be
  picked up by the next host-side rebuild)

## Phase 5 progress

- Before tick: 39 / 100-160 target
- After tick:  **42 / 100-160** target

## Pattern observation (b0361 → b0362 → b0363 → b0364 → b0365)

The `pdf-tail-2pages` fallback continues to rescue a non-trivial
fraction of the deferred-queue candidates (b0361: 2/8; b0362: 0/8;
b0363: 0/8; b0364: 2/8; b0365: 3/8 — combined yield 7/40 = 17.5 %).
This tick's three rescues all relied on numbered/closing
disposition lines ("[44] Accordingly, the Petition fails and is
hereby dismissed", "[90] We thus find no merit … and we dismiss
it", "1] Our conclusion is that all grounds of appeal fail and
are hereby [dismissed]"). The five deferrals are again ratio-style
or partial-disposition summaries (joinder permitted; leave-to-amend
limited; impartiality-rebuttal; presidential-residence
justiciability; originating-summons dismissed-as-personalised) that
do not match SUMMARY_PATTERNS, paired with PDF tails that lack a
recognised disposition phrasing. The recommendation to bump to
parser_v0.3.2 (vocabulary widening) remains the highest-leverage
next step, subject to Peter's approval.

## Next tick

Two viable paths (unchanged from b0364):

1. **Continue reparse-first sweep** (mechanical, low-yield expected):
   target zmcc/2023/{21,20,19,18,17,16,15,14} — the next eight
   raw-on-disk candidates with no record (year-DESC, num-DESC,
   skipping zmcc/2023/22 already in records/). Zero fetch cost.
   Likely yield similar to b0365 (a handful via pdf-tail-2pages,
   the rest deferred under `html_no_summary_pdf_no_match`).

2. **Pivot to parser-vocabulary widening** (recommended after one
   more confirmatory reparse tick): a parser_v0.3.2 bump that adds
   (a) "denied | refused | granted in part | declaratory relief
   refused | improperly filed | joinder permitted | leave to amend
   limited" to SUMMARY_PATTERNS and (b) a passive-voice
   operative-paragraph extractor would likely resolve a sizeable
   fraction of the current deferred backlog. This parser bump
   requires Peter's approval; the recommendation is logged here
   for the next human review.

3. **OCR pass on scanned PDFs**: `zmcc/2021/{15,14}` (b0360) and
   `zmcc/2025/19` (b0362) remain deferred under
   `pdf_extraction_empty_likely_scanned`. A small Tesseract-driven
   OCR pass would unblock these specifically.

`phase_5_judgments` remains approved + incomplete; worker does not
flip approval flags. Next tick continues the reparse-first sweep.
