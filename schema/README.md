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
`enacted_date`, `commencement_date`, `in_force`, `amended_by`, `repealed_by`,
`sections`, `paragraphs`, `court`, `case_number`, `parties`, `judges`,
`cited_authorities`.

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

## Worked example 1 — an Act

```json
{
  "id": "example-act-xxx-2099",
  "type": "act",
  "jurisdiction": "ZM",
  "title": "Example Placeholder Act, 2099",
  "citation": "Example Act No. 0 of 2099",
  "enacted_date": "2099-01-01",
  "commencement_date": "2099-01-15",
  "in_force": true,
  "amended_by": [],
  "repealed_by": null,
  "sections": [
    {
      "number": "1",
      "heading": "Short title",
      "text": "This Act may be cited as the Example Placeholder Act, 2099.",
      "subsections": []
    },
    {
      "number": "2",
      "heading": "Interpretation",
      "text": "In this Act, unless the context otherwise requires— ...",
      "subsections": [
        {
          "number": "2(1)",
          "heading": null,
          "text": "\"Minister\" means the Minister responsible for example matters;",
          "subsections": []
        }
      ]
    }
  ],
  "source_url": "https://example.invalid/acts/0-of-2099.pdf",
  "source_hash": "sha256:0000000000000000000000000000000000000000000000000000000000000000",
  "fetched_at": "2099-01-20T10:00:00Z",
  "parser_version": "0.1.0"
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
  "enacted_date": "2099-03-15",
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
- `enacted_date` is repurposed for the date of decision; this is intentional
  so that "when did this authority come into existence" has a single field
  across types.
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
