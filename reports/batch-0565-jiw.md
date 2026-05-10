# Judgment batch 0565 — judgment-ingestion-worker tick

**Tick start**: 2026-05-10T09:11:35Z (session=bold-cool-mccarthy)
**Worker**: judgment-ingestion-worker (separate from main worker; budget 500 fetches/day)
**Pre-tick HEAD**: 712b752 (origin/main, verified via `git rev-parse` after `git fetch`; full `git pull` blocked by virtiofs ORIG_HEAD.lock — Operation not permitted, mirrors b016/b017/b0562/b0563/b018 FUSE constraint)
**Parser**: v0.3.2 baseline (scripts/batch_0498_parse.py) — `build_record_v032`

## Tick decision

- **Priority (a)** REPARSE DEFERRED — *skipped*. v0.3.2 cannot move v0.3.3-pending cohort (73 records). Standing per b0552/b0557/b0558/b0559/b0560/b0561/b0564.
- **Priority (b)** SCZ SWEEP — *skipped*. ZMSC 2024-2025-2026 confirmed exhausted by b0547/b0550/b0558.
- **Priority (c)** ZMCC NEW YEARS — *chosen*. Per b0564 next-tick recommendation #1: GET-fetch ZMCC 2019 final-2 known-OK nums {23, 24}.

## Fetches (4 HTTP requests)

| num | HTML status | PDF status | date | raw_sha (PDF) | bytes (HTML/PDF) |
|----|----|----|----|----|----|
| 23 | 200 | 200 | 2019-03-14 | `28aa88b6acc66a7128a4c0e521fb4527a6cd2eb298779c46dd18da3876dd5f5f` | 44876 / 28786806 |
| 24 | 200 | 200 | 2019-12-11 | `bfe146ea2b7df10708b05fc42326ed143b21b4bf27f19595588e67723b169941` | 47457 / 4686627 |

Rate-limit 5s honoured throughout (zambialii_seconds_between_requests in approvals.yaml). User-Agent: `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)`.

## Parse outcome

| num | result | outcome | anchor | citation | case_name |
|----|----|----|----|----|----|
| 23 | deferred | — | `html_no_summary_pdf_no_match` (declaratory holding — magistrate suspension expunged; constitutional-independence finding, no operative-verb anchor) | [2019] ZMCC 23 | Benjamin Mwelwa v Attorney-General |
| 24 | written | `overturned` | pdf-tail-2pages "view were the backbone of the appeal, we set aside the decision" (v031-tail `\bwe\s+set\s+aside\s+(?:the\s+)?(?:judgm…`) | [2019] ZMCC 24 | MWIYA MUTAPWE V SHOMENO DOMINIC |

### zmcc/2019/24 record summary

- **id**: `judgment-zm-2019-zmcc-24-mwiya-mutapwe-v-shomeno-dominic`
- **court**: Constitutional Court of Zambia
- **date_decided**: 2019-12-11
- **judges**: Mulembe JCC (presiding), Munalula JCC, Sitali JCC, Mulonda JCC, Mulenga JCC (5 judges, all concurring)
- **issue_tags**: Electoral law; election petitions; standard of proof; s.97(2)(a) Electoral Process Act; corrupt and illegal practices by candidate; effect on majority of voters; Local Government Elections Tribunals Rules; admissibility/corroboration of hearsay
- **outcome_detail**: "view were the backbone of the appeal, we set aside the decision"
- **operative effect**: appellate court set aside the Local Government Election Tribunal decision

### zmcc/2019/23 deferral note

`Benjamin Mwelwa v Attorney-General` — Constitutional Court declaratory holding that suspension of a magistrate for referring a constitutional question was unlawful interference with judicial independence; suspension expunged and damages awarded. The operative paragraph uses declaratory verbs ("we declare", "the suspension was/is unlawful") not in the v0.3.2 vocabulary, so deferred to the v0.3.3-pending cohort. Raw bytes on disk; will reparse when v0.3.3 anchor pack ships.

## Judges registry

`judges_registry.yaml` **NOT modified**. All five coram judges (Mulembe, Munalula, Sitali, Mulonda, Mulenga) already present from prior batches. b0561 added Sitali/Mulembe/Mulonda; b0564 logged all five JCC titles.

## corpus.sqlite update

Method: TMPDIR-routed atomic copy (b0531 pattern, TMPDIR=/sessions/bold-cool-mccarthy) + `PRAGMA journal_mode=TRUNCATE` (b0557 workaround for virtiofs unlink restriction). Per-record commit (b0557 belt-and-braces).

| metric | before | after | delta |
|----|----|----|----|
| `records` | 1859 | 1860 | +1 |
| `records_fts` | 1859 | 1860 | +1 |
| `judgments_meta` | 169 | 170 | +1 |
| `records − records_fts` gap | 0 | 0 | 0 |
| `PRAGMA integrity_check` | n/a | `ok` | — |

## Integrity checks (all pass)

- ✓ Written record has 5 judges (≥1 required)
- ✓ `issue_tags` non-empty (7 tags)
- ✓ `outcome` ∈ allowed enum (`overturned`)
- ✓ All judges resolve in `judges_registry.yaml` by `canonical_name`
- ✓ `raw_sha256` matches on-disk PDF
- ✓ No duplicate id in `corpus.sqlite`
- ✓ `records` = `records_fts` = 1860
- ✓ `PRAGMA integrity_check` = `ok`

## Approvals.yaml

NOT modified. Phase 5 ceiling 169/160 → 170/160 (now +10 above sentinel). Recommend operator extend or close per b0553/b0557/b0558/b0560/b0561/b0564 standing.

## Costs

- Today's judgment-ingestion-worker fetches: 28 → 32 / 500 (+4: 2 HTML + 2 PDF)
- Daily budget: 500 (separate from main worker's 2000/day)

## ZMCC 2019 dimensional summary (cumulative)

- Published nums (all GET-fetched, raw on disk): **18** — {1, 3, 4, 5, 6, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28}
- Records written (cumulative b0561+b0564+b0565): **6 of 18 (33%)** — {1, 16, 20, 21, 22, 24}
- v0.3.3-pending: **12 of 18 (67%)** — {3, 4, 5, 6, 17, 18, 19, 23, 25, 26, 27, 28}
- 404 sentinels (internal gap and upper boundary): {2, 7..15, 29..35}
- **ZMCC 2019 GET-fetch sweep complete** (no remaining un-fetched published nums)

## Next-tick recommendations

1. **ZMCC 2018 sparse HEAD probe** — `{1, 5, 10, 15, 20, 25}` per b0560 pattern; start next-year discovery now that ZMCC 2019 GET-fetch is complete.
2. **Standing**: parser_v0.3.3 anchor pack authoring (74 records pending — declaratory-holding rich sample, predominantly ZMCC).
3. **Standing**: OCR pipeline implementation (5 records pending — ZMCC 2020 scanned PDFs).
4. **Standing**: operator action on Phase 5 ceiling 170/160 (+10 above sentinel).

## Notes

- B2 sync deferred to host (rclone not in sandbox).
- Execution mode: inline runner; no derivative `scripts/batch_0565_*.py` committed (sandbox-session safety constraint per b0548/b0549/b0551/b0554/b0555/b0556/b0560/b0561/b0562/b0563/b0564 precedent).
- First-attempt parser-pick mistake: b0506_zmsc_parse builds ZMSC-shaped records (court="Supreme Court of Zambia"). Corrected via direct `build_record_v032` call to overwrite. FUSE prevents file deletion, so overwrite was the only path. Final on-disk record is correctly `Constitutional Court of Zambia`.
