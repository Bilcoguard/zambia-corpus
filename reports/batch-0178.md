# Batch 0178 — Phase 4 sis_corporate

**Started:** 2026-04-24T11:03:58Z
**Completed:** 2026-04-24T11:04:43Z
**Phase / sub-phase:** Phase 4 bulk — `sis_corporate` (priority_order item 2)
**Batch size used:** 3 ingests + 2 discovery = 8 fetches (MAX_BATCH_SIZE = 8 records)

## Scope

Ingest the 3 strongest novel corporate-keyword SI candidates surfaced by
batch-0177 pages 9-10 discovery of
`https://zambialii.org/legislation/subsidiary`:

1. **si/2015/87** — Diplomatic Immunities and Privileges (ZEP-RE PTA
   Re-Insurance Company) Order, 2015 (corporate entity; re-insurance)
2. **si/2014/56** — Income Tax (European Investment Bank) (Approval and
   Exemption) Order, 2014 (bank; investment)
3. **si/2016/18** — Insurance Premium Levy (Exemption) Order, 2016
   (insurance; regulatory)

Continue `/legislation/subsidiary` discovery sweep with pages 11 and 12.

## Results

### Records committed (3)

| ID | Sections | Source | Raw size |
| --- | --- | --- | --- |
| `si-zm-2015-087-diplomatic-immunities-and-privileges-zep-re-pta-re-insurance-company-order-2015` | 27 | PDF | 160,546 B |
| `si-zm-2014-056-income-tax-european-investment-bank-approval-and-exemption-order-2014` | 3 | PDF | 73,613 B |
| `si-zm-2016-018-insurance-premium-levy-exemption-order-2016` | 2 | PDF | 33,259 B |

All three followed the HTML → PDF-fallback pattern (HTML AKN page is
sparse, PDF attachment contains the text). Titles pulled from og:title
where possible and sanity-checked against title hints.

### Gaps (0)

None.

### Discovery sweep (pages 11–12)

Both pages returned HTTP 404 from ZambiaLII
(`https://zambialii.org/legislation/subsidiary?page=11` and `?page=12`,
17,595 bytes each — the standard Django 404 body). This confirms the
`/legislation/subsidiary` listing is exhausted at page 10 (50
entries/page × 10 pages = ~500 SIs listed), even though ZambiaLII's
`/akn/zm/act/si/` namespace obviously contains many more SI records
than that. The listing is therefore a bounded discovery channel and is
now exhausted for sis_corporate sweeping.

Novel corporate candidates from this batch: **0**.
Novel other candidates from this batch: **0**.

### Fetches (8 this batch)

- 3 × AKN HTML (200 OK, crawl-delay 5s honoured)
- 3 × AKN PDF fallback (200 OK)
- 2 × /legislation/subsidiary listing (404 — listing exhausted)

Today cumulative: **~80 / 2000** (well within daily budget).

## Integrity checks (batch-scoped)

- **CHECK1** unique IDs within batch — **PASS** (3 unique)
- **CHECK2** no YYYY-NNN prefix collision vs `git ls-tree HEAD records/sis/` — **PASS**
- **CHECK3** source_hash matches raw PDF bytes on disk (sha256) — **PASS** (3/3 verified)
- **CHECK4** amended_by / repealed_by / cited_authorities cross-refs resolve — **PASS** (none in batch)
- **CHECK5** required fields + format (source_url, source_hash, fetched_at ISO-8601 UTC, parser_version, sections) — **PASS**

Corpus-wide CHECK1 not re-run (documented 42 pre-existing Appropriation
Act duplicate-ID entries from batch-0173 persist in `gaps.md`, unrelated
to this batch, queued for future cleanup tick).

## Next-tick plan

`/legislation/subsidiary` listing is now exhausted (pages 11–12 return
404; listing ends at page 10). Must pivot discovery channel.
Preference order:

1. **Seed-list pivot** — build a direct seed list from Companies Act
   2017 referenced SIs (Tenth Schedule / commencement SIs), BoZ SI
   catalogue (boz.zm), PIA SI catalogue (pia.org.zm), SEC SI
   catalogue (seczambia.org.zm), PACRA SI catalogue. Much higher
   corporate-yield density than general keyword sweep over a generic
   subsidiary listing.
2. **ZambiaLII year-indexed AKN traversal** — iterate
   `https://zambialii.org/akn/zm/act/si/YYYY` index pages for 2010-2026,
   compare to HEAD, apply CORPORATE_RE word-boundary filter.
3. **Government Gazette archive** — if accessible; for SIs not yet
   indexed on ZambiaLII.
4. **Regulator direct downloads** — PACRA, ZRA, BoZ, PIA, SEC, ZPPA,
   ZEMA, ODPC SI / Directive pages.

Strongly recommend (1) — Phase 4 priority_order item 2 (`sis_corporate`)
is best served by targeted seed lists rather than keyword-matching
against a generic subsidiary listing, and the listing channel has now
empirically exhausted its novel corporate yield.

## Corpus state after batch

- HEAD acts (records/acts): 899 (unchanged)
- HEAD SI records committed via this batch: +3 → 52 SI JSONs on disk
- parser_version: 0.5.0
