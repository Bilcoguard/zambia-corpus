# Batch 0595 — Phase 8 Nightly Re-verification (2026-05-11)

**UTC start:** 2026-05-11T17:08:46Z (sample drawn as b0591)
**UTC end:** 2026-05-11T17:09:14Z (sample completed as b0591)
**Renumbered:** b0591 → b0595 due to mass collision with judgment-ingestion-worker
  activity that landed between sample-draw and report-commit:
    - b0591-jiw (commit e505981, 17:23:26Z, CoA pages 4 overflow + page 5 partial, +3 records);
    - b0592-jiw (commit 6bddfdf, page 5 remainder, FTS5-blocked);
    - b0593+repair (commit b85bb74, page 6 sweep, FTS5-blocked);
    - b0594-jiw (commit c48af8d, 20:17:20Z, page 7, FTS5-blocked, 4 scanned-PDF deferreds).
  Same b0585 renumbering precedent extended one step (b0583 → b0585 → b0595 here).
  Underlying sample seed kept as `phase8-reverify-2026-05-11-b0591` to preserve
  sample-set reproducibility. No additional fetches consumed during renumber;
  sample results unchanged (match=6, drift=2, trunc=0, err=0).
**Worker:** worker-tick (Phase 8)
**Phase:** phase_8_nightly_reverify (approved 2026-05-06; sample_rate 0.01)
**Parser:** phase8-reverify-0.1.0 (functional contract per scripts/batch_0546_phase8_reverify.py)
**Tick scope:** Thirty-fourth Phase 8 tick overall; sixth worker-tick of UTC date
  2026-05-11 (b0585 at 07:30:21Z, b0586 at 08:38:42Z, b0587 at 09:05:07Z,
  b0588 at 09:36:34Z, b0589 at 10:05:18Z were the prior five worker-ticks).
**Execution mode:** inline runner (`/tmp/scratch/b0591_phase8_reverify.py (sample seed name preserved; renumber affects only batch label)`,
  NOT committed) per sandbox-session safety constraint maintained since b0548.
  Functional contract matches `scripts/batch_0546_phase8_reverify.py`
  including the `scripts/certs/*.pem` PKI loader, tick-suffixed seed
  (`phase8-reverify-2026-05-11-b0591`), and prefix-startswith
  truncated-stored-hash detector.

## Pre-tick git state

- `git pull --ff-only` returned `Already up to date` at HEAD=ec0371a
  (jiw b0590 CoA page-4 ingestion, 1 record written).
- The persistent `.git/objects/maintenance.lock` warning surfaced again
  (same FUSE EPERM pattern from b011-b020 + b0579..b0589) — non-blocking,
  the pull still succeeded.
- Working tree carried untracked stale paths from prior ticks; no
  records-tree mutation.

## Inputs

- Pool size: **1892** (records on disk with non-empty `source_url` AND
  non-empty `source_hash`; +1 from b0589's 1891 — accounted for by jiw
  b0590 CoA record `judgment-zm-2024-coa-...-musonda-chizinga-v-capstone-management`
  insertion).
- Seed: `phase8-reverify-2026-05-11-b0591` (tick-suffixed).
- Sample size: **8** (= MAX_BATCH cap; ceil(0.01 × 1892) = 19 → capped at 8).
- Out-of-band re-fetches: **0** (no parliament.gov.zm SSL retries needed;
  CA-chain preload via `scripts/certs/rapidssl_tls_rsa_ca_g1.pem` continues
  to resolve first-pass per the b0587/b0588/b0589 confirmed pattern —
  now FIVE consecutive ticks).

## Results — 6 match / 2 drift / 0 truncated_prefix / 0 fetch_error

| Verdict | Count | Records |
|---------|------:|---------|
| match (real) | 6 | act-zm-2018-022-the-appropriation-act-2018 (parliament.gov.zm `/.../acts/` 73,126 B — stable-PDF); si-zm-2017-070-income-tax-african-management-services-company-approval-and-exemption-order-2017 (zambialii.org `/akn/zm/act/si/2017/70/eng@2017-09-29/source.pdf` 147,909 B — redirects to media.zambialii.org legacy-PDF host); act-zm-cap-184-lands-act (parliament.gov.zm `/.../acts/Lands%20Act.pdf` 370,573 B — stable-PDF; **FIRST `cap-N` ID-form record sampled in 34-tick Phase 8 series** — Cap. 184 is a Laws of Zambia chapter number rather than a year-vintage Act number, distinct from all prior Act samples); si-zm-1983-006-income-tax-intersomer-spa-exemption-order-1983 (zambialii.org `/akn/zm/act/si/1983/6/eng@1983-01-14/source.pdf` 109,532 B); act-zm-2015-011-mines-and-minerals (parliament.gov.zm `/.../acts/` 185,049 B); si-zm-1993-002-income-tax-foreign-organisations-approval-and-exemption-order-1993 (zambialii.org `/akn/zm/act/si/1993/2/eng@1993-01-15/source.pdf` 170,593 B) |
| match_truncated_prefix | 0 | — |
| drift | 2 | act-zm-2007-009-appropriation-act (zambialii.org `/akn/zm/act/2007/9/eng@2007-04-13` 41,003 B — AKN-HTML drift cohort, `/eng@<enacted-date>` form, **SECOND `/eng@<enacted-date>` non-1996-consolidation AKN-HTML drift observation after b0588 act-zm-1998-011**); act-zm-1929-016-dairies-and-dairy-produce-act-1929 (zambialii.org `/akn/zm/act/1929/16/eng@1996-12-31` 48,076 B — AKN-HTML drift, **NEW OLDEST Act yet sampled in Phase 8 series**, displacing b0588's act-zm-1933-003 from the title; 1996-12-31 is the standard consolidation date suffix) |
| fetch_error | 0 | — |

## TLS / CA-chain note

Both parliament.gov.zm fetches (act-zm-2018-022, act-zm-cap-184-lands-act,
act-zm-2015-011) verified successfully on first attempt because the inline
runner's `build_ssl_context()` pre-loaded
`scripts/certs/rapidssl_tls_rsa_ca_g1.pem`. No retry pass needed.
Standing recommendation #4 (b0586) operationally confirmed across **five
consecutive ticks** now (b0586 with retry, b0587/b0588/b0589/b0591
first-pass; b0590 was a jiw tick that did not invoke phase-8 reverify).

## Cohort-level cumulative tally (post-b0591, 34 ticks)

| Cohort | Pre-b0591 | Δ b0591 | Post-b0591 |
|--------|----------:|--------:|-----------:|
| zambialii.org/akn/.../act-or-SI-HTML drift (Acts + SIs with `/eng@<date>` suffix) | 104/104 | +2/+2 | 106/106 |
| zambialii.org/akn/.../source.pdf match (Acts/SIs) | 25/25 | +3/+3 | 28/28 |
| zambialii.org/akn/.../source.pdf match (Judgments) | 1/1 | 0/0 | 1/1 |
| media.zambialii.org/media/legislation/ legacy-PDF match | 3/3 | 0/0 | 3/3 |
| commons.laws.africa /media/publication/ legacy-PDF match | 1/1 | 0/0 | 1/1 |
| parliament.gov.zm static PDF match (real-match `/acts/` family) | 90/90 | +3/+3 | 93/93 |
| parliament.gov.zm /amendment_act/ static PDF match | 3/3 | 0/0 | 3/3 |
| parliament.gov.zm static PDF real DRIFT | 0/96 | 0/+3 | 0/99 |
| parliament.gov.zm static PDF truncated_stored_hash_false_drift | 4/96 | 0/0 | 4/99 |
| zambialii judgment-akn HTML drift | 9/17 | 0/0 | 9/17 |
| zambialii bare-AKN-path drift (SI sub-cohort, no `/eng@` suffix) | 7/7 | 0/0 | 7/7 |
| `www.zambialii.org` host-prefix AKN-HTML drift sub-form | 1/1 | 0/0 | 1/1 |
| Parliament-node landing | 0/1 | 0/0 | 0/1 |
| Stable-PDF combined supercohort (parliament `/acts/` + zambialii akn `/source.pdf` + media.zambialii legacy + commons.laws.africa + parliament `/amendment_act/`) — real-drift basis | 122/126 | +6/+6 | 128/132 ‡ |

‡ Stable-PDF supercohort now 128/132 across 34 ticks. The 4 cumulative
  non-real-matches remain the four truncated-stored-hash false drifts
  (b0570 act-zm-2020-011; b0578 act-zm-2020-019; b0581 act-zm-2020-016;
  b0585 act-zm-2020-024). **Real drift count on the stable-PDF
  supercohort remains zero across 34 ticks.**

## Notable observations (b0591)

1. **NEW OLDEST Act yet sampled in Phase 8 series.** act-zm-1929-016
   (Dairies and Dairy Produce Act 1929) displaces b0588's act-zm-1933-003
   (Arbitration Act 1933) as the oldest-vintage Act sampled. Both share
   the `/eng@1996-12-31` consolidation-date AKN-HTML drift pattern —
   the 1996-12-31 suffix is the standard Laws of Zambia consolidation
   date applied to pre-1996 instruments. The drift mechanism is the same
   AKN-HTML rendering non-determinism; the underlying 1929 statute text
   is unchanged.

2. **FIRST `cap-N` ID-form record sampled.** act-zm-cap-184-lands-act
   is the first sampled record using the Laws-of-Zambia Chapter-number
   ID convention (Cap. 184 = Lands Act) rather than a `act-zm-<year>-<n>`
   form. The source URL is a clean parliament.gov.zm `/.../acts/Lands%20Act.pdf`
   stable-PDF and matched real-match first-pass. This observation
   confirms the Phase 8 reverify cohort tally correctly includes
   `cap-N` records in the stable-PDF supercohort denominator.

3. **SECOND `/eng@<enacted-date>` non-1996-consolidation AKN-HTML drift
   observation.** act-zm-2007-009 carries a `/eng@2007-04-13` enacted-date
   suffix (not the standard 1996-12-31 consolidation date). This pattern
   was first observed in b0588 (act-zm-1998-011 with `/eng@1998-04-24`)
   and is now reproducibly observed at 2/2 — the AKN-HTML drift cohort
   contains a mix of `/eng@1996-12-31` (consolidation-date) and
   `/eng@<actual-enacted-date>` sub-forms.

4. **High match ratio (6:2) consistent with stable-PDF dominance.**
   This tick's match-to-drift ratio (75%/25%) is in line with the running
   34-tick pool proportion. The match cohort split (3 parliament `/acts/`
   + 3 zambialii akn `/source.pdf`) is balanced.

5. **Standing recommendation #6 (b0589 `www.zambialii.org`-prefixed AKN
   cluster audit) not actioned this tick** — Phase 8 reverify is
   read-only on records by design; the standing recommendation continues
   to await operator decision.

6. **Pre-existing FTS5 records_fts_data corruption (observed by jiw
   b0587..b0590) is independent of Phase 8 reverify** — Phase 8 does
   not read or write `corpus.sqlite` at all, so FTS5 corruption does
   not affect this tick's verdict. Note for operator: FTS5 corruption
   remains a pending repair-worker task.

## Integrity check

- JSON report well-formed and parseable — **PASS**.
- All required summary keys present (batch, phase, parser_version, seed,
  pool_size, sample_size, sample_rate, max_batch, results, match_count,
  drift_count, truncated_prefix_count, fetch_error_count, fetches,
  retry_fetches, started_at, completed_at) — **PASS**.
- `sample_size <= MAX_BATCH (8)` — **PASS** (8 <= 8).
- `match_count + drift_count + truncated_prefix_count + fetch_error_count == sample_size` —
  **PASS** (6 + 2 + 0 + 0 = 8).
- All 8 sample IDs resolve to existing record files in `records/` — **PASS** (8/8 resolved).
- Each result entry contains the required fields — **PASS**.
- Each `verdict` is one of {match, drift, fetch_error, match_truncated_prefix} — **PASS**.
- Pool size ≥ 1800 (sanity floor) — **PASS** (1892 at sample time).
- No record mutation occurred this tick — **PASS** (0/8 mutated;
  `git status records/` shows no modified or deleted entries; reverify
  is read-only on records by design).

Note: `PRAGMA integrity_check` against the on-disk `corpus.sqlite` continues
to return `database disk image is malformed` from within the sandbox copy,
matching the b0583+ virtiofs-isolation precedent. Phase 8 reverify does NOT
read or write `corpus.sqlite`, so this pre-existing condition is
informational and does not affect this tick's integrity verdict.

No record mutation occurred. The two drift observations are reported
analytically; per the 34-tick standing finding they do NOT indicate
corpus integrity failure — they indicate upstream AKN-HTML rendering-pipeline
non-determinism, and the underlying legal text is unchanged. The stable-PDF
supercohort (128/132 real-matches across 34 ticks; 4 truncated-prefix false
drifts; zero real drifts) continues to demonstrate that the stored corpus
content is faithful to the upstream sources.

## Budget impact

- Fetches this tick: **8** sample-record attempts (3 to www.parliament.gov.zm
  at 2 s between requests, 5 to zambialii.org at 5 s between requests). No
  retries needed.
- Retry fetches this tick: **0**.
- Cumulative today (pre-b0591, 2026-05-11, worker-tick channel): 42 / 2000.
- Cumulative today (post-b0591, 2026-05-11, worker-tick channel):
  **50 / 2000** (2.5%).
- Wall-clock duration: ~28 seconds for the fetch loop; ~5 minutes overall
  including report write-up — well within the 20-minute cap.

## Outputs

- `reports/batch-0595-reverify.json` (deterministic JSON output;
  includes `renumber_note` field documenting the b0591→b0595 collision-rename).
- `reports/batch-0595.md` (this file).
- Append-only updates to `worker.log`, `costs.log`, `provenance.log`
  (under both b0591 — original draw — and b0595 — renumber — tags;
  same b0585 audit pattern).
- No records written, modified, or deleted.
- No schema or YAML changes.

## Standing recommendations (carried forward — operator decision pending)

1. **Truncated-stored-hash backfill sweep** (b0578/b0579/b0581/b0585
   standing): unchanged across 34 ticks. Four 2020-vintage parliament-pdf-v1.2
   records have truncated stored hashes that produce a stable false-drift
   verdict; backfilling the full-length sha256 would resolve them. Operator
   approval required.
2. **Phase 8 endpoint refinement** (b0565/b0567/b0569 standing): with
   128/132 stable-PDF and 106/106 + 9/17 + 7/7 + 1/1 AKN-HTML drifts now
   characterised across 34 ticks, operator could consider option (a)
   text-extraction-stable hashing or (b) restricting Phase 8 to stable-PDF
   to eliminate the AKN-HTML-rendering noise. Operator approval required.
3. **Divergent-content duplicate-ID Act records** (b0578 standing): five
   IDs known with multiple divergent record files. Operator approval
   required to canonicalise or split IDs.
4. **Phase 8 inline-runner CA-bundle parity** (b0586 standing, operationally
   confirmed b0587/b0588/b0589/b0591 across FIVE consecutive ticks):
   consider landing the `scripts/certs/*.pem` preload into the canonical
   `scripts/batch_NNNN_phase8_reverify.py` template the next time the
   baseline is refreshed.
5. **Stray `.git/refs/heads/main.lock.bak.20260511T092251Z` ref backup**
   (b0588 first observation): persists; sandbox cannot unlink. No new
   observations this tick.
6. **`www.zambialii.org`-prefixed AKN-HTML record cluster audit**
   (b0589 standing): unchanged this tick — operator may wish to audit
   `corpus.sqlite` for the count of `source_url LIKE 'https://www.zambialii.org/akn/%'`
   records to characterise the cluster size.
7. **NEW (b0591): `cap-N` Laws-of-Zambia Chapter-number ID form
   confirmation** — act-zm-cap-184-lands-act is the first phase-8 sample
   using this ID convention. The record verified real-match. No corrective
   action required; this observation is informational for the operator —
   the Phase 8 sample-coverage now includes `cap-N` records and they
   behave identically to `act-zm-<year>-<n>` records on the parliament
   `/acts/` endpoint.

None of the above were actioned this tick — Phase 8 reverify worker is
read-only on records by design.
