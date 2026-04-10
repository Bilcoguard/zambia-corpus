#!/usr/bin/env python3
"""
B-POL-3 Step 3 — record build for the Konkola pilot judgment.

Reads parse.json (audit artefact), cherry-picks schema-valid fields,
writes records/judgments/judgment-zm-2026-scz-09-konkola-v-ag.json,
then validates against schema/record.schema.json using the jsonschema
Draft202012Validator.

Halts on validation failure (no silent amendment).
"""

import hashlib
import json
import sys
from pathlib import Path

import jsonschema
from jsonschema import Draft202012Validator

ROOT = Path("/sessions/magical-inspiring-hawking/mnt/corpus")
PARSE_PATH = ROOT / "raw/pilot/judiciary-zm/appeal-no-09-2024-konkola-copper-mins-plc-vs-attorney-general-2-others-mar-2026-coram-musonda-kaoma-and-mutuna-jjs/parse.json"
PARSE_EXPECTED_SHA256 = "544f3b125160214903715e7dfe9ce7bf93a8884a1eefcae71643fadc44dc4013"
PDF_EXPECTED_SHA256 = "2f790701cc6c882bd58881ad3e1b760a407d34a35b0231e2f70c45f81ceaa0ee"
SCHEMA_PATH = ROOT / "schema/record.schema.json"
RECORD_PATH = ROOT / "records/judgments/judgment-zm-2026-scz-09-konkola-v-ag.json"

PARSER_VERSION = "0.2.0"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    # ASSERT: parse.json integrity — this is the audit anchor
    parse_hash = sha256_file(PARSE_PATH)
    assert parse_hash == PARSE_EXPECTED_SHA256, (
        f"parse.json sha256 mismatch: expected {PARSE_EXPECTED_SHA256}, got {parse_hash}"
    )

    parse = json.loads(PARSE_PATH.read_text(encoding="utf-8"))

    # ASSERT: parse.json carries the expected PDF hash (propagation check)
    assert parse["source_metadata"]["sha256"] == PDF_EXPECTED_SHA256, (
        "parse.json source_metadata.sha256 does not match expected PDF hash"
    )

    # ------------------------------------------------------------------
    # rights_notice (per Ruling A5)
    # ------------------------------------------------------------------
    rights_notice = (
        "Publisher source page (judiciaryzambia.com) displays no copyright notice. "
        "Retention and re-use by Kate Weston Legal Practitioners is under the "
        "fair-dealing exceptions of the Copyright and Performance Rights Act, "
        "Cap. 406 of the Laws of Zambia, for the purposes of legal research and "
        "professional commentary. Judgments of the Supreme Court of Zambia are "
        "public acts of the state and are cited for their legal authority only."
    )

    # ------------------------------------------------------------------
    # notes block — combines (i) retrieval policy provenance,
    # (ii) OCR pipeline, (iii) four ruling-sourced sentences,
    # (iv) neutral-citation gap sentence
    # ------------------------------------------------------------------
    notes_lines = [
        "[Retrieval policy provenance]",
        (
            "Raw bytes retrieved from judiciaryzambia.com under the B-POL-2c "
            "revised content-length envelope (500 KB-50 MB band for Supreme "
            "Court PDFs on this publisher). Fetch authorised under the B-POL-2d "
            "fallback after candidate #06 (App-No-09-2024) failed the judgment "
            "heading gate as a ruling. The post HTML was retrieved first "
            "(raw/discovery/judiciary-zm/supreme-court/posts/post-01-konkola-appeal-09-2024.html, "
            "sha256 2b27bc3c10d195093ec3c1d2df8ed726b826248c87815924aafea15cac8623ef), "
            "the single embedded PDF URL extracted, then fetched via "
            "scripts/fetch_one.py (fetcher_version 0.2.0). The upstream "
            "Last-Modified header was Tue, 31 Mar 2026 13:38:18 GMT; the "
            "upstream ETag was \"69cbce4a-f5fa2b\". The natural-experiment "
            "pair (Appeal-No-09-2024 judgment vs App-No-09-2024 ruling, same "
            "parties, same panel, five months apart) confirmed the filename "
            "prefix as a reliable proceeding-class signal on this publisher.",
        )[0],
        "",
        "[OCR pipeline]",
        (
            "Source PDF carries no text layer. Full-document OCR was performed "
            "via pdftoppm 22.02.0 (poppler) through pdf2image at 200 DPI for "
            "the 33-page body, with the cover page separately re-rendered at "
            "300 DPI for close-read calibration, then processed through "
            "tesseract 4.1.1 via pytesseract 0.3.13 (eng). Raw OCR output was "
            "5,763 words / 33,739 characters. A calibrated cleanup set of ten "
            "substitutions was applied (anchored in the page-1 OCR excerpt and "
            "the publisher post title) to produce clean text of 5,761 words / "
            "33,735 characters. Paragraph structure (1-56) was recovered via "
            "a numbered-paragraph header regex. The full audit trail — "
            "including both applied and not-applied cleanup entries and the "
            "body text in both raw and clean forms — is held in the parse.json "
            "sibling file under raw/pilot/judiciary-zm/."
        ),
        "",
        "[Editorial rulings — date interpretation]",
        (
            "Coram line lists two sitting dates (4 February 2026 and 31 March "
            "2026). By Zambian Supreme Court convention the earlier is the "
            "hearing date and the later is the delivery date; the closing "
            "signature block carries no separate date stamp. Delivery date "
            "taken from the coram line."
        ),
        "",
        "[Editorial rulings — judicial designation]",
        (
            "Musonda DCJ also holds the designation State Counsel (SC) per "
            "the signature block; recorded in parse.json coram_struct, not in "
            "the record judges array."
        ),
        "",
        "[Editorial rulings — rights notice]",
        (
            "Publisher source page (judiciaryzambia.com) displays no copyright "
            "notice; publisher-asserted rights are silent, not absent. The "
            "rights_notice field records Kate Weston Legal Practitioners' own "
            "fair-dealing basis under Cap. 406, not a reproduction of any "
            "publisher notice."
        ),
        "",
        "[Editorial rulings — OCR garble not applied]",
        (
            "Five inferential OCR corrections were identified during parse but "
            "NOT applied to the clean text (see parse.json cleanup_log_not_applied). "
            "Raw OCR output is preserved in body_text_clean pending Phase 4 "
            "re-OCR at 300 DPI or human transcription."
        ),
        "",
        "[Neutral-citation gap]",
        (
            "The judgment as published carries a docket citation "
            "('APPEAL NO. 09/2024') but no neutral citation in the form "
            "'[YYYY] ZMSC NN' on the face of the document. No authoritative "
            "neutral-citation scheme was observable on the publisher source "
            "page. The record 'citation' field captures the docket citation "
            "verbatim in its normalised form ('Appeal No. 09 of 2024')."
        ),
    ]
    notes = "\n".join(notes_lines)

    # ------------------------------------------------------------------
    # Cherry-pick record fields (schema v0.4, additionalProperties: false)
    # ------------------------------------------------------------------
    record = {
        "id": "judgment-zm-2026-scz-09-konkola-v-ag",
        "type": "judgment",
        "jurisdiction": "ZM",
        "title": "Konkola Copper Mines PLC v Attorney General, Shenzen Resources Limited and Kakoso Metals Leach Limited",
        "citation": "Appeal No. 09 of 2024",
        "date_of_assent": "2026-03-31",
        "court": "Supreme Court of Zambia",
        "case_number": "Appeal No. 09 of 2024",
        "parties": {
            "appellant": ["Konkola Copper Mines PLC"],
            "respondent": [
                "Attorney General",
                "Shenzen Resources Limited",
                "Kakoso Metals Leach Limited",
            ],
        },
        "judges": ["Musonda DCJ", "Kaoma JS", "Mutuna JS"],
        "cited_authorities": [],
        "source_url": parse["source_metadata"]["url"],
        "source_hash": f"sha256:{PDF_EXPECTED_SHA256}",
        "fetched_at": parse["source_metadata"]["fetched_at"],
        "parser_version": PARSER_VERSION,
        "notes": notes,
        "rights_notice": rights_notice,
        "sensitive_data_categories": ["none"],
    }

    # ------------------------------------------------------------------
    # Write record
    # ------------------------------------------------------------------
    RECORD_PATH.parent.mkdir(parents=True, exist_ok=True)
    RECORD_PATH.write_text(
        json.dumps(record, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    # ------------------------------------------------------------------
    # Validate via Draft202012Validator
    # ------------------------------------------------------------------
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)  # meta-validate schema itself
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(record), key=lambda e: list(e.absolute_path))

    record_hash = sha256_file(RECORD_PATH)
    print(f"record path:  {RECORD_PATH}")
    print(f"record bytes: {RECORD_PATH.stat().st_size}")
    print(f"record sha256: {record_hash}")
    print(f"parse.json sha256 (audit anchor): {parse_hash}")
    print(f"jsonschema version: {jsonschema.__version__}")
    print(f"validator: Draft202012Validator")

    if errors:
        print(f"VALIDATION: FAIL ({len(errors)} errors)")
        for i, err in enumerate(errors, 1):
            path = "/".join(str(p) for p in err.absolute_path) or "(root)"
            print(f"  [{i}] path: {path}")
            print(f"      message: {err.message}")
            print(f"      validator: {err.validator}")
        return 2
    print("VALIDATION: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
