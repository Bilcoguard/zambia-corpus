# Zambia Corpus Repair — Batch 006

**Date:** 2026-05-08 UTC (scheduled run)
**Worker:** repair-corpus (automated tick, scheduled-task SKILL)
**Operator:** automated (Claude scheduled task; session `quirky-loving-dirac`)
**Status:** **COMPLETE — 7 successful repairs; integrity OK; live DB updated**
**Headline:** Continued the queue from batch 005. After this tick: **37 of 42** manifest targets repaired, **5** remain corrupted (one of which is the recurring parliament.gov.zm HTTP-404 record `act-zm-2026-005-national-payment-system-act`).

## Pre-flight

* Scheduled-task pre-step `find .git -name "*.lock" -delete` and `find .git -name "*.lock.bak" -delete` ran. The FUSE mount blocks unlink on some lock files (same constraint as batches 001/003/004/005). `git pull --ff-only` returned `Already up to date.` (with non-fatal warning about `.git/objects/maintenance.lock` which the FUSE mount won't allow Python to delete). Functionally up-to-date with the remote `main`.
* Live `corpus.sqlite` (~107 MB) carried 1845 records / 1845 FTS rows pre-batch. Pre-batch counts matched.
* Identified 12 still-corrupted records on entry (9 Acts + 3 SIs).
* Pre-batch DB staged via `/tmp/repair_batch_006/corpus.sqlite` (TMPDIR-routed atomic copy) to dodge the FUSE journal-cleanup limitation.

## Records attempted (8)

In MANIFEST order, the first eight still-corrupted records:

| # | Record ID | Status | Body chars | PDF bytes |
|---|---|---:|---:|---:|
| 1 | `act-zm-2026-005-national-payment-system-act` | **fail** (HTTP 404) | — | — |
| 2 | `act-zm-2011-023-education-act-2011` | ok | 116,056 | 142,766 |
| 3 | `act-zm-2011-031-customs-and-excise-amendment-act-2011` | ok | 87,701 | 258,559 |
| 4 | `act-zm-2010-024-the-competition-and-consumer-protection-2010` | ok | 100,621 | 131,109 |
| 5 | `act-zm-2011-004-urban-and-regional-act-2011` | ok | 61,521 | 79,159 |
| 6 | `act-zm-2023-018-the-public-private-partnership-act-2023` | ok | 118,092 | 1,149,155 |
| 7 | `act-zm-2024-010-civil-aviation-authority-amendment-act-2024` | ok | 143,026 | 3,224,064 |
| 8 | `act-zm-2024-011-civil-aviation-amendment-act-2024` | ok | 143,026 | 3,224,064 |

All seven successful repairs passed the quality gate (`length > 500`, fewer than 50% pure-digit lines, at least one ≥6-letter word) and were section-normalised before being written to `records.body`. The FTS row for each was deleted and re-inserted from the new body. Post-batch counts are `records=1845` and `records_fts=1845` (matched). Total body characters added this tick: **769,043**.

## Records that failed this tick

| Record | URL | Failure |
|---|---|---|
| `act-zm-2026-005-national-payment-system-act` | `…/National%20Payment%20System%20Act%20No.%205%20of%202026.pdf` | HTTP 404 on parliament.gov.zm — same outcome as batches 001, 003, 004, and 005. Filename appears permanently dead; manifest URL fix needed. |

The 404 was logged once to `gaps.md` as `REPAIR | HTTP_404`.

## Note: identical body for civil aviation 2024 records

Records `act-zm-2024-010-civil-aviation-authority-amendment-act-2024` and `act-zm-2024-011-civil-aviation-amendment-act-2024` were sourced from distinct ZambiaLII URLs (`/akn/zm/act/2024/10/...` and `/akn/zm/act/2024/11/...`) but the `source.pdf` endpoint served the **same gazette PDF** in both cases (sha1 identical, both 3,224,064 bytes; Government Gazette No. 7,631 of 16 August 2024, Vol. LX No. 996, which contains both Acts 10 and 11 of 2024 sequentially). Bodies are therefore identical. This is a publisher-side characteristic, not a worker bug — both records now hold the legally-correct gazette text and pass the quality gate. A future enhancement could split the gazette by Act-number anchor to give each record only its own Act, but that is out of scope for the repair worker.

## Records still remaining after this tick (5)

After batch 006 the following records remain corrupted and should be addressed by future ticks:

| Record ID | Source URL |
|---|---|
| `act-zm-2026-005-national-payment-system-act` | parliament.gov.zm — recurring HTTP 404 (manifest URL needs human fix) |
| `act-zm-2016-005-civil-aviation-act-2016` | https://zambialii.org/akn/zm/act/2016/5/eng@2016-01-06/source.pdf |
| `si-zm-financial-intelligence-centre-prescribed-threshold-regulations-2022` | https://zambialii.org/akn/zm/act/si/2022/53/eng@2022-08-19/source.pdf |
| `si-zm-financial-intelligence-centre-general-regulations-2022` | https://zambialii.org/akn/zm/act/si/2022/54/eng@2022-08-19/source.pdf |
| `si-zm-financial-intelligence-centre-general-regulations-2016` | https://zambialii.org/akn/zm/act/si/2016/9/eng@2016-01-29/source.pdf |

At one new tick per cycle and 4 viable records remaining (the 404 record will keep failing without a manifest URL fix), the queue should clear in **1 more tick** assuming no further OCR-required PDFs emerge.

## Diagnostics

* `worker.log` updated with `START`, pre/post counts, per-record outcomes, and `END`.
* `gaps.md` appended with one row for the HTTP-404 record.
* `costs.log` appended with `repair-batch-006 records_repaired=7 fetches=8`.
* B2 sync: **deferred to host** — `rclone` not available in this sandbox (logged to `worker.log`).
* Per-record fetch obeys 2 s rate-limit; UA `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)`.

## Integrity

* Pre-batch: records=1845, fts=1845 — matched.
* Post-batch: records=1845, fts=1845 — matched.
* No INSERT or DELETE of records was performed. Only seven UPDATE statements (one row each) plus seven matched DELETE+INSERT pairs on `records_fts`. `approvals.yaml` was not touched.

## Action items for the human operator

1. **Fix manifest URL** for `act-zm-2026-005-national-payment-system-act` — the parliament.gov.zm path returns 404 across five consecutive batches. Locate the live PDF (likely at a different filename or on ZambiaLII) and update the manifest in `SKILL.md`.
2. **B2 sync** — run `rclone copyto corpus.sqlite b2raw:kwlp-corpus-raw/corpus.sqlite` from the host once the commit lands.
3. **Optional**: split the shared 2024 gazette PDF body so that each Civil Aviation Amendment Act record holds only its own sections rather than both. This is a quality refinement, not a repair-worker concern.
