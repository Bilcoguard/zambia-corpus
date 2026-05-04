# Batch 0518 — judgment-ingestion-worker (dedicated scheduled task)

- **Tick:** 2026-05-04T11:37Z
- **Worker:** judgment-ingestion-worker (separate budget 500/day)
- **Parser:** v0.3.2 (baseline `scripts/batch_0498_parse.py` via `batch_0506_zmsc_parse.py` wrapper)
- **Phase 5 target band:** 100–160 records (now 127 — IN BAND)

## Summary

Continued ZMSC 2024 most-recent-first DESC sweep per b0517 next-tick recommendation.
8 candidates probed (nums 10..3); 7 fetched OK, 1 confirmed 404 (num=4).
Wrote 4 records, deferred 3 under `html_no_summary_pdf_no_match`, deferred 1 under
`raw_bytes_not_on_disk` (the 404).

ZMSC 2024 inventory boundary at num=34 unchanged. Two nums remain untouched
(2, 1) to close out the year.

## Records resolved (raw on disk b0518 → corpus)

| ID | Case | Date | Outcome | Source pattern |
|:---|:-----|:-----|:--------|:----------------|
| zmsc/2024/10 | Astro Holding Limited and Ors v Edgar Hamulele | 2024-04-25 | dismissed | summary |
| zmsc/2024/8  | Peter Katampi and Ors v The People | 2024-05-21 | dismissed | pdf-tail-2pages |
| zmsc/2024/7  | Faustin Kabwe and Bimal Thaker v Ndola Trust School | 2024-05-08 | dismissed | pdf-tail-2pages |
| zmsc/2024/3  | Masautso Banda v The People | 2024-04-19 | dismissed | pdf-tail-2pages |

## Deferred (raw on disk, awaiting parser_v0.3.3)

- **zmsc/2024/9** Constitutional driving-licence-for-deaf-persons declaratory
  question — `html_no_summary_pdf_no_match`. Summary: "Denial or suspension of
  driving licences for deaf persons did not, per se, violate Articles 11, 22
  or 23 of the Constitution." — pure declaratory/interpretive framing (same
  family as zmsc/2024/11 deferred in b0517). Raw retained.
  source_url: https://zambialii.org/akn/zm/judgment/zmsc/2024/9/eng@2024-05-16
- **zmsc/2024/6** Civil/banking matter — `html_no_summary_pdf_no_match`.
  Interpretive ratio framing without operative-verb disposition. Raw retained.
  source_url: https://zambialii.org/akn/zm/judgment/zmsc/2024/6/eng@2024-05-14
- **zmsc/2024/5** Civil/family matter — `html_no_summary_pdf_no_match`.
  Interpretive ratio framing without operative-verb disposition. Raw retained.
  source_url: https://zambialii.org/akn/zm/judgment/zmsc/2024/5/eng@2024-05-06

## Confirmed 404

- **zmsc/2024/4** — HTTP 404 from canonical URL pattern.
  Likely gap in Cadastre internal numbering (court did not assign num=4
  in 2024). Recorded; no raw retained.

## Integrity checks (`scripts/integrity_check_b0518.py`)

- **PASSED: 119**
- **FAILED: 0**
- **Total judgment records on disk:** 127 (up from 123)

Checks performed per the SKILL.md non-negotiables:
1. Required schema fields present
2. Every judgment has ≥1 judge
3. issue_tags non-empty
4. Outcome from allowed enum
5. All judges resolve in canonical registry
6. raw_sha256 matches on-disk PDF SHA-256
7. No duplicate IDs across the corpus
Plus: id matches filename, type=judgment, court=Supreme Court of Zambia,
source_url is ZambiaLII canonical, exactly one matching raw PDF on disk.

## Judges registry

13 judge-resolutions across the 4 written panels. **1 new canonical entry**:

- **Mambilima CJ** (CJ) — historic Chief Justice; first encountered on
  zmsc/2024/8 (Peter Katampi panel).

12 existing canonical re-confirmations:
- Hamaundu JJS ×3, Mutuna JJS ×3, Chinyama JJS ×2, Malila CJ ×2,
  Kabuka JJS ×1, Kaoma JJS ×1, Chisanga JJS ×1.

## corpus.sqlite

- Insert pattern: in-tmp INSERT OR REPLACE → atomic cp back to mounted DB
  (with stale-journal cleanup via cowork `allow_file_delete` for
  `corpus.sqlite-journal`).
- `records`: 1812 → 1816 (+4)
- `judgments_meta`: 123 → 127 (+4)
- `records_fts`: deferred to host-side rebuild via
  `scripts/batch_0504_build_fts5.py` (FUSE write semantics for FTS5
  shadow tables remain unreliable in sandbox).

## B2 sync

- B2 sync deferred to host (rclone not in sandbox) — same as every prior
  judgment-ingestion-worker tick. Raw HTML+PDF retained at
  `raw/zambialii/judgments/zmsc/2024/`.

## Cohort cumulative (judgment-ingestion-worker since b0504)

| tick   | written | deferred | 404 |
|:-------|--------:|---------:|----:|
| b0504/0506 | 5  | 3 | 0 |
| b0511      | 4  | 1 | 3 |
| b0515      | 5  | 3 | 0 |
| b0516      | 6  | 2 | 0 |
| b0517      | 6  | 2 | 0 |
| b0518      | 4  | 3 | 1 |
| **total**  | **30** | **14** | **4** |

Outstanding raw-on-disk-pending-v0.3.3 deferrals (cohort total 14):
- zmsc/2026/{2,3}, zmsc/2025/{1,5}, zmsc/2024/{5,6,9,11,18,22,26,28,29,31}

## Costs / budget

- Today's fetches (judgment-ingestion-worker): **56/500** (was 40/500
  before this tick; this tick spent ~16 fetches: 8 HTML + 7 PDF + 1 404).
- Budget: well within daily quota.

## Next-tick recommendation

Close out ZMSC 2024 with nums **{2, 1}** — only 2 candidates remain.
Cheap probe (~4 fetches). After ZMSC 2024 is fully attempted, sweep
ZMSC 2023 most-recent-first DESC, starting from the inventory boundary
(probe via 404 sentinel to find the highest valid num for 2023).

ZMSC 2024 status after b0518: **32 of 34 attempted** (21 written, 10
deferred, 1 404). Inventory boundary at num=34 unchanged.

## Notes

- approvals.yaml NOT modified per human-only confirmation rule.
- All 4 written records had clean canonical-URL date redirects (no
  fallback to body-scrape needed).
- All 4 outcomes were `dismissed` — coincidence, not pattern: the panel
  in num=10 dismissed a leave-to-appeal application on s.13(3) Court of
  Appeal Act grounds; nums 8 and 3 were criminal appeals dismissed on
  merits; num=7 was a contempt motion dismissed for failure to make out
  the elements.
