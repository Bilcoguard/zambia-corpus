# Batch 0523 — Judgment-ingestion worker tick

- **Date (UTC):** 2026-05-06
- **Worker:** judgment-ingestion-worker (dedicated scheduled task)
- **Parser:** v0.3.2 (scripts/batch_0506_zmsc_parse.py wrapping batch_0498_parse + batch_0360_parse helpers)
- **Targets:** ZMSC 2022 nums {53..46} (continuation of b0522 most-recent-first DESC sweep)
- **Outcome:** 8/8 fetched OK · 4 written · 4 deferred · 0 errors · 0 fetch 404s

## Tick-level totals
- Fetches: 16 (8 HTML + 8 PDF), all 200 OK
- Records written: 4
- Records deferred: 4
- Records skipped (already on disk): 0
- Cumulative today: 16/500 fetches (well under daily budget)
- Wall-clock: under 20 minutes (target met)

## Written records (records/judgments/zmsc/2022/)

| Num | ID | Outcome | Outcome detail (head) | Source |
|-----|----|---------|------------------------|--------|
| 50 | judgment-zm-2022-zmsc-50-banda-v-people | dismissed | "Appeal dismissed: unchallenged extrajudicial confession … warranting murder conviction and death sentence" | summary |
| 49 | judgment-zm-2022-zmsc-49-nkonde-and-ors-v-attorney-general | dismissed | "(19) We accordingly dismiss the application, with costs to the …" | pdf-tail-2pages v032 |
| 48 | judgment-zm-2022-zmsc-48-mbazima-v-tobacco-association-of-zambia | dismissed | "We accordingly dismiss it" | pdf-tail-2pages v032 |
| 47 | judgment-zm-2022-zmsc-47-mwandila-v-phiri | remitted | "Summary possession under Order 113 RSC cannot resolve disputed title; matter remitted for full trial under Order 28(8) RSC" | summary |

## Deferred (raw on disk)

| Num | Reason | Notes |
|-----|--------|-------|
| 53  | html_no_summary_pdf_no_match | Interpretive-ratio family (parser v0.3.3 standing-pending cohort) — corruption appeal upheld |
| 52  | html_no_summary_pdf_no_match | Interpretive-ratio family (parser v0.3.3 standing-pending cohort) — estate administrator standing |
| 51  | pdf_extraction_empty_likely_scanned | 19.6 MB PDF — appears image-only / scanned. Defer for OCR pass |
| 46  | html_no_summary_pdf_no_match | Interpretive-ratio family (parser v0.3.3 standing-pending cohort) — Lands Act customary interest |

## Outcome-source breakdown
- 1 via `summary[upheld/dismissed pattern]` (num 50 — appeal dismissed via summary)
- 1 via `pdf-tail-2pages[v032 we-(hereby|therefore|accordingly)…]` (num 49 + num 48)
- 1 via `summary[remitted pattern]` (num 47 — remitted via summary)

## Judges resolutions
7 judge-resolutions across 4 panels — all matched existing canonical entries; no new judges:
- Hamaundu JJS×2
- Kaoma JJS
- Mutuna JJS×2
- Wood JJS×3
- Chinyama JJS
- Malila CJ
- Kabuka JJS

## Integrity check details
- All 4 records: required fields present, judges>=1, issue_tags non-empty, outcome in allowed enum, all judges resolve in registry, raw_sha256 matches on-disk PDF
- 0 duplicate IDs across 144 unique judgment records on disk
- 115 total assertions PASS (scripts/integrity_check_b0523.py)

## Operational notes
- corpus.sqlite write via TMPDIR-routed atomic copy pattern (b0519/b0520/b0521/b0522 precedent) — no FUSE issues this tick
- records_fts deferred to host-side rebuild via batch_0504_build_fts5.py
- B2 sync: rclone unavailable in sandbox; deferred to host-side
- approvals.yaml NOT modified (human-only confirmation rule)
- judges_registry.yaml NOT modified (no new canonical names this tick)

## Cohort cumulative since b0504
- Written: 47 (43 + 4)
- Deferred: 36 (32 + 4)
- 404: 5 (unchanged)

## ZMSC year status
- ZMSC 2026: prior cohort coverage on dataset
- ZMSC 2025: prior cohort coverage on dataset
- ZMSC 2024: 32 of 34 attempted (21 written, 10 deferred, 1 404)
- ZMSC 2023: COMPLETE — 22 of 22 attempted (9 written, 11 deferred, 2 404)
- ZMSC 2022: 16 of ~60 attempted (8 written, 7 v0.3.3-pending deferred, 1 OCR-pending deferred, 1 internal 404 at num 20)

## Phase 5 progress
140 → 144 judgments_meta records (target band 100-160; IN BAND)

## Next-tick recommendation
Continue ZMSC 2022 most-recent-first DESC sweep with nums {45..38} (8 candidates).
Inner-gap enumeration of num 20 still deferred to closing pass.
