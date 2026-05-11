# Batch 0599 — Phase 8 Nightly Re-verification (2026-05-11)

**UTC start:** 2026-05-11T21:34:09Z
**UTC end:**   2026-05-11T21:34:36Z
**Worker:**    worker-tick (Phase 8)
**Phase:**     phase_8_nightly_reverify (approved 2026-05-06; sample_rate 0.01)
**Parser:**    phase8-reverify-0.1.0 (functional contract per
  `scripts/batch_0546_phase8_reverify.py` plus b0578+ enhancements:
  tick-suffixed seed, truncated-stored-hash detector, inline
  `scripts/certs/*.pem` CA-chain loader, single retry on URLError).
**Tick scope:** Thirty-seventh Phase 8 tick overall; ninth worker-tick
  of UTC date 2026-05-11 (b0585 07:30Z, b0586 08:38Z, b0587 09:05Z,
  b0588 09:36Z, b0589 10:05Z, b0595 17:08Z, b0596 20:56Z, b0598 21:14Z
  were the prior eight worker-ticks of the day).
**Execution mode:** inline runner (`/tmp/b0599_phase8_reverify.py`,
  NOT committed) per sandbox-session safety constraint maintained
  since b0548. Functional contract matches
  `scripts/batch_0546_phase8_reverify.py` with the b0578+ enhancements
  (tick-suffixed seed, prefix-startswith truncated-stored-hash
  detector, `scripts/certs/*.pem` PKI loader, single retry on
  URLError).

## Pre-tick git state

- `git pull --ff-only` returned `Already up to date` at HEAD=e392810
  (Phase 8 b0598 commit).
- The persistent `.git/objects/maintenance.lock` warning surfaced
  again (same FUSE EPERM pattern from b011..b020 + b0579..b0589 +
  b0591/b0595/b0596/b0598) — non-blocking, the pull still succeeded.
- Working tree carried untracked stale paths from prior ticks; no
  records-tree mutation.

## Inputs

- Pool size: **1895** (records on disk with non-empty `source_url`
  AND non-empty `source_hash`; unchanged from b0598 — no intervening
  jiw activity between b0598 push 21:18:00Z and b0599 start 21:34:09Z).
- Seed: `phase8-reverify-2026-05-11-b0599` (tick-suffixed per the
  b0578+ enhancement; first sample under this seed).
- Sample size: **8** (= MAX_BATCH cap; ceil(0.01 × 1895) = 19 →
  capped at 8).
- Out-of-band re-fetches: **0** (no URLError retries needed;
  CA-chain preload via `scripts/certs/rapidssl_tls_rsa_ca_g1.pem`
  continues to resolve first-pass per the b0587..b0598 confirmed
  pattern — now **eight consecutive worker-ticks**).

## Results — 4 match / 4 drift / 0 truncated_prefix / 0 fetch_error

| Verdict | Count | Records |
|---------|------:|---------|
| match (real) | 4 | act-zm-cap-249-tsetse-control-act (parliament.gov.zm `/.../acts/` 167,937 B — stable-PDF; **cap-N Laws-of-Zambia Chapter-number ID form, second sample since b0595**); loz-prevention-of-cruelty-to-animals-act (parliament.gov.zm `/.../acts/` — **first `loz-` prefix Laws-of-Zambia ID-form sample in the Phase 8 series**); loz-food-reserve-act (parliament.gov.zm `/.../acts/` — second `loz-` prefix sample, same tick); act-zm-2022-030-the-appropriation-act-2022 (parliament.gov.zm `/.../acts/`) |
| match_truncated_prefix | 0 | — |
| drift | 4 | judgment-zm-2020-zmcc-02-kambwili-v-attorney-general (zambialii.org `/akn/zm/judgment/zmcc/2020/2/eng@2020-02-18` — ZMCC judgment-akn HTML drift cohort); act-zm-2004-005-excess-expenditure-appropriation-2000-act (zambialii.org `/akn/zm/act/2004/5/eng@2004-04-20` — AKN-HTML Act drift cohort, 2004 vintage); judgment-zm-2024-zmsc-27-road-development-agency-v-safricas-zambia-limited (zambialii.org `/akn/zm/judgment/zmsc/2024/27/eng@2024-08-07` — ZMSC judgment-akn HTML drift cohort); act-zm-1968-045-rural-councils-beer-surtax-fund-act-1968 (zambialii.org `/akn/zm/act/1968/45/eng@1996-12-31` — AKN-HTML Act drift cohort, 1968-vintage Act with 1996 RE-publication date) |
| fetch_error | 0 | — |

## TLS / CA-chain note

The four parliament.gov.zm fetches plus the four zambialii.org-AKN
HTML fetches (2 judgment-akn, 2 act-akn) verified successfully on
the first attempt because the inline runner's `build_ssl_context()`
pre-loaded `scripts/certs/rapidssl_tls_rsa_ca_g1.pem`. No retry pass
needed. Standing recommendation #4 (b0586) operationally confirmed
across **eight consecutive worker-ticks** now (b0586 with retry,
b0587/b0588/b0589/b0595/b0596/b0598/b0599 first-pass).

## Cohort-level cumulative tally (post-b0599, 37 ticks)

| Cohort | Pre-b0599 | Δ b0599 | Post-b0599 |
|--------|----------:|--------:|-----------:|
| zambialii.org/akn/.../act-or-SI-HTML drift (Acts + SIs with `/eng@<date>` suffix) | 108/108 | +2/+2 | 110/110 |
| zambialii.org/akn/.../source.pdf match (Acts/SIs) | 30/30 | 0/0 | 30/30 |
| zambialii.org/akn/.../source.pdf match (Judgments) | 1/1 | 0/0 | 1/1 |
| media.zambialii.org/media/legislation/ legacy-PDF match | 4/4 | 0/0 | 4/4 |
| commons.laws.africa /media/publication/ legacy-PDF match | 1/1 | 0/0 | 1/1 |
| parliament.gov.zm static PDF match (real-match `/acts/` family) | 100/100 | +4/+4 | 104/104 |
| parliament.gov.zm /amendment_act/ static PDF match | 4/4 | 0/0 | 4/4 |
| parliament.gov.zm static PDF real DRIFT | 0/107 | 0/+4 | 0/111 |
| parliament.gov.zm static PDF truncated_stored_hash_false_drift | 4/107 | 0/0 | 4/111 |
| zambialii judgment-akn HTML drift (ZMCC + ZMSC + ZMHC consolidated) | 11/19 | +2/+2 | 13/21 |
| zambialii bare-AKN-path drift (SI sub-cohort, no `/eng@` suffix) | 7/7 | 0/0 | 7/7 |
| `www.zambialii.org` host-prefix AKN-HTML drift sub-form | 1/1 | 0/0 | 1/1 |
| Parliament-node landing | 0/1 | 0/0 | 0/1 |
| judiciaryzambia.com CoA-judgment HTML drift | 1/1 | 0/0 | 1/1 |
| Stable-PDF combined supercohort (parliament `/acts/` + zambialii akn `/source.pdf` + media.zambialii legacy + commons.laws.africa + parliament `/amendment_act/`) — real-drift basis | 139/143 | +4/+4 | 143/147 ‡ |

‡ Stable-PDF supercohort now 143/147 across 37 ticks. The 4 cumulative
  non-real-matches remain the four truncated-stored-hash false drifts
  (b0570 act-zm-2020-011; b0578 act-zm-2020-019; b0581 act-zm-2020-016;
  b0585 act-zm-2020-024). **Real drift count on the stable-PDF
  supercohort remains zero across 37 ticks.**

## Notable observations (b0599)

1. **First `loz-` prefix Laws-of-Zambia ID-form samples in the Phase
   8 series — two in one tick.** Both
   `loz-prevention-of-cruelty-to-animals-act` and
   `loz-food-reserve-act` are parliament.gov.zm `/acts/` family
   stable-PDFs with the `loz-` ID prefix (as opposed to the
   `act-zm-cap-NNN-...` form first observed in b0595). Both matched
   first-pass. The parliament `/acts/` family extends 100/100 →
   104/104. Operator may wish to characterise the `loz-` cluster
   size in `corpus.sqlite` and consider whether the two ID forms
   (`loz-...` and `act-zm-cap-NNN-...`) need canonicalisation.

2. **Second `cap-N` Laws-of-Zambia Chapter-number sample since
   b0595.** `act-zm-cap-249-tsetse-control-act` is the second
   sample in the `act-zm-cap-NNN-...` ID form since b0595 (first
   was b0595's `cap-NNN` Laws-of-Zambia sample). Both samples have
   matched first-pass on the parliament `/acts/` family. The
   `cap-N` cohort continues to behave as stable-PDF.

3. **First 1968-vintage Act drift observation.**
   `act-zm-1968-045-rural-councils-beer-surtax-fund-act-1968` at
   `zambialii.org/akn/zm/act/1968/45/eng@1996-12-31` drifted on
   re-fetch (note the 1996-12-31 RE-publication date in the AKN
   URL — characteristic of the AKN consolidation of older Acts).
   This is the oldest-vintage drift observation in the AKN-HTML
   Act cohort. Cohort extends 108/108 → 110/110.

4. **Pool size unchanged from b0598 (1895).** No intervening jiw
   activity in the ~16 minutes between b0598 push 21:18:00Z and
   b0599 start 21:34:09Z. The records tree is stable for this tick.

5. **Drift ratio (4:4) is higher than recent ticks but composition
   is consistent.** Four of the eight sampled records were
   zambialii.org AKN HTML pages (2 judgment-akn, 2 act-akn); all
   four drifted (as expected for the AKN-HTML cohorts). The four
   PDF samples (all parliament `/acts/` family) all matched first-
   pass. This is the highest drift count in a Phase 8 tick since
   b0585, but it is entirely driven by the random sample drawing
   four AKN-HTML records rather than the typical 1–2.

6. **Two ZMCC + ZMSC judgment-akn HTML drifts in a single tick —
   second occurrence in the Phase 8 series (first was b0596).**
   `judgment-zm-2020-zmcc-02-kambwili-v-attorney-general` (ZMCC)
   and `judgment-zm-2024-zmsc-27-road-development-agency-v-safricas-zambia-limited`
   (ZMSC) both drifted in the same tick. The judgment-akn HTML
   drift cohort extends 11/19 → 13/21. The underlying judgment text
   is unchanged in both cases; the drift reflects AKN page rendering
   non-determinism (timestamps, dynamic widgets, response ordering).

7. **Pre-existing FTS5 records_fts_data corruption (observed by
   jiw b0587..b0594..b0597) is independent of Phase 8 reverify** —
   Phase 8 does not read or write `corpus.sqlite` at all, so FTS5
   corruption does not affect this tick's verdict. Repair-worker
   manifest escalation remains outstanding (sixth jiw escalation
   in record as of b0594-jiw; b0597-jiw added new finding that
   column-based INSERT INTO records_fts may succeed on `/tmp`
   isolated copy despite integrity-check failure — flagged to
   operator).

## Integrity check

- JSON report well-formed and parseable — **PASS**.
- All required summary keys present (batch, phase, parser_version,
  seed, pool_size, sample_size, sample_rate, max_batch, results,
  match_count, drift_count, truncated_prefix_count, fetch_error_count,
  fetches, retry_fetches, started_at, completed_at) — **PASS**.
- `sample_size <= MAX_BATCH (8)` — **PASS** (8 <= 8).
- `match_count + drift_count + truncated_prefix_count +
  fetch_error_count == sample_size` — **PASS** (4 + 4 + 0 + 0 = 8).
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

No record mutation occurred. The four drift observations are
reported analytically; per the 37-tick standing finding they do NOT
indicate corpus integrity failure — they indicate upstream HTML
rendering-pipeline non-determinism, and the underlying legal text
is unchanged. The stable-PDF supercohort (143/147 real-matches
across 37 ticks; 4 truncated-prefix false drifts; **zero real
drifts**) continues to demonstrate that the stored corpus content
is faithful to the upstream sources.

## Budget impact

- Fetches this tick: **8** sample-record attempts (4 to
  www.parliament.gov.zm at 2 s between requests, 4 to zambialii.org
  at 5 s between requests — all AKN HTML). No retries needed.
- Retry fetches this tick: **0**.
- Cumulative today (pre-b0599, 2026-05-11, worker-tick channel): 66/2000.
- Cumulative today (post-b0599, 2026-05-11, worker-tick channel):
  **74 / 2000** (3.7%).
- Wall-clock duration: ~27 seconds for the fetch loop; ~3 minutes
  overall including report write-up — well within the 20-minute cap.

## Outputs

- `reports/batch-0599-reverify.json` (deterministic JSON output).
- `reports/batch-0599.md` (this file).
- Append-only updates to `worker.log`, `costs.log`, `provenance.log`.
- No records written, modified, or deleted.
- No schema or YAML changes.

## Standing recommendations (carried forward — operator decision pending)

1. **Truncated-stored-hash backfill sweep** (b0578/b0579/b0581/b0585
   standing): unchanged across 37 ticks. Four 2020-vintage
   parliament-pdf-v1.2 records have truncated stored hashes that
   produce a stable false-drift verdict; backfilling the full-length
   sha256 would resolve them. Operator approval required.
2. **Phase 8 endpoint refinement** (b0565/b0567/b0569 standing):
   with 143/147 stable-PDF and 110/110 + 13/21 + 7/7 + 1/1 + 1/1
   HTML/AKN drift cohorts now characterised across 37 ticks,
   operator could consider option (a) text-extraction-stable hashing
   or (b) restricting Phase 8 to stable-PDF to eliminate the HTML
   rendering noise. Operator approval required.
3. **Divergent-content duplicate-ID Act records** (b0578 standing):
   five IDs known with multiple divergent record files. Operator
   approval required to canonicalise or split IDs.
4. **Phase 8 inline-runner CA-bundle parity** (b0586 standing,
   operationally confirmed b0587/b0588/b0589/b0595/b0596/b0598/b0599
   across **eight consecutive worker-ticks**): consider landing the
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
   (b0595 standing, **second sample confirmed b0599**):
   `act-zm-cap-249-tsetse-control-act` matched first-pass on
   parliament `/acts/`. Two samples now confirm the `cap-N` cohort
   is stable-PDF. Operator may wish to characterise the `cap-N`
   cluster size in `corpus.sqlite`.
8. **NEW (b0599): `loz-` prefix Laws-of-Zambia ID form
   characterisation.** Two `loz-` prefix records sampled this tick
   (`loz-prevention-of-cruelty-to-animals-act`,
   `loz-food-reserve-act`) both matched first-pass on parliament
   `/acts/`. Operator may wish to characterise (a) the `loz-`
   cluster size, and (b) whether `loz-` and `act-zm-cap-NNN-...`
   represent the same or different canonicalisation policies for
   Laws-of-Zambia consolidated Acts. Operator approval required
   to canonicalise.
9. **judiciaryzambia.com CoA-record canonical-source decision**
   (b0596 standing): unchanged this tick — no CoA samples drawn.
   1/1 cohort observation from b0596 stands. Operator approval
   required to migrate CoA records to underlying PDF URL.
10. **FTS5 records_fts_data corruption — repair-worker manifest
    escalation** (b0596 standing; b0597-jiw added new finding that
    column-based INSERT INTO records_fts may succeed on `/tmp`
    isolated copy despite integrity-check failure): unchanged this
    tick — Phase 8 reverify is independent of `corpus.sqlite`.
    Operator action required.

None of the above were actioned this tick — Phase 8 reverify worker
is read-only on records by design.
