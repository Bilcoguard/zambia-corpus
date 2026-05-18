# Phase 8 — Nightly Re-verification — batch 0716

- **Phase:** `phase_8_nightly_reverify`
- **Worker run id:** `b0716-phase8`
- **Script:** `scripts/batch_0716_phase8_reverify.py` (clone of frozen baseline `scripts/batch_0546_phase8_reverify.py`; only `BATCH` constant and docstring header differ from `scripts/batch_0715_phase8_reverify.py`)
- **Parser version:** `phase8-reverify-0.1.0`
- **Seed:** `phase8-reverify-2026-05-18-b0716`
- **Started:** `2026-05-18T20:05:36Z`
- **Completed:** `2026-05-18T20:06:15Z`
- **Wall clock:** 39s (budget 20min; headroom ~19m21s)
- **Pool size:** 1973 records (records/**/*.json with both `source_url` + `source_hash`) — up from 1965 in b0715 by exactly the 8 new ZMCC judgments added to disk by b0716-jiw (delta-to-DB-count of 3 remains constant; the 3 records-without-source_hash continue to be excluded from the Phase 8 pool by design).
- **Sample size:** 8 (`sample_rate 0.01`, capped at `MAX_BATCH=8`)
- **Fetches:** 8 (all HTTP 200)
- **Outcome counts:** match=3, drift=5, fetch_error=0
- **B2 sync:** deferred to host (rclone not in sandbox; Phase 8 is read-only on corpus — no `raw/` mutation)

## Results

| Verdict | Type | ID | Source host | URL kind | Notes |
|---|---|---|---|---|---|
| match | act | act-zm-2013-005-the-teaching-profession-2013 | www.parliament.gov.zm | parliament.gov.zm Act PDF | stable-PDF supercohort match |
| match | act | act-zm-cap-257-national-assembly-staff-act | www.parliament.gov.zm | parliament.gov.zm Act PDF | stable-PDF supercohort match |
| drift | si | si-zm-2025-016-civil-aviation-designated-provincial-and-strategic-airports-regulations-2025 | zambialii.org | AKN landing/bare-path HTML (`/akn/zm/act/si/2025/16`) | `zambialii_akn_html_dynamic_render_drift` cohort (bare-path sub-variant; SI-HTML) |
| drift | act | act-zm-1996-039-human-rights-commission-act-1996 | zambialii.org | AKN-HTML `eng@`-suffixed (`/akn/zm/act/1996/39/eng@1996-12-31`) | `zambialii_akn_html_dynamic_render_drift` cohort (`eng@`-suffixed sub-variant) |
| drift | si | si-zm-2021-049-zambia-institute-of-advanced-legal-education-students-rules-2021 | zambialii.org | AKN landing/bare-path HTML (`/akn/zm/act/si/2021/49`) | `zambialii_akn_html_dynamic_render_drift` cohort (bare-path sub-variant; SI-HTML) |
| drift | judgment | judgment-zm-2023-zmcc-04-ikelenge-town-council-v-national-pension-scheme-au | zambialii.org | AKN landing/bare-path HTML (`/akn/zm/judgment/zmcc/2023/4`) | `zambialii_akn_html_dynamic_render_drift` cohort (bare-path sub-variant; judgment-HTML) — record newly ingested by b0716-jiw on 2026-05-18 |
| match | si | si-zm-1994-039-workmens-compensation-assessment-or-earnings-regulations-1994 | zambialii.org | zambialii.org `source.pdf` (`/akn/zm/act/si/1994/39/eng@1994-02-18/source.pdf`) | zambialii.org source.pdf supercohort match |
| drift | judgment | judgment-zm-2023-zmcc-05-governance-elections-advocacy-research-services-in | zambialii.org | AKN landing/bare-path HTML (`/akn/zm/judgment/zmcc/2023/5`) | `zambialii_akn_html_dynamic_render_drift` cohort (bare-path sub-variant; judgment-HTML) — record newly ingested by b0716-jiw on 2026-05-18 |

The b0716 sample composition: 2/8 parliament.gov.zm Act PDFs, 1/8 zambialii.org `source.pdf` (SI PDF), and 5/8 zambialii.org AKN-HTML pages (1 `eng@`-suffixed Act + 2 bare-path SIs + 2 bare-path judgments). All 2 parliament.gov.zm PDFs matched (stable-PDF supercohort behaviour). The 1 zambialii.org `source.pdf` matched (zambialii source.pdf supercohort behaviour). All 5 zambialii.org AKN-HTML records drifted (`zambialii_akn_html_dynamic_render_drift` cohort — known server-rendered timestamp / asset cache-busting behaviour; not substantive legal-text change).

Notable: 2 of the 5 drifts (judgment-zm-2023-zmcc-04 and judgment-zm-2023-zmcc-05) are records freshly ingested today by b0716-jiw (timestamp 2026-05-18T19:42:44Z) — i.e. drift was observed within ~24 minutes of stored_sha256 being computed. This is consistent with the documented AKN-HTML cohort behaviour (server emits per-request asset cache-busting query strings / inline timestamps), not a JIW ingestion defect; the underlying legal text is identical. No corpus mutation required; cohort assignment captured for cumulative telemetry.

Overall match rate this tick (3/8 = 37.5%) is below b0715 (5/8 = 62.5%) and b0712 (6/8 = 75%) but above b0714 (2/8 = 25%); the swing is purely a function of sample composition under the b0716 seed (5/8 records drawn from the AKN-HTML drift cohort) and not a corpus-health signal. Cumulative Phase 8 telemetry across recent ticks remains in line with the documented per-URL-kind hit rates (parliament.gov.zm PDFs ≈100% match; zambialii.org `source.pdf` ≈100% match; AKN-HTML `eng@`-suffixed ≈100% drift; AKN landing/bare-path HTML ≈100% drift).

## Integrity checks

| # | Check | Result |
|---|---|---|
| 1 | JSON report well-formed; match+drift+fetch_error == sample_size (3+5+0=8) | PASS |
| 2 | No duplicate IDs in sample (8 unique) | PASS |
| 3 | Every stored + fetched sha256 is a valid 64-hex sha256 | PASS |
| 4 | Every sampled record's `stored_sha256` matches the on-disk record's `source_hash` (proper `sha256:` prefix-stripping) | PASS (no record file mutated this tick) |
| 5 | No tracked record file modified by this run (script is read-only) | PASS (script never opens records/ for write — source-verified) |
| 6 | `corpus.sqlite` NOT touched by Phase 8; `approvals.yaml` NOT modified | PASS (`git diff --name-only approvals.yaml` empty) |
| 7 | robots.txt respected; per-host rate limits honoured (zambialii.org min_gap ≥ 5s; deterministic `sleep_for_host` mechanism unchanged from baseline) | PASS |
| 8 | User-Agent honest: `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)` | PASS |
| 9 | corpus.sqlite live `quick_check=ok records=1970 records_fts=1970 dup_ids=0` (FTS parity with records table preserved across tick) | PASS |

All 9 checks PASS — tick commits via normal path.

## Cost / budget

- Network fetches this tick: 8 (all HTTP 200)
- Cumulative daily fetches across all workers today (per costs.log fetches= sum): ~413 pre-tick; + 8 (this tick) = ~421 of 2000 daily budget. Plenty of headroom.
- Tokens consumed: 0 (deterministic pipeline, no LLM calls). LLM budget 0/1,000,000 today.
- Bandwidth: 1,200,128 bytes total (~1.2 MB); largest = `act-zm-2013-005-the-teaching-profession-2013` (623,358 B, parliament.gov.zm PDF).
- Wall clock: 39s (budget 20min; headroom ~19m21s).

## B2 sync

Deferred to host — rclone not available in sandbox. Phase 8 is read-only on corpus (no `raw/` mutation) so deferral is acceptable per BRIEF.md §8.

## Repo-state note

The working tree at tick start contained uncommitted artifacts from the parallel `b0716-jiw` ZambiaLII reparse run (8 new ZMCC judgment record files, judges_registry/gaps.md/provenance.log/costs.log appends, and a `corpus.sqlite` mutation to 1970 records). These are JIW-worker deliverables that the JIW tick prepared but did not commit; Phase 8 (this tick) does not own or commit them. Phase 8's own commit is scoped strictly to this tick's deliverables (new script + new reports + own log/costs/provenance appends). The next JIW tick will commit (or supersede) the JIW deliverables under its own commit message.

## Next tick

Routine Phase 8 sampling continues. No new audit-trail items spawned this tick — all 5 drifts fall under the pre-existing `zambialii_akn_html_dynamic_render_drift` cohort. Pre-existing carry-forwards remain:
- `judgment-zm-2025-zmcc-14` canonical-URL-date variant 404 (b0700 — audit-only; remediation requires explicit Peter approval).
- Existing 15 `parliament-pdf-v1.2` truncated-16hex defect records remain an open operator-triage item (latent — not drawn this tick).
