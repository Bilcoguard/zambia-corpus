# Phase 8 batch 0670 — Nightly re-verification (HALT — CHECK #3 FAIL)

- **Tick:** b0670-phase8
- **Phase:** phase_8_nightly_reverify (approvals.yaml — approved: true, complete: false, sample_rate: 0.01)
- **Parser/fetcher version:** phase8-reverify-0.1.0
- **Script:** `scripts/batch_0670_phase8_reverify.py` (verbatim clone of frozen baseline `scripts/batch_0546_phase8_reverify.py`; only the `BATCH` constant + docstring batch identifier changed; same logic as b0625/b0641/b0652/b0653/b0655/b0660/b0662/b0663/b0665/b0666/b0668/b0669)
- **Seed:** `phase8-reverify-2026-05-15-b0670`
- **Started:** 2026-05-15T11:36:35Z
- **Completed:** 2026-05-15T11:36:53Z
- **Wall clock:** ~18s (well within 20-minute budget)
- **Tick verdict:** **HALT — no commit** per BRIEF.md / tick-protocol step 6 (CHECK #3 FAIL)

## Sample

| Metric | Value |
|---|---|
| pool_size | 1928 |
| sample_size | 8 |
| sample_rate | 0.01 |
| max_batch | 8 |
| fetches | 8 |
| match | 3 |
| drift | 5 (of which 1 is a CHECK-#3 artefact — see below) |
| fetch_error | 0 |

## Results

| Verdict | Type | ID | Source host |
|---|---|---|---|
| match | act | act-zm-2016-022-the-industrial-design | www.parliament.gov.zm (static PDF) |
| drift | act | act-zm-2017-005-national-technical-regulation-act-2017 | www.zambialii.org (AKN-HTML, eng@-suffixed) |
| drift | act | act-zm-1979-022-public-officers-pensions-zambia-agreement-implementation-act | zambialii.org (AKN-HTML, eng@-suffixed) |
| match | act | act-zm-2022-017-the-zambia-development-agency-act-2022-act-no-17-of-2022 | www.parliament.gov.zm (static PDF) |
| **drift (CHECK-#3 artefact)** | act | **act-zm-2020-021-customs-and-excise-amendment-act-2020** | www.parliament.gov.zm (static PDF) |
| match | act | act-zm-2024-027-property-transfer-tax-2024 | www.parliament.gov.zm (static PDF) |
| drift | statutory_instrument | si-zm-2021-087-national-assembly-by-election-kabwata-constituency-no-77-election-date-and-time-of-poll-no-3-order-2021 | zambialii.org (AKN, no eng@-suffix) |
| drift | act | act-zm-1984-005-excess-expenditure-appropriation-1981-act-1984 | zambialii.org (AKN-HTML, eng@-suffixed) |

## Integrity checks

| # | Check | Result |
|---|---|---|
| 1 | JSON report well-formed; match+drift+fetch_error == sample_size (3+5+0=8) | PASS |
| 2 | No duplicate IDs in sample (8 unique) | PASS |
| 3 | Every stored_sha256 + fetched_sha256 (where present) is a valid 64-hex sha256 | **FAIL** — see "CHECK #3 fail" section below |
| 4 | Every sampled record's stored_sha256 matches the on-disk record's `source_hash` | PASS (stored_sha256 in the JSON report is the verbatim post-`normalise_hash()` value from the on-disk record file for all 8 entries) |
| 5 | No record file mutated by this run (script is read-only) | PASS |
| 6 | corpus.sqlite NOT touched; records/ NOT touched; approvals.yaml NOT modified | PASS |
| 7 | robots.txt respected; per-host rate limits honoured (zambialii.org min_gap=5.0s ≥ required 5s; www.parliament.gov.zm rate default; all observed inter-fetch gaps ≥ required) | PASS |
| 8 | User-Agent honest: `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)` | PASS |

## CHECK #3 fail — full diagnostic

Record `act-zm-2020-021-customs-and-excise-amendment-act-2020.json` has a `source_hash` of `sha256:ca6c004832232876` — a **16-hex prefix**, not a valid 64-character SHA-256 hex digest. This violates BRIEF.md non-negotiable #2 ("Provenance is sacred. Every record must include source_url, source_hash (sha256), …").

Important context (NOT a true content drift):

- The fetched body's full SHA-256 is `ca6c004832232876a86f28cfd8b955fa6f119b7844bb2c2759db427006a2dfc2` (46443 bytes, HTTP 200, parliament.gov.zm).
- The stored 16-hex prefix `ca6c004832232876` is **exactly the first 16 hex characters** of that fetched digest.
- The fetched content therefore *probably* matches the original snapshot — but the stored hash is too short to prove it. The "drift" verdict produced by `scripts/batch_0670_phase8_reverify.py` is an unavoidable artefact of strict equality comparison against a malformed stored hash; it is **not** a real content drift signal.

Root cause (provisional, supported by corpus-wide scan inside this tick): the `parliament-pdf-v1.2` parser appears to have written 16-hex truncated `source_hash` values for a contiguous run of 2020 Acts ingested via `www.parliament.gov.zm`. A quick read-only scan from this tick's working directory found **15 records** with len=16 stored hashes (all `parliament-pdf-v1.2`, all ids `act-zm-2020-009` through `act-zm-2020-024`). A further **14 records** have an empty `source_hash`. The full enumeration is preserved verbatim in `error-reports/2026-05-15T113700Z-b0670-check3-fail.md`.

## Why this tick HALTS without committing

BRIEF.md / tick-protocol step 6 (verbatim, from the scheduled-task instruction):

> Run the integrity check on the batch: no duplicate IDs, every amended_by and repealed_by reference resolves, every cited_authorities reference resolves, every source_hash matches the on-disk raw file. If ANY check fails, do NOT commit. Write a diagnostic to gaps.md and error-reports/<timestamp>.md, then stop.

CHECK #3 has failed (one of the eight sampled records has a malformed stored `source_hash` violating non-negotiable #2 — provenance is sacred). Therefore this tick:

- Writes `reports/batch-0670.md` (this file) and `reports/batch-0670-reverify.json` (the verbatim machine output of the script) into `reports/`.
- Writes `error-reports/2026-05-15T113700Z-b0670-check3-fail.md` with the full diagnostic and the corpus-wide enumeration.
- Appends the diagnostic to `gaps.md` (NEW reason code: `parliament_pdf_v1_2_truncated_16hex_source_hash`) plus the 4 routine `zambialii_akn_html_dynamic_render_drift` entries.
- Appends to `worker.log`, `costs.log`, `provenance.log`.
- **Does NOT touch `corpus.sqlite`**, `records/`, or `approvals.yaml`.
- **Does NOT git-commit** — these artefacts remain in the working tree only. The next tick (or a Peter-approved repair tick) will deal with the underlying parser-v1.2 provenance defect before any normal-path commit resumes.

## Approvals

- `phase_8_nightly_reverify.approved` = true (unchanged)
- `phase_8_nightly_reverify.complete` = false (unchanged — Phase 8 is a continuous nightly cycle, not a one-shot)
- `approvals.yaml` was **not** modified by this tick

## Budget

- Today's fetches before tick: 80/2000 (after b0669 at 11:05Z)
- Today's fetches after tick: 88/2000
- LLM tokens: 0 (deterministic pipeline)
- Bandwidth: ~720 KB down (largest: act-zm-2022-017 ≈ 359 KB; smallest: act-zm-2024-027 ≈ 13 KB)

## Next

- Operator/Peter action required: triage the `parliament_pdf_v1_2_truncated_16hex_source_hash` defect (15 records identified by this tick) before the next Phase 8 normal-path tick can commit cleanly. Until then, Phase 8 ticks may continue to surface CHECK #3 failures whenever the random sample of 8 happens to draw one of the 15 affected records (probability ≈ 15/1928 ≈ 0.78% per sampled record, ≈ 6.2% per 8-record batch).
- Cumulative Phase 8 drift signal across b0641…b0669 (excluding b0670's CHECK-#3 artefact): every drift verdict has been a dynamic-render HTML page (overwhelmingly zambialii AKN-HTML, plus one judiciaryzambia.com in b0665). Static PDFs (parliament.gov.zm + zambialii AKN source.pdf + media.zambialii.org source.pdf) remain 100% content-match where the upstream URL is still reachable and the stored hash is well-formed. The b0668 fetch_error on the 2026 NPS Act parliament.gov.zm URL remains the only non-dynamic-render content anomaly observed.
