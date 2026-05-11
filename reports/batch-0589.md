# Batch 0589 — Phase 8 Nightly Re-verification (2026-05-11)

**UTC start:** 2026-05-11T10:04:56Z
**UTC end:** 2026-05-11T10:05:18Z
**Worker:** worker-tick (Phase 8)
**Phase:** phase_8_nightly_reverify (approved 2026-05-06; sample_rate 0.01)
**Parser:** phase8-reverify-0.1.0 (functional contract per scripts/batch_0546_phase8_reverify.py)
**Tick scope:** Thirty-third Phase 8 tick overall; fifth worker-tick of UTC date
  2026-05-11 (b0585 at 07:30:21Z, b0586 at 08:38:42Z, b0587 at 09:05:07Z,
  b0588 at 09:36:34Z were the prior four worker-ticks of the day).
**Execution mode:** inline runner (`/tmp/scratch/b0589_phase8_reverify.py`,
  NOT committed) per sandbox-session safety constraint maintained since b0548.
  Functional contract matches `scripts/batch_0546_phase8_reverify.py`
  including the `scripts/certs/*.pem` PKI loader. Tick-suffixed seed
  `phase8-reverify-2026-05-11-b0589`.

## Pre-tick git state

- `git pull --ff-only` returned `Already up to date` at HEAD=8de061e (b0588).
- A persistent `.git/objects/maintenance.lock` warning surfaced again (same
  FUSE EPERM pattern from b011-b020 + b0579..b0588) — non-blocking, the pull
  still succeeded.
- Working tree carried untracked stale paths and a modified `worker.log` from
  the standing append-only logging contract; no records-tree mutation.

## Inputs

- Pool size: **1891** (records on disk with non-empty `source_url` AND
  non-empty `source_hash`; unchanged from b0588 — no jiw batch landed
  between b0588 and b0589).
- Seed: `phase8-reverify-2026-05-11-b0589` (tick-suffixed).
- Sample size: **8** (= MAX_BATCH cap; ceil(0.01 × 1891) = 19 → capped at 8).
- Out-of-band re-fetches: **0** (no parliament.gov.zm SSL retries needed;
  CA-chain preload via `scripts/certs/rapidssl_tls_rsa_ca_g1.pem` continues
  to resolve first-pass per the b0587/b0588 confirmed pattern).

## Results — 6 match / 2 drift / 0 truncated_prefix / 0 fetch_error

| Verdict | Count | Records |
|---------|------:|---------|
| match (real) | 6 | si-zm-2024-065-income-tax-gopa-infra-gmbh-approval-and-exemption-order-2024 (zambialii.org `/akn/zm/act/si/2024/65/eng@2024-10-17/source.pdf` 3,776,199 B — redirects to media.zambialii.org legacy-PDF host, real match); act-zm-2012-006-the-persons-with-disabilities-act-2012 (parliament.gov.zm `/sites/default/files/documents/acts/` 1,273,209 B — stable-PDF supercohort); si-zm-2017-007-legal-practitioners-conveyancing-and-non-contentious-matters-costs-order-2017 (zambialii.org `/akn/zm/act/si/2017/7/eng@2017-01-20/source.pdf` 143,636 B — redirects to media.zambialii.org); act-zm-2010-019-the-forfeiture-of-proceeds-of-crime-2010 (parliament.gov.zm `/.../acts/` 1,584,410 B); act-zm-2013-013-the-weights-and-measures-amendment-2013 (parliament.gov.zm `/.../documents/amendment_act/` 14,949 B — **THIRD `parliament.gov.zm/.../amendment_act/` URL sub-path observation**, cohort 2/2 → 3/3 — pattern reproducibility now confirmed across three observations); act-zm-2024-030-antiterrorism-nonproliferation-2024 (parliament.gov.zm `/.../acts/` 484,097 B — 2024 vintage parliament Act, no truncated-prefix concern) |
| match_truncated_prefix | 0 | — |
| drift | 2 | act-zm-1988-029-sports-council-of-zambia-act-1988 (zambialii.org `/akn/zm/act/1988/29/eng@1996-12-31` 137,298 B — AKN-HTML drift cohort); si-zm-2019-079-medicines-and-allied-substances-marketing-authorisation-of-medicines (www.zambialii.org `/akn/zm/act/si/2019/79/eng@2019-11-22` 41,061 B — AKN-HTML drift, **NEW SUB-FORM: `www.zambialii.org` host with `/eng@<date>` SI URL** — distinct from the SI bare-AKN-path drift cohort of 7) |
| fetch_error | 0 | — |

## TLS / CA-chain note

Both parliament.gov.zm fetches (act-zm-2012-006, act-zm-2010-019,
act-zm-2013-013, act-zm-2024-030) verified successfully on first attempt
because the inline runner's `build_ssl_context()` pre-loaded
`scripts/certs/rapidssl_tls_rsa_ca_g1.pem`. No retry pass needed.
Standing recommendation #4 (b0586) operationally confirmed across four
consecutive ticks now (b0586 with retry, b0587/b0588/b0589 first-pass).

## Cohort-level cumulative tally (post-b0589, 33 ticks)

| Cohort | Pre-b0589 | Δ b0589 | Post-b0589 |
|--------|----------:|--------:|-----------:|
| zambialii.org/akn/.../act-or-SI-HTML drift (Acts + SIs with `/eng@<date>` suffix) | 102/102 | +2/+2 | 104/104 |
| zambialii.org/akn/.../source.pdf match (Acts/SIs) | 23/23 | +2/+2 | 25/25 |
| zambialii.org/akn/.../source.pdf match (Judgments) | 1/1 | 0/0 | 1/1 |
| media.zambialii.org/media/legislation/ legacy-PDF match | 3/3 | 0/0 | 3/3 |
| commons.laws.africa /media/publication/ legacy-PDF match | 1/1 | 0/0 | 1/1 |
| parliament.gov.zm static PDF match (real-match `/acts/` family) | 87/87 | +3/+3 | 90/90 |
| parliament.gov.zm /amendment_act/ static PDF match | 2/2 | +1/+1 | 3/3 |
| parliament.gov.zm static PDF real DRIFT | 0/92 | 0/+4 | 0/96 |
| parliament.gov.zm static PDF truncated_stored_hash_false_drift | 4/92 | 0/0 | 4/96 |
| zambialii judgment-akn HTML drift | 9/17 | 0/0 | 9/17 |
| zambialii bare-AKN-path drift (SI sub-cohort, no `/eng@` suffix) | 7/7 | 0/0 | 7/7 |
| Parliament-node landing | 0/1 | 0/0 | 0/1 |
| Stable-PDF combined supercohort (parliament `/acts/` + zambialii akn `/source.pdf` + media.zambialii legacy + commons.laws.africa + parliament `/amendment_act/`) — real-drift basis | 116/120 | +6/+6 | 122/126 ‡ |

‡ Stable-PDF supercohort now 122/126 across 33 ticks. The 4 cumulative
  non-real-matches remain the four truncated-stored-hash false drifts
  (b0570 act-zm-2020-011; b0578 act-zm-2020-019; b0581 act-zm-2020-016;
  b0585 act-zm-2020-024). **Real drift count on the stable-PDF
  supercohort remains zero across 33 ticks.**

## Notable observations (b0589)

1. **Third `parliament.gov.zm/.../amendment_act/` URL sub-path observation.**
   act-zm-2013-013 (Weights and Measures (Amendment) Act 2013) fetched
   cleanly from
   `/sites/default/files/documents/amendment_act/Weights%20and%20Measures%20%28Amendment%29%20Act%202013.PDF`
   (14,949 B) and matched the stored hash exactly. The `/amendment_act/`
   sub-path opened by b0587's act-zm-2014-002 and reproduced by b0588's
   act-zm-2015-006 is now confirmed reproducible at 3/3 real-match —
   the sub-path is a stable parliament endpoint, not a one-off.

2. **NEW SUB-FORM AKN-HTML drift: `www.zambialii.org` host with `/eng@<date>`
   SI URL.** si-zm-2019-079 uses `www.zambialii.org/akn/zm/act/si/2019/79/eng@2019-11-22`
   (with the `www.` host prefix). This is distinct from:
   - The bare-AKN-path SI sub-cohort (7 of 7) which has NO `/eng@<date>`
     suffix and is hosted on `zambialii.org` (no `www.`).
   - The mainline AKN-HTML drift cohort which is hosted on
     `zambialii.org` (no `www.`) with `/eng@<date>` suffix.
   The fetch followed a redirect from `www.zambialii.org` → `zambialii.org`
   (final URL `https://zambialii.org/akn/zm/act/si/2019/79/eng@2019-11-22`);
   drift mechanism is the same AKN-HTML rendering non-determinism, but the
   `www.` host prefix in the stored `source_url` is a new sub-form for
   this series. Pool likely contains a small `www.zambialii.org` cluster
   recoverable by future audits.

3. **2024-vintage parliament Act real-match confirmation.** act-zm-2024-030
   (Anti-Terrorism and Non-Proliferation Act 2024) verifies that 2024-vintage
   parliament `/acts/` PDFs do NOT exhibit the 2020-vintage truncated-prefix
   false-drift pattern (per the 4 known cases all from 2020). The
   truncated-prefix anomaly remains a 2020-cohort-specific concern.

4. **High match-to-drift ratio (6:2) this tick complements b0588's 2:6.**
   Across the two ticks the combined sample (16 records) gave 8 match / 8 drift,
   which is closer to the underlying pool's stable-PDF-vs-AKN-HTML proportion
   than either tick taken alone. The two-tick combined view is consistent with
   no real corpus drift.

5. **Pre-existing five divergent-content duplicate-ID Act records finding
   REAFFIRMED** — none of b0589 sample IDs are involved.

## Integrity check

- JSON report well-formed and parseable — **PASS**.
- All required summary keys present (batch, phase, parser_version, seed,
  pool_size, sample_size, sample_rate, max_batch, results, match_count,
  drift_count, truncated_prefix_count, fetch_error_count, fetches,
  retry_fetches, started_at, completed_at) — **PASS**.
- `sample_size <= MAX_BATCH (8)` — **PASS** (8 <= 8).
- `match_count + drift_count + truncated_prefix_count + fetch_error_count == sample_size` —
  **PASS** (6 + 2 + 0 + 0 = 8).
- All 8 sample IDs resolve to existing record files in `records/` — **PASS** (8/8 resolved).
- Each result entry contains the required fields — **PASS**.
- Each `verdict` is one of {match, drift, fetch_error, match_truncated_prefix} — **PASS**.
- Pool size ≥ 1800 (sanity floor) — **PASS** (1891 at sample time).
- No record mutation occurred this tick — **PASS** (0/8 mutated;
  `git status records/` shows no modified or deleted entries; reverify is
  read-only on records by design).

Note: `PRAGMA integrity_check` against the on-disk `corpus.sqlite` continues
to return `database disk image is malformed` from within the sandbox copy,
matching the b0583+ virtiofs-isolation precedent. Phase 8 reverify does NOT
read or write `corpus.sqlite`, so this pre-existing condition is
informational and does not affect this tick's integrity verdict.

No record mutation occurred. The two drift observations are reported
analytically; per the 33-tick standing finding they do NOT indicate
corpus integrity failure — they indicate upstream AKN-HTML rendering-pipeline
non-determinism, and the underlying legal text is unchanged. The stable-PDF
supercohort (122/126 real-matches across 33 ticks; 4 truncated-prefix false
drifts; zero real drifts) continues to demonstrate that the stored corpus
content is faithful to the upstream sources.

## Budget impact

- Fetches this tick: **8** sample-record attempts (4 to www.parliament.gov.zm
  at 2 s between requests, 3 to zambialii.org / www.zambialii.org at 5 s
  between requests, 0 to media.zambialii.org direct (the two zambialii.org
  `/akn/.../source.pdf` fetches followed redirects to media.zambialii.org but
  count against the originating zambialii.org host limit), 1 to
  www.zambialii.org at 5 s between requests). No retries needed.
- Retry fetches this tick: **0**.
- Cumulative today (pre-b0589, 2026-05-11, worker-tick channel): 34 / 2000.
- Cumulative today (post-b0589, 2026-05-11, worker-tick channel):
  **42 / 2000** (2.1%).
- Wall-clock duration: ~22 seconds for the fetch loop; ~5 minutes overall
  including report write-up — well within the 20-minute cap.

## Outputs

- `reports/batch-0589-reverify.json` (deterministic JSON output).
- `reports/batch-0589.md` (this file).
- Append-only updates to `worker.log`, `costs.log`, `provenance.log`.
- No records written, modified, or deleted.
- No schema or YAML changes.

## Standing recommendations (carried forward — operator decision pending)

1. **Truncated-stored-hash backfill sweep** (b0578/b0579/b0581/b0585
   standing): unchanged across 33 ticks. Four 2020-vintage parliament-pdf-v1.2
   records have truncated stored hashes that produce a stable false-drift
   verdict; backfilling the full-length sha256 would resolve them. Operator
   approval required.
2. **Phase 8 endpoint refinement** (b0565/b0567/b0569 standing): with
   122/126 stable-PDF and 104/104 + 9/17 + 7/7 AKN-HTML drifts now
   characterised across 33 ticks, operator could consider option (a)
   text-extraction-stable hashing or (b) restricting Phase 8 to stable-PDF
   to eliminate the AKN-HTML-rendering noise. Operator approval required.
3. **Divergent-content duplicate-ID Act records** (b0578 standing): five
   IDs known with multiple divergent record files. Operator approval
   required to canonicalise or split IDs.
4. **Phase 8 inline-runner CA-bundle parity** (b0586 standing, operationally
   confirmed b0587/b0588/b0589 across FOUR consecutive ticks): consider
   landing the `scripts/certs/*.pem` preload into the canonical
   `scripts/batch_NNNN_phase8_reverify.py` template the next time the
   baseline is refreshed.
5. **Stray `.git/refs/heads/main.lock.bak.20260511T092251Z` ref backup**
   (b0588 first observation): persists; sandbox cannot unlink. No new
   observations this tick.
6. **NEW (b0589): possible `www.zambialii.org`-prefixed AKN-HTML record
   cluster** — si-zm-2019-079 is the first sample with this host prefix in
   the 33-tick series. Operator may wish to audit `corpus.sqlite` for the
   count of `source_url LIKE 'https://www.zambialii.org/akn/%'` records to
   characterise the cluster size, since the host prefix is a recoverable
   indicator that could be normalised in a future canonicalisation pass.

None of the above were actioned this tick — Phase 8 reverify worker is
read-only on records by design.
