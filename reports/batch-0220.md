# Phase 4 — Batch 0220 report

**Started:** 2026-04-25T08:32Z (UTC)
**Completed:** 2026-04-25T08:45Z (UTC)
**Sub-phase:** cross-sub_phase fill — sis_health (6) + sis_education (2)
**Records written:** 8/8 attempted (Yield = 100%)
**Cumulative SI records after batch:** 357 (+8 over batch-0219's 349)
**Judgment records:** 25 (case_law_scz remains paused per zambialii.org robots.txt Disallow on /akn/zm/judgment/)

## What this batch did

1. `git pull --ff-only` was blocked by stale staged-deletions in the sandbox index (carryover from batches 0215..0219 host-side commits). Cleared with `GIT_INDEX_FILE=/tmp/git_idx_tick220` + `read-tree HEAD` + ref-write directly to `refs/heads/main = 318c5aa` (origin/main batch-0219 close-out commit). Working tree already matched origin so no merge required. Files on disk preserved.
2. Re-verified zambialii.org robots.txt — sha256 prefix `fce67b697ee4ef44` unchanged from batches 0193-0219 (full sha256: `fce67b697ee4ef44e0694134e23108c2701b5e7661eed885013efb9b75dcd8f0`).
3. **No alphabet probes spent this tick.** Reused batch-0219 discovery cache (`_work/batch_0219_discovery.json` — `novel_pre_keyword_sample` field, 128 entries) per the batch-0219 next-tick plan ("sis_health has 6 more cached candidates in novel_pre_keyword_sample ... can be ingested without re-fetching alphabets if state cache is preserved").
4. Selected 8 candidates from the cached sample by cross-sub_phase keyword scan:
   - **sis_health: 6** — National Health Research Act 2018/4 derivatives (3) + Medicines & Allied Substances Act 2013/3 expert advisory committee (1) + Pharmacy and Poisons Act fees (1) + Medical Aid Societies and Nursing Homes authorisation fees (1).
   - **sis_education: 2** — Education Act 2011/23 derivatives (aided educational institutions + district education offices establishment).
5. Wrote `_work/batch_0220_discovery.json` with the 8 selected candidates (each carrying its own `sub_phase` field) and a `cross_sub_phase_rotation: true` flag.
6. Modified `cmd_ingest` in `scripts/batch_0220.py` to use per-target `sub_phase` (`t.get("sub_phase") or SUB_PHASE_TAG`) so the 6 sis_health and 2 sis_education entries are tagged correctly in provenance and in the per-record entry log — `SUB_PHASE_TAG = "sis_health"` is now only the default fallback.
7. Ingested in 4 slices (slice_0_2 + slice_2_4 + slice_4_6 + slice_6_8) honouring 6s crawl delay (margin over robots-declared 5s) — 16 ingest fetches total + 1 robots reverify = **17 fetches this batch**.
8. Ran integrity checks CHECK1a (batch-scoped) / CHECK1b (corpus-wide) / CHECK2 (`amended_by`) / CHECK3 (`repealed_by`) / CHECK4 (`source_hash` matches on-disk raw bytes) / CHECK5 (required fields) — **all PASS** (no collisions introduced; 34 pre-existing flat-vs-year-subdir duplicate paths under `records/acts/` unchanged from batches 0217+, non-blocking).
9. Wrote 8 record JSON files under `records/sis/{1991,1993,2013,2018,2019,2020,2021}/` and 16 raw HTML+PDF files under `raw/zambialii/si/{1991,1993,2013,2018,2019,2020,2021}/`.

## Records written (8)

| Year/No   | Sub-phase     | Title                                                                                                                          | Sections | PDF bytes |
|-----------|---------------|--------------------------------------------------------------------------------------------------------------------------------|----------|-----------|
| 1991/030  | sis_health    | Medical Aid Societies and Nursing Homes (Exemption, Establishment and Operation) (Authorisation Fees) Order, 1991              | 1        | 153,361   |
| 1993/046  | sis_health    | Pharmacy and Poisons (Fees) Order, 1993                                                                                        | 19       | 145,134   |
| 2013/012  | sis_education | Education (District Education Offices) (Establishment) Order, 2013                                                             | 2        | 182,968   |
| 2018/092  | sis_health    | National Health Research (Material Transfer) Regulations, 2018                                                                 | 14       | 257,064   |
| 2019/080  | sis_health    | Medicines and Allied Substances (Expert Advisory Committee) Regulations, 2019                                                  | 6        | 23,744    |
| 2020/024  | sis_health    | National Health Research (Bio Banking) Regulations, 2020                                                                       | 34       | 155,063   |
| 2020/025  | sis_health    | National Health Research (Registration and Accreditation) Regulations, 2020                                                    | 25       | 168,632   |
| 2021/045  | sis_education | Education (Aided Educational Institutions) Regulations, 2021                                                                   | 52       | 177,217   |

All 8 records carry `parser_version: "0.5.0"`, sha256 source_hash, fetched_at ISO 8601 UTC, and an alternate_sources entry pointing at the discovery HTML page.

## Highlights

- **National Health Research Act 2018/4 cluster** (3 records) — material transfer (2018/092), bio banking (2020/024), and registration/accreditation (2020/025). These are the core operational regulations under Zambia's NHR Act and matter for any KWLP client doing clinical research, sample export, or health-data IRB pathways.
- **2019/080 Medicines and Allied Substances (Expert Advisory Committee) Regulations** — completes the parent-Act-driven sweep around MAS 2013/3 begun in batch 0219 (which captured agro-veterinary shops, dispensing certificates, health shops, fees, importation, and certificate of registration). Together with batch 0219's six MAS records, this gives KWLP a clean ZAMRA regulatory bench.
- **1991/030 Medical Aid Societies and Nursing Homes Authorisation Fees Order** — niche but still operative; useful in advisory on private medical scheme establishment.
- **2021/045 Education (Aided Educational Institutions) Regulations** + **2013/012 District Education Offices Establishment Order** — first sis_education records the corpus has ingested under the Education Act 2011/23. Establishes the sub-phase footprint for future education-sector SIs.

## Budgets

- **Today's fetches:** 356 / 2,000 (17.8%) — well under cap. All on zambialii.org under the robots-declared 5s crawl-delay using a 6s safety margin.
- **Today's tokens:** within budget (no LLM calls; pdfplumber parsing + sha256 hashing only).
- **Per-batch fetches:** 17 (1 robots reverify + 0 alphabet probes + 16 ingest URL/PDF pairs). **0 alphabet probes thanks to discovery-cache reuse from batch 0219.**

## Integrity checks

| Check | Description                                                  | Result                       |
|-------|--------------------------------------------------------------|------------------------------|
| C1a   | Batch-scoped record id uniqueness                            | PASS (8 unique)              |
| C1b   | Corpus-wide record id uniqueness                             | PASS (0 collisions introduced; 34 pre-existing flat-vs-year-subdir duplicates under records/acts/ unchanged) |
| C2    | `amended_by` references all resolve                          | PASS (0 references in batch) |
| C3    | `repealed_by` references all resolve                         | PASS (0 references in batch) |
| C4    | `source_hash` sha256 matches on-disk raw PDF bytes           | PASS (8/8 verified)          |
| C5    | Required fields present (id/type/title/citation/sections/source_url/source_hash/fetched_at/parser_version) | PASS |

## Infrastructure follow-up (non-blocking, unchanged)

- 16 batch-0220 raw SI files on disk plus accumulated batches 0192-0219 raw files awaiting host-driven B2 sync. **rclone unavailable in sandbox** — Peter to run `rclone sync raw/ b2raw:kwlp-corpus-raw/ --fast-list --transfers 4` from the host.
- `corpus.sqlite` stale rollback-journal still blocks in-sandbox FTS rebuild (disk I/O error on read). Deferred to host-side maintenance.
- Persistent virtiofs `.git/index.lock` unlink-failure warnings — non-fatal; the `GIT_INDEX_FILE` workaround remains stable across batches 0192-0220.
- Sandbox-bash 45s call cap forced ingest into 4 slices (2+2+2+2) plus finalize.
- The 34 pre-existing flat-vs-year-subdir duplicate paths under `records/acts/` (surfaced in batches 0217+) are unchanged this tick — non-blocking, queued for a future cleanup tick.

## Next-tick plan

- **sis_health pool from batch-0219 cache is now exhausted** — all 12 sis_health candidates from the cached novel_pre_keyword_sample have been ingested (6 in batch 0219 + 6 in batch 0220).
- **2 sis_education candidates remain** in the cached sample for next-tick consumption: `2015/085 education (teacher training college boards) (establishment) order` + `2021/004 electoral process (voter education) regulations`. Together with fresh alphabet probes for sis_education / sis_courts / sis_family this should fill a batch:
  - Probe alphabets **W** (Wills, Workers' Compensation), **J** (Juveniles, Justices), **I** (Industrial, Insurance) for sis_family/sis_courts/sis_employment derivatives.
  - Probe alphabets **E**, **S**, **T** specifically for sis_education (Education Act 2011/23 derivatives, Skills Development Act, Teaching Profession Act, TEVETA, ZAQA).
- Fallback if combined yield <3: rotate to **sis_family** parent-Act probes — Wills and Administration of Testate Estates Act, Marriage Act 2024 derivatives (the 2024 Marriage Act is the most-recently amended family-law statute and will have implementing SIs).
- Re-verify robots.txt at start of next tick.
- **7 consecutive 100% record-yield ticks now** (0214, 0215, 0216, 0217, 0218, 0219, 0220). Discovery-cache reuse this tick achieved 0 alphabet-probe fetches — a new efficiency low for the sub-phase rotation pattern.
