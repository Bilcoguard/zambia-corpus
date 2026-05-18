# Repair batch b0697

- **Batch**: b0697
- **Date**: 2026-05-18
- **Worker**: scheduled-task `repair-corpus` (Repair Corpus Worker v4)
- **Session**: happy-vibrant-turing
- **Predecessor**: b0695 (8 SIs repaired, 65 remaining)
- **Parser version**: repair-0.6.97

## Summary

| Metric                | Value                                          |
| --------------------- | ---------------------------------------------- |
| Targets identified    | 65 (SIs with no body — all zambialii.org AKN-SI) |
| Repaired this tick    | 8                                              |
| Failed this tick      | 0                                              |
| Remaining after tick  | 57                                             |
| Elapsed sec           | 22.2                                           |
| records count         | 1946                                           |
| records_fts count     | 1946                                           |
| Integrity (sums)      | PASS (records == records_fts)                  |
| `PRAGMA quick_check`  | ok                                             |
| Tick verdict          | MUTATION; 8 SIs body+FTS rebuilt               |

## Identification

Ran all three live SQL queries against `corpus.sqlite` (per v4 SKILL.md Step 2):

- **Condition A** (digit-ratio corrupted body): **0 found**
- **Condition B** (no body, type IN ('act','si')): **65 found** — all zambialii.org AKN-SI URLs
- **Condition C** (stub body, length < 200): **0 found**

These 65 remain from the larger live-DB Condition B backlog. The
b0695 tick reduced 73→65; this tick (b0697) reduces 65→57.

## Upstream status

ZambiaLII was reachable throughout: probe `HEAD /akn/zm/act/si/2022/5` →
HTTP 302 (redirect to expression URL, normal) at tick start. No 5xx errors.

## Records repaired

| # | ID | Source URL | Body bytes |
| - | -- | ---------- | ---------- |
| 1 | si-zm-2021-068-electoral-process-local-government-elections-election-date-and-time-of-poll-no-2-order-2021 | https://zambialii.org/akn/zm/act/si/2021/68 | 1,931 |
| 2 | si-zm-2021-069-public-holidays-declaration-notice-2021 | https://zambialii.org/akn/zm/act/si/2021/69 | 993 |
| 3 | si-zm-2021-071-public-holidays-declaration-no-2-notice-2021 | https://zambialii.org/akn/zm/act/si/2021/71 | 845 |
| 4 | si-zm-2021-072-public-holidays-declaration-no-3-notice-2021 | https://zambialii.org/akn/zm/act/si/2021/72 | 943 |
| 5 | si-zm-2021-073-public-holidays-declaration-no-4-notice-2021 | https://zambialii.org/akn/zm/act/si/2021/73 | 880 |
| 6 | si-zm-2021-074-national-assembly-kaumbwe-constituency-no-50-election-date-and-time-of-poll-order-2021 | https://zambialii.org/akn/zm/act/si/2021/74 | 2,143 |
| 7 | si-zm-2021-075-electoral-process-local-government-elections-election-date-and-time-of-poll-order-2021 | https://zambialii.org/akn/zm/act/si/2021/75 | 2,040 |
| 8 | si-zm-2021-087-national-assembly-by-election-kabwata-constituency-no-77-election-date-and-time-of-poll-no-3-order-2021 | https://zambialii.org/akn/zm/act/si/2021/87 | 2,289 |

All 8 passed the quality gate:

- body length > 200 chars (smallest 845, largest 2,289 — short-but-valid SI orders)
- digit-ratio test passes (not line-numbers-only)
- legal-text markers present (order/notice/minister/by virtue/schedule/etc.)

## Pipeline used

Per v4 SKILL.md Step 3 ZambiaLII branch:

1. `GET https://zambialii.org/akn/zm/act/si/2021/<N>` (HTML, with UA header).
2. Regex-extract `href="/akn/.../source.pdf"` from the HTML.
3. `GET` the source.pdf (LE-chain trusted by certifi; no custom CA needed for zambialii).
4. `pdfplumber` per-page text extraction → join with `\n\n`.
5. Section-prefix normalisation (split `1.A` → `1. A`).
6. SHA-256 hash of the extracted body.
7. `UPDATE records SET body=?, source_hash=?, fetched_at=?, parser_version=?` (parameterised).
8. `DELETE FROM records_fts WHERE id=?` then `INSERT … SELECT … FROM records WHERE id=?`.
9. `commit()` after each record (per SKILL.md non-batched commit rule).

No OCR fallback was needed (no extracted body < 200 chars).

## Integrity

```
records         : 1946
records_fts     : 1946
match           : True
PRAGMA quick_check: ok
```

## B2 sync

`rclone` not available in sandbox — sync deferred to host (consistent with
b0688/b0691/b0692/b0694/b0695).

## Wall-clock

~22 seconds — well under the 20-minute budget; the bottleneck is per-record
HTTP round-trip with 1-second courtesy delay between records.

## Next tick

57 SIs remain in Condition B. Continue same pipeline; no operator action
required.

## Concurrency note

This tick used direct in-place mutation under `PRAGMA journal_mode=MEMORY`
(no stage-and-replace), per the b0695-jiw lesson in worker.log
("stage-promote pattern + concurrent-writer mutation is INHERENTLY unsafe").
