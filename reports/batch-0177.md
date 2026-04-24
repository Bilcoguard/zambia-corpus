# Batch 0177 — Phase 4 sis_corporate

**Date (UTC):** 2026-04-24
**Phase:** 4 (bulk ingestion) / sub-phase: sis_corporate
**Target:** ingest 4 strongest novel corporate SIs from batch-0176 pages 7-8 discovery; sweep /legislation/subsidiary pages 9 & 10 for next-tick candidates

## Committed records (+4)

| ID | Title | Sections | Source |
|----|-------|----------|--------|
| `si-zm-2017-019-national-pension-scheme-investment-regulations-2017` | National Pension Scheme (Investment) Regulations, 2017 | 21 | PDF (zambialii) |
| `si-zm-2016-009-financial-intelligence-centre-general-regulations-2016` | Financial Intelligence Centre (General) Regulations, 2016 | 63 | PDF (zambialii) |
| `si-zm-2016-052-financial-intelligence-centre-prescribed-thresholds-regulations-2016` | Financial Intelligence Centre (Prescribed Thresholds) Regulations, 2016 | 49 | PDF (zambialii) |
| `si-zm-2016-095-national-pension-scheme-medical-board-regulations-2016` | National Pension Scheme (Medical Board) Regulations, 2016 | 11 | PDF (zambialii) |

All 4 were novel vs HEAD. HTML AKN pages returned 0 sections (ZambiaLII render anomaly for 2016/2017 SIs), so PDF fallback was used and produced clean per-section output.

## Fetches

Total: 10 (within today's budget)
- 4 HTML AKN pages (si/2017/19, si/2016/9, si/2016/52, si/2016/95)
- 4 PDF source files (fallback after sparse HTML)
- 2 discovery listings (/legislation/subsidiary?page=9, page=10)

Rate limit: 5s ZambiaLII crawl-delay honoured (enforced between successive fetches in the same sub-tick; across sub-ticks the inter-call host delay is always >>5s).
Robots.txt: `/akn/zm/act/si/` and `/legislation/subsidiary` are explicitly allowed.

## Integrity checks

All batch-scoped checks PASS:
- **CHECK1** unique IDs within batch ✓ (4/4)
- **CHECK2** no HEAD filename collision ✓
- **CHECK3** source_hash sha256 matches on-disk raw ✓ (4/4)
- **CHECK4** no unresolved cross-refs (amended_by / repealed_by / cited_authorities all empty on these SIs) ✓
- **CHECK5** required fields present (id, type, jurisdiction, title, citation, source_url, source_hash, fetched_at, parser_version, sections) ✓

## Discovery (pages 9 & 10)

4 novel corporate candidates surfaced for next tick:

| Year/Num | Title | Keywords |
|----------|-------|----------|
| 2016/18 | Insurance Premium Levy (Exemption) Order, 2016 | insurance |
| 2015/87 | Diplomatic Immunities and Privileges (ZEP-RE PTA Re-Insurance Company) Order, 2015 | company, insurance |
| 2015/33 | Road Traffic (Certificates of Security and Insurance) (Display) Regulations, 2015 | insurance |
| 2014/56 | Income Tax (European Investment Bank) (Approval and Exemption) Order, 2014 | bank, investment |

95 novel non-corporate candidates also surfaced — preserved in the raw listing HTML for later sub-phase sweeps (sis_employment, sis_tax, sis_mining, sis_data_protection, sis_family).

## Gaps

None this batch.

## Next tick plan

1. Ingest 2-4 of the 4 novel corporate candidates above, prioritising:
   - 2015/87 Diplomatic Immunities and Privileges (ZEP-RE PTA Re-Insurance Company) Order — adds corporate-entity statutory status record
   - 2014/56 Income Tax (European Investment Bank) (Approval and Exemption) Order — investment-bank exemption
   - 2016/18 Insurance Premium Levy (Exemption) Order — insurance levy exemption
2. Defer 2015/33 Road Traffic (Certificates of Security and Insurance) Displacement — corporate keyword match is on compulsory-insurance terminology, not corporate regulation substance.
3. Continue /legislation/subsidiary sweep with pages 11 & 12 if the listing has more pages, or pivot to ZambiaLII /akn/zm/act/si/YYYY listings by year.

## B2 raw sync

Deferred to host (rclone not available in sandbox). Peter to run:
```
rclone sync raw/ b2raw:kwlp-corpus-raw/ --fast-list --transfers 4
```
