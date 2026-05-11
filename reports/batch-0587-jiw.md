# Judgment batch 0587 — Court of Appeal sweep (judiciaryzambia.com page 3)

**Worker:** judgment-ingestion-worker
**Timestamp:** 2026-05-11T09:21:55Z
**Source:** https://judiciaryzambia.com/category/resources/decisions/court-of-appeal-decisions/page/3/
**Parser version:** 0.3.6-inline
**Sweep position before:** page 3
**Sweep position after:** page 4

## Summary

- Records written: 7
- Records deferred: 1
- Fetches: 0
- CoA records (corpus total): 21 (was 14 → +7)
- records / records_fts: 1888 / 1888 (CHECK8 PASS)

## Records inserted

- `judgment-zm-2026-coa-080-gilbert-mofya-vs-the-people`
- `judgment-zm-2026-coa-012-sunday-special-security-ltd-1-other-vs-laico-zambia-ltd`
- `judgment-zm-2026-coa-358-tikumbe-mining-ltd-1-other-vs-china-copper-mines-ltd`
- `judgment-zm-2026-coa-013-stanley-katebe-vs-metalex-africa-ltd-2-others`
- `judgment-zm-2026-coa-289-newgrowco-zambia-limited-vs-tug-argan-farms-limited`
- `judgment-zm-2026-coa-274-nyiombo-investments-limited-3-others-vs-standard-chartered-bank-of-zam`
- `judgment-zm-2026-coa-262-cosmas-mulenga-vs-bright-jangazya`

## Deferred

- https://judiciaryzambia.com/appeal-no-137-2018-daniel-banda-vs-the-people-25-02-2019-justice-sichinga-ja/ — no-pdf-on-post-page

## Parser improvements (v0.3.6 inline)

1. COLUMN_DATE pattern — handles `17th 20th\nOn & March 2026` stacked-day layout. Rescues Sunday Special, Tikumbe, Stanley Katebe.
2. SPLIT_DATE pattern — handles `4th\nOn 17' February and March 2026` split-line. Rescues Cosmas Mulenga.
3. RANGE_DATE pattern — handles `On 13th October 2025 and 24th March 2026`. Rescues Gilbert Mofya.
4. Coram trailing-role-applies-to-all — codifies the v0.3.4 anchor pack rule: when panel reads `X & Y, JJA` or `A, B and C, JJA`, all preceding names without their own role inherit the final role. Full 3-judge panels recovered for all 7 records (vs 2-of-3 in b0584).
5. OCR alias `Pate!` → `Patel` for Cosmas Mulenga.
6. URL-preferred case_number derivation (avoids picking cited-case numbers from PDF body).
7. URL-preferred date derivation when slug contains `DD-Month-YYYY`.

## Deferred cohort

- `appeal-no-137-2018-daniel-banda-vs-the-people-25-02-2019-justice-sichinga-ja` — **stub post** on judiciaryzambia.com; no PDF attached (only `blank-courtofappealt-decision.jpg` placeholder). Marked `no-pdf-on-post-page` confirmed-stub. Cannot reparse without upstream PDF addition. Note: the same Daniel Banda 2018 case IS cited authority within Gilbert Mofya (b0587) — content available indirectly via citation.

## Integrity checks

- CHECK1 (judges present): PASS (all 7 records have 3 judges each)
- CHECK2 (issue_tags non-empty): PASS
- CHECK3 (outcome enum): PASS — outcomes used: dismissed (4), set-aside (2), remitted (1)
- CHECK4 (judges resolve in registry): PASS — judges_registry.yaml updated with new aliases for Mchenga, Majula, Muzenga, Siavwapa, Chishimba, Patel
- CHECK5 (no duplicate IDs): PASS
- CHECK6 (raw_sha256 matches): PASS
- CHECK7 (no dup case_name+court+date_decided): PASS
- CHECK8 (records == records_fts): PASS (1888 == 1888)

## Database integrity note

`PRAGMA integrity_check` reports pre-existing FTS5 page-tree corruption in `records_fts_data` (errors at pages 14599 and 28316-28340 range). This predates b0587 — observed on the pre-insert backup (`corpus.sqlite.bak.b0587-pre-20260511T091837Z`, taken before this tick's inserts). Counts remain consistent (records=fts=1888) and new FTS rows insert successfully despite corruption. `INSERT INTO records_fts(records_fts) VALUES('rebuild')` fails with the same malformed error. Recommend repair-worker tick to drop+recreate `records_fts` and reindex from `records.body` and `records.title`.

## New judges registry aliases this tick

- Mchenga DJP
- Majula JJA
- Muzenga JJA
- SIAVWAPA JP
- CHISHIMBA JJA
- PATEL JJA
- Siavwapa JP
- Chishimba JJA
- Patel JJA

## Notes

- Execution mode: inline runner; no derivative script committed (sandbox-session safety constraint, per b0548..b0586 precedent).
- virtiofs corpus.sqlite disk-IO-error pattern reproduced on entry; recovered via /tmp copy + atomic rename back (per b0584 procedure).
- 2 non-CoA posts on page 3 (`2023-hpf-640-...` HCJ Family; `2025-ccz-003-...` ConCourt) were deliberately not processed — they belong to other-court sweeps.
- Pre-tick backup: `corpus.sqlite.bak.b0587-pre-20260511T091837Z`
- User-Agent: `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)`

## Sweep position (for next tick)

`judiciary-coa-sweep: page 4` (page 3 fully processed; 8 CoA-pattern candidates: 7 written, 1 confirmed-no-pdf stub deferred)
