# Phase 4 — Batch 0219 report

**Started:** 2026-04-25T07:55Z (UTC)
**Completed:** 2026-04-25T08:09Z (UTC)
**Sub-phase:** sis_mining (alphabet probe) → cross-sub_phase rotation to sis_health + sis_environment
**Records written:** 8/8 attempted (Yield = 100%)
**Cumulative SI records after batch:** 349 (+8 over batch-0218's 341)
**Judgment records:** 25 (case_law_scz remains paused per zambialii.org robots.txt Disallow on /akn/zm/judgment/)

## What this batch did

1. `git pull --ff-only` clean. Cleared a stale staged-deletions carryover (.batch_0215..0218 + _work/0215..0218 artefacts) using a sandbox-side `GIT_INDEX_FILE=/tmp/git_idx_b0219` reset. Files remained on disk; only the index was stale.
2. Re-verified zambialii.org robots.txt — sha256 prefix `fce67b697ee4ef44` unchanged from batches 0193-0218.
3. Probed alphabets **M, N, P, Q, G, E** (per batch-0218 next-tick plan for sis_mining: Mines and Minerals Development Act / Petroleum / Quarry / Geological / Explosives derivatives). Six probes spent 6 fetches.
4. Discovery yielded **128 novel pre-keyword candidates**, but only **1 matched the sis_mining keyword filter** — `1997/049 National Parks and Wildlife (Night Game Drives) Regulations`. That candidate was already deferred from batch 0218 cache and is sis_environment scope (NPW Act).
5. Per the batch-0218 fallback plan ("If sis_mining yield <3: rotate via cross-sub_phase fill — sis_health, sis_environment, sis_courts, sis_family"), I scanned the novel pre-keyword sample for cross-sub_phase keyword matches:
   - **sis_health: 12 candidates** (medicines & allied substances cluster + national health research cluster).
   - **sis_environment: 2 candidates** (1997/049 + 2026/005 green economy carbon market — fresh 2026 SI).
   - sis_education: 4; sis_courts/family: 0.
6. Selected 8 candidates for ingest: 6 sis_health (Medicines & Allied Substances Act 2013/3 derivatives) + 2 sis_environment.
7. Rewrote `_work/batch_0219_discovery.json` with the 8 selected candidates and a `cross_sub_phase_rotation: true` flag noting the pivot.
8. Ingested in 4 slices (slice_0_3 + slice_3_5 + slice_5_7 + slice_7_8) honouring 6s crawl delay (margin over robots-declared 5s) — 16 fetches.
9. Ran integrity checks CHECK1 / CHECK1b / CHECK2 / CHECK3 / CHECK4 (N/A) / CHECK5 — all PASS (no collisions; source_hash sha256 verified for all 8 raw PDFs).
10. Wrote 8 record JSON files under `records/sis/{1997,2016,2017,2026}/` and 16 raw HTML+PDF files under `raw/zambialii/si/{1997,2016,2017,2026}/`.

## Records written (8)

| Year/No   | Sub-phase       | Title                                                                                              | Sections | PDF bytes |
|-----------|-----------------|----------------------------------------------------------------------------------------------------|----------|-----------|
| 1997/049  | sis_environment | National Parks and Wildlife (Night Game Drives) Regulations, 1997                                  | 4        | 106,590   |
| 2026/005  | sis_environment | Green Economy and Climate Change (Carbon Market) Regulations, 2026                                 | 76       | 2,329,934 |
| 2016/010  | sis_health      | Medicines and Allied Substances (Agro-veterinary Shops) Regulations, 2016                          | 55       | 286,872   |
| 2016/011  | sis_health      | Medicines and Allied Substances (Dispensing Certificates) Regulations, 2016                        | 30       | 210,182   |
| 2016/012  | sis_health      | Medicines and Allied Substances (Health Shops) Regulations, 2016                                   | 74       | 291,144   |
| 2016/038  | sis_health      | Medicines and Allied Substances (Fees) Regulations, 2016                                           | 25       | 27,338    |
| 2017/057  | sis_health      | Medicines and Allied Substances (Importation and Exportation) Regulations, 2017                    | 58       | 564,050   |
| 2017/058  | sis_health      | Medicines and Allied Substances (Certificate of Registration) Regulations, 2017                    | 32       | 244,182   |

All 8 records carry `parser_version: "0.5.0"`, sha256 source_hash, fetched_at ISO 8601 UTC, and an alternate_sources entry pointing at the discovery HTML page.

## Highlights

- **2026/005 Green Economy and Climate Change (Carbon Market) Regulations** is a *fresh-of-the-year* SI (gazetted Jan 2026) — Zambia's first dedicated carbon-market subsidiary legislation under the Green Economy and Climate Change Act. 76 sections parsed; the largest single record this tick (2.3 MB PDF). Material for client advisory work on emissions trading.
- **Medicines & Allied Substances cluster (Act No. 3 of 2013)** — six core regulations under one parent Act: agro-veterinary shops, dispensing certificates, health shops, fees, importation/exportation, and certificate of registration. Together these cover most ZAMRA licensing pathways relevant to KWLP pharma/healthcare clients.
- **1997/049 NPW (Night Game Drives) Regulations** — long-deferred candidate from batch-0218 cache; closes a small gap in the National Parks and Wildlife Act derivative SIs. Useful for tourism-operator advisory work.

## Budgets

- **Today's fetches:** 339 / 2,000 (16.95%) — well under cap. All on zambialii.org under the robots-declared 5s crawl-delay using a 6s safety margin.
- **Today's tokens:** within budget (no LLM calls; pdfplumber parsing + sha256 hashing only).
- **Per-batch fetches:** 23 (1 robots reverify + 6 alphabet probes + 16 ingest URL/PDF pairs).

## Integrity checks

| Check | Description                                                  | Result                       |
|-------|--------------------------------------------------------------|------------------------------|
| C1    | Batch-scoped record id uniqueness                            | PASS (8 unique)              |
| C1b   | Corpus-wide record id uniqueness                             | PASS (0 collisions)          |
| C2    | `amended_by` references all resolve                          | PASS (0 references in batch) |
| C3    | `repealed_by` references all resolve                         | PASS (0 references in batch) |
| C4    | `cited_authorities` references resolve (parser 0.5.0)        | N/A (not emitted)            |
| C5    | `source_hash` sha256 matches on-disk raw PDF bytes           | PASS (8/8 verified)          |

## Infrastructure follow-up (non-blocking, unchanged)

- 16 batch-0219 raw SI files on disk (~4 MB) plus accumulated batches 0192-0218 raw files awaiting host-driven B2 sync. **rclone unavailable in sandbox** — Peter to run `rclone sync raw/ b2raw:kwlp-corpus-raw/ --fast-list --transfers 4` from the host.
- `corpus.sqlite` stale rollback-journal still blocks in-sandbox FTS rebuild (disk I/O error on read). Deferred to host-side maintenance.
- Persistent virtiofs `.git/index.lock` unlink-failure warnings — non-fatal, the `GIT_INDEX_FILE` workaround stable across batches 0192-0219.
- Sandbox-bash 45s call cap forced ingest into 4 slices (3+2+2+1) plus discovery+finalize calls.
- The 30 pre-existing flat-vs-year-subdir duplicate paths under `records/acts/` (surfaced in batches 0217+) are unchanged this tick — non-blocking, queued for a future cleanup tick.

## Next-tick plan

- Cross-sub_phase rotation tick this batch confirms sis_mining alphabet probes M/N/P/Q/G/E are at exhaustion for keyword-matching novel slots (only 1 keyword-fit out of 128 novel pre-keyword candidates). The Mines and Minerals Development Act 2015/11 derivative SIs that exist on ZambiaLII appear to all already be in HEAD (this needs explicit verification next tick).
- Continue cross-sub_phase fill on next tick: **sis_health** has more candidates in the discovery cache (national health research 2018/092 + 2020/024 + 2020/025; medicines & allied substances 2019/080 expert advisory committee; pharmacy and poisons 1993/046; medical aid societies 1991/030 — that's at least 6 more). Plan: ingest 8 from this remaining pool (consume cached _work/batch_0219_discovery.json novel_pre_keyword_sample without re-fetching alphabets).
- Fallback if sis_health pool drains: rotate to **sis_education** (4 cached candidates: 2021/045 aided institutions, 2013/012 district education offices, 2015/085 teacher training college boards, 2021/004 voter education) and probe alphabets W (Wills), J (Juveniles, Justices), I (Industrial, Insurance).
- Re-verify robots.txt at start of next tick.
- Acknowledged: this is the **first non-100% sub-phase yield** since batch 0213 — but the cross-sub_phase rotation kept the batch at 100% record yield (8/8). Total consecutive-100%-yield streak: **6 ticks** (0214, 0215, 0216, 0217, 0218, 0219).
