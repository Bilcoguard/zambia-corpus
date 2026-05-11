# Batch 0592 — Judgment-Ingestion-Worker

**Date:** 2026-05-11T18:15:00Z
**Worker:** judgment-ingestion-worker
**Sweep:** Court of Appeal — judiciaryzambia.com, page 5 remainder (3 final CoA candidates)
**Parser:** v0.3.8-inline
**User-Agent:** `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)`
**Cumulative fetches today:** 64/500

## Summary

- **3 posts + 3 PDFs fetched** successfully (all 3 page-5 remainder CoA-pattern posts)
- **3 records parsed cleanly** (full 3-judge panels, outcome detection PASS, quality-gate PASS)
- **0 records inserted** — ALL 3 deferred-fts5 due to pre-existing `records_fts_data` corruption (pages 14599 + 28316–28340; first observed b0587; persists 13 ticks later despite repair-batch-023 IDLE for 12 consecutive ticks at 18:11Z)
- **0 confirmed-404**, **0 dedupe-collisions**, **0 quality-gate failures**
- **CHECK8 PASS** via transaction rollback: `records=1892 records_fts=1892` unchanged
- **No corpus.sqlite mutation this tick.**

## Parsed (3) — all deferred-fts5

| ID | Case Number | Date Decided | Outcome | Judges |
|----|-------------|--------------|---------|--------|
| judgment-zm-2026-coa-210-clifford-simfukwe-v-zesco | APP/210/2023 | 2026-01-29 | dismissed | Kondolo SC, Makungu, Chembe JJA |
| judgment-zm-2026-coa-291-bank-of-zambia-v-bernard-fundi | APP/291/2024 | 2026-01-27 | set-aside | Kondolo, Majula, Muzenga JJA |
| judgment-zm-2026-coa-304-julian-sichalwe-v-saturina-regna-pension-trust-limited-lumwana-mining-company-li | APP/304/2024 | 2026-01-27 | dismissed | Siavwapa (JP), Chishimba, Patel JJA |

### Case notes

- **Clifford Simfukwe v ZESCO** — Electricity-utility appeal against ZESCO (Zambia Electricity Supply Corporation). Ground-by-ground dismissal. Tail-of-document operative paragraph: "appeal is dismissed".
- **Bank of Zambia v Bernard Fundi** — BoZ v former employee Bernard Fundi. Judgment of the lower court set aside; matter remitted to the High Court. **URL-slug omits `-sc-` marker** for Kondolo SC — parser produced bare "Kondolo" judge name; PDF body confirms Kondolo SC. Will resolve cleanly via parser v0.3.9 Coram-SC-suffix recovery from PDF body.
- **Julian Sichalwe v Saturina Regna Pension Trust + Lumwana Mining** — Pension trust + mining (Lumwana) co-respondent case. Appeal dismissed. **Siavwapa is President of the Court of Appeal (role "JP", Justice President)** but parser tagged as JJA; URL slug contains `-siavwapa-jp-` and the JP role must be preserved. Will resolve via parser v0.3.9 JP-role detection. ID slug truncated at ~100 chars (deterministic; acceptable).

## Deferred-fts5 backlog (carried forward + new)

| Source tick | Records |
|-------------|---------|
| b0590 | 7 |
| b0591 | 4 |
| **b0592 (this tick)** | **3** |
| **Total** | **14** |

All 14 records have:
- Raw PDFs on disk under `raw/judiciary-zm/coa/`
- Parsed metadata preserved in JSON files (b0592 archive: `raw/judiciary-zm/coa/_deferred/b0592_parsed_records.json`)
- Quality-gate PASS, judge-extraction PASS (with v0.3.9 noted corrections for b0592 records 291 + 304), outcome detection PASS

## Parser v0.3.9 improvements flagged (not yet implemented)

1. **Coram SC suffix recovery from PDF body** when URL slug omits `-sc-` marker (b0592 record 291: URL = `coram-justice-kondolo-majula-muzenga-jja`; PDF body confirms Kondolo SC). Implementation: scan PDF body for `KONDOLO, SC` or `<judge>, SC` patterns within 1500 chars of Coram header; attach SC suffix to matching slug-extracted judge.
2. **JP role suffix detection** for Court of Appeal President (b0592 record 304: URL slug `coram-justice-siavwapa-jp-chishimba-patel-jja`; role JP for Justice President of CoA — must NOT be stripped as JJA-equivalent). Implementation: extend the JJA-stripping pattern bag to recognise `<judge>-jp-` as a distinct role marker.

## Pre-existing FTS5 corruption — operator escalation

`PRAGMA integrity_check` reports `database disk image is malformed` with damage localised to `records_fts_data` page-tree pages 14599 and 28316–28340. The corruption:

- First observed: b0587 (2026-05-11T09:21Z) on the pre-insert backup (predates b0587 itself)
- Persists 13 JIW/repair ticks later
- **Repair-batch-023 (latest repair-worker tick at 2026-05-11T18:11:02Z) reports `IDLE manifest=48/48-clean repaired=0 fetched=0 verdict=idle-12th-consecutive-tick`**

The repair-worker's manifest does NOT yet include the `records_fts` rebuild task. **Recommendation for operator (or repair-worker manifest update):**

```
Task: fts5-rebuild-records-fts
Action:
  1. Save the existing schema: sqlite> SELECT sql FROM sqlite_master WHERE name='records_fts';
  2. DROP TABLE records_fts;
  3. CREATE VIRTUAL TABLE records_fts USING fts5(
       id UNINDEXED, type UNINDEXED, title, citation, case_name, outcome_detail, body,
       tokenize='porter unicode61'
     );
  4. INSERT INTO records_fts(id, type, title, citation, case_name, outcome_detail, body)
       SELECT r.id, r.type, r.title, r.citation,
              jm.case_name, jm.outcome_detail, r.body
       FROM records r
       LEFT JOIN judgments_meta jm ON jm.id = r.id;
  5. INSERT INTO records_fts(records_fts) VALUES('integrity-check');
  6. Reverify CHECK8: SELECT (SELECT COUNT(*) FROM records) = (SELECT COUNT(*) FROM records_fts);
```

Until this is run, JIW yield will remain near-zero (3/3 deferred this tick).

## CHECK results

- CHECK1 (≥1 judge per record): PASS — 3 judges each on all 3 parsed
- CHECK2 (issue_tags non-empty): PASS — 11–12 tags each
- CHECK3 (outcome ∈ enum): PASS — dismissed, set-aside, dismissed
- CHECK4 (judges resolve in registry): PASS for 8/9 distinct judges; bare "Kondolo" in record 291 needs Kondolo-SC alias (will be corrected on parser v0.3.9 reparse)
- CHECK5 (no duplicate IDs): PASS
- CHECK6 (raw_sha256 == on-disk sha): PASS
- CHECK7 (no duplicate case_name+court+date): PASS
- CHECK8 (records.count == records_fts.count): **PASS via rollback** — 1892 == 1892 unchanged

## Sweep position

- **Before tick:** `judiciary-coa-sweep: page 5 remaining` (3 unprocessed CoA candidates)
- **After tick:** `judiciary-coa-sweep: page 6` (page 5 fully processed; 0 CoA candidates remaining on page 5; sp-71-charlse-mpundu remains on page 5 listing but was classified non-CoA by prior tick — TBD whether to ingest as Subordinate-Procedure appeal)

## Execution

- Inline runner, no derivative script committed (sandbox-session safety constraint, per b0548..b0591 precedent)
- /tmp-isolated `corpus.sqlite` working copy: `/tmp/b0592/corpus.sqlite`
- Pre-tick backup: `corpus.sqlite.bak.b0592-pre-20260511T181019Z`
- No atomic copy-back (no records written; corpus.sqlite untouched)
- Parsed JSON archive: `raw/judiciary-zm/coa/_deferred/b0592_parsed_records.json`
- B2 sync: deferred-to-host (rclone not in sandbox)
