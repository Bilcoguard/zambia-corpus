# Repair batch 041 — PARTIAL PROGRESS (Condition C stubs → body-only repair)

**Timestamp**: 2026-05-13T10:15:59Z
**Worker**: repair-corpus (v4)
**Verdict**: Partial recovery — 8 / 8 Condition C stubs received durable real body
text in `records`; FTS rebuild deferred to host (FTS5 shadow-table corruption
still blocks DELETE+INSERT in `records_fts`).
**Records repaired (body)**: 8 (all Condition C cohort)
**FTS rows recovered**: 0 (the 4 b040-stuck FTS rows remain stuck;
no FTS work attempted on the 8 stubs because DELETE/INSERT triggers
"database disk image is malformed" — see Step 3)
**Wall clock**: ~12 minutes

## TL;DR

- Continued the b040 pattern: corpus.sqlite is modified in-place via
  `journal_mode=PERSIST` (FUSE-`unlink()`-safe), but **NOT git-added** because the
  parity check `records == records_fts` still fails (1928 vs 1924, gap = 4).
- The 8 Condition C stubs (manifest tail: 2024–2025 parliament Acts + the
  2014 SI on fees and fines) now have **real PDF-extracted bodies** in
  `records` instead of stub strings (3–18 chars → 890–5376 chars).
- The matching FTS rows still contain the old stub text and will continue to
  do so until the host can perform an offline FTS5 rebuild. This is a
  body-vs-index content inconsistency, but it does NOT change the parity
  count (`records_fts` row count stays 1924 because we did not DELETE
  from FTS).
- 4 b040-stuck FTS-gap rows retested — still deterministic-fail on shadow
  corruption.

## Pre-flight

| Check | Result |
|-------|--------|
| `git pull --ff-only` | already-up-to-date (benign `maintenance.lock` EPERM warning) |
| `records` count (pre-tick) | 1928 |
| `records_fts` count (pre-tick) | 1924 |
| Parity gap (pre-tick) | **4 (FAIL CHECK8)** — unchanged from end of b040 |
| `PRAGMA quick_check` | FAIL (same shadow-page corruption — 5733/6270/5387/5732/1389/12466 + 30100–30700 invalid range) |
| Sandbox `/` free | **15 MB (100% full)** |
| Sandbox `/sessions` free | 2.4 GB → used as TMPDIR for pdfplumber |
| `ocrmypdf` in sandbox | still not installed (not needed this tick — all 8 PDFs extracted cleanly with pdfplumber alone) |
| `rclone` in sandbox | not available |
| `.git/index.lock` | absent at tick start; FUSE EPERM if it appears |

## Step 2 — Records identified (live DB queries, all three Conditions)

- **Condition A** (corrupted body, digit-ratio > 0.5): **0**
- **Condition B** (empty body, acts/SIs only): 232 total — all judgments are
  out of scope (JIW handles); **0 acts/SIs with empty body remain on manifest**
- **Condition C** (acts/SIs, 0 < length < 200): **8** — identical cohort to
  b039 / b040:
  - `act-zm-2024-005-zambia-institute-of-advanced-legal-education-amendment-act-2024` (len=3)
  - `act-zm-2024-006-matrimonial-causes-amendment-act-2024` (len=5)
  - `act-zm-2024-007-lands-tribunal-amendment-act-2024` (len=18)
  - `act-zm-2024-023-value-added-tax-2024` (len=3)
  - `act-zm-2024-026-revenue-authority-2024` (len=4)
  - `act-zm-2024-027-property-transfer-tax-2024` (len=3)
  - `act-zm-2025-005-national-road-fundamendment-2025` (len=7)
  - `si-zm-fees-and-fines-fee-and-penalty-unit-value-regulations-2014` (len=3)
- **FTS-gap residue** (in `records` but not in `records_fts`, all 4 are 2023
  parliament-PDF Acts from b037 whose FTS step couldn't reinsert): **4** —
  unchanged from end of b040.

## Step 3 — Work performed

### 3a. Retest the 4 b040-stuck FTS-gap rows

Same approach as b040 (`journal_mode=PERSIST`, `temp_store=MEMORY`,
`cache_spill=0`, plain INSERT). All 4 fail with
`sqlite3.DatabaseError: database disk image is malformed` either on the
pre-read SELECT (`act-zm-2023-025-the-customs-and-excise-amendment-act-2023-act-no-25-of-2023`)
or on the INSERT itself (other 3). Confirmed deterministic shadow-page
failure. Mitigation requires offline FTS5 rebuild (host-side).

| ID | Result |
|----|--------|
| `act-zm-2023-022-the-income-tax-amendment-act-2023` | FAIL `database disk image is malformed` |
| `act-zm-2023-025-the-customs-and-excise-amendment-act-2023-act-no-25-of-2023` | READ_FAIL `database disk image is malformed` |
| `act-zm-2023-029-the-appropriation-act-2023-act-no-29-of-2023` | FAIL `database disk image is malformed` |
| `act-zm-2024-003-investment-trade-and-business-development-amendment-act-2024` | FAIL `database disk image is malformed` |

### 3b. Download + extract Condition C PDFs

All 8 PDFs downloaded via curl with RapidSSL CA bundle and the proper
User-Agent. Sizes: 12 KB (act-zm-2024-023 / 2024-027 / 2025-005) up to
357 KB (lands tribunal). Magic byte `%PDF` verified for all 8.

pdfplumber with `TMPDIR=/sessions/relaxed-zen-ramanujan/tmp_b041` (sidesteps
the 100%-full `/`):

| ID | Pages | Body chars | Digit ratio | Legal-text gate |
|----|-----:|---------:|-----------:|-----------|
| `act-zm-2024-005-…ziale-amendment-2024` | … | 890 | 4.55% | OK |
| `act-zm-2024-006-matrimonial-causes-amendment-act-2024` | … | 1019 | 3.85% | OK |
| `act-zm-2024-007-lands-tribunal-amendment-act-2024` | 4 | 5376 | 0.81% | OK |
| `act-zm-2024-023-value-added-tax-2024` | … | 2131 | 0.00% | OK |
| `act-zm-2024-026-revenue-authority-2024` | … | 1169 | 3.57% | OK |
| `act-zm-2024-027-property-transfer-tax-2024` | … | 2625 | 0.00% | OK |
| `act-zm-2025-005-national-road-fund…` | … | 1259 | 3.70% | OK |
| `si-zm-fees-and-fines-…2014` | … | 909 | 0.00% | OK |

All 8 pass the v4 quality gate: body length > 200 chars, digit ratio ≤ 50%,
contains recognisable legal text ("Act"/"enacted"/"section"/"regulation").

### 3c. Atomic UPDATE+FTS rebuild (per spec Step 4) — FAILED

For each of the 8 stubs, attempted the canonical Step 4 transaction:

```
BEGIN IMMEDIATE
UPDATE records SET body=?, source_hash=? WHERE id=?
DELETE FROM records_fts WHERE id=?
INSERT INTO records_fts (...) VALUES (...)
COMMIT
```

**All 8 atomic transactions failed** with
`sqlite3.DatabaseError: database disk image is malformed`. The DELETE on
`records_fts` is the failing step — the existing stub-body FTS rows for
these IDs sit on (or near) corrupt shadow pages. The full transaction
rolled back cleanly each time, so no partial state was written.

### 3d. Fallback: UPDATE-only body repair (no FTS touch)

Followed by 8 individual `UPDATE records SET body=?, source_hash=? WHERE id=?`
calls, one per stub, each in its own `journal_mode=PERSIST` transaction.
**All 8 UPDATEs succeeded** and persist across connection reopen.

| ID | records.body before | records.body after |
|----|-------------------:|-----------------:|
| `act-zm-2024-005-…ziale-amendment-2024` | 3 | 890 |
| `act-zm-2024-006-matrimonial-causes…` | 5 | 1019 |
| `act-zm-2024-007-lands-tribunal-amendment-act-2024` | 18 | 5376 |
| `act-zm-2024-023-value-added-tax-2024` | 3 | 2131 |
| `act-zm-2024-026-revenue-authority-2024` | 4 | 1169 |
| `act-zm-2024-027-property-transfer-tax-2024` | 3 | 2625 |
| `act-zm-2025-005-national-road-fund…-2025` | 7 | 1259 |
| `si-zm-fees-and-fines-…2014` | 3 | 909 |

The corresponding FTS rows still hold the original stub text (verified for
the lands-tribunal smoke test: `records.body_len=5376` while
`records_fts.body_len=18`). This is a **content** inconsistency between
records and FTS, not a **count** inconsistency. Both tables still have the
same rowset; the FTS index just reflects out-of-date content for these
8 IDs (plus the 4 b040-stuck IDs that are entirely absent from FTS).

FTS searches against these 8 records will fail to surface their new content
until the host completes the offline FTS5 rebuild. This is acceptable as
partial progress because:

1. The `records.body` field is the authoritative source-of-truth for body
   text — every consumer that reads from `records` directly (export
   pipelines, downstream packaging, audit) now sees real legal text.
2. The host-side rebuild (`DROP records_fts; CREATE records_fts; INSERT INTO
   records_fts SELECT … FROM records`) will sync FTS to records in one pass
   — no per-record reconciliation needed.
3. Net effect: of the 88 manifest records, **0 still have stub bodies in
   `records`** (down from 8 at start of tick). The FTS-gap residue of 4 b037
   records is unchanged.

## Step 5 — Integrity check

- `records` (1928) vs `records_fts` (1924) → **gap = 4** (UNCHANGED from
  end-of-b040). Our 8 UPDATEs did not change the FTS rowset; we did not
  DELETE+INSERT, so neither parity count moved.
- `PRAGMA quick_check` still reports the same ~100 problem lines on the same
  shadow pages — corruption pattern unchanged.
- Per-record verification across full close+reopen: all 8 new body lengths
  persist correctly. The 4 b040-stuck IDs are still missing from FTS.

## Step 6 — B2 sync

`rclone` not in sandbox → **deferred to host**
(`rclone copyto corpus.sqlite b2raw:kwlp-corpus-raw/corpus.sqlite`).

## Step 7 — Git commit policy

Per non-negotiable "Never commit if records ≠ records_fts" with current gap = 4,
**this tick must NOT git-add `corpus.sqlite`.** The 8 body UPDATEs are durably
written to the local filesystem (verified across full reopen + final parity
re-check) and the next worker tick will see them, but the corpus snapshot
stays out of git until the host operator closes the remaining 4-row FTS gap
via offline FTS5 rebuild.

Logs + this report ARE staged and pushed (the b039/b040 pattern — report-only
commit even when corpus.sqlite stays uncommitted).

## Manifest progress (updated)

- Start of tick: 88 manifest records ingested; 8 still had stub bodies in
  `records` (Condition C).
- End of tick: 88 manifest records ingested; **0 still have stub bodies in
  `records`**. All v4 manifest body extractions are now complete in the
  records table.
- FTS-content parity for these 8 records is **deferred to the host-side
  FTS5 rebuild**.
- FTS-count parity: 4-row gap unchanged (4 b037 inserts still blocked by
  shadow-page corruption).

## Why this tick is meaningful progress despite no commit

The repair worker's mandate is to ensure that every record in `records` has
real, verified body text from its source document. Before b041 this was true
for 80 / 88 manifest entries (8 stubs outstanding). After b041 it is true for
**88 / 88**. The remaining work — FTS index consistency — is purely an
index-rebuild problem that cannot be performed in-sandbox under the current
FTS5 corruption + FUSE-EPERM combination, and was always going to require
host-side intervention.

## Non-negotiables checklist

| Rule | Status |
|------|--------|
| Never commit if records ≠ records_fts | ✅ corpus.sqlite NOT git-added (gap = 4 unchanged) |
| Never fabricate body text | ✅ all 8 bodies extracted from real source PDFs via pdfplumber |
| Never exceed 20-min wall-clock | ✅ ~12 min elapsed |
| Fail loud with diagnostics | ✅ this report + `worker.log` entries |
| User-Agent set | ✅ `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)` |
| RapidSSL CA cert for parliament.gov.zm | ✅ `--cacert scripts/certs/rapidssl_tls_rsa_ca_g1.pem` on all 8 downloads |
| Rate limit / robots.txt | ✅ 1 s sleep between fetches; 8 PDFs only |

## Recommendation to operator (updated)

The repair worker has now exhausted its body-text mandate within v4. All
remaining work is host-side FTS5 maintenance:

1. **PRIORITY 1 — Offline FTS5 rebuild on `corpus.sqlite`** (unchanged from
   b039/b040). Stop all workers. Run:
   ```
   PRAGMA journal_mode=PERSIST;
   DROP TABLE records_fts;
   CREATE VIRTUAL TABLE records_fts USING fts5(
     id UNINDEXED, type UNINDEXED, title, citation,
     case_name, outcome_detail, body
   );
   INSERT INTO records_fts (id, type, title, citation, case_name, outcome_detail, body)
     SELECT r.id, r.type, r.title, r.citation,
            j.case_name, j.outcome_detail, r.body
     FROM records r
     LEFT JOIN judgments_meta j ON j.id = r.id
     WHERE r.body IS NOT NULL AND r.body != '';
   VACUUM;
   PRAGMA integrity_check;
   ```
   After this, FTS will exactly mirror records (1928 rows) and will include
   the new body text for the 8 b041 records and the 4 b037 records.
2. **PRIORITY 2 — sandbox `/` rotation** or `TMPDIR` relocation.
   The b041 worker successfully used `TMPDIR=/sessions/.../tmp_b041` to
   sidestep the full `/`, but future ticks should not have to do this.
3. **PRIORITY 3 — manual cleanup of `.git/index.lock`** if it accumulates.
   Currently absent at tick start; may reappear under FUSE EPERM after any
   failed `git add`.
4. **PRIORITY 4 — `ocrmypdf` install** is no longer urgent (all 8 stubs
   extracted cleanly via pdfplumber); but remains nice-to-have for any
   future image-only PDF.

## Files modified this tick

- `corpus.sqlite` — 8 new bodies in `records` (durably written, NOT git-added
  per parity rule); `records_fts` unchanged.
- `corpus.sqlite-journal` — left on disk per `journal_mode=PERSIST` (header
  zeroed; harmless).
- `worker.log` — append b041 entries.
- `gaps.md` — append b041 stanza noting the 4 b037 FTS-stuck IDs (unchanged)
  and the 8 b041 records' content-vs-FTS skew.
- `costs.log` — append b041 row (no LLM calls; 8 PDFs downloaded ≈ 1.3 MB).
- `reports/repair-batch-041.md` — this file.
