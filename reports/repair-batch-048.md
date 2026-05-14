# Repair batch 048 — Report

**Date**: 2026-05-14T15:15Z
**Worker**: repair (autonomous scheduled task, b0648)
**Wall-clock**: ~7 minutes (well within 20-min cap)
**Tick verdict**: 8 SIs repaired body-only; corpus.sqlite NOT staged per parity rule

## Pre-tick state

- records = 1928
- records_fts = 1924
- gap = 4 (unchanged since b0638 — chronic FTS5 shadow-page corruption)
- Integrity: NOT-OK — same FTS5 shadow-page corruption fingerprint as b0638–b0647 (pages 5733/6270/5387/12466/12465/22491/29610; rowid 1185 out of order; invalid page numbers; child-page-depth differs)
- Disk: corpus FS 12G free; root FS 100% full (6.6M free) — chronic
- Tools: pdfplumber 0.11.9 present; ocrmypdf absent; rclone absent; sqlite3 CLI absent (Python sqlite3 only)
- Workdir: `/sessions/zen-busy-gates/tmp/repair_b0648`

## Lock cleanup

`find .git -name "*.lock*" -delete` ran with EPERM warnings on `maintenance.lock` and `ORIG_HEAD.lock` (chronic since b0608). `git pull --ff-only` succeeded with "Already up to date" — HEAD unchanged from b0647's `ac64a1f` (b0648-jiw committed only logs/report, no corpus mutation).

## Discovery (this tick)

Live database queries via rowid pagination (1..1928 in 50-row batches) using `PRAGMA cell_size_check = OFF`.

| Condition | Count |
| --- | --- |
| A — corrupted body (line-numbers-only) | not scanned (held off — corruption windows known) |
| B — no-body acts | **0** |
| B — no-body SIs | **196** (was 196 post-b0647 — confirmed unchanged) |
| B — no-body judgments | (skipped — JIW domain) |
| C — stub acts/SIs (<200 chars, >0) | **0** |
| Read errors (malformed-page rowid windows) | 2 (rows 1100–1150 malformed; 1150–1200 UTF-8 decode error on `body`) |

Manifest cross-check: the v4 manifest IDs in the task spec still do not exist in the live `records` table (consistent with b0643–b0647). Per spec the live DB is the source of truth — working set is the 196-SI Condition-B backlog.

## Repair actions

Batch size = MAX_BATCH_SIZE = 8. All from Condition B SIs sorted alphabetically (continuation of b0647's 2016/03 → 2016/04+ cohort). The two earlier-alphabetic candidates `local-courts-administration-of-estates-rules-1969` and `local-courts-rules-1966` are again skipped (their `source_url` points at `commons.laws.africa` media URLs with a different host/URL shape — consistent with b0643–b0647 skipping them).

| # | id | source | result | body_bytes | sha256(8) |
| --- | --- | --- | --- | --- | --- |
| 1 | si-zm-2016-040-zambia-wildlife-zambia-wildlife-police-uniforms-and-badges-regulations-2016 | zambialii HTML → source.pdf | OK | 6880 | ed9211c1 |
| 2 | si-zm-2016-041-zambia-wildlife-game-animals-order-2016 | zambialii HTML → source.pdf | OK | 1834 | 212facf1 |
| 3 | si-zm-2016-042-zambia-wildlife-protected-animals-order-2016 | zambialii HTML → source.pdf | OK | 1672 | 14026a03 |
| 4 | si-zm-2016-043-zambia-wildlife-export-prohibition-order-2016 | zambialii HTML → source.pdf | OK | 1564 | 45c3cf20 |
| 5 | si-zm-2016-049-national-prosecutions-authority-witness-allowances-and-expenses-regulations-2016 | zambialii HTML → source.pdf | OK | 3774 | d215e428 |
| 6 | si-zm-2016-059-national-museums-entry-fees-regulations-2016 | zambialii HTML → source.pdf | OK | 1268 | 4ae98d19 |
| 7 | si-zm-2016-062-electoral-process-code-of-conduct-enforcement-regulations-2016 | zambialii HTML → source.pdf | OK | 3952 | 5e418e28 |
| 8 | si-zm-2016-063-electoral-process-general-regulations-2016 | zambialii HTML → source.pdf | OK | 91175 | b7668ff8 |

**Successes**: 8/8. **Failures**: 0. **Total body bytes written**: 112,119.

Pipeline per record:
1. Fetch `https://zambialii.org/akn/zm/act/si/{year}/{n}` (HTML viewer) — UA `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)`
2. Regex `href="…source.pdf"` to discover dated source-PDF URL
3. Download PDF (cached under `/sessions/zen-busy-gates/tmp/repair_b0648/{i}.pdf`)
4. pdfplumber page-by-page text extraction
5. Section-marker normalisation `(\d+)\.([A-Z])` → `\1. \2`
6. Quality gate: ≥200 chars + line-numbers-only test (digit-line ratio) + legal-marker test (Act|Regulations|section|Order|Statutory Instrument|By-Laws|Rules|Notice)
7. `UPDATE records SET body, source_hash, fetched_at, parser_version=repair-0.6.1` (body-only — FTS untouched per parity rule)
8. CRAWL_DELAY = 5 s between requests (zambialii robots.txt)

## Post-tick state

- records = 1928 (unchanged)
- records_fts = 1924 (unchanged — FTS deliberately not touched)
- gap = 4 (unchanged)
- Condition-B SIs remaining: **188** (was 196 — drained 8)
- Integrity: NOT-OK — corruption fingerprint pages unchanged (5733/6270/5387/12466/12465/22491/29610); only cell-index offsets shift as expected from body row-overflow updates on healthy rows
- `journal_mode=MEMORY` workaround applied; no new orphan journals observed

## Git policy

corpus.sqlite is NOT staged this tick per parity rule (records ≠ records_fts; gap=4 unchanged). Logs + report + script staged only. Continues b0626..b0647 pattern. Repaired bodies persist in local `corpus.sqlite` for the next tick / host-side reconciliation.

## B2 sync

Deferred to host (`rclone` not in sandbox). Corpus mutation is local-only this tick.

## Host actions still required

1. **FTS5 rebuild** (DROP records_fts + CREATE + INSERT-SELECT FROM records + VACUUM) to clear gap=4 and shadow-page corruption. Until then JIW continues to abort and the repair worker keeps draining Condition-B SIs without FTS-side reconciliation. **22nd consecutive tick this is needed.**
2. `rm -f .git/objects/maintenance.lock` and `.git/ORIG_HEAD.lock` (EPERM in sandbox; precedent: b0608/b0640/b0641/b0645/b0647).
3. Rotate sandbox-`/` (6.6 MB free, 100%); install `ocrmypdf` for parliament.gov.zm scanned PDF fallback.
4. Reconcile the 14 orphan FTS rows reported by b0643 (`FTS-not-in-records`).
5. Clean up orphan journals from b0644 (`corpus.sqlite-journal.b0644-orphan*`).
6. Address read-error rowid windows 1100–1150 (malformed) and 1150–1200 (UTF-8 decode failure on body) — likely a corrupted-body record needing dedicated repair.

## Next

b0649-repair t+60 min — will continue draining Condition-B SIs from 2016/070+ onwards (188 remaining).
