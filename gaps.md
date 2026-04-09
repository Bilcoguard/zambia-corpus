# Gaps Log — Zambian Authorities Corpus

This file tracks known gaps, deferrals, and unresolved questions encountered
during corpus ingestion. Each entry is dated (UTC) and should describe what
is missing, why it could not be resolved at the time, and what would be
needed to close it.

## [2026-04-09] as-enacted Companies Act 2017 deferred

The pilot record for Companies Act No. 10 of 2017 ingested under Phase 2
will be sourced from ZambiaLII, which publishes the consolidated version
(amendments folded in). The as-enacted text from the authoritative
publisher (Parliament of Zambia) is still needed. Parliament URL structure
is unknown as of Phase 2 Checkpoint A (2026-04-09: /sitemap.xml returned
404, homepage not yet fetched). Deferred to a later phase or a dedicated
Parliament-resolution pass. When the as-enacted record lands, it should
be linked to the consolidated record via whatever "prior_version" or
"as_enacted_id" field the schema carries at that time (v0.3+).

## [2026-04-09] ZambiaLII closed — Phase 3 judgment source TBD

ZambiaLII is closed to KWLP corpus use per Phase 2 Checkpoint A policy
decision (Content-Signal ai-input=no + EU 2019/790 Art. 4 reservation).
Phase 3 (pilot judgment) therefore cannot use ZambiaLII. Candidate
alternative sources: (1) Judiciary of Zambia official site
(judiciary.gov.zm) direct judgment publication, (2) Government Gazette
where judgments are gazetted, (3) Parliament of Zambia if any judgments
are hosted there. All three require discovery work. Deferred to Phase 3
kickoff.
