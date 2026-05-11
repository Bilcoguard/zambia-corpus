# Batch 0584 — judgment-ingestion-worker (2026-05-11)

**UTC:** 2026-05-11T11:30Z
**Worker:** judgment-ingestion-worker (scheduled tick)
**Parser:** parser_v0.3.3 (inline) + parser_v0.3.4 reparse (inline) — applied this tick, not yet packaged
**Tick scope:** Priority (b) Court of Appeal sweep — `judiciaryzambia.com` page 2 (continuation of b0583 first-ever CoA ingestion)
**User-Agent:** `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)`

## Tick scope decisions

- **Priority (a) reparse**: skipped — standing per b0571 redeferral evidence. v0.3.4 inline date regex *was* used to rescue 4 b0584-tick records that v0.3.3 had date-deferred (in-tick reparse, not standing-pool reparse).
- **Priority (b) judiciary-coa-sweep**: chosen — page 2 continuation per b0583 gaps.md sweep position. Page 1 was fully processed in b0583 (10 posts → 7 written + 3 v0.3.3-pending). Page 2 yielded 8 posts; this tick processed all 8 within MAX_BATCH_SIZE budget.
- **Priority (c)**: not exercised this tick — page-2 sweep consumed batch-size budget.

## Source listing — judiciaryzambia.com page 2

| # | post slug                                                                | size | status     | record id (if written)                                                                              |
|---|--------------------------------------------------------------------------|-----:|------------|-----------------------------------------------------------------------------------------------------|
| 1 | `app-79-2024-zebron-makanda-vs-the-people/`                              | ~40k | **written**| `judgment-zm-2025-coa-079-zebron-makanda-v-the-people`                                              |
| 2 | `app-330-2024-giford-kabunda-vs-enala-mulambo/`                          | ~40k | **written**| `judgment-zm-2025-coa-330-giford-kabunda-v-enala-mulambo`                                           |
| 3 | `app-182-2025-eleana-stella-koukoudis-vs-image-civil-and-electrical-eng…`| ~40k | **written**| `judgment-zm-2025-coa-182-eleana-stella-koukoudis-1-other-v-image-civil-and-electrical-engineering-ltd` |
| 4 | `app-16-2025-nampak-zambia-ltd-vs-nice-products-ltd/`                    | ~40k | **written**| `judgment-zm-2026-coa-016-nampak-zambia-ltd-v-nice-products-ltd`                                    |
| 5 | `app-82-2025-kenneth-kaira-vs-mulenga-mwiche/`                           | ~40k | **written**| `judgment-zm-2026-coa-082-kenneth-kaira-v-mulenga-mwiche-1-other`                                   |
| 6 | `app-75-2025-chris-hamuwele-vs-mulungushi-university/`                   | ~40k | **written**| `judgment-zm-2026-coa-075-chris-hamuwele-v-mulungushi-university-respondent`                        |
| 7 | `22607-2/` (slug override — Levi Chimfwembe v Sampa Leonard Musonda)     | ~40k | **written**| `judgment-zm-2026-coa-226-levi-chimfwembe-v-sampa-leonard-musonda`                                  |
| 8 | `app-203-2023-deton-engineering-…/`                                      | ~40k | deferred   | (v0.3.3-pending — outcome anchor not matched)                                                       |

**8 of 8 fetched, 7 written, 1 deferred.**

## Records written this tick (7)

### coa/2025/079 — *Zebron Makanda v The People*

- **citation**: `[2025] ZMCA 79`
- **court**: Court of Appeal
- **date_decided**: 2025-… (rescued via v0.3.4 `ORD_TOL` — original PDF ordinal corrupted)
- **outcome**: dismissed
- **judges**: Mchenga DJP (DIP→DJP OCR alias applied), Majula JJA, Muzenga JJA
- **raw_path**: `raw/judiciary-zm/coa/App-79-2024-Zebron-Makanda-vs-The-People-Coram-Justice-Mchenga-DJP-Majula-Muzenga-JJA.pdf`

### coa/2025/330 — *Giford Kabunda v Enala Mulambo*

- **citation**: `[2025] ZMCA 330`
- **judges**: Chashi JJA, Ngulube JJA, Banda-Bobo JJA
- **date rescued via v0.3.4** (`ORD_TOL`)

### coa/2025/182 — *Eleana Stella Koukoudis & 1 Other v Image Civil and Electrical Engineering Ltd*

- **judges**: Chashi JJA, Ngulube JJA, Banda-Bobo JJA
- **parsed by v0.3.3 inline** (date in canonical form)

### coa/2026/016 — *Nampak Zambia Ltd v Nice Products Ltd*

- **judges**: Siavwapa JJA, Chishimba JJA, Patel JJA
- **date rescued via v0.3.4**

### coa/2026/082 — *Kenneth Kaira v Mulenga Mwiche & 1 Other*

- **judges**: Makungu JJA, Ngulube JJA, Chembe JJA (Chembe added to judges_registry.yaml this tick)

### coa/2026/075 — *Chris Hamuwele v Mulungushi University*

- **judges**: Chashi JJA, Ngulube JJA, Banda-Bobo JJA

### coa/2026/226 — *Levi Chimfwembe v Sampa Leonard Musonda*

- **citation**: `[2026] ZMCA 226`
- **judges**: Chashi JJA, Ngulube JJA, Banda-Bobo JJA
- **outcome**: `dismissed` (patched from initial `withdrawn` — see parser-quality notes below)
- **raw_path**: `raw/judiciary-zm/coa/App-226-2023-Levi-Chimfwembe-vs-Sampa-Leonard-Musonda-Coram-Chashi-Ngulube-Banda-Bobo-JJA.pdf` (slug override `22607-2` → `app-226-2023-...`)
- **date rescued via v0.3.4**

## Records deferred this tick (1)

### v0.3.3-pending — `html_no_summary_pdf_no_match`

- **app-203-2023 — Deton Engineering Ltd v …** — text-extracted native PDF, no v0.3.3 outcome anchor match. Joins the b0583 v0.3.3-pending cohort (3 entries). Standing parser_v0.3.4 anchor-pack candidate.

## Parser v0.3.4 inline improvements (this tick)

Four parser-quality issues from b0583's gaps.md were materially addressed this tick by inline parser changes. None of these have been promoted to the packaged parser; they are documented here and in gaps.md for v0.3.4 packaging in a subsequent tick.

1. **ORD_TOL — date regex ordinal-suffix tolerance**: extended b0583's lone-`t` allowance to a broader permissive pattern `(?:[\s\dtshrdnh]{0,4})` that absorbs OCR junk like `"17 1 h"`, `"25t"`, `"251"` (missing-space artefact). Rescued: `coa-079`, `coa-330`, `coa-016`, `coa-226` (4 of 4 v0.3.3 date-deferred records). Composite patterns `COMPOSITE_RE` and `COMPOSITE2_RE` added for two-date "DAY ord and DAY ord MONTH YEAR" headers.

2. **PANEL_END_RE — Coram first-role-wins truncation**: replaced b0583's last-role-wins regex with first-role-wins. Pattern: `\b(JJA|JJ|JCC|JJC|JJS|DCJ|DJP|PCA)\b` — truncates the Coram region at the FIRST panel-completing role token (the suffix appears once at the end of the judge list). The b0583 greedy version was gobbling lawyer details (e.g. `JS` matching inside `JUDGMENT`). All 7 records re-parsed cleanly. Three iterations of the fix script (v1 greedy → v2 last-role-wins → v3 first-role-wins) before settling on v3.

3. **DIP→DJP OCR alias**: `ROLE_OCR_ALIASES = {"DIP": "DJP"}` — Mchenga's `DJP` was being mis-OCR'd as `DIP` in `coa-079`. Treat alias as the canonical role at parse time.

4. **`\bwithdrawn\b` false-positive in OUTCOME_PATTERNS**: bare-anchor `\bwithdrawn\b` matched body text discussing a withdrawn contract in `coa-226` (actual disposition: `dismissed`). Patched in-place via direct DB+JSON update; the package fix should require `withdrawn` to be co-located with disposition anchors (`appeal is/was withdrawn`, `accordingly withdrawn`).

## CHECK6 raw_path field added

A `raw_path` field was added to all 7 b0584 records during the integrity-check phase, after initial CHECK6 caught that the Levi Chimfwembe record's PDF could not be located by deriving from `source_url` slug (`22607-2`) because of the slug override. The new field stores the relative on-disk path (`raw/judiciary-zm/coa/…`) and is verified to match `raw_sha256` for all 7. Pattern recommended for all JIW ticks going forward where post-slug differs from filename.

## Integrity checks (8/8 PASS)

```
CHECK0_pragma_integrity:        PASS
CHECK1_no_duplicate_ids:        PASS
CHECK2_judges_present:          PASS  (all 7 records have ≥1 judge)
CHECK3_issue_tags_nonempty:     PASS  (all 7 records have ≥1 issue_tag)
CHECK4_outcome_in_enum:         PASS  (all 7 outcomes in allowed set)
CHECK5_judges_registry_resolve: PASS  (all 21 judge entries resolve to canonical_name)
CHECK6_raw_sha256_matches:      PASS  (all 7 raw PDF sha256 verified via raw_path)
CHECK7_sqlite_counts:           records=1881 fts=1881 fts_gap=0 meta=191
CHECK8_json_count_eq_meta:      on_disk_jsons=191  sqlite_meta=191
```

## Cohort tallies after b0584

| Cohort                     | Pre-b0584 | Δ   | Post-b0584 |
|----------------------------|----------:|----:|-----------:|
| Records (total)            |     1874  | +7  | **1881**   |
| records_fts                |     1874  | +7  | **1881**   |
| judgments_meta             |      184  | +7  | **191**    |
| On-disk judgment JSONs     |      184  | +7  | **191**    |
| Court of Appeal coverage   |        7  | +7  | **14**     |
| v0.3.3-pending             |       86  | +1  | **87**     |
| OCR-pending                |       27  |  0  | 27         |

## judges_registry.yaml diff

- **+1 new canonical_name**: `Chembe` (title `JJA`, court Court of Appeal, first_seen_in `judgment-zm-2026-coa-082-kenneth-kaira-v-mulenga-mwiche-1-other`)
- No alias additions; all other judges (Mchenga, Majula, Muzenga, Chashi, Ngulube, Banda-Bobo, Siavwapa, Chishimba, Patel, Makungu) already present from b0583.

## Sandbox notes

- **virtiofs `corpus.sqlite` malformed-image** mid-tick: `sqlite3` on the workspace-mounted DB hit "database disk image is malformed" after the v3 judges-fix run. Diagnosed as a virtiofs caching artefact — the `/tmp` working copy was healthy. Recovered via `cp /tmp/jiw_b0584/corpus.sqlite corpus.sqlite.new && mv corpus.sqlite.new corpus.sqlite`. Recommended that future JIW ticks add a workspace-level `PRAGMA integrity_check` after the /tmp copy-out to detect this earlier.
- **/tmp disk exhaustion**: 7 redundant 111 MB sqlite copies accumulated across v1/v2/v3 judges-fix iterations and the v0.3.4 date reparse. Cleaned up mid-tick to free ~522 MB.
- **Pre-tick backup**: `corpus.sqlite.bak.b0584-pre-20260511T101000Z` written before any DB mutation.
- **Execution mode**: inline runner; no scripts/batch_0584_*.py derivative committed (sandbox-session safety constraint, per b0548..b0583 precedent). v0.3.4 inline changes documented in gaps.md for next-tick packaging.
- **B2 sync** deferred to host (rclone not available in sandbox).

## Cumulative budget

- Today (2026-05-11) JIW fetches consumed pre-tick: **16/500** (per b0583 — 16 fetches: 8 HTML + 8 PDF)
- This tick: 16 fetches (8 HTML + 8 PDF)
- Today (2026-05-11) JIW fetches consumed post-tick: **32/500** (within budget; 468 remaining)

## Next-tick recommendation

1. **Continue page 3** of `judiciaryzambia.com/category/resources/decisions/court-of-appeal-decisions/` — sweep position now at page 3.
2. **Package v0.3.4 parser**: codify the four inline fixes applied this tick (`ORD_TOL`, `PANEL_END_RE`, `ROLE_OCR_ALIASES`, `withdrawn` anchor co-location) into the packaged parser so subsequent ticks do not have to re-implement them inline. Estimated effort: small (~50 LOC) but should be a dedicated tick to allow clean before/after delta on the existing v0.3.3-pending cohort (87 records).
3. **v0.3.3-pending cohort reparse trial**: once v0.3.4 is packaged, run a single-tick reparse trial over the 87-record v0.3.3-pending cohort to see how many unblock. The b0584 inline `ORD_TOL` fix unblocked 4/4 date-deferred records this tick — extrapolating to the broader cohort is unwarranted but the trial is cheap (0 fetches).
4. **Standing**: parser_v0.3.4 anchor pack authoring (87 records pending — 1 added this tick, `coa-203 deton-engineering`).
5. **Standing**: OCR pipeline implementation (27 records pending — unchanged this tick).
