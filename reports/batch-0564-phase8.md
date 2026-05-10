# Batch 0564 — Phase 8 Nightly Re-verification (worker-tick variant)

> **Co-existence note:** batch number 0564 is shared this tick by two
> independent workers running in parallel — `worker-tick` (this report —
> Phase 8 nightly reverify) and `judgment-ingestion-worker`
> (`reports/batch-0564.md`, ZMCC 2019 finish, +3 records). Both
> coexist per the established b0560 collision-coexistent precedent.

**Date:** 2026-05-10
**Worker:** worker-tick (scheduled 30-min cadence)
**Phase:** phase_8_nightly_reverify
**Parser version:** phase8-reverify-0.1.0
**Tick number:** second worker-tick of UTC date 2026-05-10; sixteenth Phase 8 tick overall.

## Summary

| Metric | Value |
|---|---|
| Pool size (at sample time) | 1860 |
| Sample size | 8 (cap = MAX_BATCH_SIZE) |
| Sample seed | `phase8-reverify-2026-05-10-b0564` |
| Match | 3 |
| Drift | 5 |
| Fetch error | 0 |
| Truncated-stored-hash false drift | 0 |
| Fetches | 8 / 2000 (cumulative_today 8 → 16; main worker budget) |
| Records mutated by Phase 8 | 0 |
| approvals.yaml mutated | no |
| Integrity check | 8 / 8 PASS (stored source_hash unchanged on disk pre/post tick for the 8 sampled ids) |
| Started at (UTC) | 2026-05-10T06:02:06Z |
| Completed at (UTC) | 2026-05-10T06:02:42Z |

## Pool size note

Pool size at sample time was 1860 (records/ JSON files with both `source_url` and `source_hash`). The parallel `judgment-ingestion-worker` b0564 tick added 3 new ZMCC 2019 judgment records (nums 16, 21, 22) to corpus.sqlite at ~06:03:30Z, after the Phase 8 sample was drawn at 06:02:06Z and the verdicts were fixed at 06:02:42Z. The 3 new records became part of records/ during the Phase 8 tick window but were not in the sample pool — the post-tick records/ count is therefore 1863, while the pool sampled by Phase 8 was 1860. Phase 8 verdicts and integrity checks are unaffected by the parallel worker's writes (Phase 8 only verifies the 8 sampled ids' source_hash unchanged pre/post the fetch window — confirmed 8/8 PASS).

## Verdicts

### Match (3) — all stable byte-for-byte endpoints

1. `act-zm-2013-014-the-property-transfer-tax-amendment-2013` — `https://www.parliament.gov.zm/sites/default/files/documents/amendment_act/Property%20Transfer%20%28Amendment%29%20Act%202013.PDF` (parliament.gov.zm `amendment_act/` static PDF)
2. `local-government-appointment-of-local-government-administrator-kafue-town-counci-2022` — `https://zambialii.org/akn/zm/act/si/2022/71/eng@2022-11-04/source.pdf` (zambialii `/source.pdf` endpoint)
3. `act-zm-2018-009-the-public-private-partnership-amendment-act-2018` — `https://www.parliament.gov.zm/sites/default/files/documents/acts/The%20Public-Private%20Partnership%20Act.pdf` (parliament.gov.zm `/acts/` static PDF)

### Drift (5) — 4 act-or-SI-akn-HTML cohort + 1 judgment-akn-HTML cohort

1. `judgment-zm-2025-zmcc-22-sean-tembo-suing-in-his-capacity-as-spokesperson-o` — `https://zambialii.org/akn/zm/judgment/zmcc/2025/22/eng@2025-11-27` (zambialii judgment-akn-HTML; **fifth** judgment-akn drift observation)
2. `act-zm-2007-008-supplementary-appropriation-2005-act` — `https://zambialii.org/akn/zm/act/2007/8/eng@2007-04-13` (zambialii act-akn-HTML)
3. `si-zm-2019-069-palabana-university-declaration-order-2019` — `https://zambialii.org/akn/zm/act/si/2019/69` (zambialii SI-akn-HTML; **bare path** without `/eng@` suffix — see notable observation below)
4. `si-zm-2019-031-defence-regular-forces-officers-amendment-regulations-2019` — `https://zambialii.org/akn/zm/act/si/2019/31` (zambialii SI-akn-HTML; bare path without `/eng@` suffix)
5. `act-zm-1967-014-plant-variety-and-seeds-act-1967` — `https://zambialii.org/akn/zm/act/1967/14/eng@1996-12-31` (zambialii act-akn-HTML)

### Fetch error (0)

None.

## Cumulative Phase 8 tally (across 16 ticks; 14 on 2026-05-09 + 2 on 2026-05-10)

| Cohort | Match | Drift | Fetch err |
|---|---|---|---|
| zambialii.org `/akn/zm/act/.../HTML` (act + SI, with `/eng@` suffix or bare) | 0 | 53 | 0 |
| zambialii.org `/akn/zm/act/.../source.pdf` + parliament.gov.zm static PDFs | 54 | 0 | 0 |
| zambialii.org `/akn/zm/judgment/.../HTML` | 1 | 5 | 0 |
| parliament.gov.zm `/node/...` landing | 0 | 1 | 0 |

(Roll-up adjusted from b0563 cumulative 51 PDF match / 49 act-or-SI-akn-HTML drift / 1m-4d judgment-akn / 0m-1d parliament-node by adding 3 PDF match, 4 act-or-SI-akn-HTML drift, and 1 judgment-akn-HTML drift this tick.)

## Notable observation this tick

Two of the five drift records (`si-zm-2019-069` and `si-zm-2019-031`) carry the **bare** AKN path `https://zambialii.org/akn/zm/act/si/2019/{NN}` with no `/eng@<date>` language-and-version suffix, in contrast to the dominant `/akn/zm/act/2007/8/eng@2007-04-13` form seen on `act-zm-2007-008` and `act-zm-1967-014` this same tick. Both bare-path SIs drift identically to the suffixed form, confirming the rendering-layer drift hypothesis is not language-and-version-suffix-dependent — the same Cantemo / akoma-ntoso renderer is reached via both URL shapes and produces equally time-varying byte content. This complements the `www.zambialii.org` host-prefix-insensitivity finding from b0563.

Judgment-akn-HTML now has **5 cumulative drift observations** (of 6 sampled — 1m/5d, ~83% drift rate, n=6) per b0554 revised hypothesis. Trend continues to support full inclusion of judgment-akn-HTML URLs in the same drift cohort as act-and-SI-akn-HTML URLs.

## Working hypothesis (unchanged)

Stable PDF endpoints (zambialii `source.pdf` and parliament.gov.zm static PDFs) preserve byte-for-byte stability. Dynamically-rendered HTML endpoints (zambialii AKN-HTML for act/SI/judgment, parliament.gov.zm `/node/*` landings) carry slow-time-varying byte content — likely a server-rendered timestamp, freshness pin, or rotating ETag-derived footer. Recommendation for operator (carries forward from b0549, b0554, b0555, b0561, b0562, b0563): consider Phase 8 evolving to either (a) content-equivalent (text-extraction-stable) hashing, or (b) restricting Phase 8 to stable-PDF endpoints only. No action taken this tick.

## Integrity (Phase 8 scope only)

- `pool_size` at sample time: 1860 records on disk with both `source_url` and `source_hash`.
- All 8 sampled record ids present on disk; stored `source_hash` unchanged across the tick (post-fetch verification re-read each `records/{type}/{year}/{id}.json` and compared `source_hash` to the value captured at sample time — 8/8 matched).
- No `records/` mutation by Phase 8. No `corpus.sqlite` mutation by Phase 8. No `judges_registry.yaml` mutation by Phase 8. No `approvals.yaml` mutation.
- `MAX_BATCH_SIZE = 8` honoured (exactly 8 fetches consumed by Phase 8).
- Rate limit: 5s per zambialii.org request and 2s default for parliament.gov.zm honoured throughout.
- User-Agent: `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)` on every request.

## Execution mode

Inline runner (b0548 / b0549 / b0551 / b0554 / b0555 / b0556 / b0560 / b0561 / b0562 / b0563 precedent). No `scripts/batch_0564_phase8_reverify.py` committed, due to sandbox-session safety constraint (the persistent stale `.git/objects/maintenance.lock` virtiofs unlink-not-permitted issue). Functionality matches the frozen baseline `scripts/batch_0546_phase8_reverify.py` including PKI cert loader, host-aware rate limiting, and tick-suffixed seed.

## Next-tick recommendations

1. Continue Phase 8 nightly reverify cadence (no change to seed scheme).
2. Standing operator action: decide on Phase 8 evolution to content-equivalent hashing or stable-PDF-only sampling, given 16-tick consistent pattern (54 stable-PDF match / 53 act-or-SI-akn-HTML drift, 1m/5d judgment-akn-HTML, 0m/1d parliament-node).
3. judgment-ingestion-worker continues independently (last tick b0564 — 3 ZMCC 2019 written, 5 deferred; ZMCC 2019 final 2 + ZMCC 2018 HEAD probe recommended next).
4. Standing parser_v0.3.3 anchor pack request unchanged (73 records pending in v0.3.3-pending cohort after b0564 +5).
5. Standing OCR pipeline request unchanged (5 records pending).
6. Standing operator action on Phase 5 ceiling 169/160 (nine above sentinel after b0564 +3).

## B2 sync

Deferred to host (rclone not in sandbox).
