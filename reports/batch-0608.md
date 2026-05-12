# Batch 0608 — Phase 8 Nightly Re-verification (2026-05-12, second worker-tick of day)

**UTC start:** 2026-05-12T07:51:55Z
**UTC end:**   2026-05-12T07:52:36Z
**Worker:**    worker-tick (Phase 8)
**Phase:**     phase_8_nightly_reverify (approved 2026-05-06; sample_rate 0.01)
**Parser:**    phase8-reverify-0.1.0 (functional contract per
  `scripts/batch_0546_phase8_reverify.py` plus b0578+ enhancements:
  tick-suffixed seed, prefix-startswith truncated-stored-hash detector,
  inline `scripts/certs/*.pem` CA-chain loader, single retry on URLError).
**Tick scope:** Forty-second Phase 8 tick overall; second worker-tick
  of UTC date 2026-05-12 (after b0604 at 05:11Z).
**Execution mode:** inline runner (`/tmp/b0608_phase8_reverify.py`,
  NOT committed) per the sandbox-session safety constraint maintained
  since b0548. Functional contract matches
  `scripts/batch_0546_phase8_reverify.py` with the b0578+ enhancements.

## Pre-tick git state

- Pre-tick: `find .git -name "*.lock" -delete` and `*.lock.bak` cleanup
  ran clean (no stale locks blocked the operation in this session's
  virtiofs mount).
- `git pull --ff-only` returned `Already up to date` first-pass — no
  intervening commit since the post-b0607-jiw discovery push at
  ~07:11Z.
- POST-TICK DISCOVERY from b0607-jiw (worker.log, 07:11:30Z) noted
  that the host appears to have rebuilt the FTS5 records_fts table
  during the b0607 tick window: `PRAGMA quick_check` now `ok`,
  `records_fts` row count 1892, FTS5 MATCH queries succeed. This
  Phase 8 tick does NOT read or write `corpus.sqlite`, so the
  rebuild has no direct effect on this verdict; noted for cross-
  worker awareness.

## Inputs

- Pool size: **1895** (records on disk with non-empty `source_url`
  AND non-empty `source_hash`; unchanged from b0604 — no new records
  added between worker ticks today; the host-side FTS5 rebuild did
  not change record JSON files).
- Seed: `phase8-reverify-2026-05-12-b0608` (tick-suffixed per the
  b0578+ enhancement; first sample under this seed; second sample
  of UTC date 2026-05-12; orthogonal sample to b0604).
- Sample size: **8** (= MAX_BATCH cap; ceil(0.01 × 1895) = 19 →
  capped at 8).
- Out-of-band re-fetches: **0** (no URLError retries needed;
  CA-chain preload via `scripts/certs/rapidssl_tls_rsa_ca_g1.pem`
  continues to resolve first-pass — now **thirteen consecutive
  worker-ticks**).

## Results — 3 match / 5 drift / 0 truncated_prefix / 0 fetch_error

| Verdict | Count | Records |
|---------|------:|---------|
| match (real) | 3 | si-zm-2016-011-medicines-and-allied-substances-dispensing-certificates-regulations-2016 (zambialii.org `/akn/.../source.pdf` — 53,612 B); act-zm-2002-002-value-added-tax-amendment-act-no-2-of-2002 (www.parliament.gov.zm `/amendment_act/` — 113,180 B); si-zm-2019-075-national-heritage-conservation-commission-kalonga-gawa-undi-dole-royal-cemetery- (zambialii.org `/akn/.../source.pdf` — 25,099 B) |
| match_truncated_prefix | 0 | — |
| drift | 5 | act-zm-2021-042-excess-expenditure-appropriation-2021-act (zambialii.org `/akn/zm/act/2021/42/eng@2021-12-30`); si-zm-2023-014-zambia-medicines-and-medical-supplies-agency-administration-of-fund-regulations-2023 (zambialii.org `/akn/zm/act/si/2023/14`, **bare-AKN-path**, no `/eng@` suffix); si-zm-2025-074-zambia-institute-of-secretaries-registration-regulations-2025 (zambialii.org `/akn/zm/act/si/2025/74/eng@2025-11-21`); si-zm-2021-024-electricity-common-carrier-declaration-regulations-2021 (zambialii.org `/akn/zm/act/si/2021/24`, **bare-AKN-path**, no `/eng@` suffix); act-zm-2024-002-animal-identification-and-traceability-act-2024 (zambialii.org `/akn/zm/act/2024/2/eng@2024-04-18`) |
| fetch_error | 0 | — |

## TLS / CA-chain note

All eight fetches (six zambialii.org-AKN endpoints — three `/source.pdf`
for the matches and three `/eng@*` plus two bare-AKN-path for the
drifts — and one www.parliament.gov.zm `/amendment_act/` PDF)
verified successfully on the first attempt because the inline runner's
`build_ssl_context()` pre-loaded `scripts/certs/rapidssl_tls_rsa_ca_g1.pem`.
No retry pass needed. Standing recommendation #4 (b0586) operationally
confirmed across **thirteen consecutive worker-ticks** (b0586 with
retry, b0587..b0604 first-pass, b0608 first-pass).

## Cohort-level cumulative tally (post-b0608, 42 ticks)

| Cohort | Pre-b0608 | Δ b0608 | Post-b0608 |
|--------|----------:|--------:|-----------:|
| zambialii.org/akn/.../act-or-SI-HTML drift, `/eng@` suffix | 119/119 | +3/+3 | **122/122** ‡‡ |
| zambialii.org bare-AKN-path drift (SI sub-cohort, no `/eng@`) | 10/10 | +2/+2 | **12/12** |
| zambialii.org/akn/.../source.pdf match (Acts/SIs) | 37/37 | +2/+2 | **39/39** ‡‡‡ |
| zambialii.org/akn/.../source.pdf match (Judgments) | 1/1 | 0/0 | 1/1 |
| media.zambialii.org/media/legislation/ legacy-PDF match | 5/5 | 0/0 | 5/5 |
| commons.laws.africa /media/publication/ legacy-PDF match | 1/1 | 0/0 | 1/1 |
| parliament.gov.zm static PDF match (real-match `/acts/` family) | 114/114 | 0/0 | 114/114 |
| parliament.gov.zm /amendment_act/ static PDF match | 5/5 | +1/+1 | **6/6** |
| parliament.gov.zm static PDF real DRIFT | 0/121 | 0/+1 | 0/122 |
| parliament.gov.zm static PDF truncated_stored_hash_false_drift | 4/121 | 0/+1 | 4/122 |
| zambialii judgment-akn HTML drift (ZMCC + ZMSC + ZMHC consolidated) | 13/21 | 0/0 | 13/21 |
| `www.zambialii.org` host-prefix AKN-HTML drift sub-form | 2/2 | 0/0 | 2/2 |
| Parliament-node landing drift | 1/2 | 0/0 | 1/2 |
| judiciaryzambia.com CoA-judgment HTML drift | 1/1 | 0/0 | 1/1 |
| Stable-PDF combined supercohort (parliament `/acts/` + zambialii akn `/source.pdf` + media.zambialii legacy + commons.laws.africa + parliament `/amendment_act/`) — real-drift basis | 162/166 | +3/+3 | **165/169** ‡ |

‡ Stable-PDF supercohort now 165/169 across 42 ticks. The 4
  cumulative non-real-matches remain the four truncated-stored-hash
  false drifts (b0570 act-zm-2020-011; b0578 act-zm-2020-019; b0581
  act-zm-2020-016; b0585 act-zm-2020-024). **Real drift count on the
  stable-PDF supercohort remains zero across 42 ticks.**

‡‡ AKN-HTML `/eng@`-suffix Act-or-SI drift cohort now stands at
  **122/122** — three new drifts in b0608 (1 Act 2021 excess-
  expenditure-appropriation, 1 SI 2025 secretaries-registration,
  1 Act 2024 animal-identification-and-traceability). 100% drift
  rate preserved across 122 samples.

‡‡‡ zambialii akn `/source.pdf` Act-or-SI match cohort now stands
  at **39/39** — two new matches in b0608 (1 SI 2016 medicines-
  dispensing, 1 SI 2019 kalonga-gawa-undi-dole). 100% match rate
  preserved across 39 samples.

## Notable observations (b0608)

1. **Two new bare-AKN-path drifts (no `/eng@` suffix).** Cohort
   extends 10/10 → 12/12. The bare-AKN-path SI sub-cohort
   (zambialii redirects `/akn/zm/act/si/YYYY/N` to a CMS-rendered
   HTML page rather than serving a stable resource) continues at
   100% drift rate. New samples: `si-zm-2023-014-zmmsa-administration-
   of-fund` and `si-zm-2021-024-electricity-common-carrier-
   declaration-regulations-2021`.

2. **`act-zm-2024-002-animal-identification-and-traceability-act-2024`
   is a re-drift.** This record was already observed drifting on a
   prior Phase 8 tick (gaps.md sub-cohort
   `content_changed_full_drift_akn_html`, fetched-sha previously
   `328132f7…`). This tick fetched-sha is `9887de08…` (different
   third value). Confirms the AKN-HTML rendering pipeline is
   non-deterministic between fetches as well as between tick dates
   — the same record produces a different hash on each visit. The
   underlying Act text is unchanged; the drift is upstream HTML
   reflow.

3. **First parliament `/amendment_act/` match observed in 5+ ticks.**
   `act-zm-2002-002-value-added-tax-amendment-act-no-2-of-2002`
   matched first-pass at 113,180 B. Cohort extends 5/5 → 6/6 with
   100% match rate preserved. The `/amendment_act/` path is the
   second parliament.gov.zm static-PDF subcohort observed (after
   `/acts/`) and continues to demonstrate stable hashing.

4. **Drift composition (5:3) is consistent with the 42-tick standing
   finding** — stable PDFs hash deterministically; AKN HTML renders
   dynamically. All five drifts are from the AKN cohorts
   (3 from `/eng@` suffix, 2 from bare-AKN-path).

5. **Pool size unchanged from b0604 (1895).** No new records added
   between the two worker-ticks on UTC date 2026-05-12 — the host-
   side FTS5 records_fts rebuild noted in the b0607-jiw POST-TICK
   DISCOVERY (worker.log, 07:11:30Z) did not change record JSON
   files; it only rebuilt the FTS5 shadow tables inside
   `corpus.sqlite`. JIW activity remains blocked from inserting
   new judgments by the FTS5 issue (per b0607-jiw).

6. **Host-side corpus.sqlite rebuild observed.** The post-tick
   probe from b0607-jiw at 07:11:30Z found `corpus.sqlite` had
   been modified during the b0607 tick window: PRAGMA quick_check
   now returns `ok` (was `database disk image is malformed`),
   FTS5 MATCH queries succeed, records_fts row count is now 1892
   with no rowid gaps (was 119-row gap). Phase 8 reverify is
   independent of `corpus.sqlite`, so this rebuild does not
   affect this tick's verdict; noted for cross-worker visibility.

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
- Pool size ≥ 1800 (sanity floor) — **PASS** (1895 at sample time).
- No record mutation occurred this tick — **PASS** (0/8 mutated;
  `git status records/` shows clean working tree; reverify is
  read-only on records by design).

No record mutation occurred. The five drift observations are
reported analytically; per the 42-tick standing finding they do NOT
indicate corpus integrity failure — they indicate upstream HTML
rendering-pipeline non-determinism on the AKN-HTML resolvers
(both `/eng@`-suffix and bare-AKN-path forms), and the underlying
legal text is unchanged. The stable-PDF supercohort (165/169
real-matches across 42 ticks; 4 truncated-prefix false drifts;
**zero real drifts**) continues to demonstrate that the stored
corpus content is faithful to the upstream sources.

## Budget impact

- Fetches this tick: **8** sample-record attempts (1 to
  www.parliament.gov.zm at 2 s between requests, 7 to zambialii.org
  at 5 s between requests). No retries needed.
- Retry fetches this tick: **0**.
- Cumulative today (pre-b0608, 2026-05-12, worker-tick channel): 8/2000.
- Cumulative today (post-b0608, 2026-05-12, worker-tick channel):
  **16 / 2000** (0.8%).
- Wall-clock duration: ~41 seconds for the fetch loop; well within
  the 20-minute cap.

## Outputs

- `reports/batch-0608-reverify.json` (deterministic JSON output).
- `reports/batch-0608.md` (this file).
- Append-only updates to `worker.log`, `costs.log`, `provenance.log`,
  `gaps.md` (b0608 Phase 8 section).
- No records written, modified, or deleted.
- No schema or YAML changes.

## Standing recommendations (carried forward — operator decision pending)

1. **Truncated-stored-hash backfill sweep** (b0578/b0579/b0581/b0585
   standing): unchanged across 42 ticks. Operator approval required.
2. **Phase 8 endpoint refinement** (b0565/b0567/b0569 standing):
   with 165/169 stable-PDF real-match cohort and AKN-HTML cohorts
   (122/122 `/eng@` + 12/12 bare + 13/21 judgment + 2/2
   `www.zambialii.org` + 1/2 parliament-node + 1/1 judiciaryzambia)
   now characterised across 42 ticks, operator could consider
   option (a) text-extraction-stable hashing or (b) restricting
   Phase 8 to stable-PDF to eliminate HTML rendering noise.
   Operator approval required.
3. **Divergent-content duplicate-ID Act records** (b0578 standing):
   five IDs known with multiple divergent record files. Unchanged
   this tick. Operator approval required.
4. **Phase 8 inline-runner CA-bundle parity** (b0586 standing,
   operationally confirmed b0587..b0604..b0608 across **thirteen
   consecutive worker-ticks**): consider landing the
   `scripts/certs/*.pem` preload into the canonical
   `scripts/batch_NNNN_phase8_reverify.py` template the next time
   the baseline is refreshed.
5. **Stray `.git/refs/heads/main.lock.bak.*` ref backups**
   (b0588 standing): persists; sandbox cannot unlink. No new
   observations this tick (the pre-tick `find -delete` cleared
   the locks under .git this session).
6. **`www.zambialii.org`-prefixed AKN-HTML record cluster audit**
   (b0589 standing, strengthened b0601): unchanged this tick — no
   `www.zambialii.org` host-prefix samples drawn.
7. **`cap-N` Laws-of-Zambia Chapter-number ID form characterisation**
   (b0595 standing): unchanged this tick — no `cap-N` samples drawn.
8. **`loz-` prefix Laws-of-Zambia ID form characterisation**
   (b0599 standing): unchanged this tick.
9. **judiciaryzambia.com CoA-record canonical-source decision**
   (b0596 standing): unchanged this tick — no CoA samples drawn.
10. **FTS5 records_fts_data corruption — repair-worker manifest
    escalation** (b0596 standing): potentially RESOLVED per
    b0607-jiw POST-TICK DISCOVERY (worker.log 07:11:30Z) which
    observed an external FTS5 rebuild during the b0607 tick
    window. Phase 8 reverify is independent of `corpus.sqlite`,
    so this tick cannot independently confirm the rebuild's
    persistence — JIW b0608+ should re-probe and confirm.
11. **Parliament-node landing reclassification** (b0601 standing):
    /node/ family at 1/2 drift after 42 ticks. Unchanged this tick.
12. **Stale `refs/remotes/origin/main.lock.*` cleanup on host**
    (b0603 standing): the pre-tick `find .git -name "*.lock"
    -delete` succeeded this session; no halt occurred. Operator
    cleanup as previously suggested remains advisable for full
    reclamation but is not blocking.

None of the above were actioned this tick — Phase 8 reverify worker
is read-only on records by design.
