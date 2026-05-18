# Zambia Corpus Repair — Batch 013

**Date:** 2026-05-09 08:15 UTC (scheduled run)
**Worker:** repair-corpus (automated tick, scheduled-task SKILL v3 manifest, 48 records)
**Operator:** automated (Claude scheduled task; session `clever-vigilant-mendel`)
**Status:** **5 records repaired in DB; git commit DEFERRED per Step 4 strict reading (pre-existing FTS gap)**
**Headline:** Repair worker re-activated against the new 48-record manifest (v3 SKILL.md), discovered 5 still-corrupted records (3 newly enqueued from 2024-2026 cohort plus 2 from earlier years), repaired all 5 to clean PDF-extracted bodies. The pre-existing FTS gap (records=1851, records_fts=1846, Δ=5) is documented as not caused by this tick — Δ is unchanged across the tick — but Step 4's literal `records == records_fts` assertion would fail, so the git commit is deferred per the spec's "Never commit if records count ≠ records_fts count" non-negotiable.

## Pre-flight

* Pre-step `find .git -name "*.lock" -delete` and `find .git -name "*.lock.bak" -delete` ran. FUSE mount silently rejected unlink on `.git/ORIG_HEAD.lock` — same pre-existing constraint as every prior repair batch; non-fatal.
* `git pull --ff-only` returned `Already up to date.`
* Working tree carries pre-existing untracked artifacts and modifications from other workers (costs.log, gaps.md, provenance.log, worker.log, _stale_*, _repair_batch_*) — left untouched (outside repair worker's domain).

## Step 2 — manifest re-verification

Manifest expanded from 42 records (b008–b012 era) to **48 records** (45 Acts + 3 SIs) in v3 SKILL.md. Iterated all 48 manifest record IDs and applied the corruption test:

```python
lines = body.strip().split('\n')
num_lines = sum(1 for l in lines if l.strip().isdigit())
is_corrupted = (num_lines > len(lines) * 0.5 and len(lines) > 10)
```

Result:

| Bucket | Count |
|---|---|
| OK (passes quality gate) | **43** |
| Still corrupted | **5** |
| Not found in DB | **0** |

The 5 still-corrupted records (all body filled with line-numbers like `1\n2\n3\n...`):

| ID | body chars (corrupted) |
|---|---|
| `act-zm-2010-004-the-public-interest-disclosure-protection-of-whistleblowers` | 47 |
| `act-zm-2011-005-the-management-services-board-repeal-act-2011` | 27 |
| `act-zm-2021-033-the-cannabis-act-2021` | 40 |
| `act-zm-2024-025-moblie-money-transactions-levy-2024` | 29 |
| `act-zm-2026-002-disaster-management-amendment-act` | 32 |

All 5 are within MAX_BATCH_SIZE = 8, so the entire remaining queue could be attempted in this tick.

## Step 3 — Process batch (5 records)

### 3a. Download PDFs (all parliament.gov.zm)

All 5 URLs were `parliament.gov.zm` Apache 2.4 PDFs. Direct `urllib.request` failed with `SSL: CERTIFICATE_VERIFY_FAILED` (Python's certifi bundle does not include `RapidSSL TLS RSA CA G1` which signs `*.parliament.gov.zm`). Fell back to `curl --cacert scripts/certs/rapidssl_tls_rsa_ca_g1.pem` (the on-disk PKI loader used by other workers). All 5 downloads returned HTTP 200 + valid PDF magic bytes.

| ID | bytes | %PDF- header |
|---|---|---|
| act-zm-2010-004… | 740,074 | yes |
| act-zm-2011-005… | 22,048 | yes |
| act-zm-2021-033… | 82,204 | yes |
| act-zm-2024-025… | 382,152 | yes |
| act-zm-2026-002… | 337,024 | yes |

User-Agent: `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)`. 2 s sleep between fetches (4 inter-request gaps = 8 s of rate-limit wait).

### 3b/3c. Extract text (pdfplumber 0.11.9; OCR not needed)

All 5 PDFs extracted ≥ 200 chars on first pass — none triggered OCR fallback (which would have been deferred since `ocrmypdf` is not installed in sandbox).

| ID | pdfplumber raw chars |
|---|---|
| act-zm-2010-004… | 58,993 |
| act-zm-2011-005… | 6,820 |
| act-zm-2021-033… | 45,453 |
| act-zm-2024-025… | 6,944 |
| act-zm-2026-002… | 17,751 |

### 3d. Quality gate

All 5 passed (length > 500, not line-numbers, ≥ 1 word > 5 chars).

### 3e. Section normalisation

Applied `normalise_sections()` per the spec. None of the 5 had multi-section concatenations that triggered a split (input texts had clean line breaks between sections), so output length == input length for all five. The function ran without error.

### 3f. UPDATE corpus.sqlite + rebuild FTS

Initial attempt batched all 5 records in one transaction; `commit()` raised `sqlite3.OperationalError: disk I/O error` and SQLite rolled back the journal — DB returned to pre-tick state (verified). Diagnosis: FUSE mount appears to handle large rollback-journal writes poorly when bundling ~135 KB of body changes in one transaction. Recovery: deleted the orphan `corpus.sqlite-journal` (via `mcp__cowork__allow_cowork_file_delete`; SQLite had already cleaned it on next open in any case), re-opened DB, **re-ran updates one record at a time with explicit `commit()` after each step** (records UPDATE, FTS DELETE, FTS INSERT) — all 5 records went through cleanly. This per-record commit pattern matches what other workers (judgment-ingestion-worker) effectively do via the inline runner.

For each repaired record:
1. `UPDATE records SET body = ? WHERE id = ?` (rowcount asserted == 1)
2. `DELETE FROM records_fts WHERE id = ?` (rowcount == 1)
3. `INSERT INTO records_fts (...) SELECT ... FROM records WHERE id = ?` with `judgments_meta` LEFT JOIN per spec
4. `commit()` after each statement

Verification: `SELECT length(body) FROM records_fts WHERE id = ?` returns the same length as the new body for all 5 — FTS rebuild confirmed in sync per-record.

## Step 4 — Integrity check

```text
records      = 1851
records_fts  = 1846
delta        = 5
```

**Spec assertion `records == records_fts` would fail (1851 ≠ 1846).**

The 5-row delta is **pre-existing and not introduced by this tick**:
- Pre-tick state (before Step 3): records=1851, records_fts=1846, Δ=5
- Post-tick state (after Step 3): records=1851, records_fts=1846, Δ=5
- **Δ is unchanged across the tick.** No new gap introduced.

Provenance of the 5-row gap (per worker.log + costs.log):
- b011 (2026-05-08 23:12Z) and b012 (2026-05-09 06:11Z) recorded a 3-row pre-existing gap (records=1849, fts=1846), attributed to three judgment-zm-2020-zmsc-* IDs added by judgment-ingestion-worker without corresponding FTS rows.
- b0553 (judgment-ingestion-worker, 2026-05-09 08:14:02Z, ~15 min before this tick) added 2 more judgments (zmsc-2025-4 Minimart and zmsc-2025-32 Shaba-Mulengela) per costs.log, raising records 1849 → 1851. FTS row count stayed at 1846, so the gap grew 3 → 5.
- All 5 gap rows belong to the judgment-ingestion-worker domain. Repair worker has no licence to touch them (Non-negotiable: "Never INSERT or DELETE records — only UPDATE existing bodies.").

**Per Non-negotiable "Never commit if records count ≠ records_fts count":** git commit and push are DEFERRED.

PRAGMA integrity_check returns `ok` — no DB-level corruption.

## Step 5 — B2 sync

Skipped — `rclone` is not installed in sandbox; B2 sync deferred to host (matches every prior tick).

## Step 6 — Commit and push

**DEFERRED per Step 4.**

The 5 body repairs are committed to the local SQLite file (per-record SQLite commits succeeded and were re-verified post-tick). They are NOT in git.

**Recommendation to operator / next worker:**
1. The judgment-ingestion-worker (or main worker) should rebuild `records_fts` rows for the 5 missing judgment IDs (the 3 from the 2020 ZMSC cohort flagged by b011, plus the 2 new ones from b0553). After that fix, `records == records_fts` will be true (1851 == 1851) and the next worker tick can `git add corpus.sqlite && git commit` and the repair-body changes from this tick will go up with it.
2. Alternative: the operator may relax the strict assertion in v4 of SKILL.md to `delta_after <= delta_before` (i.e. "this tick must not introduce a new gap"), which would have allowed this tick to git-commit the body repairs cleanly.

## Records attempted (5)

| ID | URL | Outcome | New body chars |
|---|---|---|---|
| act-zm-2010-004-the-public-interest-disclosure-protection-of-whistleblowers | parliament.gov.zm/.../Public%20Interest%20Disclosure%20…2010.PDF | repaired | 58,993 |
| act-zm-2011-005-the-management-services-board-repeal-act-2011 | parliament.gov.zm/.../Management%20Services%20board%20Act%2C%202011.pdf | repaired | 6,820 |
| act-zm-2021-033-the-cannabis-act-2021 | parliament.gov.zm/.../Act%20No.%2033%20of%202021…Cannabis%20Act…pdf | repaired | 45,453 |
| act-zm-2024-025-moblie-money-transactions-levy-2024 | parliament.gov.zm/.../Act%20No.%2025%20of%202024…Mobile%20Money…pdf | repaired | 6,944 |
| act-zm-2026-002-disaster-management-amendment-act | parliament.gov.zm/.../Disaster%20Management%20Amendment%20Act%20No.%202%20of%202026.pdf | repaired | 17,751 |

## Records successfully repaired (5)

All 5 above. New body in DB, FTS in sync per-record.

## Records failed (0)

None.

## Records still remaining (0)

All 48 manifest records now pass the corruption test:

```text
Total manifest: 48
Still corrupted: 0
Fixed: 48
```

## Live-DB integrity snapshot

* `records` = **1851** (was 1849 at b012; +2 from b0553 judgment ingestion)
* `records_fts` = **1846** (unchanged since b011)
* Δ = **5 rows** (was 3 at b012; +2 from b0553)
* PRAGMA integrity_check = `ok`
* All 5 repaired record bodies confirmed not-corrupted post-tick

## Tick budget

* Wall clock: ~10 minutes (well under 20-min limit)
* PDF fetches: 5 (all parliament.gov.zm)
* Records updated: 5
* Records below MAX_BATCH_SIZE=8 by 3 (no need to re-tick)
* OCR invocations: 0
* B2 sync: deferred (no rclone)
* Git commit: DEFERRED per Step 4 (pre-existing FTS gap)

## Recommendation

* **DO NOT disable repair-corpus** despite b008-b012 idle ticks — the v3 manifest expansion to 48 records exposed 5 newly-corrupted entries. Expect more as the main worker continues to ingest 2024-2026 acts.
* Operator should ask the judgment-ingestion-worker or main corpus worker to backfill the 5 missing FTS rows (3 × judgment-zm-2020-zmsc-* + judgment-zm-2025-zmsc-4-minimart + judgment-zm-2025-zmsc-32-shaba-mulengela) so that the pre-existing FTS gap closes and this tick's body repairs can be committed via the next normal worker push.
* Consider relaxing the SKILL.md v3 assertion to `delta_after <= delta_before` so the repair worker can ride through pre-existing inconsistencies that are not its fault.
