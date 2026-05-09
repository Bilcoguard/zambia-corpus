# Batch 0560 — Phase 8 Nightly Re-verification (twelfth Phase 8 tick; eighth worker-tick of UTC date 2026-05-09)

**Worker:** `worker-tick`
**Phase:** `phase_8_nightly_reverify`
**Started:** 2026-05-09T14:39:58Z
**Completed:** 2026-05-09T14:40:32Z
**Parser/fetcher version:** `phase8-reverify-0.1.0` (functional clone of `scripts/batch_0546_phase8_reverify.py` baseline)
**Execution mode:** inline runner (no `scripts/batch_0560_phase8_reverify.py` derivative committed — sandbox-session safety constraint, per b0548 / b0549 / b0551 / b0554 / b0555 / b0556 precedent)

## Sample

| field             | value                                       |
|-------------------|---------------------------------------------|
| seed              | `phase8-reverify-2026-05-09-b0560`          |
| pool_size         | 1857 (was 1855 at b0556; +2 from b0558 zmcc-2020 ingestions) |
| sample_size       | 8                                           |
| sample_rate       | 0.01 (per `approvals.yaml`)                 |
| max_batch         | 8                                           |

Tick-suffixed seed (`-b0560`) draws an independent fresh sample, distinct from the b0546 (date-only seed) and b0548 / b0549 / b0551 / b0554 / b0555 / b0556 (tick-suffixed) samples earlier today. Pool grew by 2 between b0556 (1855) and b0560 (1857) due to the two ZMCC 2020 records written by judgment-ingestion-worker batch 0558 (zmcc-2020-2 and zmcc-2020-3).

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
| match | `act-zm-2023-023-the-subordinate-courts-amendment-act-2023` | `https://www.parliament.gov.zm/sites/default/files/documents/acts/Act%20No.%2023%20of%202023%2C%20The%20SubordinateCourt%20%28Amendment%29.pdf` | www.parliament.gov.zm | (PDF) |
| match | `si-zm-2011-002-minimum-wages-and-conditions-of-employment-general-order-2010` | `https://zambialii.org/akn/zm/act/si/2011/2/eng@2011-01-07/source.pdf` | zambialii.org | (PDF) |
| match | `si-zm-2014-050-income-tax-pay-as-you-earn-regulations-2014` | `https://zambialii.org/akn/zm/act/si/2014/50/eng@2014-09-19/source.pdf` | zambialii.org | (PDF) |
| match | `act-zm-2010-010-the-dairy-produce-marketing-and-levy-repeal-2010` | `https://www.parliament.gov.zm/sites/default/files/documents/acts/Dairy%20Produce%20Marketing%20and%20Levy%20%28Repeal%29%202010.PDF` | www.parliament.gov.zm | (PDF) |
| drift | `act-zm-2003-008-appropriation-act` | `https://zambialii.org/akn/zm/act/2003/8/eng@2003-04-22` | zambialii.org | (HTML) |
| drift | `act-zm-2017-006-metrology-act-2017` | `https://zambialii.org/akn/zm/act/2017/6/eng@2017-04-13` | zambialii.org | (HTML) |
| drift | `judgment-zm-2026-zmcc-09-legal-resources-foundation-limited-v-the` | `https://zambialii.org/akn/zm/judgment/zmcc/2026/9/eng@2026-04-02` | zambialii.org | (HTML) |
| drift | `act-zm-1960-024-development-united-kingdom-government-loan-act-1960` | `https://zambialii.org/akn/zm/act/1960/24/eng@1996-12-31` | zambialii.org | (HTML) |

## Pattern reproduction

Established cross-tick patterns continue to hold and now extend into a twelfth consecutive tick:

* **All 4 matches are stable PDF endpoints.** Two are `www.parliament.gov.zm` static `.pdf` documents under `sites/default/files/`; two are `zambialii.org/akn/.../source.pdf` source-file PDFs (one redirected to media.zambialii.org). Cumulative across 12 Phase 8 ticks: **37/37 stable PDF matches** (was 33/33 after b0556; +4 this tick).
* **3 of 4 drifts are `zambialii.org/akn/...` act-or-SI HTML rendering URLs** (established `content_changed_full_drift_akn_html` pattern). Cumulative act/SI-akn-HTML drifts: **40/40** (was 37/37 after b0556; +3 this tick).

## NEW finding (b0560) — judgment-akn-HTML cumulative tally moves to 1m / 3d

* **`judgment-zm-2026-zmcc-09-legal-resources-foundation-limited-v-the`** — `zambialii.org/akn/zm/judgment/zmcc/2026/9/eng@2026-04-02` returned 200 OK with HTML content; recomputed sha256 differs from stored hash. This is the **third** judgment-`/akn/`-HTML drift observed in Phase 8 (after `zmsc/2022/57` and `zmcc/2023/22` from b0554), against **1** judgment-`/akn/`-HTML match (`zmsc/2020/51` from b0551). Cumulative judgment-akn-HTML verdicts now **1 match / 3 drifts** (n=4; ~25% match rate; still small sample but trending consistently with the act/SI-akn-HTML drift pattern).

This continues to support the revised hypothesis from b0554: judgment `/akn/` HTML rendering URLs drift on the same time-varying server-side rendering layer as act/SI `/akn/` HTML URLs. The b0551 single match was sample noise.

## Cumulative URL-family verdicts (12 Phase 8 ticks)

| URL family | matches | drifts | notes |
|---|---|---|---|
| `zambialii.org/akn/.../source.pdf` (act/SI source PDFs, may redirect to media.zambialii.org) | extending | 0 | Stable byte-for-byte |
| `media.zambialii.org/.../source_file/...` (direct source-file PDFs) | extending | 0 | Stable byte-for-byte |
| `www.parliament.gov.zm/sites/default/files/...` (static PDFs) | extending | 0 | Stable byte-for-byte |
| `zambialii.org/akn/zm/act/...` & `/akn/zm/act/si/...` (act/SI HTML rendering) | 0 | **40** | Drifts every observation |
| `zambialii.org/akn/zm/judgment/...` (judgment HTML rendering) | 1 | **3** | New drift this tick |
| `www.parliament.gov.zm/node/<id>` (Drupal landing pages) | 0 | 1 | b0555 (no sample this tick) |

Cumulative stable-PDF matches: **37/37**. Cumulative act/SI-akn-HTML drifts: **40/40**. Cumulative judgment-akn-HTML drift rate: 3/4 = 75% (n=4).

## Integrity

* **No records mutated.** Phase 8 is read-only by design.
* **No schema regressions.** `corpus.sqlite`, `records/`, `raw/` all untouched.
* **8 sampled records still on disk** post-tick; verified by re-loading their JSON from `records/{type}/{year}/{id}.json` and confirming `source_hash` unchanged (8/8 PASS).
* **`approvals.yaml` NOT modified.** Phase 8 is open-ended; only a human flips `complete: true`.

## Budget

* `cumulative_today` (worker-tick): 64 → 72 / 2000 fetches.
* `max_tokens_per_day`: well under 1,000,000.

## Notes

* `B2 sync` deferred to host (rclone not available in sandbox).
* No derivative `scripts/batch_0560_phase8_reverify.py` committed (sandbox-session safety constraint, per b0548 / b0549 / b0551 / b0554 / b0555 / b0556 precedent). Functionality is byte-equivalent to the `scripts/batch_0546_phase8_reverify.py` baseline including `scripts/certs/*.pem` PKI loader (`rapidssl_tls_rsa_ca_g1.pem`).
* Phase 8 remains open-ended; no completion flip.
