# Batch 0522 — judgment-ingestion-worker tick (2026-05-04)

## Summary
- **Worker:** judgment-ingestion-worker (dedicated scheduled task)
- **Cohort:** ZMSC 2022 upper-boundary probe + most-recent-first DESC sweep nums {61..54}
- **Targets:** 8
- **Boundary probes:** 19 HEAD requests confirmed max num=61 (probes at {10,20,30,40,50,60,61,62..69,70,80,90,100}; inner gap at num=20 noted)
- **Fetched OK:** 8 of 8 (zero 404s in {54..61} block)
- **Written records:** 4
- **Deferred:** 4 (all `html_no_summary_pdf_no_match`)
- **Parser version:** 0.3.2 (scripts/batch_0506_zmsc_parse.py wrapping batch_0498_parse.py)
- **Integrity:** 32/32 PASS
- **SQLite:** records 1826 → 1830 (+4); judgments_meta 136 → 140 (+4)

## Written records

| Record ID | Outcome | Detail (head) | Judges |
|-----------|---------|---------------|--------|
| judgment-zm-2022-zmsc-60-yotumu-banda-v-the-people | dismissed | "We dismiss the appeal, uphold the conviction, set aside the …" | Hamaundu, Kaoma, Chinyama |
| judgment-zm-2022-zmsc-59-nelly-mulenga-and-anor-v-bonface-chilambwe-fundafu | dismissed | "The appeal is dismissed with costs to the respondents to be taxed in default" | Malila, Wood, Kajimanga |
| judgment-zm-2022-zmsc-58-luboni-simunga-v-the-people | upheld | "Court upheld murder convictions, substituted death with 20 years due to mitigation" | Hamaundu, Mutuna, Chinyama |
| judgment-zm-2022-zmsc-57-zesco-limited-v-isaac-mbewe-25-ors | allowed | "Contract workers failed to prove entitlement to unpaid/underpaid camping allowance" | Mambilima, Kabuka, Chinyama |

## Deferred (raw on disk)

| Num | Reason | Notes |
|-----|--------|-------|
| 61  | html_no_summary_pdf_no_match | Interpretive-ratio family (parser v0.3.3 standing-pending cohort) |
| 56  | html_no_summary_pdf_no_match | Interpretive-ratio family (parser v0.3.3 standing-pending cohort) |
| 55  | html_no_summary_pdf_no_match | Interpretive-ratio family (parser v0.3.3 standing-pending cohort) — 4.3MB PDF |
| 54  | html_no_summary_pdf_no_match | Interpretive-ratio family (parser v0.3.3 standing-pending cohort) |

## Outcome-source breakdown
- 1 via `pdf-tail-2pages[v032 we-(hereby|therefore|accordingly)…]` (num 60)
- 1 via `pdf-tail-2pages[v031 (petition|appeal|application|action)… dismissed]` (num 59)
- 1 via `summary[Court upheld]` (num 58)
- 1 via `summary[(appeal|petition|application)… (hereby )?allowed]` (num 57)

## Judges resolutions
9 distinct judges encountered across 4 panels (12 judge-resolutions total):
- 1 new canonical entry: **Kajimanga JJS** (first seen in num 59)
- 8 existing canonical re-confirmations: Hamaundu JJS×2, Kaoma JJS, Chinyama JJS×3, Malila CJ, Wood JJS, Mutuna JJS, Mambilima CJ, Kabuka JJS

## Integrity check details
- All 4 records: required fields present, judges>=1, issue_tags non-empty, outcome in allowed enum, all judges resolve in registry, raw_sha256 matches on-disk PDF
- 0 duplicate IDs across 140 unique judgment records on disk
- 32 total assertions PASS (4 records × 8 checks: pdf_present, sha_match, required, judges_min, issue_tags_min, outcome_enum, judges_resolved, body_present)

## Operational notes
- corpus.sqlite write via TMPDIR-routed atomic copy pattern (b0519/b0520 precedent) — no FUSE issues this tick
- records_fts deferred to host-side rebuild via batch_0504_build_fts5.py
- B2 sync: rclone unavailable in sandbox; deferred to host-side
- approvals.yaml NOT modified (human-only confirmation rule)

## Cohort cumulative since b0504
- Written: 43 (39 + 4)
- Deferred: 32 (28 + 4)
- 404: 5 (unchanged)

## ZMSC year status
- ZMSC 2026: prior cohort coverage on dataset
- ZMSC 2025: prior cohort coverage on dataset
- ZMSC 2024: 32 of 34 attempted (21 written, 10 deferred, 1 404)
- ZMSC 2023: **COMPLETE** — 22 of 22 attempted (9 written, 11 deferred, 2 404)
- ZMSC 2022: 8 of ~60 attempted (4 written, 4 deferred); known internal gap at num=20

## Phase 5 progress
136 → 140 judgments_meta records (target band 100-160; IN BAND)

## Next-tick recommendation
Continue ZMSC 2022 most-recent-first DESC sweep with nums {53..46} (8 candidates).
Inner-gap enumeration of num 20 deferred to closing pass.
