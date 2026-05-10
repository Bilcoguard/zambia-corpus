# Batch 0563 — Phase 8 Nightly Re-verification

**Date:** 2026-05-10
**Worker:** worker-tick (scheduled 30-min cadence)
**Phase:** phase_8_nightly_reverify
**Parser version:** phase8-reverify-0.1.0
**Tick number:** first worker-tick of UTC date 2026-05-10; fifteenth Phase 8 tick overall.

## Summary

| Metric | Value |
|---|---|
| Pool size | 1860 |
| Sample size | 8 (cap = MAX_BATCH_SIZE) |
| Sample seed | `phase8-reverify-2026-05-10-b0563` |
| Match | 4 |
| Drift | 4 |
| Fetch error | 0 |
| Truncated-stored-hash false drift | 0 |
| Fetches | 8 / 2000 (cumulative_today 0 → 8 — first tick of new UTC date) |
| Records mutated | 0 |
| approvals.yaml mutated | no |
| Integrity check | 8 / 8 PASS (stored_sha256 unchanged on disk for all 8 sampled ids) |

## Pool growth since prior tick

Pool unchanged at 1860 since b0562 (worker-tick close). No judgment-ingestion-worker tick has run since b0561 added zmcc-2019/1 + zmcc-2019/20.

## Verdicts

### Match (4) — all stable PDF endpoints

1. `act-zm-2011-023-education-act-2011` — parliament.gov.zm static PDF
2. `act-zm-2009-015-information-and-communication-technologies` — parliament.gov.zm static PDF (18.7 MB)
3. `si-zm-2024-003-national-pension-scheme-penalty-waiver-regulations-2024` — zambialii `/source.pdf`
4. `act-zm-2013-016-the-customs-and-excise-amendment-2013` — parliament.gov.zm static PDF (amendment_act path)

### Drift (4) — 3 act-akn-HTML cohort + 1 judgment-akn-HTML cohort

1. `act-zm-2012-005-supplementary-appropriation-2010-act` — `/akn/zm/act/2012/5/eng@2012-04-16` HTML (zambialii AKN-HTML act cohort)
2. `act-zm-1995-015-electricity-act-1995` — `/akn/zm/act/1995/15/eng@1996-12-31` HTML (zambialii AKN-HTML act cohort)
3. `act-zm-1994-031-national-arts-council-of-zambia-act-1994` — `/akn/zm/act/1994/31/eng@1996-12-31` HTML on `www.zambialii.org` host (zambialii AKN-HTML act cohort; bare-vs-www host both behave identically per established hypothesis)
4. `judgment-zm-2023-zmsc-05-mwansa-v-people` — `/akn/zm/judgment/zmsc/2023/5/eng@2023-04-13` HTML (judgment-akn-HTML drift cohort — fourth observation)

### Fetch error (0)

None.

## Cumulative Phase 8 tally (across 15 ticks; 14 on 2026-05-09 + 1 on 2026-05-10)

| Cohort | Match | Drift | Fetch err |
|---|---|---|---|
| zambialii.org `/akn/zm/act/.../HTML` (act + SI) | 0 | 49 | 0 |
| zambialii.org `/akn/zm/act/.../source.pdf` + parliament.gov.zm static PDFs | 51 | 0 | 0 |
| zambialii.org `/akn/zm/judgment/.../HTML` | 1 | 4 | 0 |
| parliament.gov.zm `/node/...` landing | 0 | 1 | 0 |

(Roll-up adjusted from b0562 cumulative 47 PDF match / 46 act-or-SI-akn-HTML drift / 1m-3d judgment-akn / 0m-1d parliament-node by adding 4 PDF match, 3 act-or-SI-akn-HTML drift, and 1 judgment-akn-HTML drift this tick.)

## Notable observation this tick

The `act-zm-1994-031-national-arts-council-of-zambia-act-1994` candidate carries the `www.zambialii.org` host prefix (versus the bare `zambialii.org` host on the rest of the AKN-HTML cohort). Drift verdict is identical, confirming the rendering-layer drift is not host-prefix-sensitive — the same Cantemo / akoma-ntoso renderer is reached via both DNS aliases.

## Working hypothesis (unchanged)

Stable PDF endpoints (zambialii `source.pdf` and parliament.gov.zm static PDFs) preserve byte-for-byte stability. Dynamically-rendered HTML endpoints (zambialii AKN-HTML for act/SI/judgment, parliament.gov.zm `/node/*` landings) carry slow-time-varying byte content — likely a server-rendered timestamp, freshness pin, or rotating ETag-derived footer. Recommendation for operator (carries forward from b0549, b0554, b0555, b0561, b0562): consider Phase 8 evolving to either (a) content-equivalent (text-extraction-stable) hashing, or (b) restricting Phase 8 to stable-PDF endpoints only. No action taken this tick.

## Integrity

- `pool_size`: 1860 records on disk with both `source_url` and `source_hash`.
- All 8 sampled record ids present on disk; stored sha256 unchanged across the tick (post-fetch verification re-read each `records/{type}/{year}/{id}.json` and compared `source_hash` to the value captured at sample time — 8/8 matched).
- No `records/` mutation. No `corpus.sqlite` mutation. No `judges_registry.yaml` mutation. No `approvals.yaml` mutation.
- `MAX_BATCH_SIZE = 8` honoured (exactly 8 fetches consumed).
- Rate limit: 5s per zambialii.org request and 2s default for parliament.gov.zm honoured throughout.
- User-Agent: `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)` on every request.

## Execution mode

Inline runner (b0548 / b0549 / b0551 / b0554 / b0555 / b0556 / b0560 / b0561 / b0562 precedent). No `scripts/batch_0563_phase8_reverify.py` committed, due to sandbox-session safety constraint (the persistent stale `.git/objects/maintenance.lock` virtiofs unlink-not-permitted issue). Functionality matches the frozen baseline `scripts/batch_0546_phase8_reverify.py` including PKI cert loader, host-aware rate limiting, and tick-suffixed seed.

## Next-tick recommendations

1. Continue Phase 8 nightly reverify cadence (no change to seed scheme).
2. Standing operator action: decide on Phase 8 evolution to content-equivalent hashing or stable-PDF-only sampling, given 15-tick consistent pattern (51 stable-PDF match / 49 act-or-SI-akn-HTML drift, 1m/4d judgment-akn-HTML, 0m/1d parliament-node).
3. judgment-ingestion-worker continues independently (last tick b0561 — 2 written, 6 deferred; ZMCC 2019 finish + ZMCC 2018 HEAD probe recommended).
4. Standing parser_v0.3.3 anchor pack request unchanged (68 records pending in v0.3.3-pending cohort).
5. Standing OCR pipeline request unchanged (5 records pending).
6. Standing operator action on Phase 5 ceiling 166 / 160 (six above sentinel after b0561).

## B2 sync

Deferred to host (rclone not in sandbox).
