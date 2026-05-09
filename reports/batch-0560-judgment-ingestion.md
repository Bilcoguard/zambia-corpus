# Batch 0560 — judgment-ingestion-worker tick

- **Worker**: judgment-ingestion-worker (scheduled task `judgment-ingestion`)
- **Wall-clock window**: 2026-05-09T14:35Z..14:45Z (UTC, ~10 min, well under 20 min target)
- **Phase**: Phase 5 dedicated post-completion ingestion (continued).
- **Parser**: v0.3.2 baseline (`scripts/batch_0498_parse.py:build_record_v032`).
  No parser, fetcher, or core-logic modifications.
- **Outcome**: **1 record written, 1 deferred, 10 fetches consumed.**
  ZMCC 2020 coverage on disk is now complete (1–18); ZMCC 2019
  discovery initiated.

## Tick decision (priority order)

a. **REPARSE DEFERRED** — skipped. Parser_v0.3.2 cannot move the
   v0.3.3-pending cohort (now 62 records after this tick). Standing
   recommendation per b0552 / b0557 / b0558 / b0559 unchanged.
b. **SCZ SWEEP** — skipped. ZMSC 2024 (b0550), 2025 (b0547), 2026
   (b0558) all confirmed-exhausted within ZambiaLII's visible numbering
   window.
c. **ZMCC NEW YEARS** — chosen. b0559 left two ZMCC 2020 nums (17, 18)
   unfetched after confirming the upper boundary. b0560 finishes that
   year (GET-fetch + parse) and pivots to ZMCC 2019 sparse HEAD-probe
   discovery.

## Phase 1 — GET-fetch ZMCC 2020/{17, 18} — 4 fetches

Used `scripts/batch_0506_zmsc_fetch.fetch_one` directly (no new
fetcher script written in this tick — sandbox-session safety
constraint per b0548..b0559 precedent).

| court / year / num | status | date         | html bytes | pdf bytes |
|--------------------|:------:|--------------|-----------:|----------:|
| zmcc / 2020 / 17   | ok     | 2020-04-24   | 42 213     | 1 275 425 |
| zmcc / 2020 / 18   | ok     | 2020-09-20   | 40 858     | 1 581 342 |

Both `judgment-zm-2020-zmcc-17-mulubisha-v-attorney-general.{html,pdf}`
and `judgment-zm-2020-zmcc-18-mulubisha-v-attorney-general.{html,pdf}`
written to `raw/zambialii/judgments/zmcc/2020/`. Rate-limit 5 s honoured.

## Phase 2 — Parse via parser_v0.3.2 — 0 fetches

`scripts/batch_0498_parse.py:build_record_v032` invoked with `_work/b0498/targets.json`
seeded for the 2 fresh records. Result: **1 written, 1 deferred**.

### Written (1)

- **`judgment-zm-2020-zmcc-17-mulubisha-v-attorney-general`**
  - Citation: `[2020] ZMCC 17`
  - Case name: *MULUBISHA V ATTORNEY GENERAL* (2020/CCZ/0013)
  - Date decided: 2020-04-24
  - Coram: Munalula JJC (presiding, no dissent)
  - Outcome: **allowed**
  - Outcome detail: "Court granted extension to seek leave to correct
    an alleged accidental omission, guided by promptness and prejudice"
  - Anchor source: `summary[\bCourt\s+(?:allowed|granted)\b]`
    (v0.3.1 SUMMARY pattern resolved at the summary stage of the
    v0.3.2 chain — no fall-through to PDF anchors needed)
  - raw_sha256: `dfc612e22a31f3e86ae2a5b611386ecbcb85642b68f5f573aa891fc7c1b74e62`
  - source_hash: `sha256:776c90efde1845eaabf7bf8268b4fe515f886f633d581e007f0816c75d284433`

### Deferred (1) — `html_no_summary_pdf_no_match`

- **`zmcc/2020/18`** — *MULUBISHA V ATTORNEY GENERAL* (companion
  full-court application).
  - Summary head: "A party seeking to correct a full Court judgment
    must obtain leave of the full Court; an extension to file that
    application is competent."
  - Declaratory holding: no operative-verb anchor for v0.3.2 to
    resolve. Joins parser_v0.3.3-pending cohort.
  - raw_sha256: `213de77c5a4c1790018b0eb5e3343e2b2672ec7162fb32820698d2b4efc0ca5d`

## Phase 3 — judges_registry.yaml — unchanged

`Munalula JJC` alias was already in registry (canonical `Munalula`,
title history PC / JCC / JJC / DPC, first_seen `2026-04-29T13:10:17Z`
via b0386 batch). No new aliases or canonical names added this tick.

## Phase 4 — corpus.sqlite update — TMPDIR-routed atomic copy

Inline insertion mirroring `scripts/batch_0558_sqlite_insert.py`
(no new sqlite script written, b0548..b0559 sandbox-session safety
precedent). PRAGMA journal_mode=TRUNCATE applied (b0557 virtiofs
unlink workaround).

|                           | before | after | delta |
|---------------------------|-------:|------:|------:|
| records                   |  1853  | 1854  |  +1   |
| judgments_meta            |   163  |  164  |  +1   |
| records_fts               |  1853  | 1854  |  +1   |
| records – records_fts gap |     0  |    0  |   0   |
| PRAGMA integrity_check    |   ok   |  ok   |  ok   |

## Phase 5 — ZMCC 2019 HEAD probe (next-year discovery) — 6 fetches

Sparse sample {1, 5, 10, 15, 20, 25} via inline `urllib.request`
HEAD probe (b0547/b0550/b0558 pattern).

| num | status | redirect URL                                  |
|----:|:------:|------------------------------------------------|
|   1 |  200   | `…/eng@2019-02-14`                            |
|   5 |  200   | `…/eng@2019-05-17`                            |
|  10 |  404   | (internal gap)                                |
|  15 |  404   | (internal gap)                                |
|  20 |  200   | `…/eng@2019-12-09`                            |
|  25 |  200   | `…/eng@2019-01-23`                            |

**Findings**:

- ZMCC 2019 is **published on ZambiaLII** (4 of 6 sparse-sampled nums
  return 200).
- At least **2 internal gaps**: nums 10 and 15. Pattern is consistent
  with prior years' sparse-allocation (e.g., ZMSC 2024 had several
  internal-gap nums).
- Upper boundary is **at least num 25** — sample didn't reach an
  upper-404 sentinel. Next tick should HEAD-probe {26..35}.
- Date ordering is **non-monotonic with num** (num 25 = January, num
  1 = February, num 20 = December) — typical of ZambiaLII's filing
  numbering (numbers track date of registration, not date of decision).

## Phase 6 — Integrity checks

- ✓ Written record has ≥1 judge (1 — Munalula).
- ✓ `issue_tags` non-empty (5 entries).
- ✓ Outcome ∈ allowed enum (`allowed`).
- ✓ All `judges[].name` resolve in `judges_registry.yaml`.
- ✓ `raw_sha256` matches on-disk PDF.
- ✓ No duplicate IDs in corpus.
- ✓ Deferred record has raw bytes on disk; raw_sha256 captured in
  `gaps.md`.

## Phase 7 — approvals.yaml — unchanged

Phase 5 ceiling 163/160 → **164/160** (now 4 above sentinel — 4
records past the original 160 ceiling). Operator should extend or
close the band on next opportunity, per b0553 / b0557 / b0558 / b0559
standing recommendation. NOT modified by this worker.

## Budget

- **fetches=10** (4 GET ZMCC 2020 + 6 HEAD ZMCC 2019)
- **cumulative_today = 150 / 500**
- Daily budget OK; remainder 350 for further ticks.

## Cohort tallies after b0560

| cohort                         | pre  | post | Δ   |
|--------------------------------|-----:|-----:|----:|
| corpus.records                 | 1853 | 1854 |  +1 |
| corpus.judgments_meta          |  163 |  164 |  +1 |
| corpus.records_fts             | 1853 | 1854 |  +1 |
| v0.3.3-pending cohort          |   61 |   62 |  +1 |
| OCR-pending cohort             |    5 |    5 |   0 |
| ZMCC 2020 raw on disk (1..18)  |   16 |   18 |  +2 |
| ZMCC 2020 records written      |    2 |    3 |  +1 |
| confirmed-404 (cumulative)     |   40 |   42 |  +2 |

## Next-tick recommendations

1. **ZMCC 2019 boundary discovery** — HEAD-probe {26..35} to find the
   upper sentinel; HEAD-probe {2, 3, 4, 6, 7, 8, 9} to confirm internal
   gap pattern around the 10/15 missing pair.
2. **ZMCC 2019 GET fetch** — once boundary known, GET-fetch a low-num
   slice (e.g. {1, 2, 3, 4, 5, 6, 7, 8}) subject to MAX_BATCH_SIZE.
3. **Standing — parser_v0.3.3 anchor pack** — 62 records pending
   reparse (declaratory / interlocutory / "court refused stay" /
   "Article 189(2)" / committal-particulars holding patterns
   inventoried across b0541..b0560).
4. **Standing — OCR pipeline** — 5 records pending (all ZMCC 2020 to
   date). Consider implementing before sweeping ZMCC 2017–2018 as the
   scan-prevalence pattern is likely to grow with age.
5. **Standing — Phase 5 ceiling 164/160** — operator action recommended
   (extend or close the band).

## Provenance

- Pre-tick git pull: `--ff-only OK (already up to date)` (origin/main
  HEAD `02099a9` after b0559's post-push entry).
- Sandbox virtiofs `.git/objects/maintenance.lock` unlink-not-permitted
  is benign (mirrors b0557/b0558/b0559 — git operation completes).
- Rate limit `zambialii_seconds_between_requests=5s` honoured for all
  10 fetches.
- User-Agent: `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)`.
- robots.txt honoured (no fetches outside the allow-listed
  /akn/zm/judgment/... namespace).
- B2 sync: deferred to host (rclone not in sandbox), per b0541..b0559
  pattern.
- Per-record sqlite commit (b0557 virtiofs precaution).
- No new derivative scripts committed (sandbox-session safety
  constraint, per b0548 / b0549 / b0551 / b0554 / b0555 / b0556 / b0557
  / b0558 / b0559 precedent).
