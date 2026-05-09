# Batch 0544 — judgment-ingestion-worker tick

- **Worker**: judgment-ingestion-worker (scheduled task `judgment-ingestion`)
- **Wall-clock window**: 2026-05-09T00:0xZ..00:1xZ (UTC, well under 20 min target)
- **Phase**: Phase 5 dedicated post-completion ingestion (continued).
- **Parser**: v0.3.2 baseline (`scripts/batch_0498_parse.py` +
  `scripts/batch_0506_zmsc_parse.py` wrapper). No parser, fetcher, or
  core-logic modifications. Only configuration-tier reuse via inline
  invocation pointing at `_work/b0544/targets.json`.
- **Outcome**: **0 records written, 8 records reparsed (all redeferred
  under `html_no_summary_pdf_no_match`)**. Zero fetches consumed.

## Tick decision (priority order)

a. **REPARSE DEFERRED** — chosen for this tick. Selected the 8 smallest
   on-disk-deferred PDFs (97 KB to 286 KB) from the `raw/zambialii/judgments/`
   tree to maximise the chance of text-extractable PDFs hitting the
   v0.3.2 outcome-anchor patterns. **Result**: all 8 PDFs extract text
   normally (none deferred under `pdf_extraction_empty_likely_scanned`),
   but none of the HTML summaries or PDF tail anchors matched any
   v0.3.2 operative-verb pattern. All 8 redeferred under
   `html_no_summary_pdf_no_match` — i.e., they remain in the
   v0.3.3-pending cohort.

b. **SCZ SWEEP** — not run this tick.
c. **ZMCC NEW YEARS** — not run this tick.

## Phase 0 — target selection (zero fetch cost)

Walked `raw/zambialii/judgments/` and cross-referenced
`records/judgments/` to enumerate **163 raw-on-disk records with no
written record** (the union of the v0.3.3-pending and OCR-pending
cohorts plus any historic deferrals). Sorted by PDF size and selected
the 8 smallest:

| court / num   | PDF size  | summary head (first 120 chars)                                                                          |
|---------------|----------:|----------------------------------------------------------------------------------------------------------|
| zmsc/2022/61  |   97.0 KB | Court refused a late amendment to a motion (styled as an appeal) because allowing it would prejudice... |
| zmsc/2022/54  |  112.8 KB | Eyewitness identification corroborated by possession of stolen property sustained appellant's convict...|
| zmcc/2023/27  |  177.8 KB | An originating-summons challenge to seizures involving a former President was dismissed as personalis...|
| zmsc/2024/22  |  183.6 KB | Evidence of telephone confirmations and corroborating call-back stamps upheld a court-martial convict...|
| zmsc/2026/2   |  184.4 KB | Applicants failed to show a point of public importance or reasonable prospects of success to obtain l...|
| zmsc/2024/18  |  184.8 KB | The State successfully appealed: extenuation lacked evidential basis and the six-year sentence was qu...|
| zmsc/2022/46  |  239.1 KB | Chief's alleged withdrawal or consent could not validly extinguish another's customary interest with...|
| zmsc/2022/2   |  285.9 KB | Respondents granted 14-day extension where lack of notice excused delay; full-bench leave-to-appeal...|

## Phase 1 — reparse via parser_v0.3.2

Invoked `scripts/batch_0506_zmsc_parse.py` against
`_work/b0544/targets.json`. All 8 candidates extracted PDF text
successfully (>200 chars, not scanned). The HTML summary contained a
flynote-style legal issue in each case rather than an explicit
operative-verb anchor, and the PDF tail similarly contained no
v0.3.2-recognised disposition pattern. Result:

| court / num   | result   | reason                            |
|---------------|----------|-----------------------------------|
| zmsc/2022/61  | deferred | html_no_summary_pdf_no_match      |
| zmsc/2022/54  | deferred | html_no_summary_pdf_no_match      |
| zmcc/2023/27  | deferred | html_no_summary_pdf_no_match      |
| zmsc/2024/22  | deferred | html_no_summary_pdf_no_match      |
| zmsc/2026/2   | deferred | html_no_summary_pdf_no_match      |
| zmsc/2024/18  | deferred | html_no_summary_pdf_no_match      |
| zmsc/2022/46  | deferred | html_no_summary_pdf_no_match      |
| zmsc/2022/2   | deferred | html_no_summary_pdf_no_match      |

### Confirmation of v0.3.3 patterns gap

Reading the summary heads alongside the parser_v0.3.2 anchor list
(`scripts/batch_0498_parse.py`), the failures group cleanly into three
v0.3.3-pending pattern families already enumerated in b0541:

- **"Court refused" + non-stay object** (zmsc/2022/61): v0.3.2 only
  matches `court refused (a) (the) stay`. The flynote describes the
  court refusing a *late amendment*. Pattern needs broadening to
  `court refused (the|to) (grant|allow|permit) <object>`.
- **"upheld <conviction|sentence|judgment>" past tense / passive
  variants** (zmsc/2022/54, zmsc/2024/22): summary head reads
  "...sustained appellant's conviction" and "...upheld a court-martial
  conviction". v0.3.2 requires `<noun> is/was upheld` with a
  bounded adverb cluster; "sustained" is not in the verb list and
  the upheld-with-direct-object form is not anchored.
- **"failed to show / failed to establish" → dismissed inference**
  (zmsc/2026/2, zmcc/2023/27): the operative finding is that the
  applicant failed a threshold test; v0.3.2 requires the explicit
  "appeal/application is dismissed" form rather than the inference.
- **"successfully appealed"** (zmsc/2024/18, with explicit
  "sentence was quashed" further down the summary): v0.3.2's
  set-aside/quashed anchors are TAIL-ONLY (per the b0498 false-positive
  guard) and only the active "we set aside" form is allowed at the
  summary stage. The passive "was quashed" in the summary is therefore
  not picked up.
- **"granted 14-day extension"** (zmsc/2022/2): the application was
  granted; v0.3.2 anchor `<noun> (is) granted` requires the noun to be
  one of {application, petition, appeal, leave, relief}. "Extension"
  is not in the list.
- **"dismissed as personalised, contentious"** (zmcc/2023/27):
  v0.3.2's `dismissed for (lack|failing|want|failure)` anchor matches
  on a closed adjunct list; "dismissed as personalised" falls outside.

These six near-miss patterns are all candidates for v0.3.3 expansion
but cannot be authored in this scheduled tick under the existing
`Your ONLY job is ingesting judgments. You do NOT run any other phase`
constraint that limits parser-baseline modifications to dedicated
parser ticks.

## Phase 2 — corpus.sqlite update

**Skipped — zero records written.** corpus.sqlite unchanged.
records: 1849 (no change). judgments_meta: 159 (no change).

Phase 5 ceiling **159/160** unchanged. **One record under ceiling.**

## Phase 3 — judges_registry update

**Skipped — zero records written.** judges_registry.yaml unchanged.

## Phase 4 — integrity checks

Trivially **PASS** — the corpus state is unchanged from b0543.

- 159 unique judgment IDs, no duplicates.
- All judges in all records resolve in `judges_registry.yaml`.
- All `raw_sha256` values match on-disk PDFs (unchanged).

## B2 sync

B2 sync deferred to host (`rclone` not in sandbox; same as every prior
batch since b0517).

## Cohort cumulative tracking (since b0504)

| metric                                 | b0543 | b0544 (this tick) |
|----------------------------------------|------:|-------------------:|
| written                                |    62 |                 62 |
| v0.3.3-pending deferred                |    51 |                 51 |
| OCR-pending deferred                   |    37 |                 37 |
| confirmed 404                          |    27 |                 27 |

**Net change**: zero. The 8 reparsed records remain in the
v0.3.3-pending cohort. They were already counted in the 51-record
total (since they were originally deferred under
`html_no_summary_pdf_no_match` in earlier batches).

## Daily fetch budget

| component                           | fetches |
|-------------------------------------|--------:|
| pre-tick                            |      70 |
| this tick: reparse (zero fetch)     |       0 |
| **post-tick total**                 |  **70** |
| budget                              |     500 |

430 fetches remain in today's judgment-ingestion budget.

## Next-tick recommendation

The current parser-modification freeze imposed on scheduled ticks
means the v0.3.3-pending cohort (51 records, now confirmed via b0544
to span at least 6 distinct near-miss pattern families) cannot be
unlocked by reparse alone. Two productive paths remain:

1. **Continue ZMSC 2020 upper-boundary discovery** (HEAD-only probes
   at {95, 100, 105, 110, 115, 120, 130, 150}) — 8 fetches, probably
   mostly 404s near 150, helps localise true ceiling. Adds zero
   records (informational).
2. **Continue ZMSC 2020 internal-gap GET sweep at nums 81-89**
   (8 fetches) — at b0543's 4-of-7 yield, would write ~3-4 records.
   Phase 5 ceiling is at 160; this would push to 162-163 — **the
   ceiling needs to be lifted or the tick needs to write only 1
   record**.
3. **Author parser v0.3.3 patches outside the scheduled tick**: the
   six near-miss families enumerated above plus the three from b0541
   (succeeds/fails, remitted, jurisdictional set-aside) — combined
   target ≥ 9 distinct anchor additions that could unlock ~30+ of
   the 51-record v0.3.3-pending cohort in a single dedicated parser
   tick.

The OCR-pending cohort (37 records, ~269 MB) likewise awaits an OCR
backfill workflow authored outside the scheduled tick.
