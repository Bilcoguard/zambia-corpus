#!/usr/bin/env python3
"""Integrity checks for batch 0254 (CHECK1a-CHECK6).

corpus.sqlite is gitignored (rebuilt from raw files each session per
commit 4a2544c) so all checks operate on JSON records on disk and the
provenance.log audit trail. Stops with non-zero exit and a diagnostic
if any check fails. On pass, prints a JSON summary.
"""
import os, sys, json, hashlib, glob

BATCH_NUM = "0254"
PARSER_VERSION = "0.6.0-act-zambialii-2026-04-26"

PICK_IDS = [
    "act-zm-1926-020-clubs-registration-act-1926",
    "act-zm-1963-064-central-african-power-corporation-act-1963",
    "act-zm-1964-007-central-african-civil-air-transport-act-1964",
    "act-zm-1968-018-calculation-of-taxes-act-1968",
    "act-zm-1981-003-central-committee-act-1981",
]

REQUIRED_FIELDS = [
    "id", "type", "jurisdiction", "title", "in_force",
    "source_url", "source_hash", "fetched_at", "parser_version", "sections",
]


def find_record(rid):
    parts = rid.split("-")
    yr = parts[2]
    return f"records/acts/{yr}/{rid}.json"


def load_all_known_ids():
    ids = set()
    for p in glob.glob("records/**/*.json", recursive=True):
        try:
            with open(p) as f:
                rec = json.load(f)
            if "id" in rec:
                ids.add(rec["id"])
        except Exception:
            pass
    return ids


def main():
    failures = []
    records = []

    # CHECK1a: batch unique IDs
    if len(set(PICK_IDS)) != len(PICK_IDS):
        failures.append(("CHECK1a", "duplicate IDs in batch"))

    # Load each record
    for rid in PICK_IDS:
        p = find_record(rid)
        if not os.path.exists(p):
            failures.append(("CHECK0_load", f"{rid} record file missing: {p}"))
            continue
        with open(p) as f:
            rec = json.load(f)
        records.append(rec)

    all_ids = load_all_known_ids()
    # The batch records are now on disk so they're already in all_ids.
    # CHECK1b: every batch ID appears exactly once across the corpus.
    for rec in records:
        # count occurrences in records/ to ensure no duplicate file
        matches = glob.glob(f"records/**/{rec['id']}.json", recursive=True)
        if len(matches) != 1:
            failures.append(("CHECK1b", f"{rec['id']} occurs {len(matches)} times: {matches}"))

    # CHECK2: amended_by references resolve
    for rec in records:
        for ref in rec.get("amended_by") or []:
            if ref not in all_ids:
                failures.append(("CHECK2", f"amended_by {ref} unresolved in {rec['id']}"))

    # CHECK3: repealed_by reference resolves
    for rec in records:
        ref = rec.get("repealed_by")
        if ref and ref not in all_ids:
            failures.append(("CHECK3", f"repealed_by {ref} unresolved in {rec['id']}"))

    # CHECK4: source_hash matches raw HTML
    for rec in records:
        rid = rec["id"]
        parts = rid.split("-")
        yr = parts[2]; num = parts[3]
        raw = f"raw/zambialii/act/{yr}/{yr}-{num}.html"
        if not os.path.exists(raw):
            failures.append(("CHECK4", f"raw missing for {rid}: {raw}"))
            continue
        h = hashlib.sha256(open(raw, "rb").read()).hexdigest()
        expect = rec["source_hash"].split(":", 1)[-1]
        if h != expect:
            failures.append(("CHECK4", f"hash mismatch for {rid}: disk={h[:12]} json={expect[:12]}"))

    # CHECK5: required fields present and non-empty
    for rec in records:
        for fld in REQUIRED_FIELDS:
            if fld not in rec:
                failures.append(("CHECK5", f"missing {fld} in {rec['id']}"))
            elif rec[fld] in (None, "", []) and fld not in ("amended_by",):
                failures.append(("CHECK5", f"empty {fld} in {rec['id']}"))
        if rec.get("parser_version") != PARSER_VERSION:
            failures.append(("CHECK5_pv", f"parser_version mismatch in {rec['id']}: {rec.get('parser_version')}"))

    # CHECK6: cited_authorities resolve
    for rec in records:
        for ref in rec.get("cited_authorities") or []:
            if ref not in all_ids:
                failures.append(("CHECK6", f"cited_authorities {ref} unresolved in {rec['id']}"))

    if failures:
        os.makedirs("error-reports", exist_ok=True)
        from datetime import datetime, timezone
        ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        rpt = f"error-reports/{ts}-batch-{BATCH_NUM}.md"
        with open(rpt, "w") as f:
            f.write(f"# Batch {BATCH_NUM} integrity failures\n\n")
            for chk, msg in failures:
                f.write(f"- {chk}: {msg}\n")
        with open("gaps.md", "a") as f:
            f.write(f"\n## Batch {BATCH_NUM} integrity failure ({ts})\n")
            for chk, msg in failures:
                f.write(f"- {chk}: {msg}\n")
        print(json.dumps({"status": "FAIL", "failures": failures, "report": rpt}, indent=2))
        sys.exit(1)

    summary = {
        "status": "PASS",
        "ingested": [r["id"] for r in records],
        "section_counts": [len(r.get("sections") or []) for r in records],
    }
    os.makedirs("_work", exist_ok=True)
    with open(f"_work/batch_{BATCH_NUM}_integrity.json", "w") as f:
        json.dump(summary, f, indent=2)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
