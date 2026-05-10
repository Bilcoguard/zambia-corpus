# Batch 0562 — Phase 8 Nightly Re-verification

**Date:** 2026-05-09
**Worker:** worker-tick (scheduled 30-min cadence)
**Phase:** phase_8_nightly_reverify
**Parser version:** phase8-reverify-0.1.0
**Tick number:** tenth worker-tick of UTC date 2026-05-09; fourteenth Phase 8 tick overall.

## Summary

| Metric | Value |
|---|---|
| Pool size | 1860 |
| Sample size | 8 (cap = MAX_BATCH_SIZE) |
| Sample seed | `phase8-reverify-2026-05-09-b0562` |
| Match | 5 |
| Drift | 3 |
| Fetch error | 0 |
| Truncated-stored-hash false drift | 0 |
| Fetches | 8 / 2000 (cumulative_today 80 → 88) |
| Records mutated | 0 |
| approvals.yaml mutated | no |
| Integrity check | 8 / 8 PASS (stored_sha256 unchanged on disk for all 8 sampled ids) |

## Pool growth since prior tick

Pool grew 1858 → 1860 (+2) since b0561 (worker-tick), driven by b0561 judgment-ingestion-worker writing zmcc-2019/1 and zmcc-2019/20.

## Verdicts

### Match (5) — all stable PDF endpoints

1. `si-zm-2011-002-minimum-wages-and-conditions-of-employment-general-order-2010` — zambialii `/source.pdf`
2. `act-zm-2021-011-the-public-service-pensions-amendment-act-2021` — parliament.gov.zm static PDF
3. `act-zm-2010-020-the-plea-negotiations-and-agreements-2010` — parliament.gov.zm static PDF
4. `si-zm-1993-012-income-tax-foreign-organisations-approval-and-exemption-no-2-order-1993` — zambialii `/source.pdf`
5. `si-zm-1985-019-income-tax-foreign-organisations-exemption-approval-no-4-order-1985` — zambialii `/source.pdf`

### Drift (3) — all on the established zambialii AKN-HTML drift cohort

1. `act-zm-1968-058-deeds-of-arrangement-act-1968` — `/akn/zm/act/1968/58/eng@1996-12-31` HTML
2. `si-zm-2022-060-urban-and-regional-planning-designated-local-planning-authorities-regulations-2022` — `/akn/zm/act/si/2022/60` HTML (no eng-pin — consistent with b0549 si-2020-108 finding that absence of eng-pin doesn't change drift behaviour)
3. `act-zm-1966-028-education-act-1966` — `/akn/zm/act/1966/28/eng@2003-09-16` HTML

### Fetch error (0)

None.

## Cumulative Phase 8 tally (across 14 ticks of UTC date 2026-05-09)

| Cohort | Match | Drift | Fetch err |
|---|---|---|---|
| zambialii.org `/akn/zm/act/.../HTML` (act + SI) | 0 | 46 | 0 |
| zambialii.org `/akn/zm/act/.../source.pdf` + parliament.gov.zm static PDFs | 47 | 0 | 0 |
| zambialii.org `/akn/zm/judgment/.../HTML` | 1 | 3 | 0 |
| parliament.gov.zm `/node/...` landing | 0 | 1 | 0 |

(Roll-up adjusted from b0561 cumulative 42 PDF match / 43 act-or-SI-akn-HTML drift / 1m-3d judgment-akn / 0m-1d parliament-node by adding 5 PDF match and 3 act-or-SI-akn-HTML drift this tick.)

## Working hypothesis (unchanged)

Stable PDF endpoints (zambialii `source.pdf` and parliament.gov.zm static PDFs) preserve byte-for-byte stability. Dynamically-rendered HTML endpoints (zambialii AKN-HTML for act/SI/judgment, parliament.gov.zm `/node/*` landings) carry slow-time-varying byte content — likely a server-rendered timestamp, freshness pin, or rotating ETag-derived footer. Recommendation for operator (carries forward from b0549, b0554, b0555, b0561): consider Phase 8 evolving to either (a) content-equivalent (text-extraction-stable) hashing, or (b) restricting Phase 8 to stable-PDF endpoints only. No action taken this tick.

## Integrity

- `pool_size`: 1860 records on disk with both `source_url` and `source_hash`.
- All 8 sampled record ids present on disk; stored sha256 unchanged across the tick (post-fetch verification re-read each `records/{type}/{year}/{id}.json` and compared `source_hash` to the value captured at sample time — 8/8 matched).
- No `records/` mutation. No `corpus.sqlite` mutation. No `judges_registry.yaml` mutation. No `approvals.yaml` mutation.
- `MAX_BATCH_SIZE = 8` honoured (exactly 8 fetches consumed).
- Rate limit: 5s per zambialii.org request and 2s default for parliament.gov.zm honoured throughout.
- User-Agent: `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)` on every request.

## Execution mode

Inline runner (b0548 / b0549 / b0551 / b0554 / b0555 / b0556 / b0560 / b0561 precedent). No `scripts/batch_0562_phase8_reverify.py` committed, due to sandbox-session safety constraint (the persistent stale `.git/index.lock` virtiofs unlink-not-permitted issue prevents reliable per-script commits without the b0511-pattern recovery dance, which is overkill for an idempotent re-run-safe Phase 8 reverify clone).

## Next-tick recommendations

1. Continue Phase 8 nightly reverify cadence (no change to seed scheme).
2. Standing operator action: decide on Phase 8 evolution to content-equivalent hashing or stable-PDF-only sampling, given 14-tick consistent pattern (47 stable-PDF match / 46 act-or-SI-akn-HTML drift, 1m/3d judgment-akn-HTML, 0m/1d parliament-node).
3. judgment-ingestion-worker continues independently (last tick b0561 — 2 written, 6 deferred, ZMCC 2019 dense low-num done; ZMCC 2018 HEAD probe + ZMCC 2019 finish recommended).
4. Standing parser_v0.3.3 anchor pack request unchanged (68 records pending in v0.3.3-pending cohort).
5. Standing OCR pipeline request unchanged (5 records pending).
6. Standing operator action on Phase 5 ceiling 166 / 160 (six above sentinel after b0561).

## B2 sync

Deferred to host (rclone not in sandbox).
