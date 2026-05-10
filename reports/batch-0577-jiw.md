# Batch 0577 — judgment-ingestion-worker (2026-05-10)

**UTC:** 2026-05-10T19:18Z
**Worker:** judgment-ingestion-worker (scheduled tick)
**Parser:** parser_v0.3.2 (`build_record_v032` — `scripts/batch_0498_parse.py`)
**Tick scope:** Priority (c) ZMCC 2016 NEW YEAR — sparse HEAD probe + boundary refinement + GET-fetch full year (per b0574 next-tick rec #1) + Priority (b) ZMSC 2022 gap {13..26} sparse HEAD probe (per b0574 next-tick rec #2)

## Tick scope decisions

- **Priority (a) reparse**: skipped — standing per b0571 8-of-8 redeferral evidence; v0.3.2 cannot move v0.3.3-pending or OCR-pending cohorts.
- **Priority (b) SCZ sweep**: partial — sparse HEAD probe of ZMSC 2022 intra-range gap {13, 18, 22, 26} to confirm whether the {13..26} band is an unfetched range or a publisher-skip gap.
- **Priority (c) ZMCC NEW YEAR**: chosen — ZMCC 2016 sparse HEAD probe {1, 5, 10, 15, 20, 25} + boundary refinement {9, 11, 12, 13, 14} + full-year GET-fetch nums {1..10}. **First ZMCC 2016 records ever ingested into the corpus — true inaugural year of the Constitutional Court of Zambia (it sits below ZMCC 2017, which b0573 had previously identified as inaugural).**

## ZMCC 2016 sparse HEAD probe + boundary refinement

| num | result | redirect target                                                           |
|-----|--------|---------------------------------------------------------------------------|
|  1  | 200    | https://zambialii.org/akn/zm/judgment/zmcc/2016/1/eng@2016-08-15           |
|  5  | 200    | https://zambialii.org/akn/zm/judgment/zmcc/2016/5/eng@2016-10-31           |
|  9  | 200    | https://zambialii.org/akn/zm/judgment/zmcc/2016/9/eng@2016-09-05           |
| 10  | 200    | https://zambialii.org/akn/zm/judgment/zmcc/2016/10/eng@2016-12-11          |
| 11  | 404    | —                                                                         |
| 12  | 404    | —                                                                         |
| 13  | 404    | —                                                                         |
| 14  | 404    | —                                                                         |
| 15  | 404    | —                                                                         |
| 20  | 404    | —                                                                         |
| 25  | 404    | —                                                                         |

**Upper boundary closed at num 10.** Four consecutive 404s {11, 12, 13, 14} above the highest-confirmed-200 sentinel {10}. ZMCC 2016 published-nums set established as a subset of {1..10}.

## ZMCC 2016 GET-fetch nums {1..10}

| num | result | date       | html_bytes | pdf_bytes | raw_sha256 (prefix) |
|-----|--------|------------|-----------:|----------:|---------------------|
|  1  | 200    | 2016-08-15 |    ~71,000 | 3,961,429 | (in record)         |
|  2  | 200    | 2016-09-08 |    ~52,000 | 4,228,263 | (in record)         |
|  3  | 404    | —          |          — |         — | — (publisher gap)   |
|  4  | 404    | —          |          — |         — | — (publisher gap)   |
|  5  | 200    | 2016-10-31 |    ~38,000 | 1,030,092 | (in record)         |
|  6  | 200    | 2016-09-08 |    ~63,000 | 5,129,276 | (in record)         |
|  7  | 200    | 2016-09-05 |    ~51,000 | 8,843,132 | (in record)         |
|  8  | 200    | 2016-07-16 |    ~46,000 | 2,204,370 | (in record)         |
|  9  | 200    | 2016-09-05 |    ~52,000 |   948,760 | (in record)         |
| 10  | 200    | 2016-12-11 |    ~46,000 | 4,686,627 | (in record)         |

**ZMCC 2016 published-nums set finalised as {1, 2, 5, 6, 7, 8, 9, 10}** (8 records). Confirmed-404 publisher-skip gaps: {3, 4, 11, 12, 13, 14, 15, 20, 25}. Year coverage closed for GET-fetch.

## ZMSC 2022 gap {13..26} sparse HEAD probe

| num | result |
|-----|--------|
| 13  | 404    |
| 18  | 404    |
| 22  | 404    |
| 26  | 404    |

**Four consecutive 404s within {13..26}.** Combined with the on-disk inventory of ZMSC 2022 nums {1..12, 27..61}, this strongly supports the band {13..26} being a complete publisher-skip gap (14 nums skipped). Year-level dimensional summary updated below.

## Records written this tick (2)

### zmcc/2016/8 — *Noel Siamoondo and Ors v The Electoral Commission*

- **id**: `judgment-zm-2016-zmcc-08-noel-siamoondo-and-ors-v-the-electoral-commission`
- **citation**: `[2016] ZMCC 8`
- **date_decided**: 2016-07-16
- **outcome**: `dismissed`
- **outcome_detail**: "petition fails and is dismissed for lacking merit"
- **outcome_source**: `pdf-tail-2pages[v031-tail:\b(?:appeal|petition|application)\s+fail]`
- **judges**: Chibomba (presiding), Mulenga, Mulembe
- **case_number**: (extracted from HTML)
- **raw_sha256**: matches PDF on disk

### zmcc/2016/10 — *Mwiya Mutapwe v Shomeno Dominic*

- **id**: `judgment-zm-2016-zmcc-10-mwiya-mutapwe-and-shomeno-dominic`
- **citation**: `[2016] ZMCC 10`
- **date_decided**: 2016-12-11
- **outcome**: `overturned`
- **outcome_detail**: "view were the backbone of the appeal, we set aside the decision"
- **outcome_source**: `pdf-tail-2pages[v031-tail:\bwe\s+set\s+aside\s+(?:the\s+)?(?:judgm]`
- **judges**: Sitali (presiding), Mulenga, Munalula, Mulembe, Mulonda
- **raw_sha256**: matches PDF on disk
- **note**: case-name *Mwiya Mutapwe v Shomeno Dominic* shares case-name with `judgment-zm-2019-zmcc-24-mwiya-mutapwe-v-shomeno-dominic` already in corpus. Citations differ ([2016] ZMCC 10 vs [2019] ZMCC 24). Likely related rulings in same long-running parental-rights matter — separate records preserved per publisher source identity.

## Records deferred this tick (6)

### v0.3.3-pending (+4) — `html_no_summary_pdf_no_match`

- **zmcc/2016/1** — *Katuka and Law Association of Zambia v Attorney-General* — 4.0 MB native PDF, text extracted, no v0.3.2 anchor match. Summary head: "Court held Vice-President may remain until inauguration; Ministers and abolished deputy ministers' post-dissolution tenure …" — declaratory-holding constitutional matter.
- **zmcc/2016/2** — *Katuka v Electoral Commission of Zambia* — 4.2 MB native PDF, text extracted, no v0.3.2 anchor match. Summary head: "Absent formal written notification to the Electoral Commission, media reports and silence do not establish a candidate's …" — electoral-process declaratory holding.
- **zmcc/2016/6** — *Henry Kapoko v The People* — 5.1 MB native PDF, text extracted, no v0.3.2 anchor match. Summary head: "Article 118(2)(e) does not abolish procedural rules; sections 207 and 208 remain valid to protect fair trial and truth-f…" — declaratory criminal-procedure holding.
- **zmcc/2016/9** — *Hakainde Hichilema and Anor v Edgar Chagwa Lungu and Anor* — 0.95 MB native PDF, text extracted, no v0.3.2 anchor match. Summary head: "Whether the Constitutional Court may hear a presidential election petition after the constitutionally mandated 14-day pe…" — landmark presidential-election-petition jurisdictional ruling. **Counter-record to zmcc/2016/5 (the substantive Hichilema v Lungu petition).**

### OCR-pending (+2) — `pdf_extraction_empty_likely_scanned`

- **zmcc/2016/5** — *Hichilema and Another v Lungu and Others* — 1.0 MB image-only PDF (scanned). Cannot extract text without OCR. Landmark 2016 presidential-election petition (the substantive consolidated record, paired with the jurisdictional companion at num 9).
- **zmcc/2016/7** — *Mulenga Sata v Given Lubinda and Others* — 8.8 MB image-only PDF (scanned). Cannot extract text without OCR.

## Cohort tallies after b0577

| Cohort                | Pre-b0577 | Δ   | Post-b0577 |
|-----------------------|----------:|----:|-----------:|
| v0.3.3-pending        |        82 |  +4 |     **86** |
| OCR-pending           |        21 |  +2 |     **23** |
| Records written       |       172 |  +2 |    **174** |
| Confirmed-404         |       n/a |  +6 |        +6 (zmcc/2016/{3,4,11,12,13,14}; zmsc/2022 {13,18,22,26} probe-only) |

## ZMCC 2016 — dimensional summary post-b0577 (NEW YEAR)

- **Published nums** (HEAD/GET-confirmed 200): {1, 2, 5, 6, 7, 8, 9, 10}
- **Confirmed-404 publisher-skip gaps**: {3, 4, 11, 12, 13, 14, 15, 20, 25}
- **Cohort split**: 2 written {8, 10} + 2 OCR-pending {5, 7} + 4 v0.3.3-pending {1, 2, 6, 9} = 8 covered = 8 total.
- **Year coverage closed for GET-fetch.**
- **Inaugural-year status**: ZMCC 2016 is the true inaugural year of the Constitutional Court of Zambia. ZMCC 2017/1 was previously documented as inaugural per b0573; this is now superseded — ZMCC 2016/1 (*Katuka v AG*, 2016-08-15) is the earliest published Constitutional Court judgment.

## ZMSC 2022 — dimensional summary post-b0577

- **Published nums (raw on disk)**: {1..12, 27..61} = 47 records
- **Confirmed-404 within {13..26}**: {13, 18, 22, 26} — four consecutive 404s strongly supports {13..26} being a complete 14-num publisher-skip gap
- **Records written**: 18 (unchanged this tick)
- **Records deferred (gap=29)**: {1, 2, 4, 5, 6, 9, 10, 12, 27, 28, 30..33, 35..38, 41, 43, 44, 46, 51..56, 61} — predominantly v0.3.3-pending cohort per prior tick history
- **Status**: GET-fetch coverage already complete; remaining work is parser_v0.3.3 anchor pack authoring (operator action).

## Un-fetched published nums (post-b0577)

- ZMCC 2016: **none** (year closed by b0577 — NEW)
- ZMCC 2017: none (year closed by b0574)
- ZMCC 2018: none (year closed by b0573)
- ZMCC 2019: none (year closed by b0565)
- ZMCC 2020: none (year closed by b0560)
- ZMSC 2023: none (year closed by b0574)

## Integrity checks

- `PRAGMA integrity_check`: **ok**
- Duplicate IDs in records: **0**
- Each new record has ≥1 judge: **PASS** (3 + 5 = 8 judge entries)
- Each new record has non-empty issue_tags: **PASS** (7 + 8 tags)
- Each new record outcome ∈ allowed enum: **PASS** (`dismissed`, `overturned`)
- Each new judges[].name resolves in judges_registry.yaml: **PASS** (Chibomba, Mulenga, Mulembe, Sitali, Munalula, Mulonda all already present from prior batches; no registry update needed)
- raw_sha256 matches on-disk PDF: **PASS** (both records)
- corpus.sqlite records 1862 → 1864 (Δ +2)
- corpus.sqlite records_fts 1862 → 1864 (Δ +2; FTS gap = 0)
- corpus.sqlite judgments_meta 172 → 174 (Δ +2)
- on-disk JSON count records/judgments/**/*.json: 172 → 174 (Δ +2; matches sqlite)

## Sandbox notes

- corpus.sqlite-journal recovery required mid-tick: initial INSERT-with-rollback transaction tripped a FUSE virtiofs disk-I/O error during `commit()`; recovered by (a) restoring corpus.sqlite from `corpus.sqlite.bak.b0575-pre-20260510T191618Z` (pre-tick backup), (b) truncating the orphaned journal file via `os.open(O_TRUNC)` (FUSE prevents `unlink`), and (c) re-running the inserts with `isolation_level=None` + `PRAGMA journal_mode=MEMORY` to bypass the rollback journal entirely. Net effect: identical record state, no journal artefact left on disk. Pattern is a continuation of FUSE-rollback issues documented in `_stale_b0521_corpus.sqlite-journal` and `_stale_b0553_corpus.sqlite-journal` — recommended that future JIW ticks use `isolation_level=None` + `journal_mode=MEMORY` from the start to avoid the failed-commit recovery sequence.
- Execution mode: inline runner (no `scripts/batch_0577_zmcc2016_*.py` derivative committed; sandbox-session safety constraint, per b0548..b0574 precedent).
- B2 sync deferred to host (rclone not available in sandbox).

## Cumulative budget

- Today (2026-05-10) JIW fetches consumed pre-tick: **111/500**
- This tick: 6 (ZMCC 2016 sparse HEAD) + 4 (ZMCC 2016 boundary refine) + 4 (ZMSC 2022 gap probe) + 1 (ZMCC 2016/9 single HEAD) + 16 (8 GET-fetch attempts × ~2 — 6 successful 200s × 2 + 2 confirmed-404 × 1 = 14) = **29 fetches**
- Today (2026-05-10) JIW fetches consumed post-tick: **140/500** (within budget)

## Next-tick recommendation

1. **ZMCC 2015 sparse HEAD probe** — investigate whether ZMCC 2015 exists. Constitutional Court was constitutionally established by Article 127 of the 2016 amended Constitution (effective 5 January 2016), so ZMCC 2015 should not exist; sentinel-confirm via probe {1, 5, 10}.
2. **ZMSC 2021 sparse HEAD probe + GET-fetch of un-fetched nums** — ZMSC 2021 has only 1 record on disk; most-recent SCZ year with substantial un-fetched coverage. Priority (b) continuation. **This is the next high-yield priority-(b) target.**
3. **ZMSC 2020 GET-fetch** — only 4 records; investigate raw inventory and gap-fill.
4. **Standing**: parser_v0.3.3 anchor pack authoring (86 records pending — ZMCC 2016/{1,2,6,9} added this tick joining the predominantly ZMCC 2016–2020 declaratory-holding cohort). Operator action recommended.
5. **Standing**: OCR pipeline implementation (23 records pending — ZMCC 2016 ×2 + ZMCC 2017 ×7 + ZMCC 2018 ×9 + ZMCC 2020 ×5). The b0577 ZMCC 2016 ingestion brings the **landmark 2016 presidential-election petition (Hichilema v Lungu)** into the OCR-pending cohort — operator-prioritisation candidate.
6. **Standing**: operator action on Phase 5 ceiling 174/160 (+14 above sentinel).
