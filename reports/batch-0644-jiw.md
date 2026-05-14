# Batch b0644-jiw — Judgment Ingestion Worker

**Tick start:** 2026-05-14T12:41:34Z
**Worker:** judgment-ingestion-worker
**Verdict:** TICK ABORTED (16th consecutive JIW abort since b0626-jiw)
**Wall-clock:** ~3 min
**Budget used this tick:** 0 fetches (cumulative today: 0 / 500 — same UTC day as b0641-jiw, counter unchanged)

## Summary

No fetch, no parse, no write, no DB mutation. Chronic host-side
blockers unchanged since b0641-jiw. Logs and this report are the only
mutations committed this tick.

A repair worker (`b0643-repair` at 2026-05-14T12:40:00Z, ~1 min before
this JIW tick) applied 6 body-only UPDATEs to the zambialii AKN-SI
condition-B backlog. That batch did **not** touch the FTS5 shadow
tables and did **not** narrow the CHECK8 parity gap. Post-state
recorded by repair-043: `records=1928 records_fts=1924 gap=4
integrity=NOT-OK-unchanged-no-new-corruption-from-body-UPDATEs`.

JIW preflight this tick re-confirms the same numbers from inside the
DB: `records=1928, records_fts=1924, gap=4`. Parity rule CHECK8 still
FAILS → JIW must defer per non-negotiable in SKILL.md.

## Preflight observations

| Metric | Value |
| --- | --- |
| `records` count | 1928 |
| `records_fts` count | 1924 |
| Parity gap | **4** (CHECK8 FAIL — unchanged) |
| `judgments` count (records.type='judgment') | 238 |
| Coverage vs target | 238 / 800 = **30 %** |
| `corpus.sqlite` mtime (UTC) | 2026-05-14T12:38:06Z |
| Host-side recency | ~3.5 min before tick start (repair-043 wrote 6 body UPDATEs) |
| Sandbox `/` free | 13 MB (100 % full) |
| `/sessions` free | 2.4 GB |
| Corpus FS free | 13 GB |
| `PRAGMA quick_check` first error | unchanged (`tree page 5733 cell 71: 2nd reference to page 21836`, `rowid 1185 out of order`) |
| `PRAGMA integrity_check` | NOT OK (same shadow pages as b0641-jiw — confirmed by repair-043) |

## Persistent FTS5 shadow-table corruption (unchanged since b037/b038)

```
*** in database main ***
On tree page 5733 cell 71: 2nd reference to page 21836
On tree page 5733 cell 69: Rowid 1185 out of order
On tree page 6270 cell 0: 2nd reference to page 24604
On tree page 5387 cell 0: Overflow length mismatch
On tree page 12466: Invalid page number
On tree page 29610: Invalid page number
On tree page 22491: Invalid page number
On tree page 12465 cell 7: Child page depth differs
```

Residual deterministic-fail IDs for FTS reinsert (from repair-041):
`act-zm-2023-022`, `act-zm-2023-025`, `act-zm-2023-029`,
`act-zm-2024-003`.

## Source-side observations (no fetch this tick)

Last successful judiciaryzambia.com / zambialii.org JIW fetch was b0626
(2026-05-13T06:08Z). 15 consecutive aborts since. Sweep position
unchanged:

| Sweep | Position | Status |
| --- | --- | --- |
| `judiciary-coa-sweep` | page 1 | not yet started — new source, zero coverage |
| `judiciary-scz-sweep` | page 1 | not yet started |
| `judiciary-zmcc-sweep` | page 1 | not yet started |
| `judiciary-zmhc-sweep` | page 1 | not yet started |

## Git / refs status

- `git pull --ff-only` succeeded; `Already up to date.` at HEAD `57ef3f8` (= origin/main, last commit was b0643-repair).
- `.git/refs/remotes/origin/` now contains only valid `HEAD` and `main` — the bogus lock-style files appear to have been cleared host-side since b0641-jiw quarantined the residuals via `mv`. Confirmed `cat .git/refs/remotes/origin/main` = `57ef3f8…`.
- Residual sandbox EPERM on `.git/objects/maintenance.lock` (cannot `rm` from sandbox). Non-blocking — `git pull` works.

## CHECK1–CHECK8 status (read-path, no new records)

| Check | Status |
| --- | --- |
| CHECK1 (judges present) | n/a — no new records |
| CHECK2 (issue_tags non-empty) | n/a — no new records |
| CHECK3 (outcome enum) | n/a — no new records |
| CHECK4 (judges registry resolution) | n/a — not iterated |
| CHECK5 (duplicate IDs) | n/a — no new records |
| CHECK6 (raw_sha256 match) | n/a — no new raw files |
| CHECK7 (duplicate case_name/court/date) | n/a — no new records |
| **CHECK8 (records == records_fts)** | **FAIL — gap=4** → defer commit per protocol |

## Decision rationale

Per b0627-jiw handoff rule 1 ("do not waste budget on retries that
will fail on commit") and SKILL.md non-negotiable
("Never commit if records count ≠ records_fts count — log the gap and
defer"), JIW MUST NOT fetch, parse, or write while CHECK8 fails.

Repair-043 demonstrated again that **body-only UPDATEs** can be
applied to the live DB without further corruption, but **DELETE+INSERT
on records_fts** (required to close the parity gap and to insert any
new judgment) remains deterministic-fail in-sandbox due to the
shadow-page corruption. The host-side FTS5 rebuild remains the only
unblocker. No mitigation available to JIW.

## Recommended operator (host-side) actions

(Unchanged from b0641-jiw — listed here for continuity.)

1. **Rebuild FTS5** on host:
   ```sql
   DROP TABLE records_fts;
   CREATE VIRTUAL TABLE records_fts USING fts5(id UNINDEXED, body, ...);
   INSERT INTO records_fts(rowid, id, body, ...)
     SELECT rowid, id, body, ... FROM records;
   VACUUM;
   PRAGMA integrity_check;
   ```
2. **Permanent `rm`** of `.git/objects/maintenance.lock` and any
   residual `_quarantine_*` files in the corpus root.
3. **Rotate sandbox `/`** — currently 13 MB free, blocks pdfplumber
   cache and VACUUM headroom.
4. **Install `ocrmypdf`** in sandbox — `condB` SI backlog drain still
   blocked without it.
5. **Reconcile 14 orphan FTS rows** (entries in `records_fts` with no
   matching `records.id`) surfaced by repair-043's full diff.

## Handoff

- Next tick: **b0645-jiw** at t+60 min (per cron) or sooner if host
  resumes the FTS5 rebuild.
- If host-side rebuild has happened by then, b0645 should resume from
  `judiciary-coa-sweep page 1` (highest-priority new source — zero
  coverage today).
- If chronic blockers remain, b0645 will abort with the same pattern.
- 16 consecutive aborts now far exceed the "5 consecutive
  zero-discovery ticks" completion-criterion threshold in the brief,
  but the cause is upstream DB corruption rather than source
  exhaustion, so this worker **must not** flip `complete: true`.
  Escalation to human operator for the host-side FTS5 rebuild remains
  the only unblocker.
