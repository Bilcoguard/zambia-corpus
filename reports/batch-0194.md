# Batch 0194 — Phase 4 sis_mining closeout + sis_family opener

- **Date**: 2026-04-24
- **Phase**: phase_4_bulk
- **Sub-phase**: sis_mining (closeout) + sis_family (opener)
- **Parser version**: 0.5.0
- **User-Agent**: `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)`
- **Crawl delay**: 6 s (robots.txt 5 s + 1 s margin)

## Summary

- **Targets attempted**: 2 (plus 1 discovery fetch)
- **Records written**: 2 / 2 (100 %)
- **Fetches used**: 5 (4 ingest HTML+PDF pairs + 1 discovery)
- **Integrity checks**: CHECK1–5 all PASS (batch-scoped; no duplicate IDs
  introduced, all `source_hash` values match on-disk PDFs, all required
  fields populated, `amended_by`/`repealed_by` correctly empty)
- **Gaps logged this batch**: 0

## Robots.txt re-verification

Re-fetched `https://zambialii.org/robots.txt` at the start of this tick.
Policy unchanged since batch-0193:

- `User-agent: *` section:
  - `Allow: /`
  - `Disallow: /akn/zm/judgment/`
  - `Disallow: /akn/zm/officialGazette/`
  - `Disallow: /search/`, `/en/search/`, `/api/`, etc.
  - `Crawl-delay: 5`

All three URL paths used this tick (`/akn/zm/act/si/...`,
`commons.laws.africa/akn/zm/act/si/...`,
`/legislation/subsidiary?alphabet=A`) are permitted for `User-agent: *`.
No judgment or officialGazette paths fetched.

## Records ingested

| # | Year/No | Sub-phase | Record ID | Sections | PDF bytes |
|---|---------|-----------|-----------|----------|-----------|
| 1 | 2018/082 | sis_mining | `si-zm-2018-082-mining-appeals-tribunal-rules-2018` | 43 | 1 593 542 |
| 2 | 2023/038 | sis_family | `si-zm-2023-038-intestate-succession-rules-2023` | 77 |   450 346 |

### 1. Mining Appeals (Tribunal) Rules, 2018 — SI 82 of 2018

- **AKN URL**: https://zambialii.org/akn/zm/act/si/2018/82
- **PDF URL**: https://zambialii.org/akn/zm/act/si/2018/82/eng@2018-10-19/source.pdf
- **PDF sha256**: `0ff7bb29e2a10dcae0c617b3f9ea223e29781bf44f2d9d17265a6401aa4b9645`
- **Made under**: Mines and Minerals Development Act No. 11 of 2015
  (parent act already in corpus at `act-zm-2015-mines-and-minerals-development-act`)
- **Sub-phase**: `sis_mining` — closes out known-alphabet-M sis_mining
  candidates. Prior HEAD held 6 mining SIs (1 from batch ≤ 0192 —
  Ndola Lime Remission 2020/28 — plus 5 from batch 0193); this is the
  7th and the last novel candidate surfaced by discovery so far.

### 2. Intestate Succession Rules, 2023 — SI 38 of 2023

- **AKN URL**: https://zambialii.org/akn/zm/act/si/2023/38
- **PDF URL**: https://commons.laws.africa/akn/zm/act/si/2023/38/media/publication/zm-act-si-2023-38-publication-document.pdf
- **PDF sha256**: `18a78be7974bc4efeb325e87ce7abf5ce4fe72ef9fdf3b9142b38e60fd4ac628`
- **Made under**: Intestate Succession Act (Cap. 59 of the Laws of Zambia)
  (parent act already in corpus at `act-zm-1989-005-intestate-succession-act-1989`)
- **Sub-phase**: `sis_family` — **first** `sis_family` SI record in
  the corpus. HEAD had 0 `sis_family` SIs prior to this batch (family
  Acts were present — Marriage 1918, Matrimonial Causes 2007,
  Children's Code 2022, Affiliation 1995, Intestate 1989 — but no
  subsidiary instruments).

## Sub-phase rotation rationale

Per the batch-0193 next-tick plan: *"if yield thins below 3, rotate to
sis_family (priority_order item 8)."* Second-tier mining discovery
(parent-act back-references on MMDA 2015 Act /akn/zm/act/2015/11)
yielded 0 SI links — that page does not inline subsidiary legislation.
With only 1 novel mining SI remaining from alphabet=M (si/2018/82,
ingested this tick), mining yield for this tick was 1 → below the
3-record threshold → rotate.

`sis_family` is priority_order item 8 and was previously cold (0 SI
records). This batch therefore serves dual roles: **closeout** of
sis_mining and **opener** of sis_family.

## Discovery fetch — alphabet=A

- **URL**: https://zambialii.org/legislation/subsidiary?alphabet=A
- **sha256**: `5a135742534643dbcb4b8c61f532419ce35c4d3fcaad510f1a2ae088defe5449`
- **Cached at**: `_work/batch_0194_alphabet_A.html` (93 755 bytes)
- **Total SIs on page**: 20
- **Machine-tagged family candidates**: 0 (no titles matched keywords
  `adopt`, `affili`, `administration`)

### Hand-review of alphabet=A for next-tick sis_family candidates

A second-pass hand scan of the page (the machine filter was narrow) found
**one additional family-law SI** on alphabet=A that the regex missed:

- `/akn/zm/act/si/2016/8` — **Anti-Gender Based Violence (Court) Rules,
  2016** — made under the Anti-Gender-Based Violence Act 2011
  (parent act already in corpus at `act-zm-2011-001-anti-gender-based-violence-act`)

This is queued as a next-tick sis_family target. Note: the machine
filter keyed on `adopt|affili|administration of estate` which did not
match "Anti-Gender Based Violence"; the filter will be widened in
batch 0195 to include `gender-based|gbv|violence against|protection`.

## Budget status

- **Today's fetches**: 270 / 2 000 (13.5 %) — plenty of headroom.
  (Breakdown: 265 before this batch + 5 this batch.)
- **Today's bytes**: ≈ 204.1 MB
- **Rate-limit compliance**: all inter-request gaps ≥ 5 s (measured:
  one 6.0 s + two 5.2–5.3 s gaps; first request had no predecessor).

## Next-tick plan (batch 0195)

Continue `sis_family` rotation. Candidates identified this tick:

1. **`si/2016/8` Anti-Gender Based Violence (Court) Rules, 2016**
   — hand-identified from alphabet=A cache (parent-act AGBV Act 2011
   already in corpus)

Further discovery required. Candidate probes for next tick:

2. Fetch `https://zambialii.org/legislation/subsidiary?alphabet=J`
   (Juveniles Act cap 53 → probable juvenile/children orders)
3. Revisit cached alphabet=M / alphabet=I for Marriage/Matrimonial
   SIs (prior scans found none, but widen keyword filter)
4. Fetch `https://zambialii.org/legislation/subsidiary?alphabet=G`
   (Gender-based violence, Guardianship)
5. Parent-act back-reference probe on
   `/akn/zm/act/2022/12` (Children's Code Act) for commencement orders
   or general regulations

If sis_family discovery also thins below 3 novel candidates, rotate
to **sis_tax** (priority_order item 3) — a well-populated sub-phase
with many unspent candidates under alphabet=I (Income Tax) and
alphabet=C (Customs and Excise).

## Infrastructure notes (non-blocking)

- `rclone` still not available in tick sandbox → B2 sync deferred to
  host for 12 new raw files this tick (2 records this tick +
  10 from batches 0192–0193 pending).
- `corpus.sqlite` stale rollback-journal still blocks in-sandbox FTS
  rebuild; separate host-side maintenance task.
- 34 legacy-schema act JSON dupes under `records/acts/` remain
  unresolved (pre-existing; not introduced by this batch).
