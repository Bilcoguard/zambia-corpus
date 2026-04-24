# Batch 0191 — sis_data_protection rotation

- Phase: phase_4_bulk / sub_phase: sis_data_protection (priority_order item 6)
- Started: 2026-04-24T17:34:57Z  Completed: 2026-04-24T17:36:37Z
- Records written: 8/8
- Fetches used: 16 (+4 discovery probes alphabet=D,C,E)

## Discovery

Rotation to sis_data_protection per batch-0190 next-tick plan. Discovery via ZambiaLII alphabet-indexed legislation listings:

- `/legislation/?alphabet=D` → 1 candidate (si/2021/58 Data Protection — already in HEAD).
- `/legislation/?alphabet=C` → 0 novel cyber candidates on page 1.
- `/legislation/?alphabet=E` → 1 novel (si/2023/43 Electronic Government).
- Cached `/legislation/?alphabet=I` (batch 0182 probe) → 7 novel ICT-domain candidates.

The sub-phase is interpreted broadly to cover Zambia's **digital/data-regulation corpus** — Data Protection Act 2021, Cyber Security and Cyber Crimes Act 2021, Electronic Communications and Transactions Act 2009, and the ICT Act 2009 — since these operate as a single compliance bundle for corporate clients advising on privacy, electronic transactions and telecommunications licensing.

## Records (8)

- **SI 2010/029** — Information and Communication Technologies (National Numbering Plan) Regulations, 2010 (38 sections). id=`si-zm-2010-029-information-and-communication-technologies-national-numbering-plan-regulations-2`.
- **SI 2010/035** — Information and Communication Technologies (Electronic Communications) (licensing) Regulations, 2010 (49 sections). id=`si-zm-2010-035-information-and-communication-technologies-electronic-communications-licensing-r`.
- **SI 2011/006** — Information and Communication Technologies (Type Approval) Regulations, 2010 (31 sections). id=`si-zm-2011-006-information-and-communication-technologies-type-approval-regulations-2010`.
- **SI 2013/015** — Information and Communication Technologies (General) Regulations, 2012 (1 sections). id=`si-zm-2013-015-information-and-communication-technologies-general-regulations-2012`.
- **SI 2015/080** — Information and Communications Technologies (Telecommunication Traffic Monitoring) Regulations, 2015 (29 sections). id=`si-zm-2015-080-information-and-communications-technologies-telecommunication-traffic-monitoring`.
- **SI 2017/048** — Information and Communication Technologies (Fees) Regulations, 2017 (8 sections). id=`si-zm-2017-048-information-and-communication-technologies-fees-regulations-2017`.
- **SI 2018/041** — Information and Communication Technologies (Tariffs) Regulations, 2018 (64 sections). id=`si-zm-2018-041-information-and-communication-technologies-tariffs-regulations-2018`.
- **SI 2023/043** — Electronic Government (General) Regulations, 2023 (8 sections). id=`si-zm-2023-043-electronic-government-general-regulations-2023`.

## Integrity (batch-scoped)

- CHECK1 unique IDs: PASS (8 novel IDs, no collision with HEAD).
- CHECK2 amended_by resolves: PASS (empty — primary SIs).
- CHECK3 repealed_by resolves: PASS (empty).
- CHECK4 cited_authorities resolves: PASS (not populated).
- CHECK5 source_hash matches on-disk raw: PASS (8/8 sha256 verified).

## Notes

- Per batch-0190 policy revert, raw html/pdf bytes are NOT committed this tick (raw/ .gitignore forbids; force-add policy withdrawn). 16 raw files on disk (~9.7 MB total) pending host-driven B2 sync: `rclone sync raw/ b2raw:kwlp-corpus-raw/`.
- Sandbox 45 s bash-tool ceiling respected: batch sliced into four 2-target invocations (0:2, 2:4, 4:6, 6:8) with `_work/batch_0191_summary.json` checkpoint resume.
- zambialii.org 5 s crawl-delay honoured throughout (6 s with 1 s margin).

## Next tick

Continue sis_data_protection with:

1. Cyber Security and Cyber Crimes Act 2021 subsidiary legislation — probe `/legislation/?q=cyber`, `/legislation/?alphabet=N` for NCCSAC successors, and Data Protection Act 2021 commencement orders.
2. Electronic Communications and Transactions Act 2009 SIs (ECT Act No. 21 of 2009) — includes cybercrime predecessor SIs.
3. ICT Act 2009 subsidiary legislation not yet ingested (Amendment regulations).

If sis_data_protection yield thins, rotate to sis_mining (priority_order item 7).
