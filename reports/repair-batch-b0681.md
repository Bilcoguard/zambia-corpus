# Repair batch b0681 — 2026-05-18

Worker: repair-corpus (v4)
Session: relaxed-nifty-johnson
Parent commit: e1cd58f

## Summary

- Targets identified (Condition B, acts/SIs with empty body): 105
- Targets identified (Condition A, line-numbers-only corruption): 0
- Targets identified (Condition C, stub acts/SIs <200 chars): 0
- Batched this tick: 8 (MAX_BATCH cap)
- Repaired: 8
- Failed: 0
- Quality-gate rejections: 0
- Remaining after this tick (Condition B): 97
- Judgments with no body: skipped per v4 (judgment ingestion worker owns those).

## Records repaired

All 8 sourced from ZambiaLII AKN pages → `source.pdf` extraction (pdfplumber).

| id | body_len | source |
|---|---:|---|
| si-zm-2020-069-plant-pests-and-diseases-phytosanitary-certification-regulations-2020 | 14082 | pdf |
| si-zm-2020-070-plant-pests-and-diseases-plant-quarantine-and-phytosanitary-service-fees-regulations-2020 | 3226 | pdf |
| si-zm-2020-071-national-assembly-by-election-mwansabombwe-constituency-no-65-and-lukashya-constituency-no-98-election-date-and-time-pol | 2294 | pdf |
| si-zm-2020-072-electoral-process-local-government-by-elections-election-date-and-time-of-poll-no-7-order-2020 | 2041 | pdf |
| si-zm-2020-073-civil-aviation-authority-search-and-rescue-regulations-2020 | 43215 | pdf |
| si-zm-2020-079-electoral-process-local-government-by-elections-election-date-and-time-of-poll-no-8-order-2020 | 1816 | pdf |
| si-zm-2020-084-animal-identification-general-regulations-2020 | 23139 | pdf |
| si-zm-2020-085-animal-health-tsetse-fly-area-and-tsetse-fly-control-area-declaration-notice-2020 | 1903 | pdf |

## Integrity

- records: 1925
- records_fts: 1925
- PRAGMA quick_check: ok
- Body quality gate: all 8 pass (>200 chars, no line-numbers-only, contains recognisable legal keywords).

## Notes

- DB staged on `/tmp/b0681_recover/corpus.sqlite` to avoid virtiofs write-back I/O issues (volume at 91% capacity), then copied back.
- corpus.sqlite NOT staged in git (gitignored per Phase 6 b0504; B2 sync deferred to host — rclone unavailable in sandbox).
- Cohort drainage: SIs in the ZambiaLII 2020 series (run resumed from b0667).
- Elapsed: ~33s for 8 fetches.
