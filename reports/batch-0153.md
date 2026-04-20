# Batch 0153 Report

**Date:** 2026-04-20T20:37:34Z
**Phase:** 4 (Bulk Ingestion)
**Records committed:** 8
**Repeal-chain links applied:** 0
**Fetches (script):** 15
**Integrity:** PASS

## Strategy

Two-stage candidate generation. Stage 1 processes the 5 MAX_RECORDS-deferred candidates that batch 0151 and 0152 flagged in `gaps.md` (year/number already verified in prior probes): Carriage by Air 1968/59, Rhodesia Railways Loans Guarantee 1950/18, General Loans (Guarantee) 1964/51, National Savings and Credit 1972/24, Corrupt Practice 1980/14. Stage 2 probes the ZambiaLII search API for Sale of Goods, Bills of Exchange, Juveniles Act, Hire Purchase, Stamp Duty, and Insurance Act parent (Cap. 392, likely 1997); hits surviving HEAD + title filters fill remaining slots up to MAX_RECORDS=8. Title filter rejects any slot whose AKN-page title contains `amendment`, `appropriation`, `repeal`, `supplementary`, `validation`, or `transitional` — applied pre-write, so rejected slots produce no raw or record file. PDF fallback is invoked only when the HTML returns fewer than 2 parsed sections.

## Committed records

| # | ID | Title | Citation | Sections | Source | Origin |
|---|----|-------|----------|----------|--------|--------|
| 1 | `act-zm-1968-059-carriage-by-air-act-1968` | Carriage by Air Act, 1968 | Act No. 59 of 1968 | 25 | HTML/AKN | seed |
| 2 | `act-zm-1950-018-rhodesia-railways-loans-guarantee-act-1950` | Rhodesia Railways Loans Guarantee Act, 1950 | Act No. 18 of 1950 | 7 | HTML/AKN | seed |
| 3 | `act-zm-1964-051-general-loans-guarantee-act-1964` | General Loans (Guarantee) Act, 1964 | Act No. 51 of 1964 | 6 | HTML/AKN | seed |
| 4 | `act-zm-1972-024-national-savings-and-credit-act-1972` | National Savings and Credit Act, 1972 | Act No. 24 of 1972 | 37 | HTML/AKN | seed |
| 5 | `act-zm-1980-014-corrupt-practice-act-1980` | Corrupt Practice Act, 1980 | Act No. 14 of 1980 | 121 | PDF | seed |
| 6 | `act-zm-1995-010-tanzania-zambia-railway-act-1995` | Tanzania-Zambia Railway Act, 1995 | Act No. 10 of 1995 | 104 | HTML/AKN | probe |
| 7 | `act-zm-1957-063-day-nurseries-act-1957` | Day Nurseries Act, 1957 | Act No. 63 of 1957 | 14 | HTML/AKN | probe |
| 8 | `act-zm-1952-009-savings-certificates-act-1952` | Savings Certificates Act, 1952 | Act No. 9 of 1952 | 14 | HTML/AKN | probe |

**Total sections:** 328

## Repeal-chain links

No new repeal-chain links applied this batch — deferred until the Insurance Act Cap. 392 parent is confirmed.

## Seed summary

- Seed candidates queued: 5
- Seed candidates committed: 5
- Seed candidates gapped: 0

## Probe summary

- Probe queries issued: 6 ('sale of goods', 'bills of exchange', 'juveniles act', 'hire purchase', 'stamp duty', 'insurance act 1997')
- Candidates discovered (novel): 17
- Candidates surviving HEAD + title filters: 9
- Candidates processed this batch: 3

## Integrity checks
- CHECK 1 (batch unique IDs): PASS
- CHECK 2 (no HEAD collision): PASS
- CHECK 3 (source_hash matches raw on disk): PASS
- CHECK 4 (amended_by / repealed_by reference resolution): PASS — no new cross-references introduced this batch
- CHECK 5 (required fields present): PASS

## Raw snapshots

All raw bytes saved to `raw/zambialii/<year>/<id>.{html|pdf}`. B2 sync deferred to host (rclone not available in sandbox).

## Gaps / skipped targets

- 1963/65 "Workers' Compensation Act, 1963": batch cap reached (MAX_RECORDS=8) — deferred
- 2003/13 'National Council for Construction Act, 2003': batch cap reached (MAX_RECORDS=8) — deferred
- 1954/12 'Control of Goods Act , 1954': batch cap reached (MAX_RECORDS=8) — deferred
- 1995/4 'Value Added Tax Act , 1995': batch cap reached (MAX_RECORDS=8) — deferred
- 1995/31 'Mines and Minerals Act , 1995': batch cap reached (MAX_RECORDS=8) — deferred
- 1996/28 'Pension Scheme Regulation Act , 1996': batch cap reached (MAX_RECORDS=8) — deferred
- 1990/32 'Stamp Duty (Amendment) Act, 1990': pre-fetch reject — title contains 'amendment' (via query 'bills of exchange')
- 2011/3 'Juveniles (Amendment) Act , 2011': pre-fetch reject — title contains 'amendment' (via query 'juveniles act')
- 1999/12 'Environment Protection and Pollution Control (Amendment) Act, 1999': pre-fetch reject — title contains 'amendment' (via query 'hire purchase')
- 1994/17 'Stamp Duty (Repeal) Act, 1994': pre-fetch reject — title contains 'repeal' (via query 'stamp duty')
- 1992/8 'Stamp Duty (Amendment) Act, 1992': pre-fetch reject — title contains 'amendment' (via query 'stamp duty')
- 1984/3 'Stamp Duty (Amendment) Act, 1984': pre-fetch reject — title contains 'amendment' (via query 'stamp duty')
- 2005/26 'Insurance (Amendment) Act , 2005': pre-fetch reject — title contains 'amendment' (via query 'insurance act 1997')
- 1997/7 'Control of Goods (Amendment) Act , 1997': pre-fetch reject — title contains 'amendment' (via query 'insurance act 1997')

## Notes

- Seed candidates are primary statutes that batch 0151/0152 title-filtered in prior probes and verified as not-in-HEAD by (year, number) tuple lookup; no re-probe was required.
- B-POL-ACT-1 title filter applied pre-write for probe-stage candidates: any slot whose AKN-page title contained an amendment-style token was rejected without raw or record file.
- Next tick: depending on seed outcomes, continue the primary-statute sweep — Juveniles Act parent (Cap. 53), Hire Purchase Act parent, Stamp Duty parent, Sale of Goods parent, Bills of Exchange parent, Insurance Cap. 392 parent (if not surfaced by this probe); also Patents Cap. 400 and Copyright Cap. 406 parents remain unresolved by batches 0146 and 0152 probes.

