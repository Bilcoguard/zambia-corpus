# Repair batch b0688

- **Batch**: b0688
- **Date**: 2026-05-18
- **Worker**: scheduled-task `repair-corpus` (Repair Corpus Worker v4)
- **Session**: loving-fervent-heisenberg
- **Predecessor**: b0685 (commit 33b9b58, "Repair batch b0685: fixed 8 SI records (zambialii AKN-SI cohort drainage)")
- **Parser version**: repair-0.6.88 (pattern unchanged from repair-0.6.85)

## Summary

| Metric                | Value                                          |
| --------------------- | ---------------------------------------------- |
| Targets identified    | 89 (acts/SIs with no body)                     |
| Repaired this tick    | 8                                              |
| Failed this tick      | 0                                              |
| Remaining after tick  | 81                                             |
| Elapsed sec (extract) | 32                                             |
| records count         | 1936                                           |
| records_fts count     | 1936                                           |
| Integrity (sums)      | PASS (records == records_fts)                  |
| `PRAGMA quick_check`  | ok                                             |

## Identification

Ran all three live SQL queries against `corpus.sqlite` (per v4 SKILL.md Step 2):

- **Condition A** (digit-ratio corrupted body): **0 found**
- **Condition B** (no body, type IN ('act','si')): **89 found** — all zambialii.org AKN SI URLs (judgments with no body skipped per v4 rule, those are JIW territory)
- **Condition C** (stub body, length < 200): **0 found**

The 89 Condition-B records continue the same zambialii AKN-SI cohort drained by
b0667/b0681/b0685. Same parser, same source-pdf preference, no logic changes.

## Records repaired

| # | ID                                                                                                                                          | Source URL                                          | Body bytes |
| - | ------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------- | ---------- |
| 1 | si-zm-2020-122-tourism-and-hospitality-licensing-temporary-disapplication-of-renewal-and-retention-fee-regulations-2020                     | https://zambialii.org/akn/zm/act/si/2020/122        | 1,332      |
| 2 | si-zm-2020-123-tourism-and-hospitality-registration-of-hotel-managers-temporary-disapplication-of-registration-fee-regulations-2020         | https://zambialii.org/akn/zm/act/si/2020/123        | 1,305      |
| 3 | si-zm-2021-001-forest-reserve-no-4-maposa-cessation-order-2021                                                                              | https://zambialii.org/akn/zm/act/si/2021/1          | 1,977      |
| 4 | si-zm-2021-002-kasama-national-forest-no-p-47-alteration-of-boundaries-order-2021                                                           | https://zambialii.org/akn/zm/act/si/2021/2          | 3,463      |
| 5 | si-zm-2021-003-national-forest-no-f31-kabwe-alteration-of-boundaries-order-2021                                                             | https://zambialii.org/akn/zm/act/si/2021/3          | 5,159      |
| 6 | si-zm-2021-007-electoral-process-local-government-by-elections-election-time-and-time-of-poll-order-2021                                    | https://zambialii.org/akn/zm/act/si/2021/7          | 1,933      |
| 7 | si-zm-2021-010-kasama-municipal-council-vehicle-loading-and-parking-levy-by-laws-2021                                                       | https://zambialii.org/akn/zm/act/si/2021/10         | 4,112      |
| 8 | si-zm-2021-015-diplomatic-immunities-and-privileges-international-centre-for-tropical-agriculture-order-2021                                | https://zambialii.org/akn/zm/act/si/2021/15         | 10,647     |

All eight repaired via `source.pdf` route (ZambiaLII linked PDF found and
pdfplumber extraction passed the >200-char threshold and the digit-ratio
quality gate on the first attempt — no OCR fallback required).

## Concurrent-session note

Between this tick's Step 2 query (records=1928) and the runner's stage-copy
(records=1936) a concurrent judgment ingestion worker added 8 judgments
(244 → 252 judgments). The staged DB was therefore based on the 1936-record
snapshot and the post-promote live count matched (1936/1936). No JIW writes
were lost.

## FUSE EPERM workaround

- Stale `corpus.sqlite-journal` (25,136 bytes, mtime 02:14) blocked initial
  post-promote open with `disk I/O error`. Could not `rm` (EPERM on virtiofs).
  Parked via `mv` to `corpus.sqlite-journal.b0688-stale.bak` (established
  b0652/b0657/b0658/b0659 pattern). Re-promote then opened cleanly,
  quick_check=ok.
- B2 sync deferred to host (rclone unavailable in sandbox).

## Disk

`/sessions/loving-fervent-heisenberg/mnt/corpus` is 92% full (208G / 229G).
Continue to stage on `/tmp` and prune `_repair_b06*` PDF caches outside the
tick where possible.
