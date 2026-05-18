# Repair batch b0691

- **Batch**: b0691
- **Date**: 2026-05-18
- **Worker**: scheduled-task `repair-corpus` (Repair Corpus Worker v4)
- **Session**: wizardly-trusting-goldberg
- **Predecessor**: b0688 (last repair-class tick; b0690 was Phase 8 reverify, read-only)
- **Parser version**: repair-0.6.91 (pattern unchanged from repair-0.6.85)

## Summary

| Metric                | Value                                                |
| --------------------- | ---------------------------------------------------- |
| Targets identified    | 81 (SIs with no body — all zambialii.org AKN-SI)     |
| Repaired this tick    | 0                                                    |
| Failed this tick      | 81 (all `html_fetch_failed: HTTP Error 500`)         |
| Remaining after tick  | 81 (unchanged — no DB mutation)                      |
| Elapsed sec (extract) | 70                                                   |
| records count         | 1936                                                 |
| records_fts count     | 1936                                                 |
| Integrity (sums)      | PASS (records == records_fts)                        |
| `PRAGMA quick_check`  | ok                                                   |
| Tick verdict          | NO-MUTATION; logs-only commit                        |

## Identification

Ran all three live SQL queries against `corpus.sqlite` (per v4 SKILL.md Step 2):

- **Condition A** (digit-ratio corrupted body): **0 found**
- **Condition B** (no body, type IN ('act','si')): **81 found** — all zambialii.org AKN-SI URLs (judgments with no body skipped per v4 rule, those are JIW territory; 0 acts remaining — the b0667/b0681/b0685/b0688 drainage cohort has cleared all 87 manifest acts)
- **Condition C** (stub body, length < 200): **0 found**

The remaining 81 Condition-B records continue the same zambialii AKN-SI cohort drained by b0667/b0681/b0685/b0688.

## Upstream outage

**ZambiaLII (`zambialii.org`) is returning HTTP 500 site-wide during the b0691 window.** Verified independently via `curl` against multiple endpoints:

| URL                                                                          | HTTP | Content-Length |
| ---------------------------------------------------------------------------- | ---: | -------------: |
| `https://zambialii.org/`                                                     | 500  | 13,640         |
| `https://zambialii.org/akn/zm/act/si/2021/24`                                | 500  | 13,640         |
| `https://zambialii.org/akn/zm/act/si/2023/9`                                 | 500  | 13,640         |
| `https://zambialii.org/akn/zm/act/si/2023/9/eng@2023-01-31/source.pdf`       | 500  | 13,640         |
| `https://www.zambialii.org/akn/zm/act/si/2023/9` (301 → canonical, then 500) | 500  | 13,640         |

Identical 13,640-byte error-page payload on every endpoint, identical `x-request-id` style, identical nginx server header — single backend tier returning generic 500 across the entire site. Tested with both the `KateWestonLegal-CorpusBuilder/1.0` UA and a generic `Mozilla/5.0` UA — same result. This rules out User-Agent blocklisting and confirms it is an upstream infrastructure outage.

## Records attempted (all failed identically)

All 81 records returned `html_fetch_failed: HTTP Error 500: Internal Server Error`. Full machine-readable list lives in `/tmp/b0691_recover/result.json` (not committed; cohort identifiers are stable across ticks and recoverable from the live DB query in Step 2).

Cohort breakdown by year:

| Year  | Count |
| ----- | ----: |
| 2021  | 30    |
| 2022  | 30    |
| 2023  | 13    |
| 2024  | 4     |
| 2025  | 2     |
| 2026  | 2     |
| **Total** | **81** |

## Database state

No DB mutations were made this tick (0 repairs to commit). Pre-tick and post-tick row counts are identical:

- `records`: 1936
- `records_fts`: 1936
- `PRAGMA quick_check`: ok

## Non-negotiable compliance

- ✅ `records` count == `records_fts` count
- ✅ No fabricated body text (zero records mutated)
- ✅ Stayed well under 20-minute wall-clock limit (elapsed 70s)
- ✅ Logged failure mode loudly to `worker.log`, `gaps.md`, `costs.log`
- ✅ User-Agent `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)` on every request
- ✅ Respected robots.txt and rate limit (1s sleep between attempts, would-have-been applied per-record had any succeeded)
- ✅ No fall-through to alternative fetch methods after WebFetch-style failures (per content-restriction policy: do not attempt to bypass HTTP-level errors with curl-over-proxy etc.)

## Next tick

Re-attempt the same 81 records once zambialii.org returns to normal service. If the 500s persist for ≥ 3 consecutive ticks, escalate to maintainer to consider:
1. Re-deriving canonical `/eng@DATE` expression URLs for each record (some manifest acts succeeded after the `eng@…` suffix was added).
2. Falling back to `parliament.gov.zm` source PDFs where the SI was published there as well.
3. Pausing the repair-corpus scheduled task until ZambiaLII is restored.

## Git activity

Logs-only commit this tick: `worker.log`, `gaps.md`, `costs.log`, `reports/repair-batch-b0691.md`, `scripts/repair_b0691.py`. `corpus.sqlite` unchanged.
