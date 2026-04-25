# Batch 0214 — Phase 4 (Bulk Ingest, Mixed sub_phase rotation)

**Started:** 2026-04-25T05:01:00Z
**Completed:** 2026-04-25T05:14Z (approx)
**Records written:** 8 (3 sis_corporate + 1 sis_employment + 2 sis_courts + 1 sis_corporate/AML + 1 sis_environment)
**Targets attempted:** 8 (0 failures)
**Yield:** 8/8 = 100%
**Daily fetches used:** ~234/2000 (11.7%)
**Robots.txt SHA256 prefix:** fce67b697ee4ef44 (unchanged from batches 0193-0213)

## Records added

| # | ID | Sub-phase | Parent Act |
|---|----|-----------|------------|
| 1 | si-zm-2025-019-investmenttrade-and-business-development-fintech-city-multi-facility-economic-zo | sis_corporate | Investment, Trade and Business Development Act 2022/18 (Multi-Facility Economic Zones) |
| 2 | si-zm-2024-004-investment-trade-and-business-development-luano-industrial-park-declaration-orde | sis_corporate | Investment, Trade and Business Development Act 2022/18 (industrial park declaration) |
| 3 | si-zm-2023-013-forfeiture-of-proceeds-of-crime-fund-and-property-management-regulations-2023 | sis_corporate | Forfeiture of Proceeds of Crime Act 2010/19 (AML/CFT — FIA-aligned) |
| 4 | si-zm-2022-015-ministerial-and-parliamentary-offices-emoluments-amendment-regulations-2022 | sis_employment | Ministerial and Parliamentary Offices (Emoluments) Act |
| 5 | si-zm-2021-061-protection-of-traditional-knowledge-genetic-resources-and-expressions-of-folklor | sis_corporate | Protection of Traditional Knowledge, Genetic Resources and Expressions of Folklore Act 2016/16 (IP) |
| 6 | si-zm-2024-012-subordinate-courts-civil-jurisdiction-rules-2024 | sis_courts | Subordinate Courts Act Cap. 28 (civil jurisdiction limit) |
| 7 | si-zm-2023-020-small-claims-court-limit-of-jurisdiction-liquidated-claims-rules-2023 | sis_courts | Small Claims Courts Act Cap. 47 (liquidated-claims limit) |
| 8 | si-zm-2021-048-environmental-management-strategic-environmental-assessment-regulations-2021 | sis_environment | Environmental Management Act 2011/12 (SEA — sis_mining adjacent) |

## Sub-phase rotation rationale

Per batch-0213 next-tick plan, this tick was scheduled to continue sis_tax with parent-Act-driven probes for 1970s ITA exemption ranges, plus alphabet=N (NAPSA, NHIMA), R (Refugees, Road Traffic) probes — and rotate to sis_employment if sis_tax yield <3 (per the 2-consecutive-tick rule; batch 0213 was the 1st low-yield tick at 1/5).

Discovery this tick:
- **Phase A (sis_employment first attempt):** alphabets E, L, N, O, M (5 alphabets, robots-reverify + 5 fetches) — yielded 153 novel pre-keyword slots but only **1 post-keyword candidate** (2022/013 minimum-wages truck-and-bus drivers — already a recurring image-only PDF fail). All 153 novel slots inspected; none cleanly fit the sis_employment keyword set.
- **Phase A2 (sis_employment broader):** added alphabets I, P, S, A, F, W (6 fetches) — 83 additional novel slots, **0 post-keyword candidates**.
- **Conclusion:** sis_employment is at exhaustion across 11 alphabets (E/L/N/O/M/I/P/S/A/F/W); only candidates are the recurring image-only PDFs (2022/013 minimum-wages, 2017/051 health-research) which require OCR backfill (deferred). Per the 2-consecutive-tick rule (batch 0213 sis_tax: 1/5; batch 0214 sis_employment: 0/0 clean), next tick should rotate to sis_data_protection (priority_order item 6) or sis_mining (item 7).

Per the proven cross-sub_phase rotation pattern from batches 0211–0213, the worker performed parallel cross-sub_phase discovery using the cached alphabet HTML (no additional fetches). That produced 8 high-quality curated candidates from sis_corporate (4: investment-MFEZ/industrial-park/forfeiture-of-proceeds/IP), sis_employment (1: ministerial emoluments), sis_courts (2: subordinate courts + small-claims court), and sis_environment (1: SEA regulations under EMA 2011/12, sis_mining adjacent).

## Sub-phase exhaustion observations (informational, for next tick planning)

- **sis_employment**: tight-keyword sweep across alphabets E/L/N/O/M/I/P/S/A/F/W returned only 1 novel candidate (2022/013, recurring image-only PDF fail). No clean alternate Employment Code Act / NAPSA / NHIMA / Workers' Compensation / Factories / Apprenticeship / Pneumoconiosis / Skills Development SI surfaces remain. Existing HEAD coverage: 2020/048 (Employment Code exemption), 2020/106 (truck-and-bus minimum wages), 2023/048-050 (Employment Code minimum-wages general/domestic/shop workers), 2019/063 (NHIMA general), 2019/072 (NAPSA informal sector), 2020/105 (service commissions LGSC) — covering the principal Employment Code Act 2019/3 derivative regime.
- **sis_tax**: see batch 0213 — also at exhaustion modulo OCR backfill.
- **sis_corporate**: cross-sub_phase rotation found 4 high-quality novel candidates this tick (2025/019 + 2024/004 + 2023/013 + 2021/061), all with parent Acts that align with the priority_order. Suggests sis_corporate has remaining depth via parent-Act-driven probes (Investment Trade and Business Development Act 2022/18, Forfeiture of Proceeds of Crime Act 2010/19, Protection of Traditional Knowledge Act 2016/16). Recommend rotating fully to sis_corporate next tick.
- **sis_courts**: 2 novel candidates this tick (2024/012 + 2023/020). Subordinate Courts Act + Small Claims Courts Act jurisdiction-limit rules form a coherent procedural sub-phase that complements existing 2024/010 (Economic and Financial Crimes Court rules). Useful extension target.
- **sis_environment / sis_mining**: 1 candidate this tick (2021/048 SEA regulations under EMA 2011/12). EMA-derivative SI universe is broad — SEA, EIA (2026/003 visible in alphabet), forest carbon stock (2021/066), forest reserve cessation/alteration (2021/001-003 + 2020/012-013) — recommend dedicated sis_mining tick.
- **sis_data_protection**: not probed this tick. Existing coverage: 2025/056 (Access to Information General), 2021/058 (DPA registration & licensing). May benefit from full alphabet sweep.

## Integrity checks

- CHECK1 (id uniqueness): batch ids=8, unique=8, prior collisions=0 — PASS
- CHECK1b (id uniqueness corpus-wide): 309 SI records, all unique — PASS
- CHECK2 (amended_by/repealed_by resolve): no cross-references emitted by parser — PASS (vacuous)
- CHECK3 (cited_authorities resolve): no citations emitted — PASS (vacuous)
- CHECK4 (source_hash matches on-disk): 8/8 verified — PASS
- CHECK5 (required fields): 8/8 records have id/type/jurisdiction/title/citation/sections/source_url/source_hash/fetched_at/parser_version — PASS

**ALL CHECKS PASS.**

## Provenance summary

- **Robots.txt re-verified once** at tick start (sha256=fce67b697ee4ef44e0694134e23108c2701b5e7661eed885013efb9b75dcd8f0, prefix unchanged across batches 0193–0214).
- **Crawl-delay margin:** 6 s (margin over the robots-declared 5 s zambialii crawl-delay).
- **User-Agent:** `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)` — per approvals.yaml.
- **Daily fetch budget:** ~234/2000 (11.7%); well under 50 % usage. Tokens within budget.
- **Sources fetched this tick:** 1 commons.laws.africa (2023/020 PDF — zambialii redirected) + the rest on zambialii.org. All under the documented per-domain rate limit.
- **B2 raw sync:** rclone unavailable in sandbox; deferred to host (`rclone sync raw/ b2raw:kwlp-corpus-raw/ --fast-list --transfers 4`).

## Cumulative corpus state after this batch

- **Acts:** 1116 records (unchanged this tick)
- **Statutory Instruments:** 309 records (+8 over batch 0213's 301)
- **Judgments:** 25 records (unchanged — case_law_scz remains paused per robots.txt Disallow on `/akn/zm/judgment/`)
- **Total:** 1450 records (+8 over 1442)

## Next-tick plan

Primary: **rotate to sis_data_protection** (priority_order item 6) since sis_employment is at exhaustion (this tick) and sis_tax is at exhaustion (batch 0213). Probe alphabets D (Data Protection / DPA), A (Access to Information), C (Cyber Security and Cyber Crimes), E (Electronic Communications and Transactions), I (Information and Communication Technologies / Internet Service Provider), R (Records / Registration), and pick up parent-Act-driven probes: DPA 2021/3 derivatives, Access to Information Act 2023/26 derivatives (besides 2025/056 General Regs already in HEAD), Electronic Communications and Transactions Act 2021/4 derivatives, Cyber Security and Cyber Crimes Act 2021/2 derivatives (besides 2021/052 Council Regs already in HEAD), ICT Act 2009/15 derivatives.

Fallback if sis_data_protection yield <3: rotate to **sis_mining** (priority_order item 7) with EMA-derivative probes (EIA 2026/003, Forest carbon stock 2021/066, NHCC monument-declaration series 2023/026-035) plus parent-Act-driven probes for Mines and Minerals Development Act 2015/11, Petroleum (Exploration and Production) Act, National Heritage Conservation Commission Act.

Cross-sub_phase fill remains the established pattern: sis_corporate (Investment Act 2022/18 derivatives appear deep), sis_courts (Subordinate Courts / Small Claims / Industrial Relations Court rules), sis_family (Wills and Administration of Testate Estates derivatives, Marriage Act).

Re-verify robots.txt at start of next tick.

## Infrastructure follow-up (non-blocking)

- 16 batch-0214 raw SI files on disk (8 HTML + 8 PDF, ~2.1 MB) plus accumulated batches 0192–0213 raw files awaiting host-driven B2 sync (rclone unavailable in sandbox).
- corpus.sqlite stale rollback-journal still blocks in-sandbox FTS rebuild (disk I/O error on read).
- Persistent virtiofs unlink-failure warnings on `.git/objects/maintenance.lock` (workaround stable across batches 0192–0214: `find .git -name "*.lock" -delete` at tick start, GIT_INDEX_FILE for stage/commit).
- Sandbox-bash 45 s call cap forced ingest into 4 invocations (slice 1_4 + slice 4_7 + slice 7_9 + finalize). 8/8 ingest success rate (no slot reattempts; no PDF parse failures; no HTTP errors). 100 % yield is the highest since batch 0212.
