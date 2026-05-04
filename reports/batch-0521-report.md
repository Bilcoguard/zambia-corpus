# Batch 0521 — judgment-ingestion-worker tick (2026-05-04)

## Summary
- **Worker:** judgment-ingestion-worker (dedicated scheduled task)
- **Cohort:** ZMSC 2023 most-recent-first DESC sweep, nums {9..2}
- **Targets:** 8
- **Fetched OK:** 8 (zero 404s — internal sweep block)
- **Written records:** 6
- **Deferred:** 2 (both `html_no_summary_pdf_no_match`)
- **Parser version:** 0.3.2 (scripts/batch_0506_zmsc_parse.py wrapping batch_0498_parse.py)
- **Integrity:** 172/172 PASS (scripts/integrity_check_b0521.py)
- **SQLite:** records 1820 → 1826 (+6); judgments_meta 130 → 136 (+6)

## Written records

| Record ID | Outcome | Detail | Judges |
|-----------|---------|--------|--------|
| judgment-zm-2023-zmsc-09-hamuguyu-v-the-people | allowed | "For that reason, we allow the appeal" | Hamaundu, Chisanga, Kabuka |
| judgment-zm-2023-zmsc-08-sitali-and-ors-v-the-people | dismissed | "the entire appeal and we dismiss it" | Kabuka, Hamaundu, Chinyama |
| judgment-zm-2023-zmsc-07-banda-v-people | upheld | rape conviction; weak ID cured by corroboration | Kabuka, Hamaundu |
| judgment-zm-2023-zmsc-06-sakala-v-people | dismissed | provocation/self-defence rejected | Kabuka, Hamaundu |
| judgment-zm-2023-zmsc-05-mwansa-v-people | dismissed | malice aforethought from head-targeting assault | Kabuka, Hamaundu |
| judgment-zm-2023-zmsc-04-attorney-general-v-siakakole-and-ors | dismissed | "no merit in this appeal and we dismiss it" | Malila, Wood, Chinyama |

## Deferred (raw on disk)

| Num | Reason | Summary |
|-----|--------|---------|
| 3   | html_no_summary_pdf_no_match | Voluntary exit under revised separation scheme — conduct acceptance |
| 2   | html_no_summary_pdf_no_match | Council by-laws/standing orders required before parking levy; public notice unlawful |

## Outcome-source breakdown
- 1 via `summary[v032: conviction-upheld pattern]`
- 2 via `summary[appeal/petition/application... dismissed]`
- 3 via `pdf-tail-2pages[v031/v032 we-(hereby|therefore|accordingly)... pattern]`

## Judges resolutions
6 distinct judges encountered: Hamaundu, Chisanga, Kabuka, Chinyama, Malila, Wood. All resolved against existing canonical entries in judges_registry.yaml — no new canonical entries this tick. Registry unchanged.

## Integrity check details
- 7 required SKILL.md non-negotiables: PASS
- All 6 records: required fields, judges>=1, issue_tags non-empty, outcome enum, registry resolution, raw_sha256 matches on-disk PDF
- 0 duplicate IDs in corpus across 136 unique records on disk

## Operational notes
- FUSE-symptomatic disk I/O error on first sqlite commit; cleared `corpus.sqlite-journal` (rolled back) and re-ran insert successfully (idempotent INSERT OR REPLACE)
- records_fts deferred to host-side rebuild via batch_0504_build_fts5.py per b0517-b0520 precedent
- B2 sync: rclone unavailable in sandbox; deferred to host-side `rclone copyto corpus.sqlite → b2raw:kwlp-corpus-raw/corpus.sqlite`
- approvals.yaml NOT modified (per human-only confirmation rule)

## Cohort cumulative since b0504
- Written: 39 (33 + 6)
- Deferred: 28 (26 + 2)
- 404: 5 (unchanged)

## ZMSC year status
- ZMSC 2023: **COMPLETE** — 22 of 22 attempted (9 written, 11 deferred, 2 404)
- ZMSC 2024: 32 of 34 attempted (21 written, 10 deferred, 1 404)
- ZMSC 2025: prior cohort coverage on dataset
- ZMSC 2026: prior cohort coverage on dataset

## Phase 5 progress
130 → 136 judgments_meta records (target band 100-160; IN BAND)

## Next-tick recommendation

ZMSC 2023 closed. Pivot to **ZMSC 2022** upper-boundary probe + most-recent-first DESC sweep (~ 8 candidates per tick). Estimate 4–5 ticks to fully attempt ZMSC 2022 cohort.
