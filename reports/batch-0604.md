# Batch 0604 — Phase 8 Nightly Re-verification (2026-05-12)

**UTC start:** 2026-05-12T05:10:29Z
**UTC end:**   2026-05-12T05:11:09Z
**Worker:**    worker-tick (Phase 8)
**Phase:**     phase_8_nightly_reverify (approved 2026-05-06; sample_rate 0.01)
**Parser:**    phase8-reverify-0.1.0 (functional contract per
  `scripts/batch_0546_phase8_reverify.py` plus b0578+ enhancements:
  tick-suffixed seed, prefix-startswith truncated-stored-hash detector,
  inline `scripts/certs/*.pem` CA-chain loader, single retry on URLError).
**Tick scope:** Forty-first Phase 8 tick overall; first worker-tick of
  UTC date 2026-05-12 (the previous worker-tick attempts at 01:32:44Z
  and 05:07:42Z today halted on `git pull --ff-only` failure — see
  worker.log for the stale-ref diagnostic; this tick is the first
  successful pull in 2026-05-12).
**Execution mode:** inline runner (`/tmp/b0603_phase8_reverify.py`,
  NOT committed) per the sandbox-session safety constraint maintained
  since b0548. Functional contract matches
  `scripts/batch_0546_phase8_reverify.py` with the b0578+ enhancements.
**Renumber note:** Originally drew sample as **b0603** at
  2026-05-12T05:10:29Z. Renumbered **b0603 → b0604** due to collision
  with judgment-ingestion-worker `batch-0603-jiw` commit `0c82d0f`
  (read-only confirmation, 20th FTS5-blocked JIW tick, pushed at
  2026-05-12T05:11:05+0200). Same b0585 / b0591 / b0595 / b0598
  renumbering precedent. Report filename, commit message, and worker
  log entries use **b0604**. The underlying RNG seed is preserved as
  `phase8-reverify-2026-05-12-b0603` to maintain sample-set
  reproducibility (re-runnable for audit).

## Pre-tick git state

- `git pull --ff-only` returned `Already up to date` at HEAD=`90d20f6`
  (jiw b0602 final commit — diagnostic FTS5 virtual-table-test
  FALSIFIED, 19th consecutive blocked jiw tick, fully recovered from
  self-inflicted damage).
- The persistent `.git/ORIG_HEAD.lock` warning surfaced (same FUSE
  EPERM pattern from prior ticks) — non-blocking, pull succeeded.
- The two preceding scheduled worker-ticks today (01:32:44Z and
  05:07:42Z) ran in different sandbox sessions (funny-eloquent-newton
  and lucid-dazzling-brahmagupta respectively) whose virtiofs mounts
  carried stale `refs/remotes/origin/main.lock.*` files that the
  sandbox could not unlink (EPERM). This session
  (sharp-magical-meitner) is a fresh virtiofs mount that does not
  carry those particular stale refs, so the pull succeeded
  first-pass.

## Inputs

- Pool size: **1895** (records on disk with non-empty `source_url`
  AND non-empty `source_hash`; unchanged from b0602 — no intervening
  jiw activity that grew the pool since the last worker-tick).
- Seed: `phase8-reverify-2026-05-12-b0603` (tick-suffixed per the
  b0578+ enhancement; first sample under this seed; first sample of
  UTC date 2026-05-12).
- Sample size: **8** (= MAX_BATCH cap; ceil(0.01 × 1895) = 19 →
  capped at 8).
- Out-of-band re-fetches: **0** (no URLError retries needed;
  CA-chain preload via `scripts/certs/rapidssl_tls_rsa_ca_g1.pem`
  continues to resolve first-pass — now **twelve consecutive
  worker-ticks**).

## Results — 5 match / 3 drift / 0 truncated_prefix / 0 fetch_error

| Verdict | Count | Records |
|---------|------:|---------|
| match (real) | 5 | act-zm-financial-intelligence-centre-act-2010 (zambialii.org `/akn/.../source.pdf` — 1,541,618 B = 1.47 MB); si-zm-2006-003-banking-and-financial-services-microfinance-regulations-2006 (zambialii.org `/akn/.../source.pdf` — 3,913,168 B = 3.73 MB; **NEW LARGEST akn/source.pdf SI sample observed in Phase 8 series — 3.73 MB displaces b0602's 2.38 MB by a wide margin**); si-zm-2019-053-national-heritage-conservation-commission-tarbuttite-site-national-monument-prov (zambialii.org `/akn/.../source.pdf` — 11,703 B; **smallest akn/source.pdf SI sample observed**); act-zm-2019-007-food-safety-act-2019 (www.parliament.gov.zm `/acts/` — 180,310 B); si-zm-2021-106-value-added-tax-electronic-fiscal-devices-amendment-regulations-2021 (zambialii.org `/akn/.../source.pdf` — 85,294 B) |
| match_truncated_prefix | 0 | — |
| drift | 3 | act-zm-1973-039-forests-act-1973 (zambialii.org `/akn/zm/act/1973/39/eng@1996-12-31` — 242,508 B); act-zm-1996-029-small-enterprise-development-act-1996 (zambialii.org `/akn/zm/act/1996/29/eng@1996-12-31` — 183,934 B); act-zm-1980-005-supplementary-appropriation-1978-act-1980 (zambialii.org `/akn/zm/act/1980/5/eng@1980-04-11` — 38,765 B) |
| fetch_error | 0 | — |

## TLS / CA-chain note

The four zambialii.org-AKN `/source.pdf` fetches plus the one
www.parliament.gov.zm `/acts/` PDF fetch plus the three zambialii.org
AKN-HTML `/eng@*` Act fetches all verified successfully on the first
attempt because the inline runner's `build_ssl_context()` pre-loaded
`scripts/certs/rapidssl_tls_rsa_ca_g1.pem`. No retry pass needed.
Standing recommendation #4 (b0586) operationally confirmed across
**twelve consecutive worker-ticks** now (b0586 with retry,
b0587..b0603 first-pass).

## Cohort-level cumulative tally (post-b0603, 41 ticks)

| Cohort | Pre-b0603 | Δ b0603 | Post-b0603 |
|--------|----------:|--------:|-----------:|
| zambialii.org/akn/.../act-or-SI-HTML drift (Acts + SIs with `/eng@<date>` suffix) | 116/116 | +3/+3 | **119/119** ‡‡ |
| zambialii.org/akn/.../source.pdf match (Acts/SIs) | 33/33 | +4/+4 | **37/37** ‡‡‡ |
| zambialii.org/akn/.../source.pdf match (Judgments) | 1/1 | 0/0 | 1/1 |
| media.zambialii.org/media/legislation/ legacy-PDF match | 5/5 | 0/0 | 5/5 |
| commons.laws.africa /media/publication/ legacy-PDF match | 1/1 | 0/0 | 1/1 |
| parliament.gov.zm static PDF match (real-match `/acts/` family) | 113/113 | +1/+1 | 114/114 |
| parliament.gov.zm /amendment_act/ static PDF match | 5/5 | 0/0 | 5/5 |
| parliament.gov.zm static PDF real DRIFT | 0/120 | 0/+1 | 0/121 |
| parliament.gov.zm static PDF truncated_stored_hash_false_drift | 4/120 | 0/+1 | 4/121 |
| zambialii judgment-akn HTML drift (ZMCC + ZMSC + ZMHC consolidated) | 13/21 | 0/0 | 13/21 |
| zambialii bare-AKN-path drift (SI sub-cohort, no `/eng@` suffix) | 10/10 | 0/0 | 10/10 |
| `www.zambialii.org` host-prefix AKN-HTML drift sub-form | 2/2 | 0/0 | 2/2 |
| Parliament-node landing drift | 1/2 | 0/0 | 1/2 |
| judiciaryzambia.com CoA-judgment HTML drift | 1/1 | 0/0 | 1/1 |
| Stable-PDF combined supercohort (parliament `/acts/` + zambialii akn `/source.pdf` + media.zambialii legacy + commons.laws.africa + parliament `/amendment_act/`) — real-drift basis | 157/161 | +5/+5 | **162/166** ‡ |

‡ Stable-PDF supercohort now 162/166 across 41 ticks. The 4
  cumulative non-real-matches remain the four truncated-stored-hash
  false drifts (b0570 act-zm-2020-011; b0578 act-zm-2020-019; b0581
  act-zm-2020-016; b0585 act-zm-2020-024). **Real drift count on the
  stable-PDF supercohort remains zero across 41 ticks.**

‡‡ AKN-HTML `/eng@`-suffix Act-or-SI drift cohort now stands at
  **119/119** — three new Act drifts in b0603 (1973 forests, 1996
  small-enterprise, 1980 supplementary-appropriation). 100% drift rate
  preserved across 119 samples.

‡‡‡ zambialii akn `/source.pdf` Act-or-SI match cohort now stands at
  **37/37** — four new matches in b0603 (1 Act, 3 SIs). 100% match
  rate preserved across 37 samples.

## Notable observations (b0603)

1. **NEW LARGEST `akn/source.pdf` SI sample observed (3.73 MB).**
   `si-zm-2006-003-banking-and-financial-services-microfinance-
   regulations-2006` at
   `zambialii.org/akn/zm/act/si/2006/3/eng@2006-01-30/source.pdf`
   is **3,913,168 B (3.73 MB)** — the largest `akn/source.pdf` SI
   sample observed in the Phase 8 series, displacing b0602's
   `si-zm-2018-065-environmental-management-EPR` (2.38 MB) by a
   wide margin. Matched first-pass. Reaffirms that the akn
   `/source.pdf` SI path is hash-stable across an even wider size
   range than previously observed (11.7 KB to 3.73 MB observed).

2. **Smallest `akn/source.pdf` SI sample observed (11.7 KB).**
   `si-zm-2019-053-national-heritage-conservation-commission-
   tarbuttite-site-national-monument-prov` at
   `zambialii.org/akn/zm/act/si/2019/53/eng@2019-09-06/source.pdf`
   is **11,703 B** — the smallest `akn/source.pdf` SI sample
   observed. Matched first-pass.

3. **Three AKN-HTML `/eng@`-suffix Act drifts in a single tick.**
   `act-zm-1973-039-forests-act-1973`,
   `act-zm-1996-029-small-enterprise-development-act-1996`, and
   `act-zm-1980-005-supplementary-appropriation-1978-act-1980` all
   drifted on re-fetch. Cohort extends 116/116 → 119/119. The
   1973-vintage `forests-act-1973` is not a new oldest-vintage
   drift (b0601 already observed 1914-vintage
   `authentication-of-documents-act-1914`), but the
   1980-vintage `supplementary-appropriation-1978-act-1980` is the
   third pre-1990 AKN-HTML Act drift sampled in Phase 8 (after
   b0600's 1967 tobacco-levy and b0601's 1914 + 1960 cohort).
   Pattern: AKN-HTML rendering pipeline is non-deterministic across
   all vintages.

4. **Drift composition (3:5) is consistent with the 41-tick
   standing finding** — stable PDFs hash deterministically; AKN
   HTML renders dynamically. All three drifts are from the AKN-HTML
   `/eng@`-suffix Act-or-SI cohort.

5. **First successful worker-tick of UTC date 2026-05-12.** Two
   prior scheduled worker-tick attempts today (01:32:44Z and
   05:07:42Z) halted on `git pull --ff-only` failure due to stale
   `refs/remotes/origin/main.lock.*` files in their sandbox
   virtiofs mounts (sandbox EPERM blocks unlink, as observed since
   b0334+). This session's virtiofs mount does not carry those
   particular stale refs, so the pull succeeded first-pass.
   Operator action remains advisable to clean up stale refs on the
   host side (see worker.log 2026-05-12T05:07:42Z recommendation),
   but the worker is not blocked while the rotating virtiofs mount
   strategy continues to produce clean sessions.

6. **Pool size unchanged from b0602 (1895).** No intervening jiw
   activity since the b0602 worker-tick (the b0602-jiw diagnostic
   at 23:11Z did not insert any new records — FTS5 corruption
   continues to block jiw writes; 19th consecutive blocked jiw
   tick).

7. **Pre-existing FTS5 records_fts_data corruption (observed by
   jiw b0587..b0594..b0597..b0598..b0602) remains independent of
   Phase 8 reverify** — Phase 8 does not read or write
   `corpus.sqlite` at all, so FTS5 corruption does not affect this
   tick's verdict. Repair-worker manifest escalation remains
   outstanding (still 19 consecutive jiw ticks blocked as of last
   jiw observation).

## Integrity check

- JSON report well-formed and parseable — **PASS**.
- All required summary keys present (batch, phase, parser_version,
  seed, pool_size, sample_size, sample_rate, max_batch, results,
  match_count, drift_count, truncated_prefix_count,
  fetch_error_count, fetches, retry_fetches, started_at,
  completed_at) — **PASS**.
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
reported analytically; per the 41-tick standing finding they do NOT
indicate corpus integrity failure — they indicate upstream HTML
rendering-pipeline non-determinism on the AKN-HTML `/eng@`-suffix
resolver, and the underlying legal text is unchanged. The stable-PDF
supercohort (162/166 real-matches across 41 ticks; 4 truncated-prefix
false drifts; **zero real drifts**) continues to demonstrate that the
stored corpus content is faithful to the upstream sources.

## Budget impact

- Fetches this tick: **8** sample-record attempts (1 to
  www.parliament.gov.zm at 2 s between requests, 7 to zambialii.org
  at 5 s between requests). No retries needed.
- Retry fetches this tick: **0**.
- Cumulative today (pre-b0603, 2026-05-12, worker-tick channel): 0/2000.
- Cumulative today (post-b0603, 2026-05-12, worker-tick channel):
  **8 / 2000** (0.4%).
- Wall-clock duration: ~40 seconds for the fetch loop; well within
  the 20-minute cap.

## Outputs

- `reports/batch-0604-reverify.json` (deterministic JSON output).
- `reports/batch-0604.md` (this file).
- Append-only updates to `worker.log`, `costs.log`, `provenance.log`.
- No records written, modified, or deleted.
- No schema or YAML changes.

## Standing recommendations (carried forward — operator decision pending)

1. **Truncated-stored-hash backfill sweep** (b0578/b0579/b0581/b0585
   standing): unchanged across 41 ticks. Four 2020-vintage
   parliament-pdf-v1.2 records have truncated stored hashes that
   produce a stable false-drift verdict; backfilling the full-length
   sha256 would resolve them. Operator approval required.
2. **Phase 8 endpoint refinement** (b0565/b0567/b0569 standing,
   **strengthened b0603**): with 162/166 stable-PDF and 119/119 +
   13/21 + 10/10 + 2/2 + 1/2 HTML/AKN drift cohorts now characterised
   across 41 ticks (AKN-HTML `/eng@` Act-or-SI cohort still at 100%
   drift on 119 samples), operator could consider option (a)
   text-extraction-stable hashing or (b) restricting Phase 8 to
   stable-PDF to eliminate the HTML rendering noise. Operator
   approval required.
3. **Divergent-content duplicate-ID Act records** (b0578 standing):
   five IDs known with multiple divergent record files. Operator
   approval required to canonicalise or split IDs.
4. **Phase 8 inline-runner CA-bundle parity** (b0586 standing,
   operationally confirmed b0587..b0603 across **twelve consecutive
   worker-ticks**): consider landing the `scripts/certs/*.pem`
   preload into the canonical `scripts/batch_NNNN_phase8_reverify.py`
   template the next time the baseline is refreshed.
5. **Stray `.git/refs/heads/main.lock.bak.*` ref backups**
   (b0588 first observation): persists; sandbox cannot unlink.
   No new observations this tick.
6. **`www.zambialii.org`-prefixed AKN-HTML record cluster audit**
   (b0589 standing, strengthened b0601): unchanged this tick — no
   `www.zambialii.org` host-prefix samples drawn. Two-sample cohort
   from b0601 stands.
7. **`cap-N` Laws-of-Zambia Chapter-number ID form characterisation**
   (b0595 standing, three-sample confirmation b0600): unchanged
   this tick — no `cap-N` samples drawn.
8. **`loz-` prefix Laws-of-Zambia ID form characterisation**
   (b0599 standing): unchanged this tick — no `loz-` prefix samples
   drawn. Two-sample confirmation from b0599 stands.
9. **judiciaryzambia.com CoA-record canonical-source decision**
   (b0596 standing): unchanged this tick — no CoA samples drawn.
10. **FTS5 records_fts_data corruption — repair-worker manifest
    escalation** (b0596 standing; b0598-jiw confirmed full
    write-and-rebuild blockage with workaround falsification;
    b0602-jiw confirmed parallel-fts5-table workaround FALSIFIED):
    unchanged this tick — Phase 8 reverify is independent of
    `corpus.sqlite`. Operator action required (19 consecutive jiw
    ticks blocked as of last jiw observation).
11. **Parliament-node landing reclassification** (b0601 standing):
    /node/ family at 1/2 drift after 41 ticks; further samples
    needed before pattern is conclusive. Unchanged this tick — no
    /node/ sample drawn.
12. **Stale `refs/remotes/origin/main.lock.*` cleanup on host**
    (b0603 new observation): two scheduled worker-tick attempts
    today (01:32Z, 05:07Z) halted on `git pull --ff-only` failure
    due to sandbox EPERM on stale refs in their virtiofs mounts.
    This session's virtiofs mount produced a clean pull. Operator
    may wish to run on the host:
    `cd ~/KateWestonCorpus/corpus && rm -f .git/refs/remotes/origin/main.lock.* .git/refs/remotes/origin/_stale_main_pf_* .git/refs/remotes/origin/test_file .git/objects/maintenance.lock && git fetch --prune origin`
    to fully reclaim the locks from the next sandbox session.

None of the above were actioned this tick — Phase 8 reverify worker
is read-only on records by design.
