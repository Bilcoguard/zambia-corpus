# Batch 0574 — judgment-ingestion-worker (2026-05-10)

**UTC:** 2026-05-10T18:25:00Z
**Worker:** judgment-ingestion-worker (scheduled tick)
**Parser:** parser_v0.3.2 (build_record_v032 — `scripts/batch_0498_parse.py`)
**Tick scope:** Priority (c) ZMCC 2017 final-1 GET-fetch + Priority (b) ZMSC 2023 upper-bound HEAD probe & intra-range gap-fill

## Tick scope

- Priority (a) reparse: skipped (v0.3.2 cannot move v0.3.3-pending or OCR-pending; standing per b0571 8-of-8 evidence).
- Priority (b) SCZ sweep: ZMSC 2023 upper-bound HEAD probe + intra-range gap-fill {01, 13}.
- Priority (c): ZMCC 2017 final-1 GET-fetch (num 8) per b0573 next-tick rec #1.

## ZMCC 2017 final-1 (num 8)

| num | result | date       | html_bytes | pdf_bytes | raw_sha256 (prefix)         |
|-----|--------|------------|-----------:|----------:|------------------------------|
| 8   | 200    | 2017-11-17 |     38,284 | 6,487,792 | bb2b40e4854d9c4f…            |

Case: *Maluba v Mwewa and Another* — `[2017] ZMCC 8` — `html_url` https://zambialii.org/akn/zm/judgment/zmcc/2017/8/eng@2017-11-17.

**Parse result:** `record is None`, reason `pdf_extraction_empty_likely_scanned` — joins ZMCC 2017 OCR-pending cohort.

ZMCC 2017 now fully GET-fetched: 8 of 8 published nums on disk. Year coverage closed.

## ZMSC 2023 upper-bound HEAD probe

| num | result |
|-----|--------|
| 24  | 404    |
| 25  | 404    |
| 30  | 404    |

Upper boundary closed at num 23 (three consecutive 404s above plus prior on-disk evidence of {2..23 minus 13}).

## ZMSC 2023 intra-range gap-fill (nums 01, 13)

| num | result | date       | html_bytes | pdf_bytes |
|-----|--------|------------|-----------:|----------:|
| 01  | 200    | 2023-03-10 |     44,008 | 1,465,577 |
| 13  | 404    | —          |          — |         — |

- **zmsc/2023/01** *Citibank Zambia Ltd v Dudhia* — parsed: `record is None`, reason `html_no_summary_pdf_no_match`. Summary head: "One-year deadline to dispose labour complaints should be interpreted purposively; expiry does not automatically divest the court of jurisdiction." Joins v0.3.3-pending cohort.
- **zmsc/2023/13** confirmed-404 — publisher num-skip gap; not a fetch error.

**ZMSC 2023 published-nums set:** `{1..12, 14..23}` = 22 records. Year GET-fetch coverage now closed.

## Records written this tick (0)

None — both candidates returned `record is None`.

## Records deferred this tick (2)

| court/year/num | reason                                    | summary / note                                                                                          |
|----------------|-------------------------------------------|---------------------------------------------------------------------------------------------------------|
| zmcc/2017/8    | `pdf_extraction_empty_likely_scanned`     | 6.5 MB image-only PDF; ZMCC 2017 OCR-pending cohort.                                                    |
| zmsc/2023/1    | `html_no_summary_pdf_no_match`            | Labour-jurisdiction declaratory holding; v0.3.3-pending cohort.                                         |

## Confirmed-404 this tick (1)

| court/year/num | url                                                              |
|----------------|------------------------------------------------------------------|
| zmsc/2023/13   | https://zambialii.org/akn/zm/judgment/zmsc/2023/13/eng           |

## Cohort tallies after b0574

| Cohort           | Pre-b0574 | Δ b0574 | Post-b0574 |
|------------------|----------:|--------:|-----------:|
| v0.3.3-pending   |        81 |      +1 |     **82** |
| OCR-pending      |        20 |      +1 |     **21** |
| Records written  |       172 |       0 |    **172** |

## Fetch budget accounting

- This tick consumed **8 fetch units** (1 fetch_one ok = 2 requests, 1 fetch_one ok = 2 requests, 1 fetch_one 404 = 1 request, 3 HEAD probes = 3 requests).
- Cumulative today: **103 + 8 = 111 / 500** (worker = judgment-ingestion-worker; main worker-tick budget tracked separately).

## Integrity checks

- corpus.sqlite: `PRAGMA integrity_check` = `ok`; records=1862, judgments_meta=172, records_fts=1862 (unchanged from pre-tick — no new records written).
- Raw files on disk: ZMCC 2017/8 (html 38,284 B + pdf 6,487,792 B; pdf sha256 verified MATCH against fetch). ZMSC 2023/1 (html 44,008 B + pdf 1,465,577 B).
- judges_registry.yaml: not modified this tick.
- approvals.yaml: not modified this tick.
- gaps.md: appended b0574 entry.

## ZMCC 2017 — dimensional summary post-b0574

- Published nums: {1..8}
- HEAD-404 sentinels: {9, 10, 15, 20, 25}
- Coverage: 1 written {1} + 7 OCR-pending {2..8} + 0 v0.3.3-pending = 8 covered. **Year closed.**

## ZMSC 2023 — dimensional summary post-b0574

- Published nums: {1..12, 14..23} = 22.
- HEAD-404 sentinels: {13, 24, 25, 30}.
- On-disk raw: {1..12, 14..23} = 22.
- Records written: {4..9, 11, 14, 20} = 9.
- Deferred (no record yet): {1, 2, 3, 10, 12, 15..19, 21..23} = 13 (cohort split: zmsc/2023/1 v0.3.3-pending after this tick; nums 2, 3, 10, 12, 15..19, 21..23 carry prior-tick reason codes pending audit). **Year GET-fetch closed.**

## Next-tick recommendation

1. **ZMCC 2016 sparse HEAD probe** — investigate whether ZMCC 2016 exists (carry-over from b0573 rec #2).
2. **ZMSC 2022 GET-fetch missing nums** — raw=47, records=18, gap=29; most recent SCZ year with substantial un-fetched coverage.
3. **Standing**: parser_v0.3.3 anchor pack authoring (82 records pending).
4. **Standing**: OCR pipeline implementation (21 records pending).
5. **Standing**: operator action on Phase 5 ceiling 172/160.

## Execution mode

Inline runner; no derivative scripts committed (sandbox-session safety constraint, consistent with b0548..b0573 precedent). Driver imported `scripts/batch_0506_zmsc_fetch.py::fetch_one` for fetches and `scripts/batch_0498_parse.py::build_record_v032` for parsing.

## B2 sync

`rclone` not in sandbox — B2 sync of new raw bytes deferred to host (4 new raw files: ZMCC 2017/8 html+pdf, ZMSC 2023/1 html+pdf).

