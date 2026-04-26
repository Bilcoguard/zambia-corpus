# Batch 0265 Report

**Phase:** 4 (bulk ingest)
**Sub-phase:** acts_in_force (alphabet T probe — sweep 1)
**Date:** 2026-04-26
**Records added:** 8
**Yield:** 8/8 (100%)

## Records

| ID | Title | Sections | Source |
|---|---|---|---|
| act-zm-1929-038-treasury-bills-act-1929 | Treasury Bills Act, 1929 | 7 | https://zambialii.org/akn/zm/act/1929/38/eng@1996-12-31 |
| act-zm-1929-042-tanganyika-victoria-memorial-institute-act-1929 | Tanganyika Victoria Memorial Institute Act, 1929 | 16 | https://zambialii.org/akn/zm/act/1929/42/eng@1996-12-31 |
| act-zm-1929-054-theatres-and-cinematograph-exhibition-act-1929 | Theatres and Cinematograph Exhibition Act, 1929 | 12 | https://zambialii.org/akn/zm/act/1929/54/eng@1996-12-31 |
| act-zm-1963-044-tax-reserve-certificates-act-1963 | Tax Reserve Certificates Act, 1963 | 4 | https://zambialii.org/akn/zm/act/1963/44/eng@1996-12-31 |
| act-zm-1964-018-traditional-beer-levy-act-1964 | Traditional Beer (Levy) Act, 1964 | 12 | https://zambialii.org/akn/zm/act/1964/18/eng@1996-12-31 |
| act-zm-1965-026-taxation-provisional-charging-act-1965 | Taxation (Provisional Charging) Act, 1965 | 4 | https://zambialii.org/akn/zm/act/1965/26/eng@1996-12-31 |
| act-zm-1968-037-therapeutic-substances-act-1968 | Therapeutic Substances Act, 1968 | 13 | https://zambialii.org/akn/zm/act/1968/37/eng@1996-12-31 |
| act-zm-1970-064-trusts-restriction-act-1970 | Trusts Restriction Act, 1970 | 9 | https://zambialii.org/akn/zm/act/1970/64/eng@1996-12-31 |

## Provenance

All 8 records fetched from zambialii.org. Robots.txt re-verified at tick start
(sha256 fce67b697ee4ef44e0694134e23108c2701b5e7661eed885013efb9b75dcd8f0
unchanged across batches 0193-0265). Crawl-delay 5s honoured at 6s margin.
User-Agent: KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com).

## Discovery

Probed `/legislation?alphabet=T&nature=act` this tick (raw cached at
`raw/zambialii/_alphabets/legislation-alphabet-T-20260426T120505Z.html`,
sha256 b8651c053378d3011819214625c1b51a75f44832546236724c4ef29c777a1e38,
142,037 bytes). Filter cross-checked 26 listing candidates against
records/acts/**/*.json by `(yr, num)` key:

- 15 already on disk (filtered out)
- 11 new candidates
- 8 picked (chronological order, MAX_BATCH_SIZE cap filled exactly)
- 3 reserved residuals carry to next tick: 1972/26 Termination of Pregnancy
  Act, 1972 + 1972/37 Technical Education and Vocational Training Act, 1972
  + 1973/49 Trades Charges Act, 1973

## Integrity

- CHECK1a (batch unique IDs): PASS 8/8
- CHECK1b (on-disk presence): PASS 8/8
- CHECK2 (amended_by refs resolve): PASS (0 refs)
- CHECK3 (repealed_by refs resolve): PASS (0 refs)
- CHECK4 (source_hash sha256 matches raw): PASS 8/8 against
  raw/zambialii/act/(1929,1963,1964,1965,1968,1970)/
- CHECK5 (required fields present): PASS 128 (= 16 × 8)
- CHECK6 (cited_authorities refs resolve): PASS (0 refs)

## Notes

- All 8 records parsed cleanly via `akn-section` HTML; no PDF fallback
  required. Smallest 4 sections (1963/44 Tax Reserve Certificates Act +
  1965/26 Taxation Provisional Charging Act); largest 16 sections (1929/42
  Tanganyika Victoria Memorial Institute Act).
- Possible cap-form overlap flagged for human review: 1929/54 Theatres and
  Cinematograph Exhibition Act, 1929 has a chapter-form pre-existing record
  at id `act-zm-cap-158-theatres-and-cinematograph-exhibition-act`. The
  `(yr, num)`-keyed filter treats them as distinct (no silent overwrite —
  IDs differ). Recommend canonicalising or marking the 1929 record as the
  original-version predecessor of the cap consolidation in a follow-up tick.
- Continues acts_in_force alphabetic walk from batches 0253–0264. 100%-yield
  streak now extends across batches 0246–0265 (20 consecutive at 100%).
