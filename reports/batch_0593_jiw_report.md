# Batch 0593 — Judgment Ingestion Worker

**Tick:** 2026-05-11 (jiw seventh worker-tick of UTC date)
**Time:** ~19:16Z
**Mode:** judgment-ingestion-worker
**Priority focus:** (b) Court of Appeal sweep — judiciaryzambia.com page 6
**Worker scope:** judgments only; does NOT touch approvals.yaml; does NOT run Phase 8 reverify; does NOT run repair-worker actions

## Tick verdict

**ok-partial-fts5-blocked-backlog-20**

- 14 fetches (1 listing + 7 post HTMLs + 7 PDFs; minus zero confirmed_404)
- 7 PDFs parsed via pdfplumber 0.11.9
- 6 records reached metadata extraction; 1 record deferred at quality-gate (scanned-PDF, needs ocrmypdf)
- **0 records inserted** — pre-existing FTS5 corruption persists for 15th consecutive jiw tick
- CHECK8 PASS by transaction rollback (`records=1892, records_fts=1892` unchanged)
- Cumulative today: 78/500 fetches (budget healthy)

## Sweep position

| field | before | after |
|---|---|---|
| judiciary-coa-sweep | page 6 | page 7 |

## Page-6 listing inventory (10 posts)

| # | post-id | slug-hint | status |
|---|---|---|---|
| 1 | 20731 | appeal-95-2024 lamasat | parsed-dirty (deferred-fts5 + v0.4 pending) |
| 2 | 20728 | caz-8-331-2024 jennifer-tembo-njovu | parsed-dirty (deferred-fts5 + v0.4 pending) |
| 3 | 20725 | app-176-2022 bright-jangazya | **parsed-clean** (deferred-fts5 only) |
| 4 | 20686 | app-170-2025 mukamunya-homeowners | parsed-dirty (deferred-fts5 + v0.4 pending) |
| 5 | 20683 | caz-09-127-2025 philemon-dyamini | parsed-dirty (deferred-fts5 + v0.4 pending) |
| 6 | 20680 | application-108-2024 pilatus-engineering | **SKIPPED** — already in corpus from b0591 |
| 7 | 20677 | sp-71-2024 charles-mpundu | parsed-dirty (deferred-fts5 + v0.4 pending) |
| 8 | 20674 | app-91-2024 fqm-trident | **SKIPPED** — known b0591 dedup-collision pending human review |
| 9 | 20671 | app-105-2023 nimble-resources | **SKIPPED** — URL-variant dedup-hit (different post-URL, same case in corpus b0591) |
| 10 | 20380 | app-309-2023 emergency-response | **deferred quality-gate-fail-scanned-pdf** (20 pages, 19 chars extracted; needs ocrmypdf) |

## Records by category

### Deferred — parsed-clean, fts5-blocker only (1)
- `judgment-zm-2025-coa-176-bright-jangazya-v-first-national-bank-zambia-limited`
  - case_number: APP/176/2022 (with CAZ/08/075/2022 secondary)
  - date_decided: 2025-12-31
  - outcome: dismissed (Operative paragraph: "all three grounds of Appeal are dismissed for want of merit")
  - panel: Kondolo SC / Makungu / Banda-Bobo JJA
  - issue_tags: banking-finance, contract, appellate-procedure

### Deferred — parsed-dirty (v0.4.0 parser improvements needed) (5)
- `judgment-zm-2025-coa-095-lamasat-international-limited-v-african-banking-corporation-zambia-limited` (single-judge chambers ruling, Chashi J)
- `judgment-zm-2025-coa-008-jennifer-tembo-njovu-v-administrator-general` (single-judge chambers ruling, Kondolo SC J)
- `judgment-zm-2025-coa-170-mukamunya-homeowners-association-v-leslie-szeftel` (full panel, **date_decided 2025-06-30 may be wrong**)
- `judgment-zm-2025-coa-009-philemon-dyamini-v-the-people` (single-judge chambers ruling, Mchenga DJP)
- `judgment-zm-2024-coa-071-charles-mpundu-v-food-reserve-agency` (full panel, **date_decided 2024-09-09 is hearing date — actual decision date later**)

### Deferred — scanned-PDF quality-gate-fail (1)
- emergency-response-zambia-v-betternow-finance (APP/309/2023, panel: Ngulube/Muzenga/Chembe JJA)
  - PDF 3.2 MB / 20 pages, pdfplumber extracted only 19 chars → scanned-image PDF
  - Action: needs `ocrmypdf` fallback (not in sandbox)

## Backlog tally (deferred-fts5 awaiting repair-worker FTS5 rebuild)

| tick | court | added | running total |
|---|---|---|---|
| b0590 | CoA | 7 | 7 |
| b0591 | CoA | 4 | 11 |
| b0592 | CoA | 3 | 14 |
| b0593 | CoA | 6 | **20** |

## FTS5 corruption — operator escalation REPEATED

### Status verified this tick (on /tmp isolated copy)
- `INSERT INTO records_fts(records_fts) VALUES('rebuild')` → **FAILED** (`database disk image is malformed`)
- `INSERT INTO records_fts(records_fts) VALUES('integrity-check')` → **FAILED**

### Repair worker status
- Most recent repair-batch-023 at 2026-05-11T18:11:02Z → `IDLE manifest=48/48-clean repaired=0 fetched=0`
- **13 consecutive idle ticks**
- The `fts5-rebuild-records-fts` task is NOT in the repair-worker manifest

### Remediation required (out of jiw scope per task spec)
The repair worker manifest needs:
```yaml
fts5-rebuild-records-fts:
  preconditions:
    - records.count > 0
    - INSERT('integrity-check') fails on records_fts
  action:
    - BACKUP corpus.sqlite to corpus.sqlite.bak.fts5-rebuild-<ts>
    - DROP TABLE records_fts
    - CREATE VIRTUAL TABLE records_fts USING fts5(
        id UNINDEXED, type UNINDEXED, title, citation, case_name, outcome_detail, body,
        tokenize='porter unicode61')
    - INSERT INTO records_fts(id, type, title, citation, case_name, outcome_detail, body)
        SELECT r.id, r.type, r.title, r.citation,
               (SELECT case_name FROM judgments_meta WHERE judgment_id=r.id),
               (SELECT outcome_detail FROM judgments_meta WHERE judgment_id=r.id),
               r.body
        FROM records r
    - INSERT INTO records_fts(records_fts) VALUES('integrity-check')
    - VERIFY records.count == records_fts.count
```

**JIW productivity will remain near-zero until this is unblocked.**

## v0.4.0 parser improvements flagged

1. **BETWEEN-block case_name extraction** — stop at first role keyword (APPLICANT/APPELLANT/RESPONDENT/CLAIMANT/PETITIONER) before any embedded date stamps
2. **Coram extraction defensive guard** — when `CORAM:` / `BEFORE:` anchor is ABSENT in PDF body, do NOT slurp the `For the Appellant:` counsel block
3. **Single-judge CoA chambers ruling pattern** — handle `Mr. Justice X` single-judge panel for chambers rulings (3 records this tick are chambers rulings)
4. **Outcome detection for chambers rulings** — add `I find / I order / we recommend / the application is granted/refused` anchors
5. **Date_decided for SP-prefix Special Procedure** — prefer `DELIVERED ON <date>` or court-date-stamp over hearing date (Charles Mpundu SP/71/2024)
6. **PDF-body OCR noise tolerance** — pre-strip `c6urt`/`ric`/`jic`/`iC OF iRT` cover-page artifacts
7. **Scanned-PDF ocrmypdf fallback** — when pdfplumber returns <200 chars and pages>=5 (Emergency Response Zambia, APP/309/2023)

## Integrity checks (CHECK1-CHECK8)

| check | result | notes |
|---|---|---|
| CHECK1 (judges non-empty) | N/A (no inserts) | parser produced judges for 5/6 fully-clean records; 5 have judges from URL-slug or PDF-body Coram |
| CHECK2 (issue_tags non-empty) | N/A (no inserts) | parser ensured non-empty via fallback `general-court-of-appeal` |
| CHECK3 (outcome enum) | partial | clean records: dismissed, allowed, granted; dirty records: outcome=other in 2 cases |
| CHECK4 (judges resolve) | N/A (no inserts) | judges_registry.yaml not modified this tick |
| CHECK5 (no dup IDs) | N/A (no inserts) | |
| CHECK6 (raw_sha256 matches on-disk) | PASS | all 7 PDFs hashed in /tmp/b0593/parsed_full.pkl matches raw/judiciary-zm/coa/*.pdf |
| CHECK7 (no dup case_name+court+date) | N/A (no inserts) | |
| **CHECK8 (records.count == records_fts.count)** | **PASS** | 1892 == 1892 via no-mutation rollback |

## Execution mode

- Inline runner via `/tmp/b0593/*.py`; no derivative script committed (sandbox-session safety constraint, per b0548..b0592 precedent)
- Corpus.sqlite NOT mutated this tick (no records inserted; transaction rolled back)
- User-Agent: `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)`
- Git ops: pull (already-up-to-date), commit (pending), push (pending)
- B2 sync: deferred to host (rclone not in sandbox)

## Continuation plan (b0594)

1. Continue priority-b: judiciaryzambia.com CoA page 7
2. Monitor repair-worker for `fts5-rebuild-records-fts` task adoption — if observed, backlog auto-drains
3. If FTS5 still blocked at b0594, consider parser-only-archival mode: parse page 7 with v0.3.9 fixes, archive to `_deferred/` without `INSERT` attempt, document parser-clean-vs-dirty split

