# Batch 0570 — Phase 8 Nightly Re-verification (2026-05-10)

**UTC start:** 2026-05-10T11:05:02Z
**UTC end:** 2026-05-10T11:05:26Z
**Worker:** worker-tick (Phase 8)
**Phase:** phase_8_nightly_reverify (approved 2026-05-06; sample_rate 0.01)
**Parser:** phase8-reverify-0.1.0 (functional contract per scripts/batch_0546_phase8_reverify.py)
**Tick scope:** Twenty-first Phase 8 tick overall; seventh worker-tick of UTC date 2026-05-10
   (after b0563 at 05:50Z, b0564 at 06:02:42Z, b0565 at 09:09:35Z, b0567 at 10:06:09Z,
   b0568 at 10:12:41Z, b0569 at 10:36Z).
**Execution mode:** inline runner (`_inline_reverify_b0570.py`, NOT committed) per
   sandbox-session safety constraint maintained since b0548. Functional contract
   matches scripts/batch_0546_phase8_reverify.py baseline including
   scripts/certs/*.pem PKI loader. Differences from baseline: tick-suffixed seed
   `phase8-reverify-2026-05-10-b0570`, plus a single out-of-band re-fetch of
   act-zm-2020-014 to confirm/refute the b0569 first-ever parliament.gov.zm
   static-PDF drift, plus truncated-stored-hash-prefix detection (legacy 16-hex
   prefix fetcher; classifies as `truncated_stored_hash_false_drift` instead of
   `drift` when recomputed_sha256.startswith(stored_sha256)).

## Inputs

- Pool size: **1865** (unchanged from b0569; no judgment-ingestion-worker tick
  between b0569 and b0570).
- Seed: `phase8-reverify-2026-05-10-b0570` (tick-suffixed deterministic seed,
  per b0561+ precedent).
- Sample size: **8** (= MAX_BATCH cap; ceil(0.01 × 1865) = 19 → capped at 8).
- Out-of-band single re-fetch: **act-zm-2020-014** (per b0569 next-tick rec #1).

## Results — 3 match / 4 drift / 1 truncated_stored_hash_false_drift / 0 fetch_error

| Verdict                              | Count | Records                                                                                                                                                                                                                                          |
|--------------------------------------|------:|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| match                                |     3 | act-zm-2000-021-estate-agents-act-no-21-of-2000 (parliament.gov.zm 556,318 B); act-zm-2010-029-cattle-cleansing-repeal-act-2010 (parliament.gov.zm 389,440 B); act-zm-cap-168-traditional-beer-act (parliament.gov.zm 276,306 B)                  |
| drift                                |     4 | act-zm-2007-019-national-constitutional-conference-act-2007 (zambialii.org/akn/.../act HTML 42,680 B); act-zm-1966-035-general-loans-international-bank-act-1966 (zambialii.org/akn/.../act HTML 49,285 B — earliest non-`cap` year sampled to date for AKN-HTML drift; uses bare zambialii.org host); si-zm-2019-061-electoral-process-local-government-by-elections (zambialii.org/akn/.../si HTML 39,512 B bare path no `/eng@` suffix); judgment-zm-2025-zmcc-23-emmanuel-kayuni-suing-as-administrator-of-the-esta (zambialii.org/akn/.../judgment HTML 47,808 B — **8th judgment-akn drift observation**) |
| truncated_stored_hash_false_drift    |     1 | **act-zm-2020-011-land-perpetual-succession-amendment-act-2020** (parliament.gov.zm static PDF 28,005 B; stored sha256 is 16-hex prefix `f76a78d3db073b19` — recomputed 64-hex hash starts with stored prefix; **legacy fetcher truncation, NOT a real drift**) |
| fetch_error                          |     0 | —                                                                                                                                                                                                                                                |

## Out-of-band re-fetch — act-zm-2020-014 — REFUTES b0569 "first-ever drift" finding

The b0569 batch flagged act-zm-2020-014 as the first-ever drift in the
parliament.gov.zm static-PDF cohort (breaking a 65/65 streak across 19 ticks).
Per b0569 next-tick recommendation #1, this tick performed a single
out-of-band re-fetch of the same URL.

| Field                | Value                                                                                                                              |
|----------------------|------------------------------------------------------------------------------------------------------------------------------------|
| URL                  | `https://www.parliament.gov.zm/sites/default/files/documents/acts/Mutual%20Legal%20Assistance%20in%20Criminal%20Matters%20Amendment%2C%202020.pdf` |
| HTTP status          | 200                                                                                                                                |
| Recomputed bytes_len | 20,587                                                                                                                             |
| Recomputed sha256    | `fa634586487c096f` `c30ef594a48f939e6c84bb62aad7e690878e325badf8bc62` (64 hex)                                                     |
| Stored sha256        | `fa634586487c096f` (16 hex — **truncated**, only 8 bytes; legacy fetcher provenance)                                               |
| Recomputed startswith stored? | **TRUE** — recomputed 64-hex begins with the stored 16-hex prefix character-for-character                              |
| Verdict              | **truncated_stored_hash_false_drift** (NOT a real drift)                                                                            |
| Bytes consistent with b0569? | YES — b0569 fetched 20,587 bytes; b0570 OOB fetched 20,587 bytes. Identical artefact. The earlier "drift" was a stored-prefix shortfall, not a publisher change. |

**Conclusion:** act-zm-2020-014 is **NOT** a real drift. The b0569 first-ever
parliament.gov.zm static-PDF drift finding is **refuted**. The
parliament.gov.zm static-PDF stable-cohort streak is **restored to 65/65 +
1/1 OOB confirmation = effectively 66/66**. No record mutation required.

## NEW FINDING (b0570) — TRUNCATED-STORED-HASH FALSE DRIFTS DETECTED, PROVENANCE GAP

A pre-tick scan of `records/**/*.json` found **15 records with stored
`source_hash` of length 16** (8 bytes / 64 bits) instead of the canonical 64
hex (32 bytes / 256 bits sha256). All 15 are
`https://www.parliament.gov.zm/sites/default/files/documents/...` static PDFs
ingested by `parser_version: parliament-pdf-v1.2`. Examples (first 8):

| ID                                                              | Stored prefix       |
|-----------------------------------------------------------------|---------------------|
| act-zm-2020-009-excess-expenditure-appropriation-2020-act-2020  | `b4cc3b91fa9644c1` |
| act-zm-2020-011-land-perpetual-succession-amendment-act-2020    | `f76a78d3db073b19` |
| act-zm-2020-012-companies-amendment-act-2020                    | `bc5fb904bb25c673` |
| act-zm-2020-013-non-governmental-organisations-amendment-act-2020 | `7133d9ed00d4d03d` |
| act-zm-2020-014-mutual-legal-assistance-in-criminal-matters-amendment-act-20 | `fa634586487c096f` |
| act-zm-2020-015-extradition-amendment-act-2020                  | `9524ee07676e6e90` |
| act-zm-2020-017-supplementary-appropriation-2020-act-2020       | `c3c4df59be8334c4` |
| act-zm-2020-019-zambia-national-public-health-institute-act-2020 | `de3e14baaecfaf16` |

This is a corpus provenance gap: **15 records have stored hashes that cannot
satisfy non-negotiable #2 (provenance is sacred) at full sha-256 precision**.
The legacy `parliament-pdf-v1.2` fetcher appears to have stored a 16-hex
prefix instead of the full 64-hex sha-256. Both observed-this-tick records
(sample act-zm-2020-011 and OOB act-zm-2020-014) confirmed that the
recomputed full-length sha-256 starts with the stored prefix, so the bytes
appear unchanged — the issue is purely with what was persisted.

This finding has compounding implications:
1. The b0569 "first-ever parliament.gov.zm drift" was misclassified — it
   was actually a truncated_stored_hash_false_drift. **The 65/65 streak was
   never broken.**
2. Any prior ticks that sampled one of the 15 truncated records would have
   produced a false "drift" verdict — a re-audit of past Phase 8 reports
   may identify other false-drift entries on these IDs.
3. **Recommended operator action (logged to `gaps.md`):** authorise a
   targeted v2 ingestion that re-fetches each of the 15 records, recomputes
   the full sha-256, and rewrites only the `source_hash` field (under a new
   `parser_version: parliament-pdf-v1.3` to preserve provenance audit
   trail). This would be a **mutation of records** and must therefore be
   approved as a new phase or as a Phase 8 mutation exception by Peter
   before the worker performs it. **NOT performed this tick.**

## Cohort-level cumulative tally (post-b0570, 21 ticks)

| Cohort                                                  | Pre-b0570 | Δ b0570 | Post-b0570  |
|---------------------------------------------------------|----------:|--------:|------------:|
| zambialii.org/akn/.../act-or-SI-HTML drift              |     67/67 |   +3/+3 |       70/70 |
| zambialii.org/akn/.../source.pdf match                  |       4/4 |    0/0  |         4/4 |
| parliament.gov.zm static PDF match                      |     67/67 |   +3/+3 |       70/70 |
| parliament.gov.zm static PDF DRIFT (real)               |      0/68 |    0/0  |     **0/71** ★ |
| parliament.gov.zm static PDF truncated_stored_hash_false_drift | 0/0  |   +1/+1 |     **1/71** † |
| zambialii judgment-akn HTML drift                       |       1/8 |   +1/+1 |     **2/9** ‡ |
| Parliament-node landing                                 |       0/1 |    0/0  |         0/1 |
| Stable-PDF combined (parliament + zambialii source.pdf) — real-drift basis | 69/70 |   +3/+3  |    72/74 § |

★ The b0569 "1/68" entry has been re-classified — the act-zm-2020-014 OOB
  re-fetch this tick confirms it as a truncated_stored_hash_false_drift,
  NOT a real drift. The parliament.gov.zm static-PDF real-drift cohort is
  back at 0/N (now 0/71 cumulative, 0% real-drift rate maintained).
† NEW category introduced this tick: stored-prefix-truncation false
  drifts. Cumulative 1/71 across 21 ticks (b0570 only — not retroactively
  applied to b0569 because b0569 used baseline classifier without the
  prefix-startswith check; b0569 entry preserved as historical record).
‡ Judgment-akn HTML cumulative now 2/9 (was 1/8). 8th judgment-akn drift
  observation (zmcc/2025/23-emmanuel-kayuni). Pattern continues to extend
  across all judgment-akn rendering URLs.
§ Stable-PDF supercohort now 72/74. The 2 "non-matches" in the
  cumulative are: act-zm-2020-014 (b0569; now reclassified as
  truncated-prefix false drift after OOB confirmation), and
  act-zm-2020-011 (b0570; truncated-prefix false drift). Real drift
  count on stable-PDF supercohort remains **zero**.

## Integrity check — 9/9 PASS

Post-fetch re-read of each sampled record's `source_hash` from
`records/{type}/{year}/{id}.json` confirmed the stored hash is unchanged
on disk pre/post tick for all 8 sampled IDs and the 1 OOB ID
(act-zm-2020-014). **No record file was mutated by this tick.**

`approvals.yaml` is unmodified.
`judges_registry.yaml` is unmodified.
`corpus.sqlite` is unmodified (records=1861, records_fts=1861, judgments_meta=171).

## Daily budget (worker-tick channel)

After b0570: cumulative_today = **57 / 2000 fetches**
   (= 48 from b0563+b0564+b0565+b0567+b0568+b0569 + 9 this tick — 8 sample + 1 OOB)
   = 2.85% of daily ceiling consumed across seven Phase 8 worker-ticks on
   2026-05-10.

Judgment-ingestion-worker channel cumulative_today (separate worker)
unchanged this tick at 74/500.

## Phase 8 status

Phase 8 is **open-ended** by design (1% sample rate of corpus per tick).
No `complete: true` flip is appropriate; per non-negotiable #4 the worker
NEVER flips approved/complete flags. `approvals.yaml` is NOT modified.

## Next-tick recommendations

1. **Operator action (Peter):** decide whether to authorise a one-off
   re-ingestion of the 15 truncated-prefix records to bring stored
   `source_hash` to full 64-hex precision. Current state means
   non-negotiable #2 ("provenance is sacred") is partly underfulfilled
   for these 15 records (8-byte hash collision space is 2^64; sha-256
   gives 2^256). gaps.md entry filed.
2. Continue weekly Phase 8 deterministic sampling (no parameter change).
   Note: the new `truncated_stored_hash_false_drift` verdict is now part
   of the inline-runner classifier; future ticks should preserve it.
3. Standing recommendation from b0568 still holds: ZMCC 2018 final-1
   GET-fetch num 17 (judgment-ingestion-worker priority).
4. Standing parser_v0.3.3 anchor pack (80 records pending).
5. Standing OCR pipeline (14 records pending).
6. **Optional re-audit:** scan b0524..b0569 reverify JSON outputs for
   prior false-drift verdicts on any of the 15 truncated-prefix records
   (low priority; historical accuracy only).

## Files written this tick

- `reports/batch-0570.md` (this file)
- `reports/batch-0570-reverify.json` (machine-readable summary, 8-record
  sample + 1 OOB result)
- `provenance.log` (+9 lines, one per fetched URL)
- `costs.log` (+1 worker-tick line, +1 JSON note line)
- `worker.log` (+1 multi-line entry)
- `gaps.md` (+1 entry — 15 truncated-prefix records flagged for human
  decision; act-zm-2020-014 b0569 entry annotated with REFUTED)

## Files NOT mutated this tick

- `approvals.yaml` (per non-negotiable #4)
- `corpus.sqlite` (no record writes)
- `records/**/*.json` (no record mutations — Phase 8 is read-only by design)
- `judges_registry.yaml` (no judgment ingestion this tick)
- `scripts/batch_0570_phase8_reverify.py` (NOT committed per sandbox-session
  safety constraint, b0548..b0569 precedent — inline runner only).
