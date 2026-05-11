# Batch 0598 — Phase 8 Nightly Re-verification (2026-05-11)

**UTC start:** 2026-05-11T21:14:43Z
**UTC end:**   2026-05-11T21:15:10Z
**Worker:**    worker-tick (Phase 8)
**Phase:**     phase_8_nightly_reverify (approved 2026-05-06; sample_rate 0.01)
**Parser:**    phase8-reverify-0.1.0 (functional contract per
  `scripts/batch_0546_phase8_reverify.py` plus b0578+ enhancements:
  tick-suffixed seed, truncated-stored-hash detector, inline
  `scripts/certs/*.pem` CA-chain loader, single-retry on URLError).
**Tick scope:** Thirty-sixth Phase 8 tick overall; eighth worker-tick
  of UTC date 2026-05-11 (b0585 07:30Z, b0586 08:38Z, b0587 09:05Z,
  b0588 09:36Z, b0589 10:05Z, b0595 (drawn as b0591) 17:08Z, b0596 20:56Z
  were the prior seven worker-ticks of the day).
**Renumber note:** Originally drew sample as **b0597** at 2026-05-11T21:14:43Z.
  Renumbered **b0597 → b0598** mid-tick due to collision with
  `judgment-ingestion-worker batch-0597-jiw` push at 2026-05-11T21:14:36Z
  (commit `cc16892`, CoA page 8: 0 inserts / 2 deferred FTS5 + 5 deferred OCR).
  Same renumbering precedent as b0585 (b0583→b0585), b0591 (b0591→b0592),
  and b0595 (b0591→b0595). Underlying sample seed
  `phase8-reverify-2026-05-11-b0597` preserved (sample-set
  reproducibility). Report and commit use b0598; results unchanged.
**Execution mode:** inline runner (`/tmp/b0597_phase8_reverify.py`,
  NOT committed) per sandbox-session safety constraint maintained
  since b0548. Functional contract matches
  `scripts/batch_0546_phase8_reverify.py` with the b0578+ enhancements
  (tick-suffixed seed, prefix-startswith truncated-stored-hash
  detector, `scripts/certs/*.pem` PKI loader, single retry on
  URLError).

## Pre-tick git state

- `git pull --ff-only` returned `Already up to date` at HEAD=0165d90
  (Phase 8 b0596 commit).
- The persistent `.git/objects/maintenance.lock` warning surfaced
  again (same FUSE EPERM pattern from b011-b020 + b0579..b0589 +
  b0591/b0595/b0596) — non-blocking, the pull still succeeded.
- Working tree carried untracked stale paths from prior ticks; no
  records-tree mutation.

## Inputs

- Pool size: **1895** (records on disk with non-empty `source_url`
  AND non-empty `source_hash`; unchanged from b0596 — no intervening
  jiw activity between b0596 push 20:57:00Z and b0598 start 21:14:43Z).
- Seed: `phase8-reverify-2026-05-11-b0597` (tick-suffixed — preserved
  across the b0597→b0598 renumber for sample-set reproducibility).
- Sample size: **8** (= MAX_BATCH cap; ceil(0.01 × 1895) = 19 →
  capped at 8).
- Out-of-band re-fetches: **0** (no URLError retries needed;
  CA-chain preload via `scripts/certs/rapidssl_tls_rsa_ca_g1.pem`
  continues to resolve first-pass per the b0587..b0596 confirmed
  pattern — now **seven consecutive worker-ticks**).

## Results — 6 match / 2 drift / 0 truncated_prefix / 0 fetch_error

| Verdict | Count | Records |
|---------|------:|---------|
| match (real) | 6 | act-zm-2023-001-the-national-pension-scheme-amendment-act-2023 (parliament.gov.zm `/.../acts/` 339,920 B — stable-PDF); act-zm-2011-027-income-tax-amendment-act-2011 (parliament.gov.zm `/.../amendment_act/` — first sample of an `/amendment_act/` PDF since b0577; cohort grows to 4/4); act-zm-2025-029-zambia-institute-of-procurement-and-supply-act (parliament.gov.zm `/.../acts/` — **first 2025-vintage parliament `/acts/` sample, stable-PDF**); si-zm-1992-043-factories-plant-inspection-and-examination-fees-regulations-1992 (zambialii.org akn `/source.pdf`); act-zm-2011-018-trades-licensing-repeal-act-2011 (parliament.gov.zm `/.../acts/`); si-zm-2020-082-income-tax-double-taxation-relief-taxes-on-income-the-swiss-confederation-order (zambialii.org akn `/source.pdf`) |
| match_truncated_prefix | 0 | — |
| drift | 2 | act-zm-2007-008-supplementary-appropriation-2005-act (zambialii.org `/akn/zm/act/2007/8/eng@2007-04-13` 0/0 → AKN-HTML Act drift cohort, 2007 vintage); act-zm-2025-004-cyber-crimes-act (zambialii.org `/akn/zm/act/2025/4/eng@2025-04-15` — **first 2025-vintage AKN Act drift observation**, well-known cohort) |
| fetch_error | 0 | — |

## TLS / CA-chain note

The four parliament.gov.zm fetches plus the two zambialii.org-AKN
PDF fetches plus the two zambialii.org-AKN HTML fetches verified
successfully on the first attempt because the inline runner's
`build_ssl_context()` pre-loaded
`scripts/certs/rapidssl_tls_rsa_ca_g1.pem`. No retry pass needed.
Standing recommendation #4 (b0586) operationally confirmed across
**seven consecutive worker-ticks** now (b0586 with retry,
b0587/b0588/b0589/b0595/b0596/b0598 first-pass).

## Cohort-level cumulative tally (post-b0598, 36 ticks)

| Cohort | Pre-b0598 | Δ b0598 | Post-b0598 |
|--------|----------:|--------:|-----------:|
| zambialii.org/akn/.../act-or-SI-HTML drift (Acts + SIs with `/eng@<date>` suffix) | 106/106 | +2/+2 | 108/108 |
| zambialii.org/akn/.../source.pdf match (Acts/SIs) | 28/28 | +2/+2 | 30/30 |
| zambialii.org/akn/.../source.pdf match (Judgments) | 1/1 | 0/0 | 1/1 |
| media.zambialii.org/media/legislation/ legacy-PDF match | 4/4 | 0/0 | 4/4 |
| commons.laws.africa /media/publication/ legacy-PDF match | 1/1 | 0/0 | 1/1 |
| parliament.gov.zm static PDF match (real-match `/acts/` family) | 97/97 | +3/+3 | 100/100 |
| parliament.gov.zm /amendment_act/ static PDF match | 3/3 | +1/+1 | 4/4 |
| parliament.gov.zm static PDF real DRIFT | 0/103 | 0/+4 | 0/107 |
| parliament.gov.zm static PDF truncated_stored_hash_false_drift | 4/103 | 0/0 | 4/107 |
| zambialii judgment-akn HTML drift (ZMCC + ZMSC + ZMHC consolidated) | 11/19 | 0/0 | 11/19 |
| zambialii bare-AKN-path drift (SI sub-cohort, no `/eng@` suffix) | 7/7 | 0/0 | 7/7 |
| `www.zambialii.org` host-prefix AKN-HTML drift sub-form | 1/1 | 0/0 | 1/1 |
| Parliament-node landing | 0/1 | 0/0 | 0/1 |
| judiciaryzambia.com CoA-judgment HTML drift | 1/1 | 0/0 | 1/1 |
| Stable-PDF combined supercohort (parliament `/acts/` + zambialii akn `/source.pdf` + media.zambialii legacy + commons.laws.africa + parliament `/amendment_act/`) — real-drift basis | 133/137 | +6/+6 | 139/143 ‡ |

‡ Stable-PDF supercohort now 139/143 across 36 ticks. The 4 cumulative
  non-real-matches remain the four truncated-stored-hash false drifts
  (b0570 act-zm-2020-011; b0578 act-zm-2020-019; b0581 act-zm-2020-016;
  b0585 act-zm-2020-024). **Real drift count on the stable-PDF
  supercohort remains zero across 36 ticks.**

## Notable observations (b0598)

1. **FIRST 2025-vintage parliament.gov.zm `/acts/` sample.**
   `act-zm-2025-029-zambia-institute-of-procurement-and-supply-act`
   is the first 2025-vintage record drawn from the
   `www.parliament.gov.zm/sites/default/files/documents/acts/` family
   in the Phase 8 series. Verdict: **match**, first-pass. Confirms the
   stable-PDF property holds for the most recent vintage available
   in the corpus on this host. The stable-PDF supercohort extends
   from 97/97 to 100/100 on the `/acts/` family.

2. **FIRST 2025-vintage AKN-HTML Act drift observation.**
   `act-zm-2025-004-cyber-crimes-act` at
   `zambialii.org/akn/zm/act/2025/4/eng@2025-04-15` drifted on
   re-fetch. This is the first 2025-vintage entry in the
   `zambialii.org/akn/.../act-or-SI-HTML drift` cohort, confirming
   that the HTML rendering non-determinism on the AKN page is
   independent of vintage. Cohort extends 106/106 → 108/108.

3. **First sample of parliament `/amendment_act/` PDF family since
   b0577.** `act-zm-2011-027-income-tax-amendment-act-2011` matched
   first-pass. The `/amendment_act/` family is now 4/4 across the
   Phase 8 series. Stable-PDF supercohort gains +1 from the
   `/amendment_act/` strand.

4. **Pool size unchanged from b0596 (1895).** No intervening jiw
   activity in the ~17 minutes between b0596 push 20:57:00Z and
   b0598 start 21:14:43Z. The records tree is stable for this tick.

5. **Drift ratio (2:6) consistent with PDF-heavy sample composition.**
   Two of the eight sampled records were AKN HTML pages; both
   drifted (as expected for the AKN-HTML Act cohort). The six PDF
   samples (4 parliament `/acts/` and `/amendment_act/`, 2 zambialii
   AKN `/source.pdf`) all matched first-pass.

6. **Pre-existing FTS5 records_fts_data corruption (observed by
   jiw b0587..b0594) is independent of Phase 8 reverify** — Phase 8
   does not read or write `corpus.sqlite` at all, so FTS5 corruption
   does not affect this tick's verdict. Repair-worker manifest
   escalation remains outstanding (sixth jiw escalation in record
   as of b0594-jiw; this tick has no jiw activity to add).

## Integrity check

- JSON report well-formed and parseable — **PASS**.
- All required summary keys present (batch, phase, parser_version,
  seed, pool_size, sample_size, sample_rate, max_batch, results,
  match_count, drift_count, truncated_prefix_count, fetch_error_count,
  fetches, retry_fetches, started_at, completed_at) — **PASS**.
- `sample_size <= MAX_BATCH (8)` — **PASS** (8 <= 8).
- `match_count + drift_count + truncated_prefix_count +
  fetch_error_count == sample_size` — **PASS** (6 + 2 + 0 + 0 = 8).
- All 8 sample IDs resolve to existing record files in `records/` —
  **PASS** (8/8 resolved).
- Each result entry contains the required fields — **PASS**.
- Each `verdict` is one of {match, drift, fetch_error,
  match_truncated_prefix} — **PASS**.
- Pool size ≥ 1800 (sanity floor) — **PASS** (1895 at sample time).
- No record mutation occurred this tick — **PASS** (0/8 mutated;
  `git status records/` shows no modified or deleted entries;
  reverify is read-only on records by design).

Note: `PRAGMA integrity_check` against the on-disk `corpus.sqlite`
continues to return `database disk image is malformed` from within
the sandbox copy, matching the b0583+ virtiofs-isolation precedent.
Phase 8 reverify does NOT read or write `corpus.sqlite`, so this
pre-existing condition is informational and does not affect this
tick's integrity verdict.

No record mutation occurred. The two drift observations are
reported analytically; per the 36-tick standing finding they do NOT
indicate corpus integrity failure — they indicate upstream HTML
rendering-pipeline non-determinism, and the underlying legal text
is unchanged. The stable-PDF supercohort (139/143 real-matches
across 36 ticks; 4 truncated-prefix false drifts; **zero real
drifts**) continues to demonstrate that the stored corpus content
is faithful to the upstream sources.

## Budget impact

- Fetches this tick: **8** sample-record attempts (4 to
  www.parliament.gov.zm at 2 s between requests, 4 to zambialii.org
  at 5 s between requests — 2 AKN HTML, 2 AKN `/source.pdf`).
  No retries needed.
- Retry fetches this tick: **0**.
- Cumulative today (pre-b0598, 2026-05-11, worker-tick channel): 58/2000.
- Cumulative today (post-b0598, 2026-05-11, worker-tick channel):
  **66 / 2000** (3.3%).
- Wall-clock duration: ~27 seconds for the fetch loop; ~5 minutes
  overall including report write-up — well within the 20-minute cap.

## Outputs

- `reports/batch-0597-reverify.json` (deterministic JSON output).
- `reports/batch-0597.md` (this file).
- Append-only updates to `worker.log`, `costs.log`, `provenance.log`.
- No records written, modified, or deleted.
- No schema or YAML changes.

## Standing recommendations (carried forward — operator decision pending)

1. **Truncated-stored-hash backfill sweep** (b0578/b0579/b0581/b0585
   standing): unchanged across 36 ticks. Four 2020-vintage
   parliament-pdf-v1.2 records have truncated stored hashes that
   produce a stable false-drift verdict; backfilling the full-length
   sha256 would resolve them. Operator approval required.
2. **Phase 8 endpoint refinement** (b0565/b0567/b0569 standing):
   with 139/143 stable-PDF and 108/108 + 11/19 + 7/7 + 1/1 + 1/1
   HTML/AKN drift cohorts now characterised across 36 ticks,
   operator could consider option (a) text-extraction-stable hashing
   or (b) restricting Phase 8 to stable-PDF to eliminate the HTML
   rendering noise. Operator approval required.
3. **Divergent-content duplicate-ID Act records** (b0578 standing):
   five IDs known with multiple divergent record files. Operator
   approval required to canonicalise or split IDs.
4. **Phase 8 inline-runner CA-bundle parity** (b0586 standing,
   operationally confirmed b0587/b0588/b0589/b0595/b0596/b0598 across
   **seven consecutive worker-ticks**): consider landing the
   `scripts/certs/*.pem` preload into the canonical
   `scripts/batch_NNNN_phase8_reverify.py` template the next time
   the baseline is refreshed.
5. **Stray `.git/refs/heads/main.lock.bak.20260511T092251Z` ref
   backup** (b0588 first observation): persists; sandbox cannot
   unlink. No new observations this tick.
6. **`www.zambialii.org`-prefixed AKN-HTML record cluster audit**
   (b0589 standing): unchanged this tick — operator may wish to
   audit `corpus.sqlite` for the count of
   `source_url LIKE 'https://www.zambialii.org/akn/%'` records to
   characterise the cluster size.
7. **`cap-N` Laws-of-Zambia Chapter-number ID form confirmation**
   (b0595 standing): unchanged this tick. No new `cap-N` samples drawn.
8. **judiciaryzambia.com CoA-record canonical-source decision**
   (b0596 standing): unchanged this tick — no CoA samples drawn.
   1/1 cohort observation from b0596 stands. Operator approval
   required to migrate CoA records to underlying PDF URL.
9. **FTS5 records_fts_data corruption — repair-worker manifest
   escalation** (b0596 standing): unchanged this tick — Phase 8
   reverify is independent of `corpus.sqlite`. Operator action
   required.

None of the above were actioned this tick — Phase 8 reverify worker
is read-only on records by design.
