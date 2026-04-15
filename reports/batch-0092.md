# Batch 0092 — Phase 4 Bulk Ingestion

**Date:** 2026-04-15
**Worker:** KateWestonLegal-CorpusBuilder/1.0
**Phase:** 4 (bulk ingestion — acts_in_force)
**Source:** ZambiaLII (zambialii.org)
**Parser version:** 0.5.0

## Records Added (8)

| # | Record ID | Title | Year | Sections | Format |
|---|-----------|-------|------|----------|--------|
| 1 | act-zm-1952-039-international-bank-loan-rhodesia-railways-act-1952 | International Bank Loan (Rhodesia Railways) Act, 1952 | Act No. 39 of 1952 | 9 | HTML/AKN |
| 2 | act-zm-1953-015-probation-of-offenders-act-1953 | Probation of Offenders Act, 1953 | Act No. 15 of 1953 | 18 | HTML/AKN |
| 3 | act-zm-1953-021-international-bank-loan-approval-act-1953 | International Bank Loan (Approval) Act, 1953 | Act No. 21 of 1953 | 14 | HTML/AKN |
| 4 | act-zm-1953-046-defamation-act-1953 | Defamation Act, 1953 | Act No. 46 of 1953 | 19 | HTML/AKN |
| 5 | act-zm-1953-059-noxious-weeds-act-1953 | Noxious Weeds Act, 1953 | Act No. 59 of 1953 | 14 | HTML/AKN |
| 6 | act-zm-1954-012-control-of-goods-act-1954 | Control of Goods Act, 1954 | Act No. 12 of 1954 | 8 | HTML/AKN |
| 7 | act-zm-1956-034-national-assembly-powers-and-privileges-act-1956 | National Assembly (Powers and Privileges) Act, 1956 | Act No. 34 of 1956 | 35 | HTML/AKN |
| 8 | act-zm-1957-008-lotteries-act-1957 | Lotteries Act, 1957 | Act No. 8 of 1957 | 15 | HTML/AKN |

**Total sections:** 132

## Integrity Checks

- Duplicate IDs: PASS (682 total unique IDs)
- Source hash verification: ALL PASS (8/8)
- Reference resolution (amended_by/repealed_by): ALL PASS
- Required fields: ALL PASS
- ID pattern: ALL PASS

## Notes

- All 8 acts fetched via HTML/AKN format from ZambiaLII eng@1996-12-31 consolidation endpoint.
- ZambiaLII pagination (pages 1-10) continues to work.
- Acts span 1952-1957 era legislation.
- All records parsed as consolidated versions (consolidated_as_of: 1996-12-31).

## Budget

- Fetches this batch: 8
- Today's total fetches: ~282/2000
- Budget status: WITHIN LIMITS

## Next Targets

Batch 0093 should continue with next acts from ZambiaLII pagination (late 1950s-early 1960s era).
