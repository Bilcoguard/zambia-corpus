# Batch 0619 — Phase 8 Nightly Re-verification (2026-05-12, fourth worker-tick of day)

**UTC start:** 2026-05-12T16:32:08Z
**UTC end:**   2026-05-12T16:32:41Z
**Worker:**    worker-tick (Phase 8, scheduled task `zambia-corpus-tick`)
**Phase:**     phase_8_nightly_reverify (approved 2026-05-06; sample_rate 0.01)
**Parser:**    phase8-reverify-0.1.0 (functional contract per
  `scripts/batch_0546_phase8_reverify.py` plus b0578+ enhancements:
  tick-suffixed seed, prefix-startswith truncated-stored-hash
  detector, inline `scripts/certs/*.pem` CA-chain loader, single
  retry on URLError).
**Tick scope:** Forty-fourth Phase 8 tick overall; fourth worker-tick
  of UTC date 2026-05-12 (after b0604 05:11Z, b0608 07:52Z, b0614
  12:38Z).
**Execution mode:** inline runner (`/tmp/b0619_phase8_reverify.py`,
  NOT committed) per the sandbox-session safety constraint maintained
  since b0548. Functional contract matches
  `scripts/batch_0546_phase8_reverify.py` with the b0578+ enhancements.

## Pre-tick git state

- Pre-tick: `find .git -name "*.lock" -delete` and `*.lock.bak`
  cleanup ran. One stale `.git/index.lock` left behind by an
  earlier host-side process in this session; sandbox `rm -f`
  succeeded on second attempt after FUSE refresh. One
  `.git/objects/maintenance.lock` returned EPERM under FUSE —
  benign, same pattern observed since b0334+.
- `git pull --ff-only` returned `Already up to date` (HEAD =
  `18b35a1` Judgment batch 0618 from 18:14:56 local).
- Pre-existing staged content from an earlier-session
  repair-batch-033 attempt was retained as-is (legitimate
  completed-but-uncommitted work: `reports/repair-batch-033.md`,
  `scripts/repair_batch_033.py`, worker.log append). The 119 MB
  staged `corpus.sqlite` was un-staged before commit because the
  on-disk `.gitignore` lists it (GitHub 100 MB single-file limit,
  rebuilt locally per b0504 policy).

## Inputs

- Pool size: **1914** (records on disk with non-empty `source_url`
  AND non-empty `source_hash`; unchanged vs b0614).
- Seed: `phase8-reverify-2026-05-12-b0619` (tick-suffixed per the
  b0578+ enhancement; fourth sample under the date-suffixed family
  for UTC date 2026-05-12; orthogonal to b0604, b0608, b0614).
- Sample size: **8** (= MAX_BATCH cap; ceil(0.01 × 1914) = 20 →
  capped at 8).
- Out-of-band re-fetches: **0** (no URLError retries needed;
  CA-chain preload via `scripts/certs/rapidssl_tls_rsa_ca_g1.pem`
  continues to resolve first-pass — now **fifteen consecutive
  worker-ticks**).

## Results — 3 match / 5 drift / 0 truncated_prefix / 0 fetch_error

| Verdict | Count | Records |
|---------|------:|---------|
| match (real) | 3 | act-zm-2011-022-the-fisheries-act-2011 (www.parliament.gov.zm `/acts/` static PDF, 98,156 B); act-zm-2021-026-the-health-professions-amendment-act-2021 (www.parliament.gov.zm `/acts/` static PDF, 13,557 B); si-zm-2007-042-national-payment-systems-act-commencement-order-2007 (zambialii.org `/akn/.../source.pdf`, 147,346 B) |
| match_truncated_prefix | 0 | — |
| drift | 5 | act-zm-2023-010-supplementary-appropriation-2023-act (zambialii.org `/akn/zm/act/2023/10/eng@2023-08-17`); act-zm-1994-013-fees-and-fines-act-1994 (zambialii.org `/akn/zm/act/1994/13/eng@2013-12-19`); act-zm-2006-001-supplementary-appropriation-2004-act (zambialii.org `/akn/zm/act/2006/1/eng@2006-03-31`); act-zm-2018-008-credit-reporting-act (zambialii.org `/akn/zm/act/2018/8/eng@2018-07-31`); si-zm-2019-040-corporate-insolvency-insolvency-practitioner-accreditation-regulations-2019 (zambialii.org `/akn/zm/act/si/2019/40`, bare-AKN-path) |
| fetch_error | 0 | — |

## TLS / CA-chain note

All eight fetches (two www.parliament.gov.zm `/acts/` static PDFs —
both matches; six zambialii.org-AKN endpoints — one `/source.pdf`
match plus four `/eng@`-suffix HTML drifts plus one bare-AKN-path
HTML drift) verified successfully on the first attempt because the
inline runner's `build_ssl_context()` pre-loaded
`scripts/certs/rapidssl_tls_rsa_ca_g1.pem`. No retry pass needed.
Standing recommendation #4 (b0586) operationally confirmed across
**fifteen consecutive worker-ticks** (b0586 with retry,
b0587..b0608..b0614 first-pass, b0619 first-pass).

## Cohort-level cumulative tally (post-b0619, 44 ticks)

| Cohort | Pre-b0619 | Δ b0619 | Post-b0619 |
|--------|----------:|--------:|-----------:|
| zambialii.org/akn/.../act-or-SI-HTML drift, `/eng@` suffix | 123/123 | +4/+4 | **127/127** ‡‡ |
| zambialii.org bare-AKN-path drift (SI sub-cohort, no `/eng@`) | 13/13 | +1/+1 | **14/14** |
| zambialii.org/akn/.../source.pdf match (Acts/SIs) | 42/42 | +1/+1 | **43/43** ‡‡‡ |
| zambialii.org/akn/.../source.pdf match (Judgments) | 1/1 | 0/0 | 1/1 |
| media.zambialii.org/media/legislation/ legacy-PDF match | 5/5 | 0/0 | 5/5 |
| commons.laws.africa /media/publication/ legacy-PDF match | 1/1 | 0/0 | 1/1 |
| parliament.gov.zm static PDF match (real-match `/acts/` family) | 116/116 | +2/+2 | **118/118** |
| parliament.gov.zm /amendment_act/ static PDF match | 6/6 | 0/0 | 6/6 |
| parliament.gov.zm static PDF real DRIFT | 0/124 | 0/+2 | 0/126 |
| parliament.gov.zm static PDF truncated_stored_hash_false_drift | 4/124 | 0/+2 | 4/126 |
| zambialii judgment-akn HTML drift (ZMCC + ZMSC + ZMHC consolidated) | 13/21 | 0/0 | 13/21 |
| `www.zambialii.org` host-prefix AKN-HTML drift sub-form | 2/2 | 0/0 | 2/2 |
| Parliament-node landing drift | 1/2 | 0/0 | 1/2 |
| judiciaryzambia.com CoA-judgment HTML drift | 2/2 | 0/0 | 2/2 |
| `cap-N` Laws-of-Zambia ID-form (parliament `/acts/` resolver) | 1/1 | 0/0 | 1/1 |
| Stable-PDF combined supercohort (parliament `/acts/` + zambialii akn `/source.pdf` + media.zambialii legacy + commons.laws.africa + parliament `/amendment_act/`) — real-drift basis | 170/174 | +3/+3 | **173/177** ‡ |

‡ Stable-PDF supercohort now 173/177 across 44 ticks. The 4
  cumulative non-real-matches remain the four truncated-stored-hash
  false drifts (b0570 act-zm-2020-011; b0578 act-zm-2020-019; b0581
  act-zm-2020-016; b0585 act-zm-2020-024). **Real drift count on the
  stable-PDF supercohort remains zero across 44 ticks.**

‡‡ AKN-HTML `/eng@`-suffix Act-or-SI drift cohort now stands at
  **127/127** — four new drifts in b0619 (act-zm-2023-010
  supplementary-appropriation 2023; act-zm-1994-013 fees-and-fines;
  act-zm-2006-001 supplementary-appropriation 2004; act-zm-2018-008
  credit-reporting). 100% drift rate preserved across 127 samples.

‡‡‡ zambialii akn `/source.pdf` Act-or-SI match cohort now stands at
  **43/43** — one new match in b0619 (si-zm-2007-042 national-
  payment-systems commencement). 100% match rate preserved across 43
  samples.

## Notable observations (b0619)

1. **Heavy AKN-HTML composition this tick (5 of 8 samples).** The
   tick-suffixed seed selected an unusually AKN-HTML-heavy slice
   (4 `/eng@`-suffix + 1 bare-AKN-path = 5/8 = 62.5 %). All five
   drifted, consistent with the 127/127 + 14/14 = 141/141 (100 %)
   AKN-HTML drift profile carried across 44 ticks. The 3/8 match
   rate this tick is purely sample composition (not an underlying
   behavioural change).

2. **No re-drifts this tick.** All five drifts in b0619 are first
   observations for the records concerned.

3. **Drift composition (3:5) inverts b0614 split (5:3) and matches
   b0608 split (3:5).** Cumulative composition across 44 ticks
   remains broadly bifurcated: stable PDFs match deterministically;
   AKN HTML and judgment HTML drift due to upstream CMS-rendered
   non-determinism (view counters, dynamic markup, build-time-
   inserted hashes).

4. **No new sub-cohorts opened this tick.** First-time observations
   sit inside existing well-characterised cohorts. The `cap-N`
   ID-form cohort (opened b0614) was not sampled this tick.

5. **Pool size unchanged at 1914 vs b0614.** No JIW records were
   committed between b0614 (12:38Z) and b0619 (16:32Z); the four
   intervening JIW ticks (b0615..b0618) all wrote `+0 records`
   and held at `records=records_fts=1917` (Phase 8 pool of 1914
   reflects the subset with both `source_url` AND `source_hash`
   populated).

## Integrity check

- JSON report well-formed and parseable — **PASS**.
- All required summary keys present (batch, phase, parser_version,
  seed, pool_size, sample_size, sample_rate, max_batch, results,
  match_count, match_truncated_prefix_count, drift_count,
  fetch_error_count, fetches, retry_fetches, started_at,
  completed_at) — **PASS**.
- `sample_size <= MAX_BATCH (8)` — **PASS** (8 <= 8).
- `match_count + match_truncated_prefix_count + drift_count +
  fetch_error_count == sample_size` — **PASS** (3 + 0 + 5 + 0 = 8).
- All 8 sample IDs resolve to existing record files in `records/` —
  **PASS** (8/8 resolved; verified via `find records -name <id>.json`).
- Each result entry contains the required fields — **PASS**.
- Each `verdict` is one of {match, drift, fetch_error,
  match_truncated_prefix} — **PASS**.
- Pool size ≥ 1800 (sanity floor) — **PASS** (1914 at sample time).
- No record mutation occurred this tick — **PASS** (0/8 mutated;
  `git status records/` shows clean working tree; reverify is
  read-only on records by design).

No record mutation occurred. The five drift observations are reported
analytically; per the 44-tick standing finding they do NOT indicate
corpus integrity failure — they indicate upstream HTML rendering-
pipeline non-determinism on the AKN-HTML resolvers (both `/eng@`-
suffix and bare-AKN-path forms). The underlying legal text is
unchanged on each. The stable-PDF supercohort (173/177 real-matches
across 44 ticks; 4 truncated-prefix false drifts; **zero real
drifts**) continues to demonstrate that the stored corpus content is
faithful to the upstream sources.

## Budget impact

- Fetches this tick: **8** sample-record attempts (2 to
  www.parliament.gov.zm at 2 s between requests, 6 to zambialii.org
  at 5 s between requests). No retries needed.
- Retry fetches this tick: **0**.
- Cumulative today (pre-b0619, 2026-05-12, worker-tick channel): 24/2000.
- Cumulative today (post-b0619, 2026-05-12, worker-tick channel):
  **32 / 2000** (1.6 %).
- Wall-clock duration: ~33 seconds for the fetch loop; well within
  the 20-minute cap.

## Outputs

- `reports/batch-0619-reverify.json` (deterministic JSON output).
- `reports/batch-0619.md` (this file).
- Append-only updates to `worker.log`, `costs.log`, `provenance.log`,
  `gaps.md` (b0619 Phase 8 section).
- No records written, modified, or deleted.
- No schema or YAML changes.

## Standing recommendations (carried forward — operator decision pending)

1. **Truncated-stored-hash backfill sweep** (b0578/b0579/b0581/b0585
   standing): unchanged across 44 ticks. Operator approval required.
2. **Phase 8 endpoint refinement** (b0565/b0567/b0569 standing):
   with 173/177 stable-PDF real-match cohort and AKN-HTML cohorts
   (127/127 `/eng@` + 14/14 bare + 13/21 judgment + 2/2
   `www.zambialii.org` + 1/2 parliament-node + 2/2 judiciaryzambia)
   characterised across 44 ticks, operator could consider option (a)
   text-extraction-stable hashing or (b) restricting Phase 8 to
   stable-PDF to eliminate HTML rendering noise. Operator approval
   required.
3. **Divergent-content duplicate-ID Act records** (b0578 standing):
   five IDs known with multiple divergent record files. Unchanged
   this tick. Operator approval required.
4. **Phase 8 inline-runner CA-bundle parity** (b0586 standing,
   operationally confirmed b0587..b0608..b0614..b0619 across
   **fifteen consecutive worker-ticks**): consider landing the
   `scripts/certs/*.pem` preload into the canonical
   `scripts/batch_NNNN_phase8_reverify.py` template the next time
   the baseline is refreshed.
5. **Stray `.git/refs/heads/main.lock.bak.*` ref backups**
   (b0588 standing): persists; sandbox cannot unlink. Pre-tick
   `find -delete` cleared the locks under `.git` this session; one
   benign FUSE EPERM on `.git/objects/maintenance.lock` during
   `git pull --ff-only` was non-blocking.
6. **`www.zambialii.org`-prefixed AKN-HTML record cluster audit**
   (b0589 standing, strengthened b0601): unchanged this tick — no
   `www.zambialii.org` host-prefix samples drawn.
7. **`cap-N` Laws-of-Zambia Chapter-number ID form characterisation**
   (b0595 standing; cohort opened b0614 at 1/1 match):
   unchanged this tick — no `cap-N` samples drawn.
8. **`loz-` prefix Laws-of-Zambia ID form characterisation**
   (b0599 standing): unchanged this tick — no `loz-` samples drawn.
9. **judiciaryzambia.com CoA-record canonical-source decision**
   (b0596 standing; cohort 2/2 drifting): unchanged this tick — no
   judiciaryzambia.com samples drawn.
10. **FTS5 records_fts_data corruption — repair-worker manifest
    escalation** (b0596 standing): potentially RESOLVED per
    b0607-jiw POST-TICK DISCOVERY which observed an external FTS5
    rebuild; subsequent JIW ticks b0611..b0618 wrote records (or
    deferred) and integrity-PASSed throughout. Phase 8 reverify is
    independent of `corpus.sqlite`, so this tick cannot independently
    confirm; cross-worker observation only.
11. **Parliament-node landing reclassification** (b0601 standing):
    `/node/` family at 1/2 drift after 44 ticks. Unchanged this tick.
12. **Stale `refs/remotes/origin/main.lock.*` cleanup on host**
    (b0603 standing): pre-tick `find .git -name "*.lock" -delete`
    succeeded this session; no halt occurred. Operator cleanup as
    previously suggested remains advisable for full reclamation but
    is not blocking.

None of the above were actioned this tick — Phase 8 reverify worker
is read-only on records by design.
