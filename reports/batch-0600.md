# Batch 0600 — Phase 8 Nightly Re-verification (2026-05-11)

**UTC start:** 2026-05-11T22:04:12Z
**UTC end:**   2026-05-11T22:04:39Z
**Worker:**    worker-tick (Phase 8)
**Phase:**     phase_8_nightly_reverify (approved 2026-05-06; sample_rate 0.01)
**Parser:**    phase8-reverify-0.1.0 (functional contract per
  `scripts/batch_0546_phase8_reverify.py` plus b0578+ enhancements:
  tick-suffixed seed, truncated-stored-hash detector, inline
  `scripts/certs/*.pem` CA-chain loader, single retry on URLError).
**Tick scope:** Thirty-eighth Phase 8 tick overall; tenth worker-tick
  of UTC date 2026-05-11 (b0585 07:30Z, b0586 08:38Z, b0587 09:05Z,
  b0588 09:36Z, b0589 10:05Z, b0595 17:08Z, b0596 20:56Z, b0598 21:14Z,
  b0599 21:34Z were the prior nine worker-ticks of the day).
**Execution mode:** inline runner (`/tmp/b0600_phase8_reverify.py`,
  NOT committed) per sandbox-session safety constraint maintained
  since b0548. Functional contract matches
  `scripts/batch_0546_phase8_reverify.py` with the b0578+ enhancements
  (tick-suffixed seed, prefix-startswith truncated-stored-hash
  detector, `scripts/certs/*.pem` PKI loader, single retry on
  URLError).

## Pre-tick git state

- `git pull --ff-only` returned `Already up to date` at HEAD=21d10cf
  (Phase 8 b0599 commit).
- The persistent `.git/objects/maintenance.lock` warning surfaced
  again (same FUSE EPERM pattern from b011..b020 + b0579..b0589 +
  b0591/b0595/b0596/b0598/b0599) — non-blocking, the pull still
  succeeded.
- Working tree carried untracked stale paths from prior ticks plus
  a small uncommitted append to `worker.log` from the b0599 tail
  (GIT_COMMIT/GIT_PUSH/STOP lines that were written after the
  b0599 commit). No records-tree mutation.

## Inputs

- Pool size: **1895** (records on disk with non-empty `source_url`
  AND non-empty `source_hash`; unchanged from b0599 — no intervening
  jiw activity between b0599 push 21:36:00Z and b0600 start 22:04:12Z).
- Seed: `phase8-reverify-2026-05-11-b0600` (tick-suffixed per the
  b0578+ enhancement; first sample under this seed).
- Sample size: **8** (= MAX_BATCH cap; ceil(0.01 × 1895) = 19 →
  capped at 8).
- Out-of-band re-fetches: **0** (no URLError retries needed;
  CA-chain preload via `scripts/certs/rapidssl_tls_rsa_ca_g1.pem`
  continues to resolve first-pass — now **nine consecutive
  worker-ticks**).

## Results — 4 match / 4 drift / 0 truncated_prefix / 0 fetch_error

| Verdict | Count | Records |
|---------|------:|---------|
| match (real) | 4 | si-zm-2014-050-income-tax-pay-as-you-earn-regulations-2014 (zambialii.org `/akn/zm/act/si/2014/50/eng@2014-09-19/source.pdf` — 138,516 B; akn /source.pdf SI cohort); act-zm-cap-257-national-assembly-staff-act (parliament.gov.zm `/acts/` — 68,163 B; **third `cap-N` Laws-of-Zambia sample after b0595's cap-NNN and b0599's act-zm-cap-249**); act-zm-2018-008-the-anti-terrorism-and-non-proliferation-act-2018 (parliament.gov.zm `/acts/` — 204,434 B); act-zm-2010-045-veterinary-and-veterinary-para-professions-2010 (parliament.gov.zm `/acts/` — **1,211,863 B = 1.16 MB; notably large parliament `/acts/` sample, second-largest stable-PDF observed in the Phase 8 series after b0596's 1.41 MB media.zambialii sample**) |
| match_truncated_prefix | 0 | — |
| drift | 4 | act-zm-2019-017-supplementary-appropriation-2019-no-2-act (zambialii.org `/akn/zm/act/2019/17/eng@2019-12-27` — 38,542 B; AKN-HTML Act drift cohort, 2019-vintage); act-zm-1967-065-tobacco-levy-act-1967 (zambialii.org `/akn/zm/act/1967/65/eng@1996-12-31` — 86,409 B; **NEW OLDEST-VINTAGE AKN-HTML Act drift — 1967-vintage Act with 1996-12-31 RE-publication date; displaces b0599's 1968-vintage rural-councils-beer-surtax**); act-zm-1994-035-parliamentary-and-ministerial-code-of-conduct-act (zambialii.org `/akn/zm/act/1994/35/eng@1996-12-31` — 101,021 B; AKN-HTML Act drift cohort, 1994-vintage with 1996 RE-publication date); si-zm-2014-016-animal-health-livestock-cleansing-order-2014 (zambialii.org `/akn/zm/act/si/2014/16` — 39,132 B; **bare-AKN-path SI drift cohort, no `/eng@` suffix; extends cohort 7/7 → 8/8**) |
| fetch_error | 0 | — |

## TLS / CA-chain note

The three parliament.gov.zm fetches plus the four zambialii.org-AKN
HTML fetches (3 act-akn + 1 bare-AKN SI) plus the one zambialii.org
/source.pdf SI verified successfully on the first attempt because
the inline runner's `build_ssl_context()` pre-loaded
`scripts/certs/rapidssl_tls_rsa_ca_g1.pem`. No retry pass needed.
Standing recommendation #4 (b0586) operationally confirmed across
**nine consecutive worker-ticks** now (b0586 with retry,
b0587/b0588/b0589/b0595/b0596/b0598/b0599/b0600 first-pass).

## Cohort-level cumulative tally (post-b0600, 38 ticks)

| Cohort | Pre-b0600 | Δ b0600 | Post-b0600 |
|--------|----------:|--------:|-----------:|
| zambialii.org/akn/.../act-or-SI-HTML drift (Acts + SIs with `/eng@<date>` suffix) | 110/110 | +3/+3 | 113/113 |
| zambialii.org/akn/.../source.pdf match (Acts/SIs) | 30/30 | +1/+1 | 31/31 |
| zambialii.org/akn/.../source.pdf match (Judgments) | 1/1 | 0/0 | 1/1 |
| media.zambialii.org/media/legislation/ legacy-PDF match | 4/4 | 0/0 | 4/4 |
| commons.laws.africa /media/publication/ legacy-PDF match | 1/1 | 0/0 | 1/1 |
| parliament.gov.zm static PDF match (real-match `/acts/` family) | 104/104 | +3/+3 | 107/107 |
| parliament.gov.zm /amendment_act/ static PDF match | 4/4 | 0/0 | 4/4 |
| parliament.gov.zm static PDF real DRIFT | 0/111 | 0/+3 | 0/114 |
| parliament.gov.zm static PDF truncated_stored_hash_false_drift | 4/111 | 0/+3 | 4/114 |
| zambialii judgment-akn HTML drift (ZMCC + ZMSC + ZMHC consolidated) | 13/21 | 0/0 | 13/21 |
| zambialii bare-AKN-path drift (SI sub-cohort, no `/eng@` suffix) | 7/7 | +1/+1 | 8/8 |
| `www.zambialii.org` host-prefix AKN-HTML drift sub-form | 1/1 | 0/0 | 1/1 |
| Parliament-node landing | 0/1 | 0/0 | 0/1 |
| judiciaryzambia.com CoA-judgment HTML drift | 1/1 | 0/0 | 1/1 |
| Stable-PDF combined supercohort (parliament `/acts/` + zambialii akn `/source.pdf` + media.zambialii legacy + commons.laws.africa + parliament `/amendment_act/`) — real-drift basis | 143/147 | +4/+4 | 147/151 ‡ |

‡ Stable-PDF supercohort now 147/151 across 38 ticks. The 4 cumulative
  non-real-matches remain the four truncated-stored-hash false drifts
  (b0570 act-zm-2020-011; b0578 act-zm-2020-019; b0581 act-zm-2020-016;
  b0585 act-zm-2020-024). **Real drift count on the stable-PDF
  supercohort remains zero across 38 ticks.**

## Notable observations (b0600)

1. **NEW OLDEST-VINTAGE AKN-HTML Act drift — 1967.**
   `act-zm-1967-065-tobacco-levy-act-1967` at
   `zambialii.org/akn/zm/act/1967/65/eng@1996-12-31` drifted on
   re-fetch, displacing b0599's 1968-vintage `rural-councils-beer-
   surtax-fund-act-1968` as the oldest-vintage drift observation
   in the AKN-HTML Act cohort. Note again the characteristic
   1996-12-31 RE-publication date in the AKN URL — the AKN
   consolidation of older Acts continues to use the 1996 cut-off
   date for the chapter-revision publication. Cohort extends
   110/110 → 113/113.

2. **Third `cap-N` Laws-of-Zambia Chapter-number sample —
   first-pass match continues.** `act-zm-cap-257-national-assembly-
   staff-act` is the third sample in the `act-zm-cap-NNN-...` ID
   form (after b0595's `cap-NNN` Laws-of-Zambia sample and b0599's
   `act-zm-cap-249-tsetse-control-act`). All three samples have
   matched first-pass on the parliament `/acts/` family. The
   `cap-N` cohort continues to behave as stable-PDF. Standing
   recommendation #7 (cap-N cluster characterisation) remains.

3. **Notably large parliament `/acts/` PDF sample matched first-
   pass.** `act-zm-2010-045-veterinary-and-veterinary-para-
   professions-2010` is 1,211,863 B = 1.16 MB — the second-largest
   stable-PDF observed in the Phase 8 series (largest was b0596's
   media.zambialii legacy PDF at 1.41 MB). Confirms that
   parliament.gov.zm static-PDF hashing is stable across files
   well over 1 MB.

4. **bare-AKN-path SI drift cohort extends 7/7 → 8/8.**
   `si-zm-2014-016-animal-health-livestock-cleansing-order-2014`
   at `zambialii.org/akn/zm/act/si/2014/16` (no `/eng@` suffix)
   drifted on re-fetch, joining the bare-AKN-path SI sub-cohort
   that consistently drifts. This is the first bare-AKN-path
   drift since b0577 (per cohort history). All 8 samples in this
   cohort have drifted — the AKN bare-path resolver appears to
   render a fresh HTML page on each request with non-deterministic
   widget content.

5. **Pool size unchanged from b0599 (1895).** No intervening
   jiw activity in the ~28 minutes between b0599 push 21:36:00Z
   and b0600 start 22:04:12Z. The records tree is stable for
   this tick.

6. **Drift composition (4:4) is identical in COUNT to b0599 but
   different in COMPOSITION.** b0599 had 4 AKN-HTML drifts (2
   judgment-akn + 2 act-akn) and 4 parliament `/acts/` matches.
   b0600 has 3 AKN-HTML drifts (all act-akn) + 1 bare-AKN-path
   SI drift, with 3 parliament `/acts/` matches and 1 akn
   /source.pdf SI match. No judgment-akn samples drawn this
   tick — judgment-akn HTML drift cohort unchanged at 13/21.

7. **Pre-existing FTS5 records_fts_data corruption (observed by
   jiw b0587..b0594..b0597) is independent of Phase 8 reverify** —
   Phase 8 does not read or write `corpus.sqlite` at all, so FTS5
   corruption does not affect this tick's verdict. Repair-worker
   manifest escalation remains outstanding.

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
reported analytically; per the 38-tick standing finding they do NOT
indicate corpus integrity failure — they indicate upstream HTML
rendering-pipeline non-determinism, and the underlying legal text
is unchanged. The stable-PDF supercohort (147/151 real-matches
across 38 ticks; 4 truncated-prefix false drifts; **zero real
drifts**) continues to demonstrate that the stored corpus content
is faithful to the upstream sources.

## Budget impact

- Fetches this tick: **8** sample-record attempts (3 to
  www.parliament.gov.zm at 2 s between requests, 5 to zambialii.org
  at 5 s between requests — 1 SI source.pdf + 3 act-akn HTML + 1
  bare-AKN-path SI HTML). No retries needed.
- Retry fetches this tick: **0**.
- Cumulative today (pre-b0600, 2026-05-11, worker-tick channel): 74/2000.
- Cumulative today (post-b0600, 2026-05-11, worker-tick channel):
  **82 / 2000** (4.1%).
- Wall-clock duration: ~27 seconds for the fetch loop; well within
  the 20-minute cap.

## Outputs

- `reports/batch-0600-reverify.json` (deterministic JSON output).
- `reports/batch-0600.md` (this file).
- Append-only updates to `worker.log`, `costs.log`, `provenance.log`.
- No records written, modified, or deleted.
- No schema or YAML changes.

## Standing recommendations (carried forward — operator decision pending)

1. **Truncated-stored-hash backfill sweep** (b0578/b0579/b0581/b0585
   standing): unchanged across 38 ticks. Four 2020-vintage
   parliament-pdf-v1.2 records have truncated stored hashes that
   produce a stable false-drift verdict; backfilling the full-length
   sha256 would resolve them. Operator approval required.
2. **Phase 8 endpoint refinement** (b0565/b0567/b0569 standing):
   with 147/151 stable-PDF and 113/113 + 13/21 + 8/8 + 1/1 + 1/1
   HTML/AKN drift cohorts now characterised across 38 ticks,
   operator could consider option (a) text-extraction-stable hashing
   or (b) restricting Phase 8 to stable-PDF to eliminate the HTML
   rendering noise. Operator approval required.
3. **Divergent-content duplicate-ID Act records** (b0578 standing):
   five IDs known with multiple divergent record files. Operator
   approval required to canonicalise or split IDs.
4. **Phase 8 inline-runner CA-bundle parity** (b0586 standing,
   operationally confirmed b0587/b0588/b0589/b0595/b0596/b0598/b0599/b0600
   across **nine consecutive worker-ticks**): consider landing the
   `scripts/certs/*.pem` preload into the canonical
   `scripts/batch_NNNN_phase8_reverify.py` template the next time
   the baseline is refreshed.
5. **Stray `.git/refs/heads/main.lock.bak.*` ref backups**
   (b0588 first observation): persists; sandbox cannot
   unlink. No new observations this tick.
6. **`www.zambialii.org`-prefixed AKN-HTML record cluster audit**
   (b0589 standing): unchanged this tick.
7. **`cap-N` Laws-of-Zambia Chapter-number ID form characterisation**
   (b0595 standing, **third sample confirmed b0600**):
   `act-zm-cap-257-national-assembly-staff-act` matched first-pass
   on parliament `/acts/`. Three samples now confirm the `cap-N`
   cohort is stable-PDF. Operator may wish to characterise the
   `cap-N` cluster size in `corpus.sqlite`.
8. **`loz-` prefix Laws-of-Zambia ID form characterisation**
   (b0599 standing): unchanged this tick — no `loz-` prefix
   samples drawn. Two-sample confirmation from b0599 stands.
9. **judiciaryzambia.com CoA-record canonical-source decision**
   (b0596 standing): unchanged this tick — no CoA samples drawn.
10. **FTS5 records_fts_data corruption — repair-worker manifest
    escalation** (b0596 standing; b0597-jiw added new finding that
    column-based INSERT INTO records_fts may succeed on `/tmp`
    isolated copy despite integrity-check failure): unchanged this
    tick — Phase 8 reverify is independent of `corpus.sqlite`.
    Operator action required.

None of the above were actioned this tick — Phase 8 reverify worker
is read-only on records by design.
