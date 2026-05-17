# Repair batch b0685

- **Batch**: b0685
- **Date**: 2026-05-18
- **Worker**: scheduled-task `repair-corpus` (Repair Corpus Worker v4)
- **Session**: gifted-hopeful-hawking
- **Predecessor**: b0681 (commit 9e47adf, "Repair batch b0681: fixed 8 SI records (zambialii 2020 cohort drainage)")
- **Parser version**: repair-0.6.85

## Summary

| Metric                | Value                                          |
| --------------------- | ---------------------------------------------- |
| Targets identified    | 97 (acts/SIs with no body)                     |
| Repaired this tick    | 8                                              |
| Failed this tick      | 0                                              |
| Remaining after tick  | 89                                             |
| Elapsed sec           | 35                                             |
| records count         | 1925                                           |
| records_fts count     | 1925                                           |
| Integrity (sums)      | PASS (records == records_fts)                  |
| `PRAGMA quick_check`  | ok                                             |

## Identification

Ran all three live SQL queries against `corpus.sqlite` (per v4 SKILL.md Step 2):

- Condition A (digit-ratio corrupted body): **0 found**
- Condition B (no body, type IN ('act','si')): **97 found** — all zambialii.org AKN SI URLs
- Condition C (stub body, length < 200): **0 found**

The 97 Condition-B records continue the same cohort drained in b0667/b0681 (zambialii SIs without `eng@<date>` suffix in the source URL).

## Records repaired

| # | ID                                                                                                                          | Source URL                                          | Body bytes |
| - | --------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------- | ---------- |
| 1 | si-zm-2020-086-animal-health-establishment-of-tsetse-control-pickets-and-check-points-regulations-2020                      | https://zambialii.org/akn/zm/act/si/2020/86         | 1,283      |
| 2 | si-zm-2020-087-animal-health-designated-border-inspection-posts-regulations-2020                                            | https://zambialii.org/akn/zm/act/si/2020/87         | 1,503      |
| 3 | si-zm-2020-093-animal-health-import-and-export-of-animal-animal-product-animal-by-product-or-article-regulations-2020       | https://zambialii.org/akn/zm/act/si/2020/93         | 23,310     |
| 4 | si-zm-2020-094-animal-health-bee-keeping-regulations-2020                                                                   | https://zambialii.org/akn/zm/act/si/2020/94         | 26,826     |
| 5 | si-zm-2020-095-local-government-appointment-of-local-government-administrator-kalumbila-town-council-order-2020             | https://zambialii.org/akn/zm/act/si/2020/95         | 1,465      |
| 6 | si-zm-2020-097-public-finance-management-general-regulations-2020                                                           | https://zambialii.org/akn/zm/act/si/2020/97         | 172,699    |
| 7 | si-zm-2020-101-electoral-process-local-government-by-elections-election-date-and-time-of-poll-no-8-order-2020               | https://zambialii.org/akn/zm/act/si/2020/101        | 1,922      |
| 8 | si-zm-2020-108-urban-and-regional-planning-designated-local-planning-authorities-no-3-regulations-2020                      | https://zambialii.org/akn/zm/act/si/2020/108        | 1,121      |

All 8 records fetched via the zambialii `source.pdf` linked PDF (extraction tool: `pdfplumber`). Quality gate passed for all.

## Pipeline

1. Fetched the zambialii AKN HTML page.
2. Located the `source.pdf` link from the page.
3. Downloaded the linked PDF (User-Agent: `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)`).
4. Extracted with `pdfplumber`; applied section-number normalisation regex.
5. Quality gate: length > 200, digit-ratio test, legal-text keyword check — all passed.
6. SHA-256 hashed; `UPDATE records SET body = ?, source_hash = ?`.
7. FTS rebuild: `DELETE` from `records_fts` for the rowid, then `INSERT … SELECT` for the same rowid.
8. Committed after each record (per v4 SKILL.md Step 4.3).

## Staging

Staged DB on `/tmp/b0685_recover/corpus.sqlite` to avoid virtiofs write-back I/O errors on the 91%-full workspace volume (established pattern from b0659/b0664/b0667/b0681). After successful run, copied back to workspace.

## Integrity checks

- `records` count: 1925
- `records_fts` count: 1925
- Sums balance: PASS
- `PRAGMA quick_check`: ok

## Remaining work

89 Condition-B records remain (all zambialii.org AKN SIs without `eng@<date>` suffix). Next tick will continue drainage in batches of ≤ 8.

## B2 sync

`rclone` not available in sandbox. B2 sync deferred to host.
