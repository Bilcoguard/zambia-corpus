# Batch 0569 — Phase 8 Nightly Re-verification (2026-05-10)

**UTC start:** 2026-05-10T10:30Z (approx)
**Worker:** worker-tick (Phase 8)
**Phase:** phase_8_nightly_reverify (approved 2026-05-06; sample_rate 0.01)
**Parser:** phase8-reverify-0.1.0 (functional contract per scripts/batch_0546_phase8_reverify.py)
**Tick scope:** Twentieth Phase 8 tick overall; sixth worker-tick of UTC date 2026-05-10
   (after b0563 at 05:50Z, b0564 at 06:02:42Z, b0565 at 09:09:35Z, b0567 at 10:06:09Z,
   b0568 at 10:12:41Z).
**Execution mode:** inline runner (`_inline_reverify_b0569.py`, NOT committed) per
   sandbox-session safety constraint maintained since b0548. Functional contract
   matches scripts/batch_0546_phase8_reverify.py baseline including
   scripts/certs/*.pem PKI loader.

## Inputs

- Pool size: **1865** (unchanged from b0568; no judgment-ingestion-worker tick
  between b0568 and b0569).
- Seed: `phase8-reverify-2026-05-10-b0569` (tick-suffixed deterministic seed
  per b0561+ precedent).
- Sample size: **8** (= MAX_BATCH cap; ceil(0.01 × 1865) = 19 → capped at 8).

## Results — 4 match / 4 drift / 0 fetch_error

| Verdict | Count | Records |
|---------|------:|---------|
| match   |     4 | act-zm-2018-015 (parliament.gov.zm 14,937 B); si-zm-2006-044-lands-ground-rent-fees-and-charges-regulations-2006 (zambialii.org/akn/.../source.pdf 876,676 B); si-zm-1997-050-property-transfer-tax-exemption-order-1997 (zambialii.org/akn/.../source.pdf 117,466 B); act-zm-2021-033-the-cannabis-act-2021 (parliament.gov.zm 82,204 B) |
| drift   |     4 | act-zm-2016-005-civil-aviation-act-2016 (zambialii.org/akn/.../act HTML 44,086 B); **act-zm-2020-014-mutual-legal-assistance-in-criminal-matters-amendment-act-20** (parliament.gov.zm static PDF 20,587 B — **FIRST-EVER parliament.gov.zm static PDF drift**); act-zm-1992-022-legal-services-corporation-dissolution-act-1992 (zambialii.org/akn/.../act HTML 39,455 B); act-zm-2015-009-supplementary-appropriation-2013-act (zambialii.org/akn/.../act HTML 39,562 B) |
| fetch_error | 0 | — |

## NEW FINDING (b0569) — PARLIAMENT.GOV.ZM STATIC PDF DRIFT BREAKS 65/65 STREAK

`act-zm-2020-014-mutual-legal-assistance-in-criminal-matters-amendment-act-20`
fetched from
`https://www.parliament.gov.zm/sites/default/files/documents/acts/Mutual%20Legal%20Assistance%20in%20Criminal%20Matters%20Amendment%2C%202020.pdf`
returned status 200 with **20,587 bytes** but the recomputed SHA-256 differs
from the stored `source_hash`. Across the prior 19 Phase 8 ticks
(b0524..b0568), every parliament.gov.zm static-PDF candidate sampled returned
a byte-perfect match (cumulative 65/65). This is the **first observed drift**
on that cohort and breaks the 100%-stable streak.

Possible explanations (NOT investigated this tick — single sample only):
1. Publisher re-issued the PDF (e.g. metadata refresh, watermark change,
   ToolChain re-render) since the original fetch.
2. CDN edge variation returning a slightly different byte-stream (header
   ordering, metadata, etc.) — though parliament.gov.zm has not previously
   shown CDN-edge instability.
3. Transient delivery anomaly (partial cache, MIME re-encoding).

**Recommended follow-up (next tick or operator):** re-fetch
act-zm-2020-014 once more under the same User-Agent to determine if the
new byte stream is now stable (publisher change) or itself drifts again
(cache instability). If publisher change, the canonical URL still returns
content but the corpus's stored hash references a superseded version —
worth flagging in gaps.md for human decision on whether to re-ingest the
new bytes (with a new hash) or preserve the original. Per non-negotiable
#2 (provenance is sacred) the tick does NOT mutate the record this batch.

## Cohort-level cumulative tally (post-b0569, 20 ticks)

| Cohort                                                  | Pre-b0569 | Δ b0569 | Post-b0569  |
|---------------------------------------------------------|----------:|--------:|------------:|
| zambialii.org/akn/.../act-or-SI-HTML drift              |     64/64 |   +3/+3 |   **67/67** |
| zambialii.org/akn/.../source.pdf match                  |     ~/~   |   +2/+2 | (in stable) |
| parliament.gov.zm static PDF match                      |     65/65 |   +2/+2 |       67/67 |
| parliament.gov.zm static PDF DRIFT                      |       0/65|   +1/+3 |  **1/68 ☆** |
| zambialii judgment-akn HTML drift                       |      1/8  |    0/0  |        1/8  |
| Parliament-node landing                                 |      0/1  |    0/0  |        0/1  |
| Stable-PDF combined (parliament + zambialii source.pdf) |     65/65 |   +4/+5 |    69/70 ★  |

★ first non-match in the previously-100%-stable PDF supercohort.
☆ first drift in the previously-100%-stable parliament.gov.zm static PDF cohort.

The AKN-HTML drift pattern continues at 100% (now 67/67 across 20 ticks);
the cohort split is intact for AKN-HTML. The PDF supercohort split is
now imperfect — one drift observation requires confirmation by a re-fetch
to determine whether it is an isolated event or a new pattern.

## Integrity check — 8/8 PASS

Post-fetch re-read of each record's `source_hash` from
`records/{type}/{year}/{id}.json` confirmed the stored hash is unchanged
on disk pre/post tick for all 8 sampled IDs. **No record file was
mutated by this tick.**

`approvals.yaml` is unmodified.
`judges_registry.yaml` is unmodified.
`corpus.sqlite` is unmodified (records=1861, records_fts=1861, judgments_meta=171).

## Daily budget (worker-tick channel)

After b0569: cumulative_today = **48 / 2000 fetches** (2.4% of daily ceiling
consumed across six Phase 8 worker-ticks on 2026-05-10).

Judgment-ingestion-worker channel cumulative_today (separate worker)
unchanged this tick at 74/500.

## Phase 8 status

Phase 8 is **open-ended** by design (1% sample rate of corpus per tick).
No `complete: true` flip is appropriate; per non-negotiable #4 the worker
NEVER flips approved/complete flags. `approvals.yaml` is NOT modified.

## Next-tick recommendations

1. **Confirm/refute parliament.gov.zm drift:** sample act-zm-2020-014
   ONCE more (out-of-band single fetch, not consuming the deterministic
   seeded sample) to determine whether the new bytes are stable or
   themselves drift. Document in next batch report.
2. Continue weekly Phase 8 deterministic sampling (no parameter change).
3. Standing recommendation from b0568 still holds: ZMCC 2018 final-1
   GET-fetch num 17 (judgment-ingestion-worker priority).
4. Standing parser_v0.3.3 anchor pack (80 records pending).
5. Standing OCR pipeline (14 records pending).

## Files written this tick

- `reports/batch-0569.md` (this file)
- `reports/batch-0569-reverify.json` (machine-readable summary, 8-record sample)
- `provenance.log` (+8 lines, one per sampled record)
- `costs.log` (+1 worker-tick line, +1 JSON note line)
- `worker.log` (+1 multi-line entry)
- `gaps.md` (+1 entry — parliament.gov.zm drift flagged for human review)

## Files NOT mutated this tick

- `approvals.yaml` (per non-negotiable #4)
- `corpus.sqlite` (no record writes)
- `records/**/*.json` (no record mutations — Phase 8 is read-only by design)
- `judges_registry.yaml` (no judgment ingestion this tick)
- `scripts/batch_0569_phase8_reverify.py` (NOT committed per sandbox-session
  safety constraint, b0548..b0568 precedent — inline runner only).
