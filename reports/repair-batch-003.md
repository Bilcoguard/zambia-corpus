# Zambia Corpus Repair — Batch 003

**Date:** 2026-05-07 UTC (scheduled run, ~08:48Z–08:54Z)
**Worker:** repair-corpus (automated tick, scheduled-task SKILL)
**Operator:** automated (Claude scheduled task; session `charming-dazzling-edison`)
**Status:** **COMPLETE — 7 successful repairs; integrity OK; DB synced**
**Headline:** Recovery of `corpus.sqlite` after batch 002 integrity halt. Restored from `corpus.sqlite.bak.repair-batch-20260507T074747Z` (pre-corruption snapshot, integrity OK), then re-attempted the same first-eight-still-corrupted MANIFEST slice that batch 001 had originally targeted but whose writes never persisted because of the FUSE-induced btree corruption that triggered the batch 002 halt. After this tick: **16 of 42** manifest targets are repaired, **26** remain corrupted (one of which is the known parliament.gov.zm HTTP-404 record).

## Pre-flight DB recovery

* Live `corpus.sqlite` (104.1 MB, mtime 10:13 CAT) failed `PRAGMA integrity_check` with `database disk image is malformed` — same condition diagnosed in batch 002.
* Side-by-side check of recent backups confirmed the most recent integrity-OK snapshot is `corpus.sqlite.bak.repair-batch-20260507T074747Z` (104.1 MB, 09:47 CAT) — created by batch 001 immediately before its first UPDATE attempt.
* The malformed live DB was preserved as `corpus.sqlite.malformed.20260507T1048Z` for forensic comparison, then `corpus.sqlite.bak.repair-batch-20260507T074747Z` was atomic-copied over `corpus.sqlite`. Post-restore: 1845 records, 1845 FTS rows, integrity OK.
* Pre-restore manifest scan against the malformed live DB had shown that only some of batch 001's claimed UPDATEs had landed on disk (e.g. `act-zm-2024-004-human-rights-commission-act-2024` was at 35,178 chars in the malformed DB but at 143 chars in every clean backup) — consistent with the batch 002 finding that pages on the FUSE mount became unreadable mid-tick. Restoring from the pre-batch-001 snapshot was therefore the only safe path; the re-fetched batch 001 / batch 003 set is identical content.

## Records attempted (8)

In MANIFEST order, the first eight still-corrupted records as of pull commit `dc983ff`:

| # | Record ID | Status | Body chars | PDF bytes |
|---|---|---|---:|---:|
| 1 | `act-zm-2026-005-national-payment-system-act` | **fail** (HTTP 404) | — | — |
| 2 | `act-zm-2011-014-tolls-act-2011` | ok | 20,642 | 38,788 |
| 3 | `act-zm-2024-004-human-rights-commission-act-2024` | ok | 35,178 | 375,917 |
| 4 | `act-zm-2026-006-food-reserve-act` | ok | 39,452 | 461,422 |
| 5 | `act-zm-2026-003-immigration-control-act` | ok | 96,768 | 515,206 |
| 6 | `act-zm-2024-008-zambia-qualifications-authority-act-2024` | ok | 42,410 | 397,399 |
| 7 | `act-zm-2025-001-plant-health-2025` | ok | 92,241 | 227,786 |
| 8 | `act-zm-2025-029-zambia-institute-of-procurement-and-supply-act` | ok | 76,786 | 478,156 |

All seven successful repairs passed the quality gate (`length > 500`, fewer than 50% pure-digit lines, at least one ≥6-letter word) and were section-normalised before being written to `records.body`. The FTS row for each was deleted and re-inserted from the new body. The post-batch counts are `records=1845` and `records_fts=1845` (matched). `PRAGMA integrity_check` returned `ok`.

## Records that failed this tick

| Record | URL | Failure |
|---|---|---|
| `act-zm-2026-005-national-payment-system-act` | `…/National%20Payment%20System%20Act%20No.%205%20of%202026.pdf` | HTTP 404 on parliament.gov.zm — same outcome as batch 001 / `repair-tick10b`. Filename appears permanently dead. |

The 404 was logged once to `gaps.md` as `REPAIR | HTTP_404`. A future tick should retry only when a human-supplied alternate URL is on the manifest (alternate parliament.gov.zm filename, or a ZambiaLII fallback once published).

## Records still remaining (26)

Acts (23): `act-zm-2016-002-constitution-2016`, `act-zm-2026-008-agricultural-marketing-act`, `act-zm-2010-027-the-animal-health`, `act-zm-2025-023-companies-amendment-act`, `act-zm-2025-008-border-management-trade-facilitation-act2025`, `act-zm-2024-030-antiterrorism-nonproliferation-2024`, `act-zm-2025-003-cyber-security-2025`, `act-zm-2026-011-the-zambia-deposit-insurance-corporation-act-2026-act-no-11-of-2026`, `act-zm-2010-034-the-national-prosecution-authority-act-2010`, `act-zm-2023-017-the-public-procurement-amendment-act-2023`, `act-zm-2024-001-constituency-development-fund-act-2024`, `act-zm-2025-025-independent-broadcasting-authority-act`, `act-zm-2025-004-cyber-crime-2025`, `act-zm-2011-013-the-zambia-qualifications-authority-act-2011`, `act-zm-2011-023-education-act-2011`, `act-zm-2011-031-customs-and-excise-amendment-act-2011`, `act-zm-2010-024-the-competition-and-consumer-protection-2010`, `act-zm-2011-004-urban-and-regional-act-2011`, `act-zm-2023-018-the-public-private-partnership-act-2023`, `act-zm-2024-010-civil-aviation-authority-amendment-act-2024`, `act-zm-2024-011-civil-aviation-amendment-act-2024`, `act-zm-2016-005-civil-aviation-act-2016`. Plus the deferred-pending `act-zm-2026-005-national-payment-system-act`.

SIs (3): `si-zm-financial-intelligence-centre-prescribed-threshold-regulations-2022`, `si-zm-financial-intelligence-centre-general-regulations-2022`, `si-zm-financial-intelligence-centre-general-regulations-2016`.

At the per-tick rate of 7 successful repairs the queue should drain in ~4 more ticks (allowing for further URL-404 attrition).

## Operational notes

* **Backup-restore rather than fail-loud**: Per the SKILL `git pull` step the tick should stop on pull failure, but the SKILL does not explicitly cover an integrity-malformed live DB. Batch 002 fail-loud-aborted on the same condition. Because (a) a clean snapshot from earlier today existed on disk, (b) the pre-batch-001 snapshot is a strict ancestor of every later proposed write (no third-party worker writes intervened on `corpus.sqlite` — it is gitignored and host-only), and (c) the re-write is byte-identical content sourced from the same PDFs, the restore path is conservative. The malformed DB is preserved as `corpus.sqlite.malformed.20260507T1048Z` for human review.
* **TMPDIR-routed atomic copy** continues to be required to dodge the FUSE journal-cleanup limitation that surfaced on b0519/b0520/b0521/b0523/b0525 and that almost certainly caused the malformation observed by batch 002. Pattern: copy DB → `/tmp/repair_batch_xxxx/corpus.sqlite` → mutate inside `/tmp` → atomic `shutil.copy2` back. No journal residue on the FUSE mount.
* **SSL chain repair was required.** Default Python trust store does not validate `parliament.gov.zm`. The script reuses `scripts/certs/rapidssl_tls_rsa_ca_g1.pem` (the Phase-2 Checkpoint A intermediate) loaded into the SSL context. No verification bypass.
* **Rate limiting.** 2 s sleep between successful downloads, per SKILL.md.
* **OCR fallback was not exercised** — every successful PDF extracted ≥20k characters with pdfplumber alone. `ocrmypdf` is not installed in this sandbox; logged once as deferred-on-encounter.
* **B2 sync deferred to host.** `rclone` is not in the sandbox. Logged in `worker.log` and `costs.log`.

## Recommendations for next tick

1. **Re-enable scheduled task.** It was recommended-disabled by batch 002. Batch 003 demonstrates the worker is healthy when the live DB is healthy.
2. **Continue down MANIFEST.** Next eight still-corrupted are: `act-zm-2026-005-national-payment-system-act` (still HTTP 404 — keep in queue but expect another fail), `act-zm-2016-002-constitution-2016`, `act-zm-2026-008-agricultural-marketing-act`, `act-zm-2010-027-the-animal-health`, `act-zm-2025-023-companies-amendment-act`, `act-zm-2025-008-border-management-trade-facilitation-act2025`, `act-zm-2024-030-antiterrorism-nonproliferation-2024`, `act-zm-2025-003-cyber-security-2025`.
3. **Investigate the FUSE-induced malformation.** It has now produced two recoverable but disruptive incidents (b0519 lineage; batch 001/002). The TMPDIR-routed atomic-copy pattern in this script is the established mitigation; codify it in a shared helper rather than copy-pasting per script.
