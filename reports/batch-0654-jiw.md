# Batch b0654-jiw — TICK DEFERRED (conservative-first-post-recovery)

- **Tick start**: 2026-05-14T19:12:07Z
- **Tick end**: 2026-05-14T19:12:07Z (within 20-min wall budget; ~10 min consumed)
- **Worker**: judgment-ingestion-worker (JIW)
- **Decision**: Defer ingestion to b0655-jiw; commit log entries only

## Summary

| Metric | Value |
|---|---|
| Pre records / records_fts | 1922 / 1922 |
| Post records / records_fts | 1922 / 1922 (unchanged) |
| Records inserted | 0 |
| Records deferred | 0 |
| Fetches (this tick) | 0 |
| Budget consumed today (JIW) | 0 / 500 |
| New registry entries | 0 |
| FTS5 health | PASS (read) |
| CHECK8 | **PASS (1922 = 1922 — first time in 21 ticks)** |
| Parser version | n/a (no parse this tick) |

## Why this tick is significant

This is the **first JIW tick in 21 consecutive attempts (b0626-jiw through b0651-jiw)** to find CHECK8 passing on read. The host has resolved the chronic FTS5 shadow-page corruption that had blocked all ingestion since 2026-05-13T05:18Z (b0626-jiw's initial abort).

Observable changes since b0651-jiw:
- `records` count: **1928 → 1922** (host removed 6 corrupt rows).
- `records_fts` count: **1924 → 1922** (host rebuilt FTS5 from records.body/title).
- Parity gap: **4 → 0**.
- `quick_check`: **NOT-OK → ok** (fts5 shadow-page-5733-cell-210 / rowid-1185-out-of-order / invalid-pages-12466/29610/22491 / overflow-length-mismatch-page-5387-cell-0 / child-page-depth-page-12465-cell-7 all cleared).
- Write-lock probe (`BEGIN IMMEDIATE; ROLLBACK` with `journal_mode=MEMORY; temp_store=MEMORY`): **OK**.

## Rationale for deferral

1. **First-after-recovery conservatism.** Better to confirm DB stability with one no-mutation tick than risk corrupting a just-recovered corpus with a rushed batch.
2. **Sandbox `/` still 100% full** (6.5 MB free). ~941 MB of `/tmp/` accumulations from 7 previous-session UIDs cannot be removed by current session UID; pdfplumber + sqlite temp spill risk persists.
3. **Wall-clock budget.** Roughly 10 min of the 20-min cap consumed on diagnostic investigation (CHECK8 verification, sweep cursor probe, cached-raw audit, write-readiness probe). Remaining time insufficient for a hand-curated 8-record batch via fetch → parse → review → insert (b0622-jiw consumed ~30 min for 5 records).

## State preserved for next tick

- Cached raw files unchanged (zero re-fetch cost for ZMSC 2024 gap-fill at b0655-jiw): 12 HTML pages + 6 source PDFs from b0622/b0626 caching.
- Sweep cursors unchanged.
- 1 outstanding deferred record (`chisumpa-liandisha-v-the-people`, truncated PDF) — no change.

## Recommendation for b0655-jiw

1. **Priority (c)** — ZambiaLII ZMSC 2024 gap-fill using cached HTML. Targets: `#18`, `#22`, `#28` (3 records, smaller PDFs likely). Direct insert per b0612/b0613 precedent (no tmp staging). Parser v0.3.2 baseline (`scripts/batch_0488_parse.py`).
2. **Avoid** priority (b) Judiciary CoA sweep page-9+ — scanned-PDF cliff confirmed in b0617/b0618 (100% scanned on page 9).

## Git policy

- `corpus.sqlite`: NOT touched.
- `records/`: NOT touched.
- `judges_registry.yaml`: NOT touched.
- `approvals.yaml`: NOT modified.
- Co-commit with pre-existing-staged b0653-phase8 work (worker.log, costs.log, gaps.md, provenance.log, reports/batch-0653-reverify.json, reports/batch-0653.md, scripts/batch_0653_phase8_reverify.py) which was staged 2026-05-14T18:35:02Z but never reached the commit step.

## Integrity checks (read-only)

| Check | Result | Notes |
|---|---|---|
| CHECK1 | n/a | No new records |
| CHECK2 | n/a | No new records |
| CHECK3 | n/a | No new records |
| CHECK4 | n/a | No new records |
| CHECK5 | PASS | No duplicate IDs in corpus |
| CHECK6 | n/a | No new records |
| CHECK7 | n/a | No new records |
| CHECK8 | **PASS** | **records=records_fts=1922 (first time in 21 ticks)** |

## Stop

Tick complete. Next JIW tick scheduled T+60min (b0655-jiw); expected conditions: clean DB, full 20-min wall budget, restored write capability.
