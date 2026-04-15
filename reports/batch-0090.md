# Batch 0090 — Phase 4 Bulk Ingestion

**Date:** 2026-04-15
**Worker:** KateWestonLegal-CorpusBuilder/1.0
**Phase:** 4 (bulk ingestion — acts_in_force)
**Source:** ZambiaLII (zambialii.org)
**Parser version:** 0.5.0

## Records Added (8)

| # | Record ID | Title | Year | Sections | Format |
|---|-----------|-------|------|----------|--------|
| 1 | act-zm-1930-042-penal-code-1930 | Penal Code, 1930 | 1930 | 818 | PDF |
| 2 | act-zm-1931-021-loan-act-1931 | Loan Act, 1931 | 1931 | 5 | HTML/AKN |
| 3 | act-zm-1933-010-employment-of-young-persons-and-children-act-1933 | Employment of Young Persons and Children Act, 1933 | 1933 | 21 | HTML/AKN |
| 4 | act-zm-1933-023-criminal-procedure-code-1933 | Criminal Procedure Code, 1933 | 1933 | 428 | HTML/AKN |
| 5 | act-zm-1936-022-probates-resealing-act-1936 | Probates (Resealing) Act, 1936 | 1936 | 8 | HTML/AKN |
| 6 | act-zm-1937-005-foreign-judgments-reciprocal-enforcement-act-1937 | Foreign Judgments (Reciprocal Enforcement) Act, 1937 | 1937 | 13 | HTML/AKN |
| 7 | act-zm-1937-021-markets-act-1937 | Markets Act, 1937 | 1937 | 11 | HTML/AKN |
| 8 | act-zm-1938-011-money-lenders-act-1938 | Money Lenders Act, 1938 | 1938 | 22 | HTML/AKN |

**Total sections:** 1,326

## Integrity Checks

- Duplicate IDs: PASS
- Source hash verification: ALL PASS (8/8)
- Reference resolution (amended_by/repealed_by): ALL PASS
- Required fields: ALL PASS

## Notes

- Penal Code (1930) required PDF fallback — HTML page had no inline content (behind sign-in wall). PDF successfully parsed with 818 sections across 118 pages.
- Criminal Procedure Code (1933) is a substantial act with 428 sections via AKN HTML.
- ZambiaLII pagination working (pages 0-10, ~459 principal acts discoverable). 234 unprocessed acts remain.
- All acts fetched via `eng@1996-12-31` consolidation endpoint.

## Budget

- Fetches this batch: ~33
- Today's total fetches: ~287/2000
- Budget status: WITHIN LIMITS

## Next Targets

Batch 0091 should continue with: Debtors Act 1938, Inquests Act 1938, Interpretation and General Provisions Act 1938, Juveniles Act 1938, Landlord and Tenant (Business Premises) Act 1938, Liquor Licensing Act 1938, Penal Code (Amendment) Act 1938, Prisons Act 1938.
