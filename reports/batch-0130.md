# Batch 0130 Report

**Date:** 2026-04-17T14:42:39Z
**Phase:** 4 (Bulk Ingestion)
**Records committed:** 2 (8 attempted; 6 rejected as duplicates of existing corpus entries)
**Fetches:** 17
**Integrity:** PASS (on 2 committed records)

## Committed records (2)

- **Citizenship of Zambia (Amendment) Act, 1988** (Act No. 24 of 1988): 4 sections — new to corpus
  - `records/acts/1988/act-zm-1988-citizenship-of-zambia-act.json`
  - source: https://www.zambialii.org/akn/zm/act/1988/24/eng@1988-07-29/source.pdf
  - sha256: f5ffd2606f3fc3645af62ac853175a525110d67eb9119a0cc60bf9800438017a
- **Citizenship of Zambia (Amendment) Act, 1990** (Act No. 10 of 1990): 2 sections — new to corpus
  - `records/acts/1990/act-zm-1990-citizenship-of-zambia-act.json`
  - source: https://www.zambialii.org/akn/zm/act/1990/10/eng@1990-07-23/source.pdf
  - sha256: 47e4fe788b357fc47f5890bc9469cc76bb323b08ff533e2da0196ac930e92214

## Rejected as duplicates (6 — already in corpus)

The initial ZambiaLII listing scan (pages 9-10) returned candidates alphabetically
in the C-block (Children / Citizens / Citizenship) rather than the intended
"National..." block from batch 0129's next-tick notes, because pages 9-10 are
much earlier than expected in the alphabetical ordering. The dedup index
`_work/existing_urls.json` did not catch these duplicates because this worker
does not index ZambiaLII `eng@DATE` URL variants — only the bare AKN URLs.

Records fetched + parsed but NOT committed because canonical variants already
exist in git:

- Children's Code Act, 2022 (Act No. 12 of 2022) — canonical: `records/acts/act-zm-2022-012-the-childrens-code-act-2022.json`
- Citizens Economic Empowerment (Amendment) Act, 2021 (Act No. 5 of 2021) — canonical: `records/acts/2021/act-zm-2021-005-citizens-economic-empowerment-amendment-act-2021.json`
- Citizens Economic Empowerment (Amendment) Act, 2010 (Act No. 43 of 2010) — canonical: `records/acts/2010/act-zm-2010-043-citizens-economic-empowerment-amendment-act-2010.json`
- Citizenship of Zambia (Amendment) Act, 1986 (Act No. 17 of 1986) — canonical: `records/acts/1986/act-zm-1986-017-citizenship-of-zambia-amendment-act-1986.json`
- Citizenship of Zambia Act, 1975 (Act No. 26 of 1975) — canonical: `records/acts/1975/act-zm-1975-026-citizenship-of-zambia-act-1975.json`
- Citizenship of Zambia Act, 2016 (Act No. 33 of 2016) — canonical: `records/acts/act-zm-2016-033-the-citizenship-of-zambia.json`

## Known issues / gaps

- The on-disk dedup index (`_work/existing_urls.json`) is URL-source-sensitive:
  earlier batches used Parliament / raw-PDF URLs; ZambiaLII `eng@DATE` URLs
  are not present in the index, so re-fetches from ZambiaLII can generate
  apparent "new" candidates that are in fact covered. Next tick should
  **normalise URLs to title+act_num+year** when checking dedup, not raw URL.
- Citizens Economic Empowerment Act, 2006 (Act No. 9 of 2006) fetched but
  yielded 0 sections from both HTML and PDF; logged to gaps.md.
- 6 duplicate-content files exist on disk as untracked entries (see list above);
  they are **not** committed and will not affect git state. The sandbox does
  not permit deletion, so they will remain as untracked orphans until the
  host removes them.
- ID naming for the 2 new records does not include the act number prefix
  (`act-zm-1988-citizenship-of-zambia-act` rather than `act-zm-1988-024-...`).
  This is because deletion was not permitted, so the original filename had to
  be retained. A follow-up cleanup tick should rename these records.

## Fetch accounting

- Listing page fetches: 2 (pages 9 and 10)
- Act HTML fetches: 8 (of which 6 produced duplicates, now rejected)
- PDF fallback fetches: 7 (one per Act where HTML had <3 sections)
- Total: 17 fetches, well under daily budget (195/2000 for 2026-04-17)

## Next tick

Phase 4 continues. Target "National..." Acts listed in batch 0129's next-tick
notes: **National Anthem Act 1973, National Archives Act 1969, National Arts
Council Act 1994, National Assembly Speaker's Retirement Benefits Act 1997,
National College for Management (Repeal) Act 2005, National Council for
Scientific Research Act 1967, National Food and Nutrition Commission Act 1967,
National Health Services Act 1995.** These are earlier in the alphabetical
ZambiaLII listing than pages 9-10; the next tick should use the ZambiaLII
search endpoint or target pages 8-9 explicitly for N-block Acts.
