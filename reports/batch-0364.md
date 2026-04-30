# Batch 0364 — Phase 5 reparse-first triage continuation

- Tick start: 2026-04-30T16:35:00Z
- Sandbox session: loving-gifted-brown
- Phase: phase_5_judgments (approved + incomplete)
- Parser version: 0.3.1 (frozen baseline `scripts/batch_0360_parse.py`,
  copied via `scripts/batch_0363_parse.py` to `scripts/batch_0364_parse.py`
  with only TARGETS slice + `_work` directory + version-bump comments;
  the b0361 specific-reason-code refinement is preserved unchanged)
- Mode: REPARSE-FIRST (zero fresh fetch budget consumed)

## Slice

Continuation of the b0363 reparse-first sweep (next eight raw
HTML+PDF pairs already on disk, year-DESC then num-DESC after the
b0363 set; zmcc/2025/04 and zmcc/2024/09 already in records/ and
correctly skipped by the SKIP-existing guard at parse time):

| # | Court/Year/# | Date       | Source URL |
|---|--------------|------------|------------|
| 1 | zmcc/2025/03 | 2025-03-06 | https://zambialii.org/akn/zm/judgment/zmcc/2025/3/eng@2025-03-06 |
| 2 | zmcc/2025/02 | 2025-02-06 | https://zambialii.org/akn/zm/judgment/zmcc/2025/2/eng@2025-02-06 |
| 3 | zmcc/2025/01 | 2025-02-13 | https://zambialii.org/akn/zm/judgment/zmcc/2025/1/eng@2025-02-13 |
| 4 | zmcc/2024/08 | 2024-06-07 | https://zambialii.org/akn/zm/judgment/zmcc/2024/8/eng@2024-06-07 |
| 5 | zmcc/2024/07 | 2024-06-06 | https://zambialii.org/akn/zm/judgment/zmcc/2024/7/eng@2024-06-06 |
| 6 | zmcc/2024/06 | 2024-04-16 | https://zambialii.org/akn/zm/judgment/zmcc/2024/6/eng@2024-04-16 |
| 7 | zmcc/2024/05 | 2024-03-15 | https://zambialii.org/akn/zm/judgment/zmcc/2024/5/eng@2024-03-15 |
| 8 | zmcc/2024/04 | 2024-02-23 | https://zambialii.org/akn/zm/judgment/zmcc/2024/4/eng@2024-02-23 |

## Yield

- Records written: **2 / 8**
- Records deferred: **6 / 8** (specific reason codes, no banned generic)
- Outcome-source breakdown: 2/2 via `pdf-tail-2pages` fallback
- Fresh fetches this tick: **0** (all raw bytes already on disk —
  reparse-first compliance)

### Written

| Record ID | Outcome | Source | Detail (truncated) |
|-----------|---------|--------|--------------------|
| `judgment-zm-2025-zmcc-03-petrushika-trading-limited-v-the-attorney-general` | dismissed | pdf-tail-2pages | "Petition fails and is hereby dismissed" |
| `judgment-zm-2025-zmcc-01-dr-godfrey-hampwaya-and-ors-v-the-council-of-the-u` | dismissed | pdf-tail-2pages | "1] The petition is dismissed for lack of merit" |

### Deferred

All six classified with the specific code
`html_no_summary_pdf_no_match` from `approvals.yaml`
`deferral_reasons_locked`; the banned generic
`outcome_not_inferable_under_tightened_policy` was NOT used. Raw
HTML+PDF retained on disk for a future widened-vocabulary or
OCR-augmented re-parse.

| Court/Year/# | Reason |
|--------------|--------|
| zmcc/2025/02 | html_no_summary_pdf_no_match |
| zmcc/2024/08 | html_no_summary_pdf_no_match |
| zmcc/2024/07 | html_no_summary_pdf_no_match |
| zmcc/2024/06 | html_no_summary_pdf_no_match |
| zmcc/2024/05 | html_no_summary_pdf_no_match |
| zmcc/2024/04 | html_no_summary_pdf_no_match |

See gaps.md "Batch 0364" section for per-record case names,
case numbers, summary heads, and deferral rationale.

## Integrity

`scripts/integrity_check_b0364.py` PASS (2 records). All required
fields present, source_hash and raw_sha256 match raw HTML/PDF on
disk, judges resolve in `judges_registry.yaml` (Chisunka, Mulongoti,
Mwandenga, Musaluke, Kawimbe — all under `JJC` title), outcome enum
+ court enum + role enum all valid, outcome_detail safety checks
green (12+ alphabetic chars; no blacklisted substrings; no
mid-word-fragment leading char), no duplicate IDs.

## Budget impact

- Fresh fetches: 0 (reparse-pass: zero-cost)
- Cumulative today: 19 -> 19 / 2000 (~0.95%) — pre-tick fetch counter
  unchanged because no new HTTP requests issued. (The 19 entries
  reflect b0360 + b0361 + b0362 + b0363 cumulative HTML+PDF
  fetches earlier today.)
- Tokens: not separately metered this tick
- B2 sync: deferred to host (rclone not available in sandbox)
- SQLite ingestion: deferred to host (corpus.sqlite FTS5 index
  reports `database disk image is malformed` on read — consistent
  with the b0360–b0363 pattern of skipping in-tick SQLite writes;
  records JSON files are the source of truth on disk and will be
  picked up by the next host-side rebuild)

## Phase 5 progress

- Before tick: 37 / 100-160 target
- After tick:  **39 / 100-160** target

## Discovery / completion-criterion accounting

Four consecutive low-yield reparse ticks (b0361: 2 written / 6
deferred; b0362: 0 written / 8 deferred; b0363: 0 written / 8
deferred; b0364: 2 written / 6 deferred). None of these performed
a fresh DESC sweep, so the BRIEF.md "five consecutive zero-discovery
ticks" completion criterion does NOT apply — the reparse-first pass
is bounded above by the existing on-disk backlog and is not a
discovery probe. When the reparse queue is exhausted we resume
fresh DESC sweeps; only then does the zero-discovery counter apply.

## Pattern observation (b0361 → b0362 → b0363 → b0364)

The `pdf-tail-2pages` fallback continues to rescue ~25–30 % of the
deferred-queue candidates (b0361: 2/8; b0362: 0/8; b0363: 0/8;
b0364: 2/8 — combined yield 4/32 ≈ 12.5 %). Both rescues this tick
were on cases with a "petition is dismissed" closing line in the
PDF tail (Petrushika; Hampwaya v UNZA Council). The six deferrals
this batch are almost all ratio-style summary heads ("Notice of
motion dismissed because…", "A judicial officer who declines
retirement at 55 may only retire upon attaining 65…", "Petition
challenging tourism concession allocations dismissed as statutory
…") that do not match SUMMARY_PATTERNS, paired with PDF tails that
likewise lack a "we therefore dismiss" or "petition is dismissed"
disposition phrasing recognised by the parser. Recommendation
unchanged from b0363: a parser_v0.3.2 vocabulary-widening bump is
the next high-leverage move (subject to Peter's approval).

## Next tick

Two viable paths (unchanged from b0363):

1. **Continue reparse-first sweep** (mechanical, low-yield expected):
   target zmcc/2024/{03,02,01} + zmcc/2023/{n…} — the next eight
   raw-on-disk candidates with no record. Zero fetch cost. Likely
   yield is again low for the same ratio-style-summary reason, but
   it clears the queue ahead of any future parser-vocabulary
   widening.

2. **Pivot to parser-vocabulary widening** (recommended after one
   more confirmatory reparse tick): a parser_v0.3.2 bump that adds
   (a) "denied | refused | granted in part | declaratory relief
   refused | improperly filed" to SUMMARY_PATTERNS and (b) a
   passive-voice operative-paragraph extractor would likely resolve
   a sizeable fraction of the current deferred backlog. This
   parser bump requires Peter's approval; the recommendation is
   logged here for the next human review.

3. **OCR pass on scanned PDFs**: `zmcc/2021/{15,14}` (b0360) and
   `zmcc/2025/19` (b0362) remain deferred under
   `pdf_extraction_empty_likely_scanned`. A small Tesseract-driven
   OCR pass would unblock these specifically.

`phase_5_judgments` remains approved + incomplete; worker does not
flip approval flags. Next tick continues the reparse-first sweep.
