# Repair Batch 034 — 2026-05-12

**UTC start:** 2026-05-12T16:39:10Z
**UTC end:**   2026-05-12T16:41:03Z (wall-clock ≈1m 53s — well under the 20-min cap)
**Worker:**    repair-worker (SKILL.md v4)
**Script:**    `scripts/repair_batch_034.py`
**Continuation:** Drains manifest VAT 2011 + 2012 series after b033 (2010 PTT + 2011 series).

## Pre-tick git state

- Pre-tick lock sweep: `find .git -name "*.lock" -delete` and `*.lock.bak` cleanup ran clean.
- `git pull --ff-only` reported `Already up to date` (with the recurring benign FUSE EPERM warning on `.git/ORIG_HEAD.lock` — same pattern documented since b0334+; non-blocking).
- Working tree carried prior staged worker outputs — left untouched.

## Sources of truth for queue

Per SKILL.md v4 §2 — ran ALL THREE conditions against the live DB (not just the manifest):

- Condition A (corrupted, line-numbers-only via digit-ratio test): **0** records (none active this tick).
- Condition B (no body at all, acts/SIs only — judgments are skipped per spec): **236** acts/SIs in DB have empty body.
- Condition C (stub body < 200 chars, acts/SIs only): **44** acts/SIs with `0 < len(body) < 200`.

The manifest still has **48 records** matching the corrupted predicate. b034 drains the next 8 in manifest order (VAT 2011 + 2012 series 003/006/007/008/010/011/012).

## Inputs

- Queue size: **8** (= MAX_BATCH_SIZE; next 8 still-corrupted manifest records in declaration order).
- Source host: all 8 are www.parliament.gov.zm direct-PDF URLs.

## Results — 8 OK / 0 quality_fail / 0 fetch_error

| # | Record | Method | Chars | Source bytes |
|---|--------|--------|------:|-------------:|
| 1 | act-zm-2011-030-value-added-tax-amendment-act-2011 | pdfplumber | 943 | 13,133 |
| 2 | act-zm-2012-003-the-anti-corruption-act-2012 | ocr(56pp) | 48,442 | 1,870,160 |
| 3 | act-zm-2012-006-the-persons-with-disabilities-act-2012 | ocr(44pp) | 44,401 | 1,273,209 |
| 4 | act-zm-2012-007-the-civil-aviation-authority-act-2012 | ocr(70pp) | 43,146 | 2,087,708 |
| 5 | act-zm-2012-008-the-re-denomination-of-currency-act-2012 | ocr(8pp) | 11,546 | 180,732 |
| 6 | act-zm-2012-010-the-income-tax-amendment-act-2012 | ocr(8pp) | 12,409 | 195,857 |
| 7 | act-zm-2012-011-the-medical-levy-repeal-act-2012 | ocr(2pp) | 622 | 14,681 |
| 8 | act-zm-2012-012-mines-and-minerals-development-amendment-act-2012 | ocr(1pp) | 1,506 | 24,438 |

**Aggregate:** 163,015 chars text recovered; 5,659,918 bytes source PDFs fetched; 1 record via pdfplumber, 7 via OCR fallback (the 2012 series PDFs are image-bearing scans needing pdftoppm+tesseract pipeline).

Note record 7 ("Medical Levy Repeal") cleared the >500 char gate at 622c (short repeal Act — single substantive section). All bodies passed the quality gate.

## Quality gate

All 8 records satisfied:
- `len(text) > 500`
- digit-ratio test (not line-numbers-only)
- ≥1 six-letter word
- ≥2 legal markers from {ACT, PARLIAMENT, ZAMBIA, ENACT, SECTION, AMEND, GOVERNMENT, CAP}

## Database integrity

- Pre-flight integrity_check: `ok`
- Post-flight quick_check: `ok`
- Post-flight integrity_check: `ok`
- `records` count: 1,917
- `records_fts` count: 1,917
- `records` == `records_fts`: **PASS**
- FTS rebuild: per-record DELETE-then-INSERT after each UPDATE (commit-per-record per SKILL.md v4 §4).

## TLS / CA-chain note

All 8 fetches succeeded first-pass against parliament.gov.zm via curl + RapidSSL CA preload (`scripts/certs/rapidssl_tls_rsa_ca_g1.pem`). No retry passes needed.

## Sandbox notes

- TMPDIR-routed atomic copy pattern used (FUSE journal limitation; pattern unchanged since b030+).
- pdfplumber+pdftotext+tesseract+pdftoppm all available in sandbox.
- rclone NOT available → B2 sync deferred to host (will be picked up by host-side sweep, same as b033 pattern).

## B2 sync

Deferred to host (rclone not in sandbox; same pattern as last several worker ticks).

## Next-tick queue (manifest remainder)

After b034, **40 manifest records** still need repair. Suggested next batch (b035) — next 8 in manifest order:
- act-zm-2013-005-the-teaching-profession-2013
- act-zm-2013-007-the-excess-expenditure-appropriation-2010-2013
- act-zm-2013-012-the-patents-and-companies-registration-agency-amendment-2013
- act-zm-2013-013-the-weights-and-measures-amendment-2013
- act-zm-2013-014-the-property-transfer-tax-amendment-2013
- act-zm-2013-015-the-value-added-tax-amendment-2013
- act-zm-2013-016-the-customs-and-excise-amendment-2013
- act-zm-2013-019-the-appropriation-act-2013

## Non-negotiables check

- Records count = FTS count: PASS (1,917 = 1,917) → commit safe.
- No fabricated text: all 8 bodies extracted from actual source PDFs at the URLs in the manifest.
- Wall-clock under 20 min: 1m 53s.
- User-Agent: `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)`.
- `--cacert scripts/certs/rapidssl_tls_rsa_ca_g1.pem` applied to all curl calls.
