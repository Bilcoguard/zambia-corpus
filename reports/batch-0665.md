# Phase 8 batch 0665 — Nightly re-verification

- **Tick:** b0665-phase8
- **Phase:** phase_8_nightly_reverify (approvals.yaml — approved: true, complete: false, sample_rate: 0.01)
- **Parser/fetcher version:** phase8-reverify-0.1.0
- **Script:** `scripts/batch_0665_phase8_reverify.py` (verbatim clone of frozen baseline `scripts/batch_0546_phase8_reverify.py`; only the `BATCH` constant + docstring batch identifier changed; same logic as b0625/b0641/b0652/b0653/b0655/b0660/b0662/b0663)
- **Seed:** `phase8-reverify-2026-05-15-b0665`
- **Started:** 2026-05-15T09:34:43Z
- **Completed:** 2026-05-15T09:35:11Z
- **Wall clock:** ~28s (well within 20-minute budget)

## Sample

| Metric | Value |
|---|---|
| pool_size | 1928 |
| sample_size | 8 |
| sample_rate | 0.01 |
| max_batch | 8 |
| fetches | 8 |
| match | 2 |
| drift | 6 |
| fetch_error | 0 |

Pool size 1928 unchanged from b0663 (no JIW ingestions between b0663 at 09:04Z and b0665 at 09:34Z; the intervening b0664 repair tick mutated existing records in place but did not add new records).

## Results

| Verdict | Type | ID | Source host |
|---|---|---|---|
| drift | act | act-zm-1967-001-suicide-act-1967 | zambialii.org (AKN-HTML, eng@-suffixed) |
| drift | judgment | judgment-zm-2026-zmcc-08-munir-zulu-v-the-attorney-general-and-or | zambialii.org (AKN-HTML, eng@-suffixed) |
| drift | act | act-zm-1975-021-medical-aid-societies-and-nursing-homes--dissolution-and-prohibition--act--1975 | www.zambialii.org (AKN-HTML, eng@-suffixed) |
| drift | act | act-zm-1995-034-national-road-safety-council-act-1995 | www.zambialii.org (AKN-HTML, eng@-suffixed) |
| drift | act | act-zm-1994-005-appropriation-act-1994 | zambialii.org (AKN-HTML, eng@-suffixed) |
| match | si | si-zm-2000-034-national-pension-scheme-transfer-of-employees-order-2000 | zambialii.org (AKN source.pdf) |
| match | act | loz-tobacco-levy-act | www.parliament.gov.zm (static PDF) |
| drift | judgment | judgment-zm-2026-coa-080-gilbert-mofya-vs-the-people | judiciaryzambia.com (dynamic HTML) |

Five drift verdicts are on **ZambiaLII AKN-HTML** pages — known dynamic-content rendering pattern from b0641/b0642/b0652/b0653/b0655/b0660/b0662/b0663 (rendered timestamps and footer counters drift the response sha256 across re-fetches even though the legal content is unchanged). The sixth drift is on **judiciaryzambia.com** — a Court of Appeal judgment URL whose HTML also renders dynamic per-request content. This is the first Phase 8 drift verdict observed on a non-ZambiaLII host in this sample series; pattern is the same family (dynamic_render_drift on dynamic HTML), distinct host. Both match verdicts are on static PDFs (zambialii `source.pdf` Akoma Ntoso publication PDF + parliament.gov.zm static PDF), consistent with the long-running observation that static-PDF canonical URLs are 100% match while dynamic HTML pages drift.

## Integrity checks

| # | Check | Result |
|---|---|---|
| 1 | JSON report well-formed; match+drift+fetch_error == sample_size (2+6+0=8) | PASS |
| 2 | No duplicate IDs in sample (8 unique) | PASS |
| 3 | Every stored_sha256 + fetched_sha256 is a valid 64-hex sha256 | PASS |
| 4 | Every sampled record's stored_sha256 matches the on-disk record's `source_hash` | PASS |
| 5 | No record file mutated by this run (all mtimes < started_at) | PASS |
| 6 | corpus.sqlite NOT touched; records/ NOT touched; approvals.yaml NOT modified | PASS |
| 7 | robots.txt respected; per-host rate limits honoured (zambialii.org=5s gaps observed 6.0/10.0/7.0s; www.zambialii.org=5s gap observed 7.0s; other hosts single-fetch) | PASS |
| 8 | User-Agent honest: `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)` | PASS |

## Drift handling

Per BRIEF.md non-negotiable #4 ("never silently overwrite"), drift on dynamically-rendered HTML pages is **flagged** in `gaps.md`, not auto-overwritten. A separate human-approved remediation tick would be required to either (a) re-snapshot the affected records and update `source_hash`, or (b) switch the canonical `source_url` to a static `source.pdf` Akoma Ntoso publication PDF (where available on media.zambialii.org). For judiciaryzambia.com judgments, no static-PDF alternative is currently known on the same host; remediation would necessarily be route-(a) re-snapshot. None of the drift records' `source_hash` values on disk were modified by this tick.

## Approvals

- `phase_8_nightly_reverify.approved` = true (unchanged)
- `phase_8_nightly_reverify.complete` = false (unchanged — Phase 8 is a continuous nightly cycle, not a one-shot)
- `approvals.yaml` was **not** modified by this tick

## Budget

- Today's fetches before tick: 32/2000 (from b0655-phase8 03:10Z + b0660-phase8 08:05Z + b0662-phase8 08:35Z + b0663-phase8 09:04Z)
- Today's fetches after tick: 40/2000
- LLM tokens: 0 (deterministic pipeline)
- Bandwidth: ~1.14 MB down (650 KB zambialii source.pdf + 145 KB parliament.gov.zm PDF + ~340 KB zambialii AKN-HTML payloads + ~166 KB judiciaryzambia.com HTML)

## Next

- Next Phase 8 tick will continue the nightly sampling cycle (different seed → different 8 records).
- Cumulative Phase 8 drift signal across b0641/b0642/b0652/b0653/b0655/b0660/b0662/b0663/b0665: every drift verdict so far has been a dynamic-render HTML page; static PDFs (parliament.gov.zm + media.zambialii.org source.pdf) remain 100% match. b0665 is the first batch in this series to register dynamic_render_drift on `judiciaryzambia.com` — same family, distinct host. Pattern remains stable enough that a Peter-approved bounded remediation tick — either re-snapshot dynamic-render records or switch canonical URLs to source.pdf where available — would clear most outstanding drift entries in `gaps.md`.
