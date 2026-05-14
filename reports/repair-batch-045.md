# Repair batch 045 — Report

**Date**: 2026-05-14T15:11Z (approx)
**Worker**: repair (autonomous scheduled task, b0645)
**Wall-clock**: ~10 minutes (within 20-min cap)
**Tick verdict**: 8 SIs repaired body-only; corpus.sqlite NOT staged per parity rule

## Pre-tick state

- records = 1928
- records_fts = 1924
- gap = 4 (unchanged since b038 — chronic FTS5 shadow-page corruption)
- Integrity: NOT-OK — same FTS5 shadow-page corruption fingerprint as b038–b044 (pages 5733/6270/5387/12466/12465/22491/29610; rowid 1185 out of order; invalid page numbers; child-page-depth differs)
- Disk: corpus FS 13G free; root FS 100% full (6.6M free) — chronic since b038; workdir relocated to /sessions (2.4G free) this tick
- Tools: pdfplumber 0.11.9 present; ocrmypdf absent; rclone absent

## Lock cleanup

`find .git -name "*.lock*" -delete` ran with EPERM warnings on `maintenance.lock` (chronic). `git pull --ff-only` succeeded with "Already up to date".

## Discovery (this tick)

Live database queries via rowid pagination (1..1928 in 50-row batches). NO read errors this tick (in contrast to b0644 which saw two malformed windows — likely because we did not re-read the bad windows; we only need Condition-B SIs which lie outside the corrupt rowid ranges).

| Condition | Count |
| --- | --- |
| B — no-body SIs | **212** (was 220 pre-b0644; b0644 drained 8) |
| Read errors (malformed-page rowid windows) | 0 |

Manifest cross-check: the v4 manifest IDs in the task spec still do not exist in the live `records` table (unchanged from b0643/b0644). Per spec, the live DB is the source of truth — working set is the 212-SI Condition-B backlog.

## Repair actions

Batch size = MAX_BATCH_SIZE = 8. All from Condition B SIs sorted alphabetically (continuation of b0644's 1986–1998 cohort), next 8 in alphabetical order being 2001–2009 zambialii.org bare-path AKN URLs. Pipeline: HTML → `source.pdf` discovery → pdfplumber.

| # | id | source | result | body_bytes | sha256(8) |
| --- | --- | --- | --- | --- | --- |
| 1 | si-zm-2001-032-air-services-permit-fees-regulations-2001 | zambialii HTML → source.pdf | OK | 2705 | 86a85a01 |
| 2 | si-zm-2003-049-zambia-national-broadcasting-corporation-amendment-act-commencement-order-2003 | zambialii HTML → source.pdf | OK | 984 | de6a13ad |
| 3 | si-zm-2004-022-national-council-for-construction-exemption-regulations-2004 | zambialii HTML → source.pdf | OK | 1390 | 889d3aea |
| 4 | si-zm-2005-019-national-road-fund-act-commencement-order-2005 | zambialii HTML → source.pdf | OK | 831 | d1ac90f4 |
| 5 | si-zm-2006-010-zambia-police-fees-regulations-2006 | zambialii HTML → source.pdf | OK | 2336 | eb4d4db1 |
| 6 | si-zm-2008-016-national-road-fund-charges-and-fees-apportionment-regulations-2008 | zambialii HTML → source.pdf | OK | 1737 | 2c1a31c4 |
| 7 | si-zm-2008-024-national-constitutional-conference-committees-regulations-2008 | zambialii HTML → source.pdf | OK | 30989 | f4f9dc56 |
| 8 | si-zm-2009-037-national-council-for-construction-forms-and-fees-regulations-2009 | zambialii HTML → source.pdf | OK | 41459 | d9cc14d9 |

**Successes**: 8/8. **Failures**: 0.

Pipeline per record:
1. Fetch `https://zambialii.org/akn/zm/act/si/{year}/{n}` (HTML viewer) — UA `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)`
2. Regex `href="…source.pdf"` to discover dated source-PDF URL
3. Download PDF (cached at `/sessions/trusting-upbeat-curie/tmp/repair_b0645/{i}.pdf`)
4. pdfplumber 0.11.9 page-by-page text extraction
5. Section-marker normalisation `(\d+)\.([A-Z])` → `\1. \2`
6. Quality gate: ≥200 chars + line-numbers-only test + legal-marker test (Act|Regulations|section|Order|Statutory Instrument|By-Laws|Rules|Notice)
7. `UPDATE records SET body, source_hash, fetched_at, parser_version=repair-0.6.0` (body-only — FTS untouched per parity rule)
8. CRAWL_DELAY = 5 s between requests (zambialii robots.txt)

## Post-tick state

- records = 1928 (unchanged)
- records_fts = 1924 (unchanged — FTS deliberately not touched)
- gap = 4 (unchanged)
- Condition-B SIs remaining: **204** (was 212 — drained 8)
- Integrity: NOT-OK — fingerprint unchanged from b0644 (body-only UPDATEs on non-corrupt rows did not propagate new corruption)
- journal_mode=MEMORY workaround applied; **no orphan journals created** this tick (no rollback-mode attempts before applying MEMORY pragma)

## Git policy

corpus.sqlite is NOT staged this tick per parity rule (records ≠ records_fts; gap=4 unchanged). Logs + report + script staged only. Continues b0626..b0644 pattern. Repaired bodies persist in local corpus.sqlite for the next tick / host-side reconciliation.

## B2 sync

Deferred to host (`rclone` not in sandbox). Corpus mutation is local-only this tick.

## Host actions still required

1. **FTS5 rebuild** (DROP records_fts + CREATE + INSERT-SELECT FROM records + VACUUM) to clear gap=4 and shadow-page corruption. Until then JIW continues to abort and repair worker keeps draining Condition-B without FTS-side reconciliation.
2. `rm -f .git/maintenance.lock` and any other bogus refs (EPERM in sandbox; precedent: b0608/b0640/b0641).
3. Rotate sandbox-/ (6.6 MB free, 100 %); install ocrmypdf for parliament.gov.zm scanned PDF fallback.
4. Reconcile the 14 orphan FTS rows reported by b0643 (`FTS-not-in-records`).
5. Clean up orphan journals from b0644 (`corpus.sqlite-journal.b0644-orphan*`) — sandbox `rm` still EPERM-blocked.

## Next

b0646-repair t+60 min — will continue draining Condition-B SIs from 2009 onwards (204 remaining).
