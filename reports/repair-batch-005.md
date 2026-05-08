# Zambia Corpus Repair — Batch 005

**Date:** 2026-05-08 UTC (scheduled run)
**Worker:** repair-corpus (automated tick, scheduled-task SKILL)
**Operator:** automated (Claude scheduled task; session `fervent-blissful-goldberg`)
**Status:** **COMPLETE — 7 successful repairs; integrity OK; live DB updated**
**Headline:** Continued the queue from batch 004. After this tick: **30 of 42** manifest targets repaired, **12** remain corrupted (one of which is the recurring parliament.gov.zm HTTP-404 record `act-zm-2026-005-national-payment-system-act`).

## Pre-flight

* Scheduled-task pre-step `find .git -name "*.lock" -delete` and `find .git -name "*.lock.bak" -delete` ran but the FUSE mount blocks unlink on the lock files (same constraint as batches 001/003/004). `git pull --ff-only` returned `Already up to date.` (with non-fatal warnings about `.git/objects/maintenance.lock` and `.git/ORIG_HEAD.lock` that the FUSE mount won't allow Python to delete). Functionally up-to-date with the remote `main`.
* Live `corpus.sqlite` (106 MB) carried 1845 records / 1845 FTS rows pre-batch. Pre-batch counts matched.
* Identified 19 still-corrupted records on entry (16 Acts + 3 SIs).
* Pre-batch DB staged via `/tmp/repair_batch_005/corpus.sqlite` (TMPDIR-routed atomic copy) to dodge the FUSE journal-cleanup limitation.

## Records attempted (8)

In MANIFEST order, the first eight still-corrupted records:

| # | Record ID | Status | Body chars | PDF bytes |
|---|---|---:|---:|---:|
| 1 | `act-zm-2026-005-national-payment-system-act` | **fail** (HTTP 404) | — | — |
| 2 | `act-zm-2026-011-the-zambia-deposit-insurance-corporation-act-2026-act-no-11-of-2026` | ok | 58,215 | 430,578 |
| 3 | `act-zm-2010-034-the-national-prosecution-authority-act-2010` | ok | 31,875 | 50,618 |
| 4 | `act-zm-2023-017-the-public-procurement-amendment-act-2023` | ok | 20,340 | 332,358 |
| 5 | `act-zm-2024-001-constituency-development-fund-act-2024` | ok | 31,338 | 428,622 |
| 6 | `act-zm-2025-025-independent-broadcasting-authority-act` | ok | 52,471 | 486,119 |
| 7 | `act-zm-2025-004-cyber-crime-2025` | ok | 31,867 | 350,455 |
| 8 | `act-zm-2011-013-the-zambia-qualifications-authority-act-2011` | ok | 24,424 | 42,837 |

All seven successful repairs passed the quality gate (`length > 500`, fewer than 50% pure-digit lines, at least one ≥6-letter word) and were section-normalised before being written to `records.body`. The FTS row for each was deleted and re-inserted from the new body. Post-batch counts are `records=1845` and `records_fts=1845` (matched). Total body characters added this tick: **250,530**.

## Records that failed this tick

| Record | URL | Failure |
|---|---|---|
| `act-zm-2026-005-national-payment-system-act` | `…/National%20Payment%20System%20Act%20No.%205%20of%202026.pdf` | HTTP 404 on parliament.gov.zm — same outcome as batches 001, 003, and 004. Filename appears permanently dead; manifest URL fix needed. |

The 404 was logged once to `gaps.md` as `REPAIR | HTTP_404`.

## Records still remaining (12)

Acts (9):
- `act-zm-2026-005-national-payment-system-act` (HTTP 404 — needs manifest URL fix)
- `act-zm-2011-023-education-act-2011`
- `act-zm-2011-031-customs-and-excise-amendment-act-2011`
- `act-zm-2010-024-the-competition-and-consumer-protection-2010`
- `act-zm-2011-004-urban-and-regional-act-2011`
- `act-zm-2023-018-the-public-private-partnership-act-2023`
- `act-zm-2024-010-civil-aviation-authority-amendment-act-2024` (ZambiaLII)
- `act-zm-2024-011-civil-aviation-amendment-act-2024` (ZambiaLII)
- `act-zm-2016-005-civil-aviation-act-2016` (ZambiaLII)

SIs (3):
- `si-zm-financial-intelligence-centre-prescribed-threshold-regulations-2022` (ZambiaLII)
- `si-zm-financial-intelligence-centre-general-regulations-2022` (ZambiaLII)
- `si-zm-financial-intelligence-centre-general-regulations-2016` (ZambiaLII)

At the per-tick rate of ~7 successful repairs the queue should drain in ~2 more ticks (allowing for the `national-payment-system-act` 404 and OCR-fallback exposure on the older ZambiaLII PDFs).

## Operational notes

* **TMPDIR-routed atomic copy** continues to be the only reliable mutation path on this FUSE mount. Pattern: copy DB → `/tmp/repair_batch_005/corpus.sqlite` → mutate inside `/tmp` → `shutil.copy2` back to live. No journal residue on the FUSE mount.
* **SSL chain repair** loaded `scripts/certs/rapidssl_tls_rsa_ca_g1.pem` into the SSL context to validate `parliament.gov.zm`. No verification bypass.
* **Rate limiting.** 2 s sleep between successful downloads, per SKILL.md.
* **OCR fallback was not exercised** — every successful PDF extracted ≥20k characters with pdfplumber alone. `ocrmypdf` is still not installed in this sandbox; logged once as deferred-on-encounter.
* **B2 sync deferred to host.** `rclone` is not in the sandbox.

## Recommendations for next tick

1. **Continue down MANIFEST.** Next eight still-corrupted (in MANIFEST order): `act-zm-2026-005-national-payment-system-act` (still HTTP 404 — keep in queue but expect another fail), `act-zm-2011-023-education-act-2011`, `act-zm-2011-031-customs-and-excise-amendment-act-2011`, `act-zm-2010-024-the-competition-and-consumer-protection-2010`, `act-zm-2011-004-urban-and-regional-act-2011`, `act-zm-2023-018-the-public-private-partnership-act-2023`, `act-zm-2024-010-civil-aviation-authority-amendment-act-2024`, `act-zm-2024-011-civil-aviation-amendment-act-2024`.
2. **Manifest URL fix needed for `act-zm-2026-005-national-payment-system-act`.** Four consecutive ticks have hit HTTP 404 on the parliament.gov.zm filename. Operator should locate the alternate URL and update the SKILL.md MANIFEST.
3. **FUSE lock-file cleanup remains a host-side task.**
