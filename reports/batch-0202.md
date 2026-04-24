# Batch 0202 Report — Phase 4 sis_corporate continuation

- **Batch:** 0202
- **Phase:** 4 (Bulk ingestion)
- **Sub-phase:** sis_corporate
- **Started:** 2026-04-24T23:05:23Z
- **Completed:** 2026-04-24T23:11:12Z
- **Records written:** 6 / 6 targets attempted (within MAX_BATCH_SIZE = 8)
- **Fetches used (this batch):** 23 (see breakdown)
- **Cumulative today:** ~393 / 2000 (19.7%) — well within budget
- **Robots.txt re-verified:** sha256 prefix `fce67b697ee4ef44` (unchanged from
  batches 0193–0201; re-fetched 3 times this batch — first attempt, orphan
  recovery, and clean run — all matched)
- **Integrity checks:** all PASS (CHECK1 id uniqueness, CHECK2 cross-refs
  resolve, CHECK3 source_hash matches on-disk, CHECK4 required fields,
  CHECK5 robots.txt unchanged)
- **Gaps:** none

## Sandbox-bash execution note

The session bash sandbox uses `bwrap --unshare-pid`, so each bash invocation
has its own PID namespace and any backgrounded process is killed when the
parent bash exits. The 45 s per-call timeout therefore caps the work that
can be done in a single invocation: at the robots.txt-declared crawl-delay
of 5 s (we use 6 s as margin), one bash call covers ~7 fetches.

This batch was therefore split into three clean invocations:

| # | Phase                | Window (UTC)            | Fetches | Outcome                                        |
|---|----------------------|-------------------------|---------|------------------------------------------------|
| 1 | discovery + part-of-ingest | 23:05:23–23:05:58 | 7   | robots + 4 alphabets + 1 record (SI 2021/32) ingested before bash kill |
| – | orphan robots only   | 23:06:59                | 1       | second nohup attempt killed before discovery completed |
| 2 | discovery (re-run)   | 23:08:42–23:09:07       | 5       | robots + 4 alphabets — produces curated candidate set  |
| 3 | ingest slice 0_3     | ~23:10:09–23:10:37      | 6       | SI 2016/73, SI 2016/77, SI 2002/40            |
| 4 | ingest slice 3_5     | ~23:10:48–23:11:03      | 4       | SI 1988/33, SI 1986/29                        |
|   | **total**            |                         | **23**  | 6 records on disk + 1 orphan robots check     |

The 6 records and all 23 fetches are recorded in `provenance.log` and
`costs.log` with `batch=0202`. The orphan robots fetch is benign — it
re-confirmed robots.txt was unchanged at the moment, so the data is
consistent with the rest of the batch.

## Discovery

Live discovery probes (clean run):

- robots.txt re-verify (sha256 `fce67b697ee4ef44…`, unchanged)
- alphabet=B → 4 SI candidates, 2 novel post-HEAD
- alphabet=M → 24 SI candidates, several novel
- alphabet=P → 33 SI candidates, several novel
- alphabet=S → 17 SI candidates (also covered Securities Act 2016/41 territory)

Pre-keyword novel slot count (across the 4 alphabets, after subtracting HEAD):
59 candidates. Keyword filter retained 5; the curated next-step list dropped
two false positives — `1991/042 Preservation of Public Security (Income Tax
Act) (Suspension)` (matched on "secur" but is an emergency-era national-
security regulation, not financial securities) and `1984/002 Professional
Boxing and Wrestling Control (Insurance) Regulations` (matched "insurance"
but is sports-licensing rather than financial insurance). Two genuine
sis_corporate candidates that the plural-only `securities` keyword missed
were re-added by hand: `2016/073` and `2016/077` Movable Property (Security
Interest) Regulations — derivatives of the Movable Property (Security
Interest) Act 2016/3 / PACRA Act 2010/15 family.

## Targets ingested

| # | SI            | Sub-phase     | Sections | PDF bytes | Status |
|---|---------------|---------------|---------:|----------:|--------|
| 1 | SI 32 of 2021 | sis_corporate |       72 |       n/a | ok     |
| 2 | SI 73 of 2016 | sis_corporate |        9 |   106,603 | ok     |
| 3 | SI 77 of 2016 | sis_corporate |       47 |   303,143 | ok     |
| 4 | SI 40 of 2002 | sis_corporate |        2 |   914,073 | ok     |
| 5 | SI 33 of 1988 | sis_corporate |        – |         – | ok     |
| 6 | SI 29 of 1986 | sis_corporate |        – |         – | ok     |

(SI 2021/32 was processed during the aborted first-attempt window; the
exact pdf_bytes was not captured in the per-attempt slice file but the
record JSON, raw HTML and PDF, and provenance.log all match — its
`source_hash` was re-verified against the on-disk PDF in CHECK3.)

### Records

1. **SI 32 of 2021** — *Securities (Capital Markets Tribunal) Rules, 2021*
   - Parent: Securities Act, No. 41 of 2016
   - Source PDF: https://zambialii.org/akn/zm/act/si/2021/32/eng@2021-04-23/source.pdf
   - sha256: `f8cdd18b8193a76aabc462b…`

2. **SI 73 of 2016** — *Movable Property (Security Interest) (Fees) Regulations, 2016*
   - Parent: Movable Property (Security Interest) Act, No. 3 of 2016 (PACRA-administered)
   - Source PDF: https://zambialii.org/akn/zm/act/si/2016/73/eng@2016-10-28/source.pdf
   - sha256: `20c244388d5443f5976a4b8d829f98f287d617f6bea12c0af6471ab9f8a85e00`

3. **SI 77 of 2016** — *Movable Property (Security Interest) (General) Regulations, 2016*
   - Parent: Movable Property (Security Interest) Act, No. 3 of 2016
   - Source PDF: https://zambialii.org/akn/zm/act/si/2016/77/eng@2016-11-04/source.pdf
   - sha256: `53694a80bfe87082fc3af7dd140350cd9a19df72a696a2dd168b3b1a7542c489`

4. **SI 40 of 2002** — *Pension Fund (Annual Report) Regulations, 2002*
   - Parent: Pension Scheme Regulation Act, No. 28 of 1996
   - Source PDF: https://zambialii.org/akn/zm/act/si/2002/40/eng@2002-06-14/source.pdf
   - sha256: `5cd5e3d99d16320d136658cfe1122ee8720a3e846186204515eda9968c985986`

5. **SI 33 of 1988** — *The Building Societies (Authorised Investments) Order, 1988*
   - Parent: Building Societies Act, Cap. 412
   - Source PDF: https://zambialii.org/akn/zm/act/si/1988/33/eng@1988-02-12/source.pdf

6. **SI 29 of 1986** — *Bank of Zambia Act (Commencement) Order, 1986*
   - Parent: Bank of Zambia Act, 1985
   - Source PDF: https://zambialii.org/akn/zm/act/si/1986/29/eng@1986-02-14/source.pdf

## Integrity (CHECK1–CHECK5 + provenance audit)

- **CHECK1 (id uniqueness, batch + HEAD)** — PASS. 6 unique IDs; pre-write
  collision guards in `process_target` rejected any HEAD prefix clash.
- **CHECK2 (cross-refs)** — PASS. All `amended_by` empty, all `repealed_by`
  null, no `cited_authorities` field on SI records. Nothing to resolve.
- **CHECK3 (source_hash matches on-disk raw)** — PASS. All 6 PDFs re-hashed
  from `raw/zambialii/si/{year}/<stem>.pdf` and matched record `source_hash`.
- **CHECK4 (required fields)** — PASS. All of `id`, `type`, `jurisdiction`,
  `title`, `citation`, `sections`, `source_url`, `source_hash`, `fetched_at`,
  `parser_version` populated and non-empty.
- **CHECK5 (robots.txt drift)** — PASS. Re-fetched and confirmed sha256
  prefix `fce67b697ee4ef44` unchanged.
- **provenance.log audit** — 23 entries appended for batch=0202 (1 robots +
  4 alphabets + 2 ingest fetches in attempt 1, 1 robots in orphan, 1 robots
  + 4 alphabets + 10 ingest fetches in clean run = 23). All within crawl
  delay envelope. Reconciliation in `.batch_0202_state.json::fetches_breakdown`.

## Sub-phase running totals (post-batch)

- sis_corporate: +6 (Securities Tribunal Rules, 2× Movable Property Security
  Interest, Pension Fund Annual Report, Building Societies Authorised
  Investments, BoZ Act Commencement Order)
- sis_data_protection: unchanged (last touched batch-0201)
- sis_employment: unchanged (last touched batch-0200)
- sis_tax: unchanged (last touched batch-0199)
- sis_mining: unchanged (last touched batch-0194)
- sis_family: unchanged (last touched batch-0196)
- case_law_scz: paused per robots.txt Disallow on `/akn/zm/judgment/`
- acts_in_force: unchanged

Cumulative SI records on disk after this batch: 225 (+6 vs. batch-0201's 219).

## Next-tick plan

Yield this tick = 6 (≥ rotation threshold 3). Default rule says **continue
sis_corporate** next tick, with these probes:

- alphabet=I (already cached from batch-0196) for any Insurance Act / IPEC SIs
  not yet ingested
- alphabet=N for National Pension Scheme / National Payment Systems / NCCO
  derivatives
- alphabet=F for Financial Intelligence Centre derivatives (post-2022 there
  may be novel SIs not yet picked up; batch-0192 captured the 2016/2022 base
  Regulations)
- alphabet=A for Anti-Money Laundering / Anti-Terrorism / Co-operative
  Societies (Audit) Regulations
- Parent-Act probes: Banking and Financial Services Act 2017/7 derivatives
  (`/akn/zm/act/2017/7`), Pension Scheme Regulation Act, Building Societies
  Act, Money-Lenders Act
- Re-verify robots.txt (always at start)

Fallback if sis_corporate yield < 3:
- rotate to **sis_employment** (priority_order item 4) for the National
  Pension Scheme Authority worker-side derivatives, or
- rotate to **sis_data_protection** for IBA/Postal Services SIs probed via
  alphabet=B and alphabet=P (those parent-Act probes returned 0 SI links
  in batch-0201).

## Infrastructure follow-up (non-blocking)

- 12 batch-0202 raw files on disk (6 HTML + 6 PDF, ~1.7 MB) plus legacy
  files from batches 0192–0201 awaiting host-driven `rclone sync` to B2.
  Sandbox cannot run rclone (no B2 credentials in sandbox); logged
  "B2 sync deferred to host" for this tick (see `worker.log`).
- `corpus.sqlite` stale rollback-journal still blocks in-sandbox FTS
  rebuild — same condition as batches 0192–0201, unchanged this tick.
- 34 legacy-schema act JSON dupes under `records/acts/` + 42 Appropriation-
  Act `-000-` placeholder dupes + 63 SI records at top level of
  `records/sis/` (legacy flat layout) remain unresolved.
