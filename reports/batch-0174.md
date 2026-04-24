# Batch 0174 — Phase 4 sis_corporate discovery probe

- started: 2026-04-24T09:09:26Z
- finished: 2026-04-24T09:09:29Z
- elapsed: 2.4s
- listing url: https://zambialii.org/legislation/subsidiary?page=4
- raw file: raw/zambialii/discovery/subsidiary-page-04.html
- raw sha256: 548199bd4e379ef025ba80cd2f6d7be611b8d391e77f7c1a5e8fdad991bcf1fe
- raw bytes: 162254

## Findings

- raw <a> tags matching `/akn/zm/act/si/YYYY/N`: 50
- unique (year, num) candidates on page: 50
- existing si records in HEAD (records/sis): 87
- novel (year, num) slots vs HEAD: 44
- novel + corporate-keyword match: 2
- novel + other (non-corporate) keyword: 42

## Corporate candidates (sorted by year desc, num asc)

- SI 2020/27: Income Tax (Remission) (Ndola Lime Company Limited) Order, 2020  _(matched: compan)_
- SI 2020/28: Mines and Minerals Development (Remission) (Ndola Lime Company Limited) Regulations, 2020  _(matched: compan)_

## Non-corporate novel candidates (preview, first 20)

- SI 2021/1: Forest Reserve No. 4: Maposa (Cessation) Order, 2021
- SI 2021/2: Kasama National Forest No. P. 47: (Alteration of Boundaries) Order, 2021
- SI 2021/13: Worker’s Compensation (Domestic Workers) Regulations, 2021
- SI 2021/15: Diplomatic Immunities and Privileges (International Centre for Tropical Agriculture) Order, 2021
- SI 2021/104: Value Added Tax (Zero Rating) (Amendment) Order, 2021
- SI 2021/105: Value Added Tax (Exemption) (Amendment) Order, 2021
- SI 2021/106: Value Added Tax (Electronic Fiscal Devices), (Amendment) Regulations, 2021
- SI 2021/109: Plant Variety and Seeds (Amendment) Regulations, 2021
- SI 2021/112: Road Traffic (Fees) Regulations, 2021
- SI 2021/114: Provincial and District Boundaries (Division) (Amendment) (No. 2) Order, 2021
- SI 2020/2: National Assembly By-Election (Chilubi Constituency No. 095) (Election date and time of Poll) Order, 2020
- SI 2020/3: Electoral Process (Local Government By-Elections) (Election Date and Time of Poll) Order, 2020
- SI 2020/4: Electoral Process (Local Government By-Elections) (Election Date and Time of Poll) (No. 2) Order, 2020
- SI 2020/5: Urban and Regional Planning (Designated Local Planning Authority) Regulations, 2020
- SI 2020/7: Road Traffic (Speed Limits) Regulations, 2019
- SI 2020/8: Diplomatic Immunities and Privileges (Turkish Cooperation and Coordination Agency) Order, 2020
- SI 2020/9: Urban and Regional Planning (Designated Local Planning Authorities) Regulations, 2020
- SI 2020/13: National Forest No. F.12: Luano (Alteration of Boundaries) Order, 2020
- SI 2020/14: Local Government (Fire Services) Order, 2020
- SI 2020/21: Public Health (Notifiable Infectious Disease) (Declaration) Notice, 2020
- _(... and 22 more not shown)_

## Integrity

- discovery-only batch; no records written this tick
- no new amended_by / repealed_by / cited_authorities references introduced
- raw file written; sha256 computed and recorded in provenance.log

## Notes

- robots.txt: /legislation/subsidiary is Allow: / under zambialii.org robots; Crawl-delay: 5s honoured (single fetch).
- next tick: ingest 3-5 corporate candidates from this report (HTML AKN, PDF fallback if HTML <2 sections).
