# Batch 0229 Report

**Phase:** 4 (bulk ingestion)
**Tick start:** 2026-04-25T16:02:00Z
**Tick end:** ~2026-04-25T16:18:00Z
**Mode:** Fresh U-alphabet probe — Urban and Regional Planning Act cluster
**Yield:** 8/8 (100%) — sixth consecutive 100%-yield batch

## Records ingested (8)

| #  | Year/Num | Title | Pages | Chars  | Sub-phase | Parent Act |
|----|----------|-------|-------|--------|-----------|------------|
| 1  | 2017/060 | Urban and Regional Planning (Designated Local Planning Authorities) Regulations, 2017 | 2 | 1,796 | sis_planning | Urban and Regional Planning Act |
| 2  | 2018/043 | Urban and Regional Planning (Designated Local Planning Authorities) Regulations, 2018 | 2 | 1,109 | sis_planning | Urban and Regional Planning Act |
| 3  | 2019/042 | Urban and Regional Planning (Designated Local Planning Authorities) Regulations, 2019 | 2 | 1,013 | sis_planning | Urban and Regional Planning Act |
| 4  | 2020/005 | Urban and Regional Planning (Designated Local Planning Authority) Regulations, 2020 | 2 | 1,013 | sis_planning | Urban and Regional Planning Act |
| 5  | 2020/056 | Urban and Regional Planning (General) Regulations, 2020 | **60** | **96,478** | sis_planning | Urban and Regional Planning Act |
| 6  | 2022/057 | Urban and Regional Planning (Designated Local Planning Authorities) Regulations, 2022 | 2 | 1,075 | sis_planning | Urban and Regional Planning Act |
| 7  | 2023/021 | Urban and Regional Planning (Development Plans Guidelines and Exempted Development Classes) Regulations, 2023 | **74** | **128,910** | sis_planning | Urban and Regional Planning Act |
| 8  | 2025/065 | Urban and Regional Planning (Administration of Planning Appeals Tribunal) Regulations, 2025 | 12 | 51,493 | sis_planning | Urban and Regional Planning Act |

## Footprint

- **FIRST `sis_planning` records in corpus history** — 8-record cluster under the Urban and Regional Planning Act (Act No. 3 of 2015).
- 3 substantive Regulations: 2020/056 General Regs (60pp), 2023/021 Development Plans Guidelines (74pp — largest in batch by chars), 2025/065 Tribunal (12pp).
- 5 short DLPA (Designated Local Planning Authorities) declaration orders (2pp each, 1,013–1,796 chars) covering years 2017, 2018, 2019, 2020, 2022.

## Discovery cost

- 1 robots.txt re-verify — sha256 prefix `fce67b697ee4ef44` unchanged from batches 0193–0228.
- 1 alphabet=U probe (76,158 bytes) — surfaced 19 novel modern (≥2017) U candidates, all under URP Act. 8 picked, 11 reserved for future ticks.
- 16 per-record fetches (8 HTML + 8 PDF, 0 reused).

## Today fetches

498/2000 (24.9%) — all on zambialii.org under robots-declared 5s crawl-delay using 6s margin. Tokens within budget.

## Integrity

| Check | Result |
|---|---|
| CHECK1a (batch unique IDs)             | PASS (8/8) |
| CHECK1b (corpus presence on disk)      | PASS (8/8) |
| CHECK2/3 (amended_by/repealed_by refs) | PASS (0 refs) |
| CHECK4 (source_hash matches raw)       | PASS (8/8) |
| CHECK5 (required fields × 8 records)   | PASS (10×8 = 80) |
| CHECK6 (cited_authorities refs)        | PASS (0 refs) |

## MAX_BATCH_SIZE

8 records committed (= 8 cap). Cap honoured.

## Cumulative

SI records after this batch: **426** (+8 over batch-0228's 418). Judgments: 25 (paused per robots Disallow on `/akn/zm/judgment/`).

## Reserves for next tick

11 U-alphabet candidates remain unused (all DLPA short orders): 2019/043, 2019/045, 2019/078, 2018/044, 2017/064, 2020/009, 2020/055, 2020/108, 2022/060, 2023/009, 2023/045.

## Next-tick options

(a) Drain 11 U-alphabet residuals (DLPA declaration orders — expected 100% yield based on this cohort).
(b) Fresh probes from X/Y/Z (other unprobed alphabets per close-out plan).
(c) Re-probe earlier alphabets M/A/D/E for candidates not picked previously.
(d) Rotate to acts_in_force priority_order item 1.
(e) OCR backlog from batches 0225/0226 (5 items: 2017/068, 2018/011, 2022/004, 2022/007, 2022/012).

## Infrastructure

- B2 sync deferred to host (rclone unavailable in sandbox).
- Persistent virtiofs unlink-failure warnings non-fatal — workaround stable across batches 0192–0228 using `GIT_INDEX_FILE` + `git read-tree origin/main` + `git update-ref` + `push origin <sha>:refs/heads/main`.
- Tick-start git pull --ff-only failed due to staged-deletion noise from prior aborted local tick — resolved via `git update-ref HEAD origin/main` bypass with refreshed worker.log from origin.

## Parser version

`0.5.0`

## User-Agent

`KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)`
