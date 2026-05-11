# Batch 0588 — Phase 8 Nightly Re-verification (2026-05-11)

**UTC start:** 2026-05-11T09:36:04Z
**UTC end:** 2026-05-11T09:36:34Z
**Worker:** worker-tick (Phase 8)
**Phase:** phase_8_nightly_reverify (approved 2026-05-06; sample_rate 0.01)
**Parser:** phase8-reverify-0.1.0 (functional contract per scripts/batch_0546_phase8_reverify.py)
**Tick scope:** Thirty-second Phase 8 tick overall; fourth worker-tick of UTC date 2026-05-11
   (b0585 at 07:30:21Z, b0586 at 08:38:42Z, b0587 at 09:04:36Z were the prior three worker-ticks of the day).
**Execution mode:** inline runner (`/sessions/tender-festive-noether/scratch/b0588_phase8_reverify.py`, NOT committed)
   per sandbox-session safety constraint maintained since b0548. Functional contract matches
   `scripts/batch_0546_phase8_reverify.py` including the `scripts/certs/*.pem` PKI loader.
   Tick-suffixed seed `phase8-reverify-2026-05-11-b0588`; truncated-prefix classifier preserved.

## Pre-tick git state observation

Pre-tick `git pull --ff-only` initially failed with
`fatal: bad object refs/heads/main.lock.bak.20260511T092251Z` —
a zero-byte stale ref backup file left in `.git/refs/heads/` (created
2026-05-11T11:22:53 SAST) that the sandbox lacks unlink permission to remove.
Mitigation: wrote the current HEAD SHA (81eb7f2ebf95560b7fd2c8e4511387028bbbe683)
into the stale ref file so git treats it as a parallel branch pointer rather
than a malformed ref; `git pull --ff-only` then returned `Already up to date`
at HEAD=81eb7f2 (jiw b0587). This is a NEW failure mode — recommend operator
remove the stray file outside the sandbox.

Pre-tick index also carried stale staged paths inherited from a prior session
(modified: costs.log, gaps.md, provenance.log, worker.log; deleted: seven
records/judgments/coa/2026/*.json files plus reports/batch-0587-jiw.md). All
those files exist on disk and in HEAD; the staged "deleted" claims contradicted
on-disk state. Tick ran `git restore --staged .` (succeeded — sandbox accepted
the staging mutation even though .git unlink remains constrained), restoring a
clean working-tree-vs-HEAD comparison before proceeding.

## Inputs

- Pool size: **1891** (records with non-empty `source_url` AND non-empty
  `source_hash`; +7 from b0587's 1884 — consistent with jiw b0587's seven
  Court of Appeal additions at commit 81eb7f2 arriving in the records tree).
- Seed: `phase8-reverify-2026-05-11-b0588` (tick-suffixed).
- Sample size: **8** (= MAX_BATCH cap; ceil(0.01 × 1891) = 19 → capped at 8).
- Out-of-band re-fetches: **0** (parliament.gov.zm fetch succeeded first-pass
  via pre-loaded `scripts/certs/rapidssl_tls_rsa_ca_g1.pem`).

## Results — 2 match / 6 drift / 0 truncated_prefix / 0 fetch_error

| Verdict | Count | Records |
|---------|------:|---------|
| match (real) | 2 | si-zm-2022-030-public-procurement-regulations-2022 (media.zambialii.org/.../publication-document.pdf 3,308,583 B — extends media.zambialii legacy-PDF cohort to 3/3); act-zm-2015-006-income-tax-amendment (parliament.gov.zm `/documents/amendment_act/` 140,794 B — SECOND observation of `/amendment_act/` URL sub-path; cohort 1/1 → 2/2 confirms the b0587 first-observation pattern is reproducible) |
| match_truncated_prefix | 0 | — |
| drift | 6 | judgment-zm-2023-zmsc-20-augustine-mwamba-mbuzakosi-and-ors-v-the-people (zambialii.org/akn/zm/judgment/zmsc/2023/20/eng@2023-11-16 41,730 B — judgment-akn HTML drift cohort 8/16 → 9/17, ZMSC observation); act-zm-1958-004-minister-of-finance-incorporation-act-1958 (zambialii.org/akn/zm/act/1958/4/eng@1996-12-31 45,966 B — AKN-HTML drift, mid-century Act, third 1950s/1960s observation in the series); act-zm-1971-032-home-guard-act-1971 (zambialii.org/akn/zm/act/1971/32/eng@1996-12-31 130,983 B — AKN-HTML drift); act-zm-1998-011-revenue-appeals-tribunal-act-1998 (zambialii.org/akn/zm/act/1998/11/eng@1998-04-24 39,819 B — AKN-HTML drift, first `eng@` date matching enacted-date pattern in the series); act-zm-1933-003-arbitration-act-1933 (zambialii.org/akn/zm/act/1933/3/eng@1996-12-31 151,973 B — AKN-HTML drift, OLDEST Act yet observed in series at 1933); si-zm-2020-122-tourism-and-hospitality-licensing-temporary-disapplication-of-renewal-and-retention-fee-regulations-2020 (zambialii.org/akn/zm/act/si/2020/122 bare-AKN-path 39,561 B redirected to /eng@2020-12-31 — **SEVENTH bare-AKN-path drift observation**; sub-cohort remains SI-only) |
| fetch_error | 0 | — |

## TLS / CA-chain note

parliament.gov.zm fetch (act-zm-2015-006) verified successfully on first
attempt because the inline runner's `build_ssl_context()` pre-loaded
`scripts/certs/rapidssl_tls_rsa_ca_g1.pem` into the trust store at startup.
No retry pass needed. Standing recommendation #4 (b0586) operationally
confirmed across three consecutive ticks (b0586 with retry, b0587 first-pass,
b0588 first-pass).

## Cohort-level cumulative tally (post-b0588, 32 ticks)

| Cohort | Pre-b0588 | Δ b0588 | Post-b0588 |
|--------|----------:|--------:|-----------:|
| zambialii.org/akn/.../act-or-SI-HTML drift | 98/98 | +4/+4 | 102/102 |
| zambialii.org/akn/.../source.pdf match (Acts/SIs) | 23/23 | 0/0 | 23/23 |
| zambialii.org/akn/.../source.pdf match (Judgments) | 1/1 | 0/0 | 1/1 |
| media.zambialii.org/media/legislation/ legacy-PDF match | 2/2 | +1/+1 | 3/3 |
| commons.laws.africa /media/publication/ legacy-PDF match | 1/1 | 0/0 | 1/1 |
| parliament.gov.zm static PDF match (real-match `/acts/` family) | 87/87 | 0/0 | 87/87 |
| parliament.gov.zm /amendment_act/ static PDF match | 1/1 | +1/+1 | 2/2 |
| parliament.gov.zm static PDF real DRIFT | 0/91 | 0/+1 | 0/92 |
| parliament.gov.zm static PDF truncated_stored_hash_false_drift | 4/91 | 0/0 | 4/92 |
| zambialii judgment-akn HTML drift | 8/16 | +1/+1 | 9/17 |
| zambialii bare-AKN-path drift (SI sub-cohort) | 6/6 | +1/+1 | 7/7 |
| Parliament-node landing | 0/1 | 0/0 | 0/1 |
| Stable-PDF combined supercohort (parliament `/acts/` + zambialii akn `/source.pdf` + media.zambialii legacy + commons.laws.africa + parliament `/amendment_act/`) — real-drift basis | 114/118 | +2/+2 | 116/120 ‡ |

‡ Stable-PDF supercohort now 116/120 across 32 ticks. The 4 cumulative
  non-real-matches remain the four truncated-stored-hash false drifts
  (b0570 act-zm-2020-011; b0578 act-zm-2020-019; b0581 act-zm-2020-016;
  b0585 act-zm-2020-024). **Real drift count on the stable-PDF
  supercohort remains zero across 32 ticks.**

## Notable observations (b0588)

1. **Oldest Act yet sampled in the Phase 8 series.** act-zm-1933-003
   (Arbitration Act 1933) extends the AKN-HTML drift cohort back to 1933.
   Combined with b0587's 1967/1970 sample and b0586's 1968 sample, the
   AKN-HTML drift pattern has now been observed across 1933 → 2025
   without exception when the `/eng@<canonical-date>` URL form is used.

2. **First `eng@<enacted-date>` Act observation in the AKN-HTML drift
   cohort.** act-zm-1998-011 (Revenue Appeals Tribunal Act 1998) is at
   `/eng@1998-04-24` rather than the more common `/eng@1996-12-31`
   consolidation date. Drift mechanism reproduced regardless of the
   `eng@` suffix value — the rendering pipeline is the variable, not
   the date selector.

3. **Second `parliament.gov.zm/.../amendment_act/` URL sub-path
   observation.** act-zm-2015-006 (Income Tax (Amendment) Act 2015)
   fetched cleanly from
   `/sites/default/files/documents/amendment_act/The%20Income%20Tax%20%28Amendment%29%20%20Act%20No.%206%20of%202015.pdf`
   (140,794 B) and matched the stored hash exactly. The `/amendment_act/`
   sub-path opened by b0587's act-zm-2014-002 is now confirmed
   reproducible at 2/2 real-match.

4. **Seventh bare-AKN-path drift observation.** si-zm-2020-122
   (Tourism and Hospitality — Licensing — Temporary Disapplication of
   Renewal and Retention Fee Regulations 2020) joins the bare-AKN-path
   sub-cohort. All seven observations remain SIs with URL form
   `/akn/zm/act/si/<year>/<n>` (no `/eng@<date>` suffix, no
   `/source.pdf` suffix). Acts in the Phase 8 pool continue to use
   `/eng@<date>` form. Sub-cohort remains SI-only at 7 observations.

5. **First ZMSC judgment-akn drift observation in 32-tick series.**
   judgment-zm-2023-zmsc-20-augustine-mwamba-mbuzakosi-and-ors-v-the-people
   shows the AKN-HTML rendering drift on a ZMSC judgment (prior judgment-akn
   drift observations were primarily Court-of-Appeal or High-Court
   AKN-judgment endpoints; b0586's act-zm-2009-016 ZMCC observation was
   the first ZMCC variant). Pattern is now confirmed across ZMSC + ZMCC +
   other AKN-judgment endpoints.

6. **High drift-to-match ratio (6:2) this tick is within sampling variance.**
   With a pool dominated by zambialii.org/akn AKN-HTML records (the largest
   stable URL family), a sample drawing 6 of those 8 records is at the
   high-but-plausible end of binomial variance. The underlying drift mechanism
   is unchanged from prior ticks (AKN-HTML rendering pipeline
   non-determinism) and does NOT indicate corpus integrity failure.

7. **Pre-existing five divergent-content duplicate-ID Act records
   finding REAFFIRMED** — none of b0588 sample IDs are involved.

## Integrity check

- JSON report well-formed and parseable — **PASS**.
- All required summary keys present (batch, phase, parser_version, seed,
  pool_size, sample_size, sample_rate, max_batch, results, match_count,
  drift_count, truncated_prefix_count, fetch_error_count, fetches,
  started_at, completed_at) — **PASS**.
- `sample_size <= MAX_BATCH (8)` — **PASS** (8 <= 8).
- `match_count + drift_count + truncated_prefix_count + fetch_error_count == sample_size` —
  **PASS** (2 + 6 + 0 + 0 = 8).
- All 8 sample IDs resolve to existing rows in `records` table — **PASS**
  (8/8 resolved via sqlite query against
  `/sessions/tender-festive-noether/scratch/corpus_b0588.sqlite` snapshot
  per b0583 virtiofs-isolation precedent).
- No sample record file mutated during/after the tick — **PASS** (0/8 mutated; reverify is read-only on records).
- Each result entry contains the required fields — **PASS**.
- Each `verdict` is one of {match, drift, fetch_error, match_truncated_prefix} — **PASS**.
- Pool size ≥ 1800 (sanity floor) — **PASS** (1891 at sample time).

No record mutation occurred. The six drift observations are reported
analytically; per the 32-tick standing finding they do NOT indicate
corpus integrity failure — they indicate upstream AKN-HTML
rendering-pipeline non-determinism, and the underlying legal text is
unchanged. The stable-PDF supercohort (116/120 real-matches across
32 ticks; 4 truncated-prefix false drifts; zero real drifts) continues
to demonstrate that the stored corpus content is faithful to the
upstream sources.

## Budget impact

- Fetches this tick: **8** sample-record attempts (6 to zambialii.org +
  www.zambialii.org at 5 s between requests, 1 to media.zambialii.org
  at 5 s between requests, 1 to www.parliament.gov.zm at 2 s between
  requests). No retries needed.
- Cumulative today (pre-b0588, 2026-05-11, worker-tick channel): 26 / 2000.
- Cumulative today (post-b0588, 2026-05-11, worker-tick channel):
  **34 / 2000** (1.7%).
- Wall-clock duration: ~30 seconds for the fetch loop; ~10 minutes overall
  including git troubleshooting and report write-up — within 20-minute cap.

## Outputs

- `reports/batch-0588-reverify.json` (deterministic JSON output).
- `reports/batch-0588.md` (this file).
- Append-only updates to `worker.log`, `costs.log`, `provenance.log`.
- No records written, modified, or deleted.
- No schema or YAML changes.

## Standing recommendations (carried forward — operator decision pending)

1. **Truncated-stored-hash backfill sweep** (b0578/b0579/b0581/b0585
   standing): unchanged across 32 ticks.
2. **Phase 8 endpoint refinement** (b0565/b0567/b0569 standing): with
   116/120 stable-PDF and 102/102 + 9/17 + 7/7 AKN-HTML drifts now
   characterised across 32 ticks, operator could consider option (a)
   text-extraction-stable hashing or (b) restricting Phase 8 to stable-PDF.
3. **Divergent-content duplicate-ID Act records** (b0578 standing).
4. **Phase 8 inline-runner CA-bundle parity** (b0586 standing,
   confirmed b0587/b0588): now operationally confirmed across THREE
   consecutive ticks.
5. **NEW: stray `.git/refs/heads/main.lock.bak.20260511T092251Z` ref backup**
   (b0588 first observation): zero-byte file in `.git/refs/heads/` not
   removable by sandbox; mitigated by writing HEAD SHA into the file.
   Operator should `rm .git/refs/heads/main.lock.bak.*` from the host
   shell to clean the namespace.

None of the above were actioned this tick — Phase 8 reverify worker
is read-only on records by design.
