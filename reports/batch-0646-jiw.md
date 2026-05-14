# Batch b0646-jiw — Judgment Ingestion Worker

**Tick start:** 2026-05-14T14:08:53Z
**Worker:** judgment-ingestion-worker
**Verdict:** TICK ABORTED (18th consecutive JIW abort since b0626-jiw)
**Wall-clock:** ~3 min
**Budget used this tick:** 0 fetches (cumulative JIW today: 0 / 500)

## Summary

No fetch, no parse, no write, no DB mutation. Chronic host-side
blockers unchanged since b0641-jiw / b0644-jiw / b0645-jiw. Logs and
this report are the only mutations committed this tick.

`b0645-repair` ran ~55 min before this tick (commit `a21fdb4`,
2026-05-14T13:11:30Z UTC — note the worker.log/costs.log timestamp
strings carry a chronic local-time-mislabelled-as-Z offset documented
since b0641-jiw). It applied **8 body-only UPDATEs** to the
zambialii AKN-SI 2001–2009 cohort using `PRAGMA journal_mode=MEMORY`
to bypass the FUSE-bindfs sandbox `rm`-deny on `corpus.sqlite-journal`.
That repair batch did **not** touch FTS5 and did **not** narrow the
CHECK8 parity gap.

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
| `corpus.sqlite` mtime (UTC) | 2026-05-14T13:13:52Z |
| Host-side recency | ~55 min before tick start (repair-045 wrote 8 body UPDATEs) |
| Sandbox `/` free | 6.6 MB (100 % full — unchanged from b0645-jiw) |
| `/sessions` free | 2.4 GB |
| Corpus FS free | 13 GB |
| `PRAGMA quick_check` first error | `tree page 5733 cell 82: 2nd reference to page 21836` |
| `PRAGMA integrity_check` | NOT OK — same shadow pages as b0641-jiw / b0644-jiw / b0645-jiw |

## Persistent FTS5 shadow-table corruption (unchanged since b037/b038)

```
*** in database main ***
On tree page 5733 cell 82: 2nd reference to page 21836
On tree page 5733 cell 80: Rowid 1185 out of order
On tree page 6270 cell 0:  2nd reference to page 24604
On tree page 5387 cell 0:  overflow list length is 1 but should be 3
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

**Sandbox `/` headroom stable at 6.6 MB.** b0645-jiw recorded 6.6 MB
free; this tick remains 6.6 MB. No further drift over the ~60 minute
window. Still critically low — pdfplumber/sqlite VACUUM and any pip
operation in-sandbox will fail. **Escalated to operator-action list
(item 3) below.**

## Source-side observations (no fetch this tick)

Last successful judiciaryzambia.com / zambialii.org JIW fetch was b0626
(2026-05-13T06:08Z). 18 consecutive aborts since. Sweep position
unchanged:

| Sweep | Position | Status |
| --- | --- | --- |
| `judiciary-coa-sweep` | page 1 | not yet started — new source, zero coverage |
| `judiciary-scz-sweep` | page 1 | not yet started |
| `judiciary-zmcc-sweep` | page 1 | not yet started |
| `judiciary-zmhc-sweep` | page 1 | not yet started |

## Git / refs status

- `git pull --ff-only` succeeded; `Already up to date.` at HEAD `a21fdb4`
  (= origin/main, last commit `Repair batch 045: fixed 8 records
  (zambialii SIs 2001-2009 cohort, body-only)`).
- `.git/refs/heads/` contains only `main`. `.git/refs/remotes/origin/`
  contains only `HEAD` and `main`. Bogus lock-style refs are not
  re-appearing — `host-side rm` since b0641 continues to hold.
- Residual sandbox EPERM on `.git/objects/maintenance.lock`
  (cannot `rm` from sandbox). Non-blocking — `git pull` works.
- 9 `.git/*.lock.bak.b0644*` and `.git/*.lock.bak.b0645*` quarantine
  files remain in `.git/` (cannot be removed from sandbox). They are
  inert — git operations do not reference them.
- `.git/index.lock` ABSENT this tick — no concurrent commit in flight.
- 13 orphan `corpus.sqlite-journal.*` files on disk
  (b035-x5, b0602-x2, b0626-x2, b0644-orphan{,2,3,4}). Sandbox cannot
  `rm` them — bindfs deny. Operator action 5 below.

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

Repair-045 demonstrated **again** that **body-only UPDATEs** can be
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
   residual `.lock.bak.*` files in `.git/`.
3. **Rotate sandbox `/`** — currently **6.6 MB** free. Blocks
   pdfplumber cache and VACUUM headroom.
4. **Install `ocrmypdf`** in sandbox — `condB` SI backlog drain still
   blocked without it.
5. **Cleanup 13 orphan journals**
   (`corpus.sqlite-journal.b035-*` × 5, `b0602-*` × 2, `b0626-*` × 2,
   `b0644-orphan{,2,3,4}-*` × 4). Sandbox cannot `rm` these under the
   bindfs deny — must be host-side.
6. **Reconcile 14 orphan FTS rows** (entries in `records_fts` with no
   matching `records.id`) surfaced by repair-043's full diff.

## Handoff

- Next tick: **b0647-jiw** at t+60 min (per cron) or sooner if host
  resumes the FTS5 rebuild.
- If host-side rebuild has happened by then, b0647 should resume from
  `judiciary-coa-sweep page 1` (highest-priority new source — zero
  coverage today).
- If chronic blockers remain, b0647 will abort with the same pattern.
- 18 consecutive aborts now far exceed the "5 consecutive
  zero-discovery ticks" completion-criterion threshold in the brief,
  but the cause is upstream DB corruption rather than source
  exhaustion, so this worker **must not** flip `complete: true`.
  Escalation to human operator for the host-side FTS5 rebuild remains
  the only unblocker.
