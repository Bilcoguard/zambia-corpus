# Batch 0180 — Phase 4 sis_tax (pilot)

- **Phase:** phase_4_bulk
- **Sub-phase:** sis_tax (first ingestion under this priority_order item)
- **Batch number:** 0180
- **Completed at:** 2026-04-24T12:xx:xxZ
- **Records written:** 8
- **Fetches used:** 16 (8 AKN HTML + 8 PDF fallback, zambialii 5s+1s crawl-delay
  honoured throughout)
- **Today's fetches cumulative:** ~112/2000 (well under budget)
- **Integrity:** ALL PASS (CHECK0/1/2/3/4/5)

## Motivation

Batch 0179 next-tick plan: `/legislation/subsidiary` listing empirically
exhausted for corporate-keyword candidates; pivot to sis_tax (next in
`approvals.yaml.priority_order`). Discovery re-uses on-disk
`raw/zambialii/discovery/subsidiary-page-{04..10}.html` — no new discovery
fetches required.

## Discovery

A word-boundary tax-keyword regex over the 7 cached listing pages
(pages 4–10; pages 11–12 confirmed 404 at source in batch 0178) surfaced
**30 novel tax-keyword candidates** not in HEAD. Keyword families used:

- `income tax` / `value added tax` / `vat`
- `customs` / `excise` / `excise duty` / `customs duty`
- `property transfer tax` / `ptt`
- `tax appeals` / `taxation`
- `mineral royalty` / `turnover tax` / `withholding tax` / `presumptive tax`
- `skills development levy` / `tourism levy` / `insurance premium levy`
- `double taxation` / `transfer pricing`
- `revenue authority` / `zra`

Top-8 selected for diversity across tax-law substance:

| Slot | Title | Sections | Source |
|------|-------|---------:|--------|
| si/2021/106 | Value Added Tax (Electronic Fiscal Devices) (Amendment) Regulations, 2021 | 4 | ZambiaLII AKN PDF |
| si/2021/105 | Value Added Tax (Exemption) (Amendment) Order, 2021 | 3 | ZambiaLII AKN PDF |
| si/2021/104 | Value Added Tax (Zero Rating) (Amendment) Order, 2021 | 3 | ZambiaLII AKN PDF |
| si/2020/082 | Income Tax (Double Taxation Relief) (The Swiss Confederation) Order, 2020 | 101 | ZambiaLII AKN PDF |
| si/2020/033 | Value Added Tax (Electronic Fiscal Devices) Regulations, 2020 | 12 | ZambiaLII AKN PDF |
| si/2018/006 | Income Tax (Double Taxation Relief) (The Kingdom of Morocco) Order, 2018 | 105 | ZambiaLII AKN PDF |
| si/2018/048 | Income Tax (Tax Agent) (Terms and Conditions) Regulations, 2018 | 4 | ZambiaLII AKN PDF |
| si/2016/056 | Tourism and Hospitality (Tourism Levy) Regulations, 2016 | 12 | ZambiaLII AKN PDF |

Deferred / skipped candidates (22 of the 30):
- si/2019/25 (Income Tax Treasury Bill and Bond Regulations) — deliberately
  skipped; already gapped in batch 0179 as `pdf_parse_empty` (scan-only PDF,
  OCR out of scope).
- 21 other tax SIs queued for batch 0181+: 2020/11, 2019/11, 2018/61,
  2018/36, 2017/74, 2017/51, 2017/43, 2017/41, 2017/40, 2017/30, 2017/02,
  2016/30, 2015/95, 2015/70, 2015/46, 2015/35, 2015/31, 2015/30, 2015/20,
  2014/69, 2014/68.

## Records

All 8 records emitted to `records/sis/{year}/{id}.json` with full
provenance (source_url, source_hash, fetched_at, parser_version=0.5.0).
Raw HTML + PDF stored under `raw/zambialii/si/{year}/`.

Two of the eight — the Swiss Confederation and Morocco double-taxation
treaties — are full international tax agreements incorporated by SI, so
section counts of 101 and 105 reflect the treaty articles and protocols
rather than pure SI section structure. This is expected behaviour of the
current regex-based parser and will be cleaned up in a future parser
revision (section-count normalisation is tracked as an infrastructure
item — see worker.log batch-0171 note on running-header/TOC echoes).

## Integrity (all PASS)

- CHECK1: no batch-internal duplicate IDs (8 unique)
- CHECK2: all `amended_by` / `repealed_by` references resolve (none present
  in these records — all are primary SIs)
- CHECK3: all `cited_authorities` references resolve (none present)
- CHECK4: `source_hash` matches on-disk raw PDF for all 8 records
  (sha256 verified for each)
- CHECK5: all required fields populated on all records

## Budget

- Today: ~112 fetches / 2000 cap
- Budget slack: ~94.4%

## Next-tick plan

Continue sis_tax with next wave of 6–8 candidates from the remaining 21
deferred slots. Preference order within tax:

1. Double-taxation treaty orders with major partners
   (si/2017/41 Norway, si/2015/95 Netherlands, si/2015/70 Ireland,
   si/2015/20 Botswana) — high citation-value for cross-border work.
2. Property Transfer Tax orders 2015 (si/2015/30, 31, 35) — small
   but PTT-specific, covers a discrete tax-law sub-surface.
3. VAT exemption/zero-rating historical snapshot — si/2014/68, si/2014/69.
4. Customs/excise suspension orders — si/2017/02, 30, 40, 51,
   2018/36, 2018/61, 2019/11 — lower individual yield, consolidate in
   one batch or defer to a dedicated customs sweep.

After sis_tax at ~20+ records the sub-phase can rotate to sis_employment.

## Notes

- Word-boundary tax regex correctly excluded false positives (e.g. "suspension"
  matched "pension" in older substring filters — confirmed no recurrence here).
- sandbox 45s bash timeout: batch split into 4 sub-ticks (3+2+2+1 records)
  to stay under the timeout while respecting zambialii 5s crawl-delay.
- corpus.sqlite remains stuck at 535 rows due to the stale rollback-journal
  issue flagged in worker.log batch-0179 — this batch's records are on
  disk and committed as JSON but are not yet in FTS. Human-driven sqlite
  rebuild still required.
- rclone unavailable in sandbox: B2 raw sync deferred to host —
  `rclone sync raw/ b2raw:kwlp-corpus-raw/ --fast-list --transfers 4`.
