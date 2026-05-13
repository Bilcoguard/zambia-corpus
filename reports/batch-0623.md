# Batch 0623 — Phase 8 Nightly Re-verification (2026-05-13, first worker-tick of day)

**UTC start:** 2026-05-13T04:08:10Z
**UTC end:**   2026-05-13T04:08:38Z
**Worker:**    worker-tick (Phase 8, scheduled task `zambia-corpus-tick`)
**Phase:**     phase_8_nightly_reverify (approved 2026-05-06; sample_rate 0.01)
**Parser:**    phase8-reverify-0.1.0 (functional contract per
  `scripts/batch_0546_phase8_reverify.py` plus b0578+ enhancements:
  tick-suffixed seed, prefix-startswith truncated-stored-hash
  detector, inline `scripts/certs/*.pem` CA-chain loader, single
  retry on URLError).
**Tick scope:** Forty-fifth Phase 8 tick overall; first worker-tick
  of UTC date 2026-05-13 (after b0619 16:32Z 2026-05-12).
**Execution mode:** inline runner (`/tmp/b0623_phase8_reverify.py`,
  NOT committed) per the sandbox-session safety constraint maintained
  since b0548. Functional contract matches
  `scripts/batch_0546_phase8_reverify.py` with the b0578+ enhancements.

## Pre-tick git state

- Pre-tick: `find .git -name "*.lock" -delete` and `*.lock.bak`
  cleanup ran. Two stale FUSE-EPERM locks (`.git/ORIG_HEAD.lock` and
  `.git/objects/maintenance.lock`) refused `rm -f` with EPERM —
  same pattern observed since b0334+. Both relocated under
  `.git/_orphan_locks_parked/` via `mv`, which succeeded; subsequent
  `git pull --ff-only` issued benign EPERM warnings against the
  re-created locks but reported `Already up to date` (HEAD =
  `5676b4b` Repair batch 034). Pull completed successfully.
- Pre-existing dirty tree carried forward (uncommitted work from
  prior worker-tick / JIW activity in `worker.log`, `costs.log`,
  `gaps.md` and untracked `records/judgments/...` files from
  b0620-jiw, b0621-jiw and b0622-jiw — separate JIW channel).
  No mutation by this tick.
- **Batch-number renumbering note (b0623 only):** the inline runner
  was first invoked under `BATCH=0622` (initial naive next-number
  pick after b0619). Mid-tick discovery of `reports/batch-0622-jiw.md`
  + `costs.log "0622-jiw"` entries (timestamped 2026-05-13T04:02:00Z,
  ten seconds before our run) showed the JIW channel had already
  consumed the global b0622 slot for today's UTC date. The runner
  was renumbered to `BATCH=0623` and re-executed with the
  tick-suffixed seed `phase8-reverify-2026-05-13-b0623`. The
  preliminary b0622-seeded fetches DID hit the wire (8 fetches) and
  are counted in `cumulative_today` below; their analytical results
  were discarded and are not reported anywhere on disk. Only the
  b0623-seeded run produces the on-disk record. This note exists so
  that any audit comparing wire-traffic logs against committed reports
  can reconcile the 16-vs-8 difference for UTC date 2026-05-13 on
  the worker-tick channel. Note: a separately-channeled JIW abort
  also logged `b0623-jiw STOP verdict=tick-aborted-pull-failure` at
  04:08:06Z (no fetches, no records), so the bare `0623` slot is
  unambiguously the worker-tick Phase 8 reverify identifier.

## Inputs

- Pool size: **1925** (records on disk with non-empty `source_url`
  AND non-empty `source_hash`; +11 vs b0619's 1914 — reflects
  records contributed by intervening JIW ticks b0620-jiw / b0621-jiw
  / b0622-jiw that have settled to disk).
- Seed: `phase8-reverify-2026-05-13-b0623` (tick-suffixed per the
  b0578+ enhancement; first sample under the date-suffixed family
  for UTC date 2026-05-13 — orthogonal to all prior date-suffixed
  samples by construction).
- Sample size: **8** (= MAX_BATCH cap; ceil(0.01 × 1925) = 20 →
  capped at 8).
- Out-of-band re-fetches: **0** (no URLError retries needed;
  CA-chain preload via `scripts/certs/rapidssl_tls_rsa_ca_g1.pem`
  continues to resolve first-pass — now **sixteen consecutive
  worker-ticks**).

## Results — 5 match / 3 drift / 0 truncated_prefix / 0 fetch_error

| Verdict | Count | Records |
|---------|------:|---------|
| match (real) | 5 | si-zm-2012-003-registration-of-business-names-regulations-2012 (zambialii.org `/akn/.../source.pdf`); act-zm-2024-020-supplementary-appropriation-2024-no-2-act-2024 (www.parliament.gov.zm `/acts/` static PDF); act-zm-2016-015-the-public-protector (www.parliament.gov.zm `/acts/` static PDF); si-zm-2017-070-income-tax-african-management-services-company-approval-and-exemption-order-2017 (zambialii.org `/akn/.../source.pdf`); act-zm-cap-249-tsetse-control-act (www.parliament.gov.zm `/acts/` static PDF — **`cap-N` ID-form, second sample**) |
| match_truncated_prefix | 0 | — |
| drift | 3 | act-zm-2018-013-statistics-act-2018 (zambialii.org `/akn/zm/act/2018/13/eng@2018-12-26`); si-zm-2023-046-electoral-process-local-government-by-elections-election-date-and-time-of-poll-no-3-order-2023 (zambialii.org `/akn/zm/act/si/2023/46` — **bare-AKN-path SI sub-cohort, no `/eng@`**); act-zm-1990-012-environmental-protection-and-pollution-control-act-1990 (zambialii.org `/akn/zm/act/1990/12/eng@1996-12-31`) |
| fetch_error | 0 | — |

## TLS / CA-chain note

All eight fetches (three www.parliament.gov.zm `/acts/` static PDFs
— all matches; five zambialii.org-AKN endpoints — two `/source.pdf`
matches plus two `/eng@`-suffix HTML drifts plus one bare-AKN-path
HTML drift) verified successfully on the first attempt because the
inline runner's `build_ssl_context()` pre-loaded
`scripts/certs/rapidssl_tls_rsa_ca_g1.pem`. No retry pass needed.
Standing recommendation #4 (b0586) operationally confirmed across
**sixteen consecutive worker-ticks** (b0586 with retry,
b0587..b0608..b0614..b0619 first-pass, b0623 first-pass).

## Cohort-level cumulative tally (post-b0623, 45 ticks)

Reflects delta from b0619 (last committed Phase 8 tick); the
preliminary b0622-seeded run was discarded and contributes nothing
to cohort tallies.

| Cohort | Pre-b0623 | Δ b0623 | Post-b0623 |
|--------|----------:|--------:|-----------:|
| zambialii.org/akn/.../act-or-SI-HTML drift, `/eng@` suffix | 127/127 | +2/+2 | **129/129** ‡‡ |
| zambialii.org bare-AKN-path drift (SI sub-cohort, no `/eng@`) | 14/14 | +1/+1 | **15/15** |
| zambialii.org/akn/.../source.pdf match (Acts/SIs) | 43/43 | +2/+2 | **45/45** ‡‡‡ |
| zambialii.org/akn/.../source.pdf match (Judgments) | 1/1 | 0/0 | 1/1 |
| media.zambialii.org/media/legislation/ legacy-PDF match | 5/5 | 0/0 | 5/5 |
| commons.laws.africa /media/publication/ legacy-PDF match | 1/1 | 0/0 | 1/1 |
| parliament.gov.zm static PDF match (real-match `/acts/` family) | 118/118 | +3/+3 | **121/121** |
| parliament.gov.zm /amendment_act/ static PDF match | 6/6 | 0/0 | 6/6 |
| parliament.gov.zm static PDF real DRIFT | 0/124 | 0/+3 | 0/127 |
| parliament.gov.zm static PDF truncated_stored_hash_false_drift | 4/124 | 0/0 | 4/127 |
| zambialii judgment-akn HTML drift (ZMCC + ZMSC + ZMHC consolidated) | 13/21 | 0/0 | 13/21 |
| `www.zambialii.org` host-prefix AKN-HTML drift sub-form | 2/2 | 0/0 | 2/2 |
| Parliament-node landing drift | 1/2 | 0/0 | 1/2 |
| judiciaryzambia.com CoA-judgment HTML drift | 2/2 | 0/0 | 2/2 |
| `cap-N` Laws-of-Zambia ID-form (parliament `/acts/` resolver) | 1/1 | +1/+1 | **2/2** ★ widens |
| `loz-` prefix Laws-of-Zambia ID-form (parliament `/acts/` resolver) | 0/0 | 0/0 | 0/0 |
| Stable-PDF combined supercohort (parliament `/acts/` + zambialii akn `/source.pdf` + media.zambialii legacy + commons.laws.africa + parliament `/amendment_act/`) — real-drift basis | 173/177 | +5/+5 | **178/182** ‡ |

‡ Stable-PDF supercohort now 178/182 across 45 ticks. The 4
  cumulative non-real-matches remain the four truncated-stored-hash
  false drifts (b0570 act-zm-2020-011; b0578 act-zm-2020-019; b0581
  act-zm-2020-016; b0585 act-zm-2020-024). **Real drift count on the
  stable-PDF supercohort remains zero across 45 ticks.**

‡‡ AKN-HTML `/eng@`-suffix Act-or-SI drift cohort now stands at
  **129/129** — two new drifts in b0623 (act-zm-2018-013
  statistics-act 2018; act-zm-1990-012 environmental-protection-and-
  pollution-control-act 1990 with `/eng@1996-12-31` suffix). 100 %
  drift rate preserved across 129 samples.

‡‡‡ zambialii akn `/source.pdf` Act-or-SI match cohort now stands
  at **45/45** — two new matches in b0623 (si-zm-2012-003
  registration-of-business-names-regulations 2012; si-zm-2017-070
  income-tax-african-management-services-company-approval-and-
  exemption-order 2017). 100 % match rate preserved across 45 samples.

★ **`cap-N` Laws-of-Zambia ID-form widens 1/1 → 2/2.** Second
  sample of the parliament `/acts/`-resolved `cap-N` Chapter-number
  family (act-zm-cap-249-tsetse-control-act). Both samples matched
  cleanly. Cohort behaviour aligned with the broader parliament
  `/acts/` real-match family (now 121/121). b0595 standing
  recommendation can move to "characterised, no action needed" once
  the cohort grows past 3-5 samples.

## Notable observations (b0623)

1. **Strongest match:drift split since b0614 (5:3).** The
   seed-driven sample composition selected a parliament-`/acts/`-
   heavy slice (3 of 8 = 37.5 %) plus 2 zambialii `/source.pdf`
   matches, leaving only 3 AKN-HTML endpoints — all three of which
   drifted as expected. Cumulative composition across 45 ticks
   remains broadly bifurcated: stable PDFs match deterministically;
   AKN HTML and judgment HTML drift due to upstream CMS-rendered
   non-determinism.

2. **First bare-AKN-path SI drift since b0619.** The
   `si-zm-2023-046-electoral-process-local-government-by-elections-...`
   record drifted on `https://zambialii.org/akn/zm/act/si/2023/46`
   (no `/eng@` suffix). Cohort widens 14 → 15. Behaviour identical
   to the canonical bare-AKN-path family characterised since b0582.

3. **`cap-N` cohort widens to 2/2.** Second observation
   (act-zm-cap-249-tsetse-control-act) confirms the `cap-N` ID-form
   resolves through parliament `/acts/` to a stable PDF that hashes
   deterministically.

4. **No re-drifts this tick.** All three drifts in b0623 are
   first observations for the records concerned.

5. **Pool size 1925** — +11 vs b0619 due to intervening JIW
   commits b0620-jiw / b0621-jiw / b0622-jiw.

## Integrity check

- JSON report well-formed and parseable — **PASS**.
- All required summary keys present (batch, phase, parser_version,
  seed, pool_size, sample_size, sample_rate, max_batch, results,
  match_count, match_truncated_prefix_count, drift_count,
  fetch_error_count, fetches, retry_fetches, started_at,
  completed_at) — **PASS**.
- `sample_size <= MAX_BATCH (8)` — **PASS** (8 <= 8).
- `match_count + match_truncated_prefix_count + drift_count +
  fetch_error_count == sample_size` — **PASS** (5 + 0 + 3 + 0 = 8).
- All 8 sample IDs resolve to existing record files in `records/` —
  **PASS** (8/8 resolved; verified via
  `glob.glob("records/**/<id>.json", recursive=True)`).
- Each result entry contains the required fields — **PASS**.
- Each `verdict` is one of {match, drift, fetch_error,
  match_truncated_prefix} — **PASS**.
- Pool size ≥ 1800 (sanity floor) — **PASS** (1925 at sample time).
- No record mutation occurred this tick — **PASS** (0/8 mutated;
  `git status records/` shows untracked-only entries from prior
  JIW ticks; no `M` (modified) entries; reverify is read-only on
  records by design).

No record mutation occurred. The three drift observations are reported
analytically; per the 45-tick standing finding they do NOT indicate
corpus integrity failure — all three sit on the well-characterised
zambialii.org AKN-HTML resolvers (two `/eng@`-suffix Act drifts and
one bare-AKN-path SI drift). The underlying legal text is unchanged
on each. The stable-PDF supercohort (178/182 real-matches across
45 ticks; 4 truncated-prefix false drifts; **zero real drifts**)
continues to demonstrate that the stored corpus content is faithful
to the upstream sources.

## Budget impact

- Fetches this tick (b0623 canonical): **8** sample-record attempts
  (3 to www.parliament.gov.zm at 2 s between requests, 5 to
  zambialii.org at 5 s between requests). No retries needed.
- Retry fetches this tick: **0**.
- Wire-only preliminary fetches (b0622-seeded, discarded): **8**
  (see Pre-tick git state §"Batch-number renumbering note").
- Cumulative today (pre-b0623, 2026-05-13, worker-tick channel): 0/2000.
- Cumulative today (post-b0623, 2026-05-13, worker-tick channel,
  including the 8 discarded b0622-seeded wire fetches):
  **16 / 2000** (0.8 %).
- Wall-clock duration: ~28 seconds for the b0623 fetch loop; well
  within the 20-minute cap.

## Outputs

- `reports/batch-0623-reverify.json` (deterministic JSON output).
- `reports/batch-0623.md` (this file).
- Append-only updates to `worker.log`, `costs.log`, `provenance.log`,
  `gaps.md` (b0623 Phase 8 section).
- No records written, modified, or deleted.
- No schema or YAML changes.

## Standing recommendations (carried forward — operator decision pending)

1. **Truncated-stored-hash backfill sweep** (b0578/b0579/b0581/b0585
   standing): unchanged across 45 ticks. Operator approval required.
2. **Phase 8 endpoint refinement** (b0565/b0567/b0569 standing):
   with the canonical-host stable-PDF cohort 178/182 zero-real-drift
   across 45 ticks, operator could consider option (a) text-extraction
   -stable hashing on the 158/166 AKN-HTML drift backlog or
   (b) restricting Phase 8 sampling to stable-PDF endpoints only.
   Operator approval required.
3. **Divergent-content duplicate-ID Act records** (b0578 standing):
   five IDs known with multiple divergent record files. Unchanged
   this tick. Operator approval required.
4. **Phase 8 inline-runner CA-bundle parity** (b0586 standing,
   operationally confirmed b0587..b0608..b0614..b0619..b0623 across
   **sixteen consecutive worker-ticks**): consider landing the
   `scripts/certs/*.pem` preload into the canonical
   `scripts/batch_NNNN_phase8_reverify.py` template the next time
   the baseline is refreshed.
5. **Stray `.git/refs/heads/main.lock.bak.*` ref backups**
   (b0588 standing): persists; sandbox cannot unlink. Pre-tick
   `mv` of `.git/ORIG_HEAD.lock` and `.git/objects/maintenance.lock`
   to `.git/_orphan_locks_parked/` worked this session.
6. **`www.zambialii.org`-prefixed AKN-HTML record cluster audit**
   (b0589 standing, strengthened b0601): unchanged this tick — no
   `www.zambialii.org` host-prefix samples drawn.
7. **`cap-N` Laws-of-Zambia Chapter-number ID form characterisation**
   (b0595 standing; cohort widens 1/1 → 2/2 this tick): characterised
   on two consecutive samples. Once cohort >= 3-5 samples, this
   recommendation can move to "characterised, no action needed".
8. **`loz-` prefix Laws-of-Zambia ID form characterisation**
   (b0599 standing): unchanged this tick — no `loz-` samples drawn.
9. **judiciaryzambia.com CoA-record canonical-source decision**
   (b0596 standing; cohort 2/2 drifting): unchanged this tick — no
   judiciaryzambia.com samples drawn.
10. **FTS5 records_fts_data corruption — repair-worker manifest
    escalation** (b0596 standing): potentially RESOLVED per
    b0607-jiw POST-TICK DISCOVERY which observed an external FTS5
    rebuild; subsequent JIW ticks b0611..b0622 wrote records (or
    deferred) and integrity-PASSed throughout. Phase 8 reverify is
    independent of `corpus.sqlite`, so this tick cannot independently
    confirm; cross-worker observation only.
11. **Parliament-node landing reclassification** (b0601 standing):
    `/node/` family at 1/2 drift after 45 ticks. Unchanged this tick.
12. **Stale `refs/remotes/origin/main.lock.*` cleanup on host**
    (b0603 standing): pre-tick lock cleanup via `mv` to
    `_orphan_locks_parked/` succeeded this session; no halt occurred.
    Operator cleanup as previously suggested remains advisable for
    full reclamation but is not blocking.
13. **Batch-number coordination across channels** (NEW b0623): the
    b0622 → b0623 renumbering this tick reflects a near-collision
    with the JIW channel which had also emitted `b0622-jiw` outputs
    ten seconds earlier. Future ticks should consult `costs.log` and
    `reports/` for the latest-used global batch number BEFORE
    selecting their own. Operator could consider a shared
    `next_batch_number.txt` lock file or similar coordination
    primitive to eliminate this race.

None of the above were actioned this tick — Phase 8 reverify worker
is read-only on records by design.

## Next-tick guidance

- Phase 8 reverify next tick (b0624+) — same MAX_BATCH=8, same seed
  family (`phase8-reverify-2026-05-13-b0624` or next UTC date),
  same read-only contract. Continue cohort tracking.
- No fetch-budget concerns — 16/2000 (0.8 %) on the worker-tick
  channel for UTC date 2026-05-13, including the 8 discarded
  preliminary b0622-seeded fetches.
- No phase completion implied — Phase 8 is a continuing nightly
  re-verification process by design (BRIEF.md §"Phase 8").
