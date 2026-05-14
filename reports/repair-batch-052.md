# Repair batch 052 (b0652-repair)

**Tick:** b0652-repair
**Parent commit:** 01e2194 (b0651-jiw trailer)
**Worker:** corpus-repair-worker
**Wall-clock:** ~13min
**Date (UTC):** 2026-05-14T18:14:00Z

## Preflight

- `git pull --ff-only` initial attempt → fatal: bad object refs/heads/main.lock.bak.b0651-1778782110.
  Quarantine: moved `main.lock.bak.b0651-1778782110`, `main.lock`, and a probe file out of `.git/refs/heads/` and then out of `.git/refs/` entirely into `.git/_quarantine_outside_refs/` (rename succeeds; unlink continues to fail under the FUSE bindfs deny-unlink — same chronic mode as b0641..b0651). Second `git pull` succeeded: 2de3797..01e2194.
- Records=1928, records_fts=4 read-error (FTS5 shadow corruption confirmed unchanged; `MAX(rowid)` query on `records_fts` raises malformed-disk-image). Pre-tick parity gap held at 4 since repair-040 per b0651-jiw.
- `PRAGMA quick_check` not runnable (raises malformed-disk-image immediately); fingerprint unchanged from b0635+ per visible row read errors.
- Disk: corpus FS 12G free, sandbox `/` **6.5M** free (chronic 100%-full), /sessions tmpfs adequate.
- Tools: pdfplumber 0.11.9, curl, tesseract 4.1.1, pdftoppm 22.02.0 available. **Not** available: rclone, ocrmypdf, sqlite3 CLI.

## Discovery

Live-DB scan (per SKILL.md guidance — DB is source of truth over the v4 manifest):

- Condition A (digit-only/line-numbers-only corruption): **0** (full scan via per-row read, 1928 ids).
- Condition B (no body, acts/SIs only): **172** (170 zambialii SIs + 2 SIs with non-zambialii sources; 0 acts in the live DB had a wholly-NULL/empty body).
- Condition C (acts/SIs, 0 < length(body) < 200): **0**.
- Read errors during scan: **5** manifest acts whose body cell sits on a corrupt FTS-adjacent page or returned a UTF-8 decode error:
  - `act-zm-2012-013-property-transfer-tax-amendment-act-2012` (DatabaseError)
  - `act-zm-2021-028-the-engineering-institution-of-zambia-amendment-act-2021` (DatabaseError)
  - `act-zm-2021-030-the-chartered-institute-of-logistics-and-transport-amendment-act-2021` (DatabaseError)
  - `act-zm-2023-022-the-income-tax-amendment-act-2023` (UTF-8 decode error — recoverable)
  - `act-zm-2023-025-the-customs-and-excise-amendment-act-2023-act-no-25-of-2023` (DatabaseError)

This tick prioritised the 5 manifest-act read-error records (new pattern: dedicated parliament.gov.zm/PDF script), then back-filled the remaining batch budget with 5 zambialii SIs continuing b0650's drain from 2018/002 onward.

## Repair — primary act pass (`scripts/batch_0652_repair.py`)

Parliament.gov.zm PDF + RapidSSL G1 CA cert; pdfplumber extraction; body-only UPDATE with `journal_mode=MEMORY`; no FTS touch.

| # | ID | Bytes | SHA8 | Status |
|---|----|------:|------|--------|
| 1 | act-zm-2012-013-property-transfer-tax-amendment-act-2012 | 0 (PDF) / 5,962 (post-OCR) | — / 2566e034 | **FAIL** — image-only OmniPage PDF; tesseract OCR recovered 5,962 chars, but the UPDATE itself raised malformed-disk-image (row sits on corrupt page) |
| 2 | act-zm-2021-028-the-engineering-institution-of-zambia-amendment-act-2021 | — | — | **FAIL** — DatabaseError on UPDATE (corrupt page); PDF fetched OK (11.4 KB) |
| 3 | act-zm-2021-030-the-chartered-institute-of-logistics-and-transport-amendment-act-2021 | — | — | **FAIL** — DatabaseError on UPDATE (corrupt page); PDF fetched OK (22.6 KB) |
| 4 | act-zm-2023-022-the-income-tax-amendment-act-2023 | 7,176 | 1fe0f836 | **OK** (the UTF-8 decode error was a stale write; fresh UTF-8 body persisted cleanly) |
| 5 | act-zm-2023-025-the-customs-and-excise-amendment-act-2023-act-no-25-of-2023 | — | — | **FAIL** — DatabaseError on UPDATE (corrupt page); PDF fetched OK (318 KB) |

Act-pass result: **1/5 OK · 4 FAIL (3 corrupt-page + 1 corrupt-page after OCR success)**.

## Repair — SI back-fill (`scripts/batch_0652_repair_si.py`)

zambialii AKN HTML → source.pdf → pdfplumber → quality gate → body-only UPDATE, same pattern as b0650.

| # | ID | Bytes | SHA8 | Status |
|---|----|------:|------|--------|
| 1 | si-zm-2018-002-education-military-training-establishment-of-zambia-management-dissolution-regulations-2018 | 7,042 | 280b6f77 | OK |
| 2 | si-zm-2018-003-zambia-defence-university-declaration-order-2018 | 743 | da4806f2 | OK |
| 3 | si-zm-2018-007-railways-transportation-of-heavy-goods-regulations-2018 | 4,319 | d3c6299b | OK |
| 4 | si-zm-2018-014-tourism-and-hospitality-accommodation-establishment-standards-regulations-2018 | 740,695 | 5ff3612f | OK |
| 5 | si-zm-2018-021-electoral-process-local-government-by-election-election-date-and-time-of-poll-order-2018 | 2,130 | 79a745bf | OK |

SI-pass result: **5/5 OK · 754,929 body bytes written.**

## Totals

- **6 successful repairs** (1 act + 5 SIs), **762,105 body bytes** written
- **4 failures** (3 manifest-act DatabaseError-on-UPDATE + 1 OCR-rescued body that still couldn't UPDATE due to corrupt page)
- SHA256(8) chain (successes): 1fe0f836+280b6f77+da4806f2+d3c6299b+5ff3612f+79a745bf

All 6 success rows confirmed populated by direct SELECT post-write.

## Post-state

- records MAX(rowid)=1928 (unchanged)
- records_fts: COUNT/MAX queries still raise malformed-disk-image (FTS5 shadow page 5733 and friends unchanged since b037/b038)
- Parity gap: assumed unchanged at ≥4 (cannot enumerate records_fts to confirm); body-only UPDATEs cannot shift FTS parity in either direction
- Condition-B SI remaining: **165** (172 pre-tick − 5 repaired − 2 already-non-zambialii non-targeted; delta verified by re-scan post-write where readable)

## Quality-gate refinement

The b0650 relaxed marker check (case-insensitive + `proclamation|constitution|gazette|whereas|article`) was **not** folded into this tick's primary script per the b0650 carry-forward note, because the act-pass targets passed the standard gate (Act/section/Regulations all present in extracted text). The OCR fallback path (tesseract via pdftoppm) is new this tick and should be added to the standard primary repair script for any image-only PDFs encountered in future ticks — at present only ocrmypdf is mentioned in SKILL.md but is not installed; tesseract + pdftoppm is a viable substitute.

## Manifest reconciliation

The 5 manifest-act read-error records still sit on corrupt sqlite pages. **3 of them cannot be repaired in-sandbox** without a host-side VACUUM/page rebuild (acts 2021-028, 2021-030, 2023-025). **1 additional act (2012-013) was successfully OCR'd to a clean 5,962-char body** but its UPDATE also failed for the same reason — the recovered text is preserved in `_repair_b0652_pdfs/ocr01_p[1-4].txt` for the host to splice in post-VACUUM.

The v4 manifest also remains stale vs the live DB (per b0650 note §"Manifest reconciliation") — chronic, host-side reconciliation task.

## Git policy

- `corpus.sqlite` = **NOT committed** (gitignored; parity-rule defers commit even if it were tracked: gap unchanged at ≥4)
- Staged: `worker.log`, `costs.log`, `gaps.md`, `reports/repair-batch-052.md`, `scripts/batch_0652_repair.py`, `scripts/batch_0652_repair_si.py`

## B2 sync

Deferred to host: `rclone` not present in sandbox; no corpus-wide mutation to sync.

## Outstanding host actions (carry-forward from b0650/b0651)

(a) FTS5 rebuild to close the ≥4-row parity gap and unblock JIW
(b) Install ocrmypdf — or recognise tesseract+pdftoppm as the in-sandbox OCR substitute
(c) VACUUM / page rebuild on `records` to unlock the 4 corrupt-page act rows (3 fetched PDFs and 1 OCR'd body waiting)
(d) Stale-manifest removal / rewrite of SKILL.md v4 manifest against live IDs
(e) Cleanup 14 orphan FTS rows
(f) Cleanup orphan journals + `.git/objects/maintenance.lock` + chronic FUSE bindfs deny-unlink (every quarantine "rm" failed; only `mv` works in-sandbox)
(g) Reinstate sandbox `/` headroom (chronic 100% full, 6.5 MB free)

## Next

b0653-repair at t+1h — continue Condition-B SI drainage from 2018/022 onward (next 8 in alphabetical order are 2018/022, /023, /033, /039, /043, /044, /046, /054).
