# Phase 4 Batch 0247

**Tick started:** 2026-04-26T01:32:52Z
**Yield:** 8/8 ok (100%)
**Cumulative SI records:** 559 (+8 over batch 0246's 551)

## Records ingested

| # | ID | Sub-phase | Parent Act | Chars |
|---|---|---|---|---|
| 1 | si-zm-2021-072-public-holidays-declaration-no-3-notice-2021 | sis_governance | Public Holidays Act | 942 |
| 2 | si-zm-2021-071-public-holidays-declaration-no-2-notice-2021 | sis_governance | Public Holidays Act | 844 |
| 3 | si-zm-2021-069-public-holidays-declaration-notice-2021 | sis_governance | Public Holidays Act | 992 |
| 4 | si-zm-2020-097-public-finance-management-general-regulations-2020 | sis_governance | Public Finance Management Act | 172,695 |
| 5 | si-zm-2016-063-electoral-process-general-regulations-2016 | sis_governance | Electoral Process Act | 91,068 |
| 6 | si-zm-2016-062-electoral-process-code-of-conduct-enforcement-regulations-2016 | sis_governance | Electoral Process Act | 3,949 |
| 7 | si-zm-2016-070-electoral-process-local-government-elections-election-dates-and-times-of-poll-order-2016 | sis_governance | Electoral Process Act | 2,208 |
| 8 | si-zm-2016-049-national-prosecutions-authority-witness-allowances-and-expenses-regulations-2016 | sis_judicial | National Prosecutions Authority Act | 3,771 |

## Sub-phase footprint
- sis_governance +7 (Public Holidays Act +3 historic 2021 declarations + Public Finance Management Act 2020/97 + Electoral Process Act FIRST cluster +3)
- sis_judicial +1 (National Prosecutions Authority 2016/49)

**FIRST sis_electoral cluster** (Electoral Process Act parent — 3 records: General Regs + Code of Conduct Enforcement + LG Elections Dates/Times Order). 5th consecutive tick to expand a brand-new sub-phase footprint within sis_governance.

## Discovery cost
- 1 robots.txt re-verify (sha256 prefix fce67b697ee4ef44 unchanged from batches 0193-0246; 5s crawl-delay honoured at 6s margin; Disallow on /akn/zm/judgment/ + /akn/zm/officialGazette/ enforced)
- 8 listing probes: year=2020 p1 (16/1 novel), year=2020 p2 (404), year=2019 p1 (21/2 novel both on OCR backlog), year=2018 p1 (4/0), year=2017 p1 (7/0), alphabet=E (85/8 novel), alphabet=N (60/13 novel), year=2023 p1 (4/0)
- Total discovery fetches: 9 (1 robots + 8 listings)
- Per-record fetches: 16 (8 HTML + 8 PDF)

## Integrity
- CHECK1a: PASS — 8/8 batch unique IDs
- CHECK1b: PASS — 8/8 corpus presence on disk
- CHECK2: PASS — 0 amended_by refs
- CHECK3: PASS — 0 repealed_by refs
- CHECK4: PASS — sha256 verified 8/8 against raw/zambialii/si/(2016,2020,2021)/
- CHECK5: PASS — 10 required fields x 8 records all present
- CHECK6: PASS — 0 cited_authorities refs

## Budget
- Today fetches: 49 (pre-tick) + 25 (this tick: 1 robots + 8 listings + 16 records) = ~74/2000 (3.7% of daily budget)
- Tokens: within budget
- All fetches on zambialii.org, robots-declared 5s crawl-delay honoured at 6s margin

## Reserved residuals (carry to next tick)
- alphabet=E: 5 unused novels (1988/38 Emergency Essential Supplies, 1993/37 Emergency Regs, 1987/29 + 1985/14 Equity Levy Exemption, 2016/3 Estate Agents General Regs)
- alphabet=N: 12 unused novels (1995/29 + 1995/30 + 1986/32 National Archives, 2008/24 NCC Conf Committees, 2004/22 + 2009/37 + 2015/39 NCC, 2015/89 + 2016/59 National Museums, 2008/16 + 2005/19 National Road Fund, 1987/36 National Savings)

## OCR backlog
Unchanged at 14 items: 2017/068 + 2018/011 + 2018/075 + 2018/093 + 2020/007 + 2022/002 + 2022/003 + 2022/004 + 2022/007 + 2022/008 + 2022/012 + 2022/013 + 2025/020 + 2026/004.

## Next-tick plan
1. Drain reserved residuals (17 candidates total: 5 alphabet=E + 12 alphabet=N) — should yield 1-2 batches without fresh discovery
2. Probe additional alphabets (untested: A, B, C, D, F, H, I, J, L, M, P, S, T, V, W)
3. Rotate to acts_in_force priority_order item 1 — needs Acts-listing endpoint discovery
4. OCR retry on backlog (still 14 items) once tesseract is wired

## Infrastructure follow-up (non-blocking)
- batch-0247 raw files awaiting host-driven B2 sync (rclone unavailable in sandbox)
- corpus.sqlite stale rollback-journal still blocks in-sandbox FTS rebuild (deferred to host)
- persistent virtiofs unlink-failure warnings non-fatal (workaround stable across batches 0192-0247)
