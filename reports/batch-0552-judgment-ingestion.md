# Batch 0552 — judgment-ingestion-worker tick

- **Worker**: judgment-ingestion-worker (scheduled task `judgment-ingestion`)
- **Wall-clock window**: 2026-05-09T09:51Z..10:0xZ (UTC, well under 20 min target)
- **Phase**: Phase 5 dedicated post-completion ingestion (continued).
- **Parser**: v0.3.2 baseline (`scripts/batch_0498_parse.py` +
  `scripts/batch_0506_zmsc_parse.py` wrapper). No parser, fetcher, or
  core-logic modifications. Only configuration-tier reuse via
  `scripts/batch_0552_zmsc_parse.py` thin wrapper pointing at
  `_work/b0552/targets.json`.
- **Outcome**: **0 records written, 8 records reparsed (all redeferred
  under `html_no_summary_pdf_no_match`)**. Zero fetches consumed.


## Renumbering note

This tick was originally numbered batch 0551 but was renumbered to
0552 mid-tick after `git pull --ff-only` revealed the main
corpus-builder worker had already used batch number 0551 for its
own Phase 8 nightly reverify tick at 2026-05-09T07:55:44Z (entry
already in the unstaged costs.log / provenance.log diff). Same
renumbering pattern as b0548 (which was renumbered from 0547 due
to a collision with judgment-ingestion-worker batch-0547 in the
opposite direction). All artefacts produced by this tick
(`_work/b0552/`, `scripts/batch_0552_zmsc_parse.py`,
`reports/batch-0552-judgment-ingestion.md`, costs.log /
provenance.log / worker.log entries) are tagged b0552.

## Tick decision (priority order)

a. **REPARSE DEFERRED** — chosen for this tick. Selected 8 unsampled
   v0.3.3-pending candidates (distinct from b0541 and b0544 samples)
   with PDF sizes 290 KB to 519 KB — large enough to skip the
   tiny-stub bias of b0544 (97-286 KB) while small enough to be
   confidently text-extractable. Spread across 5 court/year cohorts
   to broaden pattern coverage.
   **Result**: all 8 PDFs extract text normally (none deferred under
   `pdf_extraction_empty_likely_scanned`); none of the HTML summaries
   or PDF tail anchors matched any v0.3.2 operative-verb pattern.
   All 8 redeferred under `html_no_summary_pdf_no_match` — they
   remain in the v0.3.3-pending cohort.

b. **SCZ SWEEP** — not run this tick (priority (a) had work).
c. **ZMCC NEW YEARS** — not run this tick.

## Phase 0 — target selection (zero fetch cost)

Walked `raw/zambialii/judgments/` and cross-referenced
`records/judgments/` to enumerate **164 raw-on-disk records with no
written record** (the union of the v0.3.3-pending and OCR-pending
cohorts plus any historic deferrals). Excluded the 16 already-sampled
records from b0541 (zmsc/2020/{2,3,4,6,7,8,9,11}) and b0544
(zmsc/2022/{61,54,46,2}, zmcc/2023/27, zmsc/2024/{22,18}, zmsc/2026/2),
filtered to PDF size 100 KB–700 KB (text-extractable but not stub),
and selected 8 records spread across courts/years (max 2 per
court/year):

| court / num   | PDF size  | summary head (first 140 chars)                                                                              |
|---------------|----------:|--------------------------------------------------------------------------------------------------------------|
| zmcc/2026/01  |  290.7 KB | A challenge to the JCC's report and removals must proceed by judicial review in the High Court, not by original petition here. |
| zmcc/2022/27  |  347.8 KB | Court dismisses functus officio objection and allows constitutional challenge to section 30 (costs) to proceed to hearing. |
| zmsc/2025/05  |  357.0 KB | Whether the corporate veil can be lifted by joinder after judgment and the appropriate procedure and proof required. |
| zmsc/2026/03  |  373.0 KB | Applicants granted leave to appeal where proposed grounds raised legal issues, mixed questions, and procedural concerns warranting Supreme C... |
| zmcc/2023/05  |  462.2 KB | Article 52(6) does not permit independent candidates to withdraw after nominations; ECZ cancels only for party candidate resignation, death... |
| zmcc/2024/02  |  496.4 KB | An individual directly affected by interpretation of Article 74(2) may be joined as an interested party to adjudicate rights and issues. |
| zmcc/2022/30  |  502.1 KB | Joinder refused where applicant failed to show the proposed party had sufficient interest or nexus to the constitutional petition. |
| zmsc/2022/01  |  519.2 KB | A delivered judgment is enforceable immediately; embodiment under Rule 75 is not a prerequisite to taxing costs. |

## Phase 1 — reparse via parser_v0.3.2

Invoked `scripts/batch_0552_zmsc_parse.py` against
`_work/b0552/targets.json`. All 8 candidates extracted PDF text
successfully (>200 chars, not scanned). The HTML summary contained a
flynote-style legal issue in each case rather than an explicit
operative-verb anchor, and the PDF tail similarly contained no
v0.3.2-recognised disposition pattern. Result:

| court / num   | result   | reason                            |
|---------------|----------|-----------------------------------|
| zmcc/2026/01  | deferred | html_no_summary_pdf_no_match      |
| zmcc/2022/27  | deferred | html_no_summary_pdf_no_match      |
| zmsc/2025/05  | deferred | html_no_summary_pdf_no_match      |
| zmsc/2026/03  | deferred | html_no_summary_pdf_no_match      |
| zmcc/2023/05  | deferred | html_no_summary_pdf_no_match      |
| zmcc/2024/02  | deferred | html_no_summary_pdf_no_match      |
| zmcc/2022/30  | deferred | html_no_summary_pdf_no_match      |
| zmsc/2022/01  | deferred | html_no_summary_pdf_no_match      |

### New near-miss families confirmed (additive to b0541 + b0544)

The b0544 reparse identified six v0.3.3-pending pattern families;
b0541 added three. b0552 confirms the same families recur in a
distinct sample and adds two more candidates:

7. **"Court dismisses ... and allows ..." compound disposition**
   (zmcc/2022/27): summary contains both an explicit dismissal and
   an explicit allowance, but in narrative third-person-singular
   present tense (`dismisses` / `allows`). v0.3.2 anchors are first-
   person-plural (`we dismiss/allow`) or passive (`is dismissed/
   allowed`). Pattern needs broadening to active-third-person form.
8. **"granted leave to appeal" / "Joinder refused" — non-list nouns**
   (zmsc/2026/03, zmcc/2022/30): "leave to appeal" is in the closed
   noun list but the surface form here is `applicants granted leave
   to appeal` (subject-verb-object, not `<noun> (is) granted`).
   "Joinder refused" likewise inverts the object/verb order.
   Pattern needs broadening to allow subject-verb-object active
   form for grant/refuse.
9. **Pure declaratory holdings — no operative disposition verb**
   (zmcc/2026/01, zmcc/2024/02, zmcc/2023/05, zmsc/2025/05,
   zmsc/2022/01): summaries are abstract legal propositions
   ("must proceed by judicial review", "may be joined as interested
   party", "does not permit independent candidates to withdraw",
   "veil can be lifted by joinder", "delivered judgment is
   enforceable immediately"). No operative verb maps to the corpus
   outcome enum. Likely require **issue-paper / declaratory-relief
   subtype** outside the current outcome vocabulary, or a
   `declaratory_holding` outcome enum addition + flynote-derived
   `outcome_detail`.

These additions bring the total v0.3.3 anchor-addition queue to
**≥ 11 distinct family additions**, of which families 7 and 8
should unlock 5+ records on inspection of the broader cohort and
family 9 affects ~15+ ZMCC declaratory rulings.

These 11 near-miss families are all candidates for v0.3.3 expansion
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

Trivially **PASS** — the corpus state is unchanged from b0550.

- 159 unique judgment IDs, no duplicates.
- All judges in all records resolve in `judges_registry.yaml`.
- All `raw_sha256` values match on-disk PDFs (unchanged).

## B2 sync

B2 sync deferred to host (`rclone` not in sandbox; same as every prior
batch since b0517).

## Cohort cumulative tracking (since b0504)

| metric                                 | b0550 | b0552 (this tick) |
|----------------------------------------|------:|-------------------:|
| written                                |    62 |                 62 |
| v0.3.3-pending deferred                |    51 |                 51 |
| OCR-pending deferred                   |    37 |                 37 |
| confirmed 404                          |    40 |                 40 |

**Net change**: zero. The 8 reparsed records were already counted in
the 51-record v0.3.3-pending total (originally deferred in earlier
batches under `html_no_summary_pdf_no_match`); redeferral does not
change the count.

## Daily fetch budget

| component                           | fetches |
|-------------------------------------|--------:|
| pre-tick                            |      86 |
| this tick: reparse (zero fetch)     |       0 |
| **post-tick total**                 |  **86** |
| budget                              |     500 |

414 fetches remain in today's judgment-ingestion budget.

## Next-tick recommendation

The current parser-modification freeze imposed on scheduled ticks
means the v0.3.3-pending cohort (51 records, confirmed via b0541 +
b0544 + b0552 to span at least 11 distinct near-miss pattern
families across 24 sampled records) cannot be unlocked by reparse
alone. Productive paths remain:

1. **Author parser v0.3.3 patches outside the scheduled tick**
   (highest leverage) — the 11 near-miss families enumerated across
   b0541/b0544/b0552 plus the procedural-refusal/grant-form/
   declaratory-holding additions could unlock 30-40+ of the 51
   v0.3.3-pending records in a single dedicated parser tick.
2. **ZMSC 2023 internal-gap probe** (HEAD-only) — only 9 records on
   disk for ZMSC 2023; sweep nums {10, 11, 12, 13, 14, 15, 16, 17}
   to map upper boundary. ~8 fetches, informational. Same pattern
   as b0547/b0550 boundary probes.
3. **ZMSC 2022 upper-boundary continuation** — 18 records; b0522
   left that year's upper boundary unresolved. ~8 HEAD fetches.
4. **OCR backfill workflow for the 37 OCR-pending records**
   (~269 MB) — outside scheduled tick; requires Tesseract or
   equivalent in the host environment.

The Phase 5 ceiling at 159/160 means even if v0.3.3 is authored
and 30+ records become unlockable, only **1** can be written
without an `approvals.yaml` lift by Peter (current ceiling
160 unchanged since 2026-05-03 completion).

## Sandbox-lock observation

Pre-tick stale `.git/ORIG_HEAD.lock` could not be unlinked (FUSE
"Operation not permitted") but did not block `git pull --ff-only`
(already up to date). No `.git/index.lock` or
`.git/objects/maintenance.lock` present this tick.
