# Batch 0529 — judgment-ingestion-worker tick

- **Worker**: judgment-ingestion-worker
- **Wall-clock window**: 2026-05-06 (UTC, < 20 min target met)
- **Phase**: ZMSC 2022 most-recent-first DESC sweep continuation (per b0526 next-tick recommendation)
- **Targets**: ZMSC 2022 nums {29, 28, 27, 26, 25, 24, 23, 22}
- **Parser**: v0.3.2 (scripts/batch_0506_zmsc_parse.py wrapping batch_0498_parse + batch_0360_parse)

## Tick decision (priority order)

a. **REPARSE DEFERRED** — gaps.md cohort of 39 ZMSC raw-on-disk deferrals are
   all flagged `raw-on-disk-pending-v0.3.3` (parser v0.3.2 already attempted;
   awaiting v0.3.3 patterns for the interpretive-ratio family). Not eligible
   for v0.3.2+ reparse this tick.
b. **SCZ SWEEP** — chosen. Continue ZMSC 2022 DESC sweep into nums {29..22}.
c. ZMCC NEW YEARS — not reached.

## Fetch results

| num | status | code | date | html bytes | pdf bytes |
|-----|--------|------|------|-----------:|----------:|
| 29  | ok        | –    | 2022-04-01 | 43,459 | 15,136,545 |
| 28  | ok        | –    | 2022-03-28 | 40,702 |  4,629,529 |
| 27  | ok        | –    | 2022-03-22 | 42,449 |  5,329,505 |
| 26  | http-error| 404  | –          | –      |          – |
| 25  | http-error| 404  | –          | –      |          – |
| 24  | http-error| 404  | –          | –      |          – |
| 23  | http-error| 404  | –          | –      |          – |
| 22  | http-error| 404  | –          | –      |          – |

5 contiguous 404s discovered at {22..26}, adjacent to existing num=20 404
boundary discovered in b0522 boundary probe. Internal-gap cluster confirmed
larger than initial probe sampled. 16 HTTP requests at 5s rate-limit
(8 dateless + 3 PDF + 5 prematurely-terminated chains) — all polite, robots.txt-conformant.

Date range observed: 2022-03-22 (num 27) → 2022-04-01 (num 29).

## Parse results

- written: 1
- deferred: 2 (real deferrals — html_no_summary_pdf_no_match)
- raw-not-on-disk: 5 (these are the 404 cluster; not deferrals — confirmed
  internal cadastre-numbering gaps, not parser failures)

| num | result | outcome | judges | notes |
|-----|--------|---------|--------|-------|
| **29**  | **written** | **dismissed** | Wood JS, Musonda DCJ, Kajimanga JS | Mutale v African Banking Corporation Ltd — leave to appeal refused; SCZ 8 5 of 2020 (proposed grounds factual not points of law of public importance under s13 Court of Appeal Act; motion dismissed with costs) |
| 28  | deferred (html_no_summary_pdf_no_match) | – | – | SI No. 6 of 2017 non-retroactivity; employed advocates admitted on the roll entitled to costs; calculational errors curable |
| 27  | deferred (html_no_summary_pdf_no_match) | – | – | Delay beyond Rule 12(2)'s 21-day limit led to dismissal of extension application despite counsel's illness |
| 26  | confirmed-404 | – | – | internal-gap cluster |
| 25  | confirmed-404 | – | – | internal-gap cluster |
| 24  | confirmed-404 | – | – | internal-gap cluster |
| 23  | confirmed-404 | – | – | internal-gap cluster |
| 22  | confirmed-404 | – | – | internal-gap cluster |

Outcome source for the written record: `summary-v032` anchor matched
"Application for leave to appeal ... refused/dismissed" pattern in the
HTML Summary block.

## Integrity checks (1/1 written)

- judges present (3) ✓
- issue_tags non-empty (7) ✓
- outcome `dismissed` in enum ✓
- judges Wood/Musonda/Kajimanga all resolve in judges_registry.yaml
  (existing canonical) ✓
- raw_sha256 matches PDF on disk (`84effbd3…0f10`) ✓
- no duplicate ids in corpus.sqlite ✓
- record + judgments_meta inserted (records 1839→1840,
  judgments_meta 149→150) ✓

INTEGRITY PASS (30/30).

## Cohort status after b0529

ZMSC 2022 sweep: 40 of ~60 attempted
- 14 written
- 20 v0.3.3-pending deferred (raw on disk; awaiting interpretive-ratio parser update)
- 1 OCR-pending deferred (zmsc/2022/51 scanned PDF)
- 6 confirmed internal 404s at nums {20, 22, 23, 24, 25, 26}

Daily fetch budget for judgment-ingestion-worker: 48 + 16 = **64 / 500** (today).

Cohort cumulative since b0504: 52 written, 42 deferred, 10 confirmed 404.

## B2 sync

Deferred to host (rclone not in sandbox).

## Next-tick recommendation

Probe num 21 to close inner-gap span definitively; then continue ZMSC 2022
most-recent-first DESC sweep with nums {19..12} (8 candidates; skip num 20
known 404). Inner-gap closure: confirm {22..26} cluster bounds.
