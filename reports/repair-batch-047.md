# Repair batch 047 — Report

**Date**: 2026-05-14T14:15Z
**Worker**: repair (autonomous scheduled task, b0647)
**Wall-clock**: ~5 minutes (well within 20-min cap)
**Tick verdict**: 8 SIs repaired body-only; corpus.sqlite NOT staged per parity rule

## Pre-tick state

- records = 1928
- records_fts = 1924
- gap = 4 (unchanged since b038 — chronic FTS5 shadow-page corruption)
- Integrity: NOT-OK — same FTS5 shadow-page corruption fingerprint as b038–b045 (pages 5733/6270/5387/12466/12465/22491/29610; rowid 1185 out of order; invalid page numbers; child-page-depth differs)
- Disk: corpus FS 13G free; root FS 100% full (6.6M free) — chronic since b038; workdir under `/sessions/youthful-compassionate-planck/tmp/repair_b0647` (this session)
- Tools: pdfplumber present; ocrmypdf absent; rclone absent; sqlite3 CLI absent (Python sqlite3 only)

## Lock cleanup

`find .git -name "*.lock*" -delete` ran with EPERM warnings on `maintenance.lock` and `ORIG_HEAD.lock` (chronic). `git pull --ff-only` succeeded with "Already up to date" at HEAD `a21fdb4`. Note: a JIW batch b0646 ran between b0645-repair and this tick (commit `7053381`); my `git pull` reports up to date so b0646's commit is already merged.

## Discovery (this tick)

Live database queries via rowid pagination (1..2027 in 50-row batches) using `PRAGMA cell_size_check = OFF`.

| Condition | Count |
| --- | --- |
| A — corrupted body (line-numbers-only) | not scanned (held off — corruption windows known) |
| B — no-body acts | **0** |
| B — no-body SIs | **204** (was 204 pre-b0645; b0645 drained 8 → 204; pre-tick 204 confirmed) |
| B — no-body judgments | (skipped — JIW domain) |
| C — stub acts/SIs (<200 chars, >0) | **0** |
| Read errors (malformed-page rowid windows) | 1 (rows 1101–1151) |

Manifest cross-check: the v4 manifest IDs in the task spec still do not exist in the live `records` table (consistent with b0643/b0644/b0645). Per spec the live DB is the source of truth — working set is the 204-SI Condition-B backlog.

## Repair actions

Batch size = MAX_BATCH_SIZE = 8. All from Condition B SIs sorted alphabetically (continuation of b0645's 2001–2009 cohort): next 8 in alphabetical order are 2013–2016 zambialii.org bare-path AKN URLs. Pipeline: HTML → `source.pdf` discovery → pdfplumber. The two earlier-alphabetic candidates `local-courts-administration-of-estates-rules-1969` and `local-courts-rules-1966` were skipped because their `source_url` points at `commons.laws.africa` media URLs with a different host/URL shape (consistent with b0643–b0645 skipping them).

| # | id | source | result | body_bytes | sha256(8) |
| --- | --- | --- | --- | --- | --- |
| 1 | si-zm-2013-018-zambia-national-service-combat-uniform-regulations-2013 | zambialii HTML → source.pdf | OK | 2016 | 48cdfebb |
| 2 | si-zm-2014-016-animal-health-livestock-cleansing-order-2014 | zambialii HTML → source.pdf | OK | 1918 | f64ee0d7 |
| 3 | si-zm-2014-024-animal-health-control-and-prevention-of-animal-disease-order-2014 | zambialii HTML → source.pdf | OK | 2852 | 3dcc2fa9 |
| 4 | si-zm-2014-059-agricultural-credits-appointment-of-authorised-agency-order-2014 | zambialii HTML → source.pdf | OK | 852 | 603ba33d |
| 5 | si-zm-2015-039-national-council-for-construction-registration-of-projects-regulations-2015 | zambialii HTML → source.pdf | OK | 17188 | 56d4716a |
| 6 | si-zm-2015-086-zambia-institute-of-advanced-legal-education-accreditation-of-legal-education-institutions-regulations-2015 | zambialii HTML → source.pdf | OK | 31619 | 0ab030f2 |
| 7 | si-zm-2015-089-national-museums-declaration-order-2015 | zambialii HTML → source.pdf | OK | 826 | 3340fa53 |
| 8 | si-zm-2016-003-estate-agents-general-regulations-2016 | zambialii HTML → source.pdf | OK | 30787 | 2d32bbbf |

**Successes**: 8/8. **Failures**: 0. **Total body bytes written**: 88,058.

Pipeline per record:
1. Fetch `https://zambialii.org/akn/zm/act/si/{year}/{n}` (HTML viewer) — UA `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)`
2. Regex `href="…source.pdf"` to discover dated source-PDF URL (e.g. `…/eng@2014-02-14/source.pdf`)
3. Download PDF (cached at `/sessions/youthful-compassionate-planck/tmp/repair_b0647/{i}.pdf`)
4. pdfplumber page-by-page text extraction
5. Section-marker normalisation `(\d+)\.([A-Z])` → `\1. \2`
6. Quality gate: ≥200 chars + line-numbers-only test (digit-line ratio) + legal-marker test (Act|Regulations|section|Order|Statutory Instrument|By-Laws|Rules|Notice)
7. `UPDATE records SET body, source_hash, fetched_at, parser_version=repair-0.6.0` (body-only — FTS untouched per parity rule)
8. CRAWL_DELAY = 5 s between requests (zambialii robots.txt)

## Post-tick state

- records = 1928 (unchanged)
- records_fts = 1924 (unchanged — FTS deliberately not touched)
- gap = 4 (unchanged)
- Condition-B SIs remaining: **196** (was 204 — drained 8)
- Integrity: NOT-OK — corruption fingerprint pages unchanged (5733/6270/5387/12466/12465/22491/29610); only cell-index offsets shift as expected from body row-overflow updates on healthy rows
- journal_mode=MEMORY workaround applied; no new orphan journals observed in `corpus.sqlite-journal.*` during this tick

## Git policy

corpus.sqlite is NOT staged this tick per parity rule (records ≠ records_fts; gap=4 unchanged). Logs + report + script staged only. Continues b0626..b0645 pattern. Repaired bodies persist in local corpus.sqlite for the next tick / host-side reconciliation.

## B2 sync

Deferred to host (`rclone` not in sandbox). Corpus mutation is local-only this tick.

## Host actions still required

1. **FTS5 rebuild** (DROP records_fts + CREATE + INSERT-SELECT FROM records + VACUUM) to clear gap=4 and shadow-page corruption. Until then JIW continues to abort and the repair worker keeps draining Condition-B SIs without FTS-side reconciliation.
2. `rm -f .git/objects/maintenance.lock` and `.git/ORIG_HEAD.lock` (EPERM in sandbox; precedent: b0608/b0640/b0641/b0645).
3. Rotate sandbox-`/` (6.6 MB free, 100 %); install ocrmypdf for parliament.gov.zm scanned PDF fallback (would enable resumption of v4-manifest-style act repairs once those IDs exist in the live DB again).
4. Reconcile the 14 orphan FTS rows reported by b0643 (`FTS-not-in-records`).
5. Clean up the orphan journals from b0644 (`corpus.sqlite-journal.b0644-orphan*`) — sandbox `rm` still EPERM-blocked.

## Next

b0648-repair t+60 min — will continue draining Condition-B SIs from 2016/04+ onwards (196 remaining).
