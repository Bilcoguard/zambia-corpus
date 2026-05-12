# Repair batch 030 — 8 records repaired (2000–2010 parliament Acts via OCR)

**Timestamp (UTC):** 2026-05-12T08:19Z
**Worker:** repair-corpus (scheduled task v4)
**Verdict:** **NON-IDLE — 8 records repaired** from the v4 manifest.

## Step 0 — Stale lock cleanup

```
find .git -name "*.lock" -delete 2>/dev/null
find .git -name "*.lock.bak" -delete 2>/dev/null
```

FUSE mount continues to reject `unlink` on `.git/objects/maintenance.lock` and
`.git/ORIG_HEAD.lock` — pre-existing constraint, non-fatal.

## Step 1 — git pull

```
$ git pull --ff-only
Already up to date.
```

HEAD on entry: continuation from b029.

## Step 2 — Identify records needing repair

Ran all three live queries (Conditions A, B, C) plus the manifest cross-check.

| Condition | Count |
|---|---:|
| A (line-numbers-only corruption) | **0** |
| B (no body, acts/SIs only) | **252** total — 252 still pending |
| C (stub body, <200 chars) | **60** total |
| Manifest items still needing repair (entering tick) | **80 / 88** |
| Manifest items still needing repair (exiting tick) | **72 / 88** |

## Step 3 — Repair pipeline

All 8 targets were scanned parliament.gov.zm PDFs (pdfplumber yielded 0 chars
except for two text-PDFs). Pipeline:

1. `curl --cacert scripts/certs/rapidssl_tls_rsa_ca_g1.pem -L -A "<UA>"` →
   downloaded all 8 PDFs in parallel (total ≈ 12 MB).
2. `pdftoppm -r 200 -gray` per page → PNG renders.
3. `tesseract -l eng` per page → text.
4. Concatenate page texts → light normalisation (collapse blank-line runs,
   trim form-feeds).
5. Quality gate: `len(body) > 200`, no digit-line corruption, contains
   recognisable legal markers (`Act`, `ENACTED`, `Parliament`, `GOVERNMENT`,
   `Cap`, `Section`, `Amendment`, `An Act`).
6. `UPDATE records SET body, source_hash` + FTS row rebuild + commit.

Two PDFs (`p7`, `p8` = `act-zm-2010-002-the-trademarks` and
`act-zm-2010-006-the-local-government-amendment-2010`) had a usable text layer
and skipped OCR — handled with `pdfplumber.extract_text()` direct.

OCR wall-clock: 242 s for the 6 scanned PDFs (31 pages combined, 200 dpi,
4-way parallel).

## Step 4 — Records repaired this tick (8)

All passed the quality gate. All FTS rows rebuilt. All committed individually.

| ID | prev len | new len | source size | extraction |
|---|---:|---:|---:|---|
| `act-zm-2000-006-the-value-added-tax-amendment-act-no-6-of-2000` | 0 | 13,889 | 4.7 MB | OCR (9 pp) |
| `act-zm-2000-020-the-penal-code-amendment-act-no-20-of-2000` | 0 | 1,937 | 739 KB | OCR (2 pp) |
| `act-zm-2001-008-the-income-tax-amendment-act-no-8-of-2001` | 0 | 1,201 | 538 KB | OCR (1 p) |
| `act-zm-2001-009-the-customs-and-excise-amendment-act-no-9-of-2001` | 0 | 1,932 | 673 KB | OCR (2 pp) |
| `act-zm-2007-024-zambia-tourism-board` | 0 | 22,157 | 2.6 MB | OCR (11 pp) |
| `act-zm-2010-001-the-zambia-development-agency` | 0 | 10,387 | 2.8 MB | OCR (6 pp) |
| `act-zm-2010-002-the-trademarks` | 1 | 2,971 | 49 KB | pdfplumber (2 pp text) |
| `act-zm-2010-006-the-local-government-amendment-2010` | 31 | 14,155 | 199 KB | pdfplumber (8 pp text) |

Spot-check (first 400 chars of each) confirms genuine legislative text — opens
with `GOVERNMENT OF ZAMBIA / Date of Assent / An Act to amend ... / ENACTED by
the Parliament of Zambia` headers as expected.

## Step 5 — Integrity check

```
records       = 1896
records_fts   = 1896
delta         = 0
PRAGMA quick_check → ok
```

Equal counts — commit not gated by Step-5 non-equality clause. Pool grew
1892 → 1896 between b029 and b030 (jiw worker activity, unrelated to repair).

## Step 6 — B2 sync

`rclone` not in sandbox PATH. **Deferred to host.** Logged in `costs.log`.

## Step 7 — Pre-flight: journal handling

The recurring `disk I/O error` from stale `corpus.sqlite-journal` is mitigated
by (a) truncating it to 0 bytes before every connection and (b) setting
`PRAGMA journal_mode = TRUNCATE` so commits truncate-in-place rather than
trying to `unlink` (which the FUSE mount refuses). Same workaround as b029.

## Step 8 — Outstanding manifest backlog

After this tick: **72 of 88** manifest items still need repair. Next ticks will
continue working through them at MAX_BATCH_SIZE=8 per tick.

Remaining by year (descending priority for next batches):

- 1989 / 1996: 4 ZambiaLII HTML/PDF (need to handle www.zambialii.org HTML path)
- 2008: 1 (`/node/` URL — HTML scrape with PDF-link lookup)
- 2010: 13 parliament PDFs remaining (after this tick fixed 3)
- 2011: 6 parliament PDFs
- 2012: 8 parliament PDFs
- 2013: 8 parliament PDFs
- 2014: 2 parliament PDFs
- 2016–2017: 3 parliament PDFs
- 2021: 6 parliament PDFs
- 2023: 11 parliament PDFs
- 2024: 8 parliament PDFs
- 2025: 0 parliament PDFs remaining (cleared in b029)
- 2026: 0 remaining (cleared in b029)
- SIs: 1 (ZambiaLII PDF)

Out-of-manifest backlog (informational, not in scope for v4 worker): 244
Condition-B SIs and ~52 Condition-C stubs not on manifest.

## Step 9 — Commit and push

```
git add corpus.sqlite worker.log gaps.md costs.log reports/repair-batch-030.md
git commit -m "Repair batch 030: fixed 8 records (2000–2010 parliament Acts via OCR)"
git push
```

(Pre-existing untracked / staged files from main and jiw workers — including
`Zambia Corpus Worker/`, `_check_b019.py`, `provenance.log`, miscellaneous
`.write*` markers — left untouched per inter-worker convention.)
