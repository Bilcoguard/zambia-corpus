# Batch 0602 — Phase 8 Nightly Re-verification (2026-05-11)

**UTC start:** 2026-05-11T23:04:21Z
**UTC end:**   2026-05-11T23:04:43Z
**Worker:**    worker-tick (Phase 8)
**Phase:**     phase_8_nightly_reverify (approved 2026-05-06; sample_rate 0.01)
**Parser:**    phase8-reverify-0.1.0 (functional contract per
  `scripts/batch_0546_phase8_reverify.py` plus b0578+ enhancements:
  tick-suffixed seed, truncated-stored-hash detector, inline
  `scripts/certs/*.pem` CA-chain loader, single retry on URLError).
**Tick scope:** Fortieth Phase 8 tick overall; twelfth worker-tick of
  UTC date 2026-05-11 (b0585 07:30Z, b0586 08:38Z, b0587 09:05Z,
  b0588 09:36Z, b0589 10:05Z, b0595 17:08Z, b0596 20:56Z, b0598 21:14Z,
  b0599 21:34Z, b0600 22:04Z, b0601 22:34Z were the prior eleven
  worker-ticks of the day).
**Execution mode:** inline runner (`/tmp/b0602_phase8_reverify.py`,
  NOT committed) per sandbox-session safety constraint maintained
  since b0548. Functional contract matches
  `scripts/batch_0546_phase8_reverify.py` with the b0578+ enhancements
  (tick-suffixed seed, prefix-startswith truncated-stored-hash
  detector, `scripts/certs/*.pem` PKI loader, single retry on
  URLError).

## Pre-tick git state

- `git pull --ff-only` returned `Already up to date` at HEAD=9f6be6d
  (worker b0601 commit — Phase 8 reverify 3 match / 5 drift / 0
  truncated-prefix / 0 fetch_error).
- The persistent `.git/objects/maintenance.lock` warning surfaced
  again (same FUSE EPERM pattern from b011..b020 + b0579..b0601) —
  non-blocking, the pull still succeeded.

## Inputs

- Pool size: **1895** (records on disk with non-empty `source_url`
  AND non-empty `source_hash`; unchanged from b0601 — no intervening
  jiw activity since the last worker-tick).
- Seed: `phase8-reverify-2026-05-11-b0602` (tick-suffixed per the
  b0578+ enhancement; first sample under this seed).
- Sample size: **8** (= MAX_BATCH cap; ceil(0.01 × 1895) = 19 →
  capped at 8).
- Out-of-band re-fetches: **0** (no URLError retries needed;
  CA-chain preload via `scripts/certs/rapidssl_tls_rsa_ca_g1.pem`
  continues to resolve first-pass — now **eleven consecutive
  worker-ticks**).

## Results — 7 match / 1 drift / 0 truncated_prefix / 0 fetch_error

| Verdict | Count | Records |
|---------|------:|---------|
| match (real) | 7 | act-zm-2023-022-the-income-tax-amendment-act-2023 (www.parliament.gov.zm `/acts/` — 299,621 B); act-zm-2024-008-zambia-qualifications-authority-act-2024 (www.parliament.gov.zm `/acts/` — 397,399 B); act-zm-2010-016-the-zambia-national-broadcasting-corporation-amendment-2010 (www.parliament.gov.zm `/amendment_act/` — 123,708 B); act-zm-2022-013-penal-code-amendment-act (www.parliament.gov.zm `/acts/` — 252,812 B); act-zm-2012-011-the-medical-levy-repeal-act-2012 (www.parliament.gov.zm `/acts/` — 14,681 B); si-zm-2015-031-property-transfer-tax-approval-and-exemption-order-2015 (zambialii.org `/akn/.../source.pdf` — 93,624 B); si-zm-2018-065-environmental-management-extended-producer-responsibility-regulations-2018 (zambialii.org `/akn/.../source.pdf` — 2,498,439 B; **NEW LARGEST source.pdf SI sample observed in Phase 8 — 2.38 MB displaces prior sub-300 KB leaders in the akn/source.pdf SI cohort**) |
| match_truncated_prefix | 0 | — |
| drift | 1 | si-zm-2022-006-zambia-police-fees-regulations-2022 (zambialii.org `/akn/zm/act/si/2022/6` — 41,828 B; **bare-AKN-path SI drift; extends bare-AKN-path SI cohort 9/9 → 10/10**) |
| fetch_error | 0 | — |

## TLS / CA-chain note

The four www.parliament.gov.zm `/acts/` PDF fetches plus the one
www.parliament.gov.zm `/amendment_act/` PDF fetch plus the two
zambialii.org-AKN `/source.pdf` SI fetches plus the one bare-AKN-path
zambialii.org SI HTML fetch all verified successfully on the first
attempt because the inline runner's `build_ssl_context()` pre-loaded
`scripts/certs/rapidssl_tls_rsa_ca_g1.pem`. No retry pass needed.
Standing recommendation #4 (b0586) operationally confirmed across
**eleven consecutive worker-ticks** now (b0586 with retry,
b0587/b0588/b0589/b0595/b0596/b0598/b0599/b0600/b0601/b0602 first-pass).

## Cohort-level cumulative tally (post-b0602, 40 ticks)

| Cohort | Pre-b0602 | Δ b0602 | Post-b0602 |
|--------|----------:|--------:|-----------:|
| zambialii.org/akn/.../act-or-SI-HTML drift (Acts + SIs with `/eng@<date>` suffix) | 116/116 | 0/0 | 116/116 |
| zambialii.org/akn/.../source.pdf match (Acts/SIs) | 31/31 | +2/+2 | 33/33 |
| zambialii.org/akn/.../source.pdf match (Judgments) | 1/1 | 0/0 | 1/1 |
| media.zambialii.org/media/legislation/ legacy-PDF match | 5/5 | 0/0 | 5/5 |
| commons.laws.africa /media/publication/ legacy-PDF match | 1/1 | 0/0 | 1/1 |
| parliament.gov.zm static PDF match (real-match `/acts/` family) | 109/109 | +4/+4 | 113/113 |
| parliament.gov.zm /amendment_act/ static PDF match | 4/4 | +1/+1 | 5/5 |
| parliament.gov.zm static PDF real DRIFT | 0/116 | 0/+4 | 0/120 |
| parliament.gov.zm static PDF truncated_stored_hash_false_drift | 4/116 | 0/+4 | 4/120 |
| zambialii judgment-akn HTML drift (ZMCC + ZMSC + ZMHC consolidated) | 13/21 | 0/0 | 13/21 |
| zambialii bare-AKN-path drift (SI sub-cohort, no `/eng@` suffix) | 9/9 | +1/+1 | **10/10** ‡‡ |
| `www.zambialii.org` host-prefix AKN-HTML drift sub-form | 2/2 | 0/0 | 2/2 |
| Parliament-node landing drift | 1/2 | 0/0 | 1/2 |
| judiciaryzambia.com CoA-judgment HTML drift | 1/1 | 0/0 | 1/1 |
| Stable-PDF combined supercohort (parliament `/acts/` + zambialii akn `/source.pdf` + media.zambialii legacy + commons.laws.africa + parliament `/amendment_act/`) — real-drift basis | 150/154 | +7/+7 | **157/161** ‡ |

‡ Stable-PDF supercohort now 157/161 across 40 ticks. The 4 cumulative
  non-real-matches remain the four truncated-stored-hash false drifts
  (b0570 act-zm-2020-011; b0578 act-zm-2020-019; b0581 act-zm-2020-016;
  b0585 act-zm-2020-024). **Real drift count on the stable-PDF
  supercohort remains zero across 40 ticks.**

‡‡ **Bare-AKN-path SI cohort hits double digits — 10/10 drift rate.**
  Every bare-AKN-path SI sample drawn in Phase 8 has drifted on
  re-fetch. The pattern is now firmly established as 100% drift across
  ten samples; the AKN bare-path resolver renders fresh non-deterministic
  HTML on each request. See standing recommendation #2 below.

## Notable observations (b0602)

1. **Strongest match-rate tick of the Phase 8 series so far (7/8 =
   87.5% match).** The 7 matches comprise 4 parliament `/acts/`
   stable-PDFs + 1 parliament `/amendment_act/` stable-PDF + 2
   zambialii akn `/source.pdf` SI stable-PDFs. The single drift is
   the bare-AKN-path SI (the consistently-100%-drifting cohort).
   This tick draws an unusually stable-PDF-heavy sample.

2. **NEW LARGEST `akn/source.pdf` SI sample observed.**
   `si-zm-2018-065-environmental-management-extended-producer-
   responsibility-regulations-2018` at
   `zambialii.org/akn/zm/act/si/2018/65/eng@2018-08-17/source.pdf`
   is **2,498,439 B (2.38 MB)** — the largest `akn/source.pdf`
   SI sample observed in the Phase 8 series. Matched first-pass.
   Confirms the akn `/source.pdf` SI path is hash-stable across
   the full size range (sub-100 KB to 2.4 MB observed).

3. **Smallest parliament `/acts/` sample now displaced.**
   `act-zm-2012-011-the-medical-levy-repeal-act-2012` at
   `www.parliament.gov.zm/.../Medical%20Levy%20%28Repeal%29.PDF`
   is 14,681 B — only the second sub-15 KB parliament `/acts/`
   sample observed (after b0601's 8,176 B
   employment-amendment-2017). Matched first-pass; reaffirms
   parliament.gov.zm static-PDF stable hashing across small
   files.

4. **Bare-AKN-path SI drift cohort hits 10/10 (100%).** With
   `si-zm-2022-006-zambia-police-fees-regulations-2022` at
   `zambialii.org/akn/zm/act/si/2022/6` (no `/eng@` suffix)
   drifting on re-fetch, the bare-AKN-path SI cohort now stands
   at 10/10. This is the most consistently-drifting cohort in the
   Phase 8 series. Operator may wish to explicitly characterise
   this as expected upstream behaviour.

5. **Pool size unchanged from b0601 (1895).** No intervening jiw
   activity since the b0601 worker-tick commit at 22:37:30Z.

6. **Drift composition (1:7) is the strongest match skew of the
   series.** Composition consistent with the 40-tick standing
   finding: stable PDFs hash deterministically; AKN HTML and
   bare-AKN paths render dynamically. The single drift is from
   the bare-AKN-path SI sub-cohort, which has now drifted on
   100% of samples (10/10).

7. **Pre-existing FTS5 records_fts_data corruption (observed by
   jiw b0587..b0594..b0597..b0598) is independent of Phase 8
   reverify** — Phase 8 does not read or write `corpus.sqlite`
   at all, so FTS5 corruption does not affect this tick's verdict.
   Repair-worker manifest escalation remains outstanding (still
   18 consecutive jiw ticks blocked as of last jiw observation).

## Integrity check

- JSON report well-formed and parseable — **PASS**.
- All required summary keys present (batch, phase, parser_version,
  seed, pool_size, sample_size, sample_rate, max_batch, results,
  match_count, drift_count, truncated_prefix_count, fetch_error_count,
  fetches, retry_fetches, started_at, completed_at) — **PASS**.
- `sample_size <= MAX_BATCH (8)` — **PASS** (8 <= 8).
- `match_count + drift_count + truncated_prefix_count +
  fetch_error_count == sample_size` — **PASS** (7 + 1 + 0 + 0 = 8).
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

No record mutation occurred. The single drift observation is reported
analytically; per the 40-tick standing finding it does NOT indicate
corpus integrity failure — it indicates upstream HTML rendering-pipeline
non-determinism on the bare-AKN-path SI resolver, and the underlying
legal text is unchanged. The stable-PDF supercohort (157/161
real-matches across 40 ticks; 4 truncated-prefix false drifts; **zero
real drifts**) continues to demonstrate that the stored corpus content
is faithful to the upstream sources.

## Budget impact

- Fetches this tick: **8** sample-record attempts (5 to
  www.parliament.gov.zm at 2 s between requests, 3 to zambialii.org
  at 5 s between requests). No retries needed.
- Retry fetches this tick: **0**.
- Cumulative today (pre-b0602, 2026-05-11, worker-tick channel): 90/2000.
- Cumulative today (post-b0602, 2026-05-11, worker-tick channel):
  **98 / 2000** (4.9%).
- Wall-clock duration: ~22 seconds for the fetch loop; well within
  the 20-minute cap.

## Outputs

- `reports/batch-0602-reverify.json` (deterministic JSON output).
- `reports/batch-0602.md` (this file).
- Append-only updates to `worker.log`, `costs.log`, `provenance.log`.
- No records written, modified, or deleted.
- No schema or YAML changes.

## Standing recommendations (carried forward — operator decision pending)

1. **Truncated-stored-hash backfill sweep** (b0578/b0579/b0581/b0585
   standing): unchanged across 40 ticks. Four 2020-vintage
   parliament-pdf-v1.2 records have truncated stored hashes that
   produce a stable false-drift verdict; backfilling the full-length
   sha256 would resolve them. Operator approval required.
2. **Phase 8 endpoint refinement** (b0565/b0567/b0569 standing,
   **strengthened b0602**): with 157/161 stable-PDF and 116/116 + 13/21
   + **10/10** + 2/2 + 1/2 HTML/AKN drift cohorts now characterised
   across 40 ticks (bare-AKN-path SI cohort now at 100% drift on 10
   samples), operator could consider option (a) text-extraction-stable
   hashing or (b) restricting Phase 8 to stable-PDF to eliminate the
   HTML rendering noise. Operator approval required.
3. **Divergent-content duplicate-ID Act records** (b0578 standing):
   five IDs known with multiple divergent record files. Operator
   approval required to canonicalise or split IDs.
4. **Phase 8 inline-runner CA-bundle parity** (b0586 standing,
   operationally confirmed b0587..b0602 across **eleven consecutive
   worker-ticks**): consider landing the `scripts/certs/*.pem`
   preload into the canonical `scripts/batch_NNNN_phase8_reverify.py`
   template the next time the baseline is refreshed.
5. **Stray `.git/refs/heads/main.lock.bak.*` ref backups**
   (b0588 first observation): persists; sandbox cannot
   unlink. No new observations this tick.
6. **`www.zambialii.org`-prefixed AKN-HTML record cluster audit**
   (b0589 standing, strengthened b0601): unchanged this tick — no
   `www.zambialii.org` host-prefix samples drawn. Two-sample cohort
   from b0601 stands.
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
    jiw ticks blocked as of last jiw observation).
11. **Parliament-node landing reclassification** (b0601 standing):
    /node/ family at 1/2 drift after 40 ticks; further samples
    needed before pattern is conclusive. Unchanged this tick — no
    /node/ sample drawn.

None of the above were actioned this tick — Phase 8 reverify worker
is read-only on records by design.
