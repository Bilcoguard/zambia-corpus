# Batch 0561 — judgment-ingestion-worker tick

- **Worker**: judgment-ingestion-worker (scheduled task `judgment-ingestion`)
- **Wall-clock window**: 2026-05-09T15:00Z..15:17Z (UTC, ~17 min, well under 20 min target)
- **Phase**: Phase 5 dedicated post-completion ingestion (continued).
- **Parser**: v0.3.2 baseline (`scripts/batch_0498_parse.py:build_record_v032`).
  No parser, fetcher, or core-logic modifications.
- **Outcome**: **2 records written, 6 deferred, 33 fetches consumed.**
  ZMCC 2019 upper boundary confirmed at num 28; first ever ZMCC 2019
  records ingested (Sean E. Tembo 2019/1 and Chama Mutambalilo
  2019/20).
- **Collision-coexistent** with worker-tick Phase 8 batch-0561 (commit
  `5269077`); mirrors the b0560 collision-coexistent pattern.

## Tick decision (priority order)

a. **REPARSE DEFERRED** — skipped. Parser_v0.3.2 cannot move the
   v0.3.3-pending cohort (now **68 records** after this tick).
   Standing recommendation per b0552 / b0557 / b0558 / b0559 / b0560
   unchanged.
b. **SCZ SWEEP** — skipped. ZMSC 2024 (b0550), 2025 (b0547), 2026
   (b0558) all confirmed-exhausted within ZambiaLII's visible numbering
   window.
c. **ZMCC NEW YEARS** — chosen. b0560 sparse-sampled ZMCC 2019 at
   {1, 5, 10, 15, 20, 25} (4 OK / 2 404). This tick performs (i) upper-
   sentinel HEAD-probe {26..35}, (ii) low-slice gap HEAD-probe
   {2,3,4,6,7,8,9}, then (iii) GET-fetch 8 known-OK nums (MAX_BATCH_SIZE).

## Phase 1a — HEAD probe ZMCC 2019/{26..35} — 10 fetches

Inline runner `_work/b0561/head_probe_zmcc_2019.py` (no committed
derivative script — sandbox-session safety constraint per b0548..b0560).

| num | status | redirect date       |
|----:|:------:|---------------------|
|  26 |  200   | 2019-10-22          |
|  27 |  200   | 2019-11-25          |
|  28 |  200   | 2019-09-12          |
|  29 |  404   | (sentinel)          |
|  30 |  404   | (sentinel)          |
|  31 |  404   | (sentinel)          |
|  32 |  404   | (sentinel)          |
|  33 |  404   | (sentinel)          |
|  34 |  404   | (sentinel)          |
|  35 |  404   | (sentinel)          |

**ZMCC 2019 upper boundary CONFIRMED at num 28** (7 consecutive 404s
{29..35} = strong sentinel). Rate-limit 5 s honoured.

## Phase 1b — HEAD probe ZMCC 2019/{2,3,4,6,7,8,9} — 7 fetches

| num | status | redirect date       |
|----:|:------:|---------------------|
|   2 |  404   | (internal gap)      |
|   3 |  200   | 2019-03-14          |
|   4 |  200   | 2019-05-21          |
|   6 |  200   | 2019-05-28          |
|   7 |  404   | (internal gap)      |
|   8 |  404   | (internal gap)      |
|   9 |  404   | (internal gap)      |

ZMCC 2019 internal-gap pattern in low slice {1..15}: nums {2, 7, 8, 9, 10, 15}
all confirmed 404 (six internal gaps), nums {1, 3, 4, 5, 6} confirmed
200 (five published).

## Phase 2 — GET-fetch ZMCC 2019 8 known-OK nums — 16 fetches

Targets: {1, 3, 4, 5, 6, 20, 25, 26}. Used
`scripts/batch_0506_zmsc_fetch.fetch_one` directly via thin wrapper
`scripts/batch_0561_fetch.py`.

| court / year / num | status | date       | html bytes | pdf bytes  |
|--------------------|:------:|------------|-----------:|-----------:|
| zmcc / 2019 / 1    |  ok    | 2019-02-14 | 40 512     | 125 612    |
| zmcc / 2019 / 3    |  ok    | 2019-03-14 | 45 115     | 5 048 872  |
| zmcc / 2019 / 4    |  ok    | 2019-05-21 | 46 272     | 6 429 300  |
| zmcc / 2019 / 5    |  ok    | 2019-05-17 | 61 845     | 2 880 214  |
| zmcc / 2019 / 6    |  ok    | 2019-05-28 | 48 370     | 4 074 462  |
| zmcc / 2019 / 20   |  ok    | 2019-12-09 | 93 363     | 9 920 236  |
| zmcc / 2019 / 25   |  ok    | 2019-01-23 | 45 176     | 4 100 419  |
| zmcc / 2019 / 26   |  ok    | 2019-10-22 | 44 028     | 3 346 764  |

8/8 OK. All 16 raw files (8 HTML + 8 PDF) saved to
`raw/zambialii/judgments/zmcc/2019/`. Rate-limit 5 s honoured.

## Phase 3 — Parse via parser_v0.3.2 — 0 fetches

`scripts/batch_0498_parse.py:build_record_v032` invoked via
`scripts/batch_0561_parse.py`. Result: **2 written, 6 deferred**.

### Written (2)

- **`judgment-zm-2019-zmcc-01-sean-e-tembo-v-attorney-general`**
  - Citation: `[2019] ZMCC 1`
  - Case name: *Sean E. Tembo v Attorney-General* (7 of 2018)
  - Date decided: 2019-02-14
  - Coram: Sitali JCC (presiding), Munalula JCC, Musaluke JCC
  - Outcome: **allowed**
  - Outcome detail: "A petitioner may discontinue a constitutional
    petition before judgment; court granted discontinuance and
    ordered each party to bear own costs"
  - Anchor source: `summary[\bCourt\s+(?:allowed|granted)\b]`
    (v0.3.1 SUMMARY pattern; resolved at the summary stage)
  - raw_sha256: `d92897dd2bc70d41f7d3f2152bc2ff0d907449a37e598b654a3768d23673f525`
  - source_hash: `sha256:a1c7d7bdbbb066b306c51147ebc6dcef1eb662936f1c1e46df2a330fd5d6301e`
  - source_url: https://zambialii.org/akn/zm/judgment/zmcc/2019/1/eng@2019-02-14

- **`judgment-zm-2019-zmcc-20-chama-mutambalilo-v-attorney-general`**
  - Citation: `[2019] ZMCC 20`
  - Case name: *Chama Mutambalilo v Attorney-General*
  - Date decided: 2019-12-09
  - Coram: Chibomba PC (presiding), Sitali JCC, Mulenga JCC,
    Mulonda JCC, Musaluke JCC
  - Outcome: **dismissed**
  - Outcome detail: "The JSC may discipline judicial officers either
    on JCC recommendation or on its own initiation under
    Article 241(c); petition dismissed"
  - Anchor source: `summary[\b(?:appeal|petition|application|action|matter)\s+(?:is\s+)?(?:hereby\s+)?dismissed\b]`
    (v0.3.1 SUMMARY pattern)
  - raw_sha256: `ce98da133fc241fb7824e27a6d354dcf6ad902e57018d2b7c43ecd532f75edd9`
  - source_hash: `sha256:27fd96e03187d49aa7853f17f654b36a2c7f6d795b8224f3afc7089a4bfe3d1e`
  - source_url: https://zambialii.org/akn/zm/judgment/zmcc/2019/20/eng@2019-12-09

### Deferred (6) — all `html_no_summary_pdf_no_match`, joining v0.3.3-pending cohort

| ID                                                                       | Reason                                                           |
|--------------------------------------------------------------------------|------------------------------------------------------------------|
| `zmcc/2019/3` Benjamin Mwelwa v AG                                        | Declaratory: judicial independence violated; damages awarded.    |
| `zmcc/2019/4` Bernard Shajilwa & Ors v AG & Ors                          | Declaratory + jurisdictional: customary chief disputes non-constitutional. |
| `zmcc/2019/5` Martin Chitondo & Ors v AG                                 | Declaratory statutory interpretation: deputy mayor terms.        |
| `zmcc/2019/6` Public Protector v INDE                                    | Declaratory jurisdictional: Public Protector subject to JR.      |
| `zmcc/2019/25` Likukela v AG & Ors                                       | "abuse of process" qualifier breaks v0.3.2 dismissed-anchor regex. |
| `zmcc/2019/26` Chansa v AG                                                | "Summons … dismissed" — token outside v0.3.2 dismissed vocabulary. |

All six raw files on disk; raw_sha256 captured in gaps.md. v0.3.3-pending
cohort: 62 → **68**.

## Phase 4 — judges_registry.yaml — UNCHANGED

All six coram judges already present:

- Sitali (canonical), Munalula (canonical), Musaluke (canonical) —
  added in earlier ZMCC ticks.
- Chibomba (canonical, PC), Mulenga (canonical), Mulonda (canonical) —
  long-standing entries from ZMSC ticks.

No new judge canonicals or aliases required.

## Phase 5 — corpus.sqlite update

TMPDIR-routed atomic copy (b0531 pattern) + PRAGMA journal_mode=TRUNCATE
(b0557 workaround for virtiofs unlink restriction). Per-record commits.

| Table         | Before | After  | Δ   |
|---------------|-------:|-------:|----:|
| records       | 1854   | 1856   | +2  |
| records_fts   | 1854   | 1856   | +2  |
| judgments_meta| 164    | 166    | +2  |

- `records ∖ records_fts` gap = 0 (maintained).
- PRAGMA integrity_check = `ok`.

## Phase 6 — Integrity checks (PASS)

- ✓ Every written judgment has ≥ 1 judge (zmcc/2019/1 has 3 judges;
  zmcc/2019/20 has 5 judges).
- ✓ `issue_tags` non-empty for both records (7 tags and 5 tags
  respectively).
- ✓ `outcome` from allowed enum (`allowed`, `dismissed`).
- ✓ All `judges[].name` resolve in `judges_registry.yaml` (Sitali,
  Munalula, Musaluke, Chibomba, Mulenga, Mulonda all canonical).
- ✓ No duplicate IDs in corpus (records IDs unique, FTS IDs unique).
- ✓ raw_sha256 for both written records matches on-disk PDF bytes
  (re-hash check passed).
- ✓ All six deferred records have raw bytes on disk with raw_sha256
  captured in gaps.md (re-hash matches the recorded value).

## Phase 7 — approvals.yaml — UNCHANGED

Phase 5 ceiling: 164/160 → **166/160** (now 6 above sentinel).
Recommend operator extend the band or close Phase 5 per b0553 /
b0557 / b0558 / b0560 standing.

## Budget accounting

- Today's fetches: 150 → **183 / 500** (33 added).
- Breakdown:
  - 10 HEAD probes (ZMCC 2019/{26..35} upper sentinel)
  - 7 HEAD probes (ZMCC 2019/{2,3,4,6,7,8,9} low-slice gap close)
  - 16 GET fetches (8 nums × HTML + PDF)
- Wall-clock: ~17 min (well under 20 min ceiling).

## Cohort tallies post-tick

- v0.3.3-pending: 62 → **68** (b0561 +6).
- OCR-pending: **5 unchanged** (no scanned-PDF deferrals this tick).

## ZMCC 2019 — coverage map after b0561

- Confirmed-200: {1, 3, 4, 5, 6, 20, 25, 26, 27, 28} (10 nums).
- Confirmed-404: {2, 7, 8, 9, 10, 15, 29..35} (12 nums).
- Un-probed: {11, 12, 13, 14, 16, 17, 18, 19, 21, 22, 23, 24} (12 nums).
- Upper boundary: **num 28** (HEAD-confirmed by 7 consecutive 404s).
- Records on disk: 8 (raw HTML+PDF for nums 1, 3, 4, 5, 6, 20, 25, 26).
- Records written to corpus.sqlite: 2 (nums 1 and 20).

## Next-tick recommendations

1. **ZMCC 2019 finish** — HEAD-probe un-probed {11..14, 16..19, 21..24}
   to fully resolve internal-gap pattern; GET-fetch remaining
   known-OK {27, 28} plus any new 200s found.
2. **ZMCC 2018 HEAD probe** — start next-year discovery.
3. **Standing**: parser_v0.3.3 anchor pack authoring (68 records
   pending — declaratory-holding patterns now well-sampled).
4. **Standing**: OCR pipeline (5 records pending).
5. **Standing**: operator action on Phase 5 ceiling 166/160 (6 above
   sentinel).

## Sandbox / safety constraints honoured

- robots.txt and ZambiaLII rate-limit (5 s) honoured throughout.
- User-Agent: `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)`.
- No fabricated citations or judges.
- `approvals.yaml` not modified.
- Per-record commits (b0557 belt-and-braces pattern for virtiofs).
- Inline HEAD-probe runner; no derivative committed for HEAD-probe
  driver (sandbox-session safety constraint per b0548..b0560
  precedent). Only the GET fetch + parse + sqlite-insert wrappers
  (`batch_0561_fetch.py`, `batch_0561_parse.py`,
  `batch_0561_sqlite_insert.py`) are committed; they are thin wrappers
  over the long-standing `batch_0506_zmsc_fetch.fetch_one`,
  `batch_0498_parse.build_record_v032`, and the b0558 sqlite-insert
  pattern.
- B2 sync deferred to host (rclone not in sandbox).
