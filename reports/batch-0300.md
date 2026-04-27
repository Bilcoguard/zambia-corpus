# Batch 0300 Report

**Phase:** 4 — bulk (minimal upstream-refresh tick)
**Tick:** 2026-04-27 (UTC) — scheduled tick, 30-min cadence
**Yield:** 0 records committed
**Wall-clock:** ~5 min
**Parser version:** 0.5.0 (probe-only — same as b0290..b0299)

## Summary

This tick is a minimal upstream-refresh probe of the two chronological
Act feeds:

- `zambialii.org/legislation/recent`
- `parliament.gov.zm/acts-of-parliament` (page 0)

All 22 active alphabet letters on zambialii were exhaustively swept
across b0291..b0293 (A,B,C,I,M,P,S,T,V in b0291; E,F,J,L,N,W in b0292;
D,G,H,K,O,R,U in b0293), so no alphabet sweep is performed this tick.

**Result:** 0 in-priority candidates; 0 off-priority candidates. All
upstream entries already in corpus. Steady state preserved across
b0290..b0300 (eleven consecutive ticks).

## Tick context

Pre-tick lock cleanup ran cleanly (no leftover `.lock` or `.lock.bak`
files removable). `git pull --ff-only` returned "Already up to date" on
first attempt (benign `unable to unlink ...maintenance.lock` warning
emitted by git but pull succeeded — sandbox cannot delete files in
`.git/objects/`, this is not a recovery condition).

## Refresh probe — zambialii /legislation/recent

13 act links enumerated:

- 2025/5  National Road Fund (Amendment) Act
- 2025/6  Building Societies (Amendment) Act
- 2025/7  Animal Health (Amendment) Act
- 2025/8  Border Management and Trade Facilitation Act
- 2025/9  Supplementary Appropriation (2025) Act
- 2025/22 Mobile Money Transaction Levy (Amendment) Act
- 2025/23 Companies (Amendment) Act
- 2025/24 Registration of Business Names (Amendment) Act
- 2025/25 Independent Broadcasting Authority Act
- 2025/26 Zambia National Broadcasting Corporation Act
- 2025/27 Betting Levy Act
- 2025/28 Appropriation Act
- 2025/29 Zambia Institute of Procurement and Supply Act

Cross-check vs `records/acts/`: **all 13 already in corpus** (verified
by direct year/num filename match: `act-zm-YYYY-NNN-*.json`).

## Refresh probe — parliament /acts-of-parliament page 0

20 acts enumerated (matched via `Act No. N of YYYY` text pattern):

- 2025/21..29 (nine acts)
- 2026/1..11  (eleven acts)

Cross-check vs `records/acts/`: **all 20 already in corpus**.

## In-priority candidates (priority_order matches): 0

| Sub-phase                     | Modern (>=2017) novel | Notes |
|-------------------------------|-----------------------|-------|
| acts_in_force                 | 0                     | all 33 chronological-feed entries already on disk |
| sis_corporate                 | 0                     | alphabet exhaust complete (b0291..b0293) |
| sis_tax                       | 0                     | alphabet exhaust complete |
| sis_employment                | 0                     | alphabet exhaust complete |
| case_law_scz                  | n/a                   | judiciary scope (not in this probe) |
| sis_data_protection           | 0                     | upstream steady state |
| sis_mining                    | 0                     | alphabet exhaust complete |
| sis_family                    | 0                     | alphabet exhaust complete |

## robots.txt re-verification

| Source     | sha256 | Match |
|------------|--------|-------|
| zambialii  | `fce67b697ee4ef44e0694134e23108c2701b5e7661eed885013efb9b75dcd8f0` | yes (unchanged from b0193..b0299) |
| parliament | `278e83bcf567badfebcdea4d5d20ca9898e4449fe4eb2e3b5a08227b4ca9b762` | yes (unchanged from b0290..b0299) |

Crawl-delays observed: zambialii 6s (robots: 5s); parliament 11s
(robots: 10s) — both still satisfy `approvals.yaml` minimums of 5s.

## Cumulative state

| Surface       | Count | Δ vs b0299 |
|---------------|-------|-----------:|
| acts          | 1169  | 0          |
| SIs           |  539  | 0          |
| judgments     |   25  | 0          |
| OCR backlog   |   21  | 0          |

## Integrity check

CHECK1..CHECK6 are **N/A** for this tick (zero record writes; no
duplicate-ID, amended_by, repealed_by, cited_authorities, source_hash,
or schema check has anything to operate on). robots.txt SHAs verified
match expected. records/ tree git-clean. corpus.sqlite untouched
(established disposition — FTS5 vtable broken, journal held open;
deferred to host).

## Fetches

4 fetches this tick (2 robots + 2 listings). Today's running total:
**92/2000** (~4.6%). Token usage: minimal probe — no record-text
ingestion this tick.

## Disposition

- Phase 4 remains **incomplete** per `approvals.yaml` (worker does not
  flip this flag).
- Phase 4 **appears to be at upstream steady state** for the eleventh
  consecutive tick (b0290..b0300), awaiting human confirmation.
- B2 sync deferred to host (rclone not available in sandbox).
- corpus.sqlite update deferred (established disposition).

## Recovery / sandbox notes

- The TLS chain workaround for parliament.gov.zm (server omits the
  RapidSSL intermediate) is documented in `scripts/batch_0300.py`. It
  uses the published intermediate at `scripts/certs/rapidssl_tls_rsa_ca_g1.pem`
  appended to certifi's bundle — no insecure fallback (verify=False)
  was used. Suggest the host operator confirm whether previous ticks
  relied on a system-trust path that included RapidSSL or also used
  this bundle approach; either way it has no functional impact.
- `git pull` warning `unable to unlink .git/objects/maintenance.lock` is
  the same benign sandbox-permissions issue noted in b0299. Pull still
  succeeded (Already up to date).
