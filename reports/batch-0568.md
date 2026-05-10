# Batch 0568 — Phase 8 Nightly Re-verification

**Date:** 2026-05-10
**Worker:** worker-tick (scheduled 30-min cadence)
**Phase:** phase_8_nightly_reverify
**Parser version:** phase8-reverify-0.1.0
**Tick number:** fifth worker-tick of UTC date 2026-05-10; nineteenth Phase 8 tick overall.

## Summary

| Metric | Value |
|---|---|
| Pool size (at sample time) | 1865 |
| Sample size | 8 (cap = MAX_BATCH_SIZE) |
| Sample seed | `phase8-reverify-2026-05-10-b0568` |
| Match | 3 |
| Drift | 5 |
| Fetch error | 0 |
| Truncated-stored-hash false drift | 0 |
| Fetches | 8 / 2000 (cumulative_today 32 → 40; main worker budget) |
| Records mutated by Phase 8 | 0 |
| approvals.yaml mutated | no |
| Integrity check | 8 / 8 PASS (stored source_hash unchanged on disk pre/post tick for the 8 sampled ids) |
| Started at (UTC) | 2026-05-10T10:09:54Z |
| Completed at (UTC) | 2026-05-10T10:10:20Z |

## Pool size note

Pool size at sample time was 1865 (records/ JSON files with both `source_url` and `source_hash`) — unchanged from b0567. No judgment-ingestion-worker tick has run between b0567 and b0568.

## Verdicts

### Match (3) — all parliament.gov.zm static PDFs

1. `act-zm-2009-018-zambia-law-development-commission-amendment-act-2009` — `https://www.parliament.gov.zm/sites/default/files/documents/amendment_act/Zambia%20Law%20Development%20Commission%20%28Amendment%29%20Act%2C%202009.PDF` (parliament.gov.zm `amendment_act/` static PDF; 393,069 bytes)
2. `act-zm-2013-015-the-value-added-tax-amendment-2013` — `https://www.parliament.gov.zm/sites/default/files/documents/amendment_act/Value%20Added%20Tax%20%28Amendment%29%20Act%202013.PDF` (parliament.gov.zm `amendment_act/` static PDF; 44,607 bytes)
3. `act-zm-2020-007-the-banking-and-financial-services-amendment-act-2020` — `https://www.parliament.gov.zm/sites/default/files/documents/acts/The%20Banking%20and%20Financial%20Services%20Amend%20Act%20No.%207%20of%202020.%20pmd.pdf` (parliament.gov.zm `acts/` static PDF; 24,779 bytes)

### Drift (5) — 4 act-akn-HTML + 1 SI-akn-HTML

1. `act-zm-cap-269-industrial-and-labour-relations-act` — `https://zambialii.org/akn/zm/act/1993/27/eng@1996-12-31` (zambialii act-akn-HTML; **first "cap-" prefixed identifier** sampled in any Phase 8 tick — confirms drift cohort coverage extends to consolidated-Cap records as well as year-numbered acts; 499,225 bytes new)
2. `act-zm-1992-026-university-act-1992` — `https://zambialii.org/akn/zm/act/1992/26/eng@1996-12-31` (zambialii act-akn-HTML; 273,399 bytes new)
3. `act-zm-1920-002-public-pounds-and-trespass-act` — `https://zambialii.org/akn/zm/act/1920/2/eng@1996-12-31` (zambialii act-akn-HTML; **NEW EARLIEST-year record sampled to date** — 1920, beats prior earliest of 1930 from b0567; 251,298 bytes new)
4. `act-zm-1973-020-medical-examination-of-young-persons--underground-work--act--1973` — `https://www.zambialii.org/akn/zm/act/1973/20/eng@1996-12-31` (zambialii act-akn-HTML; uses `www.zambialii.org` host prefix — re-confirms b0563 host-prefix-insensitive finding; 84,630 bytes new)
5. `si-zm-2018-056-national-assembly-by-election-kasenengwa-constituency-no-41-election-date-and-time-of-poll-no-2-order-2018` — `https://zambialii.org/akn/zm/act/si/2018/56` (zambialii SI-akn-HTML; bare path no `/eng@` suffix; 39,262 bytes new)

### Fetch error (0)

None.

## Cumulative Phase 8 tally (across 19 ticks; 14 on 2026-05-09 + 5 on 2026-05-10)

| Cohort | Match | Drift | Fetch err |
|---|---|---|---|
| zambialii.org `/akn/zm/act/.../HTML` (act + SI, with `/eng@` suffix or bare) | 0 | 64 | 0 |
| zambialii.org `/akn/zm/act/.../source.pdf` + parliament.gov.zm static PDFs + media.zambialii.org `/source_file/` PDFs | 65 | 0 | 0 |
| zambialii.org `/akn/zm/judgment/.../HTML` | 1 | 7 | 0 |
| parliament.gov.zm `/node/...` landing | 0 | 1 | 0 |

(Roll-up adjusted from b0567 cumulative 62 PDF match / 59 act-or-SI-akn-HTML drift / 1m-7d judgment-akn / 0m-1d parliament-node by adding 3 PDF match and 5 act-or-SI-akn-HTML drift this tick. Judgment-akn unchanged this tick — no judgment sampled.)

## Notable observations this tick

**(1) New earliest-year record:** `act-zm-1920-002-public-pounds-and-trespass-act` (1920) is the earliest-year record sampled in any Phase 8 tick to date, beating prior earliest of 1930 (b0567 `act-zm-1930-028-petroleum-act-1930`). Drift in act-akn-HTML rendering is therefore confirmed across the full chronological span back to 1920 — colonial-era statutes render with the same drift signature as modern acts.

**(2) First "cap-" prefixed identifier:** `act-zm-cap-269-industrial-and-labour-relations-act` is the first sampled record using the consolidated-Cap identifier convention rather than the year-number convention. Drift cohort coverage is confirmed to extend across both identifier conventions — drift signature is independent of corpus-side identifier scheme.

**(3) Host-prefix re-confirmation:** `act-zm-1973-020-medical-examination-of-young-persons--underground-work--act--1973` uses `www.zambialii.org` as host, and drifts byte-for-byte — re-confirming b0563's host-prefix-insensitive drift finding (rendering layer treats `zambialii.org` and `www.zambialii.org` identically for hash-drift purposes).

**(4) Cohort split holds:** 5/5 zambialii AKN-HTML drifts and 3/3 parliament.gov.zm static PDF matches under deterministic seed — the 19-tick cumulative tally (64/64 act-or-SI-akn-HTML drifts; 65/65 stable-PDF matches) shows zero exceptions in either direction.

## Working hypothesis (unchanged)

Stable PDF endpoints (zambialii `source.pdf`, media.zambialii.org `/source_file/`, and parliament.gov.zm static PDFs) preserve byte-for-byte stability. Dynamically-rendered HTML endpoints (zambialii AKN-HTML for act/SI/judgment, parliament.gov.zm `/node/*` landings) carry slow-time-varying byte content — likely a server-rendered timestamp, freshness pin, or rotating ETag-derived footer. Recommendation for operator (carries forward from b0549, b0554, b0555, b0561, b0562, b0563, b0564, b0565, b0567): consider Phase 8 evolving to either (a) content-equivalent (text-extraction-stable) hashing, or (b) restricting Phase 8 to stable-PDF endpoints only. No action taken this tick.

## Integrity (Phase 8 scope only)

- `pool_size` at sample time: 1865 records on disk with both `source_url` and `source_hash`.
- All 8 sampled record ids present on disk; stored `source_hash` unchanged across the tick (post-fetch verification re-read each `records/{type}/{year}/{id}.json` and compared `source_hash` to the value captured at sample time — 8/8 matched).
- No `records/` mutation by Phase 8. No `corpus.sqlite` mutation by Phase 8. No `judges_registry.yaml` mutation by Phase 8. No `approvals.yaml` mutation.
- `MAX_BATCH_SIZE = 8` honoured (exactly 8 fetches consumed by Phase 8).
- Rate limit: 5s per zambialii.org request and 2s default for parliament.gov.zm honoured throughout.
- User-Agent: `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)` on every request.

## Execution mode

Inline runner (b0548..b0567 precedent). No `scripts/batch_0568_phase8_reverify.py` committed, due to sandbox-session safety constraint (the persistent stale `.git/objects/maintenance.lock` virtiofs unlink-not-permitted issue). Functionality matches the frozen baseline `scripts/batch_0546_phase8_reverify.py` including PKI cert loader, host-aware rate limiting, and tick-suffixed seed.

## Next-tick recommendations

1. Continue Phase 8 nightly reverify cadence (no change to seed scheme).
2. Standing operator action: decide on Phase 8 evolution to content-equivalent hashing or stable-PDF-only sampling, given 19-tick consistent pattern (65 stable-PDF match / 64 act-or-SI-akn-HTML drift, 1m/7d judgment-akn-HTML, 0m/1d parliament-node).
3. judgment-ingestion-worker continues independently (last tick b0566 — 1 ZMCC 2018 written, 7 deferred to OCR-pending cohort which now stands at 12; ZMCC 2018 upper-boundary HEAD-probe + GET-fetch of remaining nums recommended next).
4. Standing parser_v0.3.3 anchor pack request unchanged (74 records pending in v0.3.3-pending cohort).
5. Standing OCR pipeline request unchanged (12 records pending — ZMCC 2020 ×5 + ZMCC 2018 ×7).
6. Standing operator action on Phase 5 ceiling 171/160 (+11 above sentinel).

## B2 sync

Deferred to host (rclone not in sandbox).
