# Batch 0565 — Phase 8 Nightly Re-verification

**Date:** 2026-05-10
**Worker:** worker-tick (scheduled 30-min cadence)
**Phase:** phase_8_nightly_reverify
**Parser version:** phase8-reverify-0.1.0
**Tick number:** third worker-tick of UTC date 2026-05-10; seventeenth Phase 8 tick overall.

## Summary

| Metric | Value |
|---|---|
| Pool size (at sample time) | 1863 |
| Sample size | 8 (cap = MAX_BATCH_SIZE) |
| Sample seed | `phase8-reverify-2026-05-10-b0565` |
| Match | 6 |
| Drift | 2 |
| Fetch error | 0 |
| Truncated-stored-hash false drift | 0 |
| Fetches | 8 / 2000 (cumulative_today 16 → 24; main worker budget) |
| Records mutated by Phase 8 | 0 |
| approvals.yaml mutated | no |
| Integrity check | 8 / 8 PASS (stored source_hash unchanged on disk pre/post tick for the 8 sampled ids) |
| Started at (UTC) | 2026-05-10T09:09:19Z |
| Completed at (UTC) | 2026-05-10T09:09:35Z |

## Pool size note

Pool size at sample time was 1863 (records/ JSON files with both `source_url` and `source_hash`). This is +3 from b0564's pool of 1860 — the parallel b0564 `judgment-ingestion-worker` tick added 3 new ZMCC 2019 records (nums 16, 21, 22) which are now in the sample pool for b0565. corpus.sqlite records and records_fts both stand at 1859 (the 4 records appearing in records/ but not in corpus.sqlite are pre-existing and unrelated to this tick — see standing reconciliation note in worker.log).

## Verdicts

### Match (6) — all stable byte-for-byte endpoints

1. `act-zm-2013-016-the-customs-and-excise-amendment-2013` — `https://www.parliament.gov.zm/sites/default/files/documents/amendment_act/Customs%20and%20Excise%20%28Amendment%29%20Act%202013.PDF` (parliament.gov.zm `amendment_act/` static PDF)
2. `act-zm-cap-249-tsetse-control-act` — `https://www.parliament.gov.zm/sites/default/files/documents/acts/Tsetse%20Control%20Act.pdf` (parliament.gov.zm `/acts/` static PDF)
3. `loz-dairies-and-dairy-produce-act` — `https://www.parliament.gov.zm/sites/default/files/documents/acts/Dairies%20and%20Dairy%20Produce%20Act.pdf` (parliament.gov.zm `/acts/` static PDF; Laws of Zambia consolidated)
4. `act-zm-2015-021-insurance-premium-levy-act` — `https://www.parliament.gov.zm/sites/default/files/documents/acts/The%20Insurance%20Premium%20Levy%20Act%20No.%2021%20of%202015.pdf` (parliament.gov.zm `/acts/` static PDF)
5. `si-zm-2025-009-bank-of-zambia-withdrawal-and-exchange-of-currency-regulations-2025` — `https://media.zambialii.org/media/legislation/44173/source_file/1fe34b6ef23bc96a/bank-of-zambia-withdrawal-and-exchange-of-currency-regulations-2025.pdf` (media.zambialii.org `/source_file/` PDF — first such cohort observation this Phase 8 series)
6. `act-zm-2017-010-companies` — `https://www.parliament.gov.zm/sites/default/files/documents/acts/Companies%20Act%2C%202017.pdf` (parliament.gov.zm `/acts/` static PDF; Phase 2 pilot statute)

### Drift (2) — 1 act-akn-HTML + 1 judgment-akn-HTML

1. `judgment-zm-2022-zmsc-45-abel-chipemba-v-the-people` — `https://zambialii.org/akn/zm/judgment/zmsc/2022/45/eng@2022-02-10` (zambialii judgment-akn-HTML; **sixth** judgment-akn drift observation)
2. `act-zm-1970-040-refugees-control-act-1970` — `https://zambialii.org/akn/zm/act/1970/40/eng@1996-12-31` (zambialii act-akn-HTML)

### Fetch error (0)

None.

## Cumulative Phase 8 tally (across 17 ticks; 14 on 2026-05-09 + 3 on 2026-05-10)

| Cohort | Match | Drift | Fetch err |
|---|---|---|---|
| zambialii.org `/akn/zm/act/.../HTML` (act + SI, with `/eng@` suffix or bare) | 0 | 54 | 0 |
| zambialii.org `/akn/zm/act/.../source.pdf` + parliament.gov.zm static PDFs + media.zambialii.org `/source_file/` PDFs | 60 | 0 | 0 |
| zambialii.org `/akn/zm/judgment/.../HTML` | 1 | 6 | 0 |
| parliament.gov.zm `/node/...` landing | 0 | 1 | 0 |

(Roll-up adjusted from b0564 cumulative 54 PDF match / 53 act-or-SI-akn-HTML drift / 1m-5d judgment-akn / 0m-1d parliament-node by adding 6 PDF match, 1 act-or-SI-akn-HTML drift, and 1 judgment-akn-HTML drift this tick.)

## Notable observation this tick

**First match observation on the `media.zambialii.org/source_file/` cohort** — `si-zm-2025-009` was served from `media.zambialii.org/media/legislation/44173/source_file/1fe34b6ef23bc96a/...pdf` (a PDF-asset URL with a content-hash path component) and matched byte-for-byte. This is structurally similar to zambialii `source.pdf` — a static-asset endpoint not subject to the AKN renderer drift — and is rolled into the stable-PDF cohort accordingly. The 17-tick pattern continues to support the working hypothesis: rendered HTML drifts; static PDF assets do not.

The judgment-akn-HTML cohort is now at 1m/6d (~86% drift rate, n=7), strengthening prior recommendation to fold judgment-akn-HTML into the same drift cohort as act-and-SI-akn-HTML.

This tick's sample contained an unusually high proportion of stable-PDF endpoints (6 of 8) by chance under the deterministic seed `phase8-reverify-2026-05-10-b0565`; over 17 ticks the cumulative cohort split (60 stable / 54 act-SI-akn / 6 judgment-akn / 1 parliament-node) remains representative.

## Working hypothesis (unchanged)

Stable PDF endpoints (zambialii `source.pdf`, media.zambialii.org `/source_file/`, and parliament.gov.zm static PDFs) preserve byte-for-byte stability. Dynamically-rendered HTML endpoints (zambialii AKN-HTML for act/SI/judgment, parliament.gov.zm `/node/*` landings) carry slow-time-varying byte content — likely a server-rendered timestamp, freshness pin, or rotating ETag-derived footer. Recommendation for operator (carries forward from b0549, b0554, b0555, b0561, b0562, b0563, b0564): consider Phase 8 evolving to either (a) content-equivalent (text-extraction-stable) hashing, or (b) restricting Phase 8 to stable-PDF endpoints only. No action taken this tick.

## Integrity (Phase 8 scope only)

- `pool_size` at sample time: 1863 records on disk with both `source_url` and `source_hash`.
- All 8 sampled record ids present on disk; stored `source_hash` unchanged across the tick (post-fetch verification re-read each `records/{type}/{year}/{id}.json` and compared `source_hash` to the value captured at sample time — 8/8 matched).
- No `records/` mutation by Phase 8. No `corpus.sqlite` mutation by Phase 8. No `judges_registry.yaml` mutation by Phase 8. No `approvals.yaml` mutation.
- `MAX_BATCH_SIZE = 8` honoured (exactly 8 fetches consumed by Phase 8).
- Rate limit: 5s per zambialii.org / media.zambialii.org request and 2s default for parliament.gov.zm honoured throughout.
- User-Agent: `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)` on every request.

## Execution mode

Inline runner (b0548 / b0549 / b0551 / b0554 / b0555 / b0556 / b0560 / b0561 / b0562 / b0563 / b0564 precedent). No `scripts/batch_0565_phase8_reverify.py` committed, due to sandbox-session safety constraint (the persistent stale `.git/objects/maintenance.lock` virtiofs unlink-not-permitted issue). Functionality matches the frozen baseline `scripts/batch_0546_phase8_reverify.py` including PKI cert loader, host-aware rate limiting, and tick-suffixed seed.

## Next-tick recommendations

1. Continue Phase 8 nightly reverify cadence (no change to seed scheme).
2. Standing operator action: decide on Phase 8 evolution to content-equivalent hashing or stable-PDF-only sampling, given 17-tick consistent pattern (60 stable-PDF match / 54 act-or-SI-akn-HTML drift, 1m/6d judgment-akn-HTML, 0m/1d parliament-node).
3. judgment-ingestion-worker continues independently (last tick b0564 — 3 ZMCC 2019 written, 5 deferred; ZMCC 2019 final 2 + ZMCC 2018 HEAD probe recommended next).
4. Standing parser_v0.3.3 anchor pack request unchanged (73 records pending in v0.3.3-pending cohort).
5. Standing OCR pipeline request unchanged (5 records pending).
6. Standing operator action on Phase 5 ceiling 169/160 (nine above sentinel after b0564 +3).

## B2 sync

Deferred to host (rclone not in sandbox).
