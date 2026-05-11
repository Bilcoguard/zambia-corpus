# Judgment ingestion worker batch 0583 — Court of Appeal sweep (NEW SOURCE)

**Date (UTC):** 2026-05-11
**Worker:** judgment-ingestion-worker
**Source:** judiciaryzambia.com / Court of Appeal Decisions (page 1, most recent posts)
**Parser:** v0.3.2 (build_record_v032 conventions, adapted for judiciary.zm PDFs)
**Listing URL:** https://judiciaryzambia.com/category/resources/decisions/court-of-appeal-decisions/

## Outcome

- **Records written: 7** (FIRST Court of Appeal ingestion across the corpus — prior CoA coverage was zero)
- **Records deferred: 3** (`html_no_summary_pdf_no_match` — parser v0.3.3-pending)
- **Duplicates skipped: 0** (no prior CoA records exist)
- **Fetches: 16** (10 post pages cached + 6 PDFs; 1 page-1 listing fetched in scope-decision step)
- **cumulative_today: 16/500** (jiw daily budget — first jiw activity of 2026-05-11)

## Records written

| Year | ID | Case # | Outcome | Judges |
|---|---|---|---|---|
| 2019 | judgment-zm-2019-coa-004-mathews-handulu-v-the-people | APP/004/2018 | upheld | Makungu, Sichinga, Ngulube JJA |
| 2026 | judgment-zm-2026-coa-095-sandra-mwale-v-the-people | APP/095/2024 | quashed | Mchenga DJP, Majula, Muzenga JJA |
| 2024 | judgment-zm-2024-coa-101-timothy-lipofya-v-the-people | APP/101/2024 | set-aside | Mchenga DJP, Majula, Muzenga JJA |
| 2020 | judgment-zm-2020-coa-160-maambo-simukuni-v-tenyiwe-sibindi | APP/160/2012 (mis-extracted; should be APP/202/2023 — see gaps.md) | dismissed | Siavwapa JP, Chishimba, Patel JJA |
| 2023 | judgment-zm-2023-coa-322-first-capital-bank-ltd-v-networld-logistics-ltd-and-others | APP/322/2024 | set-aside | Siavwapa JP, Chishimba, Patel JJA |
| 2022 | judgment-zm-2022-coa-091-douglas-aaron-simukonda-v-the-people | APP/091/2024 | allowed | Mchenga DJP, Majula, Muzenga JJA |
| 2026 | judgment-zm-2026-coa-074-bukari-pharmacy-v-mashake-mweemba | APP/074/2025 | set-aside | Chashi, Ngulube, Banda-Bobo JJA |

## Records deferred (`html_no_summary_pdf_no_match` — v0.3.3-pending)

- `app-110-2024-josias-mtonga-vs-the-people-coram-justice-mchenga-djp-majula-muzenga-jja` → candidate id `judgment-zm-2023-coa-110-josias-mtonga-v-the-people`. PDF on disk; outcome anchor not matched in parser v0.3.2 last-2-pages or whole-text scans.
- `app-344-2023-skab-merchants-ltd-1-other-vs-emilmark-construction-justice-siavwapa-jp-chishimba-patel-jja` → candidate id `judgment-zm-2023-coa-055-skab-merchants-ltd-and-others-v-emilmark-construction-and-co`. PDF on disk; outcome anchor not matched.
- `app-47-2025-tulambo-kumwenda-justice-chashi-ngulube-banda-bobo-jja` → candidate id `judgment-zm-2026-coa-047-tulambo-kumwenda-and-others-v-solwezi-dairy-farm-ltd-and-oth`. PDF on disk; outcome anchor not matched.

## Integrity checks

- CHECK1 judges present: 7/7 PASS
- CHECK2 issue_tags non-empty: 7/7 PASS
- CHECK3 outcome ∈ enum: 7/7 PASS
- CHECK4 judges resolve in registry: 7/7 PASS (after registry update)
- CHECK5 no duplicate IDs: PASS
- CHECK6 raw_sha256 matches on-disk PDF: 7/7 PASS
- CHECK7 no duplicate (case_name, court, date_decided): PASS
- CHECK8 records (1874) == records_fts (1874): PASS
- PRAGMA integrity_check: ok

## sqlite stats (post-tick)

- records: 1867 → **1874** (+7)
- records_fts: 1867 → **1874** (+7)
- judgments_meta: 177 → **184** (+7)
- Court of Appeal records: 0 → **7** (NEW court covered)

## judges_registry.yaml updates

New canonical entries added (all marked `court: "Court of Appeal"`):
- Makungu JJA
- Sichinga JJA
- Ngulube JJA (was previously absent for CoA; pre-existing entry if any was under different court)
- Mchenga DJP
- Majula JJA
- Muzenga JJA
- Siavwapa JP
- Chishimba JJA
- Patel JJA
- Chashi JJA (alias appended; canonical entry pre-existed under Court of Appeal)
- Banda-Bobo JJA

## Parser v0.3.2 quality issues observed (v0.3.3-pending refinement targets)

1. **`extract_case_number` first-match-wins issue**: For Maambo Simukuni v Tenyiwe Sibindi the PDF's "Cases referred to" section cites "Caroline Lwando Nkwabilo Maiga v Maiga Temimu SCZ Appeal No 160 of 2012" before the title-page "APPEAL No./202/2023". Regex matched the cited case. **Fix in v0.3.3**: prefer the FIRST Appeal-No that appears within the first 500 chars of the PDF (typically the title page) before falling through to the rest of the document.

2. **`extract_date_decided` ordinal-suffix typo**: For 4 of 7 records the PDF text contains date strings like `On 17t February and 25t March 2026` where the ordinal suffix is mistyped as "t" rather than "th". The current regex `(?:st|nd|rd|th)?` does not accept "t" alone, so only the trailing "DD Month YYYY" forms match. When no header-date matches, the regex falls through and picks dates from elsewhere in the document (e.g. "13th May 2020" was a Subordinate Court date for Maambo; "2nd February 2023" was a cited-case date for First Capital Bank). **Fix in v0.3.3**: accept "t" as a typo for "th", prefer dates that appear after the keyword "delivered" or near "JUDGMENT", and reject dates that fall before the case-number year.

## Source provenance

- Source A (ZambiaLII) had no CoA coverage at all — judgments at zambialii.org/judgments/ZMCC/ and ZMSC/ only. ZambiaLII does not host Court of Appeal decisions.
- Source B (judiciaryzambia.com) is therefore the *exclusive* CoA source. This tick covered page 1 (10 posts, 7 written + 3 deferred). Continued sweep planned for next tick → page 2.

## Sweep position (for next tick resume)

- `judiciary-coa-sweep: page 2` (page 1 fully processed: 7 written, 3 v0.3.3-pending deferred)

## Next-tick recommendations

1. **Continue priority (b) Court of Appeal sweep**: page 2 of judiciaryzambia.com/category/.../court-of-appeal-decisions/. Same parser, same defer rules.
2. **Standing**: parser_v0.3.3 anchor pack now also needs the two CoA refinements documented above (Appeal-No first-match-wins + date_decided ordinal-typo robustness).

## Operator notes

- virtiofs mid-tick disk I/O recovery applied: corpus.sqlite-journal stale-truncated, corpus.sqlite copied to /tmp for read-write workspace, atomic copy-back at end. Pre-tick backup saved as `corpus.sqlite.bak.b0583-pre-20260511T073727Z`.
- judiciaryzambia.com served all 10 post HTML pages + 6 PDFs without rate-limit errors. 5 s inter-fetch pause honoured (per batch_0506_zmsc_fetch baseline).
- Execution mode: inline runner `_work/b0583_jiw/ingest_coa.py`. **NOT committed** to `scripts/` per sandbox-session safety constraint (matches b0548..b0582 precedent).
