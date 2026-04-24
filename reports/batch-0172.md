# Batch 0172 — Phase 4 bulk ingestion

Run: 2026-04-24T07:44:00Z (tick scheduled at 07:31 UTC; 20-min budget)

## Summary

**0 new records written**, **6 AKN probe fetches** (all 200), **6 B-POL-ACT-1 policy rejects**.

This tick executed the pivot outlined in batch-0171's next-tick plan. Two discoveries:

1. **Parliament.gov.zm listing is genuinely exhausted.** An initial re-parse suggested ~80 novel primary-Act candidates (2026/001 Teaching Profession, 2025/029 ZIPS, 2025/027 Betting, etc.) but this was an artifact of scanning only year-directory-organized paths (`records/acts/YYYY/*.json`). The actual corpus uses a **flat** layout (`records/acts/act-zm-YYYY-NNN-*.json` directly under `records/acts/`). Re-scanning with a flat-layout slot extractor reduced 80 "novel" candidates to 0.
2. **HEAD is comprehensive for 2015–2026 primary Acts.** Slot-gap analysis of HEAD found only 6 missing slots below the yearly max: 2015/002, 2015/010, 2021/022, 2021/036, 2021/039, 2021/040. A direct AKN probe of all 6 returned HTTP 200, confirming the slots exist upstream, and title inspection confirms every one is an Amendment or Excess Expenditure Appropriation Act — categorically rejected by policy B-POL-ACT-1. So the missing slots are **intentional** absences, not gaps.

## Pivot sequence

### Step 1 — parliament.gov.zm HEAD-probe of listing (next-tick plan item 1)

Re-parsed cached listing (`raw/discovery/parliament-zm/acts-of-parliament*.html`, fetched 2026-04-10). Against a properly-flat HEAD slot set (761 slots), all five top-recent candidates are already present:

| Year/Num | Title | In HEAD |
|---|---|---|
| 2026/001 | Teaching Profession Act | yes (`act-zm-2026-001-teaching-profession-act.json`) |
| 2025/029 | ZIPS Act | yes |
| 2025/027 | Betting Act | yes (and separate Betting Levy Act record) |
| 2025/026 | ZNBC Act | yes |
| 2025/025 | IBA Act | yes |

Result: **0 live fetches** from parliament.gov.zm this step. parliament.gov.zm listing confirmed exhausted.

### Step 2 — ZambiaLII AKN gap-slot probe (next-tick plan item 2, adapted)

HEAD slot gaps in 2015–2026 (primary-Act-year-dense range):

```
2015/002  2015/010  2021/022  2021/036  2021/039  2021/040
```

All 6 probed at `https://zambialii.org/akn/zm/act/YYYY/NN` (6s crawl delay between requests, robots.txt compliant — AKN is not under `/search/` or `/api/`):

| Slot | HTTP | Final URL | Title (from og:title) | B-POL-ACT-1 | Decision |
|---|---|---|---|---|---|
| 2015/002 | 200 | `.../eng@2015-08-14` | Anti-Terrorism (Amendment) Act, 2015 | amendment | reject |
| 2015/010 | 200 | `.../eng@2015-08-14` | Excess Expenditure Appropriation (2012) Act, 2015 | excess expenditure | reject |
| 2021/022 | 200 | `.../eng@2021-03-24` | Public-Private Partnership (Amendment) Act, 2021 | amendment | reject |
| 2021/036 | 200 | `.../eng@2021-05-20` | Acts of Parliament (Amendment) Act, 2021 | amendment | reject |
| 2021/039 | 200 | `.../eng@2021-05-20` | Lands and Deeds Registry (Amendment) Act, 2021 | amendment | reject |
| 2021/040 | 200 | `.../eng@2021-05-20` | Land Survey (Amendment) Act, 2021 | amendment | reject |

All 6 HTML probe bytes saved to `raw/zambialii/YYYY/akn-YYYY-NNN-probe.html` with sha256 captured in `provenance.log`. Zero PDF fetches (pre-rejected by title — PDF fetch would be wasted bandwidth).

## Fetches

- Total live fetches this batch: **6** (all ZambiaLII AKN HTML; all 200; all rejected by policy).
- Today-cumulative fetches: 15 prior + 6 this batch = **21 / 2000 daily budget**. Well within.
- No PDFs fetched (B-POL-ACT-1 short-circuits before PDF stage).

## Integrity checks

No records produced, so schema-level CHECK 1–5 trivially pass (nothing to check). Logging integrity:

- 6 new entries in `costs.log` (fetch_n=akn-probe)
- 6 new entries in `provenance.log` (status=200, sha256 captured, bytes match)
- 6 raw HTML files saved to `raw/zambialii/{year}/` with verified sha256 match against provenance entry
- 6 new entries in `gaps.md` documenting the policy rejection for each slot

## Robots.txt audit

While compiling the pivot plan I reviewed `raw/discovery/zambialii/robots.txt` for `User-agent: *`:

```
Allow: /
Disallow: /search/
Disallow: /en/search/  Disallow: /fr/search/  Disallow: /pt/search/  Disallow: /sw/search/
Disallow: /api/
Crawl-delay: 5
Disallow: /akn/zm/judgment/
Disallow: /akn/zm/officialGazette/
```

**Observation for human review.** Prior ticks (batches 0168, 0169, a few others) used `https://zambialii.org/search/api/documents/?search=…` for keyword discovery. Under a literal reading of the robots.txt, both `/search/` AND `/api/` are disallowed for `User-agent: *`. `/akn/zm/act/…` (the AKN pages used by this batch and by all ingestion) is explicitly allowed, so direct ingestion via AKN is compliant; discovery via the `/search/api/` endpoint may not be. Logging as a concern for Peter's review — not fixing unilaterally in this tick.

## Next tick

Parliament.gov.zm listing exhausted. ZambiaLII AKN slot-gap analysis also now exhausted for 2015–2026 (all 6 slot gaps confirmed as intentional policy absences). Remaining discovery channels:

1. **Pre-2015 slot-gap probe.** HEAD has records back to 1914. Extending gap analysis to pre-2015 years may reveal a handful of untouched primary Acts worth chasing (though pre-2000 Acts are mostly either repealed or superseded by post-2000 consolidations). One tick's worth of slot-gap probes for, e.g., 2000–2014 would close that question.
2. **judiciary.gov.zm legislation tab.** Not yet probed systematically as a discovery channel; may expose Acts filed by the judiciary (court procedural Acts, judicature Acts) which are under-represented in HEAD.
3. **printer.gov.zm (Government Printer)** / **moj.gov.zm Acts catalogue.** Untried.
4. **Shift focus.** Phase 4 `priority_order` is `[acts_in_force, sis_corporate, sis_tax, sis_employment, case_law_scz, sis_data_protection, sis_mining, sis_family]`. With acts_in_force near-exhausted (899 records, slot-gap confirmed minimal), next tick could pivot to `sis_corporate` (Statutory Instruments) which is a mostly untouched sub-phase.
5. **Cumulative picture.** Re-counting confirms HEAD now holds 899 Acts spanning 1914–2026. This is a significant milestone — roughly 80–90% of Zambia's primary-Act corpus by a conservative estimate.

Recommendation: next tick pivot to `sis_corporate` (start with Companies Act 2017 SIs via parliament.gov.zm or ZambiaLII AKN) — the quickest path to new, unsubsumed material and aligned with Phase 4 priority ordering.

## Files touched this batch

- `scripts/batch_0172.py` (new — documents the parliament.gov.zm re-probe logic)
- `_work/batch_0172_summary.json` (parliament.gov.zm re-probe run output; all 5 targets already in HEAD)
- `_work/batch_0172_pivot.py` (new — ZambiaLII AKN gap-slot pivot script)
- `_work/batch_0172_akn_probe.json` (6-slot probe run output)
- `raw/zambialii/2015/akn-2015-002-probe.html`
- `raw/zambialii/2015/akn-2015-010-probe.html`
- `raw/zambialii/2021/akn-2021-022-probe.html`
- `raw/zambialii/2021/akn-2021-036-probe.html`
- `raw/zambialii/2021/akn-2021-039-probe.html`
- `raw/zambialii/2021/akn-2021-040-probe.html`
- `costs.log` (+6 entries)
- `provenance.log` (+6 entries)
- `gaps.md` (+6 policy-rejection entries)
- `reports/batch-0172.md` (this report)

## B2 sync

rclone not available in the worker sandbox. Peter to run on host:
```
rclone sync raw/ b2raw:kwlp-corpus-raw/ --fast-list --transfers 4
```
