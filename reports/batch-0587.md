# Batch 0587 — Phase 8 Nightly Re-verification (2026-05-11)

**UTC start:** 2026-05-11T09:04:36Z
**UTC end:** 2026-05-11T09:05:07Z
**Worker:** worker-tick (Phase 8)
**Phase:** phase_8_nightly_reverify (approved 2026-05-06; sample_rate 0.01)
**Parser:** phase8-reverify-0.1.0 (functional contract per scripts/batch_0546_phase8_reverify.py)
**Tick scope:** Thirty-first Phase 8 tick overall; third worker-tick of UTC date 2026-05-11
   (b0585 at 07:30:21Z and b0586 at 08:38:42Z were the first two worker-ticks of the day).
**Execution mode:** inline runner (`/tmp/b0587_phase8_reverify.py`, NOT committed)
   per sandbox-session safety constraint maintained since b0548 (b0548..b0586
   precedent). Functional contract matches `scripts/batch_0546_phase8_reverify.py`
   baseline including the `scripts/certs/*.pem` PKI loader behaviour (loaded
   on first run — no retry pass needed this tick). Differences from baseline:
   tick-suffixed seed `phase8-reverify-2026-05-11-b0587`, plus
   match_truncated_prefix classifier (already present in b0585/b0586 inline runners).

## Pre-tick git state observation

Pre-tick `git pull --ff-only` returned `Already up to date` at HEAD=476893f
(b0586). The default `.git/index.lock` and `.git/HEAD.lock` cleanup remain
constrained on this sandbox by `Operation not permitted` virtiofs semantics;
the same single warning about an unremovable `.git/objects/maintenance.lock`
backup file surfaced again with no effect on pull semantics. The pre-tick
index still carries the stale staged paths inherited from a prior session
(deleted: reports/batch-0585.md, reports/batch-0585-reverify.json,
reports/batch-0586.md, reports/batch-0586-reverify.json; modified:
costs.log, provenance.log, worker.log, gaps.md). All those files exist in
HEAD and on disk; the staged "deleted" claims contradict on-disk state.
This tick commits b0587's intended files via a per-PID alt-index path
(`GIT_INDEX_FILE=/tmp/b0587-commit-index`) reset to HEAD per b0579..b0586
alt-index precedent, leaving the regular index untouched.

## Inputs

- Pool size: **1884** (records with non-empty `source_url` AND non-empty
  `source_hash`; +4 from b0586's 1880 — consistent with b0584's Court of
  Appeal additions arriving in the records tree).
- Seed: `phase8-reverify-2026-05-11-b0587` (tick-suffixed).
- Sample size: **8** (= MAX_BATCH cap; ceil(0.01 × 1884) = 19 → capped at 8).
- Out-of-band re-fetches: **0** (parliament.gov.zm fetches succeeded
  first-pass because the inline runner pre-loaded
  `scripts/certs/rapidssl_tls_rsa_ca_g1.pem` via `EXTRA_CERTS_DIR`, per
  b0586's standing PKI recommendation).

## Results — 5 match / 3 drift / 0 truncated_prefix / 0 fetch_error

| Verdict | Count | Records |
|---------|------:|---------|
| match (real) | 5 | act-zm-2014-002-the-service-commissions-amendment-act-2014-act-no-2-of-2014 (parliament.gov.zm `/documents/amendment_act/` 158,307 B — FIRST observation of `/amendment_act/` URL sub-path in the 31-tick Phase-8 series; previously only `/acts/` and `/sites/default/files/documents/acts/` were seen); si-zm-2022-053-financial-intelligence-centre-prescribed-threshold-regulations-2022 (zambialii akn `/source.pdf` 665,588 B — extends Act/SI `/source.pdf` stable-PDF cohort to 23/23); act-zm-2000-021-estate-agents-act-no-21-of-2000 (parliament.gov.zm `/acts/` 556,318 B); act-zm-2010-017-the-engineering-institute-of-zambia-2010 (parliament.gov.zm `/acts/` 907,072 B); local-courts-administration-of-estates-rules-1969 (commons.laws.africa `/akn/zm/act/si/1969/297/media/publication/zm-act-si-1969-297-publication-document.pdf` 778,394 B — FIRST observation of `commons.laws.africa` host in the Phase-8 series and FIRST observation of the laws-africa `/media/publication/` URL pattern) |
| match_truncated_prefix | 0 | — |
| drift | 3 | act-zm-1970-064-trusts-restriction-act-1970 (zambialii.org/akn/zm/act/1970/64/eng@1996-12-31 78,468 B — fits AKN-HTML drift cohort, mid-century Act); act-zm-1967-045-inquiries-act-1967 (zambialii.org/akn/zm/act/1967/45/eng@1996-12-31 76,432 B — fits AKN-HTML drift cohort, mid-century Act, second 1960s-Act observation after b0586 act-zm-1968-005); si-zm-2020-079-electoral-process-local-government-by-elections-election-date-and-time-of-poll-no-8-order-2020 (zambialii.org/akn/zm/act/si/2020/79 bare-AKN-path 39,502 B — **SIXTH bare-AKN-path drift observation** after b0579 si-zm-2023-041, b0581 si-zm-2019-014, b0582 si-zm-2023-009, b0585 si-zm-2008-024, b0586 si-zm-2021-112; sub-cohort remains SI-only) |
| fetch_error | 0 | — |

## TLS / CA-chain note

Both parliament.gov.zm fetches (act-zm-2014-002 and act-zm-2010-017
plus act-zm-2000-021) verified successfully on first attempt because the
inline runner's `build_ssl_context()` already loaded the on-disk
`scripts/certs/rapidssl_tls_rsa_ca_g1.pem` into the trust store at startup
(per the b0586 standing recommendation #4). No retry pass needed. The
combined CA bundle pattern is now codified in the inline runner; future
phase-8 ticks should continue to import the same `EXTRA_CERTS_DIR` loader
to avoid the b0586 first-pass `CERTIFICATE_VERIFY_FAILED` failure mode.

## Cohort-level cumulative tally (post-b0587, 31 ticks)

| Cohort | Pre-b0587 | Δ b0587 | Post-b0587 |
|--------|----------:|--------:|-----------:|
| zambialii.org/akn/.../act-or-SI-HTML drift | 96/96 | +2/+2 | 98/98 |
| zambialii.org/akn/.../source.pdf match (Acts/SIs) | 22/22 | +1/+1 | 23/23 |
| zambialii.org/akn/.../source.pdf match (Judgments) | 1/1 | 0/0 | 1/1 |
| media.zambialii.org/media/legislation/ legacy-PDF match | 2/2 | 0/0 | 2/2 |
| commons.laws.africa /media/publication/ legacy-PDF match | 0/0 | +1/+1 | 1/1 § |
| parliament.gov.zm static PDF match (real-match) | 85/85 | +2/+2 | 87/87 |
| parliament.gov.zm /amendment_act/ static PDF match | 0/0 | +1/+1 | 1/1 § |
| parliament.gov.zm static PDF real DRIFT | 0/88 | 0/+3 | 0/91 |
| parliament.gov.zm static PDF truncated_stored_hash_false_drift | 4/88 | 0/0 | 4/91 |
| zambialii judgment-akn HTML drift | 8/16 | 0/0 | 8/16 |
| zambialii bare-AKN-path drift (SI sub-cohort) | 5/5 | +1/+1 | 6/6 |
| Parliament-node landing | 0/1 | 0/0 | 0/1 |
| Stable-PDF combined supercohort (parliament + zambialii akn /source.pdf + media.zambialii legacy + commons.laws.africa + parliament /amendment_act/) — real-drift basis | 109/113 | +5/+5 | 114/118 ‡ |

§ NEW URL-pattern cohorts opened this tick at 1/1 each.
‡ Stable-PDF supercohort now 114/118 across 31 ticks. The 4 cumulative
  non-real-matches remain the four truncated-stored-hash false drifts
  (b0570 act-zm-2020-011; b0578 act-zm-2020-019; b0581 act-zm-2020-016;
  b0585 act-zm-2020-024). **Real drift count on the stable-PDF
  supercohort remains zero across 31 ticks.**

## Notable observations (b0587)

1. **First `commons.laws.africa` host observation in the Phase-8 series.**
   local-courts-administration-of-estates-rules-1969 (Local Courts
   (Administration of Estates) Rules 1969) fetched cleanly from
   `https://commons.laws.africa/akn/zm/act/si/1969/297/media/publication/zm-act-si-1969-297-publication-document.pdf`
   (778,394 B) and the recomputed sha256 matched the stored
   `source_hash` exactly. This is the first time the Phase-8 sampler
   has drawn a record whose `source_url` resolves to the
   `commons.laws.africa` host (a laws-africa publication CDN closely
   related to the AKN tooling used by zambialii). Opens a new cohort
   at 1/1 real-match.

2. **First `parliament.gov.zm/.../amendment_act/` URL sub-path observation.**
   act-zm-2014-002 (Service Commissions (Amendment) Act 2014) fetched
   from `https://www.parliament.gov.zm/sites/default/files/documents/amendment_act/Services%20Commissions%28Amendment%29%20Act%202014.PDF`
   (158,307 B) and matched the stored hash exactly. Previously only
   `/acts/` and `/sites/default/files/documents/acts/` URL sub-paths
   had been seen in the parliament.gov.zm cohort. Opens a new cohort
   at 1/1 real-match.

3. **Mid-century-AKN drift extends.** act-zm-1970-064 (Trusts
   Restriction Act 1970) and act-zm-1967-045 (Inquiries Act 1967) both
   show the AKN-HTML rendering drift via the `/eng@1996-12-31`
   canonical-date suffix — same pipeline-driven, age-independent
   pattern documented in b0576 (act-zm-1966-001) and b0586
   (act-zm-1968-005). The cohort now spans 1966-2025 across 98
   observations with 100% reproduction of the drift mechanism.

4. **Sixth bare-AKN-path drift observation.** si-zm-2020-079
   (Electoral Process — Local Government By-Elections — Election Date
   and Time of Poll (No. 8) Order 2020) joins si-zm-2023-041 (b0579),
   si-zm-2019-014 (b0581), si-zm-2023-009 (b0582), si-zm-2008-024
   (b0585), and si-zm-2021-112 (b0586) in the bare-AKN-path drift
   sub-cohort. All six are SIs with URL form
   `/akn/zm/act/si/<year>/<n>` (no `/eng@<date>` suffix, no
   `/source.pdf` suffix). Acts in the Phase 8 pool continue to use
   `/eng@<date>` form. Sub-cohort remains SI-only at 6 observations.

5. **PKI fix held first-pass.** The inline runner's pre-loaded
   `scripts/certs/rapidssl_tls_rsa_ca_g1.pem` resolved both
   parliament.gov.zm + amendment_act fetches without the b0586-style
   retry pass. Standing recommendation #4 (b0586) is now operationally
   confirmed across two consecutive ticks.

6. **Pre-existing five divergent-content duplicate-ID Act records
   finding REAFFIRMED** — none of b0587 sample IDs are involved:
   act-zm-2025-014, act-zm-2025-028, act-zm-2019-010, act-zm-2020-010,
   act-zm-2018-001 each appear at both `records/acts/<year>/<id>.json`
   AND `records/acts/<id>.json` with divergent content. Operator dedupe
   action recommended (predates b0578).

## Integrity check

Per BRIEF.md §"Integrity checks". For a Phase 8 reverify batch (no record
mutation), the per-tick integrity check is:

- JSON report well-formed and parseable — **PASS**.
- All required summary keys present (batch, phase, parser_version,
  seed, pool_size, sample_size, sample_rate, max_batch, results,
  match_count, drift_count, truncated_prefix_count, fetch_error_count,
  fetches, started_at, completed_at) — **PASS**.
- `sample_size <= MAX_BATCH (8)` — **PASS** (8 <= 8).
- `match_count + drift_count + truncated_prefix_count + fetch_error_count == sample_size` —
  **PASS** (5 + 3 + 0 + 0 = 8).
- All 8 sample IDs resolve to existing rows in `records` table —
  **PASS** (8/8 resolved via sqlite query against a `/tmp/`-copy of
  `corpus.sqlite` per b0583 virtiofs-isolation precedent).
- No sample record file mutated during/after the tick — **PASS** (0/8 mutated; reverify is read-only on records).
- Each result entry contains the required fields (id, type, source_url,
  stored_sha256, fetched_status, verdict, fetched_bytes_len where
  applicable) — **PASS**.
- Each `verdict` is one of {match, drift, fetch_error,
  match_truncated_prefix} — **PASS**.
- Pool size ≥ 1800 (sanity floor) — **PASS** (1884 at sample time).

No record mutation occurred. No new records were written. The three
drift observations are reported analytically; per the 31-tick standing
finding they do NOT indicate corpus integrity failure — they indicate
upstream AKN-HTML rendering-pipeline non-determinism, and the
underlying legal text is unchanged. The stable-PDF supercohort
(114/118 real-matches across 31 ticks; 4 truncated-prefix false
drifts; zero real drifts) continues to demonstrate that the stored
corpus content is faithful to the upstream sources.

## Budget impact

- Fetches this tick: **8** sample-record attempts (4 to zambialii.org at
  5 s between requests, 3 to www.parliament.gov.zm at 2 s between
  requests, 1 to commons.laws.africa at 5 s between requests).
  No retries needed.
- Cumulative today (pre-b0587, on 2026-05-11, worker-tick channel):
  18 / 2000 (from b0586).
- Cumulative today (post-b0587, on 2026-05-11, worker-tick channel):
  **26 / 2000** (1.3%).
- Wall-clock duration: ~31 seconds end-to-end (well within 20-minute cap).

## Outputs

- `reports/batch-0587-reverify.json` (deterministic JSON output).
- `reports/batch-0587.md` (this file).
- Append-only updates to `worker.log`, `costs.log`, `provenance.log`.
- No records written, modified, or deleted.
- No schema or YAML changes.

## Standing recommendations (carried forward — operator decision pending)

1. **Truncated-stored-hash backfill sweep** (b0578/b0579/b0581/b0585
   standing): recompute and re-store full 64-hex `source_hash` for any
   remaining records where `parser_version=parliament-pdf-v1.2` AND
   `source_hash` length is `sha256:` + 16 hex. Cohort has reproduced
   4 times across 31 ticks; underlying raw bytes unchanged.

2. **Phase 8 endpoint refinement** (b0565/b0567/b0569 standing): the
   31-tick pattern shows stable-PDF cohort real-drifts at zero (114/118)
   and AKN-HTML cohort drifts at near-100% (98/98 + 8/16 judgments +
   6/6 bare-AKN-path SIs). Operator action options: (a) move Phase 8
   to text-extraction-stable hashing for HTML endpoints, or (b)
   restrict Phase 8 to stable-PDF endpoints only, or (c) leave as-is
   (drift observations are now well-characterised across 31 ticks).

3. **Divergent-content duplicate-ID Act records** (b0578 standing):
   dedupe the five Act records that appear at both
   `records/acts/<year>/<id>.json` AND `records/acts/<id>.json` with
   divergent content.

4. **Phase 8 inline-runner CA-bundle parity** (b0586 standing,
   confirmed b0587): operationally confirmed across b0586 (with
   retry) and b0587 (first-pass) that loading
   `scripts/certs/rapidssl_tls_rsa_ca_g1.pem` into the SSL context
   eliminates parliament.gov.zm fetch errors. Recommend codifying as
   a shared helper module reused by all phase-8 runners.

None of the above were actioned this tick — Phase 8 reverify worker
is read-only on records by design.
