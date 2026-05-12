# Batch 0607 — JIW — Post-tick discovery addendum

**Discovery time:** 2026-05-12T07:11:30Z (UTC) — after b0607-jiw STOP entry pushed
**Type:** out-of-band corpus.sqlite modification by host

## Summary

Between this tick's read-only probe (07:06:52Z) and the routine post-push
re-probe (07:11Z), `corpus.sqlite` was modified externally. The modification
appears to be the **records-table dump-and-rebuild** that has been requested in
twelve prior operator escalations (b0590 → b0606). The rebuild was executed
during the tick window — not by JIW (no schema mutations originated from this
worker; the b0607 main report verdict of "no mutations this tick" is accurate
for JIW-originated changes).

## Re-probe (read-only, `mode=ro` URI flag)

```
mtime              = 2026-05-12T07:09:26Z (CAT 09:09:26.007833475 +0200)
size               = 118,599,680 bytes (was 116,457,472 — delta +2,142,208)
md5(corpus.sqlite) = a9af40f02b8cb82a20eb49a5f893d820   (was 686f8197...)
PRAGMA integrity_check
                   → "ok"        (full DB; was records-only "ok" + FTS5 malformed)
PRAGMA quick_check
                   → "ok"        (was "database disk image is malformed")
SELECT COUNT(*) FROM records
                   → 1892        (unchanged)
SELECT COUNT(*) FROM records_fts
                   → 1892        (unchanged)
SELECT MIN(rowid), MAX(rowid) FROM records_fts
                   → (1, 1892)   (was (1, 2011) with 119 gaps — now dense)
SELECT COUNT(*) FROM records_fts WHERE records_fts MATCH 'court'
                   → 662         (FTS5 MATCH queries SUCCEED — they would
                                  have raised "malformed" pre-rebuild)
```

## Interpretation

1. **FTS5 corruption appears resolved.** All five PRAGMA / SELECT signals that
   were red since b0584 are now green.
2. **No new ingestion happened.** `records` count is unchanged at 1892, so the
   26-record `deferred-fts5` backlog and 10-record `deferred-scanned-pdf`
   backlog have NOT been flushed by the operator — only the rebuild ran.
3. **`corpus.sqlite` is gitignored.** The change is host-local and will not be
   reflected in the next `git pull`. b2/rclone sync (deferred to host) is the
   only persistence channel for this rebuild.
4. **The rowid collapse** (records_fts MAX rowid 2011 → 1892) is consistent
   with `INSERT INTO records_fts(records_fts) VALUES('rebuild')` rebuilding
   the FTS5 contentless table from scratch against the current 1892 rows in
   `records`.

## Implications for the next JIW tick (b0608)

The b0606 / b0607-main standing recommendation of "5-of-5 read-only
confirmation tick" is **OBSOLETE** if the rebuild persists. b0608 should:

1. Open `corpus.sqlite` read-only and re-run the same five probes above. If
   they remain green:
2. **Reparse the 26 deferred-fts5 records** (priority (a) per the SKILL).
   These are parser-clean records whose FTS5 `INSERT` was blocked at parse
   time. They are zero-fetch — pure local reparse.
3. After (2) succeeds without re-corrupting FTS5, **resume
   judiciary-coa-sweep page 8** (6 candidates remaining) per priority (b).
4. Take a clean backup `corpus.sqlite.bak.b0608-pre-rebuild-confirmed-...`
   before the first FTS5-touching INSERT, in case b0602's
   `CREATE VIRTUAL TABLE` self-damage pattern recurs.
5. If any of the five probes regresses to "malformed" between b0607 and
   b0608, fall back to read-only confirmation tick mode.

## Mutations by JIW this tick

Still zero. The b0607 main commit (`f9e8174` + stop entries `ce81ede`)
remains accurate for JIW-originated changes. This addendum is a discovery
report, not a retroactive amendment to the tick verdict — the verdict
"FTS5-blocked at probe time" was correct for the 07:06:52Z probe. The
07:09:26Z host-side rebuild is a separate event the next worker must verify.

## Operator acknowledgement

If the rebuild was performed by the operator: thank you. The 12-tick
escalation backlog can now stand down. The remaining workflow items
(26 deferred-fts5, 10 deferred-scanned-pdf, 6 page-8 CoA candidates) will
flow through normal JIW ticks starting at b0608, subject to b0608's
confirmation that the rebuild is persistent.

Worker contact: peter@bilcoguard.com
User-Agent: KateWestonLegal-CorpusBuilder/1.0
