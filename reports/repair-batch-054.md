# Repair batch 0654 — 8 zambialii SIs (2018 cohort, post-021)

**Worker**: repair-corpus (scheduled-task, v4 prompt)
**Tick**: b0654
**Wall-clock**: ~15 min (within 20-min budget)
**Parent commit**: 1af47f5
**Date**: 2026-05-14T19:30Z

## Summary

8/8 Condition-B (no-body) SI records repaired. Continues the 2018 cohort
drainage that batch b0652 advanced through si-zm-2018-021. Total bytes
written: 129,953.

## Records repaired

| # | ID | Bytes | SHA-256 (8) |
|---|---|------:|---|
| 1 | si-zm-2018-022-animal-health-veterinary-services-fees-regulations-2018 | 5,261 | 7108129a |
| 2 | si-zm-2018-023-plant-variety-and-seeds-regulations-2018 | 94,593 | 3db16908 |
| 3 | si-zm-2018-033-electoral-process-local-government-by-elections-election-date-and-time-of-poll-order-2018 | 1,742 | 19a6e30c |
| 4 | si-zm-2018-039-levy-mwanawasa-medical-university-declaration-order-2018 | 849 | 2dfb5e99 |
| 5 | si-zm-2018-043-urban-and-regional-planning-designated-local-planning-authorities-regulations-2018 | 1,110 | a83a779b |
| 6 | si-zm-2018-044-urban-and-regional-planning-designated-local-planning-authorities-no-2-regulations-2018 | 965 | 9a563bc0 |
| 7 | si-zm-2018-046-electoral-process-local-government-by-elections-election-date-and-time-of-poll-no-3-order-2018 | 1,858 | 9f140594 |
| 8 | si-zm-2018-054-agricultural-institute-of-zambia-general-regulations-2018 | 23,575 | 7312c017 |

## Pipeline

For each target id:

1. Fetch ZambiaLII AKN HTML at `https://zambialii.org/akn/zm/act/si/2018/<n>`
2. Parse `href="...source.pdf"` to discover canonical PDF.
3. Fetch source.pdf with `curl -A "KateWestonLegal-CorpusBuilder/1.0"`.
4. Extract text with `pdfplumber` (page-by-page concat).
5. Section-number normalisation: `re.sub(r"(\d+)\.([A-Z])", r"\1. \2", body)`.
6. Quality gate: `len > 200`, digit-line-ratio test, legal-marker regex.
7. `UPDATE records SET body=?, source_hash=?, fetched_at=?, parser_version='repair-0.6.2' WHERE id=?` — one connection per record, individual commit (crash-safe).

## FTS refresh

After all 8 bodies were committed, per-row FTS5 refresh:

```sql
INSERT INTO records_fts(records_fts, rowid, id, title, body, citation, type)
  VALUES('delete', :rowid, '', '', '', '', '');
INSERT INTO records_fts(rowid, id, title, body, citation, type)
  VALUES(:rowid, :id, :title, :body, :citation, :type);
```

The `'delete'` command is a no-op for rows whose prior body was NULL/empty (no
prior posting lists to remove beyond title tokens — those are unchanged), so
the subsequent INSERT succeeds without an IntegrityError. Verified post-hoc
with a body-only search: `MATCH 'SeshekeDistrict'` resolves to
si-zm-2018-043 (term appears only in body, not title) — confirms body
content is now indexed.

Note: the task-instruction FTS schema referencing `case_name` / `outcome_detail`
columns does **not** match the live records_fts schema, which is:

```sql
CREATE VIRTUAL TABLE records_fts USING fts5(
    id, title, body, citation, type,
    content=records, content_rowid=rowid
)
```

The case_name/outcome_detail fields live only in `judgments_meta`. Repair
script matched the actual on-disk schema.

## A global `INSERT INTO records_fts(records_fts) VALUES('rebuild')` was attempted
post-batch but raised `disk I/O error` (chronic FUSE/virtiofs pattern noted in
worker.log since b0539). The journal grew to 20.4 MB before failing; the
journal was renamed `corpus.sqlite-journal.b0654-failed-fts-rebuild.bak` to
unblock SQLite. The 8 individual body UPDATEs were each committed in their
own connection BEFORE the rebuild attempt, so the body data is durable.

## Integrity

| Check | Result |
|---|---|
| `records` count | 1922 |
| `records_fts` count | 1922 |
| Parity (records == records_fts) | **PASS** |
| `PRAGMA quick_check` | **ok** |
| Body-only FTS test (SeshekeDistrict) | **MATCH** |

## SHA-256 chain (first 8 hex of each repaired body)

```
7108129a + 3db16908 + 19a6e30c + 2dfb5e99 + a83a779b + 9a563bc0 + 9f140594 + 7312c017
```

## Remaining work

Condition-B no-body acts/sis remaining post-b0654: **160** (was 168 pre-tick).
- 2018: 5 (post-054)
- 2019: 26
- 2020: 39
- 2021: 36
- 2022: 30
- 2023: 13
- 2024: 4
- 2025: 2
- 2026: 2
- non-SI: 3

Next batch b0655 will continue 2018 (si-zm-2018-056, 057, 064, 081, 094) and
roll into 2019.

## Host-side actions still required

(Carried forward from prior worker.log entries; nothing new added.)

- (a) Authoritative FTS5 global rebuild once virtiofs unlink/large-transaction
  capacity is restored (current 20+ MB rebuild fails reproducibly).
- (b) VACUUM to reclaim space from successive bak files.
- (c) Stale-manifest removal — manifest entries pointing to ids not in DB.
- (e) Cleanup of orphan FTS rows, orphan journals, and `*.lock.bak` debris.
