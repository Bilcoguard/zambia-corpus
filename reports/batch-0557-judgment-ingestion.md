# Batch 0557 — judgment-ingestion-worker tick

- **Worker**: judgment-ingestion-worker (scheduled task `judgment-ingestion`)
- **Wall-clock window**: 2026-05-09T09:08Z..09:13Z (UTC, well under 20 min target)
- **Phase**: Phase 5 dedicated post-completion ingestion (continued).
- **Parser**: v0.3.2 baseline (no parser, fetcher, or core-logic
  modifications this tick).
- **Outcome**: **0 records written, 0 deferred, 0 fetches consumed.
  5 records_fts rows backfilled — closing the pre-existing FTS gap
  documented by repair-batch-013 as judgment-ingestion-worker domain.**

## Tick decision (priority order)

a. **REPARSE DEFERRED** — *not run this tick.* The four most recent
   reparse ticks (b0541, b0544, b0552, plus the deferral within
   b0553) all redeferred every candidate under
   `html_no_summary_pdf_no_match`. The v0.3.3-pending cohort cannot
   move under the current parser_v0.3.2 anchor inventory; authoring
   the v0.3.3 anchor additions is out-of-tick work. Running another
   redundant reparse pass with the same parser would consume tick
   wall-clock for zero progress, so this tick deliberately skips
   priority (a) in favour of closing the higher-value FTS gap below.

b. **SCZ SWEEP** — *not run this tick.* The b0547 HEAD probe
   exhausted the immediately-discoverable ZMSC-2025 frontier
   (b0553 wrote 2/3 of the {4,31,32} candidates; num 31 deferred).
   The b0550 HEAD probe of ZMSC-2024 returned 8/8 confirmed-404 in
   {4,35,36,37,38,40,45,50}. No queued GET-fetch targets remain on
   disk. Discovering further candidates would require a new HEAD
   probe pass which I'd rather sequence after the FTS gap is closed
   so the next reparse tick has a clean integrity baseline.

c. **ZMCC NEW YEARS** — *not run this tick.*

d. **FTS BACKFILL** *(taken this tick)* — repair-batch-013 (08:15Z)
   recommended that judgment-ingestion-worker backfill the 5 missing
   `records_fts` rows so the records vs records_fts gap drops from 5
   to 0. The 5 IDs are unambiguously judgment-ingestion-worker
   domain (3 added by b0541, 2 added by b0553) and the work is
   strictly local (zero fetches, zero parser changes). Closing the
   gap unblocks the repair-worker's next push of body repairs from
   b011/b013 (currently held back by the strict
   `records == records_fts` assertion).

## FTS backfill — five rows

| id | court / year / num | added by | citation |
|---|---|---|---|
| `judgment-zm-2020-zmsc-51-richard-h-chama-213-other-v-national-pension-schem` | zmsc/2020/51 | b0541 | [2020] ZMSC 51 |
| `judgment-zm-2020-zmsc-60-matias-chitigwa-mugogo-v-the-people` | zmsc/2020/60 | b0541 | [2020] ZMSC 60 |
| `judgment-zm-2020-zmsc-65-jackson-kamanga-others-v-the-people` | zmsc/2020/65 | b0541 | [2020] ZMSC 65 |
| `judgment-zm-2025-zmsc-04-minimart-development-corporation-company-limited-v` | zmsc/2025/4  | b0553 | [2025] ZMSC 4  |
| `judgment-zm-2025-zmsc-32-shaba-mulengela-and-anor-v-frank-mumba` | zmsc/2025/32 | b0553 | [2025] ZMSC 32 |

### Mechanism

Each row inserted with a pure SQL JOIN of the existing `records` and
`judgments_meta` rows — no record content was synthesised:

```sql
INSERT INTO records_fts (id, type, title, citation,
                         case_name, outcome_detail, body)
SELECT r.id, r.type, COALESCE(r.title,''),
       COALESCE(r.citation,''),
       COALESCE(j.case_name,''),
       COALESCE(j.outcome_detail,''),
       COALESCE(r.body,'')
FROM records r
LEFT JOIN judgments_meta j ON j.id = r.id
WHERE r.id = ?
```

This mirrors the column projection used by
`scripts/batch_0504_build_fts5.py` (the canonical FTS rebuild
script). The 5 records have NULL `records.body` (consistent with 54
of the 59 NULL-body judgments already in `records_fts`) — empty body
is permitted by the FTS schema and the existing population pattern
already accepts it.

### Sandbox-environment workaround

First commit attempt failed with `sqlite3.OperationalError: disk I/O
error`. Diagnosis: the sandbox filesystem (`/mnt/.virtiofs-root/...`)
permits file creation but forbids `unlink(2)` (`Operation not
permitted`). Default DELETE-mode rollback journals require unlink on
COMMIT and ROLLBACK. After confirming a manual `truncate(0)` of the
journal file works (`f.truncate(0)` succeeded), I switched the
connection to `PRAGMA journal_mode=TRUNCATE` (truncates the journal
to 0 bytes instead of unlinking it) and proceeded with per-record
commits as a belt-and-braces precaution. All 5 INSERTs succeeded
on the first commit per record. This is the same workaround pattern
repair-batch-013 used for body-repair commits (08:15Z log: "first
batched commit disk IO error recovered via per-record commits").

`PRAGMA integrity_check` returns `ok` post-tick.

### FTS sanity searches (post-tick)

| query | hits | target found |
|---|---:|---|
| `minimart` | 1 | yes |
| `mulengela` | 1 | yes |
| `mugogo` | 1 | yes |
| `kamanga` | 3 | yes |
| `"national pension"` | 23 | yes |
| `chitigwa` | 1 | yes |

## corpus.sqlite — before / after

| metric | before | after | Δ |
|---|---:|---:|---:|
| `records` | 1851 | 1851 | 0 |
| `records_fts` | 1846 | 1851 | +5 |
| `records ∖ records_fts` (gap) | 5 | **0** | −5 |
| `judgments_meta` | 161 | 161 | 0 |
| duplicate ids in `records` | 0 | 0 | 0 |
| duplicate ids in `records_fts` | 0 | 0 | 0 |

All 5 backfilled IDs were verified to have:
- a row in `records` with `type='judgment'`
- a row in `judgments_meta` with populated `case_name` and `outcome_detail`
- the canonical record JSON file on disk under `records/judgments/zmsc/...`

## Integrity checks

- ✅ Every backfilled judgment has at least one judge in its source JSON.
- ✅ `issue_tags` non-empty for all 5 records (3, 7, 1, 5, 4 tags
  respectively).
- ✅ Outcome values for all 5 are within the allowed enum
  (`allowed`, `upheld`, `dismissed`, `allowed`, `dismissed`).
- ✅ All judges in all 5 records resolve in `judges_registry.yaml`
  (Malila, Kaoma, Mambilima, Muyovwe, Chisanga, Hamaundu — all
  pre-existing canonical entries).
- ✅ No duplicate IDs in `records` or `records_fts`.
- ✅ `raw_sha256` field present and 64-hex on all 5 records (the
  hashes were verified against on-disk raw files in the original
  ingestion ticks; no re-hash this tick).
- ✅ `PRAGMA integrity_check = ok`.

## judges_registry.yaml

Untouched this tick (no new judges encountered).

## approvals.yaml

Untouched this tick (Phase 5 ceiling state unchanged at
161/160 — still one above the upper sentinel; recommend operator
extend the ceiling band or close Phase 5 on next opportunity, as
flagged by b0553).

## Costs

- Fetches this tick: **0** (zero network I/O — purely local FTS
  insert + SQLite metadata).
- `cumulative_today`: 92/500 (unchanged from b0553).

## Outstanding recommendations for next ticks

1. **Author parser_v0.3.3 anchor patterns** — out-of-tick work; the
   v0.3.3-pending cohort is now 52 records and growing each
   reparse-deferred tick. The two newly-confirmed pattern families
   (3PSP "we dismiss/allow" + SVO "grant/refuse" + declaratory
   holdings) need explicit anchor regexes added to
   `scripts/batch_0498_parse.py` before reparse can move them.
2. **Phase 5 ceiling at 161/160** — operator action: either extend
   the ceiling to 165/170 to permit further organic ZMSC sweeps, or
   close Phase 5 and start Phase 5b. Persisted observation since
   b0553.
3. **Repair-worker can now push b011/b013 body repairs** — the
   strict `records == records_fts` precondition the repair-worker
   waits on is now satisfied (1851 == 1851). Next repair-worker tick
   should be able to commit the held-back body repairs.

## B2 sync

Deferred to host (rclone not in sandbox).
