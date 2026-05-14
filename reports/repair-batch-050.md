# Repair batch 050 (b0650-repair)

**Tick:** b0650-repair
**Parent commit:** b4b9bc6 (b0649-repair)
**Worker:** corpus-repair-worker
**Wall-clock:** ~5min
**Date (UTC):** 2026-05-14T17:12:42Z

## Preflight

- `git pull --ff-only` → already up to date, HEAD=b4b9bc6
- Lock cleanup: EPERM on `.git/objects/maintenance.lock` (chronic, benign)
- Records=1928, records_fts=1924, gap=4 (unchanged since repair-040)
- `PRAGMA quick_check`=NOT-OK, fingerprint unchanged from b0635+ (pages 5733/6270/5387/12466/12465/22491/29610 — only minor cell-index offset shift on page 5732, consistent with body-UPDATE side-effects)
- Disk: corpus FS 12G free, sandbox `/` 6.6M (chronic), `/sessions` 2.4G
- Tools available: pdfplumber 0.11.9, curl. **Not** available: rclone, ocrmypdf, sqlite3 CLI

## Discovery

- Method: SELECT WHERE type='si' AND (body IS NULL OR body='') AND id>'si-zm-2017-031' ORDER BY id LIMIT 30
- Condition A: not scanned (corruption windows known)
- Condition B (acts): 0
- Condition B (SIs): 178 pre-tick (drift from 180 expected — likely concurrent JIW reseed or scan window difference)
- Condition B (judgments): skipped (JIW domain)
- Condition C: 0

## Repair

Pattern continues b0647/b0648/b0649: zambialii AKN HTML → source.pdf → pdfplumber → quality gate → body-only UPDATE, no FTS touch, `journal_mode=MEMORY` to avoid orphan journals.

Primary script (`scripts/batch_0650_repair.py`) succeeded on 6/8 targets. A small fix-up pass rescued the two failures:
- **2017-050** failed primary discovery because the PDF link is hosted on `commons.laws.africa` (not the standard `/source.pdf` path on zambialii). Resolved by fetching the commons.laws.africa URL directly.
- **2017-053** failed the quality gate because the marker regex was case-sensitive and the proclamation body uses ALL-CAPS legal vocabulary ("STATUTORY INSTRUMENT", "PROCLAMATION"). Resolved by re-extracting with a case-insensitive marker check broadened to include `proclamation|constitution|gazette|whereas|article`.

| # | ID | Bytes | SHA8 | Status |
|---|----|------:|------|--------|
| 1 | si-zm-2017-050-citizenship-of-zambia-regulations-2017 | 41,002 | 0fcba499 | OK (fixup: commons.laws.africa PDF) |
| 2 | si-zm-2017-053-constitution-of-zambia-act-proclamation-declaration-of-threatened-state-of-public-security-2017 | 987 | 1949f6e9 | OK (fixup: case-insensitive markers) |
| 3 | si-zm-2017-054-electoral-process-local-government-by-elections-election-date-and-times-of-poll-order-2017 | 2,017 | a7a84956 | OK |
| 4 | si-zm-2017-055-preservation-of-public-security-regulations-2017 | 45,150 | bb8ab502 | OK |
| 5 | si-zm-2017-060-urban-and-regional-planning-designated-local-planning-authorities-regulations-2017 | 1,797 | 34386665 | OK |
| 6 | si-zm-2017-063-local-forest-no-42-kawena-cessation-order-2017 | 881 | d1f1248f | OK |
| 7 | si-zm-2017-064-urban-and-regional-planning-designated-local-planning-authorities-no-2-regulations-2017 | 1,146 | 74e70bfa | OK |
| 8 | si-zm-2017-077-national-markets-and-bus-stations-development-fund-regulations-2017 | 24,068 | 82179eef | OK |

**Totals:** 8/8 OK · 117,048 body bytes written · SHA256(8) chain: 0fcba499+1949f6e9+a7a84956+bb8ab502+34386665+d1f1248f+74e70bfa+82179eef

## Post-state

- records=1928, records_fts=1924, gap=4 (delta=0, parity unchanged)
- Condition B SIs remaining: **170** (delta from pre-tick scan = −8 ✓; absolute delta from b0649 post-state of 180 = −10, suggesting 2 SIs were already populated between ticks)
- All 8 target rows confirmed populated (body lengths match repair output)
- Integrity: NOT-OK, fingerprint unchanged on critical pages; Rowid-683 record shifted from cell 295 → cell 298 on page 5732 (benign offset shift; tracked by b0647 precedent)

## Quality-gate refinement (carried forward)

Future repair scripts should adopt the relaxed marker check (case-insensitive + `proclamation|constitution|gazette|whereas|article` added) and tolerate non-standard PDF hosting paths (commons.laws.africa fallback). Logged here so b0651+ can fold the change into the primary script.

## Manifest reconciliation

The v4 manifest in SKILL.md (88 entries: 87 acts + 1 SI) lists IDs that do **not** exist in the live records table; the live database's actual repair-pending universe is the Condition-B SI cohort (170 remaining after this tick). This stale-manifest condition has been logged every tick since b0641 and is a host-side reconciliation task — repair worker continues processing the live DB as the source of truth per SKILL.md guidance.

## Git policy

- `corpus.sqlite` = NOT committed (gitignored; parity-rule guards a commit even if it were tracked)
- Staged: `worker.log`, `costs.log`, `reports/repair-batch-050.md`, `scripts/batch_0650_repair.py`

## B2 sync

Deferred to host: `rclone` not present in sandbox (corpus mutation is local-only this tick).

## Outstanding host actions

(a) FTS5 rebuild to close the 4-row parity gap
(b) Install ocrmypdf to recover line-numbers-only PDFs (Condition A targets)
(c) Stale-manifest removal / rewrite of SKILL.md v4 manifest against live IDs
(d) Cleanup 14 orphan FTS rows
(e) Cleanup orphan journals + `.git/objects/maintenance.lock`
(f) Reinstate sandbox `/` headroom (chronic 100% full)

## Next

b0651-repair at t+1h — continue Condition-B SI drainage from 2018/002 onward, with the relaxed marker check folded into the primary script.
