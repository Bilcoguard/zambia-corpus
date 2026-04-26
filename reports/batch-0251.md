# Batch 0251 — Phase 4 (sis bulk)

Tick: pure cache-drain of 8 of 11 reserved alphabet=Z residuals from batch 0250.

## Yield

- Attempted: 8
- OK: 8 (after one substitution: idx=3 1990/39 ZNPF skipped pdf_too_large_4624989b — substituted with 1996/44 ZNPF Statutory Contributions from SUBS pool)
- Yield: 8/8 = 100%

## Records

- si-zm-1980-049-zambia-national-provident-fund-statutory-contributions-regulations-1980 — Zambia National Provident Fund (Statutory Contributions) Regulations, 1980 (parent_act: Zambia National Provident Fund Act; sub_phase: sis_governance; pages: 6; pdf_text_chars: 7244)
- si-zm-1981-047-zambia-national-service-obligatory-service-exemption-order-1981 — Zambia National Service (Obligatory Service) (Exemption) Order, 1981 (parent_act: Zambia National Service Act; sub_phase: sis_governance; pages: 2; pdf_text_chars: 1078)
- si-zm-1982-049-zambia-airways-corporation-date-of-dissolution-order-1982 — Zambia Airways Corporation (Date of Dissolution) Order, 1982 (parent_act: Zambia Airways Corporation Act; sub_phase: sis_industry; pages: 2; pdf_text_chars: 943)
- si-zm-1996-044-zambia-national-provident-fund-statutory-contributions-regulations-1996 — Zambia National Provident Fund (Statutory Contributions) Regulations, 1996 (parent_act: Zambia National Provident Fund Act; sub_phase: sis_governance; pages: 14; pdf_text_chars: 17090)
- si-zm-1994-049-zambia-revenue-authority-commencement-and-disengagement-order-1994 — Zambia Revenue Authority (Commencement and Disengagement) Order, 1994 (parent_act: Zambia Revenue Authority Act; sub_phase: sis_tax; pages: 2; pdf_text_chars: 1053)
- si-zm-2006-010-zambia-police-fees-regulations-2006 — Zambia Police (Fees) Regulations, 2006 (parent_act: Zambia Police Act; sub_phase: sis_governance; pages: 2; pdf_text_chars: 2336)
- si-zm-2016-040-zambia-wildlife-zambia-wildlife-police-uniforms-and-badges-regulations-2016 — Zambia Wildlife (Zambia Wildlife Police Uniforms and Badges) Regulations, 2016 (parent_act: Zambia Wildlife Act; sub_phase: sis_governance; pages: 6; pdf_text_chars: 6856)
- si-zm-2016-043-zambia-wildlife-export-prohibition-order-2016 — Zambia Wildlife (Export Prohibition) Order, 2016 (parent_act: Zambia Wildlife Act; sub_phase: sis_governance; pages: 2; pdf_text_chars: 1563)

## Discovery cost

- 1 robots.txt re-verify (sha256 prefix fce67b697ee4ef44 unchanged)
- 0 alphabet listing probes (pure cache-drain from batch 0250 reserved residuals)
- 16 record fetches (8 HTML + 8 PDF) plus 1 extra HTML+PDF for skipped 1990/39 = 18 + 1 substitute attempt (1 HTML + 1 PDF) = 20 record fetches total

## Integrity

- CHECK1a unique IDs: PASS (8/8)
- CHECK1b on-disk presence: PASS (8/8)
- CHECK2/3 amended_by/repealed_by zero refs: PASS
- CHECK4 source_hash sha256 verified vs raw PDF: PASS (8/8)
- CHECK5 required fields present: PASS
- CHECK6 cited_authorities zero refs: PASS

## Sub-phase footprint this tick

- sis_governance: +6 records (ZNPF 1980/49 + ZNS 1981/47 + ZNPF 1996/44 + Zambia Police 2006/10 + Zambia Wildlife 2016/40 + 2016/43)
- sis_industry: +1 record (Zambia Airways 1982/49 — FIRST parent-Act Zambia Airways Corporation Act)
- sis_tax: +1 record (Zambia Revenue Authority 1994/49 — FIRST parent-Act Zambia Revenue Authority Act)

## Reserved residuals carry to next tick

- 1991/35 Tender (Tender Board Act)
- 1998/43 Tender (Tender Board Act)
- 1990/39 ZNPF Statutory Contributions Regs (skipped — pdf_too_large_4624989b; needs OCR or split-page parsing)

## Next-tick plan

- Drain 2 remaining alphabet=Z reserved (1991/35 + 1998/43 Tender Board Act)
- Pivot to acts_in_force priority_order item 1 (Acts-listing endpoint discovery — separate path from SI ingest)
- OCR retry on backlog (15 items now: prior 14 + 1990/39 ZNPF)

## Infrastructure

- B2 raw sync deferred to host (rclone unavailable in sandbox)
- corpus.sqlite I/O error persists (rollback-journal — host-side rebuild required)
- 26-of-26 alphabet listings probed prior to this tick — alphabet exhaustion sub-phase complete
