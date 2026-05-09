# Batch 0561 — Phase 8 Nightly Re-verification (thirteenth Phase 8 tick; ninth worker-tick of UTC date 2026-05-09)

**Worker:** `worker-tick`
**Phase:** `phase_8_nightly_reverify`
**Started:** 2026-05-09T15:04:00Z
**Completed:** 2026-05-09T15:04:40Z
**Parser/fetcher version:** `phase8-reverify-0.1.0` (functional clone of `scripts/batch_0546_phase8_reverify.py` baseline)
**Execution mode:** inline runner (no `scripts/batch_0561_phase8_reverify.py` derivative committed — sandbox-session safety constraint, per b0548 / b0549 / b0551 / b0554 / b0555 / b0556 / b0560 precedent)

## Sample

| field             | value                                       |
|-------------------|---------------------------------------------|
| seed              | `phase8-reverify-2026-05-09-b0561`          |
| pool_size         | 1858 (was 1857 at b0560; +1 from b0560 judgment-ingestion-worker zmcc-2020-17 ingestion) |
| sample_size       | 8                                           |
| sample_rate       | 0.01 (per `approvals.yaml`)                 |
| max_batch         | 8                                           |

Tick-suffixed seed (`-b0561`) draws an independent fresh sample, distinct from the b0546 (date-only seed) and b0548 / b0549 / b0551 / b0554 / b0555 / b0556 / b0560 (tick-suffixed) samples earlier today. Pool grew by 1 between b0560 (1857) and b0561 (1858) due to the one ZMCC 2020 record (zmcc-2020-17 *Mulubisha v Attorney-General*) written by judgment-ingestion-worker batch 0560 at 14:45Z.

## Verdicts

| verdict     | count |
|-------------|-------|
| match       | 5     |
| drift       | 3     |
| fetch_error | 0     |
| **truncated_stored_hash_false_drift** | **0** |
| **fetches** | **8** |

### Per-record results

| verdict | id | URL | host | bytes |
|---------|----|----|------|-------|
| match | `act-zm-2024-015-zambia-national-public-health-institute-amendment-act-2024` | `https://www.parliament.gov.zm/sites/default/files/documents/acts/Act%20No.%2015%20of%202024%20Zambia%20National%20Public%20Health%20Institute%20Act.pdf` | www.parliament.gov.zm | (PDF) |
| match | `si-zm-2016-031-postal-and-courier-services-general-regulations-2015` | `https://zambialii.org/akn/zm/act/si/2016/31/eng@2016-04-29/source.pdf` | zambialii.org | (PDF) |
| drift | `act-zm-1980-008-public-audit-act-1980` | `https://zambialii.org/akn/zm/act/1980/8/eng@1996-12-31` | zambialii.org | (HTML) |
| drift | `act-zm-1964-045-defence-act-1964` | `https://zambialii.org/akn/zm/act/1964/45/eng@1996-12-31` | zambialii.org | (HTML) |
| drift | `act-zm-1991-001-constitution-of-zambia-act-1991` | `https://zambialii.org/akn/zm/act/1991/1/eng@2025-12-18` | zambialii.org | (HTML) |
| match | `si-zm-2011-035-income-tax-foreign-personnel-approval-and-exemption-order-2011` | `https://zambialii.org/akn/zm/act/si/2011/35/eng@2011-04-15/source.pdf` | zambialii.org | (PDF) |
| match | `act-zm-2019-007-food-safety-act-2019` | `https://www.parliament.gov.zm/sites/default/files/documents/acts/The%20Food%20Safety%20%20Act%20No.%207%2C%202019.pdf` | www.parliament.gov.zm | (PDF) |
| match | `si-zm-2011-049-value-added-tax-exemption-order-2011` | `https://zambialii.org/akn/zm/act/si/2011/49/eng@2011-05-27/source.pdf` | zambialii.org | (PDF) |

## Pattern reproduction

Established cross-tick patterns continue to hold and now extend into a thirteenth consecutive tick:

* **All 5 matches are stable PDF endpoints.** Two are `www.parliament.gov.zm` static `.pdf` documents under `sites/default/files/`; three are `zambialii.org/akn/.../source.pdf` source-file PDFs. Cumulative across 13 Phase 8 ticks: **42/42 stable PDF matches** (was 37/37 after b0560; +5 this tick).
* **All 3 drifts are `zambialii.org/akn/...` act HTML rendering URLs** (established `content_changed_full_drift_akn_html` pattern). Cumulative act/SI-akn-HTML drifts: **43/43** (was 40/40 after b0560; +3 this tick).
* **No new URL-family verdicts this tick.** No judgment-/akn/-HTML or parliament-/node/-landing URLs sampled this tick; those cumulative tallies unchanged at 1m/3d and 0m/1d respectively.

## Notable individual finding (b0561) — Constitution-of-Zambia 1991 enrolled in act-akn-HTML drift cohort

* **`act-zm-1991-001-constitution-of-zambia-act-1991`** drifted on its `zambialii.org/akn/zm/act/1991/1/eng@2025-12-18` HTML rendering URL. This is the founding constitutional instrument for the Republic of Zambia — its presence in the act-akn-HTML drift cohort confirms the rendering-layer pattern applies uniformly across all act categories, including the most senior primary authority. The drift mechanism (server-side rendering layer time-variance) is unchanged; the underlying source PDF (`source.pdf` endpoint, if present in records) would be expected to remain byte-stable per the cumulative 42/42 stable-PDF pattern. **No record mutated.**

## Cumulative URL-family verdicts (13 Phase 8 ticks)

| URL family | matches | drifts | notes |
|---|---|---|---|
| `zambialii.org/akn/.../source.pdf` (act/SI source PDFs, may redirect to media.zambialii.org) | extending | 0 | Stable byte-for-byte |
| `media.zambialii.org/.../source_file/...` (direct source-file PDFs) | extending | 0 | Stable byte-for-byte |
| `www.parliament.gov.zm/sites/default/files/...` (static PDFs) | extending | 0 | Stable byte-for-byte |
| `zambialii.org/akn/zm/act/...` & `/akn/zm/act/si/...` (act/SI HTML rendering) | 0 | **43** | Drifts every observation |
| `zambialii.org/akn/zm/judgment/...` (judgment HTML rendering) | 1 | 3 | No sample this tick (cumulative tally unchanged) |
| `www.parliament.gov.zm/node/<id>` (Drupal landing pages) | 0 | 1 | b0555 (no sample this tick) |

Cumulative stable-PDF matches: **42/42**. Cumulative act/SI-akn-HTML drifts: **43/43**. Cumulative judgment-akn-HTML drift rate: 3/4 = 75% (n=4; unchanged).

## Integrity

* **No records mutated.** Phase 8 is read-only by design.
* **No schema regressions.** `corpus.sqlite`, `records/`, `raw/` all untouched by this tick.
* **8 sampled records still on disk** post-tick; verified by re-loading their JSON from `records/{type}/{year}/{id}.json` and confirming `source_hash` unchanged (8/8 PASS).
* **`approvals.yaml` NOT modified.** Phase 8 is open-ended; only a human flips `complete: true`.

## Budget

* `cumulative_today` (worker-tick): 72 → 80 / 2000 fetches.
* `max_tokens_per_day`: well under 1,000,000.

## Notes

* `B2 sync` deferred to host (rclone not available in sandbox).
* No derivative `scripts/batch_0561_phase8_reverify.py` committed (sandbox-session safety constraint, per b0548 / b0549 / b0551 / b0554 / b0555 / b0556 / b0560 precedent). Functionality is byte-equivalent to the `scripts/batch_0546_phase8_reverify.py` baseline including `scripts/certs/*.pem` PKI loader (`rapidssl_tls_rsa_ca_g1.pem`).
* Phase 8 remains open-ended; no completion flip.
