# Phase 8 batch 0671 — Nightly re-verification

- **Tick:** b0671-phase8
- **Phase:** phase_8_nightly_reverify (approvals.yaml — approved: true, complete: false, sample_rate: 0.01)
- **Parser/fetcher version:** phase8-reverify-0.1.0
- **Script:** `scripts/batch_0671_phase8_reverify.py` (verbatim clone of frozen baseline `scripts/batch_0546_phase8_reverify.py`; only the `BATCH` constant + docstring batch identifier changed; same logic as b0625/b0641/b0652/b0653/b0655/b0660/b0662/b0663/b0665/b0666/b0668/b0669)
- **Seed:** `phase8-reverify-2026-05-15-b0671`
- **Started:** 2026-05-15T12:06:02Z
- **Completed:** 2026-05-15T12:06:30Z
- **Wall clock:** ~28s (well within 20-minute budget)
- **Predecessor:** b0670-phase8 (HALT — CHECK#3 FAIL on `act-zm-2020-021` 16-hex truncated stored hash; 15-record corpus-wide defect awaiting human triage per `error-reports/2026-05-15T113700Z-b0670-check3-fail.md`).

## Sample

| Metric | Value |
|---|---|
| pool_size | 1928 |
| sample_size | 8 |
| sample_rate | 0.01 |
| max_batch | 8 |
| fetches | 8 |
| match | 5 |
| drift | 3 |
| fetch_error | 0 |

Pool size 1928 unchanged from b0666/b0668/b0669/b0670 (no record write/delete since b0669 commit `794363c`; b0667-repair files remain in working tree but never committed; the b0670 halt diagnostic added only audit-trail content under `gaps.md`/`worker.log`/`reports/`/`error-reports/`, no records mutated).

## Results

| Verdict | Type | ID | Source host | URL kind |
|---|---|---|---|---|
| match | act | act-zm-2025-004-cyber-crime-2025 | www.parliament.gov.zm | static PDF |
| drift | statutory_instrument | si-zm-2009-042-chiefs-recognition-no-5-order-2009 | www.zambialii.org | AKN `eng@/source.pdf` (FIRST `/source.pdf` drift in 28-tick Phase 8 series) |
| match | act | act-zm-2010-040-lands-and-deeds-registry-amendment | www.parliament.gov.zm | static PDF |
| match | act | loz-plant-pests-and-diseases-act | www.parliament.gov.zm | static PDF (Laws of Zambia volume) |
| drift | act | act-zm-1968-005-gwembe-district-special-fund-dissolution-act-1968 | zambialii.org | AKN-HTML `eng@`-suffixed (dynamic-render cohort) |
| match | act | act-zm-1991-023-national-assembly-staff-act-1991 | media.zambialii.org | static PDF (publication-document) |
| drift | act | act-zm-2014-006-excess-expenditure-appropriation-2011-act | zambialii.org | AKN-HTML `eng@`-suffixed (dynamic-render cohort) |
| match | statutory_instrument | si-zm-2011-004-workers-compensation-permanent-disablementcommutation-of-pension-regulation-2011 | zambialii.org | AKN `eng@/source.pdf` (stable-PDF supercohort match) |

Two of the three drifts are the well-known ZambiaLII AKN-HTML `eng@`-suffixed dynamic-render pattern (documented across b0641/b0642/b0652/b0653/b0655/b0660/b0662/b0663/b0665/b0666/b0668/b0669) — rendered timestamps and footer counters drift the response sha256 across re-fetches even though the legal content is unchanged.

**The third drift (`si-zm-2009-042`) is a first observation:** the stored URL ends in `/source.pdf`, which historically belongs to the **stable-PDF supercohort** (zero real drifts across the prior 27 ticks, supercohort cumulative 173/177 → 174/178 if this stayed a match). The fetched response (HTTP 200, 176,712 bytes) is a full PDF body; both the stored and fetched sha256 are well-formed 64-hex (so this is not a CHECK#3 truncation artefact). One subdomain detail worth flagging for operator triage: this record's `source_url` uses **`www.zambialii.org`** (with `www`), whereas the matching `si-zm-2011-004` `/source.pdf` record uses **`zambialii.org`** (no `www`). Whether the `www`-prefixed host serves a different rendering (e.g., 30x to a re-published PDF) or whether the underlying publication was re-typeset are both plausible — neither has been investigated by this read-only tick.

The five **match** verdicts are all static PDF endpoints: three on `www.parliament.gov.zm`, one on `media.zambialii.org`, one on `zambialii.org` (no-`www`) AKN `source.pdf`. Consistent with the standing observation that static-PDF canonical URLs are nearly 100% match.

## Integrity checks

| # | Check | Result |
|---|---|---|
| 1 | JSON report well-formed; match+drift+fetch_error == sample_size (5+3+0=8) | PASS |
| 2 | No duplicate IDs in sample (8 unique) | PASS |
| 3 | Every stored_sha256 + fetched_sha256 (where present) is a valid 64-hex sha256 | PASS |
| 4 | Every sampled record's stored_sha256 matches the on-disk record's `source_hash` | PASS |
| 5 | No record file mutated by this run (script is read-only) | PASS |
| 6 | corpus.sqlite NOT touched; records/ NOT touched; approvals.yaml NOT modified | PASS |
| 7 | robots.txt respected; per-host rate limits honoured (zambialii.org min_gap ≥ 5s; www.zambialii.org min_gap ≥ 5s; media.zambialii.org min_gap ≥ 5s; www.parliament.gov.zm 2s default; deterministic `sleep_for_host` mechanism unchanged from baseline) | PASS |
| 8 | User-Agent honest: `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)` | PASS |

CHECK#3 PASS — none of the 8 sampled records hit the 15-record `parliament-pdf-v1.2` truncated-16-hex stored-hash defect surfaced by the b0670 HALT. (The 15 defective records remain on disk; this tick's seed simply did not draw any of them. Probability of a future Phase 8 tick hitting at least one defective record on a random 8-of-1928 sample remains ≈ 6.1% until Peter authorises remediation per `error-reports/2026-05-15T113700Z-b0670-check3-fail.md`.)

## Drift handling

Per BRIEF.md non-negotiable #4 ("never silently overwrite"), drift on dynamically-rendered HTML pages is **flagged** in `gaps.md`, not auto-overwritten. The three drift records' `source_hash` on disk were NOT modified by this tick; the discrepancies are logged as audit signals only.

The new `/source.pdf` drift on `si-zm-2009-042` is classified separately from the AKN-HTML cohort and labelled `zambialii_source_pdf_first_observation_drift` in `gaps.md`. Recommendation in that entry is operator triage before any cohort-wide assumption is updated — one observation is not yet a pattern.

## Audit trail — b0670 halt diagnostic carried into this commit

This commit includes, in addition to b0671's own artefacts, the b0670 HALT diagnostic that was written to disk on 2026-05-15T11:37:00Z but never committed (per BRIEF.md step 6 "do not commit on integrity fail" — interpreted by b0670 as no-commit-at-all-of-the-tick). The b0670 diagnostic comprises:

- `reports/batch-0670.md`, `reports/batch-0670-reverify.json`
- `error-reports/2026-05-15T113700Z-b0670-check3-fail.md` (the 15-record truncated-hash inventory)
- An append block to `gaps.md` (the 1 CHECK#3 fail entry + 4 routine AKN-HTML drift entries)
- Append lines to `worker.log`, `costs.log`, `provenance.log`

Including the b0670 diagnostic in this commit is **not** a remediation of the defect — it is the audit trail being made visible in git so Peter can see the prior halt without having to pull a dirty working tree. The 15-record defect remains unresolved and continues to await human triage.

## Approvals

- `phase_8_nightly_reverify.approved` = true (unchanged)
- `phase_8_nightly_reverify.complete` = false (unchanged — Phase 8 is a continuous nightly cycle, not a one-shot)
- `approvals.yaml` was **not** modified by this tick

## Budget

- Today's fetches before tick: 88/2000 (after b0670 at 11:37Z; b0670 fetched 8 although it halted — those bytes left the wire)
- Today's fetches after tick: 96/2000
- Daily-budget headroom after tick: 1904
- LLM tokens: 0 (deterministic pipeline)
- Bandwidth: ~1.6 MB down (largest: loz-plant-pests-and-diseases-act ≈ 607 KB; smallest: si-zm-2009-042 ≈ 173 KB? no — `act-zm-2014-006` at 38,805 B was the smallest)

## Next

- Next Phase 8 tick will continue the nightly sampling cycle (different seed → different 8 records).
- The 15-record `parliament-pdf-v1.2` truncated-hash defect remains a latent ~6% per-tick CHECK#3 hazard. Independent of that, the new `zambialii_source_pdf_first_observation_drift` signal on `si-zm-2009-042` should be confirmed (or refuted) by operator inspection before any cohort-classification update.
- Cumulative Phase 8 drift signal across b0641…b0671 remains: 1 new `/source.pdf` first-observation drift this tick + the multi-batch AKN-HTML dynamic-render cohort. Static PDFs on parliament.gov.zm, media.zambialii.org, and zambialii.org (no `www`) AKN `/source.pdf` continue to dominate the match column.
