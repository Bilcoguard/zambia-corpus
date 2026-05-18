# Repair batch b0695

- **Batch**: b0695
- **Date**: 2026-05-18
- **Worker**: scheduled-task `repair-corpus` (Repair Corpus Worker v4)
- **Session**: amazing-nifty-planck
- **Predecessor**: b0694 (8 SIs repaired, 73 remaining)
- **Parser version**: repair-0.6.95

## Summary

| Metric                | Value                                          |
| --------------------- | ---------------------------------------------- |
| Targets identified    | 73 (SIs with no body — all zambialii.org AKN-SI) |
| Repaired this tick    | 8                                              |
| Failed this tick      | 0                                              |
| Remaining after tick  | 65                                             |
| Elapsed sec           | 27.7                                           |
| records count         | 1936                                           |
| records_fts count     | 1936                                           |
| Integrity (sums)      | PASS (records == records_fts)                  |
| `PRAGMA quick_check`  | ok                                             |
| Tick verdict          | MUTATION; 8 SIs body+FTS rebuilt               |

## Identification

Ran all three live SQL queries against `corpus.sqlite` (per v4 SKILL.md Step 2):

- **Condition A** (digit-ratio corrupted body): **0 found**
- **Condition B** (no body, type IN ('act','si')): **73 found** — all zambialii.org AKN-SI URLs
- **Condition C** (stub body, length < 200): **0 found**

These 73 are the residue of the 81 ZambiaLII SIs that became repairable once
the upstream HTTP 500 outage cleared in b0694 (b0694 repaired the first 8).
The manifest in SKILL.md v4 lists 88 records but the corpus has been
progressively cleaning that backlog plus the larger live-DB Condition B set;
the source of truth is the database, not the manifest, as the worker
instructions require.

## Upstream status

ZambiaLII was reachable throughout: probe `GET /akn/zm/act/si/2022/5` →
HTTP 200 (42,672 bytes) at tick start. No 500s observed.

## Records repaired

| # | ID | Source URL | Body bytes |
| - | -- | ---------- | ---------- |
| 1 | si-zm-2021-056-metrology-pre-packaged-commodities-regulations-2021 | https://zambialii.org/akn/zm/act/si/2021/56 | 81,397 |
| 2 | si-zm-2021-057-electoral-process-revision-of-wards-order-2021 | https://zambialii.org/akn/zm/act/si/2021/57 | 102,273 |
| 3 | si-zm-2021-058-data-protection-registration-and-licensing-regulations-2021 | https://zambialii.org/akn/zm/act/si/2021/58 | 33,333 |
| 4 | si-zm-2021-059-metrology-certification-of-competence-regulations-2021 | https://zambialii.org/akn/zm/act/si/2021/59 | 19,253 |
| 5 | si-zm-2021-060-zambia-development-agency-jiangxi-multi-facility-economic-zone-declaration-order-2021 | https://zambialii.org/akn/zm/act/si/2021/60 | 3,369 |
| 6 | si-zm-2021-062-customs-and-excise-ports-of-entry-and-routes-amendment-order-2021 | https://zambialii.org/akn/zm/act/si/2021/62 | 2,517 |
| 7 | si-zm-2021-066-forest-carbon-stock-management-regulations-2021 | https://zambialii.org/akn/zm/act/si/2021/66 | 35,531 |
| 8 | si-zm-2021-067-national-assembly-general-elections-mandevu-constituency-no-80-kasenengwa-constituency-no-41-lusaka-central-constituency | https://zambialii.org/akn/zm/act/si/2021/67 | 3,112 |

All 8 passed the quality gate:
- body length > 200 chars (smallest 2,517, largest 102,273)
- digit-ratio test (not line-numbers-only)
- legal-text markers present (section/regulation/order/schedule/minister/etc.)

## Pipeline used

ZambiaLII AKN page → regex-extract `/akn/.../source.pdf` link → `requests.get`
the PDF (Let's Encrypt CA chain is in certifi) → pdfplumber `extract_text` per
page → section-prefix normalisation → SHA-256 hash → UPDATE records →
DELETE + INSERT records_fts row → commit per record.

No OCR fallback was needed (no extracted body < 200 chars).

## Integrity

```
records         : 1936
records_fts     : 1936
match           : True
PRAGMA quick_check: ok
```

## B2 sync

`rclone` is not available inside the sandbox runtime for this scheduled task,
so the corpus.sqlite push to `b2raw:kwlp-corpus-raw/corpus.sqlite` is deferred
to the host (logged as such in worker.log). The git push below is the
ground-truth backup; B2 will be synced from the host on next opportunity.

## Next tick

65 SIs remain in Condition B (all 2022 zambialii.org AKN-SI URLs based on
ID prefixes). At the current 8/tick pace, ~9 more ticks to clear the backlog
assuming ZambiaLII stays up. No new Condition A/C work expected.

## Files touched

- `corpus.sqlite` (8 records body+FTS updated)
- `scripts/repair_b0695.py` (new)
- `reports/repair-batch-b0695.md` (this file)
- `reports/repair-batch-b0695-summary.json`
- `worker.log`, `costs.log`
- `gaps.md` (no new entries this tick)
