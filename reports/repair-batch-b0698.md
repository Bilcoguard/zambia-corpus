# Repair Batch b0698 — Summary

**Date:** 2026-05-18
**Worker:** repair-corpus
**Parser:** repair-0.6.98
**Elapsed:** 21.7 s (under 20-min budget)

## Targets identified (live SQL)

- Condition A (corrupted digit-line bodies): 0
- Condition B (no-body acts/sis): 57
- Condition C (stub acts/sis < 200 chars): 0
- **Dedup targets:** 57
- **Picked (MAX_BATCH=8):** 8

## Outcome

- Repaired: **8**
- Failed: **0**
- Remaining (Condition B for next tick): **49**

## Repaired IDs

| ID | body len |
|---|---|
| si-zm-2021-088-electoral-process-local-government-by-elections-election-date-and-time-of-poll-no-4-order-2021 | 1841 |
| si-zm-2021-092-statistics-national-census-declaration-order-2021 | 1623 |
| si-zm-2021-094-electricity-common-carrier-declaration-revocation-order-2021 | 811 |
| si-zm-2021-109-plant-variety-and-seeds-amendment-regulations-2021 | 4184 |
| si-zm-2021-112-road-traffic-fees-regulations-2021 | 4701 |
| si-zm-2021-114-provincial-and-district-boundaries-division-amendment-no-2-order-2021 | 9069 |
| si-zm-2022-005-economic-and-financial-crimes-division-of-court-order-2022 | 1300 |
| si-zm-2022-006-zambia-police-fees-regulations-2022 | 3105 |

All 8 sources: ZambiaLII AKN-SI HTML pages → `/akn/.../source.pdf` → pdfplumber extraction → quality gate passed (length > 200, digit-ratio ok, legal-text markers present).

## Integrity

- records: 1946
- records_fts: 1946
- match: **true**
- PRAGMA quick_check: **ok**

## B2 sync

Deferred to host — rclone not available in sandbox.

## Notes

- All 8 records fetched cleanly (HTTP 200) — the zambialii.org outage from earlier batches has remained resolved.
- One body (si-zm-2021-094) came in at 811 chars, above the 200-char gate but on the shorter side; quality gate passed (contains "order", "minister" markers and the document is genuinely brief — a revocation order).
- No corrupted or stub bodies in the database this tick.
