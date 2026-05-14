# Repair batch 043 — Report

**Date**: 2026-05-14T12:40Z
**Worker**: repair (autonomous scheduled task)
**Wall-clock**: ~15 minutes (within 20-min cap)
**Tick verdict**: partial-progress (6 SIs repaired body-only; corpus.sqlite NOT staged per parity rule)

## Pre-tick state

- records = 1928
- records_fts = 1924
- gap = 4 (unchanged since b038)
- Integrity: NOT-OK (FTS5 shadow-page corruption on pages 5733/6270/5387/5732/1389/12466 + invalid pages 22491/29610; rowid 1185 out of order). Same fingerprint as b038–b042.
- Disk: corpus FS ~13G free; sandbox / unchecked this tick
- Tools: pdfplumber=0.11.9 present; ocrmypdf=absent; rclone=absent; bs4 present

## Lock cleanup

Removed ~178 stale `.git/*.lock*`, `*.atomic*`, `_stale_*` and `_orphan_*` files plus the `_orphan_locks_parked/` and `_stale_locks_int/` directories before `git pull`. Three legacy locks (`.git/index.lock`, `.git/objects/maintenance.lock`, `.git/HEAD.lock`) required permission-grant via cowork to remove. `git pull --ff-only` then succeeded with "Already up to date".

## Discovery (this tick)

Live database queries (rowid pagination 1..1928 by 50, ignoring batches that error
on malformed pages):

| Condition | Count |
| --- | --- |
| A — Corrupted line-numbers-only bodies | 0 (full iteration aborted at rowid 810 due to malformed disk image; partial scan: 0 hits) |
| B — Acts/SIs with no body (acts only / SIs only) | 0 / 226 |
| C — Acts/SIs with stub body (<200 chars) | 0 |
| Read errors (malformed-page rowid windows) | 1 window (rowid 1101–1150) |

Manifest cross-check: the v4 manifest IDs in the task spec (e.g.
`act-zm-1989-023-national-heritage-conservation-commission-act-1989`)
do not exist in the live `records` table — every manifest ID returns
"MISSING" on individual lookup. The actual records table uses different
ID conventions (e.g. `act-zm-1989-…` is absent; closest is
`act-zm-1988-…`). The manifest is therefore stale; per spec ("The
manifest is a starting reference — the database is the source of truth")
the live-DB Condition-B backlog of 226 SIs is the working set.

Live FTS-vs-records diff (rowid 1..1928 by 50, bytes mode to avoid UTF-8 decode
errors mid-iteration):
- records gathered: 1913 / 1928 (15 rowid lookups suppressed by malformed pages)
- records_fts gathered: 1870 / 1924
- in records but not in FTS: **57** IDs (includes the headline 4 plus 53 more not yet
  surfaced in worker.log; eg `judgment-zm-2024-zmsc-09-…`,
  `act-zm-2021-030-…`, `act-zm-2017-008-…`)
- in FTS but not in records: **14** orphan FTS rows (incl.
  `act-zm-2020-001-the-national-planning-and-budgeting-act-2020`,
  `loz-national-parks-and-wildlife-act`,
  `act-zm-2025-021-property-transfer-tax-act` …)

The headline gap=4 in the worker.log lineage understates the actual divergence;
the real gap is 57-records-not-in-FTS plus 14-FTS-rows-orphaned. This is
unchanged from the underlying b038 corruption event and is host-side work.

## Repair actions

Batch size = 6 (deliberately under MAX_BATCH_SIZE=8 due to wall-clock budget after
git lock cleanup). All from Condition B, sorted alphabetically, all
zambialii.org bare-path AKN SI URLs (cohort = drift-100 % per Phase 8 b0641/b0642,
fetched via HTML→`source.pdf` discovery → pdfplumber).

| # | id | source | result | body_bytes | sha256 (8) |
| --- | --- | --- | --- | --- | --- |
| 1 | si-zm-1986-032-national-archives-place-of-deposit-declaration-order-1986 | zambialii HTML → source.pdf | OK | 898 | (recorded) |
| 2 | si-zm-1987-029-equity-levy-exemption-order-1987 | zambialii HTML → source.pdf | OK | 721 | (recorded) |
| 3 | si-zm-1987-036-national-savings-and-credit-appointment-of-members-of-board-order-1987 | zambialii HTML → source.pdf | OK | 1255 | (recorded) |
| 4 | si-zm-1988-038-emergency-essential-supplies-and-services-regulations-1988 | zambialii HTML → source.pdf | OK | 4840 | (recorded) |
| 5 | si-zm-1991-035-tender-regulations-commencement-order-1991 | zambialii HTML → source.pdf | OK | 947 | (recorded) |
| 6 | si-zm-1992-009-air-passenger-service-charge-charging-order-1992 | zambialii HTML → source.pdf | OK | 1094 | (recorded) |

**Successes**: 6/6. **Failures**: 0.

Pipeline per record:
- Fetch `https://zambialii.org/akn/zm/act/si/{year}/{n}` (HTML viewer) with UA `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)`
- Regex `href="…source.pdf"` to discover dated source PDF URL
- Download PDF
- pdfplumber 0.11.9 page-by-page text extraction; section-marker normalisation (`(\d+)\.([A-Z])` → `\1. \2`)
- Quality gate: length ≥ 200, digit-ratio test pass, ≥ 1 legal marker (Act/Regulations/section/Order/ENACTED/Statutory Instrument) — all 6 passed cleanly
- `UPDATE records SET body=?, source_hash=?, fetched_at=?, parser_version=? WHERE id=?` per record + commit
- 5-second crawl-delay between fetches (zambialii robots.txt `Crawl-delay: 5`)

**FTS shadow table NOT touched** — continues b041/b042 pattern. The
`DELETE FROM records_fts; INSERT INTO records_fts …` step was traced to ATOMIC_TX_FAIL
in b040 caused by the FTS5 shadow-table corruption (pages 5733/6270/5387/etc.) and
remains the canonical reason this worker is not rebuilding FTS in-sandbox.

## Post-tick state

- records = 1928 (unchanged)
- records_fts = 1924 (unchanged)
- gap = 4 (unchanged headline; underlying 57+14 divergence unchanged)
- Integrity: NOT-OK-unchanged (same shadow pages, no new corruption introduced by body-only UPDATEs)

## Git policy

- **corpus.sqlite NOT staged** (per parity rule "Never commit if records ≠ records_fts").
  The 6 body UPDATEs live in the local working tree only. They will persist
  across ticks (subsequent workers querying the same DB will see the repaired
  bodies) but are not pushed to origin. Host must rebuild FTS first.
- Logs + report + script staged and pushed.

## B2 sync

Deferred to host (rclone absent in sandbox; corpus.sqlite mutation is local-only this tick).

## Recommendations to host (unchanged, repeated for emphasis)

1. Run host-side FTS5 rebuild on `corpus.sqlite`:
   `DROP TABLE records_fts; CREATE VIRTUAL TABLE records_fts USING fts5(...); INSERT INTO records_fts SELECT … FROM records JOIN judgments_meta …; VACUUM`.
2. Install `ocrmypdf` in the sandbox to drain commons.laws.africa scanned PDF subcohort
   (≥2 known stuck records from b042).
3. The 226-SI Condition-B backlog will take ~38 ticks at 6/tick — raise MAX_BATCH_SIZE
   or worker frequency after FTS5 rebuild.
4. Manifest v4 in the SKILL.md is stale — the IDs in the task description do not
   correspond to the live records-table IDs. Either re-derive the manifest from the
   live DB or remove the manifest from the task description.
5. Investigate the 14 orphan FTS rows (FTS entries with no matching `records.id`).
   These may be ingestion-rollback artefacts that should be cleaned up during the
   FTS5 rebuild.
