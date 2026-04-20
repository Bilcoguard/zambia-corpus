# Batch 0147 Report

**Date:** 2026-04-20T13:39:24Z
**Phase:** 4 (Bulk Ingestion)
**Records committed:** 7
**Fetches (script):** 15
**Integrity:** PASS

## Strategy

Continuation of the batch 0146 next-tick plan: Bank of Zambia 2001 (2001/11, deferred from 0146), Mines and Minerals 2011 (2011/28, deferred from 0146), plus fresh primary-statute candidates from regulatory / local-government / insurance / wildlife / immigration / tourism search probes. Candidate (year, num) pairs were obtained by parsing the `results_html` fragment of the ZambiaLII search API (`/search/api/documents/?search=<q>&nature=Act`) across 16 hint queries (Trade Marks, Patents, Insurance, Pensions and Insurance, Public Finance, Local Government, National Parks, Immigration, Tourism, Consumer Protection, Copyright and Performance, Competition, Bank of Zambia 2001, Mines and Minerals, Fisheries, Probate and Administration of Estates); each hit was cross-referenced against HEAD by (year, num) tuple via `git ls-tree -r HEAD records/acts/`. Twelve non-HEAD candidates were queued; the processor fetches each AKN page, applies a title-token filter (rejects `amendment`, `appropriation`, `repeal`, `supplementary`, `validation`) BEFORE any raw or record file is written, and stops at MAX_RECORDS=8 accepted primary statutes. PDF fallback is invoked only when the HTML returns fewer than 2 parsed sections.

## Committed records

| # | ID | Title | Citation | Sections | Source |
|---|----|-------|----------|----------|--------|
| 1 | `act-zm-1974-021-fisheries-act-1974` | Fisheries Act, 1974 | Act No. 21 of 1974 | 48 | HTML/AKN |
| 2 | `act-zm-2004-015-public-finance-act-2004` | Public Finance Act, 2004 | Act No. 15 of 2004 | 67 | PDF |
| 3 | `act-zm-1965-029-immigration-and-deportation-act-1965` | Immigration and Deportation Act, 1965 | Act No. 29 of 1965 | 38 | HTML/AKN |
| 4 | `act-zm-1998-012-zambia-wildlife-act-1998` | Zambia Wildlife Act, 1998 | Act No. 12 of 1998 | 259 | PDF |
| 5 | `act-zm-1994-022-weights-and-measures-act-1994` | Weights and Measures Act, 1994 | Act No. 22 of 1994 | 51 | HTML/AKN |
| 6 | `act-zm-1991-021-local-government-elections-act-1991` | Local Government Elections Act, 1991 | Act No. 21 of 1991 | 52 | HTML/AKN |
| 7 | `act-zm-2007-023-tourism-and-hospitality-act-2007` | Tourism and Hospitality Act, 2007 | Act No. 23 of 2007 | 120 | PDF |

**Total sections:** 635

## Integrity checks
- CHECK 1 (batch unique IDs): PASS
- CHECK 2 (no HEAD collision): PASS
- CHECK 3 (source_hash matches raw on disk): PASS
- CHECK 4 (amended_by / repealed_by reference resolution): PASS — no cross-refs in this batch
- CHECK 5 (required fields present): PASS

## Raw snapshots

All raw bytes saved to `raw/zambialii/<year>/<id>.{html|pdf}`. B2 sync deferred to host (rclone not available in sandbox).

## Gaps / skipped targets

- bank-of-zambia-2001 (Act 11/2001): title rejected (contains 'amendment'): 'Development Bank of Zambia (Amendment) Act, 2001'
- mines-minerals-2011 (Act 28/2011): title rejected (contains 'amendment'): 'Mines and Minerals Development (Amendment) Act, 2011'
- pensions-and-insurance-2005 (Act 26/2005): title rejected (contains 'amendment'): 'Insurance (Amendment) Act, 2005'
- local-government-1993 (Act 30/1993): title rejected (contains 'amendment'): 'Local Government (Amendment) Act, 1993'
- immigration-1997 (Act 25/1997): title rejected (contains 'amendment'): 'Immigration and Deportation (Amendment) Bill, I997'

## Notes

- B-POL-ACT-1 title filter applied pre-write: any candidate whose AKN-page title contained `amendment`, `appropriation`, `repeal`, `supplementary`, or `validation` was rejected without producing a raw or record file.
- Next tick: continue the primary-statute sweep — pending candidates include Trade Marks Act (Cap 401 / 1958 parent), Patents Act (Cap 400 / 1957 parent), Town and Country Planning Act parents (1961/32, 1974/30), Valuation Surveyors Act (1976/34), Local Government Elections Act (2004/9), Judges (Emoluments) variants (1976/22, 1988/21), National Parks and Wildlife Act 1971/27 / 1982/33, Zambia Tourism Board / Zambia National Tourism Board parents (1979/29, 1985/22), Chartered Institute of Public Relations (2003/15), and the unresolved Citizens Economic Empowerment Act 2006 correct AKN slot. Also pending: repeal-chain links act-zm-1996-042-anti-corruption-commission-act-1996 → act-zm-2012-003 and act-zm-1965-056-prisons → act-zm-2021-037-zambia-correctional-service.

