# Phase 4 Batch 0246 — drain year=2022 p1 residuals + year=2021 p1 novel

**Tick start:** 2026-04-26T01:06:26Z (robots reverify)
**Phase:** 4 (bulk ingest, approved=true, complete=false)
**Batch number:** 0246 (predecessor 0245)
**MAX_BATCH_SIZE:** 8 — committed 8 records.

## Discovery

| Probe | Result |
|---|---|
| `subsidiary?years=2022&page=2` | HTTP 404 — year=2022 listing exhausted at p1 |
| `subsidiary?years=2021&page=2` | HTTP 404 — year=2021 listing exhausted at p1 |
| `subsidiary?years=2021&page=1` | HTTP 200, 152,595 bytes, 47 unique SI links, 7 novel after corpus filter |
| `robots.txt` re-verify | sha256 prefix `fce67b697ee4ef44` unchanged from batches 0193–0245 |

Total discovery cost: **4 fetches** (1 robots + 3 listing probes).

## Picks (8)

| # | yr/num | Title | Sub-phase |
|---|---|---|---|
| 1 | 2022/17 | Customs and Excise (Electronic Machinery and Equipment) (Suspension) (Amendment) Regulations, 2022 | sis_tax |
| 2 | 2022/20 | Public Holidays (Declaration) Notice, 2022 | sis_governance |
| 3 | 2022/36 | Customs and Excise (Ports of Entry and Routes) (Amendment) Order, 2022 | sis_tax |
| 4 | 2022/46 | Customs and Excise (Machinery and Equipment) (Suspension) (Amendment) Regulations, 2022 | sis_tax |
| 5 | 2021/52 | Cyber Security and Cyber Crimes (National Cyber Security, Advisory and Coordination Council) Regulations, 2021 | **sis_data_protection FIRST** |
| 6 | 2021/60 | Zambia Development Agency (Jiangxi Multi-Facility Economic Zone) (Declaration) Order, 2021 | sis_industry |
| 7 | 2021/62 | Customs and Excise (Ports of Entry and Routes) (Amendment) Order, 2021 | sis_tax |
| 8 | 2021/73 | Public Holidays (Declaration) (No. 4) Notice, 2021 | sis_governance |

## Ingest results

| # | yr/num | Status | Pages | Chars |
|---|---|---|---|---|
| 0 | 2022/17 | ok | 2 | 1,653 |
| 1 | 2022/20 | ok | 2 | 896 |
| 2 | 2022/36 | ok | 2 | 1,032 |
| 3 | 2022/46 | ok | 2 | 1,095 |
| 4 | 2021/52 | ok | 6 | 8,732 |
| 5 | 2021/60 | ok | 4 | 3,366 |
| 6 | 2021/62 | ok | 2 | 2,516 |
| 7 | 2021/73 | ok | 2 | 879 |

**Yield: 8/8 = 100 %.** Per-record cost: 16 fresh fetches (8 HTML + 8 PDF). Tick total fetches: ~20.

## Sub-phase footprint

- **sis_data_protection FIRST cluster** (priority_order item 6 advanced from 0 to 1) — Cyber Security and Cyber Crimes Act parent-Act linkage. The 6-page 2021/52 SI establishes the National Cyber Security, Advisory and Coordination Council under Cyber Security and Cyber Crimes Act 2 of 2021.
- sis_tax +4 — Customs and Excise Act suspension/amendment chain (continues priority_order item 3 from batch 0245).
- sis_governance +2 — Public Holidays Act declarations.
- sis_industry +1 — Zambia Development Agency Act MFEZ declaration.

## Cumulative footprint

- SI records before tick: 543 (per batch 0245 close-out).
- SI records after tick: 551 (+8).
- 4th consecutive tick to advance a brand-new priority sub-phase from zero (0243 sis_corporate → 0244 sis_industry → 0245 sis_tax+sis_mining → 0246 **sis_data_protection**).
- priority_order items advanced from 0: items 2, 3, 6, 7. Outstanding from 0: item 1 (acts_in_force), item 4 (sis_employment, 1 record only via cross-ingest), item 5 (case_law_scz, paused per robots), item 8 (sis_family).

## Integrity (all checks)

| Check | Result |
|---|---|
| 1a — batch unique ids | PASS (8/8 unique) |
| 1b — corpus presence on disk | PASS (8/8 found) |
| 2 — amended_by refs resolve | PASS (0 refs) |
| 3 — repealed_by refs resolve | PASS (0 refs) |
| 4 — source_hash sha256 matches on-disk raw | PASS (8/8 verified) |
| 5 — required fields present | PASS (10 fields × 8 records all present) |
| 6 — cited_authorities refs resolve | PASS (0 refs) |

**ALL PASS.**

## Robots.txt compliance

- UA: `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)`.
- robots-declared crawl-delay 5 s honoured at 6 s margin per fetch.
- Disallow on `/akn/zm/judgment/` and `/akn/zm/officialGazette/` enforced — case_law_scz remains paused.

## Budgets

- Today fetches at tick start: 44/2000.
- Tick fetches: 20 (1 robots + 3 listing + 16 ingest).
- Today fetches at tick end: ~64/2000 (3.2 % of daily budget).
- Tokens: well within 1 M/day budget.

## Next-tick plan

1. Probe year=2020 listings (year=2021 and year=2022 single-page exhausted).
2. Drain remaining year=2021 p1 novels (3 unused: 2021/72, 2021/71, 2021/69 — Public Holidays declarations).
3. Re-probe year=2024 deeper pages (p1=0/p2=0/p3=13novel/p4=404 — p3 was last productive).
4. Rotate to **acts_in_force** priority_order item 1 — separate Acts-listing endpoint discovery path.
5. OCR retry on backlog (still 14 items: 2017/068 + 2018/011 + 2018/075 + 2018/093 + 2020/007 + 2022/002 + 2022/003 + 2022/004 + 2022/007 + 2022/008 + 2022/012 + 2022/013 + 2025/020 + 2026/004) once tesseract is wired.

## Infrastructure status

- B2 sync deferred to host (rclone unavailable in sandbox). Peter to run `rclone sync raw/ b2raw:kwlp-corpus-raw/ --fast-list --transfers 4`.
- corpus.sqlite stale rollback-journal still blocks in-sandbox FTS rebuild — JSON records authoritative; sqlite rebuild deferred to host.
- Persistent virtiofs unlink-failure warnings non-fatal — workaround stable across batches 0192–0246 (`GIT_INDEX_FILE` bypass + `git update-ref` + `setsid` push).
- 488+ pre-existing untracked `records/sis` + `records/acts` files unchanged this tick — long-standing infrastructure backlog (queued for future reconciliation tick).
