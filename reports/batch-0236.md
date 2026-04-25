# Batch 0236 Report — Phase 4 sis_elections E-residual drain (cohort 2)

**Tick:** 2026-04-25T20:11:28Z
**Phase:** phase_4_bulk (approved+incomplete)
**Sub-phase:** sis_elections (drain — 0 first-instance sub-phases this tick)
**Cumulative SI records after batch:** 474 (+8 over batch-0235's 466)
**Yield:** 8/8 = 100.0%

## Records ingested (8/8)

  - **2022/061** — Electoral Process (Local Government By-Elections) (Election Date and Time of Poll) (No. 2) Order, 2022
    * id: `si-zm-2022-061-electoral-process-local-government-by-elections-election-date-and-time-of-poll-no-2-order-2022`
    * sha256: `91d14bd466396dbb...`
    * pdf: 2pp / 2,411 chars
    * effective: 2022-09-30

  - **2021/087** — National Assembly By-Election (Kabwata Constituency No. 77) (Election Date and Time of Poll) (No. 3) Order, 2021
    * id: `si-zm-2021-087-national-assembly-by-election-kabwata-constituency-no-77-election-date-and-time-of-poll-no-3-order-2021`
    * sha256: `fa412291573c5f3b...`
    * pdf: 2pp / 2,288 chars
    * effective: 2021-12-17

  - **2021/075** — Electoral Process (Local Government Elections) (Election Date and Time of Poll) Order, 2021
    * id: `si-zm-2021-075-electoral-process-local-government-elections-election-date-and-time-of-poll-order-2021`
    * sha256: `f043ef1a8fc1b59d...`
    * pdf: 2pp / 2,039 chars
    * effective: 2021-09-10

  - **2021/074** — National Assembly (Kaumbwe Constituency No. 50) (Election Date and Time of Poll) Order, 2021
    * id: `si-zm-2021-074-national-assembly-kaumbwe-constituency-no-50-election-date-and-time-of-poll-order-2021`
    * sha256: `c941e5dab892f2d8...`
    * pdf: 2pp / 2,142 chars
    * effective: 2021-09-10

  - **2020/101** — Electoral Process (Local Government By-Elections) (Election Date and Time of Poll) (No. 8 ) Order, 2020
    * id: `si-zm-2020-101-electoral-process-local-government-by-elections-election-date-and-time-of-poll-no-8-order-2020`
    * sha256: `559bdca27be0d0b4...`
    * pdf: 2pp / 1,922 chars
    * effective: 2020-12-11

  - **2020/079** — Electoral Process (Local Government By-Elections) (Election Date and Time of Poll) (No. 8 ) Order, 2020
    * id: `si-zm-2020-079-electoral-process-local-government-by-elections-election-date-and-time-of-poll-no-8-order-2020`
    * sha256: `74031befe8a0760c...`
    * pdf: 2pp / 1,816 chars
    * effective: 2020-09-25

  - **2020/072** — Electoral Process (Local Government By-Elections) (Election Date and Time of Poll) (No. 7 ) Order, 2020
    * id: `si-zm-2020-072-electoral-process-local-government-by-elections-election-date-and-time-of-poll-no-7-order-2020`
    * sha256: `4c3ddf4df0aab5e9...`
    * pdf: 2pp / 2,041 chars
    * effective: 2020-08-21

  - **2020/071** — National Assembly By-Election (Mwansabombwe Constituency No. 65 and Lukashya Constituency No. 98) (Election Date and Time Poll) Order, 2020
    * id: `si-zm-2020-071-national-assembly-by-election-mwansabombwe-constituency-no-65-and-lukashya-constituency-no-98-election-date-and-time-pol`
    * sha256: `df06a61d4f620b7b...`
    * pdf: 2pp / 2,294 chars
    * effective: 2020-08-21

## Discovery & cost
- Fresh discovery fetches: 1 (robots.txt re-verify; sha256 prefix `fce67b697ee4ef44` unchanged from batches 0193-0235)
- Cache reuse: batch_0233 E-probe — 47 novel candidates remaining at tick start, drained by 8.
- E residuals after this tick: ~39 (47 - 8 ingested in 0236)
- Per-record fetches: 16 (8 HTML + 8 PDF, 16 total)
- Today fetches: ~614/2000 (~30.7%); tokens within budget.

## Integrity
- CHECK1a (batch unique IDs): PASS 8/8
- CHECK1b (corpus presence on disk): PASS 8/8
- CHECK2/3 (amended_by + repealed_by refs): PASS 0 refs
- CHECK4 (source_hash sha256 verified against raw PDF): PASS 8/8
- CHECK5 (required fields x 8 records): PASS 8/8
- CHECK6 (cited_authorities refs): PASS 0 refs
- **OVERALL: ALL PASS**

## Robots.txt
- Re-verified at tick start: sha256 prefix `fce67b697ee4ef44` (unchanged)
- Crawl-delay 5s honoured at 6s margin (CRAWL=6.0)
- Disallow on `/akn/zm/judgment/` + `/akn/zm/officialGazette/` enforced

## Next-tick plan
- Continue draining E residuals (~39 left from batch-0233 cache): 2020 cohort + 2023/8 + 2023/36 + 2023/40 + 2023/46 + 2024/2 + 2024/6 + 2024/15 + 2019 cohort + others
- OR rotate to acts_in_force priority_order item 1 (requires Acts-listing endpoint discovery)
- OR re-attempt OCR backlog (6 items: 2017/068, 2018/011, 2022/004, 2022/007, 2022/008, 2022/012)
- OR fresh alphabet re-probes (G/H/K/P unprobed since earlier ticks)

## Infrastructure follow-up (non-blocking)
- batch-0236 raw files (16 = 8 HTML + 8 PDF + 1 robots ~700KB total) plus accumulated batches 0192-0235 raw files awaiting host-driven B2 sync (rclone unavailable in sandbox)
- corpus.sqlite stale rollback-journal still blocks in-sandbox FTS rebuild (deferred to host)
- persistent virtiofs unlink-failure warnings non-fatal (workaround stable: write-tree/commit-tree/update-ref/push direct)
- 488+ pre-existing untracked records files (carryover from prior ticks)
- OCR backlog at 6 items (unchanged this tick)
- worker recovered tick-start from stale-lock + diverged worker.log via update-ref refs/heads/main 5751b33 (sync to origin/main HEAD); no fresh divergence introduced

Phase 4 remains approved+incomplete; worker exits cleanly.
