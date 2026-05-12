# Batch 0609 — JIW — Deferred-FTS5 Flush (Court of Appeal, first post-rebuild flush)

**Tick start:** 2026-05-12T08:08Z (UTC)
**Worker:** judgment-ingestion-worker (JIW)
**Phase:** priority (a) — REPARSE DEFERRED
**Session:** affectionate-dreamy-gates

## Summary

First successful ingestion since b0584 (24-tick FTS5-blocked streak ended).
Following the host-side FTS5 rebuild observed at b0607T07:09:26Z (see
`reports/batch-0607-jiw-addendum.md`), this tick flushed **4 of 4 archived
b0594 Court of Appeal records** from the deferred-fts5 backlog into the
corpus.

**Result:** +4 records, 0 skipped, 0 errors, all 8 CHECKs green, FTS5
remained healthy through the inserts.

## FTS5 health pre-flush (read-only probes)

| Probe | Result |
|-------|--------|
| `PRAGMA quick_check` | `ok` |
| `PRAGMA integrity_check` | `ok` |
| `COUNT(*) FROM records` | 1892 |
| `COUNT(*) FROM records_fts` | 1892 |
| `MIN(rowid),MAX(rowid) FROM records_fts` | (1, 1900) — dense |
| `MATCH 'court'` returns | 663 hits |

All five green — the b0607 host-side rebuild is **persistent**.

## Pre-flush actions

1. `find .git -name "*.lock" -delete` (no real `*.lock` matches; stale
   marker files with `.lock.<suffix>` are not git locks).
2. `git pull --ff-only` → "Already up to date." HEAD=`50515f8`.
3. Stale `corpus.sqlite-journal` (4,616 B) truncated in place to 0 B
   (FUSE blocks unlink — per repair-batch-029 SKILL recommendation).
4. Backup taken: `corpus.sqlite.bak.b0609-jiw-pre-flush-20260512T080937Z`
   (113.7 MiB).
5. `PRAGMA journal_mode=TRUNCATE` set on the worker connection.

## Records inserted

| ID | Case | Case No. | Date | Outcome | Body |
|----|------|----------|------|---------|-----:|
| `judgment-zm-2024-coa-024-kingfred-phiri-v-life-master-limited` | Kingfred Phiri v Life Master Limited | APP/24/2023 | 2024-12-10 | dismissed | 34,470 |
| `judgment-zm-2025-coa-039-willard-hamunyangwa-and-2-others-v-the-people` | Willard Hamunyangwa & 2 Others v The People | APP/39-40-41/2023 | 2025-02-18 | allowed | 24,555 |
| `judgment-zm-2025-coa-032-starford-chimanga-v-the-people` | Starford Chimanga v The People | APP/32/2024 | 2025-02-18 | dismissed | 20,697 |
| `judgment-zm-2025-coa-027-collins-ncube-v-the-people` | Collins Ncube v The People | APP/27/2024 | 2025-02-18 | dismissed | 17,151 |

Source: judiciaryzambia.com Court of Appeal decisions, originally fetched
2026-05-11 during JIW b0594. Parsed JSON archived at
`raw/judiciary-zm/coa/_deferred/b0594_parsed_records.json` (deferred at
that tick because the records_fts virtual table was corrupted).

Notes:
- All 4 records had `parser_version: 0.4.0-inline` at original parse.
  Re-ingestion records `parser_version: 0.4.1-inline-b0609` to mark the
  re-flush tick.
- Body text re-extracted from on-disk PDFs with pdfplumber 0.11.9.
- raw_sha256 was re-verified against on-disk PDFs before insert (CHECK6).
- The Hamunyangwa appeal is a 3-appellant consolidated criminal appeal —
  case_number captures the consolidation as `APP/39-40-41/2023`. ID slot
  039 selected (the first of the three).

## Integrity check results (CHECK1–CHECK8)

| Check | Result |
|-------|--------|
| CHECK1: every judgment has ≥1 judge | PASS |
| CHECK2: issue_tags non-empty | PASS |
| CHECK3: outcome from allowed enum | PASS |
| CHECK4: all judges resolve in registry | PASS |
| CHECK5: no duplicate IDs | PASS |
| CHECK6: raw_sha256 matches on-disk file | PASS |
| CHECK7: no duplicate (case_name,court,date) | PASS |
| CHECK8: `records` count == `records_fts` count | PASS records=1896 fts=1896 |

All 14 judges on the panels (Siavwapa, Mchenga, Chashi, Kondolo SC,
Makungu, Chishimba, Sichinga, Ngulube, Banda-Bobo, Sharpe-Phiri,
Muzenga, Patel, Chembe, Majula) already exist in `judges_registry.yaml`
from prior CoA ingestion ticks. No registry mutations were needed.

## FTS5 post-insert verification

| Probe | Result |
|-------|--------|
| `PRAGMA quick_check` | `ok` |
| `PRAGMA integrity_check` | `ok` |
| `COUNT(*) FROM records` | 1896 (+4) |
| `COUNT(*) FROM records_fts` | 1896 (+4) |
| `MATCH 'appeal'` returns | 502 hits |

FTS5 remained healthy through the inserts. **No re-corruption.** This is
the first confirmation that the host-side rebuild is durable under
write-load, not just under read-load.

## Deferred-FTS5 backlog status

| Origin tick | Original count | Flushed b0609 | Remaining | Archive status |
|-------------|--------------:|---------------:|----------:|----------------|
| b0590 | 7 | 0 | 7 | parsed JSON **NOT archived** (was in `/tmp/`); raw PDFs on disk; needs fresh parse |
| b0591 | 4 | 0 | 4 | parsed JSON **NOT archived** (was in `/tmp/`); raw PDFs on disk; needs fresh parse |
| b0592 | 3 | 0 | 3 | parsed JSON archived (older "meta"-wrapped schema) |
| b0593 | 6 | 0 | 6 (1 clean + 5 v0.4-pending) | parsed JSON archived |
| b0594 | **4** | **4** | **0** | parsed JSON archived; **fully drained this tick** |
| b0597 | 2 | 0 | 2 (date_decided=null on both — gating decision needed) | parsed JSON archived |
| **Total** | **26** | **4** | **22** | — |

## Scanned-PDF backlog (unchanged this tick)

10 records still awaiting `ocrmypdf` (b0593 Emergency Response Zambia
309/2023; b0594 ×4; b0597 ×5: sichoni, savenda, zanaco-kandala,
mutale-mukumbwa, setrec-zanaco). `ocrmypdf` is not in the worker
sandbox; defer to host.

## Court coverage update

| Court | Records (pre) | Records (post) | Delta |
|-------|--------------:|---------------:|------:|
| Supreme Court of Zambia | 92 | 92 | 0 |
| Constitutional Court of Zambia | 85 | 85 | 0 |
| Court of Appeal | 25 | **29** | **+4** |
| **All judgments** | **202** | **206** | **+4** |

## Sweep position next tick (b0610)

`judiciary-coa-sweep: page 8 remaining` — **6 unprocessed CoA candidates
on judiciaryzambia.com page 8** still pending. With FTS5 now confirmed
write-safe, b0610 should:

1. Read-only re-probe (same 5 signals) to confirm rebuild is *still*
   persistent — paranoia after 24 ticks of corruption is justified.
2. Take a fresh `corpus.sqlite.bak.b0610-pre-flush-…` backup.
3. **First-class:** Flush the remaining 22 archived-deferred records
   from the b0594 cohort siblings (b0592 ×3, b0593 ×1 clean, b0597 ×2
   with `date_decided` resolved), pushing the v0.4-pending b0593 ×5
   batch and unarchived b0590/b0591 PDFs into a separate "needs fresh
   parse" priority.
4. **Second-class:** If time allows after the flush, advance the
   page-8 sweep (6 candidates).

## Logs appended

- `costs.log`: this tick — 0 fetches, 0 bytes, kind=`jiw-flush-deferred-fts5`.
- `provenance.log`: 4 INSERT entries (records+judgments_meta+records_fts).
- `worker.log`: START/STOP entries for batch-0609 plus PRAGMA / CHECK / commit verdicts.
- `gaps.md`: sweep position update + deferred-fts5 backlog update.

## B2 sync

`rclone` not in sandbox → `deferred-to-host`.

## Worker contact

`peter@bilcoguard.com` — `KateWestonLegal-CorpusBuilder/1.0`
