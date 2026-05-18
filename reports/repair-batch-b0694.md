# Repair batch b0694

- **Batch**: b0694
- **Date**: 2026-05-18
- **Worker**: scheduled-task `repair-corpus` (Repair Corpus Worker v4)
- **Session**: affectionate-optimistic-fermi
- **Predecessor**: b0692 (NO-MUTATION; ZambiaLII was returning HTTP 500)
- **Parser version**: repair-0.6.94

## Summary

| Metric                | Value                                          |
| --------------------- | ---------------------------------------------- |
| Targets identified    | 81 (SIs with no body — all zambialii.org AKN-SI) |
| Repaired this tick    | 8                                              |
| Failed this tick      | 0                                              |
| Remaining after tick  | 73                                             |
| Elapsed sec (extract) | 23.4                             |
| records count         | 1936                                 |
| records_fts count     | 1936                             |
| Integrity (sums)      | PASS (records == records_fts)                  |
| `PRAGMA quick_check`  | ok                             |
| Tick verdict          | MUTATION; 8 SIs body+FTS rebuilt               |

## Identification

Ran all three live SQL queries against `corpus.sqlite` (per v4 SKILL.md Step 2):

- **Condition A** (digit-ratio corrupted body): **0 found**
- **Condition B** (no body, type IN ('act','si')): **81 found** — all zambialii.org AKN-SI URLs (judgments-with-no-body skipped per v4 rule; those are JIW territory)
- **Condition C** (stub body, length < 200): **0 found**

These are the same 81 records that b0691/b0692 were blocked on by the upstream ZambiaLII HTTP 500 outage. As of this tick (2026-05-18 ~09:28 UTC) the site is back online and returning 200 with the usual AKN HTML + linked `source.pdf`.

## Upstream status

ZambiaLII probed at start of tick: `GET https://zambialii.org/akn/zm/act/si/2021/24` → 302 → 200 (40,502 bytes). Recovery confirmed. The 13,640-byte 500 error page no longer appears.

## Records repaired

| # | ID | Source URL | Body bytes |
| - | -- | ---------- | ---------- |
| 1 | si-zm-2021-024-electricity-common-carrier-declaration-regulations-2021 | https://zambialii.org/akn/zm/act/si/2021/24 | 4,601 |
| 2 | si-zm-2021-025-animal-health-destruction-of-pigs-compensation-order-2021 | https://zambialii.org/akn/zm/act/si/2021/25 | 4,277 |
| 3 | si-zm-2021-035-citizens-economic-empowerment-transportation-of-heavy-and-bulk-commodities-by-road-reservation-regulations-2021 | https://zambialii.org/akn/zm/act/si/2021/35 | 4,922 |
| 4 | si-zm-2021-037-zambia-medicines-and-medical-supplies-agency-re-engagement-of-staff-regulations-2021 | https://zambialii.org/akn/zm/act/si/2021/37 | 1,643 |
| 5 | si-zm-2021-040-electoral-process-general-election-election-date-and-time-of-poll-order-2021 | https://zambialii.org/akn/zm/act/si/2021/40 | 2,355 |
| 6 | si-zm-2021-049-zambia-institute-of-advanced-legal-education-students-rules-2021 | https://zambialii.org/akn/zm/act/si/2021/49 | 44,932 |
| 7 | si-zm-2021-052-cyber-security-and-cyber-crimes-national-cyber-security-advisory-and-coordination-council-regulations-2021 | https://zambialii.org/akn/zm/act/si/2021/52 | 8,737 |
| 8 | si-zm-2021-055-metrology-measuring-instruments-regulations-2021 | https://zambialii.org/akn/zm/act/si/2021/55 | 68,365 |

All eight repaired via the `source.pdf` route (ZambiaLII linked PDF found by
regex against the `data-pdf` / `href` attributes, downloaded via `requests`,
extracted with `pdfplumber`, passed the >200-char threshold and the digit-ratio
quality gate on the first attempt — no OCR fallback required).

## Sandbox quirks encountered (and resolved)

This tick had two non-trivial environment issues that consumed time before
repairs could begin. Both are now documented for future ticks.

### 1. `records_fts` schema drift vs SKILL.md (resolved)

SKILL.md v4 Step 4 prescribes an FTS rebuild SQL referencing columns
`case_name` and `outcome_detail`. The live `records_fts` table is FTS5 with
`content=records, content_rowid=rowid` and only carries
`(id, title, body, citation, type)`. The first repair pass aborted on every
record with `table records_fts has no column named case_name`.

**Fix applied** (script-local, no DB schema change): rebuild a single FTS row
via

```sql
DELETE FROM records_fts WHERE id = ?;
INSERT INTO records_fts (rowid, id, title, body, citation, type)
  SELECT rowid, id, title, body, citation, type FROM records WHERE id = ?;
```

SKILL.md should be amended in a future skill-creator pass — flagged in
`gaps.md`.

### 2. virtiofs hot-journal recovery refused (`disk I/O error`) — worked around

The first failed repair pass left a 94,904-byte SQLite hot journal
(`corpus.sqlite-journal` with magic `d9d505f920a163d7…`). Subsequent connections
attempting rollback returned `sqlite3.OperationalError: disk I/O error`. Probing
the underlying virtiofs mount (`/mnt/.virtiofs-root/.../KateWestonCorpus/corpus`)
showed:

- `touch` and `mv` succeed on new files
- `rm` returns `Operation not permitted` on any file
- `os.open(O_CREAT)` creates the file but EPERMs on subsequent `unlink`/`close`
- SQLite `COMMIT` succeeds **only** with `journal_mode=MEMORY` and
  `synchronous=OFF` (rollback-file journaling failed at the `unlink`/`fsync`
  step at COMMIT)

**Workaround applied** for this tick (in `scripts/repair_b0694.py`):

```python
PRAGMA journal_mode=MEMORY;
PRAGMA synchronous=OFF;
PRAGMA busy_timeout=60000;
```

Crash-durability is reduced to the duration of the script — the post-commit
`git push` re-establishes durability via the remote. The stale hot journal from
the first pass was renamed to `_stale_b0694_corpus.sqlite-journal*` so a fresh
session no longer sees it as hot.

Recommendation for the host: either grant write+unlink on the corpus mount
(matching the worker process UID) or pre-configure WAL mode on a tmpfs-backed
temp dir. Flagged in `gaps.md`.

## Integrity

- `records`: 1936
- `records_fts`: 1936 (match ✓)
- `PRAGMA quick_check`: ok
- FTS smoke test: `electricity AND carrier` hits both
  `si-zm-2021-024-electricity-common-carrier-declaration-regulations-2021`
  (repaired this tick) and the parent `act-zm-2019-011-electricity-act-2019`.

## Files changed

- `corpus.sqlite` — 8 row updates (body, source_hash, fetched_at,
  parser_version) + 8 FTS row rebuilds
- `worker.log`, `gaps.md`, `costs.log` — appended
- `scripts/repair_b0694.py` — new this tick
- `reports/repair-batch-b0694.md`,
  `reports/repair-batch-b0694-summary.json` — new this tick

## Next tick

- 73 zambialii AKN-SI no-body records remain. Same source-pdf route should
  drain another 8 per tick at ~3 sec each.
- Re-probe ZambiaLII before each batch — the outage history (b0691, b0692)
  suggests the site is still unstable.
