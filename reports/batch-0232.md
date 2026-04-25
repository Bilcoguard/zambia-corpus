# Batch 0232 — Phase 4 Bulk SI Ingest

**Date:** 2026-04-25
**Tick start:** 2026-04-25T18:05:51Z (robots reverify)
**Wall-clock:** ~10 min
**Phase:** phase_4_bulk
**Strategy (per batch-0231 close-out plan, option a):** re-probe earlier alphabets M / A / D for residual modern (>=2017) candidates not picked previously.

## Discovery

| Alphabet | Total SIs | Modern (>=2017) | Novel (after dedup) |
|---|---|---|---|
| M | 24 | 10 | 0 (fully drained) |
| A | 20 | 12 | 10 |
| D | 11 | 6 | 5 |
| **Total** | **55** | **28** | **15** |

Discovery cost: 1 robots reverify + 3 alphabet probes (M/A/D) = 4 discovery fetches.

## Picks (8 — MAX_BATCH_SIZE cap)

| # | Year/No. | Title (truncated) | Sub-phase | Parent Act |
|---|---|---|---|---|
| 0 | 2018/22  | Animal Health (Veterinary Services Fees) Regs                       | sis_agriculture          | Animal Health Act |
| 1 | 2018/54  | Agricultural Institute of Zambia (General) Regs                     | sis_agriculture          | Agricultural Institute of Zambia Act |
| 2 | 2019/6   | Disaster Management (Qualifications of National Coordinator) Regs   | sis_disaster_management† | Disaster Management Act |
| 3 | 2019/31  | Defence (Regular Forces) (Officers) (Amendment) Regs                | sis_defence              | Defence Act |
| 4 | 2019/81  | Animal Health (Notifiable Diseases) Regs                            | sis_agriculture          | Animal Health Act |
| 5 | 2021/15  | Diplomatic Immunities and Privileges (ICTA) Order                   | sis_foreign_affairs†     | Diplomatic Immunities and Privileges Act |
| 6 | 2021/58  | Data Protection (Registration and Licensing) Regs                   | sis_data_protection†‡    | Data Protection Act |
| 7 | 2022/70  | Defence Force (UN Peacekeeping Operations) (Emoluments) Regs        | sis_defence              | Defence Act |

† First-instance sub-phase in this corpus.
‡ priority_order item 6 in approvals.yaml `phase_4_bulk.priority_order`.

## Yield

- ok: 8 / 8 = **100%** (ninth consecutive 100%-yield batch; streak: 0223/0224/0226/0227/0228/0229/0230/0231/0232; 0225 was 73% due to scanned-image cohort)
- 0 fail, 0 skip
- 0% scanned-image rate

## Per-record stats

| idx | yr/num | pages | text chars |
|---|---|---|---|
| 0 | 2018/22 | 4 | 5,258 |
| 1 | 2018/54 | 20 | 23,556 |
| 2 | 2019/6 | 1 | 1,041 |
| 3 | 2019/31 | 2 | 2,166 |
| 4 | 2019/81 | 2 | 2,476 |
| 5 | 2021/15 | 6 | 10,647 |
| 6 | 2021/58 | 30 | 33,304 |
| 7 | 2022/70 | 2 | 1,835 |

Substantive: 2021/58 (Data Protection Registration & Licensing — 30pp/33.3K chars, the foundational implementing regulation under the 2021 Data Protection Act); 2018/54 (Agricultural Institute of Zambia General Regs — 20pp/23.6K chars).

## Integrity

- CHECK1a (batch unique IDs): 8/8 PASS
- CHECK1b (corpus presence on disk): 8/8 PASS
- CHECK2/3 (amended_by/repealed_by refs resolve): 0 refs PASS
- CHECK4 (source_hash sha256 verified against raw/zambialii/si/<yr>/): 8/8 PASS
- CHECK5 (10 required fields x 8 records): all present PASS
- CHECK6 (cited_authorities resolve): 0 refs PASS

**Result: PASS**

## Fetches

- Robots reverify: 1
- Alphabet probes (M/A/D): 3
- Per-record (HTML+PDF, all fresh): 16
- Total this batch: ~20
- Today total: 552 / 2000 (27.6%) — within budget
- Tokens: within budget

## Sub-phase footprint after batch 0232

3 first-instance sub-phases this tick:
- **sis_data_protection** (1) — first time in corpus; priority_order item 6 of phase_4_bulk
- **sis_disaster_management** (1) — first time in corpus
- **sis_foreign_affairs** (1) — first time in corpus

Plus continued growth in:
- sis_agriculture (+3)
- sis_defence (+2)

## Next-tick plan

(a) Continue alphabet re-probes — E / G / H / K / L / P (haven't been re-probed since earlier ticks; likely-fertile based on M/A/D experience: 15 novel candidates from 3 alphabets = 5/alphabet expected yield)
(b) Rotate to acts_in_force (priority_order item 1) — requires Acts-listing endpoint discovery (separate path from SI ingest)
(c) OCR backlog from batches 0225/0226 (5 items)
(d) Records reconciliation tick (488+ pre-existing untracked records files)

## Infrastructure notes

- corpus.sqlite stale rollback-journal still blocks in-sandbox FTS rebuild (insert error: 'disk I/O error' — JSON records authoritative; sqlite rebuild deferred to host)
- persistent virtiofs unlink-failure warnings non-fatal (workaround stable across batches 0192-0232 — write-tree/commit-tree path bypasses lock)
- 488+ pre-existing untracked records/sis + records/acts files on disk (not in HEAD) unchanged this tick
- B2 sync deferred to host (rclone unavailable in sandbox); raw files (HTML+PDF) preserved on disk for host-side `rclone sync raw/ b2raw:kwlp-corpus-raw/`
