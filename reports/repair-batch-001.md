# Zambia Corpus Repair — Batch 001

**Date:** 2026-05-07 UTC (scheduled run)
**Worker:** repair-corpus (automated tick, scheduled-task SKILL)
**Operator:** automated (Claude scheduled task)
**Naming:** First batch under the new `repair-batch-NNN.md` convention specified by SKILL.md. Predecessor reports are saved as `repair-tick{3,5,6,7,9,10b}-report.md` in the corpus root.

## Headline

Batch 001 repaired **7 of 8 attempted** records. One record (`act-zm-2026-005-national-payment-system-act`) returned HTTP 404 on parliament.gov.zm — a known dead URL also documented in the prior `repair-tick10b` run. Records and FTS counts remain matched at 1845 / 1845. After this batch, **16 of 42** manifest targets are now repaired and **26 remain corrupted**.

## Records attempted (8)

In MANIFEST order, the first eight still-corrupted records as of pull commit `322001a`:

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

All seven successful repairs passed the quality gate (`length > 500`, fewer than 50% pure-digit lines, at least one ≥6-letter word) and were section-normalised before being written to `records.body`. The FTS row for each was deleted and re-inserted from the new body.

## Records that failed this tick

| Record | URL | Failure |
|---|---|---|
| `act-zm-2026-005-national-payment-system-act` | `…/National%20Payment%20System%20Act%20No.%205%20of%202026.pdf` | HTTP 404 on parliament.gov.zm (same outcome as repair-tick10b — URL appears to be permanently dead at this filename). |

Logged once to `gaps.md` as `REPAIR | HTTP_404`. Needs human-supplied source URL on a future tick (e.g. an alternate parliament.gov.zm filename or a ZambiaLII fallback once published).

## Records still remaining (26)

Acts (24): `act-zm-2016-002-constitution-2016`, `act-zm-2026-008-agricultural-marketing-act`, `act-zm-2010-027-the-animal-health`, `act-zm-2025-023-companies-amendment-act`, `act-zm-2025-008-border-management-trade-facilitation-act2025`, `act-zm-2024-030-antiterrorism-nonproliferation-2024`, `act-zm-2025-003-cyber-security-2025`, `act-zm-2026-011-the-zambia-deposit-insurance-corporation-act-2026-act-no-11-of-2026`, `act-zm-2010-034-the-national-prosecution-authority-act-2010`, `act-zm-2023-017-the-public-procurement-amendment-act-2023`, `act-zm-2024-001-constituency-development-fund-act-2024`, `act-zm-2025-025-independent-broadcasting-authority-act`, `act-zm-2025-004-cyber-crime-2025`, `act-zm-2011-013-the-zambia-qualifications-authority-act-2011`, `act-zm-2011-023-education-act-2011`, `act-zm-2011-031-customs-and-excise-amendment-act-2011`, `act-zm-2010-024-the-competition-and-consumer-protection-2010`, `act-zm-2011-004-urban-and-regional-act-2011`, `act-zm-2023-018-the-public-private-partnership-act-2023`, `act-zm-2024-010-civil-aviation-authority-amendment-act-2024`, `act-zm-2024-011-civil-aviation-amendment-act-2024`, `act-zm-2016-005-civil-aviation-act-2016`. Plus the deferred-pending `act-zm-2026-005-national-payment-system-act`.

SIs (3): `si-zm-financial-intelligence-centre-prescribed-threshold-regulations-2022`, `si-zm-financial-intelligence-centre-general-regulations-2022`, `si-zm-financial-intelligence-centre-general-regulations-2016`.

At the per-tick rate of 7 successful repairs the queue should drain in ~4 more ticks (allowing for further URL-404 attrition).

## Operational notes

* **SSL chain repair was required.** Default Python trust store does not validate parliament.gov.zm. The script reuses `scripts/certs/rapidssl_tls_rsa_ca_g1.pem` (the Phase-2 Checkpoint A intermediate) loaded into the SSL context. No verification bypass.
* **FUSE/SQLite atomic-copy pattern.** Direct in-place writes to `corpus.sqlite` on the FUSE mount produced `disk I/O error` on commit (FUSE journal-cleanup limitation, mirrors the b0519/b0520/b0521/b0523/b0525 precedent). Switched to TMPDIR-routed pattern: copy → mutate → atomic copy back. No data loss; transaction was rolled back via journal before the atomic-copy switch.
* **Rate limiting.** 2 s sleep between successful downloads, per SKILL.md.
* **OCR fallback was not exercised** — every successful PDF extracted ≥20k characters with pdfplumber alone. `ocrmypdf` is not installed in this sandbox, so any future scanned PDF would be deferred (logged but skipped).
* **Approvals/registry untouched.** Only `records.body` and `records_fts` were mutated; `approvals.yaml`, `judges_registry.yaml`, `sources.yaml` unchanged.

## Integrity

```
records:     1845
records_fts: 1845
match:       PASS
```

## Cumulative repair progress

| Cohort | Repaired | Remaining | Total |
|---|---:|---:|---:|
| Acts | 16 | 23 | 39 |
| SIs  |  0 |  3 |  3 |
| **Total** | **16** | **26** | **42** |

## B2 sync

`rclone` is not available inside this sandbox. Logged `B2 sync deferred to host` to `worker.log` per SKILL.md.

## Cost log

8 fetches against budget (7 PDFs successfully retrieved + 1 HTTP 404). Wall-clock < 1 minute for the network phase, ~25 s of pdfplumber CPU.

## Next tick recommendations

1. Continue MANIFEST-order processing of the next 8 records, starting at `act-zm-2016-002-constitution-2016`.
2. The three SI records all use ZambiaLII source URLs — those normally fetch cleanly with the same SSL configuration.
3. Surface `act-zm-2026-005-national-payment-system-act` to a human reviewer (already-known dead URL after two ticks).
