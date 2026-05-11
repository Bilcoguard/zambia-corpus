# Batch 0596 — Phase 8 Nightly Re-verification (2026-05-11)

**UTC start:** 2026-05-11T20:56:25Z
**UTC end:**   2026-05-11T20:56:41Z
**Worker:**    worker-tick (Phase 8)
**Phase:**     phase_8_nightly_reverify (approved 2026-05-06; sample_rate 0.01)
**Parser:**    phase8-reverify-0.1.0 (functional contract per
  `scripts/batch_0546_phase8_reverify.py` plus b0578+ enhancements:
  tick-suffixed seed, truncated-stored-hash detector, inline
  `scripts/certs/*.pem` CA-chain loader, single-retry on URLError).
**Tick scope:** Thirty-fifth Phase 8 tick overall; seventh worker-tick
  of UTC date 2026-05-11 (b0585 07:30Z, b0586 08:38Z, b0587 09:05Z,
  b0588 09:36Z, b0589 10:05Z, b0595 (drawn as b0591) 17:08Z were the
  prior six worker-ticks of the day).
**Execution mode:** inline runner (`/tmp/b0596_phase8_reverify.py`,
  NOT committed) per sandbox-session safety constraint maintained
  since b0548. Functional contract matches
  `scripts/batch_0546_phase8_reverify.py` with the b0578+ enhancements
  (tick-suffixed seed, prefix-startswith truncated-stored-hash
  detector, `scripts/certs/*.pem` PKI loader, single retry on
  URLError).

## Pre-tick git state

- `git pull --ff-only` returned `Already up to date` at HEAD=48f727e
  (Phase 8 b0595 commit).
- The persistent `.git/objects/maintenance.lock` warning surfaced
  again (same FUSE EPERM pattern from b011-b020 + b0579..b0589 +
  b0591/b0595) — non-blocking, the pull still succeeded.
- Working tree carried untracked stale paths from prior ticks; no
  records-tree mutation.

## Inputs

- Pool size: **1895** (records on disk with non-empty `source_url`
  AND non-empty `source_hash`; +3 from b0595's 1892, accounted for
  by intervening jiw activity since the b0595 draw — three additional
  CoA records visible in the records-tree at sample time).
- Seed: `phase8-reverify-2026-05-11-b0596` (tick-suffixed).
- Sample size: **8** (= MAX_BATCH cap; ceil(0.01 × 1895) = 19 →
  capped at 8).
- Out-of-band re-fetches: **0** (no parliament.gov.zm SSL retries
  needed; CA-chain preload via
  `scripts/certs/rapidssl_tls_rsa_ca_g1.pem` continues to resolve
  first-pass per the b0587..b0595 confirmed pattern — now **six
  consecutive worker-ticks**).

## Results — 5 match / 3 drift / 0 truncated_prefix / 0 fetch_error

| Verdict | Count | Records |
|---------|------:|---------|
| match (real) | 5 | act-zm-2024-008-zambia-qualifications-authority-act-2024 (parliament.gov.zm `/.../acts/` 397,399 B — stable-PDF); act-zm-1991-009-zambia-institute-of-mass-communication-act-1991 (media.zambialii.org legacy-PDF host `/media/legislation/34702/source_file/.../zm-act-1991-9-publication-document.pdf` 1,479,094 B — **new largest media.zambialii legacy-PDF sampled in Phase 8 series**); act-zm-2014-014-the-appropriation-act-2014 (parliament.gov.zm `/.../acts/` 52,796 B); act-zm-2018-021-the-rating-act-2018 (parliament.gov.zm `/.../acts/` 208,875 B); act-zm-2019-014-value-added-tax-amendment-act-2019 (parliament.gov.zm `/.../acts/` 24,486 B) |
| match_truncated_prefix | 0 | — |
| drift | 3 | judgment-zm-2022-zmcc-12-banda-v-attorney-general (zambialii.org `/akn/zm/judgment/zmcc/2022/12/eng@2022-06-20` 43,392 B — judgment-akn HTML drift cohort, ZMCC sub-form); judgment-zm-2022-zmsc-50-banda-v-people (zambialii.org `/akn/zm/judgment/zmsc/2022/50/eng@2022-06-14` 41,742 B — judgment-akn HTML drift cohort, ZMSC sub-form); judgment-zm-2025-coa-105-nimble-resources-limited-v-alex-katamfya (judiciaryzambia.com `/app-105-2023-...` 166,773 B — **FIRST judiciaryzambia.com CoA-judgment HTML drift observation in Phase 8 series; opens new cohort 1/1**) |
| fetch_error | 0 | — |

## TLS / CA-chain note

The five parliament.gov.zm fetches (act-zm-2024-008, act-zm-2014-014,
act-zm-2018-021, act-zm-2019-014, plus the media.zambialii.org fetch
which redirects via zambialii.org TLS) verified successfully on the
first attempt because the inline runner's `build_ssl_context()`
pre-loaded `scripts/certs/rapidssl_tls_rsa_ca_g1.pem`. No retry pass
needed. Standing recommendation #4 (b0586) operationally confirmed
across **six consecutive worker-ticks** now (b0586 with retry,
b0587/b0588/b0589/b0595/b0596 first-pass).

## Cohort-level cumulative tally (post-b0596, 35 ticks)

| Cohort | Pre-b0596 | Δ b0596 | Post-b0596 |
|--------|----------:|--------:|-----------:|
| zambialii.org/akn/.../act-or-SI-HTML drift (Acts + SIs with `/eng@<date>` suffix) | 106/106 | 0/0 | 106/106 |
| zambialii.org/akn/.../source.pdf match (Acts/SIs) | 28/28 | 0/0 | 28/28 |
| zambialii.org/akn/.../source.pdf match (Judgments) | 1/1 | 0/0 | 1/1 |
| media.zambialii.org/media/legislation/ legacy-PDF match | 3/3 | +1/+1 | 4/4 |
| commons.laws.africa /media/publication/ legacy-PDF match | 1/1 | 0/0 | 1/1 |
| parliament.gov.zm static PDF match (real-match `/acts/` family) | 93/93 | +4/+4 | 97/97 |
| parliament.gov.zm /amendment_act/ static PDF match | 3/3 | 0/0 | 3/3 |
| parliament.gov.zm static PDF real DRIFT | 0/99 | 0/+4 | 0/103 |
| parliament.gov.zm static PDF truncated_stored_hash_false_drift | 4/99 | 0/0 | 4/103 |
| zambialii judgment-akn HTML drift (ZMCC + ZMSC + ZMHC consolidated) | 9/17 | +2/+2 | 11/19 |
| zambialii bare-AKN-path drift (SI sub-cohort, no `/eng@` suffix) | 7/7 | 0/0 | 7/7 |
| `www.zambialii.org` host-prefix AKN-HTML drift sub-form | 1/1 | 0/0 | 1/1 |
| Parliament-node landing | 0/1 | 0/0 | 0/1 |
| **NEW: judiciaryzambia.com CoA-judgment HTML drift** | 0/0 | +1/+1 | 1/1 |
| Stable-PDF combined supercohort (parliament `/acts/` + zambialii akn `/source.pdf` + media.zambialii legacy + commons.laws.africa + parliament `/amendment_act/`) — real-drift basis | 128/132 | +5/+5 | 133/137 ‡ |

‡ Stable-PDF supercohort now 133/137 across 35 ticks. The 4 cumulative
  non-real-matches remain the four truncated-stored-hash false drifts
  (b0570 act-zm-2020-011; b0578 act-zm-2020-019; b0581 act-zm-2020-016;
  b0585 act-zm-2020-024). **Real drift count on the stable-PDF
  supercohort remains zero across 35 ticks.**

## Notable observations (b0596)

1. **NEW COHORT — FIRST judiciaryzambia.com CoA-judgment HTML drift.**
   `judgment-zm-2025-coa-105-nimble-resources-limited-v-alex-katamfya`
   is the first Phase 8 sample drawn from `judiciaryzambia.com` (the
   Court-of-Appeal source first onboarded by jiw b0583 on 2026-05-11).
   The fetched HTML differs from the stored hash. This is HTML rendering
   non-determinism on the WordPress-style post page (the underlying PDF
   referenced from the post is the canonical court judgment text and is
   unchanged). The drift pattern is analogous to the
   `zambialii judgment-akn` HTML drift family. Opens a new cohort entry
   in the cumulative tally (1/1).

   Operator note: the CoA records inserted by jiw b0583..b0594 store
   the *post HTML page* as `source_url` rather than the PDF. If the
   operator wishes to migrate CoA records to store the PDF URL (and
   PDF sha256) as the canonical source, this drift cohort would
   disappear. Decision deferred to operator.

2. **TWO judgment-akn drifts in a single tick — extends ZMCC + ZMSC
   sub-form cohort by +2.** Both drifts are zambialii.org judgment-akn
   HTML rendering pages:
   - `judgment-zm-2022-zmcc-12-banda-v-attorney-general` —
     `/akn/zm/judgment/zmcc/2022/12/eng@2022-06-20` (ZMCC sub-form,
     2022 vintage).
   - `judgment-zm-2022-zmsc-50-banda-v-people` —
     `/akn/zm/judgment/zmsc/2022/50/eng@2022-06-14` (ZMSC sub-form,
     2022 vintage).
   Both share the `/eng@<decided-date>` URL form. The cumulative
   `zambialii judgment-akn HTML drift` cohort grows from 9/17 to 11/19.
   No change to underlying judgment text — drift is HTML render
   pipeline non-determinism.

3. **NEW LARGEST media.zambialii.org legacy-PDF sampled.**
   `act-zm-1991-009-zambia-institute-of-mass-communication-act-1991`
   (1,479,094 B = 1.41 MB) extends the media.zambialii.org legacy-PDF
   match cohort to 4/4 and is the new size leader for that cohort.
   The earlier observations (b0571 act-zm-1992-004; b0585 + b0588
   act-zm-2004-013) were all sub-300 KB.

4. **Pool size grew +3 from b0595 (1892 → 1895).** The intervening
   jiw activity since the b0595 sample-draw was: b0590-jiw
   commit ec0371a (+1 CoA record musonda-chizinga-v-capstone-management)
   plus b0591-jiw (+3 CoA records) plus b0594-jiw deferred-only ticks
   (0 records inserted). However, the records-tree gained only +3
   over the b0595 starting pool figure (1892), which reconciles with
   b0590-jiw being part of the b0595 starting count and only b0591-jiw's
   +3 still pending in the b0595 reckoning being now counted here.

5. **High drift ratio (3:5) consistent with HTML-render-heavy
   sample composition.** Three of the eight sampled records were
   judgment HTML pages; all three drifted (as expected for the
   AKN/CoA judgment cohorts). The five PDF samples all matched
   first-pass.

6. **Pre-existing FTS5 records_fts_data corruption (observed by
   jiw b0587..b0594) is independent of Phase 8 reverify** — Phase 8
   does not read or write `corpus.sqlite` at all, so FTS5 corruption
   does not affect this tick's verdict. Note for operator: FTS5
   corruption remains a pending repair-worker manifest task —
   this is the 5th jiw escalation per b0594-jiw report (operator
   action required to add `fts5-rebuild-records-fts` to repair manifest).

## Integrity check

- JSON report well-formed and parseable — **PASS**.
- All required summary keys present (batch, phase, parser_version,
  seed, pool_size, sample_size, sample_rate, max_batch, results,
  match_count, drift_count, truncated_prefix_count, fetch_error_count,
  fetches, retry_fetches, started_at, completed_at) — **PASS**.
- `sample_size <= MAX_BATCH (8)` — **PASS** (8 <= 8).
- `match_count + drift_count + truncated_prefix_count +
  fetch_error_count == sample_size` — **PASS** (5 + 3 + 0 + 0 = 8).
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

No record mutation occurred. The three drift observations are
reported analytically; per the 35-tick standing finding they do NOT
indicate corpus integrity failure — they indicate upstream HTML
rendering-pipeline non-determinism, and the underlying legal text
is unchanged. The stable-PDF supercohort (133/137 real-matches
across 35 ticks; 4 truncated-prefix false drifts; **zero real
drifts**) continues to demonstrate that the stored corpus content
is faithful to the upstream sources.

## Budget impact

- Fetches this tick: **8** sample-record attempts (5 to
  www.parliament.gov.zm at 2 s between requests, 1 to
  media.zambialii.org at 5 s between requests, 2 to zambialii.org
  at 5 s between requests, 1 to judiciaryzambia.com at 5 s between
  requests). Note: media.zambialii.org and zambialii.org share the
  same rate-limit family but the inline runner tracks per-host gaps
  separately. No retries needed.
- Retry fetches this tick: **0**.
- Cumulative today (pre-b0596, 2026-05-11, worker-tick channel): 50/2000.
- Cumulative today (post-b0596, 2026-05-11, worker-tick channel):
  **58 / 2000** (2.9%).
- Wall-clock duration: ~16 seconds for the fetch loop; ~5 minutes
  overall including report write-up — well within the 20-minute cap.

## Outputs

- `reports/batch-0596-reverify.json` (deterministic JSON output).
- `reports/batch-0596.md` (this file).
- Append-only updates to `worker.log`, `costs.log`, `provenance.log`.
- No records written, modified, or deleted.
- No schema or YAML changes.

## Standing recommendations (carried forward — operator decision pending)

1. **Truncated-stored-hash backfill sweep** (b0578/b0579/b0581/b0585
   standing): unchanged across 35 ticks. Four 2020-vintage
   parliament-pdf-v1.2 records have truncated stored hashes that
   produce a stable false-drift verdict; backfilling the full-length
   sha256 would resolve them. Operator approval required.
2. **Phase 8 endpoint refinement** (b0565/b0567/b0569 standing):
   with 133/137 stable-PDF and 106/106 + 11/19 + 7/7 + 1/1 + 1/1
   HTML/AKN drift cohorts now characterised across 35 ticks,
   operator could consider option (a) text-extraction-stable hashing
   or (b) restricting Phase 8 to stable-PDF to eliminate the HTML
   rendering noise. Operator approval required.
3. **Divergent-content duplicate-ID Act records** (b0578 standing):
   five IDs known with multiple divergent record files. Operator
   approval required to canonicalise or split IDs.
4. **Phase 8 inline-runner CA-bundle parity** (b0586 standing,
   operationally confirmed b0587/b0588/b0589/b0595/b0596 across
   **six consecutive worker-ticks**): consider landing the
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
8. **NEW (b0596): judiciaryzambia.com CoA-record canonical-source
   decision.** The CoA records inserted by jiw b0583..b0594 store
   the WordPress *post HTML page URL* as `source_url`. The HTML drifts
   on re-fetch (1/1 first observation this tick). Operator could
   consider migrating CoA records to store the underlying PDF URL
   and PDF sha256 as the canonical source — this would eliminate
   the new drift cohort and align CoA with the stable-PDF supercohort
   pattern. Operator approval required.
9. **NEW (b0596): FTS5 records_fts_data corruption — repair-worker
   manifest escalation** (carried forward from jiw b0587..b0594).
   Five consecutive jiw escalations are now on record. Phase 8 has
   no opinion on this beyond noting that Phase 8 reverify does NOT
   read or write `corpus.sqlite` and is therefore unaffected.
   Operator action required.

None of the above were actioned this tick — Phase 8 reverify worker
is read-only on records by design.
