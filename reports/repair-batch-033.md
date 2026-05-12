# Repair Batch 033 — 2026-05-12

**UTC start:** 2026-05-12T13:13:54Z
**UTC end:**   2026-05-12T13:14:25Z (wall-clock ≈31 s — well under the 20-min cap)
**Worker:**    repair-worker (SKILL.md v4)
**Script:**    `scripts/repair_batch_033.py`
**Continuation:** Drains manifest 2010/2011 parliament series after b031 (2010 Acts 007-023) and b032 (1989/1996 zambialii + 2008/2010 parliament).

## Pre-tick git state

- Pre-tick lock sweep: `find .git -name "*.lock" -delete` and `*.lock.bak` cleanup ran clean.
- `git pull --ff-only` reported `Already up to date` (two benign FUSE EPERM warnings on `.git/objects/maintenance.lock` and `.git/ORIG_HEAD.lock` — same pattern documented since b0334+; non-blocking).
- Working tree carried staged batch-0614 reverify outputs from prior worker tick — left untouched.

## Sources of truth for queue

Per SKILL.md v4 §2 — ran ALL THREE conditions against the live DB (not just the manifest):

- Condition A (corrupted, line-numbers-only via digit-ratio test): **(computed inline)** — none in scope this tick beyond what is also captured by the stub-body condition.
- Condition B (no body at all, acts/SIs only — judgments are skipped per spec): **240** acts/SIs in DB have empty body.
- Condition C (stub body < 200 chars, acts/SIs only): **48** acts/SIs with `0 < len(body) < 200`.

The manifest still has **56 records** matching the corrupted predicate. b033 drains the next 8 in manifest order (2010 PTT amendment + seven 2011 Acts).

## Inputs

- Queue size: **8** (= MAX_BATCH_SIZE; first 8 still-corrupted manifest records in declaration order).
- Source host: all 8 are www.parliament.gov.zm direct-PDF URLs.

## Results — 8 OK / 0 quality_fail / 0 fetch_error

| # | Record | Method | Chars | Source bytes |
|---|--------|--------|------:|-------------:|
| 1 | act-zm-2010-050-property-transfer-tax-amendment | ocr(2pp) | 2,641 | 41,311 |
| 2 | act-zm-2011-006-the-english-law-extent-of-application-amendment-act-2011 | pdfplumber | 1,338 | 15,800 |
| 3 | act-zm-2011-007-the-high-court-amendment-act-2011 | pdfplumber | 1,807 | 16,090 |
| 4 | act-zm-2011-008-the-supreme-court-amendment-act-2011 | pdfplumber | 1,655 | 14,387 |
| 5 | act-zm-2011-009-the-zambia-institute-of-advanced-legal-education-amendment-act-2011 | ocr(3pp) | 3,837 | 1,206,004 |
| 6 | act-zm-2011-010-the-presidental-emoluments-amendment-act-2011 | pdfplumber | 1,553 | 13,463 |
| 7 | act-zm-2011-027-income-tax-amendment-act-2011 | ocr(9pp) | 15,598 | 232,298 |
| 8 | act-zm-2011-029-zambia-development-agency-amendment-act-2011 | pdfplumber | 705 | 13,570 |

**Aggregate:** 29,134 chars text recovered; 1,552,923 bytes source PDFs fetched; 5 records via pdfplumber, 3 via OCR fallback (records 1, 5, 7 were image-bearing PDFs needing pdftoppm+tesseract pipeline).

Note record 8 ("ZDA Amendment") cleared the >500 char gate at 705c (short amendment Act — single substantive section). Quality gate (`legal markers ≥ 2`, no line-numbers-only, ≥1 long word) passed for all 8.

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
- rclone NOT available → B2 sync deferred to host (will be picked up by host-side sweep, same as b0608/b0614 pattern).

## B2 sync

Deferred to host (rclone not in sandbox; same pattern as last several worker ticks).

## Next-tick queue (manifest remainder)

After b033, **48 manifest records** still need repair. Suggested next batch (b034) — next 8 in manifest order:
- act-zm-2011-030-value-added-tax-amendment-act-2011
- act-zm-2012-003-the-anti-corruption-act-2012
- act-zm-2012-006-the-persons-with-disabilities-act-2012
- act-zm-2012-007-the-civil-aviation-authority-act-2012
- act-zm-2012-008-the-re-denomination-of-currency-act-2012
- act-zm-2012-010-the-income-tax-amendment-act-2012
- act-zm-2012-011-the-medical-levy-repeal-act-2012
- act-zm-2012-012-mines-and-minerals-development-amendment-act-2012

## Non-negotiables check

- Records count = FTS count: PASS (1,917 = 1,917) → commit safe.
- No fabricated text: all 8 bodies extracted from actual source PDFs at the URLs in the manifest.
- Wall-clock under 20 min: 31 s.
- User-Agent: `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)`.
- `--cacert scripts/certs/rapidssl_tls_rsa_ca_g1.pem` applied to all curl calls.
