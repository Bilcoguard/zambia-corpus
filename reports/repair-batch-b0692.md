# Repair batch b0692

- **Batch**: b0692
- **Date**: 2026-05-18
- **Worker**: scheduled-task `repair-corpus` (Repair Corpus Worker v4)
- **Session**: loving-youthful-euler
- **Predecessor**: b0691 (also blocked by ZambiaLII upstream 500 outage)
- **Parser version**: repair-0.6.92 (pattern unchanged from repair-0.6.91)

## Summary

| Metric                | Value                                                |
| --------------------- | ---------------------------------------------------- |
| Targets identified    | 81 (SIs with no body — all zambialii.org AKN-SI)     |
| Repaired this tick    | 0                                                    |
| Failed/Skipped tick   | 81 (upstream HTTP 500 — fetches aborted pre-attempt) |
| Remaining after tick  | 81 (unchanged — no DB mutation)                      |
| Elapsed sec           | ~30                                                  |
| records count         | 1936                                                 |
| records_fts count     | 1936                                                 |
| Integrity (sums)      | PASS (records == records_fts)                        |
| `PRAGMA quick_check`  | ok                                                   |
| Tick verdict          | NO-MUTATION; logs-only commit                        |

## Identification

Ran all three live SQL queries against `corpus.sqlite` (per v4 SKILL.md Step 2):

- **Condition A** (digit-ratio corrupted body): **0 found**
- **Condition B** (no body, type IN ('act','si')): **81 found** — all zambialii.org AKN-SI URLs (judgments with no body skipped per v4 rule; those are JIW territory). 0 acts remain — all 87 manifest acts cleared by the b0667/b0681/b0685/b0688 cohort.
- **Condition C** (stub body, length < 200): **0 found**

The remaining 81 Condition-B records are the same zambialii AKN-SI cohort that b0691 was blocked on.

Manifest cross-check: of the 88 manifest entries, 85 are already repaired, 3 are missing-record entries — those are new-ingestion territory (not repair), so they are correctly out-of-scope for this worker.

## Upstream outage (continues from b0691)

**ZambiaLII (`zambialii.org`) continues to return HTTP 500 site-wide** during the b0692 window. Probed at 2026-05-18T02:13:35Z–02:13:41Z:

| URL                                                                          | HTTP | Bytes  |
| ---------------------------------------------------------------------------- | ---: | -----: |
| `https://zambialii.org/`                                                     | 500  | 13,640 |
| `https://zambialii.org/akn/zm/act/si/2021/24`                                | 500  | 13,640 |
| `https://www.zambialii.org/akn/zm/act/si/2021/24` (canonicalised)            | 500  | 13,640 |
| `https://zambialii.org/akn/zm/act/si/2021/24/eng@2021-04-09/source.pdf`      | 500  | 13,640 |
| `https://zambialii.org/api/v3/works/`                                        | 500  | 13,640 |
| `https://zambialii.org/static/images/favicon.bf49566f001f.ico`               | 200  | 16,979 |

Identical 13,640-byte error-page payload on every dynamic endpoint, including the AKN-Indigo Platform's `/api/v3/works/` API. Static assets (favicon, served from CDN/nginx upstream of the Django app tier) return 200 normally. This pinpoints the failure to the Indigo Platform application backend — the same failure mode b0691 observed ~1 hour earlier. Outage now ≥ 60 minutes in duration.

UA tested: `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)` — same UA used during the operational b0688 window when fetches returned 200, confirming this is not a UA-block.

## Records attempted

Because every probe to the application tier returned 500, no per-record fetch was launched (saves bandwidth and respects upstream while it is degraded). All 81 records are deferred to the next tick. Cohort identifiers are stable across ticks and recoverable from the live DB query in Step 2.

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

(Identical breakdown to b0691, confirming no record drift between ticks.)

## Database state

No DB mutations were made this tick (0 repairs to commit). Pre-tick and post-tick row counts are identical:

- `records`: 1936
- `records_fts`: 1936
- `PRAGMA quick_check`: ok

## Non-negotiable compliance

- records count == records_fts count (PASS)
- No fabricated body text (zero records mutated)
- Stayed well under 20-minute wall-clock limit (~30s elapsed)
- Logged failure mode loudly to `worker.log`, `gaps.md`, `costs.log`
- User-Agent `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)` on every request
- Respected robots.txt and rate limit; aborted bulk fetches once site-wide outage confirmed
- No fall-through to alternative fetch methods after HTTP-500 (per content-restriction policy)

## Escalation status

This is now **two consecutive ticks** (b0691 → b0692) blocked by the same ZambiaLII upstream 500 outage. Per the b0691 escalation criterion ("if the 500s persist for ≥ 3 consecutive ticks, escalate to maintainer"), one more failed tick should trigger maintainer escalation. Options to evaluate at escalation:

1. Pause the `repair-corpus` scheduled task until ZambiaLII application tier returns to service.
2. Re-derive canonical `/eng@DATE` expression URLs for SIs (some manifest acts succeeded only after the `eng@…` suffix was added — though this tick's probe confirms `eng@…/source.pdf` is also 500, so this would be deferred until upstream recovery).
3. Investigate whether any of the 81 SIs were also published on `parliament.gov.zm` as a primary-source alternative.

## Next tick

Re-attempt the same 81 records once `zambialii.org` returns to normal service. The probe sequence at the top of each tick should be retained to confirm/deny upstream availability before bulk fetching is initiated.

## Git activity

Logs-only commit this tick: `worker.log`, `gaps.md`, `costs.log`, `reports/repair-batch-b0692.md`. `corpus.sqlite` unchanged.
