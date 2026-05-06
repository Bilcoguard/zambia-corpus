# Batch 0526 — judgment-ingestion-worker tick

- **Worker**: judgment-ingestion-worker
- **Wall-clock window**: 2026-05-06 (UTC, < 20 min target met)
- **Phase**: ZMSC 2022 most-recent-first DESC sweep continuation (per b0525 next-tick recommendation)
- **Targets**: ZMSC 2022 nums {37, 36, 35, 34, 33, 32, 31, 30}
- **Parser**: v0.3.2 (scripts/batch_0506_zmsc_parse.py wrapping batch_0498_parse + batch_0360_parse)

## Tick decision (priority order)

a. **REPARSE DEFERRED** — gaps.md cohort of 32 ZMSC raw-on-disk deferrals are all flagged
   `raw-on-disk-pending-v0.3.3` (parser v0.3.2 already attempted; awaiting v0.3.3 patterns
   for the interpretive-ratio family). Not eligible for v0.3.2+ reparse this tick.
b. **SCZ SWEEP** — chosen. Continue ZMSC 2022 DESC sweep into nums {37..30}.
c. ZMCC NEW YEARS — not reached.

## Fetch results

All 8 fetched OK (16 HTTP requests at 5s rate-limit). No 404s. PDF sizes 0.7–14 MB.
Date range observed: 2022-04-12 (num 30) → 2022-07-06 (num 35).

## Parse results

- written: 1
- deferred: 7

| num | result | outcome | judges | notes |
|-----|--------|---------|--------|-------|
| 37  | deferred (html_no_summary_pdf_no_match) | – | – | s.122 voir dire / child evidence on oath |
| 36  | deferred (html_no_summary_pdf_no_match) | – | – | witchcraft mitigation negated by admission |
| 35  | deferred (html_no_summary_pdf_no_match) | – | – | long service gratuity + housing allowance |
| **34**  | **written** | **allowed** | Kabuka JS | Citibank Zambia Ltd v Dudhia — leave to appeal granted under SCZ 8 8 of 2022 (Industrial Relations Division statutory one-year disposal point of public importance) |
| 33  | deferred (html_no_summary_pdf_no_match) | – | – | malice / self-defence / intoxication in murder |
| 32  | deferred (html_no_summary_pdf_no_match) | – | – | eyewitness ID despite flawed parade |
| 31  | deferred (html_no_summary_pdf_no_match) | – | – | aggravated robbery ID-parade fairness |
| 30  | deferred (html_no_summary_pdf_no_match) | – | – | leave out of time refused; admin remedies |

Outcome source for the written record: `pdf-tail-2pages` v0.3.2 anchor matched
"Leave to appeal is accordingly granted ...".

## Integrity checks (1/1 written)

- judges present (1) ✓
- issue_tags non-empty (6) ✓
- outcome `allowed` in enum ✓
- judge `Kabuka` resolves in judges_registry.yaml (existing canonical) ✓
- raw_sha256 matches PDF on disk (`f349468d…7734`) ✓
- no duplicate ids in corpus.sqlite ✓
- record + judgments_meta inserted (records 1838→1839, judgments_meta 148→149) ✓

INTEGRITY PASS.

## Cohort status after b0526

ZMSC 2022 sweep: 32 of ~60 attempted
- 13 written
- 18 v0.3.3-pending deferred (raw on disk; awaiting interpretive-ratio parser update)
- 1 OCR-pending deferred (zmsc/2022/51 scanned PDF)
- 1 known internal 404 (num 20)

Daily fetch budget for judgment-ingestion-worker: 32 + 16 = **48 / 500** (today).

## B2 sync

Deferred to host (rclone not in sandbox).

## Next-tick recommendation

Continue ZMSC 2022 most-recent-first DESC sweep with nums {29..22}
(8 candidates). Inner-gap enumeration of num 20 still deferred to closing pass.
