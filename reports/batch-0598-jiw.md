# Batch 0598 — JIW (Judgment Ingestion Worker)

**Tick:** 2026-05-12T00:11:00Z (UTC)
**Worker:** judgment-ingestion-worker
**Priority used:** (a) REPARSE DEFERRED — zero fetch cost
**Status:** FTS5-blocked — 18th consecutive blocked tick
**Result:** 0 records written; b0597's proposed workaround falsified

## Summary

This tick set out to test b0597's hypothesis that the long-running FTS5 corruption affecting `records_fts` blocks `rebuild`/`optimize`/`integrity-check`/`MATCH` operations but not direct column-based `INSERT INTO records_fts(id, type, title, …) VALUES (…)` statements. If true, the JIW could flush the 26-record deferred-fts5 backlog without waiting for operator authorisation of a repair-worker FTS5 rebuild.

**The hypothesis is wrong.** b0598 ran the same INSERT test on a /tmp isolated copy of `corpus.sqlite` **but extended it through `conn.commit()`**, which b0597 did not do. INSERT succeeds in-transaction (post-insert `COUNT(*)` rises from 1892 → 1893, as b0597 reported), but `conn.commit()` then fails with `database disk image is malformed`, automatically rolling the transaction back. Post-commit `COUNT(*)` returns to 1892. Re-opening the connection confirms the row is not durable.

b0598 also tested `DROP TABLE records_fts` on the /tmp isolated copy: this also fails with `database disk image is malformed`. The shadow tables (`records_fts_data`, `_idx`, `_content`, `_docsize`, `_config`) cannot be dropped through the SQL interface.

**Conclusion: the malformed FTS5 metadata pages corrupt the b-tree at a level that prevents any durable write to `records_fts`, and prevents DROP. The only remaining path is a dump-and-restore or specialised shadow-table recovery — repair-worker scope, not JIW scope.**

## Diagnostic transcript (excerpt)

```
$ python3 /sessions/cool-beautiful-clarke/tmp/flush_b0598.py
=== Step 0: Verify raw_sha256 for all records ===
  [OK] judgment-zm-2024-coa-024-kingfred-phiri-v-life-master-limited: 37921802939d394e942d9c498f72642e55b765b95dd92d6f0679b80c7cdb8ee1
  [OK] judgment-zm-2025-coa-039-willard-hamunyangwa-and-2-others-v-the-people: 08306da4618b84f2dd499d443e804df927a8acafe3e89f6b0f0b23d15fe0826d
  [OK] judgment-zm-2025-coa-032-starford-chimanga-v-the-people: d5f4919e739eb4ef93e89a31bf89e81ecc485af5d26108ec8306d385e78bfbf2
  [OK] judgment-zm-2025-coa-027-collins-ncube-v-the-people: e9429ddcfee17f1babc109292940e4e3c382a1610e4b4ac4e94db252d0773517
  [OK] judgment-zm-2024-coa-211-rotor-moulder-enterprises-v-stanley-jordan: c3aa3602445346d1f6a23581b791913186131cdac02988d78f141700459c88e4

=== Step 1: Pre-flush counts ===
  records: 1892, records_fts: 1892, delta: 0

=== Step 2: Insert records ===
  [judgment-zm-2024-coa-024-kingfred-phiri-v-life-master-limited]              inserted + JSON written
  [judgment-zm-2025-coa-039-willard-hamunyangwa-and-2-others-v-the-people]     inserted + JSON written
  [judgment-zm-2025-coa-032-starford-chimanga-v-the-people]                    inserted + JSON written
  [judgment-zm-2025-coa-027-collins-ncube-v-the-people]                        inserted + JSON written
  [judgment-zm-2024-coa-211-rotor-moulder-enterprises-v-stanley-jordan]        inserted + JSON written
FATAL during insert: database disk image is malformed             ← raised by conn.commit()
```

Followed by the /tmp diagnostic:

```
pre records_fts: 1892
INSERT done                              ← no error from cursor.execute(INSERT INTO records_fts …)
post-insert COUNT(*): 1893               ← b0597's observation reproducible
COMMIT FAILED: database disk image is malformed
post-commit COUNT(*): 1892               ← auto-rollback
reopen-and-lookup of __diag2__: None     ← write was never durable

# Rebuild path test
DROP TABLE records_fts → FAIL (database disk image is malformed)
remaining shadow tables: records_fts_data, records_fts_idx, records_fts_content, records_fts_docsize, records_fts_config, records_fts
```

## Records prepared (5)

All 5 records would have been valid by CHECK1–CHECK7 (all judges resolve in `judges_registry.yaml`; non-empty `issue_tags`; outcome from allowed enum; no duplicate IDs; no duplicate case_number; raw_sha256 verified against on-disk PDFs). Failure was at CHECK8 / commit only.

| id | case_number | court | date | outcome | judges (panel) |
|---|---|---|---|---|---|
| judgment-zm-2024-coa-024-kingfred-phiri-v-life-master-limited | APP/24/2023 | CoA | 2024-12-10 | dismissed | Siavwapa JP, Mchenga DJP, Chashi, Kondolo SC, Makungu, Chishimba, Ngulube, Banda-Bobo, Muzenga, Patel, Chembe JJA (11-judge expanded panel) |
| judgment-zm-2025-coa-039-willard-hamunyangwa-and-2-others-v-the-people | APP/39-40-41/2023 | CoA | 2025-02-18 | allowed | Mchenga DJP, Muzenga, Chembe JJA |
| judgment-zm-2025-coa-032-starford-chimanga-v-the-people | APP/32/2024 | CoA | 2025-02-18 | dismissed | Mchenga DJP, Ngulube, Chembe JJA |
| judgment-zm-2025-coa-027-collins-ncube-v-the-people | APP/27/2024 | CoA | 2025-02-18 | dismissed | Mchenga DJP, Ngulube, Chembe JJA |
| judgment-zm-2024-coa-211-rotor-moulder-enterprises-v-stanley-jordan | APP/211/2022 | CoA | 2024-12-31 | set-aside | Makungu, Muzenga, Chembe JJA |

All 5 records are derivable from the archived deferred-queue parsed JSON files (`raw/judiciary-zm/coa/_deferred/b0594_parsed_records.json` and `raw/judiciary-zm/coa/_deferred/b0597_parsed_records.json`) and can be re-inserted the moment the FTS5 rebuild succeeds. The corresponding orphaned JSON files have been quarantined in `_stale_b0598_orphaned_jsons/` because the fuse-mounted workspace blocks `rm` (`Operation not permitted`).

## Operator escalation (7th repeat — NOW URGENT)

**Action required:** Add `fts5-rebuild-records-fts` to the repair-worker manifest. Recipe is in `gaps.md` (b0594 block, line ~5500–5520). Repair-batch-026 (2026-05-11T22:11:45Z) reports `consecutive_idle_ticks=15` — the manifest is incorrectly clean because the integrity check uses `COUNT(*)` rather than `INSERT INTO records_fts(records_fts) VALUES('integrity-check')`. Recommend the repair-worker's STEP4 also exercise the integrity-check command and the rebuild dry-run on a /tmp copy to surface FTS5 corruption.

**Action required (interim):** If operator authorises a JIW-side rebuild, b0598 has confirmed that even `DROP TABLE records_fts` fails through the SQL interface. The most robust path is now:

1. `sqlite3 corpus.sqlite ".dump"` → `/tmp/corpus_dump.sql`
2. Edit `/tmp/corpus_dump.sql` to strip out `CREATE TABLE records_fts*` and `INSERT INTO records_fts*` statements
3. Create a fresh `/tmp/corpus_new.sqlite` from the edited dump
4. Re-create `records_fts` with the original schema (preserved at end of gaps.md b0594 escalation block)
5. Populate `records_fts` from `records` JOIN `judgments_meta` per the recipe
6. Run `INSERT INTO records_fts(records_fts) VALUES('integrity-check')` — if it passes, swap in the rebuilt DB.
7. Run a full FTS5 MATCH smoke test before swap-in.

**Action required:** Add `ocrmypdf-scanned-coa-pdfs` to the repair-worker manifest (10 records waiting).

## Total deferred backlog (UNCHANGED)

- **deferred-fts5 (parser-clean, awaiting rebuild):** 7 (b0590) + 4 (b0591) + 3 (b0592) + 6 (b0593) + 4 (b0594) + 2 (b0597) = **26 records**
- **deferred-scanned-pdf (awaiting ocrmypdf):** 1 (b0593) + 4 (b0594) + 5 (b0597) = **10 records**

## Files touched this tick

- `gaps.md` — appended b0598 entry with corrected FTS5 diagnostic and 7th operator escalation
- `worker.log` — appended b0598 entries
- `costs.log` — appended b0598 entries (0 network fetches; phase-a reparse-deferred)
- `reports/batch-0598-jiw.md` — this report
- `corpus.sqlite.bak.b0598-pre-20260511T221111Z` — pre-flush backup (116 MB, no mutation occurred so identical to live DB)
- `_stale_b0598_orphaned_jsons/` — 5 orphaned JSON files quarantined

## Records, FTS, judgments_meta counts (no change)

```
records:        1892
records_fts:    1892
judgments_meta:  202
```

CHECK8 holds: records.count == records_fts.count.

## Sweep position next tick

Unchanged from b0597: `judiciary-coa-sweep: page 8 remaining` (6 candidates).
Recommendation: continue page-8 sweep on next JIW tick — parsing is zero network cost on PDFs already on disk, and adds to the archived deferred queue against the eventual FTS5 rebuild flush. New page-8 fetches will add network cost but stay well under the 500/day budget.
