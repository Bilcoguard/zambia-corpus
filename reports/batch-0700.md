# Phase 8 — Nightly Re-verification — batch 0700

- **Phase:** `phase_8_nightly_reverify`
- **Worker run id:** `b0700-phase8`
- **Script:** `scripts/batch_0700_phase8_reverify.py`
- **Parser version:** `phase8-reverify-0.1.0`
- **Seed:** `phase8-reverify-2026-05-18-b0700`
- **Started:** `2026-05-18T12:33:29Z`
- **Completed:** `2026-05-18T12:33:57Z`
- **Wall clock:** 28s (budget 20min; headroom ~19m32s)
- **Pool size:** 1957 records (records/**/*.json with both source_url + source_hash)
- **Sample size:** 8 (sample_rate 0.01, capped at MAX_BATCH=8)
- **Fetches:** 8
- **Outcome counts:** match=4, drift=3, fetch_error=1
- **B2 sync:** deferred to host (rclone not in sandbox; Phase 8 is read-only on corpus — no `raw/` mutation)

## Results

| Verdict | Type | ID | Source host | URL kind | Notes |
|---|---|---|---|---|---|
| match | act | act-zm-2011-029-zambia-development-agency-amendment-act-2011 | www.parliament.gov.zm | parliament.gov.zm Act PDF | stable-PDF supercohort match |
| drift | judgment | judgment-zm-2023-zmsc-20-augustine-mwamba-mbuzakosi-and-ors-v-the-people | zambialii.org | AKN-HTML `eng@`-suffixed | dynamic-render cohort |
| match | act | act-zm-2007-021-anti-terrorism-act | www.parliament.gov.zm | parliament.gov.zm Act PDF | stable-PDF supercohort match |
| drift | act | act-zm-1967-026-law-reform-miscellaneous-provisions-act-1967 | zambialii.org | AKN-HTML `eng@`-suffixed | dynamic-render cohort |
| match | act | act-zm-2000-020-the-penal-code-amendment-act-no-20-of-2000 | www.parliament.gov.zm | parliament.gov.zm Act PDF | stable-PDF supercohort match |
| match | si | si-zm-2020-024-national-health-research-bio-banking-regulations-2020 | zambialii.org | AKN source.pdf | stable-PDF supercohort match |
| drift | act | act-zm-1960-041-high-court-act | zambialii.org | AKN-HTML `eng@`-suffixed | dynamic-render cohort |
| fetch_error | judgment | judgment-zm-2025-zmcc-14-the-people-v-john-sinkamba-and-ors | zambialii.org | AKN-HTML `eng@2025-07-25` | HTTP 404 — canonical-URL date variant drift (see gaps.md) |

All 3 drift verdicts are textbook `zambialii_akn_html_dynamic_render_drift` cohort — AKN-HTML landing pages whose dynamic-rendered HTML carries embedded timestamps/footer counters that change between fetches. No new sub-cohort spawned.

All 4 match verdicts are stable-PDF supercohort:
- 3× **www.parliament.gov.zm** Act PDFs (Zambia Development Agency Amdt 2011; Anti-Terrorism Act 2007; Penal Code Amdt No. 20 of 2000) — confirms the parliament.gov.zm Act-PDF supercohort remains 100% stable.
- 1× **zambialii.org** AKN `source.pdf` (national-health-research bio-banking regs SI 2020).

One **fetch_error**: `judgment-zm-2025-zmcc-14-the-people-v-john-sinkamba-and-ors` — HTTP 404 on the stored `source_url` `https://zambialii.org/akn/zm/judgment/zmcc/2025/14/eng@2025-07-25`. The record's `date_decided` on disk is `2025-07-25`, but the **original gaps.md deferral entry** (b0359 / 2026-04-29 / reconfirmed b0494 2026-05-03) records the canonical URL with `eng@2025-07-28`. This strongly suggests the canonical AKN URL date variant was `…/14/eng@2025-07-28` upstream and the on-disk `…/14/eng@2025-07-25` record was ingested against a non-canonical date variant that has since been removed/canonicalised by ZambiaLII. **Not a content removal** — sister record metadata (case 2025/CCZ/R001, citation [2025] ZMCC 14, decided 2025-07-25) is unaffected. Remediation requires Peter-approved bounded probe of the alternate URL `…/14/eng@2025-07-28` before any source_url/source_hash mutation. Per BRIEF non-negotiable #4 the on-disk record is NOT mutated by this tick. Audit-only entry written to `gaps.md`.

Drift rate this tick (3/7 successfully-fetched = ~43%) is within the long-run expected band (AKN-HTML ≈100% drift; stable PDFs ≈100% match; this sample drew 3 AKN-HTML and 4 stable-PDFs successfully → 3/3 AKN-HTML drift + 4/4 stable-PDF match, matching expectation exactly).

## Integrity checks

| # | Check | Result |
|---|---|---|
| 1 | JSON report well-formed; match+drift+fetch_error == sample_size (4+3+1=8) | PASS |
| 2 | No duplicate IDs in sample (8 unique) | PASS |
| 3 | Every stored + fetched sha256 is a valid 64-hex sha256 (fetch_error rows have null fetched_sha256 by spec — 1 this tick, properly null) | PASS |
| 4 | Every sampled record's stored_sha256 matches the on-disk record's `source_hash` (proper `sha256:` prefix-stripping) | PASS (no record file mutated this tick) |
| 5 | No tracked record file modified by this run (script is read-only) | PASS (`git diff --stat records/` empty pre-commit) |
| 6 | corpus.sqlite NOT touched; approvals.yaml NOT modified | PASS (`git diff --stat corpus.sqlite approvals.yaml` empty) |
| 7 | robots.txt respected; per-host rate limits honoured (zambialii.org min_gap ≥ 5s; deterministic `sleep_for_host` mechanism unchanged from baseline) | PASS |
| 8 | User-Agent honest: `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)` | PASS |
| 9 | corpus.sqlite live `quick_check=ok records=1954 records_fts=1954 dup_ids=0` (baseline parity preserved across tick) | PASS |

All 9 checks PASS — tick commits via normal path.

## Cost / budget

- Network fetches this tick: 8 (7× HTTP 200, 1× HTTP 404)
- Cumulative daily fetches (main + jiw, approx): 8 (b0697) + 8 (b0698) + 8 (b0700, this tick) + 48 (b0699-jiw judgments) ≈ ~145 of 2000 daily budget
- Tokens consumed: 0 (deterministic pipeline, no LLM calls)
- Bandwidth: 2,725,378 bytes total (~2.6 MB); largest = act-zm-2007-021-anti-terrorism-act (1,460,166 bytes parliament.gov.zm PDF)
- Wall clock: 28s (budget 20min; headroom ~19m32s)

## B2 sync

Deferred to host — rclone not available in sandbox. Phase 8 is read-only on corpus (no `raw/` mutation) so deferral is acceptable per BRIEF.md §8.

## Next tick

Routine Phase 8 sampling continues. New audit-trail items carried forward:
- `judgment-zm-2025-zmcc-14` canonical-URL-date variant 404 (audit-only; remediation requires explicit Peter approval before any source_url mutation).
- Existing 15 `parliament-pdf-v1.2` truncated-16hex defect records remain an open operator-triage item (latent — not drawn this tick).
