# Repair batch 049 (b0649-repair)

**Tick:** b0649-repair
**Parent commit:** c0c6498 (b0648-repair)
**Worker:** corpus-repair-worker
**Wall-clock:** ~4min
**Date (UTC):** 2026-05-14T16:13:11Z

## Preflight

- `git pull --ff-only` → already up to date, HEAD=c0c6498
- Lock cleanup: EPERM on `.git/objects/maintenance.lock` (chronic, benign)
- Records=1928, records_fts=1924, gap=4 (unchanged since repair-040)
- `PRAGMA quick_check`=NOT-OK, fingerprint unchanged from b0635+ (pages 5733/6270/5387/12466/12465/22491/29610)
- Disk: corpus FS 12G free, sandbox `/` 6.6M (100% full, chronic), `/sessions` 2.4G
- Tools available: pdfplumber 0.11.9, curl. **Not** available: rclone, ocrmypdf, sqlite3 CLI

## Discovery

- Method: SELECT WHERE type='si' AND (body IS NULL OR body='') AND id>'si-zm-2016-063' ORDER BY id LIMIT 30
- Condition A: not scanned (corruption windows known)
- Condition B (acts): 0
- Condition B (SIs): 188 (continuing drainage from b0648 cohort 2016/04+)
- Condition B (judgments): skipped (JIW domain)
- Condition C: 0

## Repair

Pattern continues b0647/b0648: zambialii AKN HTML → source.pdf → pdfplumber → quality gate → body-only UPDATE, no FTS touch, `journal_mode=MEMORY` to avoid orphan journals.

| # | ID | Bytes | SHA8 | Status |
|---|----|------:|------|--------|
| 1 | si-zm-2016-070-electoral-process-local-government-elections-election-dates-and-times-of-poll-order-2016 | 2,209 | f7bd4fa9 | OK |
| 2 | si-zm-2017-001-citizens-economic-empowerment-reservation-scheme-regulations-2017 | 1,926 | 4158446e | OK |
| 3 | si-zm-2017-018-local-government-by-elections-election-dates-and-times-of-poll-order-2017 | 1,850 | cf4aa3d4 | OK |
| 4 | si-zm-2017-020-tourism-and-hospitality-prepaid-package-tours-regulations-2017 | 4,862 | 2930d1a6 | OK |
| 5 | si-zm-2017-022-tourism-and-hospitality-casino-regulations-2017 | 66,604 | 25747b8b | OK |
| 6 | si-zm-2017-027-control-of-goods-import-and-export-forest-produce-regulations-2017 | 3,393 | 949f55ee | OK |
| 7 | si-zm-2017-028-dambwa-local-forest-no-f22-alteration-of-boundaries-order-2017 | 3,198 | 6c30c15e | OK |
| 8 | si-zm-2017-031-control-of-goods-import-and-export-forest-produce-prohibition-of-importation-order-2017 | 1,957 | dc740e32 | OK |

**Totals:** 8/8 OK · 85,999 body bytes written · SHA256(8) chain: f7bd4fa9+4158446e+cf4aa3d4+2930d1a6+25747b8b+949f55ee+6c30c15e+dc740e32

## Post-state

- records=1928, records_fts=1924, gap=4 (delta=0, parity unchanged)
- Condition B SIs remaining: **180** (was 188 — delta −8 ✓)
- All 8 target rows confirmed populated (body lengths match repair output)
- Integrity: NOT-OK, fingerprint unchanged (no new corruption from body UPDATEs — only cell-index offsets shift on affected pages)

## Manifest reconciliation

The v4 manifest in SKILL.md (88 entries: 87 acts + 1 SI) lists IDs that do **not** exist in the live records table; the live database's actual repair-pending universe is the Condition-B SI cohort (180 remaining after this tick). This stale-manifest condition has been logged every tick since b0641 and is a host-side reconciliation task — repair worker continues processing the live DB as the source of truth per SKILL.md guidance.

## Git policy

- `corpus.sqlite` = NOT committed (gitignored; parity-rule guards a commit even if it were tracked)
- Staged: `worker.log`, `costs.log`, `reports/repair-batch-049.md`, `scripts/batch_0649_repair.py`

## B2 sync

Deferred to host: `rclone` not present in sandbox (corpus mutation is local-only this tick).

## Outstanding host actions

(a) FTS5 rebuild to close the 4-row parity gap
(b) Install ocrmypdf to recover line-numbers-only PDFs (Condition A targets)
(c) Stale-manifest removal / rewrite of SKILL.md v4 manifest against live IDs
(d) Cleanup 14 orphan FTS rows
(e) Cleanup orphan journals (13) + `.git/objects/maintenance.lock`
(f) Reinstate sandbox `/` headroom (chronic 100% full)

## Next

b0650-repair at t+1h — continue Condition-B SI drainage from 2017/050 onward.
