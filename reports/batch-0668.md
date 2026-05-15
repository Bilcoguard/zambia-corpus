# Phase 8 batch 0668 — Nightly re-verification

- **Tick:** b0668-phase8
- **Phase:** phase_8_nightly_reverify (approvals.yaml — approved: true, complete: false, sample_rate: 0.01)
- **Parser/fetcher version:** phase8-reverify-0.1.0
- **Script:** `scripts/batch_0668_phase8_reverify.py` (verbatim clone of frozen baseline `scripts/batch_0546_phase8_reverify.py`; only the `BATCH` constant + docstring batch identifier changed; same logic as b0625/b0641/b0652/b0653/b0655/b0660/b0662/b0663/b0665/b0666)
- **Seed:** `phase8-reverify-2026-05-15-b0668`
- **Started:** 2026-05-15T10:33:53Z
- **Completed:** 2026-05-15T10:34:18Z
- **Wall clock:** ~25s (well within 20-minute budget)

## Sample

| Metric | Value |
|---|---|
| pool_size | 1928 |
| sample_size | 8 |
| sample_rate | 0.01 |
| max_batch | 8 |
| fetches | 8 |
| match | 3 |
| drift | 4 |
| fetch_error | 1 |

Pool size 1928 unchanged from b0666 (no new records added between b0666 at 10:05Z and b0668 at 10:33Z; b0667 was a repair tick that updated existing record bodies in place without changing record count or source_url/source_hash, so the Phase 8 pool selection is identical at 1928).

## Results

| Verdict | Type | ID | Source host |
|---|---|---|---|
| match | act | act-zm-2015-009-supplementay-appropriation-2013 | www.parliament.gov.zm (static PDF) |
| match | act | loz-dairies-and-dairy-produce-act | www.parliament.gov.zm (static PDF, LoZ chapter) |
| drift | act | act-zm-1990-012-environmental-protection-and-pollution-control-act-1990 | zambialii.org (AKN-HTML, eng@-suffixed) |
| drift | statutory_instrument | si-zm-2022-065-public-protector-rules-2022 | zambialii.org (AKN-HTML, no eng@-suffix) |
| fetch_error | act | act-zm-2026-005-national-payment-system-act | www.parliament.gov.zm (static PDF — HTTP 404) |
| match | act | act-zm-1997-026-science-and-technology-act-1997 | www.zambialii.org (AKN source.pdf) |
| drift | act | act-zm-1994-031-national-arts-council-of-zambia-act-1994 | www.zambialii.org (AKN-HTML, eng@-suffixed) |
| drift | judgment | judgment-zm-2024-zmcc-09-hastie-sibanda-v-attorney-general | zambialii.org (AKN-HTML, eng@-suffixed) |

All four **drift** verdicts are on **ZambiaLII AKN-HTML** pages — known dynamic-content rendering pattern from b0641/b0642/b0652/b0653/b0655/b0660/b0662/b0663/b0665/b0666 (rendered timestamps and footer counters drift the response sha256 across re-fetches even though the legal content is unchanged). All three **match** verdicts are on static PDFs — one on `zambialii.org`/`www.zambialii.org` AKN `source.pdf` Akoma Ntoso publication PDF, two on `www.parliament.gov.zm` static PDFs — consistent with the long-running observation that static-PDF canonical URLs are 100% match while dynamic AKN HTML pages drift. The single **fetch_error** is the first non-zero fetch_error in this Phase 8 series and is a NEW failure mode (not dynamic render drift):

- **act-zm-2026-005-national-payment-system-act** — `https://www.parliament.gov.zm/sites/default/files/documents/acts/National%20Payment%20System%20Act%20No.%205%20of%202026.pdf` now returns **HTTP 404**. The record was originally fetched at `2026-04-10T22:40:53Z` (stored `source_hash` sha256:dac92c5…). Upstream parliament.gov.zm has either renamed, moved, or removed the file. The on-disk record was NOT mutated by this tick; the discrepancy is the audit signal only.

## Integrity checks

| # | Check | Result |
|---|---|---|
| 1 | JSON report well-formed; match+drift+fetch_error == sample_size (3+4+1=8) | PASS |
| 2 | No duplicate IDs in sample (8 unique) | PASS |
| 3 | Every stored_sha256 + fetched_sha256 (where present) is a valid 64-hex sha256 | PASS |
| 4 | Every sampled record's stored_sha256 matches the on-disk record's `source_hash` | PASS |
| 5 | No record file mutated by this run (all mtimes < started_at) | PASS |
| 6 | corpus.sqlite NOT touched; records/ NOT touched; approvals.yaml NOT modified | PASS |
| 7 | robots.txt respected; per-host rate limits honoured (zambialii.org / www.zambialii.org 5s gaps observed; www.parliament.gov.zm rate-default 2s gap) | PASS |
| 8 | User-Agent honest: `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)` | PASS |

## Drift / fetch_error handling

Per BRIEF.md non-negotiable #4 ("never silently overwrite"), drift on dynamically-rendered HTML pages is **flagged** in `gaps.md`, not auto-overwritten. The fetch_error on the 2026 NPS Act is **separately** flagged in `gaps.md` under a new reason `parliament_static_pdf_now_404_upstream_url_changed`. None of the drift records' `source_hash` values on disk were modified by this tick; the fetch_error record's `source_url`/`source_hash` were likewise not modified. Remediation for the fetch_error requires a Peter-approved bounded probe to (a) confirm whether the file is permanently relocated or transiently 404, and (b) if relocated, update the `source_url` and re-fetch a fresh canonical PDF for re-snapshot.

## Approvals

- `phase_8_nightly_reverify.approved` = true (unchanged)
- `phase_8_nightly_reverify.complete` = false (unchanged — Phase 8 is a continuous nightly cycle, not a one-shot)
- `approvals.yaml` was **not** modified by this tick

## Budget

- Today's fetches before tick: 64/2000 (after b0667-repair 12:14Z)
- Today's fetches after tick: 72/2000
- LLM tokens: 0 (deterministic pipeline)
- Bandwidth: ~3.88 MB down (1 large zambialii AKN source.pdf ≈ 3.0 MB dominates; 2 parliament.gov.zm static PDFs ≈ 244 KB; 4 zambialii AKN-HTML payloads ≈ 700 KB; 1 HTTP-404 body ≈ 0 bytes)

## Next

- Next Phase 8 tick will continue the nightly sampling cycle (different seed → different 8 records).
- Cumulative Phase 8 drift signal across b0641/b0642/b0652/b0653/b0655/b0660/b0662/b0663/b0665/b0666/b0668: every drift verdict so far has been a dynamic-render HTML page (predominantly zambialii AKN-HTML, plus one judiciaryzambia.com in b0665); static PDFs (parliament.gov.zm + zambialii AKN source.pdf + media.zambialii.org source.pdf) remain 100% match where the upstream URL is still reachable. b0668 introduces the first **fetch_error** in this Phase 8 series — a static-PDF URL on parliament.gov.zm that now returns HTTP 404, distinct from dynamic-render drift. A Peter-approved bounded remediation tick for both (a) the dynamic-render-drift backlog and (b) the new 2026 NPS Act 404 would be appropriate next steps.
