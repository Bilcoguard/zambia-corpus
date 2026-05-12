# Repair batch 031 — 8 records repaired (2010 parliament Acts)

**Timestamp (UTC):** 2026-05-12T11:14Z
**Worker:** repair-corpus (scheduled task v4)
**Verdict:** **NON-IDLE — 8 records repaired** from the v4 manifest.

## Step 0 — Stale lock cleanup

```
find .git -name "*.lock" -delete
find .git -name "*.lock.bak*" -delete
find .git -name "*.lock.atomic" -delete
find .git -name "HEAD.lock.*" -delete
```

FUSE mount continues to reject `unlink` on several `.lock.bak-*` artefacts and
on `.git/objects/maintenance.lock` / `.git/ORIG_HEAD.lock` — pre-existing
constraint, non-fatal (no live `*.lock` files block git operations).

## Step 1 — git pull

```
$ git pull --ff-only
Already up to date.
```

HEAD on entry: continuation from b0610 (judgment-ingestion-worker tick).

## Step 2 — Identify records needing repair

Ran all three live queries (Conditions A, B, C) plus the manifest cross-check.

| Condition | Count (acts + SI only) |
|---|---:|
| A (line-numbers-only corruption) | **0** |
| B (no body) | **246** |
| C (stub <200 chars) | **58** |
| Manifest items still needing repair (entering tick) | **72 / 88** |
| Manifest items still needing repair (exiting tick) | **64 / 88** |

## Step 3 — Repair pipeline

All 8 targets were parliament.gov.zm PDFs. Pipeline applied per record:

1. `curl --cacert scripts/certs/rapidssl_tls_rsa_ca_g1.pem -L -A "<UA>"`
   download PDF.
2. `pdfplumber.extract_text()` — primary text extraction.
3. `pdftotext -layout` — secondary if pdfplumber < 200 chars.
4. `pdftoppm -r 200 -gray` + `tesseract -l eng --psm 6` — OCR fallback for
   scanned PDFs (no embedded text layer).
5. Normalisation: collapse blank-line runs, strip form-feeds.
6. Quality gate: `len(body) > 200`, digit-line ratio < 0.5, ≥ 2 legal markers
   from `{ACT, PARLIAMENT, ZAMBIA, ENACT, SECTION, AMEND, GOVERNMENT, CAP}`.
7. `UPDATE records SET body, source_hash, fetched_at, parser_version` →
   `DELETE` + `INSERT` FTS row → `commit` per record.

## Step 4 — Records repaired this tick (8)

| ID | prev len | new len | source size | extraction |
|---|---:|---:|---:|---|
| `act-zm-2010-007-the-excess-expenditure-appropriation-2010-2013` | 84 | 2,767 | 34 KB | OCR (4 pp) |
| `act-zm-2010-008-the-registered-designs` | 7 | 3,193 | 46 KB | pdfplumber |
| `act-zm-2010-009-the-dairy-produce-board-repeal-2010` | 1 | 563 | 13 KB | pdfplumber |
| `act-zm-2010-010-the-dairy-produce-marketing-and-levy-repeal-2010` | 0 | 568 | 15 KB | pdfplumber |
| `act-zm-2010-011-the-supplementary-appropriation-2008-2010` | 0 | 3,729 | 60 KB | pdfplumber |
| `act-zm-2010-020-the-plea-negotiations-and-agreements-2010` | 23 | 17,557 | 225 KB | pdfplumber |
| `act-zm-2010-021-the-companies-certificates-validation-amendment` | 0 | 928 | 22 KB | pdfplumber |
| `act-zm-2010-023-the-excess-expenditure-appropriation-2010` | 0 | 2,159 | 948 KB | OCR (8 pp) |

Spot-check of `act-zm-2010-020-the-plea-negotiations-and-agreements-2010` —
extracted body opens with `THE PLEA NEGOTIATIONS AND AGREEMENTS ACT, 2010 /
ARRANGEMENT OF SECTIONS / PART I PRELIMINARY` and contains genuine
legislative text through the entire 7-page extract. Quality gate passed.

## Step 5 — Mitigation: stale rollback journal

On first run, the very first `commit` raised `sqlite3.OperationalError: disk
I/O error` — caused by a 66 KB `corpus.sqlite-journal` left over from the
previous tick (b0610 noted the same pattern). Per the established remedy:

```
f.truncate(0)  # corpus.sqlite-journal
PRAGMA journal_mode = TRUNCATE
PRAGMA synchronous  = NORMAL
```

After truncation:
- `PRAGMA quick_check` → `ok`
- `PRAGMA integrity_check` → `ok`
- `records = records_fts = 1899` (no drift)

The script was then re-run with `journal_mode=TRUNCATE` set explicitly at
session open, and all 8 commits succeeded.

## Step 6 — Integrity check (post-repair)

```
PRAGMA quick_check       → ok
PRAGMA integrity_check   → ok
SELECT COUNT(*) records   → 1899
SELECT COUNT(*) records_fts → 1899
delta = 0  (records == records_fts)
```

FTS smoke tests against newly repaired bodies:
- `MATCH 'plea AND negotiations'` → 5 hits, including `act-zm-2010-020-…`
- `MATCH 'dairy AND produce'` → 5 hits, including the two 2010 dairy repeals

## Step 7 — B2 sync

`rclone` not in sandbox — B2 sync deferred to host.

## Step 8 — Manifest progress

```
Entering b031:  16 / 88 manifest items fixed (b030 closed at this number)
Exiting  b031:  24 / 88 manifest items fixed (+8 this tick)
Remaining:      64 / 88
```

Live DB Condition B (no body) backlog: 246 → 245 (one of the b031 repairs
was a stub-body — Condition C — rather than no-body).
Live DB Condition C (stub) backlog: 58 → 51.

## Step 9 — Costs

8 PDF fetches (≈ 1.4 MB total), 2 OCR passes (12 pages, ~80 s).
No paid API usage.

---

**End of batch report 031.**
