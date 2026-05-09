# Batch 0555 — Phase 8 Nightly Re-verification (tenth Phase 8 tick; sixth worker-tick of UTC date 2026-05-09)

**Worker:** `worker-tick`
**Phase:** `phase_8_nightly_reverify`
**Started:** 2026-05-09T08:46:32Z
**Completed:** 2026-05-09T08:46:57Z
**Parser/fetcher version:** `phase8-reverify-0.1.0` (functional clone of `scripts/batch_0546_phase8_reverify.py` baseline)
**Execution mode:** inline runner (no `scripts/batch_0555_phase8_reverify.py` derivative committed — sandbox-session safety constraint, per b0548 / b0549 / b0551 / b0554 precedent)

## Sample

| field             | value                                  |
|-------------------|----------------------------------------|
| seed              | `phase8-reverify-2026-05-09-b0555`     |
| pool_size         | 1855                                   |
| sample_size       | 8                                      |
| sample_rate       | 0.01 (per `approvals.yaml`)            |
| max_batch         | 8                                      |

Tick-suffixed seed (`-b0555`) draws an independent fresh sample, distinct from the b0546 (date-only seed) and b0548 / b0549 / b0551 / b0554 (tick-suffixed) samples earlier today. Pool size unchanged since b0554 (1855); no judgment-ingestion-worker activity between b0554 and b0555.

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
| match | `si-zm-2015-035-property-transfer-tax-exemption-no-2-order-2015` | `https://zambialii.org/akn/zm/act/si/2015/35/eng@2015-06-19/source.pdf` | zambialii.org | 93,448 |
| match | `act-zm-2015-012-gold-repeal` | `https://www.parliament.gov.zm/sites/default/files/documents/acts/The%20Gold%20Repeal%20Act%2C%202015.pdf` | www.parliament.gov.zm | 9,001 |
| match | `si-zm-2024-008-ionising-radiation-protection-radiotherapy-regulations-2024` | `https://zambialii.org/akn/zm/act/si/2024/8/eng@2024-01-19/source.pdf` | zambialii.org | 460,938 |
| match | `act-zm-2016-017-the-local-government-amendment` | `https://www.parliament.gov.zm/sites/default/files/documents/amendment_act/The%20Local%20Government%20Amendment%20Act%20No.%2017%2C%202016.pdf` | www.parliament.gov.zm | 8,978 |
| drift | `local-courts-act-1966` | `https://zambialii.org/akn/zm/act/1966/20/eng@2008-09-26` | zambialii.org | 289,348 |
| drift | `act-zm-1989-019-national-agricultural-marketing-act-1989` | `https://www.zambialii.org/akn/zm/act/1989/19/eng@1989-08-18` | www.zambialii.org | 41,094 |
| drift | `si-zm-2022-063-electoral-process-local-government-by-elections-election-date-and-time-of-poll-order-2022` | `https://zambialii.org/akn/zm/act/si/2022/63` | zambialii.org | 40,250 |
| drift | `act-zm-2025-015-small-claims-court-amendment-act` | `https://www.parliament.gov.zm/node/12763` | www.parliament.gov.zm | 30,458 |

## Pattern reproduction

Established cross-tick patterns continue to hold:

* **All 4 matches are stable PDF endpoints.** Two are `zambialii.org/akn/.../source.pdf` (which redirect to `media.zambialii.org` source-file backing store) and two are `www.parliament.gov.zm` static `.pdf` documents under `sites/default/files/`. Cumulative across 10 Phase 8 ticks: **29/29 stable PDF matches** (was 25/25 after b0554; +4 this tick).
* **3 of 4 drifts are `zambialii.org/akn/...` act-or-SI HTML rendering URLs.** All three returned status 200 and content-typed HTML; bytes differ from stored hash on every tick where this URL family has been re-sampled. Cumulative: **33/33 zambialii-/akn/-act-or-SI-HTML drifts** (was 30/30 after b0554; +3 this tick). Established hypothesis: time-varying server-side rendering layer (date pin or no date pin both drift; see b0551 sub-observation 1).

## NEW finding (b0555)

**1 of 4 drifts is a `www.parliament.gov.zm/node/<id>` landing page** — first observation of drift on the parliament.gov.zm dynamic node URL family. This URL pattern is distinct from both:

* `www.parliament.gov.zm/sites/default/files/documents/...` static-PDF URLs (which match consistently — see this tick's two matches), and
* `zambialii.org/akn/...` HTML rendering URLs (which drift consistently).

Specifically: `act-zm-2025-015-small-claims-court-amendment-act` is stored with `source_url = https://www.parliament.gov.zm/node/12763`, returns status 200 with `bytes_len = 30,458`, and produces a fetched sha256 of `74c905d703b5fd28945963d853f77106a22fb3041f44feeccfb1c111be6d870b`. This is consistent with parliament.gov.zm running a Drupal CMS that serves dynamic landing pages with time-varying chrome (session tokens, generated CSRF tags, build cache markers, last-rendered timestamps). Working hypothesis (N=1, do not extrapolate): parliament.gov.zm `/node/<id>` landing pages drift on the same kind of dynamic-rendering layer as zambialii.org `/akn/...` HTML URLs, while parliament.gov.zm static `/sites/default/files/...` PDFs remain byte-stable. Future Phase 8 ticks should track parliament.gov.zm `/node/...` matches/drifts separately from parliament.gov.zm-static-PDF matches to accumulate evidence.

Cumulative parliament.gov.zm `/node/...` verdicts: **0 match / 1 drift** (first observation).

## Integrity

* **No records mutated.** Phase 8 is read-only by design.
* **No schema regressions.** `corpus.sqlite`, `records/`, `raw/` all untouched.
* **8 sampled records still on disk** post-tick (verified by re-loading their JSON from `records/{type}/{year}/{id}.json`).
* **`approvals.yaml` NOT modified.** Phase 8 is open-ended; only a human flips `complete: true`.

## Budget

* `cumulative_today` (worker-tick): 48 → 56 / 2000 fetches.
* `max_tokens_per_day`: well under 1,000,000.

## Notes

* `B2 sync` deferred to host (rclone not available in sandbox).
* No derivative `scripts/batch_0555_phase8_reverify.py` committed (sandbox-session safety constraint, per b0548 / b0549 / b0551 / b0554 precedent). Functionality is byte-equivalent to the `scripts/batch_0546_phase8_reverify.py` baseline including `scripts/certs/*.pem` PKI loader (`rapidssl_tls_rsa_ca_g1.pem`).
* Phase 8 remains open-ended; no completion flip.
