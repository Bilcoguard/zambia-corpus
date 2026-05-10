# Batch 0575 — Phase 8 Nightly Re-verification (2026-05-10)

**UTC start:** 2026-05-10T18:45:53Z
**UTC end:** 2026-05-10T18:46:27Z
**Worker:** worker-tick (Phase 8)
**Phase:** phase_8_nightly_reverify (approved 2026-05-06; sample_rate 0.01)
**Parser:** phase8-reverify-0.1.0 (functional contract per scripts/batch_0546_phase8_reverify.py)
**Tick scope:** Twenty-third Phase 8 tick overall; ninth worker-tick of UTC date 2026-05-10
   (after b0563 at 05:50Z, b0564 at 06:02:42Z, b0565 at 09:09:35Z, b0567 at 10:06:09Z,
   b0568 at 10:12:41Z, b0569 at 10:36Z, b0570 at 11:08Z, b0572 at 16:34:30Z).
**Execution mode:** inline runner (`/sessions/laughing-wonderful-hopper/_inline_reverify_b0575.py`,
   NOT committed) per sandbox-session safety constraint maintained since b0548
   (b0548..b0574 precedent). Functional contract matches scripts/batch_0546_phase8_reverify.py
   baseline including scripts/certs/*.pem PKI loader. Differences from baseline:
   tick-suffixed seed `phase8-reverify-2026-05-10-b0575`, plus truncated-stored-hash-prefix
   detection (carried forward from b0570 — classifies recomputed_sha256 starting with the
   stored 16-hex prefix as `truncated_stored_hash_false_drift` instead of `drift`).

## Inputs

- Pool size: **1866** (+1 since b0572's 1865; the +1 corresponds to
  judgment-ingestion-worker b0573 ingestion of judgment-zm-2017-zmcc-1
  Malembeka v AG. b0574 wrote zero records, so pool unchanged from b0573.)
- Seed: `phase8-reverify-2026-05-10-b0575` (tick-suffixed deterministic seed).
- Sample size: **8** (= MAX_BATCH cap; ceil(0.01 × 1866) = 19 → capped at 8).
- Out-of-band re-fetches: **none** (no pending b0572 OOB recommendation).

## Results — 7 match / 1 drift / 0 truncated_stored_hash_false_drift / 0 fetch_error

This is the **highest match rate** observed across the 23-tick Phase 8 series
(prior best was b0567 at 6/8 = 75%). The 7-match tick is heavily weighted
toward stable-PDF cohorts (5 zambialii-source-PDF + 2 parliament static PDF
+ 1 media.zambialii-legacy-/media/legislation/-PDF = 7 stable-PDF endpoints
vs only 1 zambialii-akn-HTML rendering URL in the sample by chance).

| Verdict                              | Count | Records |
|--------------------------------------|------:|---------|
| match                                |     7 | si-zm-1991-042-preservation-of-public-security-income-tax-act-suspension-regulations-1991 (zambialii.org/akn/.../source.pdf 156,398 B); si-zm-2016-018-insurance-premium-levy-exemption-order-2016 (**media.zambialii.org/media/legislation/** legacy-cohort PDF 33,259 B — first observation of this URL pattern in the Phase 8 sample); si-zm-2018-001-teaching-profession-code-of-ethics-regulations-2018 (zambialii.org/akn/.../source.pdf 42,028 B); si-zm-2019-005-customs-and-excise-nickel-and-particle-board-export-duty-remission-regulations-2019 (zambialii.org/akn/.../source.pdf 132,119 B); si-zm-2003-038-banking-and-financial-services-bureau-de-change-regulations-2003 (zambialii.org/akn/.../source.pdf 3,708,035 B — largest single response in the 23-tick series, ~3.7 MB); act-zm-2010-006-the-local-government-amendment-2010 (parliament.gov.zm /amendment_act/ subdir 199,419 B); act-zm-2025-011-customs-exciseamendmentact (parliament.gov.zm /acts/ subdir 19,627 B) |
| drift                                |     1 | si-zm-2019-042-urban-and-regional-planning-designated-local-planning-authorities-regulations-2019 (zambialii.org/akn/.../si bare HTML 39,382 B no `/eng@.../source.pdf` suffix — fits the established AKN-HTML drift cohort) |
| truncated_stored_hash_false_drift    |     0 | — |
| fetch_error                          |     0 | — |

## Cohort-level cumulative tally (post-b0575, 23 ticks)

| Cohort                                                              | Pre-b0575 | Δ b0575 | Post-b0575 |
|---------------------------------------------------------------------|----------:|--------:|-----------:|
| zambialii.org/akn/.../act-or-SI-HTML drift                          |     73/73 |   +1/+1 |      74/74 |
| zambialii.org/akn/.../source.pdf match                              |       5/5 |   +4/+4 |        9/9 |
| **media.zambialii.org/media/legislation/ legacy-PDF match (NEW cohort)** |       0/0 |   +1/+1 |      **1/1** |
| parliament.gov.zm static PDF match (real-match)                     |     73/73 |   +2/+2 |      75/75 |
| parliament.gov.zm static PDF DRIFT (real)                           |      0/74 |   0/+2  |       0/76 |
| parliament.gov.zm static PDF truncated_stored_hash_false_drift      |      1/74 |    0/0  |       1/76 |
| zambialii judgment-akn HTML drift                                   |      3/10 |    0/0  |       3/10 |
| Parliament-node landing                                             |       0/1 |    0/0  |        0/1 |
| Stable-PDF combined supercohort (parliament + zambialii source.pdf + media.zambialii legacy) — real-drift basis | 76/78 | +7/+7 | 83/85 § |

§ Stable-PDF supercohort now 83/85 across 23 ticks. The 2 cumulative non-matches
  remain: act-zm-2020-014 (b0569; reclassified at b0570 OOB to truncated-prefix
  false drift), and act-zm-2020-011 (b0570 — truncated-prefix false drift).
  **Real drift count on stable-PDF supercohort remains zero across 23 ticks.**

## Notable observations (b0575)

1. **First media.zambialii.org/media/legislation/ legacy-PDF observation.**
   si-zm-2016-018 insurance-premium-levy-exemption-order-2016 was ingested
   under a legacy publisher URL that uses `media.zambialii.org/media/legislation/{node_id}/source_file/{hash}/` rather than the standard `zambialii.org/akn/.../eng@.../source.pdf` AKN-canonical pattern. The fetch matched cleanly (33,259 bytes, sha256 fe7060176370981d… unchanged), confirming this legacy URL pattern is byte-stable. This cohort is now tracked separately from the AKN-canonical /source.pdf cohort and from the parliament.gov.zm static-PDF cohort. Operator may wish to scan records/ for additional records on this URL pattern to size the cohort.

2. **Largest single-response observation across 23 Phase 8 ticks.**
   si-zm-2003-038 banking-and-financial-services-bureau-de-change-regulations-2003 (3,708,035 bytes, ~3.7 MB) was the largest single response sampled to date in the Phase 8 series, and matched cleanly. Confirms multi-MB byte-stable behaviour for the zambialii.org/akn/.../source.pdf endpoint cohort.

3. **Highest match rate in the Phase 8 series (7/8 = 87.5%).**
   This tick had the most favourable stable-PDF / AKN-HTML mix to date (7 stable-PDF endpoints sampled vs only 1 AKN-HTML rendering URL by chance). The single AKN-HTML drift continues the 74/74 cumulative AKN-HTML-drift pattern (100% reproduction — no AKN-HTML rendering URL has ever matched its stored hash across 23 Phase 8 ticks).

4. **AKN-HTML drift cohort symmetry holds.** The single drift this tick is
   `https://zambialii.org/akn/zm/act/si/2019/42` (bare path, no `/eng@.../source.pdf` suffix) — same byte-size class (39,382 bytes) and same drift mechanism observed across all prior 73 AKN-HTML observations.

5. **Zero new gaps.** No new findings this tick require a `gaps.md` entry. The b0570 truncated-prefix gap entry remains the standing operator-decision item (15 records with stored 16-hex prefix vs full 64-hex sha256).

## Integrity check — 8/8 PASS

Post-fetch re-read of each sampled record's `source_hash` from
`records/{type}/{year}/{id}.json` confirmed the stored hash is unchanged on disk
pre/post tick for all 8 sampled IDs. **No record file was mutated by this tick.**
All 8 stored hashes are full 64-hex sha256 (no truncated-prefix records sampled
this tick — expected at 8/1866 × 15 ≈ 0.064 per tick).

`approvals.yaml` is unmodified.
`judges_registry.yaml` is unmodified.
`corpus.sqlite` is unmodified (records=1862, records_fts=1862, judgments_meta=172).
SQLite `PRAGMA integrity_check` = `ok`.

## Daily budget (worker-tick channel)

After b0575: cumulative_today (worker-tick channel) = **73 / 2000 fetches**
   (= 65 from b0563+b0564+b0565+b0567+b0568+b0569+b0570+b0572 + 8 this tick)
   = 3.65% of daily ceiling consumed across nine Phase 8 worker-ticks on 2026-05-10.

Judgment-ingestion-worker channel cumulative_today (separate worker) unchanged
this tick at 111/500 (after b0573, b0574).

## Phase 8 status

Phase 8 is **open-ended** by design (1% sample rate of corpus per tick).
No `complete: true` flip is appropriate; per non-negotiable #4 the worker
NEVER flips approved/complete flags. `approvals.yaml` is NOT modified.

## Next-tick recommendations

1. **Standing operator action (Peter):** decide whether to authorise targeted
   v1.3 re-ingestion of the 15 truncated-prefix records flagged in b0570
   gaps.md (still pending; non-negotiable #2 partly underfulfilled for those
   15 records).
2. **NEW (b0575):** scan records/ for additional `media.zambialii.org/media/legislation/` legacy-cohort records to size the new cohort and decide whether stand-alone tracking is warranted long-term, or whether it should be folded into the stable-PDF supercohort.
3. Continue weekly Phase 8 deterministic sampling (no parameter change).
4. Standing parser_v0.3.3 anchor pack (80+ records pending after b0571
   reparse confirmed b0552 8/8 redeferral cohort).
5. Standing OCR pipeline (14 records pending).

## Files written this tick

- `reports/batch-0575.md` (this file)
- `reports/batch-0575-reverify.json` (machine-readable summary, 8-record sample)
- `provenance.log` (+8 lines, one per fetched URL)
- `costs.log` (+1 worker-tick line, +1 JSON note line)
- `worker.log` (+1 multi-line entry)

## Files NOT mutated this tick

- `approvals.yaml` (per non-negotiable #4)
- `corpus.sqlite` (no record writes)
- `records/**/*.json` (no record mutations — Phase 8 is read-only by design)
- `judges_registry.yaml` (no judgment ingestion this tick)
- `gaps.md` (no new finding requiring a gaps entry; b0570 truncated-prefix
  gap entry remains the standing operator-decision item)
- `scripts/batch_0575_phase8_reverify.py` (NOT committed per sandbox-session
  safety constraint, b0548..b0574 precedent — inline runner only).
