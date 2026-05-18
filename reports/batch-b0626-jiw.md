# Batch b0626-jiw — TICK ABORTED

- **Worker:** judgment-ingestion-worker
- **Start:** 2026-05-13T05:08Z (UTC)
- **End:** 2026-05-13T05:18Z
- **Wall-clock:** ~10 minutes (well within 20 min budget)
- **Records inserted:** 0
- **Records deferred:** 1 orphan JSON (zmsc-2024-11) + 6 HTMLs cached
- **Fetches:** 10 (1 listing relisting + 7 HTMLs + 1 PDF + 1 directory probe). Cumulative today: **21/500**.
- **B2 sync:** deferred to host (rclone not in sandbox).
- **Git push:** deferred to host-side sweep (no commit produced this tick).

## Verdict

Aborted before any successful database commit. `records` and `records_fts` remain at **1928 / 1928**, `PRAGMA integrity_check = ok`, no partial inserts persisted. All three-table FTS5 transactions failed at the `db.commit()` step with `sqlite3.OperationalError: disk I/O error`.

## Root cause

Two compounding factors:

1. **Sandbox `/` (root) is at 100 %** (15 MB free of 9.6 GB). Filled by accumulated `/tmp/` artefacts from prior worker sessions (`b0591`–`b0594`, `b0597`, `b0610`, `b0611`, `b031_pdfs`, plus seven 112-MB `corpus.sqlite` snapshots = ~800 MB). All owned by previous-session UIDs and **cannot be removed from the current sandbox** (`Operation not permitted`). pdfplumber's mkstemp and sqlite's temporary spill area both end up on the full root partition even with `TMPDIR` re-routed to the corpus mount.
2. **Concurrent host-side worker writing to `corpus.sqlite`**. New `corpus.sqlite-journal` files (4 K → 57 K) regenerate within seconds of each quarantine. Quarantined journals tagged `b035-pre2-20260513T051504Z`, `b035-stale3-20260513T051528Z`, and `b0626-jiw-quarantine-T2/T3` confirm an active host-side `repair-batch-035` cycle in flight while this tick was running.

Single-row writes to `corpus_meta` succeeded intermittently in between contention windows, but the JIW insert path (`records` + `judgments_meta` + FTS5 `records_fts`, all in one transaction) reliably failed at commit time.

## Work produced (cached, not committed)

| File | Size | Notes |
|------|-----:|-------|
| `raw/zambialii/zmsc/2024/zmsc-2024-11-eng.html` | 49 KB | gap-fill candidate |
| `raw/zambialii/zmsc/2024/zmsc-2024-18-eng.html` | 41 KB | gap-fill candidate |
| `raw/zambialii/zmsc/2024/zmsc-2024-22-eng.html` | 41 KB | gap-fill candidate |
| `raw/zambialii/zmsc/2024/zmsc-2024-26-eng.html` | 44 KB | gap-fill candidate |
| `raw/zambialii/zmsc/2024/zmsc-2024-28-eng.html` | 44 KB | gap-fill candidate |
| `raw/zambialii/zmsc/2024/zmsc-2024-29-eng.html` | 47 KB | gap-fill candidate |
| `raw/zambialii/zmsc/2024/zmsc-2024-31-eng.html` | 43 KB | gap-fill candidate |
| `raw/zambialii/zmsc/2024/zmsc-2024-11-source.pdf` | 18 MB | publisher-duplicate of zmsc-9/2024 |
| `_b0626_jiw/pdfs/zmsc_11.pdf` | 18 MB | working copy |

Next-tick HTML fetch cost for the remaining 6 gaps: **zero**.

## Important finding — ZMSC 11/2024 is a publisher-side duplicate of ZMSC 9/2024

PDF parsing confirmed that ZambiaLII has published the **same** Frankson Musukwa v Road Transport and Safety Agency judgment under two ZMSC numbers (9 and 11):

|                | ZMSC 9 (in corpus, b0622-jiw)  | ZMSC 11 (b0626-jiw scout)  |
|----------------|---------------------------------|----------------------------|
| Parties        | Frankson Musukwa et al v RTSA   | Frankson Musukwa et al v RTSA |
| Appeal No.     | `Appeal No. 11 of 2021`         | `APPEAL No. 11. 2021`; `SCZ/8/18/2021` |
| Date decided   | 2024-05-16                      | 2024-05-16 |
| Coram          | Kaoma, Kajimanga, Chisanga JJS  | Kaoma, Kajimanga, Chisanga JJS |
| Outcome        | dismissed                       | dismissed |
| Pages          | (full record present)           | 44 |

**Recommended treatment:** ZMSC 11/2024 should be permanently deferred as a duplicate. Do not ingest. When `b0627-jiw` retries, dedup logic (case_number + court + year, or fuzzy case_name first-40-chars + court + year) will catch this on the wire — but the duplicate-PDF file in `raw/zambialii/zmsc/2024/` and the orphan JSON in `records/judgments/zmsc/2024/` must be renamed out of the canonical trees.

This is the **second** ZambiaLII publisher-side duplication encountered (the first was zmsc-5/2025 case-number collision, logged b0621-jiw as standing item (h)). Worth re-running a publisher-side audit against the 2024–2025 ZMSC numbering to flag any further collisions before they trigger another orphan.

## Orphan record

`records/judgments/zmsc/2024/judgment-zm-2024-zmsc-11-frankson-musukwa-suing-on-his-behalf-and-as-the-executive-di.json` was written to disk by the v2 ingest before the (failed) db commit. The file is on the corpus mount and cannot be deleted from this sandbox (FUSE EPERM, same precedent as `.git/*.lock` files). It is therefore an **orphan**: 1 JSON file on disk with no corresponding `records` / `judgments_meta` / `records_fts` row.

Classification: `deferred-fts5+meta-write` (same category as the b0591/b0593 orphans that b0612 successfully drained). Resolution path next tick: rename into `raw/zambialii/zmsc/2024/_orphan_b0626/` and document the duplicate-finding rather than re-insert.

## Counts post-b0626-jiw (unchanged from b0622-jiw)

- `records` = **1928** (Δ 0)
- `records_fts` = **1928** (Δ 0)
- CHECK1–CHECK8: not run (no inserts to validate); pre-tick CHECK8 = PASS at 1928/1928.
- PRAGMA integrity_check: ok (verified twice this tick).
- ZMSC 2024 coverage: **26 / 33** (unchanged; 7 publisher gaps remain — but ZMSC 11 is a duplicate of ZMSC 9, so effective remaining = 6).
- ZMSC overall: **100**.
- Total judgments: **238** (ZMSC 100, ZMCC 87, CoA 50, ZMHC 0, IRC 0, Subordinate 0, plus 1 misc-id).
- Corpus pool: 1928.

## Recommendations for b0627-jiw

1. **Probe sandbox `/` disk first.** If still > 99 % full, abort again with the same diagnostics and do not waste budget on retries that will fail on commit.
2. **Rename the orphan ZMSC 11 JSON** (and its source.pdf raw file) into `raw/zambialii/zmsc/2024/_orphan_b0626/` once disk is freed. Log the duplicate-finding in worker.log.
3. **Drain the cached ZMSC 2024 HTMLs**: 18, 22, 26, 28, 29, 31 (6 remaining gaps; HTMLs already on disk so only the PDFs need to be fetched).
4. **Inspect zmsc-26 vs zmsc-25** (both 2024-07-24) and **zmsc-28 vs zmsc-29** (both 2024-08-15) for the same publisher-duplication pattern before inserting either.
5. **If disk-full pattern persists**: escalate item (k) to operator as a host-side maintenance request before next JIW tick.

## Operator action items (carried forward, with two new this tick)

- (a)–(i) unchanged from b0622-jiw.
- **(j) NEW**: ZMSC 11/2024 = ZMSC 9/2024 publisher-side duplicate on ZambiaLII. Should be permanently deferred. Orphan JSON to be renamed out of canonical records tree by next tick.
- **(k) NEW**: Sandbox `/` reaches 100 % during long worker chains. Host-side cleanup of accumulated `/tmp/` artefacts required. Severity: HIGH.
