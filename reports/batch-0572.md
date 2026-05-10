# Batch 0572 — Phase 8 Nightly Re-verification (2026-05-10)

**UTC start:** 2026-05-10T16:34:30Z
**UTC end:** 2026-05-10T16:34:58Z
**Worker:** worker-tick (Phase 8)
**Phase:** phase_8_nightly_reverify (approved 2026-05-06; sample_rate 0.01)
**Parser:** phase8-reverify-0.1.0 (functional contract per scripts/batch_0546_phase8_reverify.py)
**Tick scope:** Twenty-second Phase 8 tick overall; eighth worker-tick of UTC date 2026-05-10
   (after b0563 at 05:50Z, b0564 at 06:02:42Z, b0565 at 09:09:35Z, b0567 at 10:06:09Z,
   b0568 at 10:12:41Z, b0569 at 10:36Z, b0570 at 11:08Z).
**Execution mode:** inline runner (`/tmp/_inline_reverify_b0572.py`, NOT committed)
   per sandbox-session safety constraint maintained since b0548 (b0548..b0571 precedent).
   Functional contract matches scripts/batch_0546_phase8_reverify.py baseline including
   scripts/certs/*.pem PKI loader. Differences from baseline: tick-suffixed seed
   `phase8-reverify-2026-05-10-b0572`, plus truncated-stored-hash-prefix detection
   (carried forward from b0570 — classifies recomputed_sha256 starting with the
   stored 16-hex prefix as `truncated_stored_hash_false_drift` instead of `drift`).

## Inputs

- Pool size: **1865** (unchanged from b0570; no judgment-ingestion-worker tick
  between b0570 and b0572 added new records to the candidate pool — b0571 was
  a reparse-only tick that wrote zero new records).
- Seed: `phase8-reverify-2026-05-10-b0572` (tick-suffixed deterministic seed).
- Sample size: **8** (= MAX_BATCH cap; ceil(0.01 × 1865) = 19 → capped at 8).
- Out-of-band re-fetches: **none** (no pending b0571 OOB recommendation).

## Results — 4 match / 4 drift / 0 truncated_stored_hash_false_drift / 0 fetch_error

| Verdict                              | Count | Records                                                                                                                                                                                                                                          |
|--------------------------------------|------:|------|
| match                                |     4 | act-zm-2022-006-the-judges-conditions-of-service-act-2022 (parliament.gov.zm 282,247 B); act-zm-2019-016-customs-and-excise-amendment-act-2019 (parliament.gov.zm 27,974 B); act-zm-2015-014-zambia-wildlife-act (parliament.gov.zm 219,509 B); si-zm-2021-061-protection-of-traditional-knowledge-genetic-resources-and-expressions-of-folklor (zambialii.org/akn/.../source.pdf 596,918 B — second media-zambialii-/source.pdf-cohort match observation tracking from b0565 first observation) |
| drift                                |     4 | judgment-zm-2022-zmsc-39-teal-minerals-barbados-incorporated-v-zambia-reven (zambialii.org/akn/.../judgment HTML 49,912 B — **9th judgment-akn drift observation**); si-zm-2021-067-national-assembly-general-elections-mandevu-constituency (zambialii.org/akn/.../si HTML 40,176 B bare path no `/eng@` suffix); si-zm-2021-073-public-holidays-declaration-no-4-notice-2021 (zambialii.org/akn/.../si HTML 39,142 B bare path); si-zm-2022-006-zambia-police-fees-regulations-2022 (zambialii.org/akn/.../si HTML 41,828 B bare path) |
| truncated_stored_hash_false_drift    |     0 | —                                                                                                                                                                                                                                                |
| fetch_error                          |     0 | —                                                                                                                                                                                                                                                |

## Cohort-level cumulative tally (post-b0572, 22 ticks)

| Cohort                                                              | Pre-b0572 | Δ b0572 | Post-b0572 |
|---------------------------------------------------------------------|----------:|--------:|-----------:|
| zambialii.org/akn/.../act-or-SI-HTML drift                          |     70/70 |   +3/+3 |      73/73 |
| zambialii.org/akn/.../source.pdf match                              |       4/4 |   +1/+1 |        5/5 |
| parliament.gov.zm static PDF match                                  |     70/70 |   +3/+3 |      73/73 |
| parliament.gov.zm static PDF DRIFT (real)                           |      0/71 |    0/0  |       0/74 |
| parliament.gov.zm static PDF truncated_stored_hash_false_drift      |      1/71 |    0/0  |       1/74 |
| zambialii judgment-akn HTML drift                                   |       2/9 |   +1/+1 |     **3/10** ‡ |
| Parliament-node landing                                             |       0/1 |    0/0  |        0/1 |
| Stable-PDF combined (parliament + zambialii source.pdf) — real-drift basis | 72/74 |   +4/+4 |    76/78 § |

‡ Judgment-akn HTML cumulative now 3/10 (was 2/9). 9th judgment-akn drift
  observation (judgment-zm-2022-zmsc-39 teal-minerals-barbados-incorporated-v-zambia-reven).
  The judgment-akn drift cohort continues to track in lockstep with the act/SI-akn
  drift cohort.
§ Stable-PDF supercohort now 76/78. The 2 cumulative non-matches remain:
  act-zm-2020-014 (b0569; reclassified at b0570 OOB to truncated-prefix
  false drift), and act-zm-2020-011 (b0570 — truncated-prefix false drift).
  Real drift count on stable-PDF supercohort remains **zero**.

## Notable observations (b0572)

1. **Second `source.pdf` cohort match.** si-zm-2021-061 (Protection of Traditional
   Knowledge, Genetic Resources and Expressions of Folklore Regulations) sourced
   from `zambialii.org/akn/zm/act/si/2021/61/eng@2021-05-14/source.pdf` matched.
   This is the second `source.pdf`-endpoint observation across 22 ticks (first was
   b0565 lo-cal-government-administrator-kafue-town-2022). The
   `/source.pdf`-suffixed AKN-rendered-PDF cohort continues to behave like
   parliament.gov.zm static PDFs (stable bytes), distinct from the bare AKN-HTML
   cohort (consistently drifting). Cumulative now 5/5 source.pdf matches.

2. **Three SI-akn HTML drifts in a single sample.** si-zm-2021-067, si-zm-2021-073,
   si-zm-2022-006 — all bare-path (no `/eng@` suffix), all drifting. Reinforces
   the zambialii AKN-HTML rendering layer's known instability. No new finding;
   pattern is now well-established (73/73 cumulative AKN-HTML drifts).

3. **No truncated-prefix false drifts this tick.** The 15-record truncated-prefix
   cohort flagged in b0570 gaps.md remains unsampled this tick (sample drew zero
   records from that 15-record subset out of 1865). This is consistent with
   sampling probability: 8/1865 × 15 ≈ 0.064 expected truncated samples per tick.
   Operator decision (Peter) on targeted v1.3 re-ingestion still pending.

4. **First match for act-zm-2022-006-the-judges-conditions-of-service-act-2022.**
   This is a notable record because it is the statutory basis for the
   judges_registry.yaml title-history (DCJ → Acting CJ etc.) and it should remain
   stable. Confirmed match: 282,247 bytes, sha256 cf333e2df02f0b1d… unchanged.

## Integrity check — 8/8 PASS

Post-fetch re-read of each sampled record's `source_hash` from
`records/{type}/{year}/{id}.json` confirmed the stored hash is unchanged on disk
pre/post tick for all 8 sampled IDs. **No record file was mutated by this tick.**

`approvals.yaml` is unmodified.
`judges_registry.yaml` is unmodified.
`corpus.sqlite` is unmodified (records=1861, records_fts=1861, judgments_meta=171).

## Daily budget (worker-tick channel)

After b0572: cumulative_today = **65 / 2000 fetches**
   (= 57 from b0563+b0564+b0565+b0567+b0568+b0569+b0570 + 8 this tick)
   = 3.25% of daily ceiling consumed across eight Phase 8 worker-ticks on 2026-05-10.

Judgment-ingestion-worker channel cumulative_today (separate worker) unchanged
this tick at 74/500.

## Phase 8 status

Phase 8 is **open-ended** by design (1% sample rate of corpus per tick).
No `complete: true` flip is appropriate; per non-negotiable #4 the worker
NEVER flips approved/complete flags. `approvals.yaml` is NOT modified.

## Next-tick recommendations

1. **Standing operator action (Peter):** decide whether to authorise targeted
   v1.3 re-ingestion of the 15 truncated-prefix records flagged in b0570
   gaps.md (still pending; non-negotiable #2 partly underfulfilled for those
   15 records).
2. Continue weekly Phase 8 deterministic sampling (no parameter change).
3. Standing recommendation from b0568 still holds: ZMCC 2018 final-1
   GET-fetch num 17 (judgment-ingestion-worker priority).
4. Standing parser_v0.3.3 anchor pack (80 records pending after b0571
   reparse confirmed b0552 8/8 redeferral cohort).
5. Standing OCR pipeline (14 records pending).

## Files written this tick

- `reports/batch-0572.md` (this file)
- `reports/batch-0572-reverify.json` (machine-readable summary, 8-record sample)
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
- `scripts/batch_0572_phase8_reverify.py` (NOT committed per sandbox-session
  safety constraint, b0548..b0571 precedent — inline runner only).
