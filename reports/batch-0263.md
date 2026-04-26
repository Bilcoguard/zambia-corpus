# Batch 0263 — Phase 4 acts_in_force (alphabet S residuals sweep 1)

**Generated:** 2026-04-26T11:08:43Z
**Phase:** phase_4_bulk
**Sub-phase:** acts_in_force
**Source:** zambialii.org (alphabet=S re-using cached listing 20260426T103405Z)
**Records:** 8 / 8 attempted (yield 100%)

## Picks

| # | Yr/Num | Title | Sections | Path |
|---|--------|-------|----------|------|
| 1 | 1960/28 | Sheriffs Act, 1960 | 19 | records/acts/1960/act-zm-1960-028-sheriffs-act-1960.json |
| 2 | 2016/46 | Skills Development Levy Act, 2016 | 16 | records/acts/2016/act-zm-2016-046-skills-development-levy-act-2016.json |
| 3 | 1981/18 | Small Industries Development Act, 1981 | 18 | records/acts/1981/act-zm-1981-018-small-industries-development-act-1981.json |
| 4 | 2022/4 | Social Workers' Association of Zambia Act, 2022 | 47 | records/acts/2022/act-zm-2022-004-social-workers-association-of-zambia-act-2022.json |
| 5 | 2018/20 | Solid Waste Regulation and Management Act, 2018 | 128 | records/acts/2018/act-zm-2018-020-solid-waste-regulation-and-management-act-2018.json |
| 6 | 1950/47 | Specific Loan (Rhodesia Railways) Act, 1950 | 6 | records/acts/1950/act-zm-1950-047-specific-loan-rhodesia-railways-act-1950.json |
| 7 | 1988/38 | Specified Offices (Terminal Gratuities) Act, 1988 | 17 | records/acts/1988/act-zm-1988-038-specified-offices-terminal-gratuities-act-1988.json |
| 8 | 1989/9 | Specified Offices (Terminal Gratuities) Act, 1989 | 3 | records/acts/1989/act-zm-1989-009-specified-offices-terminal-gratuities-act-1989.json |

## Integrity checks (all pass)

- CHECK1a (no dup IDs in batch): 8 unique IDs.
- CHECK1b (presence on disk): 8/8.
- CHECK2 (amended_by resolves): 0 refs (all empty).
- CHECK3 (repealed_by resolves): 0 refs (all null).
- CHECK4 (source_hash matches raw): 8/8 sha256 verified against raw/zambialii/act/(1950,1960,1981,1988,1989,2016,2018,2022)/.
- CHECK5 (required fields): 16 fields × 8 records all present.
- CHECK6 (cited_authorities resolves): 0 refs (all empty).

## Discovery cost

- 1 robots.txt re-verify (sha256 prefix fce67b697ee4ef44 unchanged from batches 0193-0262).
- 0 alphabet listing fetches (re-used batch 0262's cached S listing).
- 8 record HTML fetches; no PDF fallback required - all parsed cleanly via akn-section HTML.

## Reserved residuals carried to next tick

11 S residuals: Sports Council of Zambia 1988/29 + Standardisation of Soap 1957/24 + Standards 2017/4 + State Audit Commission 2016/27 + Statistics 2018/13 + Statutory Functions 1970/43 + Stock Exchange 1990/43 + Subordinate Courts 1933/36 + Suicide 1967/1 + Superior Courts (Number of Judges) 2025/12 + Service of Process and Execution of Judgments 1956/4 (deferred — URL uses /1956/4-x/ disambiguator; flagged in gaps.md, needs special-case handler).

Prior reserved residuals still pending: 2 alphabet=C deferred (Citizens Economic Empowerment 2006/9 + Constitution of Zambia 1996/17) + 1 SI residual (1990/39 ZNPF >4.5MB OCR backlog at 15 items).

## Notes

- 1956/4 substituted with 1989/9 to maintain MAX_BATCH_SIZE=8 cap (see gaps.md).
- 100%-yield streak now extends across batches 0246-0263 (18 consecutive at 100%).
- Acts cumulative: 968 (+8 over 960). SIs unchanged at 593. Judgments paused at 25 per robots Disallow.
