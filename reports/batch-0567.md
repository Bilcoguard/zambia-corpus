# Batch 0567 — Phase 8 Nightly Re-verification

**Date:** 2026-05-10
**Worker:** worker-tick (scheduled 30-min cadence)
**Phase:** phase_8_nightly_reverify
**Parser version:** phase8-reverify-0.1.0
**Tick number:** fourth worker-tick of UTC date 2026-05-10; eighteenth Phase 8 tick overall.

## Summary

| Metric | Value |
|---|---|
| Pool size (at sample time) | 1865 |
| Sample size | 8 (cap = MAX_BATCH_SIZE) |
| Sample seed | `phase8-reverify-2026-05-10-b0567` |
| Match | 2 |
| Drift | 6 |
| Fetch error | 0 |
| Truncated-stored-hash false drift | 0 |
| Fetches | 8 / 2000 (cumulative_today 24 → 32; main worker budget) |
| Records mutated by Phase 8 | 0 |
| approvals.yaml mutated | no |
| Integrity check | 8 / 8 PASS (stored source_hash unchanged on disk pre/post tick for the 8 sampled ids) |
| Started at (UTC) | 2026-05-10T10:01:27Z |
| Completed at (UTC) | 2026-05-10T10:02:03Z |

## Pool size note

Pool size at sample time was 1865 (records/ JSON files with both `source_url` and `source_hash`). This is +2 from b0565's pool of 1863 — the parallel b0566 `judgment-ingestion-worker` tick added 1 new ZMCC 2018 record (num 1 — Chilombo v Hamaleke) plus the b0565 `judgment-ingestion-worker` ZMCC 2019/24 ingestion now visible to this tick's loader (b0565 reverify tick ran before b0565 jiw landed). corpus.sqlite records and records_fts both stand at 1861 after b0566 jiw.

## Verdicts

### Match (2) — both stable byte-for-byte parliament.gov.zm static PDFs

1. `act-zm-2024-016-the-judiciary-administration-amendment-act-2024` — `https://www.parliament.gov.zm/sites/default/files/documents/acts/Act%20No.%2016%20of%202024%2C%20The%20Judiciary%20Administration.pdf` (parliament.gov.zm `/acts/` static PDF; 276,803 bytes)
2. `act-zm-2010-050-property-transfer-tax-amendment` — `https://www.parliament.gov.zm/sites/default/files/documents/amendment_act/Property%20Transfer%20Tax%20%28Amendment%29%202010A_0.PDF` (parliament.gov.zm `amendment_act/` static PDF; 41,311 bytes)

### Drift (6) — 3 act-akn-HTML + 2 SI-akn-HTML + 1 judgment-akn-HTML

1. `act-zm-1930-028-petroleum-act-1930` — `https://zambialii.org/akn/zm/act/1930/28/eng@1996-12-31` (zambialii act-akn-HTML; 51,258 bytes new)
2. `judgment-zm-2023-zmcc-02-mwanza-v-attorney-general` — `https://zambialii.org/akn/zm/judgment/zmcc/2023/2/eng@2023-03-02` (zambialii judgment-akn-HTML; **seventh** judgment-akn drift observation; 45,379 bytes new)
3. `act-zm-1988-015-supplementary-appropriation-1986-act-1988` — `https://zambialii.org/akn/zm/act/1988/15/eng@1988-04-22` (zambialii act-akn-HTML; 38,783 bytes new)
4. `act-zm-1976-034-valuation-surveyors-act-1976` — `https://zambialii.org/akn/zm/act/1976/34` (zambialii act-akn-HTML; bare path no `/eng@` suffix; 71,365 bytes new)
5. `si-zm-2018-007-railways-transportation-of-heavy-goods-regulations-2018` — `https://zambialii.org/akn/zm/act/si/2018/7` (zambialii SI-akn-HTML; bare path no `/eng@` suffix; 39,189 bytes new)
6. `si-zm-2021-055-metrology-measuring-instruments-regulations-2021` — `https://zambialii.org/akn/zm/act/si/2021/55` (zambialii SI-akn-HTML; bare path no `/eng@` suffix; 38,996 bytes new)

### Fetch error (0)

None.

## Cumulative Phase 8 tally (across 18 ticks; 14 on 2026-05-09 + 4 on 2026-05-10)

| Cohort | Match | Drift | Fetch err |
|---|---|---|---|
| zambialii.org `/akn/zm/act/.../HTML` (act + SI, with `/eng@` suffix or bare) | 0 | 59 | 0 |
| zambialii.org `/akn/zm/act/.../source.pdf` + parliament.gov.zm static PDFs + media.zambialii.org `/source_file/` PDFs | 62 | 0 | 0 |
| zambialii.org `/akn/zm/judgment/.../HTML` | 1 | 7 | 0 |
| parliament.gov.zm `/node/...` landing | 0 | 1 | 0 |

(Roll-up adjusted from b0565 cumulative 60 PDF match / 54 act-or-SI-akn-HTML drift / 1m-6d judgment-akn / 0m-1d parliament-node by adding 2 PDF match, 5 act-or-SI-akn-HTML drift, and 1 judgment-akn-HTML drift this tick.)

## Notable observation this tick

**Highest drift proportion in 18-tick series: 6/8 = 75% drift this tick.** The sample contained 6 zambialii AKN-HTML URLs (3 act with `/eng@` suffix, 1 act bare-path, 2 SI bare-path, 1 judgment with `/eng@` suffix) and only 2 stable parliament.gov.zm static PDFs under the deterministic seed `phase8-reverify-2026-05-10-b0567`. All 6 AKN-HTML URLs drifted byte-for-byte; both parliament PDFs matched. This is the strongest single-tick signal yet for the established cohort split: rendered HTML drifts; static PDF assets do not.

The judgment-akn-HTML cohort is now at 1m/7d (~88% drift rate, n=8), strengthening prior recommendation to fold judgment-akn-HTML into the same drift cohort as act-and-SI-akn-HTML.

`act-zm-1930-028-petroleum-act-1930` is the **earliest-year** record encountered in any Phase 8 tick to date (1930 is older than the prior earliest, 1929 dairies via b0533). Drift in act-akn-HTML rendering is therefore confirmed across the full chronological span of the Acts cohort.

`act-zm-1976-034-valuation-surveyors-act-1976`, `si-zm-2018-007-railways-transportation-of-heavy-goods-regulations-2018`, and `si-zm-2021-055-metrology-measuring-instruments-regulations-2021` all use bare AKN paths (no `/eng@` suffix) — drift reproduces uniformly with the date-pinned URLs, consistent with b0563/b0564 findings that the rendering-layer drift is path-suffix-insensitive.

## Working hypothesis (unchanged)

Stable PDF endpoints (zambialii `source.pdf`, media.zambialii.org `/source_file/`, and parliament.gov.zm static PDFs) preserve byte-for-byte stability. Dynamically-rendered HTML endpoints (zambialii AKN-HTML for act/SI/judgment, parliament.gov.zm `/node/*` landings) carry slow-time-varying byte content — likely a server-rendered timestamp, freshness pin, or rotating ETag-derived footer. Recommendation for operator (carries forward from b0549, b0554, b0555, b0561, b0562, b0563, b0564, b0565): consider Phase 8 evolving to either (a) content-equivalent (text-extraction-stable) hashing, or (b) restricting Phase 8 to stable-PDF endpoints only. No action taken this tick.

## Integrity (Phase 8 scope only)

- `pool_size` at sample time: 1865 records on disk with both `source_url` and `source_hash`.
- All 8 sampled record ids present on disk; stored `source_hash` unchanged across the tick (post-fetch verification re-read each `records/{type}/{year}/{id}.json` and compared `source_hash` to the value captured at sample time — 8/8 matched).
- No `records/` mutation by Phase 8. No `corpus.sqlite` mutation by Phase 8. No `judges_registry.yaml` mutation by Phase 8. No `approvals.yaml` mutation.
- `MAX_BATCH_SIZE = 8` honoured (exactly 8 fetches consumed by Phase 8).
- Rate limit: 5s per zambialii.org request and 2s default for parliament.gov.zm honoured throughout.
- User-Agent: `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)` on every request.

## Execution mode

Inline runner (b0548 / b0549 / b0551 / b0554 / b0555 / b0556 / b0560 / b0561 / b0562 / b0563 / b0564 / b0565 precedent). No `scripts/batch_0567_phase8_reverify.py` committed, due to sandbox-session safety constraint (the persistent stale `.git/objects/maintenance.lock` virtiofs unlink-not-permitted issue). Functionality matches the frozen baseline `scripts/batch_0546_phase8_reverify.py` including PKI cert loader, host-aware rate limiting, and tick-suffixed seed.

## Next-tick recommendations

1. Continue Phase 8 nightly reverify cadence (no change to seed scheme).
2. Standing operator action: decide on Phase 8 evolution to content-equivalent hashing or stable-PDF-only sampling, given 18-tick consistent pattern (62 stable-PDF match / 59 act-or-SI-akn-HTML drift, 1m/7d judgment-akn-HTML, 0m/1d parliament-node).
3. judgment-ingestion-worker continues independently (last tick b0566 — 1 ZMCC 2018 written, 7 deferred to OCR-pending cohort which now stands at 12; ZMCC 2018 upper-boundary HEAD-probe + GET-fetch of remaining nums recommended next).
4. Standing parser_v0.3.3 anchor pack request unchanged (74 records pending in v0.3.3-pending cohort).
5. Standing OCR pipeline request unchanged (12 records pending — ZMCC 2020 ×5 + ZMCC 2018 ×7).
6. Standing operator action on Phase 5 ceiling 171/160 (+11 above sentinel after b0566 +1).

## B2 sync

Deferred to host (rclone not in sandbox).
