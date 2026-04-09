# Zambian Authorities Corpus — Record Schema

This folder defines the JSON Schema used by every record in the Kate Weston
Legal Practitioners Zambian Authorities Corpus.

The canonical schema is **`record.schema.json`** (JSON Schema draft 2020-12).
A record only enters the corpus if it validates against that schema. The
worker's pre-commit integrity checks (non-negotiable rule #7) MUST run schema
validation; commits with non-validating records are halted.

> **All examples in this document are illustrative.** Their `id` values begin
> with `example-` so they cannot be confused with real corpus entries. Do not
> cite them. Do not import them. They exist only to show the shape of a
> record.

## Why this schema exists

Every legal statement Kate Weston AI tooling produces must be grounded in a
verifiable primary source. To make grounding mechanical (and re-verifiable
nightly under Phase 7), every record carries:

- **`source_url`** — the exact URL on the authoritative host the bytes came
  from.
- **`source_hash`** — sha256 of the raw bytes, prefixed `sha256:`. If a
  re-fetch yields a different hash the record is flagged as drift.
- **`fetched_at`** — UTC timestamp of the fetch, ISO 8601 with `Z` suffix.
- **`parser_version`** — semver of the parser. Bumped on any parsing-logic
  change so re-parses are reproducible.

If any of those four fields is missing, the record is invalid by definition.

## Required vs optional fields

**Required for every record:**
`id`, `type`, `jurisdiction`, `title`, `citation`, `source_url`,
`source_hash`, `fetched_at`, `parser_version`.

**Optional but defined:**
`date_of_assent`, `commencement_date`, `in_force`, `version_type`,
`consolidated_as_of`, `amended_by`, `repealed_by`, `sections`, `paragraphs`,
`court`, `case_number`, `parties`, `judges`, `cited_authorities`, `notes`.

**Conditional:**
- Records of type `judgment` MUST include `court` and `case_number`.
- Records of type `act`, `si`, `constitution`, or `regulation` MUST include a
  `sections` array (it may be empty only if a stub is explicitly logged in
  `gaps.md`).

## Field rules worth knowing

- **`id`** — lowercase, hyphen-separated, must be unique across the corpus.
  No leading/trailing hyphens. The Phase 7 integrity check rejects duplicates.
- **`jurisdiction`** — fixed at `"ZM"`. Other jurisdictions go in other
  corpora.
- **`type`** — one of `act`, `si`, `judgment`, `constitution`, `regulation`,
  `guideline`, `directive`, `gazette_notice`. The enum is closed; adding a
  new type requires a schema bump and human approval.
- **`source_hash`** — must match `^sha256:[a-f0-9]{64}$`. Lowercase hex only.
- **`fetched_at`** — must match `^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$`. No
  fractional seconds. No offset other than `Z`.
- **`amended_by` / `repealed_by` / `cited_authorities`** — every ID must
  resolve to another record in the corpus. The pre-commit integrity check
  refuses to commit unresolved references.
- **`sections`** — verbatim text. No paraphrasing. Subsections nest
  recursively under the same shape.
- **`parser_version`** — semver. Bump on any parsing change, even if the
  output happens to be byte-identical.

### `version_type` and `consolidated_as_of` (v0.2)

For statutory instruments — `act`, `si`, `constitution`, `regulation` —
the corpus distinguishes between three textually distinct artefacts that
all share a single official title:

- **`as_enacted`** — the text exactly as published when the instrument
  was first enacted. Sourced from the authoritative publisher (Parliament
  of Zambia / Government Printer / Government Gazette).
- **`consolidated`** — a later compilation that folds in subsequent
  amendments up to a stated cut-off date. Sourced from compilers such as
  ZambiaLII or the Ministry of Justice Laws of Zambia.
- **`amendment`** — a standalone amending instrument that exists in its
  own right (e.g. "The Companies (Amendment) Act, 2022").

The `version_type` field captures which artefact a record represents.
The enum is `[null, "as_enacted", "consolidated", "amendment", "unknown"]`.
Null is permitted for records where the distinction does not apply
(judgments, gazette notices) or is genuinely unknown at ingest time.
`unknown` should be used sparingly and reviewed in `gaps.md`.

If `version_type` is `consolidated`, the record MUST also carry
`consolidated_as_of` — the ISO 8601 calendar date up to which amendments
are incorporated. The schema enforces this with a conditional rule.

**Source preference rule.** Where both as-enacted and consolidated
versions exist, the as-enacted text from the authoritative publisher is
canonically preferred for citation. Consolidated versions are useful for
research but should always be cross-referenced to the as-enacted record.

**Known v0.2 gap (deferred to v0.3).** There is currently no explicit
back-link field on a consolidated record pointing at its corresponding
as-enacted record (or vice versa). For now, the relationship is tracked
implicitly via shared `title` and `citation` and noted in `gaps.md`.
v0.3 will add a `prior_version` / `as_enacted_id` field once we have
ingested at least one as-enacted record from Parliament and know what
the link target should look like in practice.

## v0.3 changelog

v0.3 is an additive bump driven by the Phase 2 pilot ingest of the
Companies Act, 2017 (Act No. 10 of 2017). Building a real record
against v0.2 surfaced four shape mismatches that would have forced us
to drop genuine, source-attestable provenance to fit the schema. Per
non-negotiable rule #1 (no fabrication), the right move is to widen
the schema rather than coerce the record. The changes are strictly
additive — every v0.2-conformant record remains v0.3-conformant after
the field renames are applied.

1. **`x-corpus-schema-version`** bumped `0.2` → `0.3`.

2. **`enacted_date` → `date_of_assent`** (top level). Zambian
   constitutional practice distinguishes three textually distinct
   dates: enactment (Parliament passes the Bill), assent (the
   President signs), and commencement (an SI is published appointing
   the operative date). The Government Printer copies stamp "Date of
   Assent" on the cover page; that is what we record. Conflating any
   two of these into a single `enacted_date` field invites
   fabrication. The rename makes the field's meaning unambiguous and
   the new description spells out the distinction.

3. **`notes`** (top level, nullable string). Pilot records carry
   genuinely useful provenance that does not fit the structured
   fields: source typo annotations preserved verbatim, pilot-record
   qualifications, commencement-SI deferrals, bound-volume vs PDF page
   discrepancies, and observed-but-not-source-asserted amendment
   chains. The schema explicitly notes that anything written in
   `notes` MUST be source-attestable in the same way as the rest of
   the record — `notes` is provenance overflow, not editorial colour.

4. **`sections` items widened** from
   `{number, heading, text, subsections}` to
   `{number, title, part, part_title, page_start, body, subsections}`
   with `additionalProperties: false` retained.
   - `heading` → `title` (Zambian and Commonwealth statutory drafting
     conventions both call this the section title; "heading" is the
     Part heading, not the section's marginal note).
   - `text` → `body`, **now nullable**. Skeleton parses (Phase 2
     pilot, Phase 4 bulk first pass) carry null bodies and populate
     them in later phases. A null body is not a missing body — it is
     a deliberate "not yet parsed" marker.
   - **`part`** (nullable string) — the Roman numeral of the
     containing Part (e.g. `"I"`, `"XVII"`), or `null` if the
     instrument is not divided into Parts.
   - **`part_title`** (nullable string) — the verbatim Part heading,
     source typos preserved (e.g. `"PRELIMINARY PROVISONS"` — sic).
   - **`page_start`** (nullable positive integer) — 1-indexed PDF
     page where the section begins in the source PDF. Null only when
     a skeleton entry failed cross-reference and is logged in
     `gaps.md`.

`in_force` was already declared `["boolean", "null"]` in v0.2; no
change was required for the pilot's "commencement SI not yet
discovered → in_force unknown → in_force: null" pattern.

The conditional `allOf` rules are unchanged: judgments still require
`court` and `case_number`; statutory instruments still require a
`sections` array; consolidated records still require
`consolidated_as_of`.

## Worked example 1 — an Act

```json
{
  "id": "example-act-xxx-2099",
  "type": "act",
  "jurisdiction": "ZM",
  "title": "Example Placeholder Act, 2099",
  "citation": "Example Act No. 0 of 2099",
  "date_of_assent": "2099-01-01",
  "commencement_date": "2099-01-15",
  "in_force": true,
  "version_type": "as_enacted",
  "consolidated_as_of": null,
  "amended_by": [],
  "repealed_by": null,
  "sections": [
    {
      "number": "1",
      "title": "Short title",
      "part": "I",
      "part_title": "PRELIMINARY PROVISIONS",
      "page_start": 13,
      "body": "This Act may be cited as the Example Placeholder Act, 2099.",
      "subsections": []
    },
    {
      "number": "2",
      "title": "Interpretation",
      "part": "I",
      "part_title": "PRELIMINARY PROVISIONS",
      "page_start": 14,
      "body": "In this Act, unless the context otherwise requires— ...",
      "subsections": [
        {
          "number": "2(1)",
          "title": "Minister",
          "part": "I",
          "part_title": "PRELIMINARY PROVISIONS",
          "page_start": 14,
          "body": "\"Minister\" means the Minister responsible for example matters;",
          "subsections": []
        }
      ]
    }
  ],
  "source_url": "https://example.invalid/acts/0-of-2099.pdf",
  "source_hash": "sha256:0000000000000000000000000000000000000000000000000000000000000000",
  "fetched_at": "2099-01-20T10:00:00Z",
  "parser_version": "0.1.0",
  "notes": "Illustrative example only — not a real Act. Demonstrates the v0.3 record shape including date_of_assent, sections with part/part_title/page_start, and the notes field itself."
}
```

Notes on this example:
- `id` starts with `example-` and uses `xxx-2099` so it can never collide
  with a real Act. `source_url` uses the reserved `.invalid` TLD.
- `source_hash` is all zeros — a real record would carry the actual sha256
  of the fetched PDF bytes.
- `sections` is non-empty because Acts are required to carry sections.
- `parties`, `judges`, `court`, `case_number`, `paragraphs` are absent
  (judgment-only fields).

## Worked example 2 — a judgment

```json
{
  "id": "example-judgment-xxx-2099",
  "type": "judgment",
  "jurisdiction": "ZM",
  "title": "Example Placeholder v Another Example Placeholder",
  "citation": "[2099] EXAMPLE-ZMSC 0",
  "date_of_assent": "2099-03-15",
  "commencement_date": null,
  "in_force": null,
  "amended_by": [],
  "repealed_by": null,
  "court": "Supreme Court of Zambia",
  "case_number": "EXAMPLE-SCZ/00/2099",
  "parties": {
    "appellant": ["Example Placeholder"],
    "respondent": ["Another Example Placeholder"],
    "applicant": [],
    "plaintiff": [],
    "defendant": []
  },
  "judges": [
    "Example J (placeholder)",
    "Example JA (placeholder)",
    "Example JS (placeholder)"
  ],
  "paragraphs": [
    {
      "number": "1",
      "text": "This is a placeholder paragraph used solely to demonstrate the schema shape. It is not a real judgment."
    },
    {
      "number": "2",
      "text": "A second placeholder paragraph follows, also for illustration only."
    }
  ],
  "cited_authorities": [
    "example-act-xxx-2099"
  ],
  "source_url": "https://example.invalid/judgments/example-scz-0-2099.pdf",
  "source_hash": "sha256:1111111111111111111111111111111111111111111111111111111111111111",
  "fetched_at": "2099-03-20T09:30:00Z",
  "parser_version": "0.1.0"
}
```

Notes on this example:
- `type: "judgment"` triggers the conditional requirement that `court` and
  `case_number` be present.
- `date_of_assent` is repurposed for the date of decision; the schema
  description explicitly notes that for non-Acts the field captures the
  date the instrument was issued or decided, so that "when did this
  authority come into existence" has a single field across types.
- `cited_authorities` references `example-act-xxx-2099` from the previous
  example. In a real corpus, the integrity check would resolve that ID to a
  real Act record. Here, both records are placeholders, so they only resolve
  to each other in this README.
- `sections` is absent (judgments use `paragraphs`, not `sections`).
- The judge names are explicitly suffixed `(placeholder)` so they cannot be
  mistaken for real judges.

## How a record is validated

Pre-commit, the worker runs (at minimum):

1. `json.load` on every record file.
2. JSON Schema validation against `record.schema.json`.
3. Uniqueness check on `id`.
4. Resolution check on `amended_by`, `repealed_by`, `cited_authorities`.
5. Re-hash check: `sha256(open(raw_file).read()) == record["source_hash"]`.

If any check fails, the worker halts, writes to `worker.log`, and refuses to
commit. This is non-negotiable rule #7.

## Schema versioning

The schema itself is unversioned for now (Phase 1). When the first
backwards-incompatible change happens, we will add a `schema_version` field
to each record and bump it. Until then, every record is implicitly
`schema_version: "0.1"`.
