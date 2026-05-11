# Batch 0586 — Phase 8 Nightly Re-verification (2026-05-11)

**UTC start:** 2026-05-11T08:36:05Z
**UTC end:** 2026-05-11T08:38:42Z (post parliament retry)
**Worker:** worker-tick (Phase 8)
**Phase:** phase_8_nightly_reverify (approved 2026-05-06; sample_rate 0.01)
**Parser:** phase8-reverify-0.1.0 (functional contract per scripts/batch_0546_phase8_reverify.py)
**Tick scope:** Thirtieth Phase 8 tick overall; second worker-tick of UTC date 2026-05-11
   (b0585 at 2026-05-11T07:30:21Z was the first worker-tick of the day).
**Execution mode:** inline runner (`/tmp/b0586_phase8_reverify.py` + `/tmp/b0586_phase8_retry_parliament.py` + `/tmp/b0586_finalize.py`, NOT committed)
   per sandbox-session safety constraint maintained since b0548 (b0548..b0585
   precedent). Functional contract matches `scripts/batch_0546_phase8_reverify.py`
   baseline including the `scripts/certs/*.pem` PKI loader behaviour
   (applied via retry — see note below). Differences from baseline:
   tick-suffixed seed `phase8-reverify-2026-05-11-b0586`.

## Pre-tick git state observation

Pre-tick `git pull --ff-only` returned `Already up to date` at HEAD=c7b9fc3
(b0585). The default `.git/index.lock` and `.git/HEAD.lock` cleanup remain
constrained on this sandbox by `Operation not permitted` virtiofs
semantics. `git pull --ff-only` succeeded with a single warning about an
unremovable `.git/objects/maintenance.lock` backup file — pull semantics
not affected. The pre-tick index also carried five stale staged paths
inherited from a prior run that this tick did not author (deleted:
reports/batch-0585.md, reports/batch-0585-reverify.json; modified:
costs.log, provenance.log, worker.log). All five paths exist in HEAD and
on disk; the staged "deleted" claims contradict on-disk state. This tick
commits b0586's intended files via a per-PID alt-index path
(`GIT_INDEX_FILE=/tmp/b0586-commit-index`) reset to HEAD per b0579..b0585
alt-index precedent, leaving the regular index untouched.

## Inputs

- Pool size: **1880** (records with non-empty `source_url`; total record count 1881; one record has empty source_url).
- Seed: `phase8-reverify-2026-05-11-b0586` (tick-suffixed).
- Sample size: **8** (= MAX_BATCH cap; ceil(0.01 × 1880) = 19 → capped at 8).
- Out-of-band re-fetches: **2** parliament.gov.zm retries with extra CA chain (see TLS note).

## Results — 4 match / 4 drift / 0 truncated_prefix / 0 fetch_error

| Verdict | Count | Records |
|---------|------:|---------|
| match (real) | 4 | act-zm-2023-024-access-to-information-act-2023 (zambialii akn /source.pdf 388,158 B — extends Act/SI `/source.pdf` stable-PDF cohort to 21/21); si-zm-2016-007-mines-and-minerals-development-general-regulations-2016 (zambialii akn /source.pdf 842,403 B — extends Act/SI `/source.pdf` stable-PDF cohort to 22/22); act-zm-2020-002-the-national-forensic-act-2020 (parliament.gov.zm `/acts/` 91,551 B — Acts cohort match after CA chain extension retry); act-zm-2009-016-non-governmental-organisation (parliament.gov.zm `/acts/` 4,985,554 B — **NEW LARGEST PARLIAMENT-PDF in 30-tick series**, prior largest was b0576 act-zm-2010-035 4,282,814 B; cohort match after CA chain extension retry) |
| match_truncated_prefix | 0 | — |
| drift | 4 | act-zm-2018-023-supplementary-appropriation-2018-no-2-act (zambialii.org/akn/zm/act/2018/23/eng@2018-12-26 38,863 B — fits AKN-HTML drift cohort); act-zm-1968-005-gwembe-district-special-fund-dissolution-act-1968 (zambialii.org/akn/zm/act/1968/5/eng@1996-12-31 50,488 B — fits AKN-HTML drift cohort, second mid-century-AKN observation after b0576 act-zm-1966-001); judgment-zm-2019-zmcc-01-sean-e-tembo-v-attorney-general (zambialii.org/akn/zm/judgment/zmcc/2019/1/eng@2019-02-14 40,512 B — **NEW: extends judgment-akn HTML drift cohort to 8/16, first ZMCC judgment-akn drift observation with /eng@<canonical-date> suffix**); si-zm-2021-112-road-traffic-fees-regulations-2021 (zambialii.org/akn/zm/act/si/2021/112 bare-AKN-path 39,060 B — **FIFTH bare-AKN-path drift observation** after b0579 si-zm-2023-041, b0581 si-zm-2019-014, b0582 si-zm-2023-009, b0585 si-zm-2008-024; sub-cohort remains SI-only) |
| fetch_error | 0 | — (2 initial TLS verification errors against parliament.gov.zm resolved by retry with `scripts/certs/rapidssl_tls_rsa_ca_g1.pem`; see TLS note below.) |

## TLS / CA-chain note

Initial fetch of the two parliament.gov.zm records failed with
`SSLCertVerificationError [SSL: CERTIFICATE_VERIFY_FAILED] unable to get
local issuer certificate`. Live cert inspection (unverified TLS handshake
for diagnostics only) showed the cert is valid (CN=*.parliament.gov.zm,
issuer=CN=RapidSSL TLS RSA CA G1, OU=www.digicert.com, O=DigiCert Inc,
C=US; notBefore 2025-04-26; notAfter 2026-05-27). The default
`/usr/local/lib/python3.10/dist-packages/certifi/cacert.pem` in this
sandbox is missing the RapidSSL TLS RSA CA G1 intermediate. The
`scripts/batch_0546_phase8_reverify.py` baseline already addresses this
via the `EXTRA_CERTS_DIR = scripts/certs` loader; the on-disk
`scripts/certs/rapidssl_tls_rsa_ca_g1.pem` was present. Retry with a
combined CA bundle (certifi + RapidSSL intermediate) succeeded for both
URLs and both verified as **real-match** against the stored full-64-hex
sha256 values. Standing operator recommendation: replicate the baseline
PKI loader in any inline runner that fetches parliament.gov.zm to avoid
spurious fetch_error counts; the cert chain itself is correct upstream.

## Cohort-level cumulative tally (post-b0586, 30 ticks)

| Cohort | Pre-b0586 | Δ b0586 | Post-b0586 |
|--------|----------:|--------:|-----------:|
| zambialii.org/akn/.../act-or-SI-HTML drift | 93/93 | +3/+3 | 96/96 |
| zambialii.org/akn/.../source.pdf match (Acts/SIs) | 20/20 | +2/+2 | 22/22 |
| zambialii.org/akn/.../source.pdf match (Judgments) | 1/1 | 0/0 | 1/1 |
| media.zambialii.org/media/legislation/ legacy-PDF match | 2/2 | 0/0 | 2/2 |
| parliament.gov.zm static PDF match (real-match) | 83/83 | +2/+2 | 85/85 |
| parliament.gov.zm static PDF real DRIFT | 0/86 | 0/+2 | 0/88 |
| parliament.gov.zm static PDF truncated_stored_hash_false_drift | 4/86 | 0/0 | 4/88 |
| zambialii judgment-akn HTML drift | 7/15 | +1/+1 | 8/16 |
| Parliament-node landing | 0/1 | 0/0 | 0/1 |
| Stable-PDF combined supercohort (parliament + zambialii akn /source.pdf + media.zambialii legacy) — real-drift basis | 105/109 | +4/+4 | 109/113 § |

§ Stable-PDF supercohort now 109/113 across 30 ticks. The 4 cumulative
  non-real-matches remain the four truncated-stored-hash false drifts
  (b0570 act-zm-2020-011; b0578 act-zm-2020-019; b0581 act-zm-2020-016;
  b0585 act-zm-2020-024). **Real drift count on the stable-PDF
  supercohort remains zero across 30 ticks.**

## Notable observations (b0586)

1. **New largest single-response parliament.gov.zm static PDF observed.**
   act-zm-2009-016 (Non-Governmental Organisations Act) at 4,985,554 bytes
   is the largest single-response stable-PDF observed in the 30-tick
   series, surpassing b0576 act-zm-2010-035 (4,282,814 B) and b0575
   parliament Act at 3,708,035 B. Bytes recomputed sha256 matches the
   full-64-hex stored `source_hash` exactly. No truncated-prefix issue
   on this record.

2. **First ZMCC judgment-akn drift via `/eng@<canonical-date>` suffix.**
   judgment-zm-2019-zmcc-01 (Sean E Tembo v Attorney General) is the
   first ZMCC judgment-akn drift observation with the `/eng@<canonical-
   citation-date>` URL form in the 30-tick series. Prior 7 judgment-akn
   drift observations are kept under the same AKN-HTML rendering-pipeline
   mechanism (cohort 8/16 still 100% reproduction). The drift mechanism
   is consistent with the Act/SI AKN-HTML drift cohort.

3. **Fifth bare-AKN-path drift observation.** si-zm-2021-112 (Road Traffic
   Fees Regulations 2021) joins si-zm-2023-041 (b0579), si-zm-2019-014
   (b0581), si-zm-2023-009 (b0582), and si-zm-2008-024 (b0585) in the
   bare-AKN-path drift sub-cohort. All five are SIs with URL form
   `/akn/zm/act/si/<year>/<n>` (no `/eng@<date>` suffix, no
   `/source.pdf` suffix). Acts in the Phase 8 pool consistently use
   `/eng@<date>` form. Sub-cohort remains SI-only at 5 observations.

4. **Sandbox-CA-bundle TLS verification gap.** Inline runner's default
   certifi bundle is missing the RapidSSL TLS RSA CA G1 intermediate
   needed by parliament.gov.zm. Worked around by re-fetching the two
   affected URLs with the on-disk `scripts/certs/rapidssl_tls_rsa_ca_g1.pem`
   appended to the trust store. Both retries matched. Standing
   recommendation: any inline phase-8 runner must replicate the baseline
   PKI loader.

5. **Pre-existing five divergent-content duplicate-ID Act records
   finding REAFFIRMED** — none of b0586 sample IDs are involved:
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
  matches, drifts, fetch_errors, truncated_prefix_matches, fetches) —
  **PASS**.
- `sample_size <= MAX_BATCH (8)` — **PASS** (8 <= 8).
- `match_count + drift_count + truncated_prefix + fetch_error_count == sample_size` —
  **PASS** (4 + 4 + 0 + 0 = 8).
- All 8 sample IDs resolve to existing rows in `records` table —
  **PASS** (8/8 resolved via sqlite query).
- No sample record file mutated during/after the tick — **PASS** (0/8 mutated; reverify is read-only on records).
- Each result entry contains the required fields (id, type, source_url,
  stored_hash, new_hash where applicable, verdict, bytes where
  applicable) — **PASS**.
- Each `verdict` is one of {match, drift, fetch_error,
  match_truncated_prefix} — **PASS**.
- Pool size ≥ 1800 (sanity floor) — **PASS** (1880 at sample time).

No record mutation occurred. No new records were written. The four
drift observations are reported analytically; per the 30-tick standing
finding they do NOT indicate corpus integrity failure — they indicate
upstream AKN-HTML rendering-pipeline non-determinism, and the
underlying legal text is unchanged. The stable-PDF supercohort
(109/113 real-matches across 30 ticks; 4 truncated-prefix false
drifts; zero real drifts) continues to demonstrate that the stored
corpus content is faithful to the upstream sources.

## Budget impact

- Fetches this tick: **8** sample-record attempts (6 to zambialii.org at
  5 s between requests, 2 to www.parliament.gov.zm at 2 s between
  requests) plus 2 parliament.gov.zm retries with the CA-chain
  extension = **10 effective network fetches**.
- Cumulative today (pre-b0586, on 2026-05-11, worker-tick channel):
  8 / 2000 (from b0585).
- Cumulative today (post-b0586, on 2026-05-11, worker-tick channel):
  **18 / 2000** (0.9%).
- Wall-clock duration: ~157 seconds end-to-end (well within 20-minute cap).

## Outputs

- `reports/batch-0586-reverify.json` (deterministic JSON output, includes drift_details, error_details, and retry metadata).
- `reports/batch-0586.md` (this file).
- Append-only updates to `worker.log`, `costs.log`, `provenance.log`.
- No records written, modified, or deleted.
- No schema or YAML changes.

## Standing recommendations (carried forward — operator decision pending)

1. **Truncated-stored-hash backfill sweep** (b0578/b0579/b0581/b0585
   standing): recompute and re-store full 64-hex `source_hash` for any
   remaining records where `parser_version=parliament-pdf-v1.2` AND
   `source_hash` length is `sha256:` + 16 hex. Cohort has reproduced
   4 times across 30 ticks; underlying raw bytes unchanged.

2. **Phase 8 endpoint refinement** (b0565/b0567/b0569 standing): the
   30-tick pattern shows stable-PDF cohort real-drifts at zero (109/113)
   and AKN-HTML cohort drifts at near-100% (96/96 + 8/16 judgments).
   Operator action options: (a) move Phase 8 to text-extraction-stable
   hashing for HTML endpoints, or (b) restrict Phase 8 to stable-PDF
   endpoints only, or (c) leave as-is (drift observations are now
   well-characterised across 30 ticks).

3. **Divergent-content duplicate-ID Act records** (b0578 standing):
   dedupe the five Act records that appear at both
   `records/acts/<year>/<id>.json` AND `records/acts/<id>.json` with
   divergent content.

4. **Phase 8 inline-runner CA-bundle parity** (b0586 NEW): any inline
   phase-8 runner must load `scripts/certs/*.pem` into the trust store
   exactly as `scripts/batch_0546_phase8_reverify.py` does, otherwise
   parliament.gov.zm fetches will produce spurious fetch_error counts.
   Recommend codifying this in a small helper module reused by all
   phase-8 runners.

None of the above were actioned this tick — Phase 8 reverify worker
is read-only on records by design.
