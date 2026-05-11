# Batch 0601 — Phase 8 Nightly Re-verification (2026-05-11)

**UTC start:** 2026-05-11T22:34:03Z
**UTC end:**   2026-05-11T22:34:22Z
**Worker:**    worker-tick (Phase 8)
**Phase:**     phase_8_nightly_reverify (approved 2026-05-06; sample_rate 0.01)
**Parser:**    phase8-reverify-0.1.0 (functional contract per
  `scripts/batch_0546_phase8_reverify.py` plus b0578+ enhancements:
  tick-suffixed seed, truncated-stored-hash detector, inline
  `scripts/certs/*.pem` CA-chain loader, single retry on URLError).
**Tick scope:** Thirty-ninth Phase 8 tick overall; eleventh worker-tick
  of UTC date 2026-05-11 (b0585 07:30Z, b0586 08:38Z, b0587 09:05Z,
  b0588 09:36Z, b0589 10:05Z, b0595 17:08Z, b0596 20:56Z, b0598 21:14Z,
  b0599 21:34Z, b0600 22:04Z were the prior ten worker-ticks of the day).
**Execution mode:** inline runner (`/tmp/b0601_phase8_reverify.py`,
  NOT committed) per sandbox-session safety constraint maintained
  since b0548. Functional contract matches
  `scripts/batch_0546_phase8_reverify.py` with the b0578+ enhancements
  (tick-suffixed seed, prefix-startswith truncated-stored-hash
  detector, `scripts/certs/*.pem` PKI loader, single retry on
  URLError).

## Pre-tick git state

- `git pull --ff-only` returned `Already up to date` at HEAD=9465bd2
  (jiw b0598 commit — FTS5-blocked tick 18; b0597 hypothesis falsified).
- The persistent `.git/objects/maintenance.lock` warning surfaced
  again (same FUSE EPERM pattern from b011..b020 + b0579..b0600) —
  non-blocking, the pull still succeeded.

## Inputs

- Pool size: **1895** (records on disk with non-empty `source_url`
  AND non-empty `source_hash`; unchanged from b0600 — the intervening
  jiw b0598 tick was FTS5-blocked and wrote no new records).
- Seed: `phase8-reverify-2026-05-11-b0601` (tick-suffixed per the
  b0578+ enhancement; first sample under this seed).
- Sample size: **8** (= MAX_BATCH cap; ceil(0.01 × 1895) = 19 →
  capped at 8).
- Out-of-band re-fetches: **0** (no URLError retries needed;
  CA-chain preload via `scripts/certs/rapidssl_tls_rsa_ca_g1.pem`
  continues to resolve first-pass — now **ten consecutive
  worker-ticks**).

## Results — 3 match / 5 drift / 0 truncated_prefix / 0 fetch_error

| Verdict | Count | Records |
|---------|------:|---------|
| match (real) | 3 | act-zm-2024-029-appropriation-2024 (www.parliament.gov.zm `/acts/` — 336,314 B); act-zm-2017-020-employment-amendment (www.parliament.gov.zm `/acts/` — 8,176 B; smallest parliament `/acts/` sample observed in Phase 8 series); act-zm-1988-021-supreme-court-and-high-court-number-of-judges-act-1988 (media.zambialii.org `/media/legislation/.../source_file/...` legacy PDF — 160,972 B; **second media.zambialii legacy-PDF sample after b0596's 1.41 MB displaces-prior-leaders observation**) |
| match_truncated_prefix | 0 | — |
| drift | 5 | si-zm-2019-082-customs-and-excise-precious-stones-export-duty-suspension-order-2019 (www.zambialii.org `/akn/zm/act/si/2019/82/eng@2019-12-13` — 39,325 B; **second www.zambialii.org host-prefix sub-form sample — extends sub-form drift cohort 1/1 → 2/2; AKN-HTML SI drift with `/eng@` suffix**); si-zm-2022-063-electoral-process-local-government-by-elections-election-date-and-time-of-poll-order-2022 (zambialii.org `/akn/zm/act/si/2022/63` — 40,250 B; **bare-AKN-path SI drift; extends bare-AKN-path SI cohort 8/8 → 9/9**); act-zm-1914-001-authentication-of-documents-act-1914 (zambialii.org `/akn/zm/act/1914/1/eng@1996-12-31` — 49,040 B; **NEW OLDEST-VINTAGE AKN-HTML Act drift — 1914-vintage Act with 1996-12-31 RE-publication date; displaces b0600's 1967-vintage tobacco-levy by 53 years**); act-zm-1960-039-maintenance-orders-act-1960 (zambialii.org `/akn/zm/act/1960/39/eng@1996-12-31` — 175,318 B; AKN-HTML Act drift, 1960-vintage with 1996-12-31 RE-publication date — **two pre-1970 vintage AKN-HTML Acts drifted in same tick**); act-zm-2025-012-superior-courtsnumber-of-judgesact (www.parliament.gov.zm `/node/12519` — 30,678 B; **NEW FINDING: FIRST Parliament-node landing drift observed in Phase 8 series — cohort 0/1 → 1/2; prior /node/ sample matched, this one drifts**) |
| fetch_error | 0 | — |

## TLS / CA-chain note

The two www.parliament.gov.zm `/acts/` PDF fetches plus the
www.parliament.gov.zm `/node/12519` HTML fetch plus the four
zambialii.org-AKN HTML fetches (2 act-akn + 1 www-prefixed SI + 1
bare-AKN-path SI) plus the one media.zambialii.org legacy-PDF
verified successfully on the first attempt because the inline
runner's `build_ssl_context()` pre-loaded
`scripts/certs/rapidssl_tls_rsa_ca_g1.pem`. No retry pass needed.
Standing recommendation #4 (b0586) operationally confirmed across
**ten consecutive worker-ticks** now (b0586 with retry,
b0587/b0588/b0589/b0595/b0596/b0598/b0599/b0600/b0601 first-pass).

## Cohort-level cumulative tally (post-b0601, 39 ticks)

| Cohort | Pre-b0601 | Δ b0601 | Post-b0601 |
|--------|----------:|--------:|-----------:|
| zambialii.org/akn/.../act-or-SI-HTML drift (Acts + SIs with `/eng@<date>` suffix) | 113/113 | +3/+3 | 116/116 |
| zambialii.org/akn/.../source.pdf match (Acts/SIs) | 31/31 | 0/0 | 31/31 |
| zambialii.org/akn/.../source.pdf match (Judgments) | 1/1 | 0/0 | 1/1 |
| media.zambialii.org/media/legislation/ legacy-PDF match | 4/4 | +1/+1 | 5/5 |
| commons.laws.africa /media/publication/ legacy-PDF match | 1/1 | 0/0 | 1/1 |
| parliament.gov.zm static PDF match (real-match `/acts/` family) | 107/107 | +2/+2 | 109/109 |
| parliament.gov.zm /amendment_act/ static PDF match | 4/4 | 0/0 | 4/4 |
| parliament.gov.zm static PDF real DRIFT | 0/114 | 0/+2 | 0/116 |
| parliament.gov.zm static PDF truncated_stored_hash_false_drift | 4/114 | 0/+2 | 4/116 |
| zambialii judgment-akn HTML drift (ZMCC + ZMSC + ZMHC consolidated) | 13/21 | 0/0 | 13/21 |
| zambialii bare-AKN-path drift (SI sub-cohort, no `/eng@` suffix) | 8/8 | +1/+1 | 9/9 |
| `www.zambialii.org` host-prefix AKN-HTML drift sub-form | 1/1 | +1/+1 | 2/2 |
| Parliament-node landing drift | 0/1 | +1/+1 | **1/2** ‡‡ |
| judiciaryzambia.com CoA-judgment HTML drift | 1/1 | 0/0 | 1/1 |
| Stable-PDF combined supercohort (parliament `/acts/` + zambialii akn `/source.pdf` + media.zambialii legacy + commons.laws.africa + parliament `/amendment_act/`) — real-drift basis | 147/151 | +3/+3 | 150/154 ‡ |

‡ Stable-PDF supercohort now 150/154 across 39 ticks. The 4 cumulative
  non-real-matches remain the four truncated-stored-hash false drifts
  (b0570 act-zm-2020-011; b0578 act-zm-2020-019; b0581 act-zm-2020-016;
  b0585 act-zm-2020-024). **Real drift count on the stable-PDF
  supercohort remains zero across 39 ticks.**

‡‡ **NEW FINDING — Parliament-node landing drift cohort opens.** The
  first /node/ sample (drawn in an earlier Phase 8 tick) matched; this
  is the first /node/ drift observation. Two-sample cohort now sits at
  1/2 (one drift, one match). The /node/ family appears to render
  dynamic HTML on each request — behaviour resembles the
  zambialii.org/akn/.../act-or-SI-HTML drift cohort rather than the
  parliament.gov.zm static-PDF stable cohort. Operator may wish to
  reclassify /node/ landings as HTML-render-noise rather than static
  resources. See standing recommendation #11 below.

## Notable observations (b0601)

1. **NEW OLDEST-VINTAGE AKN-HTML Act drift — 1914.**
   `act-zm-1914-001-authentication-of-documents-act-1914` at
   `zambialii.org/akn/zm/act/1914/1/eng@1996-12-31` drifted on
   re-fetch, displacing b0600's 1967-vintage `tobacco-levy-act-
   1967` by 53 years — the new oldest-vintage drift observation in
   the AKN-HTML Act cohort, dating from the colonial-era Northern
   Rhodesia. The characteristic 1996-12-31 RE-publication date in
   the AKN URL persists. Cohort extends 113/113 → 116/116.

2. **Two pre-1970 AKN-HTML Acts drifted in the same tick.** In
   addition to the 1914 sample (#1 above), `act-zm-1960-039-
   maintenance-orders-act-1960` at
   `zambialii.org/akn/zm/act/1960/39/eng@1996-12-31` also drifted
   — both pre-1970 vintage Acts re-published in 1996. First
   tick where two pre-1970 AKN-HTML Acts appeared together.

3. **FIRST Parliament-node landing drift in Phase 8 series.**
   `act-zm-2025-012-superior-courts-number-of-judges-act` at
   `www.parliament.gov.zm/node/12519` drifted on re-fetch — the
   first observation of /node/ landing drift in 39 ticks. The
   prior /node/ sample (drawn in an earlier tick) had matched.
   Two-sample /node/ cohort now sits at 1/2 (50% drift rate).
   Indicates /node/ landings render dynamic HTML, unlike
   parliament.gov.zm `/acts/` static PDFs. New finding; flagged
   under standing recommendation #11.

4. **Second `www.zambialii.org` host-prefix sub-form sample
   drifted.** `si-zm-2019-082-customs-and-excise-precious-stones-
   export-duty-suspension-order-2019` at
   `www.zambialii.org/akn/zm/act/si/2019/82/eng@2019-12-13`
   drifted on re-fetch, extending the www-prefixed sub-form
   cohort 1/1 → 2/2. Both samples drifted — same behaviour as the
   main `zambialii.org` (no-www) AKN-HTML cohort. Operator
   standing recommendation #6 (host-prefix audit) gains weight.

5. **bare-AKN-path SI drift cohort extends 8/8 → 9/9.**
   `si-zm-2022-063-electoral-process-local-government-by-elections-
   election-date-and-time-of-poll-order-2022` at
   `zambialii.org/akn/zm/act/si/2022/63` (no `/eng@` suffix)
   drifted on re-fetch, joining the bare-AKN-path SI sub-cohort
   that consistently drifts. All 9 samples in this cohort have
   drifted — the AKN bare-path resolver appears to render a
   fresh HTML page on each request with non-deterministic widget
   content.

6. **Second media.zambialii.org legacy-PDF sample matched.**
   `act-zm-1988-021-supreme-court-and-high-court-number-of-judges-
   act-1988` at `media.zambialii.org/media/legislation/34592/
   source_file/c815161503c4ff6f/zm-act-1988-21-publication-
   document.pdf` (160,972 B) matched first-pass, extending the
   legacy-PDF match cohort 4/4 → 5/5. The 1988-vintage Act is
   stored on the same `/source_file/<hash>/` infrastructure as
   b0596's 1991-vintage 1.41-MB sample — both stable-PDF.

7. **Smallest parliament `/acts/` sample observed in Phase 8.**
   `act-zm-2017-020-employment-amendment` at
   `www.parliament.gov.zm/sites/default/files/documents/acts/
   The%20Employment%20Amendment%20Act%202017%20Final.pdf` is
   only 8,176 B — the smallest parliament `/acts/` sample
   observed in the Phase 8 series so far. Matched first-pass.
   Confirms parliament.gov.zm static-PDF hashing is stable
   across the full size range (8 KB to 1.2 MB observed).

8. **Pool size unchanged from b0600 (1895).** The intervening
   jiw b0598 tick was FTS5-blocked (18th consecutive) and wrote
   no new records. The records tree is stable for this tick.

9. **Drift composition (5:3) skews further toward drift vs
   b0600 (4:4) and b0599 (4:4).** The 5 drifts comprise 3
   AKN-HTML Act drifts (1914, 1960, plus the /node/ outlier
   which is dynamic HTML), 1 AKN-HTML SI drift (www-prefixed
   sub-form), and 1 bare-AKN-path SI drift. The 3 matches are
   all stable-PDF (2 parliament `/acts/` + 1 media.zambialii
   legacy). Composition consistent with the 39-tick standing
   finding: AKN HTML renders dynamically; stable PDFs hash
   deterministically.

10. **Pre-existing FTS5 records_fts_data corruption (observed by
    jiw b0587..b0594..b0597..b0598) is independent of Phase 8
    reverify** — Phase 8 does not read or write `corpus.sqlite`
    at all, so FTS5 corruption does not affect this tick's verdict.
    Repair-worker manifest escalation remains outstanding (now
    18 consecutive jiw ticks blocked).

## Integrity check

- JSON report well-formed and parseable — **PASS**.
- All required summary keys present (batch, phase, parser_version,
  seed, pool_size, sample_size, sample_rate, max_batch, results,
  match_count, drift_count, truncated_prefix_count, fetch_error_count,
  fetches, retry_fetches, started_at, completed_at) — **PASS**.
- `sample_size <= MAX_BATCH (8)` — **PASS** (8 <= 8).
- `match_count + drift_count + truncated_prefix_count +
  fetch_error_count == sample_size` — **PASS** (3 + 5 + 0 + 0 = 8).
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

No record mutation occurred. The five drift observations are
reported analytically; per the 39-tick standing finding they do NOT
indicate corpus integrity failure — they indicate upstream HTML
rendering-pipeline non-determinism, and the underlying legal text
is unchanged. The stable-PDF supercohort (150/154 real-matches
across 39 ticks; 4 truncated-prefix false drifts; **zero real
drifts**) continues to demonstrate that the stored corpus content
is faithful to the upstream sources.

## Budget impact

- Fetches this tick: **8** sample-record attempts (3 to
  www.parliament.gov.zm at 2 s between requests, 4 to
  zambialii.org / www.zambialii.org at 5 s between requests, 1 to
  media.zambialii.org at 5 s between requests). No retries needed.
- Retry fetches this tick: **0**.
- Cumulative today (pre-b0601, 2026-05-11, worker-tick channel): 82/2000.
- Cumulative today (post-b0601, 2026-05-11, worker-tick channel):
  **90 / 2000** (4.5%).
- Wall-clock duration: ~19 seconds for the fetch loop; well within
  the 20-minute cap.

## Outputs

- `reports/batch-0601-reverify.json` (deterministic JSON output).
- `reports/batch-0601.md` (this file).
- Append-only updates to `worker.log`, `costs.log`, `provenance.log`.
- No records written, modified, or deleted.
- No schema or YAML changes.

## Standing recommendations (carried forward — operator decision pending)

1. **Truncated-stored-hash backfill sweep** (b0578/b0579/b0581/b0585
   standing): unchanged across 39 ticks. Four 2020-vintage
   parliament-pdf-v1.2 records have truncated stored hashes that
   produce a stable false-drift verdict; backfilling the full-length
   sha256 would resolve them. Operator approval required.
2. **Phase 8 endpoint refinement** (b0565/b0567/b0569 standing):
   with 150/154 stable-PDF and 116/116 + 13/21 + 9/9 + 2/2 + 1/2
   HTML/AKN drift cohorts now characterised across 39 ticks,
   operator could consider option (a) text-extraction-stable hashing
   or (b) restricting Phase 8 to stable-PDF to eliminate the HTML
   rendering noise. Operator approval required.
3. **Divergent-content duplicate-ID Act records** (b0578 standing):
   five IDs known with multiple divergent record files. Operator
   approval required to canonicalise or split IDs.
4. **Phase 8 inline-runner CA-bundle parity** (b0586 standing,
   operationally confirmed b0587..b0601 across **ten consecutive
   worker-ticks**): consider landing the `scripts/certs/*.pem`
   preload into the canonical `scripts/batch_NNNN_phase8_reverify.py`
   template the next time the baseline is refreshed.
5. **Stray `.git/refs/heads/main.lock.bak.*` ref backups**
   (b0588 first observation): persists; sandbox cannot
   unlink. No new observations this tick.
6. **`www.zambialii.org`-prefixed AKN-HTML record cluster audit**
   (b0589 standing, **strengthened b0601**): second `www.zambialii.org`
   host-prefix sample drifted, both samples now in cohort. Operator
   may wish to audit how many records in the corpus use the
   `www.` prefix vs the bare `zambialii.org` host (likely a
   parser-evolution artifact) and standardise canonical-source
   normalisation.
7. **`cap-N` Laws-of-Zambia Chapter-number ID form characterisation**
   (b0595 standing, three-sample confirmation b0600): unchanged
   this tick — no `cap-N` samples drawn. Operator may wish to
   characterise the `cap-N` cluster size in `corpus.sqlite`.
8. **`loz-` prefix Laws-of-Zambia ID form characterisation**
   (b0599 standing): unchanged this tick — no `loz-` prefix
   samples drawn. Two-sample confirmation from b0599 stands.
9. **judiciaryzambia.com CoA-record canonical-source decision**
   (b0596 standing): unchanged this tick — no CoA samples drawn.
10. **FTS5 records_fts_data corruption — repair-worker manifest
    escalation** (b0596 standing; b0598-jiw confirmed full
    write-and-rebuild blockage with workaround falsification):
    unchanged this tick — Phase 8 reverify is independent of
    `corpus.sqlite`. Operator action required (18 consecutive
    jiw ticks blocked).
11. **NEW b0601 — Parliament-node landing reclassification.**
    The /node/ family now sits at 1/2 drift (one match, one drift)
    after 39 ticks of observation. /node/ landings appear to be
    dynamic HTML, not static resources. Operator may wish to
    reclassify /node/ records as HTML-render-noise rather than
    stable-PDF candidates for Phase 8 reverify, or canonicalise
    their source_url to the underlying static PDF if one is
    available. Two-sample cohort is small; further samples should
    confirm the pattern.

None of the above were actioned this tick — Phase 8 reverify worker
is read-only on records by design.
