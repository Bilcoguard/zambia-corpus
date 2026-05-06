# Batch 0525 — judgment-ingestion-worker tick (ZMSC 2022 sweep continuation)

## Summary

- **Worker:** `judgment-ingestion-worker` (scheduled task, distinct from main
  corpus worker). b0524 was already used by the main corpus worker for a
  Phase 8 nightly re-verification (see `reports/batch-0524-report.md`); this
  judgment-ingestion-worker tick advanced to **b0525** to avoid collision.
- **Phase:** Phase 5 dedicated post-Phase-5 judgment ingestion
  (Peter's 2026-05-03 directive). approvals.yaml NOT modified per
  human-only confirmation rule.
- **Goal:** Continue the ZMSC 2022 most-recent-first DESC sweep per
  the b0523 next-tick recommendation, covering nums {45..38}.
- **Targets:** 8 (zmsc/2022/{45,44,43,42,41,40,39,38}).
- **Fetches:** 8/8 successful, 0 errors, 0 404s.
- **Outcomes:** 4 written, 4 deferred.
- **Cumulative today:** 16/500 fetches (well under 500/day budget).

## Records written (4)

| ID | Citation | Date | Outcome | Detail (truncated) |
|----|----------|------|---------|--------------------|
| `judgment-zm-2022-zmsc-45-abel-chipemba-v-the-people` | [2022] ZMSC 45 | 2022-02-10 | dismissed | "appeal is dismissed" |
| `judgment-zm-2022-zmsc-42-chimanga-changa-ltd-v-export-trading-ltd` | [2022] ZMSC 42 | 2022-09-29 | upheld | "we uphold the decision of the Court of Appeal to the extent" |
| `judgment-zm-2022-zmsc-40-zambian-breweries-plc-v-maritime-freight-and-forwa` | [2022] ZMSC 40 | 2022-08-30 | allowed | "Otherwise, this appeal is allowed" |
| `judgment-zm-2022-zmsc-39-teal-minerals-barbados-incorporated-v-zambia-reven` | [2022] ZMSC 39 | 2022-08-17 | dismissed | "The appeal is accordingly dismissed with costs" |

Outcome-source pattern: parser_v0.3.2 mix of pdf-tail-2pages v031 and v032
operative-paragraph patterns.

## Records deferred (4)

All 4 deferred under `html_no_summary_pdf_no_match` (same standing
v0.3.3-pending interpretive-ratio cohort family seen in earlier
ZMSC sweeps):

| Num | Date | Reason summary |
|-----|------|----------------|
| 44  | 2022-09-01 | Mortgagee may lodge a counterclaim in pending writ proceedings; mode of commencement does not bar competent counterclaims. |
| 43  | 2022-03-02 | Bribery conviction appeal; undercover evidence and trial process found lawful, magistrate's findings upheld. |
| 41  | 2022-08-24 | Applicant failed to show public importance or prospects of success; prior judgments made the claim res judicata; leave refused. |
| 38  | 2022-06-07 | Failure to obtain mandatory leave from Court of Appeal deprived the Supreme Court of jurisdiction; appeals dismissed on jurisdictional ground. |

Raw HTML+PDF on disk for all 4 — these are now eligible for re-parse
when parser v0.3.3 lands with broader interpretive-ratio outcome
pattern coverage.

## Judges resolved (12)

All 12 judge resolutions across the 4 panels matched existing canonical
entries in `judges_registry.yaml`; **no new canonical entries were added**:

| Panel | Judges |
|-------|--------|
| zmsc/2022/45 | Hamaundu JS, Kabuka JS, Chinyama JS |
| zmsc/2022/42 | Mutuna JS, Wood JS, Kajimanga JS |
| zmsc/2022/40 | Hamaundu JS, Kaoma JS, Mutuna JS |
| zmsc/2022/39 | Hamaundu JS, Mutuna JS, Musonda DCJ |

(Hamaundu JS appears on 3 panels; Mutuna JS on 3 panels.)

## Integrity check

`scripts/integrity_check_b0525.py` — **117 / 117 passed** (zero failures).

| # | Check | Result |
|---|-------|--------|
| 1 | All 4 record JSON files exist on disk | PASS |
| 2 | All required fields present (15 fields × 4 records = 60) | PASS |
| 3 | id matches filename | PASS (4/4) |
| 4 | type = "judgment" | PASS (4/4) |
| 5 | court = "Supreme Court of Zambia" | PASS (4/4) |
| 6 | judges ≥ 1 | PASS (4/4) |
| 7 | All 12 judge.name values resolve in canonical registry | PASS (12/12) |
| 8 | issue_tags non-empty list | PASS (4/4) |
| 9 | outcome ∈ allowed enum | PASS (4/4) |
| 10 | outcome_detail non-empty | PASS (4/4) |
| 11 | Exactly one matching raw PDF on disk | PASS (4/4) |
| 12 | raw_sha256 matches on-disk PDF sha256 | PASS (4/4) |
| 13 | source_url is ZambiaLII canonical | PASS (4/4) |
| 14 | No duplicate IDs across corpus (148 unique) | PASS |

Total records on disk: **148 unique judgment IDs** (was 144).

## Database update

`scripts/batch_0525_sqlite_insert.py` succeeded via the established
TMPDIR-routed atomic copy pattern (b0519/b0520/b0521/b0522/b0523
precedent) to side-step FUSE journal cleanup errors:

- `records`: 1834 → **1838** (+4)
- `judgments_meta`: 144 → **148** (+4)
- `records_fts`: deferred to host-side rebuild via
  `scripts/batch_0504_build_fts5.py`

## Cohort cumulative (since b0504)

- Written: **51** judgments
- Deferred (v0.3.3-pending interpretive-ratio family): **40** records
  (raw HTML+PDF on disk; eligible for parser v0.3.3 reparse)
- Confirmed 404s: 5 (cadastre-numbering gaps at zmsc/2024/4, zmsc/2023/{4,13}, zmsc/2022/20)

## ZMSC 2022 progress

24 of ~60 attempted in this sweep:
- Written: 12 (zmsc/2022/{60,59,58,57,50,49,48,47,45,42,40,39})
- Deferred (v0.3.3-pending): 11 (zmsc/2022/{61,56,55,54,53,52,46,44,43,41,38})
- Deferred (OCR-pending): 1 (zmsc/2022/51 — 19.6 MB scanned image-only PDF)
- Internal 404: 1 (zmsc/2022/20, confirmed cadastre-numbering gap)

## Operational notes

- **Batch numbering:** b0524 collided with the main corpus worker's
  Phase 8 nightly re-verification tick (renumbered there from a
  default b0523 collision detection — see `reports/batch-0524-report.md`
  "Operational notes"). This judgment-ingestion-worker tick advanced
  to b0525 cleanly; no overlap with b0524 artefacts.
- **Lock-file workaround:** none required this tick — `git pull --ff-only`
  reported `Already up to date.` directly. (FUSE-block on
  `.git/objects/maintenance.lock` warned but did not block the pull.)
- **B2 sync:** `rclone` not available in sandbox; sync deferred to host
  per established pattern.
- **Costs:** 16 fetches consumed today (8 HTML + 8 PDF for the 8 targets).
  Cumulative today 32/500.

## Next-tick recommendation

Continue ZMSC 2022 most-recent-first DESC sweep with nums {37..30}
(8 candidates). Inner-gap enumeration of num 20 still deferred to
closing pass once the contiguous DESC sweep reaches the lower
boundary.
