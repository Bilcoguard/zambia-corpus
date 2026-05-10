# Batch 0568 — judgment-ingestion-worker (2026-05-10)

**UTC:** 2026-05-10T10:14:00Z
**Worker:** judgment-ingestion-worker (scheduled tick)
**Parser:** parser_v0.3.2 (build_record_v032)
**Tick scope:** Priority (c) — ZMCC 2018 close upper boundary + GET-fetch high-num cluster

## Tick scope

- Priority (a) reparse: skipped (v0.3.2 cannot move v0.3.3-pending cohort; standing per b0552/b0557/b0558/b0559/b0560/b0561/b0564/b0565/b0566)
- Priority (b) SCZ sweep: skipped (ZMSC 2024-2025-2026 confirmed exhausted by b0547/b0550/b0558)
- Priority (c) chosen: ZMCC 2018 close upper boundary HEAD-probe + GET-fetch high-num cluster per b0566 next-tick recommendation #1

## HEAD-probe ZMCC 2018 upper boundary {16, 17, 18, 19}

| num | result | redirect target |
|-----|--------|----------------|
| 16  | 200    | eng@2018-06-20 |
| 17  | 200    | eng@2018-06-22 |
| 18  | 404    | — |
| 19  | 404    | — |

**Boundary closed.** ZMCC 2018 published nums confirmed via HEAD: {1, 5, 10, 15, 16, 17}. Two consecutive 404s at {18, 19} plus prior b0566 404s at {20, 25} = strong sentinel. **Upper boundary at num 17.**

## GET-fetch results ZMCC 2018 nums {9..16}

All 8 nums returned 200 OK on both HTML and PDF. Date sequence (monotonic ascending, ZMCC chronological):

| num | date         | filename slug                                        | pdf_bytes |
|-----|--------------|------------------------------------------------------|-----------|
| 9   | (extracted)  | imbuwa-v-mundia                                      | 7,896,936 |
| 10  | (extracted)  | pule-and-others-v-attorney-general-and-others        |   379,714 |
| 11  | (extracted)  | chisanga-v-chisopa-and-others                        | 8,030,551 |
| 12  | (extracted)  | zambia-national-commercial-bank-plc-v-musonda-and    | 4,223,477 |
| 13  | (extracted)  | zambia-national-commercial-bank-plc-v-musonda-and    | 4,223,477 |
| 14  | (extracted)  | zambia-national-commercial-bank-plc-v-musonda-and    | 4,223,477 |
| 15  | (extracted)  | subulwa-v-mandandi                                   | 7,987,732 |
| 16  | (extracted)  | shabula-v-monde                                      | 7,423,147 |

**Note:** zmcc/2018/{12,13,14} share an identical 4,223,477-byte PDF ("zambia-national-commercial-bank-plc-v-musonda-and..."). This appears to be a publisher-level anomaly where the same judgment was assigned three consecutive zmcc citation numbers. Raw bytes preserved as-fetched per corpus principle of source-fidelity; deduplication is an out-of-tick downstream concern.

## Records written this tick (0)

None. All 8 nums deferred — see below.

## Records deferred this tick (8)

### OCR-pending cohort (+2)

Reason `pdf_extraction_empty_likely_scanned` — PDF text-layer extraction returned <200 chars; likely scanned images without OCR.

| num | citation       | filename slug                                        |
|-----|----------------|------------------------------------------------------|
| 9   | [2018] ZMCC 9  | imbuwa-v-mundia                                      |
| 11  | [2018] ZMCC 11 | chisanga-v-chisopa-and-others                        |

### v0.3.3-pending cohort (+6)

Reason `html_no_summary_pdf_no_match` — HTML lacks operative-verb summary anchor; PDF has extracted text but no v0.3.2 SUMMARY/TAIL/ORDER-INTRO pattern matches. These are predominantly declaratory holdings or interlocutory rulings whose disposition language is outside the v0.3.2 vocabulary. Joins the standing v0.3.3-pending cohort awaiting parser_v0.3.3 anchor pack authoring.

| num | citation        | filename slug                                                  |
|-----|-----------------|----------------------------------------------------------------|
| 10  | [2018] ZMCC 10  | pule-and-others-v-attorney-general-and-others                  |
| 12  | [2018] ZMCC 12  | zambia-national-commercial-bank-plc-v-musonda-and              |
| 13  | [2018] ZMCC 13  | zambia-national-commercial-bank-plc-v-musonda-and              |
| 14  | [2018] ZMCC 14  | zambia-national-commercial-bank-plc-v-musonda-and              |
| 15  | [2018] ZMCC 15  | subulwa-v-mandandi                                             |
| 16  | [2018] ZMCC 16  | shabula-v-monde                                                |

## Cohort tallies after b0568

| Cohort                                      | Pre-b0568 | Δ b0568 | Post-b0568 |
|---------------------------------------------|----------:|--------:|-----------:|
| v0.3.3-pending (parser anchor pack needed)  |        74 |      +6 |     **80** |
| OCR-pending (scanned PDFs)                  |        12 |      +2 |     **14** |
| Records written                             |       171 |       0 |    **171** |

## ZMCC 2018 — dimensional summary post-b0568

- HEAD-confirmed-200 nums: {1, 5, 10, 15, 16, 17} — sparse-probe + upper-boundary-close
- GET-fetched (200, raw on disk): {1..16} — all 16 nums (b0566 fetched {1..8}, b0568 fetches {9..16})
- HEAD-404 (sentinel): {18, 19, 20, 25}
- Un-probed: {2..4, 6..9, 11..14, 18, 21..24} — {2..4, 6..9, 11..14} all returned 200 on GET (so confirmed 200), {21..24} not probed but 4 consecutive 404s {18..20, 25} extending b0566 sentinels suggest no further publishing
- **Upper boundary: num 17**, lower boundary: num 1 (18 January 2018)
- Records written (cumulative): 1 of 16 (zmcc/2018/1 from b0566) = 6%
- v0.3.3-pending: 13 of 16 (81%) — {2..8 from b0566 minus pdf_scanned, 10, 12..16 from b0568}; correction: {10, 12, 13, 14, 15, 16} = 6 from b0568 + b0566 deferrals on parsing already accounted; precise tally follows

(Note: b0566 deferred {2..8} as `pdf_extraction_empty_likely_scanned` (OCR-pending), not v0.3.3-pending. So ZMCC 2018 cohort split is: 1 written + 9 OCR-pending {2..9, 11} + 6 v0.3.3-pending {10, 12..16} = 16 covered.)

## Un-fetched published nums

- {17} — only one ZMCC 2018 published num remains un-GET-fetched. To complete ZMCC 2018 in next tick.

## Integrity checks

- corpus.sqlite records=1861, records_fts=1861, judgments_meta=171 (unchanged from b0566)
- PRAGMA integrity_check = ok
- FTS gap = 0
- judges_registry.yaml unchanged (no new judges this tick)
- approvals.yaml NOT modified

## Fetch budget

- This tick: 4 HEAD + 16 GET (8 HTML + 8 PDF) = 20 zambialii fetches
- Cumulative today (judgment-ingestion-worker): 54 → **74/500**
- User-Agent: `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)`
- Rate limit: 5s between requests, honoured throughout

## Next-tick recommendation

1. **ZMCC 2018 final-1 GET-fetch** — fetch num 17 (Shanseko v Lealui or similar — discoverable on GET) to fully cover ZMCC 2018. Then close the year.
2. **ZMCC 2017 sparse HEAD probe** — start next-year discovery via `{1, 5, 10, 15, 20, 25}` per b0560/b0566 pattern. ZMCC 2017 is the first year of the Constitutional Court (year of court establishment).
3. **Standing**: parser_v0.3.3 anchor pack authoring (80 records pending — predominantly ZMCC 2017–2020 declaratory-holding sample). Recommend operator schedule v0.3.3 development.
4. **Standing**: OCR pipeline implementation (14 records pending — ZMCC 2018 ×9 + ZMCC 2020 ×5). Recommend operator schedule OCR pipeline.
5. **Standing**: operator action on Phase 5 ceiling 171/160 (+11 above sentinel; unchanged this tick since 0 records written).

## Provenance

- HEAD probes: zambialii.org/akn/zm/judgment/zmcc/2018/{16,17,18,19}/eng — 16 → eng@2018-06-20, 17 → eng@2018-06-22, 18 → 404, 19 → 404
- GET fetches: zambialii.org/akn/zm/judgment/zmcc/2018/{9..16}/eng (HTML, then `/source.pdf` for PDF) — all 8 returned 200 OK on both endpoints
- Raw bytes saved under `raw/zambialii/judgments/zmcc/2018/`
- Parse outputs in `_work/b0568/`
