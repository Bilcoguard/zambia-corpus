# Batch 0091 — Phase 4 Bulk Ingestion

**Date:** 2026-04-15
**Worker:** KateWestonLegal-CorpusBuilder/1.0
**Phase:** 4 (bulk ingestion — acts_in_force)
**Source:** ZambiaLII (zambialii.org)
**Parser version:** 0.5.0

## Records Added (8)

| # | Record ID | Title | Year | Sections | Format |
|---|-----------|-------|------|----------|--------|
| 1 | act-zm-1938-012-debtors-act-1938 | Debtors Act, 1938 | 1938 | 5 | HTML/AKN |
| 2 | act-zm-1938-052-inquests-act-1938 | Inquests Act, 1938 | 1938 | 17 | HTML/AKN |
| 3 | act-zm-1940-038-pharmacy-and-poisons-act-1940 | Pharmacy and Poisons Act, 1940 | 1940 | 18 | HTML/AKN |
| 4 | act-zm-1944-013-extermination-of-mosquitoes-act-1944 | Extermination of Mosquitoes Act, 1944 | 1944 | 6 | HTML/AKN |
| 5 | act-zm-1947-031-printed-publications-act-1947 | Printed Publications Act, 1947 | 1947 | 4 | HTML/AKN |
| 6 | act-zm-1949-019-fencing-act-1949 | Fencing Act, 1949 | 1949 | 6 | HTML/AKN |
| 7 | act-zm-1949-021-mental-disorders-act-1949 | Mental Disorders Act, 1949 | 1949 | 23 | HTML/AKN |
| 8 | act-zm-1951-027-pensions-increase-act-1951 | Pensions (Increase) Act, 1951 | 1951 | 2 | HTML/AKN |

**Total sections:** 81

## Integrity Checks

- Duplicate IDs: PASS (674 total unique IDs)
- Source hash verification: ALL PASS (8/8)
- Reference resolution (amended_by/repealed_by): ALL PASS
- Required fields: ALL PASS
- ID pattern: ALL PASS

## Notes

- All 8 acts fetched via HTML/AKN format from ZambiaLII eng@1996-12-31 consolidation endpoint.
- ZambiaLII pagination (pages 1-10) yielded ~328 unprocessed acts remaining.
- Acts span colonial-era (1938-1951) legislation.
- All records parsed as consolidated versions (consolidated_as_of: 1996-12-31).

## Budget

- Fetches this batch: 8
- Today's total fetches: ~295/2000
- Budget status: WITHIN LIMITS

## Next Targets

Batch 0092 should continue with: acts from 1952/039, 1953/015, 1953/021, 1953/046, 1953/059, 1954/012, 1956/034, 1957/008.
