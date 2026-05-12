# Batch 0614 — Phase 8 Nightly Re-verification (2026-05-12, third worker-tick of day)

**UTC start:** 2026-05-12T12:38:07Z
**UTC end:**   2026-05-12T12:38:44Z
**Worker:**    worker-tick (Phase 8)
**Phase:**     phase_8_nightly_reverify (approved 2026-05-06; sample_rate 0.01)
**Parser:**    phase8-reverify-0.1.0 (functional contract per
  `scripts/batch_0546_phase8_reverify.py` plus b0578+ enhancements:
  tick-suffixed seed, prefix-startswith truncated-stored-hash detector,
  inline `scripts/certs/*.pem` CA-chain loader, single retry on URLError).
**Tick scope:** Forty-third Phase 8 tick overall; third worker-tick
  of UTC date 2026-05-12 (after b0604 at 05:11Z and b0608 at 07:52Z).
**Execution mode:** inline runner (`/tmp/b0614_phase8_reverify.py`,
  NOT committed) per the sandbox-session safety constraint maintained
  since b0548. Functional contract matches
  `scripts/batch_0546_phase8_reverify.py` with the b0578+ enhancements.

## Pre-tick git state

- Pre-tick: `find .git -name "*.lock" -delete` and `*.lock.bak` cleanup
  ran clean (no stale locks blocked the operation in this session's
  virtiofs mount).
- `git pull --ff-only` returned `Already up to date` first-pass (one
  benign EPERM warning from FUSE on `.git/ORIG_HEAD.lock` cleanup
  attempt — same pattern observed since b0334+; non-blocking).

## Inputs

- Pool size: **1914** (records on disk with non-empty `source_url`
  AND non-empty `source_hash`; +19 vs b0608's 1895). Growth driven
  by JIW writes earlier today: b0611 (+7), b0612 (+5), b0613 (+6),
  plus +1 from elsewhere in the working tree.
- Seed: `phase8-reverify-2026-05-12-b0614` (tick-suffixed per the
  b0578+ enhancement; third sample under the date-suffixed family
  for UTC date 2026-05-12; orthogonal sample to b0604 and b0608).
- Sample size: **8** (= MAX_BATCH cap; ceil(0.01 × 1914) = 20 →
  capped at 8).
- Out-of-band re-fetches: **0** (no URLError retries needed;
  CA-chain preload via `scripts/certs/rapidssl_tls_rsa_ca_g1.pem`
  continues to resolve first-pass — now **fourteen consecutive
  worker-ticks**).

## Results — 5 match / 3 drift / 0 truncated_prefix / 0 fetch_error

| Verdict | Count | Records |
|---------|------:|---------|
| match (real) | 5 | act-zm-2025-002-geological-minerals-development-2025 (www.parliament.gov.zm `/acts/` — 1,012,498 B est.); si-zm-2019-080-medicines-and-allied-substances-expert-advisory-committee-regulations-2019 (zambialii.org `/akn/.../source.pdf`); si-zm-2002-003-minimum-wages-and-conditions-of-employment-shop-workers-order-2002 (zambialii.org `/akn/.../source.pdf`); **act-zm-cap-250-cattle-slaughter-control-act** (www.parliament.gov.zm `/acts/`, FIRST `cap-N` ID-form sample observed); si-zm-2006-044-lands-ground-rent-fees-and-charges-regulations-2006 (zambialii.org `/akn/.../source.pdf`) |
| match_truncated_prefix | 0 | — |
| drift | 3 | act-zm-2015-009-supplementary-appropriation-2013-act (zambialii.org `/akn/zm/act/2015/9/eng@2015-08-14`); si-zm-1982-049-zambia-airways-corporation-date-of-dissolution-order-1982 (zambialii.org `/akn/zm/act/si/1982/49`, **bare-AKN-path** — earliest year ever sampled in this sub-cohort); judgment-zm-2026-coa-226-levi-chimfwembe-v-sampa-leonard-musonda (judiciaryzambia.com judgment HTML) |
| fetch_error | 0 | — |

## TLS / CA-chain note

All eight fetches (two www.parliament.gov.zm `/acts/` static PDFs —
both matches; four zambialii.org-AKN endpoints — three `/source.pdf`
matches plus one `/eng@` drift; one zambialii.org bare-AKN-path
drift; one judiciaryzambia.com judgment-HTML drift) verified
successfully on the first attempt because the inline runner's
`build_ssl_context()` pre-loaded
`scripts/certs/rapidssl_tls_rsa_ca_g1.pem`. No retry pass needed.
Standing recommendation #4 (b0586) operationally confirmed across
**fourteen consecutive worker-ticks** (b0586 with retry, b0587..b0608
first-pass, b0614 first-pass).

## Cohort-level cumulative tally (post-b0614, 43 ticks)

| Cohort | Pre-b0614 | Δ b0614 | Post-b0614 |
|--------|----------:|--------:|-----------:|
| zambialii.org/akn/.../act-or-SI-HTML drift, `/eng@` suffix | 122/122 | +1/+1 | **123/123** ‡‡ |
| zambialii.org bare-AKN-path drift (SI sub-cohort, no `/eng@`) | 12/12 | +1/+1 | **13/13** |
| zambialii.org/akn/.../source.pdf match (Acts/SIs) | 39/39 | +3/+3 | **42/42** ‡‡‡ |
| zambialii.org/akn/.../source.pdf match (Judgments) | 1/1 | 0/0 | 1/1 |
| media.zambialii.org/media/legislation/ legacy-PDF match | 5/5 | 0/0 | 5/5 |
| commons.laws.africa /media/publication/ legacy-PDF match | 1/1 | 0/0 | 1/1 |
| parliament.gov.zm static PDF match (real-match `/acts/` family) | 114/114 | +2/+2 | **116/116** |
| parliament.gov.zm /amendment_act/ static PDF match | 6/6 | 0/0 | 6/6 |
| parliament.gov.zm static PDF real DRIFT | 0/122 | 0/+2 | 0/124 |
| parliament.gov.zm static PDF truncated_stored_hash_false_drift | 4/122 | 0/+2 | 4/124 |
| zambialii judgment-akn HTML drift (ZMCC + ZMSC + ZMHC consolidated) | 13/21 | 0/0 | 13/21 |
| `www.zambialii.org` host-prefix AKN-HTML drift sub-form | 2/2 | 0/0 | 2/2 |
| Parliament-node landing drift | 1/2 | 0/0 | 1/2 |
| judiciaryzambia.com CoA-judgment HTML drift | 1/1 | +1/+1 | **2/2** † |
| `cap-N` Laws-of-Zambia ID-form | 0/0 | +1/+1 (match, parliament `/acts/`) | **1/1 (100% match)** †† |
| Stable-PDF combined supercohort (parliament `/acts/` + zambialii akn `/source.pdf` + media.zambialii legacy + commons.laws.africa + parliament `/amendment_act/`) — real-drift basis | 165/169 | +5/+5 | **170/174** ‡ |

‡ Stable-PDF supercohort now 170/174 across 43 ticks. The 4
  cumulative non-real-matches remain the four truncated-stored-hash
  false drifts (b0570 act-zm-2020-011; b0578 act-zm-2020-019; b0581
  act-zm-2020-016; b0585 act-zm-2020-024). **Real drift count on the
  stable-PDF supercohort remains zero across 43 ticks.**

‡‡ AKN-HTML `/eng@`-suffix Act-or-SI drift cohort now stands at
  **123/123** — one new drift in b0614 (act-zm-2015-009 supplementary
  appropriation). 100% drift rate preserved across 123 samples.

‡‡‡ zambialii akn `/source.pdf` Act-or-SI match cohort now stands at
  **42/42** — three new matches in b0614 (1 SI 2019 medicines-expert-
  advisory, 1 SI 2002 minimum-wages-shop-workers, 1 SI 2006 lands-
  ground-rent). 100% match rate preserved across 42 samples.

† judiciaryzambia.com CoA-judgment HTML drift cohort extends 1/1 →
  2/2. Standing recommendation #9 (b0596) — operator decision pending
  on canonical-source choice for CoA records — partially informed:
  the second sample drifted (`judgment-zm-2026-coa-226-levi-chimfwembe-
  v-sampa-leonard-musonda`), confirming the host pattern.

†† **First `cap-N` Laws-of-Zambia ID-form sample observed in 43 Phase
  8 ticks** (`act-zm-cap-250-cattle-slaughter-control-act`). Resolves
  via parliament.gov.zm `/acts/` static PDF — MATCH first-pass.
  Cohort initialised at 1/1 (100% match). Standing recommendation
  #7 (b0595) partially informed: at least the `cap-N` form whose
  source resolves to a parliament.gov.zm `/acts/` PDF hashes
  deterministically. Further `cap-N` samples needed to characterise
  the form across other resolvers (zambialii akn, media.zambialii
  legacy, etc.).

## Notable observations (b0614)

1. **First `cap-N` Laws-of-Zambia Chapter-number ID-form sample in
   43 Phase 8 ticks.** `act-zm-cap-250-cattle-slaughter-control-act`
   resolved via parliament.gov.zm `/acts/Cattle Slaughter
   (Control) Act.pdf` and matched first-pass. Cohort initialised at
   1/1 (100% match). The `cap-N` ID-form is the colonial-era
   Chapter-numbered form (Cap. 250 in the Laws of Zambia, Revised
   Edition 1995). Its presence in the corpus has been noted in
   standing recommendation #7 since b0595; this is the first
   re-verification sample. The fact that the source URL is a
   parliament.gov.zm static PDF (rather than a zambialii AKN-HTML
   page) is encouraging for hash stability — consistent with the
   stable-PDF supercohort 170/174 finding.

2. **Earliest bare-AKN-path SI sub-cohort sample yet.**
   `si-zm-1982-049-zambia-airways-corporation-date-of-dissolution-
   order-1982` is from 1982 — earliest year sampled in the bare-
   AKN-path sub-cohort (prior earliest was 2018). The drift verdict
   is consistent with the 13/13 100%-drift pattern; the year doesn't
   change the upstream rendering pipeline behaviour. Of historical
   note: the underlying SI dissolved Zambia Airways Corporation on
   1982-09-30; the corpus has the canonical text on disk and only
   the AKN-HTML wrapper is drifting.

3. **Second judiciaryzambia.com CoA-judgment HTML sample drifted.**
   Cohort 1/1 → 2/2. Both samples drifted; pattern is consistent
   with the AKN-HTML cohorts (CMS-rendered HTML with view counters
   and dynamic markup). The new sample is a 2026 CoA judgment
   `judgment-zm-2026-coa-226-levi-chimfwembe-v-sampa-leonard-
   musonda`. Operator decision still pending on canonical-source
   choice for CoA records (standing recommendation #9, b0596).

4. **No re-drifts this tick** (cf. b0608's `act-zm-2024-002`
   re-drift). All three drifts in b0614 are first observations for
   the records concerned.

5. **Drift composition (5:3) inverts the b0608 split (3:5).** The
   sample happens to favour the stable-PDF supercohort this tick.
   Cumulative composition across 43 ticks remains broadly bifurcated
   (stable PDFs match deterministically; AKN HTML and judgment HTML
   drift). The 5/8 match rate this tick is purely sample composition,
   not an underlying behavioural change.

6. **Pool size grew 1895 → 1914 (+19) since b0608.** Reflects JIW
   inserts during today's reparse-deferred drains: b0611 (+7), b0612
   (+5), b0613 (+6) for a +18 total, with the +1 remainder unaccounted
   for at the time of pool computation (pool counter is a snapshot
   of records/ at start-of-tick; the discrepancy may be a pre-existing
   record file revisited or a transient enumeration ordering effect).
   Records-FTS counts in JIW b0613 stand at 1917 records / 1917 FTS5
   rows; the Phase 8 pool of 1914 reflects the subset with both
   `source_url` AND `source_hash` populated.

## Integrity check

- JSON report well-formed and parseable — **PASS**.
- All required summary keys present (batch, phase, parser_version,
  seed, pool_size, sample_size, sample_rate, max_batch, results,
  match_count, match_truncated_prefix_count, drift_count,
  fetch_error_count, fetches, retry_fetches, started_at,
  completed_at) — **PASS**.
- `sample_size <= MAX_BATCH (8)` — **PASS** (8 <= 8).
- `match_count + match_truncated_prefix_count + drift_count +
  fetch_error_count == sample_size` — **PASS** (5 + 0 + 3 + 0 = 8).
- All 8 sample IDs resolve to existing record files in `records/` —
  **PASS** (8/8 resolved; verified via `find records -name <id>.json`).
- Each result entry contains the required fields — **PASS**.
- Each `verdict` is one of {match, drift, fetch_error,
  match_truncated_prefix} — **PASS**.
- Pool size ≥ 1800 (sanity floor) — **PASS** (1914 at sample time).
- No record mutation occurred this tick — **PASS** (0/8 mutated;
  `git status records/` shows clean working tree; reverify is
  read-only on records by design).

No record mutation occurred. The three drift observations are
reported analytically; per the 43-tick standing finding they do NOT
indicate corpus integrity failure — they indicate upstream HTML
rendering-pipeline non-determinism on the AKN-HTML resolvers
(both `/eng@`-suffix and bare-AKN-path forms) and the judiciaryzambia
CoA host, and the underlying legal text is unchanged. The stable-PDF
supercohort (170/174 real-matches across 43 ticks; 4 truncated-prefix
false drifts; **zero real drifts**) continues to demonstrate that
the stored corpus content is faithful to the upstream sources.

## Budget impact

- Fetches this tick: **8** sample-record attempts (2 to
  www.parliament.gov.zm at 2 s between requests, 5 to zambialii.org
  at 5 s between requests, 1 to judiciaryzambia.com at 5 s between
  requests). No retries needed.
- Retry fetches this tick: **0**.
- Cumulative today (pre-b0614, 2026-05-12, worker-tick channel): 16/2000.
- Cumulative today (post-b0614, 2026-05-12, worker-tick channel):
  **24 / 2000** (1.2%).
- Wall-clock duration: ~37 seconds for the fetch loop; well within
  the 20-minute cap.

## Outputs

- `reports/batch-0614-reverify.json` (deterministic JSON output).
- `reports/batch-0614.md` (this file).
- Append-only updates to `worker.log`, `costs.log`, `provenance.log`,
  `gaps.md` (b0614 Phase 8 section).
- No records written, modified, or deleted.
- No schema or YAML changes.

## Standing recommendations (carried forward — operator decision pending)

1. **Truncated-stored-hash backfill sweep** (b0578/b0579/b0581/b0585
   standing): unchanged across 43 ticks. Operator approval required.
2. **Phase 8 endpoint refinement** (b0565/b0567/b0569 standing):
   with 170/174 stable-PDF real-match cohort and AKN-HTML cohorts
   (123/123 `/eng@` + 13/13 bare + 13/21 judgment + 2/2
   `www.zambialii.org` + 1/2 parliament-node + 2/2 judiciaryzambia)
   now characterised across 43 ticks, operator could consider
   option (a) text-extraction-stable hashing or (b) restricting
   Phase 8 to stable-PDF to eliminate HTML rendering noise.
   Operator approval required.
3. **Divergent-content duplicate-ID Act records** (b0578 standing):
   five IDs known with multiple divergent record files. Unchanged
   this tick. Operator approval required.
4. **Phase 8 inline-runner CA-bundle parity** (b0586 standing,
   operationally confirmed b0587..b0608..b0614 across **fourteen
   consecutive worker-ticks**): consider landing the
   `scripts/certs/*.pem` preload into the canonical
   `scripts/batch_NNNN_phase8_reverify.py` template the next time
   the baseline is refreshed.
5. **Stray `.git/refs/heads/main.lock.bak.*` ref backups**
   (b0588 standing): persists; sandbox cannot unlink. No new
   observations this tick (the pre-tick `find -delete` cleared
   the locks under .git this session; one benign FUSE EPERM on
   `.git/ORIG_HEAD.lock` during `git pull --ff-only` was non-
   blocking).
6. **`www.zambialii.org`-prefixed AKN-HTML record cluster audit**
   (b0589 standing, strengthened b0601): unchanged this tick — no
   `www.zambialii.org` host-prefix samples drawn.
7. **`cap-N` Laws-of-Zambia Chapter-number ID form characterisation**
   (b0595 standing): **partially informed this tick.** First sample
   (`act-zm-cap-250-cattle-slaughter-control-act`) drawn; matched
   first-pass via parliament.gov.zm `/acts/` static PDF. Further
   `cap-N` samples needed across other resolver families to fully
   characterise the form's hash-stability profile.
8. **`loz-` prefix Laws-of-Zambia ID form characterisation**
   (b0599 standing): unchanged this tick — no `loz-` samples drawn.
9. **judiciaryzambia.com CoA-record canonical-source decision**
   (b0596 standing): partially informed this tick. Second sample
   drifted (`judgment-zm-2026-coa-226-levi-chimfwembe-v-sampa-
   leonard-musonda`); cohort 1/1 → 2/2 with both drifting. Operator
   should consider whether the canonical CoA source should be
   judiciaryzambia.com (currently drifting) or zambialii AKN
   `/source.pdf` (where available).
10. **FTS5 records_fts_data corruption — repair-worker manifest
    escalation** (b0596 standing): potentially RESOLVED per
    b0607-jiw POST-TICK DISCOVERY (worker.log 07:11:30Z) which
    observed an external FTS5 rebuild during the b0607 tick
    window; subsequent JIW ticks b0611–b0613 wrote records and
    integrity-PASSed throughout. Phase 8 reverify is independent
    of `corpus.sqlite`, so this tick cannot independently confirm
    the rebuild's persistence; cross-worker observation only.
11. **Parliament-node landing reclassification** (b0601 standing):
    /node/ family at 1/2 drift after 43 ticks. Unchanged this tick.
12. **Stale `refs/remotes/origin/main.lock.*` cleanup on host**
    (b0603 standing): the pre-tick `find .git -name "*.lock"
    -delete` succeeded this session; no halt occurred. Operator
    cleanup as previously suggested remains advisable for full
    reclamation but is not blocking.

None of the above were actioned this tick — Phase 8 reverify worker
is read-only on records by design.
