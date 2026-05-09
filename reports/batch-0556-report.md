# Batch 0556 — Phase 8 Nightly Re-verification (eleventh Phase 8 tick; seventh worker-tick of UTC date 2026-05-09)

**Worker:** `worker-tick`
**Phase:** `phase_8_nightly_reverify`
**Started:** 2026-05-09T09:04:04Z
**Completed:** 2026-05-09T09:04:34Z
**Parser/fetcher version:** `phase8-reverify-0.1.0` (functional clone of `scripts/batch_0546_phase8_reverify.py` baseline)
**Execution mode:** inline runner (no `scripts/batch_0556_phase8_reverify.py` derivative committed — sandbox-session safety constraint, per b0548 / b0549 / b0551 / b0554 / b0555 precedent)

## Sample

| field             | value                                  |
|-------------------|----------------------------------------|
| seed              | `phase8-reverify-2026-05-09-b0556`     |
| pool_size         | 1855                                   |
| sample_size       | 8                                      |
| sample_rate       | 0.01 (per `approvals.yaml`)            |
| max_batch         | 8                                      |

Tick-suffixed seed (`-b0556`) draws an independent fresh sample, distinct from the b0546 (date-only seed) and b0548 / b0549 / b0551 / b0554 / b0555 (tick-suffixed) samples earlier today. Pool size unchanged since b0554/b0555 (1855); no judgment-ingestion-worker activity between b0555 and b0556.

## Verdicts

| verdict     | count |
|-------------|-------|
| match       | 4     |
| drift       | 4     |
| fetch_error | 0     |
| **truncated_stored_hash_false_drift** | **0** |
| **fetches** | **8** |

### Per-record results

| verdict | id | URL | host | bytes |
|---------|----|----|------|-------|
| match | `act-zm-2011-020-the-liquor-licensing-act-2011` | `https://www.parliament.gov.zm/sites/default/files/documents/acts/Liqour%20Licensing%20Act%2C%202011.pdf` | www.parliament.gov.zm | 75,885 |
| match | `act-zm-2011-006-the-english-law-extent-of-application-amendment-act-2011` | `https://www.parliament.gov.zm/sites/default/files/documents/amendment_act/The%20English%20Law%20Act.pdf` | www.parliament.gov.zm | 15,800 |
| match | `si-zm-2005-010-taxation-provisional-charging-order-2005` | `https://zambialii.org/akn/zm/act/si/2005/10/eng@2005-01-28/source.pdf` | zambialii.org | 128,972 |
| match | `si-zm-2025-009-bank-of-zambia-withdrawal-and-exchange-of-currency-regulations-2025` | `https://media.zambialii.org/media/legislation/44173/source_file/1fe34b6ef23bc96a/bank-of-zambia-withdrawal-and-exchange-of-currency-regulations-2025.pdf` | media.zambialii.org | 542,250 |
| drift | `act-zm-1960-059-land-survey-act-1960` | `https://zambialii.org/akn/zm/act/1960/59/eng@1996-12-31` | zambialii.org | 283,045 |
| drift | `si-zm-2020-101-electoral-process-local-government-by-elections-election-date-and-time-of-poll-no-8-order-2020` | `https://zambialii.org/akn/zm/act/si/2020/101` | zambialii.org | 39,524 |
| drift | `act-zm-1976-022-supreme-court-and-high-court-number-of-judges-act-1976` | `https://zambialii.org/akn/zm/act/1976/22/eng@1996-12-31` | zambialii.org | 40,552 |
| drift | `act-zm-1984-006-supplementary-appropriation-1982-act-1984` | `https://zambialii.org/akn/zm/act/1984/6/eng@1984-03-30` | zambialii.org | 38,765 |

## Pattern reproduction

Established cross-tick patterns continue to hold and now extend into an eleventh consecutive tick:

* **All 4 matches are stable PDF endpoints.** Two are `www.parliament.gov.zm` static `.pdf` documents under `sites/default/files/`, one is a `zambialii.org/akn/.../source.pdf` (which redirects to `media.zambialii.org` source-file backing store), and one is a direct `media.zambialii.org` source-file PDF. Cumulative across 11 Phase 8 ticks: **33/33 stable PDF matches** (was 29/29 after b0555; +4 this tick).
* **All 4 drifts are `zambialii.org/akn/...` act-or-SI HTML rendering URLs.** All four returned status 200 with HTML content; bytes differ from stored hash. Cumulative: **37/37 zambialii-/akn/-act-or-SI-HTML drifts** (was 33/33 after b0555; +4 this tick). Established hypothesis continues: time-varying server-side rendering layer; date-pinned and date-unpinned URLs both drift (one date-unpinned this tick: `si-zm-2020-101 → /akn/zm/act/si/2020/101`).

## NEW finding (b0556)

**No new URL-family verdicts this tick.** All 8 sampled records fall in already-tracked URL families:

* parliament.gov.zm static PDF (matches): cumulative **6/6** matches (added 2 this tick).
* zambialii.org `/akn/.../source.pdf` redirected to media.zambialii.org (matches): cumulative tally extended.
* media.zambialii.org direct source-file PDFs (matches): cumulative tally extended.
* zambialii.org `/akn/...` act-or-SI HTML (drifts): cumulative **37/37** drifts (added 4 this tick).

No judgment `/akn/` HTML URLs sampled this tick — judgment-akn cumulative tally remains at **1 match / 2 drifts** from b0551 / b0554. No parliament.gov.zm `/node/<id>` URLs sampled this tick — parliament-node cumulative tally remains at **0 match / 1 drift** from b0555.

## Integrity

* **No records mutated.** Phase 8 is read-only by design.
* **No schema regressions.** `corpus.sqlite`, `records/`, `raw/` all untouched.
* **8 sampled records still on disk** post-tick (verified by re-loading their JSON from `records/{type}/{year}/{id}.json` and confirming `source_hash` unchanged).
* **`approvals.yaml` NOT modified.** Phase 8 is open-ended; only a human flips `complete: true`.

## Budget

* `cumulative_today` (worker-tick): 56 → 64 / 2000 fetches.
* `max_tokens_per_day`: well under 1,000,000.

## Notes

* `B2 sync` deferred to host (rclone not available in sandbox).
* No derivative `scripts/batch_0556_phase8_reverify.py` committed (sandbox-session safety constraint, per b0548 / b0549 / b0551 / b0554 / b0555 precedent). Functionality is byte-equivalent to the `scripts/batch_0546_phase8_reverify.py` baseline including `scripts/certs/*.pem` PKI loader (`rapidssl_tls_rsa_ca_g1.pem`).
* Phase 8 remains open-ended; no completion flip.
