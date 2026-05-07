# Zambia Corpus Repair — Batch 004

**Date:** 2026-05-07 UTC (scheduled run, ~09:11Z–09:12Z)
**Worker:** repair-corpus (automated tick, scheduled-task SKILL)
**Operator:** automated (Claude scheduled task; session `admiring-elegant-shannon`)
**Status:** **COMPLETE — 7 successful repairs; integrity OK; DB synced**
**Headline:** Continued the queue from batch 003. After this tick: **23 of 42** manifest targets repaired, **19** remain corrupted (one of which is the known parliament.gov.zm HTTP-404 record `act-zm-2026-005-national-payment-system-act`).

## Pre-flight

* Scheduled-task pre-step `find .git -name "*.lock" -delete` and `find .git -name "*.lock.bak" -delete` ran but the FUSE mount blocks unlink on the lock files (138 lock files persist on disk, including `.git/HEAD.lock`, `.git/index.lock`, `.git/objects/maintenance.lock`, and many `_stale_*` and `*.lock.bak.*` siblings). This is the same FUSE constraint logged in batches 001 and 003.
* `git pull --ff-only` reported `fatal: bad object refs/remotes/origin/main.lock.bak.b003.1778144672` because of the dead refs left by the lock-file artefacts in `.git/refs/remotes/origin/`. However `git ls-remote origin main` returned `3d4c5743e1c1111d5938bcf87cf5cdb2794a8e1c`, which is identical to the local HEAD. **Functionally up-to-date** — there are no commits on the remote main branch beyond what is already checked out. Logged in `worker.log`; proceeded.
* Live `corpus.sqlite` (104.9 MB, mtime 12:54 CAT) `PRAGMA integrity_check` = `ok`. 1845 records, 1845 FTS rows. Pre-batch snapshot taken via `/tmp/`-routed copy as `corpus.sqlite.bak.repair-batch-004-pre-20260507T091204Z`.

## Records attempted (8)

In MANIFEST order, the first eight still-corrupted records as of pull commit `ca23193`:

| # | Record ID | Status | Body chars | PDF bytes |
|---|---|---|---:|---:|
| 1 | `act-zm-2026-005-national-payment-system-act` | **fail** (HTTP 404) | — | — |
| 2 | `act-zm-2016-002-constitution-2016` | ok | 196,365 | 228,076 |
| 3 | `act-zm-2026-008-agricultural-marketing-act` | ok | 46,009 | 401,831 |
| 4 | `act-zm-2010-027-the-animal-health` | ok | 89,852 | 114,993 |
| 5 | `act-zm-2025-023-companies-amendment-act` | ok | 40,325 | 383,773 |
| 6 | `act-zm-2025-008-border-management-trade-facilitation-act2025` | ok | 61,639 | 441,027 |
| 7 | `act-zm-2024-030-antiterrorism-nonproliferation-2024` | ok | 80,255 | 484,097 |
| 8 | `act-zm-2025-003-cyber-security-2025` | ok | 81,097 | 477,682 |

All seven successful repairs passed the quality gate (`length > 500`, fewer than 50% pure-digit lines, at least one ≥6-letter word) and were section-normalised before being written to `records.body`. The FTS row for each was deleted and re-inserted from the new body. Post-batch counts are `records=1845` and `records_fts=1845` (matched). `PRAGMA integrity_check` returned `ok` both pre and post mutation. Total body characters added this tick: **595,542**.

## Records that failed this tick

| Record | URL | Failure |
|---|---|---|
| `act-zm-2026-005-national-payment-system-act` | `…/National%20Payment%20System%20Act%20No.%205%20of%202026.pdf` | HTTP 404 on parliament.gov.zm — same outcome as batches 001 and 003. Filename appears permanently dead and a manifest URL fix is needed before the next attempt. |

The 404 was logged once to `gaps.md` as `REPAIR | HTTP_404`.

## Records still remaining (19)

Acts (16): `act-zm-2026-005-national-payment-system-act` (HTTP 404), `act-zm-2026-011-the-zambia-deposit-insurance-corporation-act-2026-act-no-11-of-2026`, `act-zm-2010-034-the-national-prosecution-authority-act-2010`, `act-zm-2023-017-the-public-procurement-amendment-act-2023`, `act-zm-2024-001-constituency-development-fund-act-2024`, `act-zm-2025-025-independent-broadcasting-authority-act`, `act-zm-2025-004-cyber-crime-2025`, `act-zm-2011-013-the-zambia-qualifications-authority-act-2011`, `act-zm-2011-023-education-act-2011`, `act-zm-2011-031-customs-and-excise-amendment-act-2011`, `act-zm-2010-024-the-competition-and-consumer-protection-2010`, `act-zm-2011-004-urban-and-regional-act-2011`, `act-zm-2023-018-the-public-private-partnership-act-2023`, `act-zm-2024-010-civil-aviation-authority-amendment-act-2024`, `act-zm-2024-011-civil-aviation-amendment-act-2024`, `act-zm-2016-005-civil-aviation-act-2016`.

SIs (3): `si-zm-financial-intelligence-centre-prescribed-threshold-regulations-2022`, `si-zm-financial-intelligence-centre-general-regulations-2022`, `si-zm-financial-intelligence-centre-general-regulations-2016`.

At the per-tick rate of ~7 successful repairs the queue should drain in ~3 more ticks (allowing for further URL-404 attrition).

## Operational notes

* **Pull broken-refs treated as functionally up-to-date.** Local HEAD = remote `refs/heads/main` = `3d4c5743e1c1`. The pull command's fatal stderr is purely a side-effect of the inert `refs/remotes/origin/main.lock.bak.*` files left over from earlier sandbox crashes; nothing on the remote main was missed. This matches the batch-001 / batch-003 precedent.
* **TMPDIR-routed atomic copy** continues to be required to dodge the FUSE journal-cleanup limitation. Pattern: copy DB → `/tmp/repair_batch_004_<RAND>/corpus.sqlite` → mutate inside `/tmp` → atomic `shutil.copy2` back. No journal residue on the FUSE mount.
* **SSL chain repair** loaded `scripts/certs/rapidssl_tls_rsa_ca_g1.pem` into the SSL context to validate `parliament.gov.zm`. No verification bypass.
* **Rate limiting.** 2 s sleep between successful downloads, per SKILL.md.
* **OCR fallback** was not exercised — every successful PDF extracted ≥40k characters with pdfplumber alone. `ocrmypdf` is not installed in this sandbox.
* **B2 sync deferred to host.** `rclone` is not in the sandbox.

## Recommendations for next tick

1. **Continue down MANIFEST.** Next eight still-corrupted (in MANIFEST order): `act-zm-2026-005-national-payment-system-act` (still HTTP 404 — keep in queue but expect another fail), `act-zm-2026-011-the-zambia-deposit-insurance-corporation-act-2026-act-no-11-of-2026`, `act-zm-2010-034-the-national-prosecution-authority-act-2010`, `act-zm-2023-017-the-public-procurement-amendment-act-2023`, `act-zm-2024-001-constituency-development-fund-act-2024`, `act-zm-2025-025-independent-broadcasting-authority-act`, `act-zm-2025-004-cyber-crime-2025`, `act-zm-2011-013-the-zambia-qualifications-authority-act-2011`.
2. **Manifest URL fix needed for `act-zm-2026-005-national-payment-system-act`.** Three consecutive ticks have hit HTTP 404 on the parliament.gov.zm filename. Operator should locate the alternate URL (likely a renamed filename on parliament.gov.zm or a ZambiaLII fallback once the SI is republished) and update the SKILL.md MANIFEST.
3. **FUSE lock-file cleanup remains a host-side task.** Sandbox cannot unlink `.git/HEAD.lock`, `.git/index.lock`, `.git/objects/maintenance.lock`, or any of the 130+ `*.lock.bak.*` siblings. Recommend a host shell (outside the FUSE mount) does `rm -f .git/**/*.lock .git/**/*.lock.bak*` periodically.
