# Batch b0633-jiw — JIW Tick Aborted (7th consecutive)

**Date:** 2026-05-13T14:08:00Z
**Worker:** judgment-ingestion-worker
**Verdict:** tick aborted pre-fetch — no corpus mutation
**Wall clock:** ~2 minutes

## Summary

This is the 7th consecutive JIW tick to abort (after b0626, b0627, b0629,
b0630, b0631, b0632). The chronic host-side blockers identified in
b0630-jiw and re-confirmed in b0631/b0632 remain unchanged. Repair-batch-042
ran in the intervening hour and applied 6 body updates to the Condition-B
SI no-body backlog, but did not touch the parity gap (UPDATE-only fallback;
no FTS DELETE+INSERT attempted).

## Pre-flight checks

| Check | Status | Detail |
|-------|--------|--------|
| `git pull --ff-only` | OK | Already up to date with origin/main |
| `.git/*.lock` cleanup | EPERM | maintenance.lock, ORIG_HEAD.lock, index.lock all FUSE-blocked (benign) |
| Daily budget | OK | 21 / 500 fetches today (well under) |
| Sandbox `/` disk | **FAIL** | 14 MB free / 100% used |
| `/sessions` disk | OK | 2.4 GB free |
| `corpus.sqlite` mtime | quiescent | 2026-05-13T14:36:48Z (~30 min ago) |
| `PRAGMA quick_check` | **FAIL** | tree page 5733 cell 71 → page 21836; extensive invalid-page errors on pages 12466 / 29610 / 22491 |
| `PRAGMA integrity_check` | **FAIL** | same signature, unchanged since b037/b038 |
| CHECK8 parity | **FAIL** | records=1928, records_fts=1924, gap=4 |

## Decision rationale

Per the protocol Step 7 non-negotiable: *"Never commit if `records` count ≠
`records_fts` count — log the gap and defer."* And per the b0627-jiw
handoff rule 1: *do not waste budget on retries that will fail on commit.*

The chronic blockers are deterministic and identical to the prior 6 ticks:

1. **CHECK8 parity gap (=4).** Residual missing FTS rows are
   `act-zm-2023-022`, `act-zm-2023-025`, `act-zm-2023-029`,
   `act-zm-2024-003`. Repair-040 reduced gap from 8 to 4 via PERSIST-mode
   workaround; repair-041 and repair-042 confirmed deterministic FTS INSERT
   failure for these 4 IDs against the malformed shadow table.
2. **SQLite integrity NOT OK.** FTS5 shadow corruption on page 5733 and an
   ever-widening invalid-page-number cohort on pages 12466 / 29610 / 22491.
   This blocks any multi-row transaction touching `records_fts`.
3. **Sandbox `/` disk 100% full (14 MB free).** Insufficient headroom for
   `pdfplumber` cache, `pypdf` temp files, or `VACUUM` on a 116 MB DB.
4. **Host-side fix still pending.** No evidence in
   `corpus.sqlite` mtime or commit log of a DROP+CREATE+INSERT-SELECT
   rebuild attempt since the handoff was first written in b0630-jiw.

Therefore: abort tick, no fetch, no parse, no write, no commit of
`corpus.sqlite`. Stage only worker.log / costs.log / gaps.md / this
report — same pattern as b0631-jiw and b0632-jiw.

## Integrity checks (read path)

| Check | Status |
|-------|--------|
| 1 — every judgment has ≥1 judge | n/a (no writes) |
| 2 — `issue_tags` non-empty | n/a (no writes) |
| 3 — `outcome` in enum | n/a (no writes) |
| 4 — judges resolve in registry | n/a (no writes) |
| 5 — no duplicate IDs | OK on existing 1928 records |
| 6 — `raw_sha256` matches on-disk | n/a (no new raw files) |
| 7 — no duplicate case_name+court+date | OK on existing 1928 records |
| 8 — `records == records_fts` | **FAIL** (1928 vs 1924, gap=4) |

## Repair-worker progress in the intervening hour

`repair-batch-042` at 14:35:30Z:

- Applied 6 `records.body` UPDATEs to Condition-B SI no-body backlog:
  - `si-zm-1980-049-zambia-national-provident-fund-statutory-contributions-regulations-1980` (0 → 7244 chars)
  - `si-zm-1981-047-zambia-national-service-obligatory-service-exemption-order-1981` (0 → 1078)
  - `si-zm-1982-049-zambia-airways-corporation-date-of-dissolution-order-1982` (0 → 943)
  - `si-zm-1985-014-equity-levy-exemption-order-1985` (0 → 808)
  - `si-zm-1985-024-air-passenger-service-charge-appointment-of-collection-agents-no-2-order-1985` (0 → 1049)
  - `si-zm-1985-045-air-services-aerial-application-permit-regulations-1985` (0 → 4106)
- 2 FETCH_FAILs on scanned PDFs:
  `local-courts-administration-of-estates-rules-1969` (1 char extracted)
  and `local-courts-rules-1966` (24 chars). `ocrmypdf` still absent.
- Condition-B SI backlog: 232 → 226 remaining.
- Parity gap: unchanged at 4.

This is informational; it does not unblock the JIW write path.

## Sweep position (unchanged since b0622-jiw)

- **ZambiaLII ZMSC 2024** gap-fill: 26/33 ingested; next IDs #11, #12, #14.
- **judiciaryzambia.com Court of Appeal**: page 1 not yet started.
  Highest-priority NEW source per Step 3(b).
- **judiciaryzambia.com Constitutional / Supreme / High Court**: not yet
  started; defer until host FTS rebuild lands.
- **judiciaryzambia.com Subordinate Court**: lowest priority; defer.

## Recommendation to host operator (unchanged)

1. Run offline FTS5 rebuild:

   ```sql
   PRAGMA journal_mode = PERSIST;
   DROP TABLE records_fts;
   CREATE VIRTUAL TABLE records_fts USING fts5(
     id, title, body, court, citation, case_number, case_name,
     content='records', content_rowid='rowid'
   );
   INSERT INTO records_fts(rowid, id, title, body, court, citation,
                            case_number, case_name)
     SELECT rowid, id, title, body, court, citation,
            case_number, case_name FROM records;
   VACUUM;
   PRAGMA integrity_check;
   ```

2. Rotate sandbox `/` cache: clear `_stale_locks_*`, old
   `corpus.sqlite.bak.*`, stale `_repair_b03N_*` workspaces,
   `_b0612_jiw_inline.py` and similar ad-hoc scripts.
3. Install `ocrmypdf` to clear the 2 scanned-PDF Condition-B IDs and the
   broader ZambiaLII image-PDF cohort.
4. Confirm `integrity_check = ok` AND `records = records_fts` before next
   JIW tick.

## Pattern observation

Seven consecutive JIW aborts on the same blocker set. The repair-worker
continues to make forward progress on Condition-B body backfill at ~6
records per tick but cannot rebuild the FTS shadow table from inside the
sandbox (insufficient `/` disk for `VACUUM` headroom; DELETE+INSERT against
the malformed shadow pages fails deterministically). Until a host-side
rebuild lands, JIW remains permanently blocked on the "new INSERT must
touch `records_fts`" path. This worker has produced no new judgments
since b0626-jiw (cumulative 0/8 of the 7-tick MAX_BATCH_SIZE budget).

## Citations / sources accessed

None this tick (zero fetches).

## UA

`KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)`
