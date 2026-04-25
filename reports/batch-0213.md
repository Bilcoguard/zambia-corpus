# Batch 0213 — Phase 4 (Bulk Ingest, Mixed sub_phase rotation)

**Started:** 2026-04-25T04:33:01Z
**Completed:** 2026-04-25T04:51Z (approx)
**Records written:** 5 (1 sis_tax 1980/051 + 1 sis_tax/customs 1984/017 + 1 sis_family 2023/037 + 1 sis_corporate 2024/001 + 1 sis_data_protection 2025/056)
**Targets attempted:** 6 (1 failure: sis_corporate 2022/012 pdf_parse_empty — image-only PDF, joins gaps queue)
**Yield:** 5/6 = 83%
**Daily fetches used:** 203/2000 (10.2%)
**Robots.txt SHA256 prefix:** fce67b697ee4ef44 (unchanged from batches 0193-0212)

## Records added

| # | ID | Sub-phase | Parent Act |
|---|----|-----------|------------|
| 1 | si-zm-1980-051-income-tax-foreign-organisations-exemption-approval-no-3-order-1980 | sis_tax | Income Tax Act Cap.323 |
| 2 | si-zm-1984-017-mines-and-minerals-amendment-bill-provisional-charging-order-1984 | sis_tax | Customs and Excise Act Cap.322 |
| 3 | si-zm-2023-037-wills-and-administration-of-testate-estates-probate-rules-2023 | sis_family | Wills and Administration of Testate Estates Act |
| 4 | si-zm-2024-001-anti-terrorism-and-non-proliferation-united-nations-security-council-resolutions | sis_corporate | Anti-Terrorism and Non-Proliferation Act 2018/6 (FIA-related implementation of UN sanctions) |
| 5 | si-zm-2025-056-access-to-information-general-regulations-2025 | sis_data_protection | Access to Information Act 2023/26 |

## Sub-phase rotation rationale

Per batch-0212 next-tick plan, this tick continued sis_tax with deeper alphabet probes (V/W/M/I from the planned-letter list, plus T/S/C added for completeness). Discovery yielded only **5 raw candidates**, of which:
- **2022/004 [V]** — recurring image-only PDF (4th batch failure, OCR backfill deferred)
- **2019/025 [I]** — recurring image-only PDF (5th batch failure)
- **2017/043 [I]** — recurring image-only PDF (5th batch failure)
- **1991/030 [M]** — Medical Aid Societies Authorisation (false positive — health-services regulation, not tax)
- **1980/051 [I]** — Income Tax Foreign Organisations Exemption Approval No. 3 — VALID, the deferral target from batch-0212

Total true sis_tax yield from the 4 planned alphabets: **1 record**. Below the <3 threshold that batch-0212's fallback rule cites for rotation. However, batch-0211 (sis_tax) yielded 8 records, so this is the FIRST low-yield tick, not a 2-consecutive-tick trigger.

To productively use the remaining batch capacity (cap is MAX_BATCH_SIZE=8, MIN target is 3+) the worker performed parallel cross-sub_phase discovery using the cached alphabet HTML files from earlier batches today (no additional fetches required for the cache hits). That produced curated single-record candidates from sis_corporate, sis_family, sis_data_protection, and sis_tax/customs — all parented on Acts that align with the approved sub_phase priority list.

## Sub-phase exhaustion observations (informational, for next tick planning)

- **sis_tax**: with 281 SI records now in HEAD, the keyword-driven candidate pool returns ≤1 novel-and-parseable record per alphabet sweep across V/W/M/I/T/S/C. Most remaining candidates are image-only PDFs (2022/4, 2019/25, 2017/43, 2022/13) requiring OCR backfill (deferred) or false positives (Control of Goods notices, CEE Reservation Scheme, Preservation of Public Security, Privatisation SIs).
- **sis_corporate**: tight-keyword sweep (companies/banking/insolvency/securities/insurance/AML/societies/PACRA) across all 18 cached alphabets returned **1 novel candidate** (2022/012 societies amendment — failed pdf_parse_empty). Broader keyword sweep with FP-exclusion returned no additional clean candidates. sis_corporate is at exhaustion without alternative parent-Act-driven probing or OCR.
- **sis_employment**: tight-keyword sweep returned **1 novel candidate** (2022/013 minimum wages — recurring image-only PDF, no clean alternates).
- **sis_mining**: tight-keyword sweep returned **1 novel candidate** (1984/017 mines and minerals amendment — but that's actually a Customs and Excise provisional charging order, not a Mines Act SI; ingested under sis_tax instead).
- **sis_family / sis_data_protection**: each had limited candidates; one each ingested this batch.

## Integrity checks

- CHECK1 (id uniqueness): batch ids=5, unique=5, prior collisions=0 — PASS
- CHECK2 (amended_by/repealed_by resolve): no cross-references emitted by parser — PASS (vacuous)
- CHECK3 (cited_authorities resolve): no citations emitted — PASS (vacuous)
- CHECK4 (source_hash matches on-disk): 5/5 verified — PASS
- CHECK5 (required fields): 5/5 records have id/type/jurisdiction/title/citation/sections/source_url/source_hash/fetched_at/parser_version — PASS

**ALL CHECKS PASS.**

## Gaps logged

- 2022/012 sis_corporate societies (amendment) rules — pdf_parse_empty (image-only PDF; OCR backfill deferred)

## B2 sync

`rclone` not available in sandbox. Step-8 sync deferred to host. Peter to run:
```
rclone sync raw/ b2raw:kwlp-corpus-raw/ --fast-list --transfers 4
```
on his local workspace. 12 batch-0213 raw files awaiting sync (5 HTML + 5 PDF for ok records + 1 HTML + 1 PDF for failed 2022/012 — kept for re-parse evidence).

## Next-tick plan

Cumulative SI records after this batch: **301** (+5 over batch-0212's 296). Judgment records unchanged at 25 (case_law_scz still paused per robots.txt Disallow on /akn/zm/judgment/).

Per the priority_order rotation rule (yield <3 across 2 consecutive ticks → rotate), this is the **first** low-yield tick for sis_tax. Batch-0214 should:

1. **Re-attempt sis_tax** alphabet=I deeper with parent-Act-driven probes for any remaining 1970s ITA exemption orders (the alphabet pages may not surface them; try `/akn/zm/act/si/197X/N` direct probes for known ranges).
2. Add **alphabet=N** (NAPSA, NHIMA — for sis_employment) and **alphabet=R** (Refugees, Road Traffic, Rural Electrification — for sis_employment-adjacent and sis_corporate-adjacent).
3. Continue cross-sub_phase rotation as proven this batch: when a sub_phase yields <3, fill remaining slots from the next priority_order item with cached-alphabet candidates, but maintain provenance + integrity + sub_phase tagging in the state file.
4. **If batch-0214 also yields <3 sis_tax records**, this becomes the 2-consecutive-tick trigger and worker should fully rotate sub_phase. Recommended order: sis_employment → sis_data_protection → sis_mining → sis_family.
5. Continue robots.txt re-verification at start of each tick.

## Infrastructure follow-up (non-blocking, persistent across batches)

- 12 batch-0213 raw SI files on disk (~1.0 MB) plus accumulated raw files from batches 0192-0212 awaiting host-driven B2 sync (rclone unavailable in sandbox).
- corpus.sqlite stale rollback-journal still blocks in-sandbox FTS rebuild (disk I/O error on read).
- Persistent virtiofs unlink-failure warnings (workaround stable across batches 0192-0213: rename .git/index.lock and stale .git/refs/remotes/origin/main.lock.* to .dN_PID siblings; write valid sha into stale-ref files when git refuses to ignore them).
- Sandbox-bash 45s-call cap forced ingest into 4 invocations (slice 14_15 sis_tax + override slice 0_2 family/corporate + override slice 2_3 customs + override2 slice 0_2 corporate/data-protection + finalize).
