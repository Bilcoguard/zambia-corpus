# Batch b0645-jiw — Judgment Ingestion Worker

**Tick start:** 2026-05-14T13:07:53Z
**Worker:** judgment-ingestion-worker
**Verdict:** TICK ABORTED (17th consecutive JIW abort since b0626-jiw)
**Wall-clock:** ~3 min
**Budget used this tick:** 0 fetches (cumulative JIW today: 0 / 500)

## Summary

No fetch, no parse, no write, no DB mutation. Chronic host-side
blockers unchanged since b0641-jiw / b0644-jiw. Logs and this report
are the only mutations committed this tick.

`b0644-repair` ran ~16 min before this tick (start 2026-05-14T12:51:23Z,
commit `40ccb2d`) applying **8 body-only UPDATEs** to the zambialii
AKN-SI condition-B backlog (1993–1998 cohort). The repair worker used
`PRAGMA journal_mode=MEMORY` to bypass the new FUSE-bindfs sandbox
`rm`-deny on `corpus.sqlite-journal`, but produced 4 orphan journals
from earlier failed attempts (`b0644-orphan{,2,3,4}`). That repair
batch did **not** touch FTS5 and did **not** narrow the CHECK8 parity
gap.

JIW preflight this tick re-confirms the same numbers from inside the
DB: `records=1928, records_fts=1924, gap=4`. Parity rule CHECK8 still
FAILS → JIW must defer per non-negotiable in SKILL.md.

## Preflight observations

| Metric | Value |
| --- | --- |
| `records` count | 1928 |
| `records_fts` count | 1924 |
| Parity gap | **4** (CHECK8 FAIL — unchanged since repair-040) |
| `judgments` count (records.type='judgment') | 238 |
| Coverage vs target | 238 / 800 = **30 %** |
| `corpus.sqlite` mtime (UTC) | 2026-05-14T12:50:43Z |
| Host-side recency | ~17 min before tick start (repair-044 wrote 8 body UPDATEs) |
| Sandbox `/` free | 6.6 MB (100 % full) |
| `/sessions` free | 2.4 GB |
| Corpus FS free | 13 GB |
| `PRAGMA quick_check` first error | unchanged (`tree page 5733 cell 77: 2nd reference to page 21836`, `Rowid 1185 out of order`) |
| `PRAGMA integrity_check` | NOT OK — same shadow pages as b0644-jiw / b0641-jiw (confirmed read-only by repair-044) |

## Persistent FTS5 shadow-table corruption (unchanged since b037/b038)

```
*** in database main ***
On tree page 5733 cell 77: 2nd reference to page 21836
On tree page 5733 cell 75: Rowid 1185 out of order
On tree page 6270 cell 0:  2nd reference to page 24604
On tree page 5387 cell 0:  overflow length 1 should be 3
On tree page 12466 cell 7: invalid page number 30645
On tree page 12466 cell 6: invalid page number 30224
On tree page 22491 cell 0: 2nd reference to page 24620
On tree page 29610 cell 4: invalid page number 30242
On tree page 12465 cell 7: Child page depth differs
```

Residual deterministic-fail IDs for FTS reinsert (from repair-041):
`act-zm-2023-022`, `act-zm-2023-025`, `act-zm-2023-029`,
`act-zm-2024-003`.

## New observation this tick

**Sandbox `/` headroom shrinking further.** b0644-jiw recorded 13 MB
free at 12:41:34Z. This tick at 13:07:53Z records **6.6 MB** free —
roughly half remaining over a 26-minute window with no JIW activity.
The drift is from Python/pip/cache writes by ambient sandbox processes
(not corpus-related). At this rate, an OOD condition on `/` is likely
inside 24 h and will start blocking even read-only sqlite cursors.
**Escalated to operator-action list (item 6) below.**

## Source-side observations (no fetch this tick)

Last successful judiciaryzambia.com / zambialii.org JIW fetch was b0626
(2026-05-13T06:08Z). 17 consecutive aborts since. Sweep position
unchanged:

| Sweep | Position | Status |
| --- | --- | --- |
| `judiciary-coa-sweep` | page 1 | not yet started — new source, zero coverage |
| `judiciary-scz-sweep` | page 1 | not yet started |
| `judiciary-zmcc-sweep` | page 1 | not yet started |
| `judiciary-zmhc-sweep` | page 1 | not yet started |

## Git / refs status

- `git pull --ff-only` succeeded; `Already up to date.` at HEAD `40ccb2d`
  (= origin/main, last commit `Repair batch 044: fixed 8 SI bodies
  (1993-1998 cohort)`).
- `.git/refs/remotes/origin/` clean — only valid `HEAD` and `main`.
  Bogus lock-style refs are not re-appearing — `host-side rm` since
  b0641 appears to have held.
- Residual sandbox EPERM on `.git/objects/maintenance.lock`
  (cannot `rm` from sandbox). Non-blocking — `git pull` works.
- 4 orphan `corpus.sqlite-journal.b0644-orphan*` files left by
  repair-044 are still on disk (sandbox cannot `rm` them — new
  bindfs deny). Operator action 5 below.

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
will fail on commit") and SKILL.md non-negotiable ("Never commit if
records count ≠ records_fts count — log the gap and defer"), JIW MUST
NOT fetch, parse, or write while CHECK8 fails.

Repair-044 demonstrated **again** that **body-only UPDATEs** can be
applied to the live DB without further corruption when run with
`journal_mode=MEMORY`. But **DELETE+INSERT on records_fts** (required
to close the parity gap and to insert any new judgment) remains
deterministic-fail in-sandbox due to the shadow-page corruption. The
host-side FTS5 rebuild remains the only unblocker. No mitigation
available to JIW.

Priority (a) "reparse deferred" was considered. Every reparse would
INSERT into `records` AND `records_fts` — and a fresh FTS insert
exercises the same shadow pages that fail. Therefore reparse is also
blocked by CHECK8 / FTS corruption, not by lack of raw material.

## Recommended operator (host-side) actions

1. **Rebuild FTS5** on host (top priority — only unblocker for JIW):
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
3. **Rotate sandbox `/`** — currently **6.6 MB** free (down from 13 MB
   one tick ago). Blocks pdfplumber cache and VACUUM headroom.
4. **Install `ocrmypdf`** in sandbox — `condB` SI backlog drain still
   blocked without it.
5. **Cleanup orphan journals** (`corpus.sqlite-journal.b035-*`,
   `b0602-*`, `b0626-*`, `b0644-orphan{,2,3,4}-*`). Sandbox cannot
   `rm` these under the new bindfs deny — must be host-side.
6. **Reconcile 14 orphan FTS rows** (entries in `records_fts` with no
   matching `records.id`) surfaced by repair-043's full diff.

## Handoff

- Next tick: **b0646-jiw** at t+60 min (per cron) or sooner if host
  resumes the FTS5 rebuild.
- If host-side rebuild has happened by then, b0646 should resume from
  `judiciary-coa-sweep page 1` (highest-priority new source — zero
  coverage today).
- If chronic blockers remain, b0646 will abort with the same pattern.
- 17 consecutive aborts now far exceed the "5 consecutive
  zero-discovery ticks" completion-criterion threshold in the brief,
  but the cause is upstream DB corruption rather than source
  exhaustion, so this worker **must not** flip `complete: true`.
  Escalation to human operator for the host-side FTS5 rebuild remains
  the only unblocker.
