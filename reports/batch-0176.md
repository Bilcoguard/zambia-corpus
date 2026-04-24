# Batch 0176 — Phase 4 sis_corporate

**Date (UTC):** 2026-04-24
**Phase:** 4 (bulk ingestion) / sub-phase: sis_corporate
**Target:** ingest 2 corporate SIs surfaced in batch-0175 discovery; sweep /legislation/subsidiary pages 7 & 8 for next-tick candidates

## Committed records (+2)

| ID | Title | Sections | Source |
|----|-------|----------|--------|
| `si-zm-2019-062-income-tax-konoike-construction-company-limited-approval-and-exemption-order-2019` | Income Tax (Konoike Construction Company Limited) (Approval and Exemption) Order, 2019 | 4 | PDF (zambialii) |
| `si-zm-2019-059-insurance-fidelity-fund-regulations-2019` | Insurance (Fidelity Fund) Regulations, 2019 | 22 | PDF (zambialii) |

Both were novel vs HEAD. HTML AKN pages returned <2 sections (ZambiaLII render anomaly for 2019 SIs), so PDF fallback was used and produced clean per-section output.

## Fetches

Total: 6 (within today's budget ~56 / 2000)
- 2 HTML AKN pages (si/2019/62, si/2019/59)
- 2 PDF source files (fallback after sparse HTML)
- 2 discovery listings (/legislation/subsidiary?page=7, page=8)

Rate limit: 5s ZambiaLII crawl-delay honoured. Robots.txt: `/akn/zm/act/si/` and `/legislation/subsidiary` are explicitly allowed.

## Integrity checks

All batch-scoped checks PASS:
- **CHECK1** unique IDs within batch ✓
- **CHECK2** no HEAD collision ✓
- **CHECK3** source_hash sha256 matches on-disk raw ✓
- **CHECK4** no unresolved cross-refs (amended_by / repealed_by / cited_authorities all empty on these SIs) ✓
- **CHECK5** required fields present (id, type, jurisdiction, title, citation, source_url, source_hash, fetched_at, parser_version, sections) ✓

## Filter refinement

`CORPORATE_KEYWORDS` now uses word-boundary regex (`\b(?:compan(?:y|ies)|...|pension|...)\b`) to fix the `pension` ⊂ `suspension` false-positive documented in batch-0175 (see `gaps.md`). Confirmed by page 7-8 results: all 6 corporate candidates matched on full-word tokens; no "suspension/pension" collisions remain.

## Discovery (pages 7 & 8)

6 novel corporate candidates surfaced for next tick:

| Year/Num | Title | Keyword |
|----------|-------|---------|
| 2017/70 | Income Tax (African Management Services Company) (Approval and Exemption) Order, 2017 | company |
| 2017/42 | Income Tax (Overseas Private Investment Corporation) (Approval and Exemption) Order, 2017 | investment |
| 2017/19 | National Pension Scheme (Investment) Regulations, 2017 | investment, pension |
| 2016/95 | National Pension Scheme (Medical Board) Regulations, 2016 | pension |
| 2016/9  | Financial Intelligence Centre (General) Regulations, 2016 | financial |
| 2016/52 | Financial Intelligence Centre (Prescribed Thresholds) Regulations, 2016 | financial |

90 novel non-corporate candidates also surfaced — preserved in the raw listing HTML for later sub-phase sweeps (sis_employment, sis_tax, sis_mining).

## Gaps

None this batch.

## Next tick plan

1. Ingest the 4 strongest novel corporate candidates above (MAX_BATCH_SIZE=8, but pace at 4 per tick to keep wall-clock safe with PDF fallback):
   - 2017/19 National Pension Scheme (Investment) Regulations (strongest corporate-governance relevance)
   - 2016/9 Financial Intelligence Centre (General) Regulations (AML/CFT cornerstone)
   - 2016/52 Financial Intelligence Centre (Prescribed Thresholds) Regulations
   - 2016/95 National Pension Scheme (Medical Board) Regulations
2. Defer the 2 "Income Tax Company Exemption Order" candidates (2017/70, 2017/42) to a later tick — they are narrow company-specific tax orders rather than generally-applicable corporate regulation.
3. Continue /legislation/subsidiary sweep with pages 9 & 10.

## B2 raw sync

Deferred to host (rclone not available in sandbox). Peter to run:
```
rclone sync raw/ b2raw:kwlp-corpus-raw/ --fast-list --transfers 4
```
