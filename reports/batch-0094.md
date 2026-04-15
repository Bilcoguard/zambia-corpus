# Batch 0094 Report — Phase 4 Bulk Ingestion

**Date:** 2026-04-15T18:05:00Z
**Phase:** 4 (Bulk Ingestion — acts_in_force)
**Source:** ZambiaLII (zambialii.org)
**Format:** HTML/AKN
**Records added:** 8
**Total sections:** 717
**Fetches this batch:** 8

## Records

| # | ID | Title | Year | Sections |
|---|-----|-------|------|----------|
| 1 | `act-zm-1960-024-development-united-kingdom-government-loan-act-1960` | Development (United Kingdom Government) Loan Act, 1960 | 1960 | 8 |
| 2 | `act-zm-1960-034-inland-waters-shipping-act-1960` | Inland Waters Shipping Act, 1960 | 1960 | 192 |
| 3 | `act-zm-1960-039-maintenance-orders-act-1960` | Maintenance Orders Act, 1960 | 1960 | 156 |
| 4 | `act-zm-1960-041-high-court-act` | High Court Act (Cap. 27) | 1960 | 0 (PDF only) |
| 5 | `act-zm-1960-048-district-messengers-act-1960` | District Messengers Act, 1960 | 1960 | 26 |
| 6 | `act-zm-1960-059-land-survey-act-1960` | Land Survey Act, 1960 | 1960 | 231 |
| 7 | `act-zm-1961-010-judgments-act` | Judgments Act (Cap. 81) | 1961 | 0 (PDF only) |
| 8 | `act-zm-1961-037-professional-boxing-and-wrestling-control-act-1961` | Professional Boxing and Wrestling Control Act, 1961 | 1961 | 104 |

## Integrity Checks

- Duplicate ID check: ALL PASS (698 unique records)
- Source hash verification: ALL PASS
- Reference resolution (amended_by/repealed_by): ALL PASS
- Required fields: ALL PASS

## Notes

- 2 acts (High Court Act Cap. 27, Judgments Act Cap. 81) have content in PDF only — HTML/AKN page is a landing stub. Logged to gaps.md for future PDF-based re-parse.
- SQLite rebuild deferred (disk I/O error on mounted workspace). To be rebuilt on next successful tick or manually.
- All 8 acts fetched via HTML/AKN format from ZambiaLII eng@1996-12-31 consolidation endpoint.

## Budget

- Fetches this batch: 8
- Today's estimated total fetches: ~308/2000
- Budget status: WITHIN LIMITS

## Next Targets

Batch 0095: Continue with 1960s-era acts from ZambiaLII pagination. ~296 ZambiaLII acts remaining.
