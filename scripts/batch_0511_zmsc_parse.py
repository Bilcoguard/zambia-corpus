#!/usr/bin/env python3
"""Batch 0511 ZMSC parser — judgment-ingestion-worker tick."""
import json
import os
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import batch_0506_zmsc_parse as p
import batch_0498_parse as v032
import batch_0360_parse as v031

ROOT = HERE.parent
RAW_DIR = ROOT / "raw" / "zambialii" / "judgments"
RECORDS_DIR = ROOT / "records" / "judgments"
WORK = ROOT / "_work" / "b0511"
WORK.mkdir(parents=True, exist_ok=True)

def main():
    targets_path = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else (WORK / "targets.json")
    targets = json.loads(targets_path.read_text())
    written = []
    deferred = []
    new_aliases = []

    for t in targets:
        court = t["court"]; year = int(t["year"]); num = int(t["num"])
        out_dir = RECORDS_DIR / court / str(year)
        out_dir.mkdir(parents=True, exist_ok=True)
        existing = list(out_dir.glob(f"judgment-zm-{year}-{court}-{num:02d}-*.json"))
        if existing:
            print(f"SKIP {court}/{year}/{num}: already in corpus ({existing[0].name})")
            continue
        raw_year_dir = RAW_DIR / court / str(year)
        html_files = list(raw_year_dir.glob(f"judgment-zm-{year}-{court}-{num:02d}-*.html"))
        pdf_files = list(raw_year_dir.glob(f"judgment-zm-{year}-{court}-{num:02d}-*.pdf"))
        if not html_files or not pdf_files:
            deferred.append({"court": court, "year": year, "num": num,
                             "reason": "raw_bytes_not_on_disk"})
            print(f"DEFER {court}/{year}/{num}: raw_bytes_not_on_disk")
            continue
        html_path = html_files[0]
        pdf_path = pdf_files[0]

        html_bytes = html_path.read_bytes()
        url_pat = re.compile(
            rf"/akn/zm/judgment/{re.escape(court)}/{year}/{num}/eng@(\d{{4}}-\d{{2}}-\d{{2}})".encode()
        )
        m = url_pat.search(html_bytes)
        dt = m.group(1).decode() if m else "0000-00-00"
        html_url = f"https://zambialii.org/akn/zm/judgment/{court}/{year}/{num}/eng@{dt}"
        pdf_url = html_url + "/source.pdf"

        record, debug = p.build_record_zmsc(court, year, num, html_path, pdf_path, html_url, pdf_url)
        if record is None:
            entry = {"court": court, "year": year, "num": num,
                     "html": str(html_path), "pdf": str(pdf_path),
                     "reason": debug.get("reason"),
                     "summary_head": debug.get("summary_head", "")[:300],
                     "html_url": html_url}
            deferred.append(entry)
            print(f"DEFER {court}/{year}/{num}: {debug.get('reason')}")
            continue

        for alias, title, j_clean in zip(debug["judges_raw"], debug["judges_titles"], record["judges"]):
            new_aliases.append((j_clean["name"], title, alias, record["id"]))

        out_path = out_dir / f"{record['id']}.json"
        out_path.write_text(json.dumps(record, indent=2, ensure_ascii=False) + "\n")
        written.append({"id": record["id"],
                        "citation": record["citation"],
                        "outcome": record["outcome"],
                        "date": record["date_decided"],
                        "case_name": record["case_name"],
                        "outcome_source": debug.get("outcome_source"),
                        "judges_raw": debug.get("judges_raw")})
        print(f"WRITE {record['id']} outcome={record['outcome']} via={debug['outcome_source']}")

    if new_aliases:
        v031.update_judges_registry(new_aliases)

    (WORK / "parse_results.json").write_text(json.dumps({
        "written": written,
        "deferred": deferred,
        "judges_added": [{"canonical": ca, "title": ti, "alias": al, "rec": r}
                         for (ca, ti, al, r) in new_aliases],
    }, indent=2, ensure_ascii=False))
    print(f"SUMMARY written={len(written)} deferred={len(deferred)} judges_added={len(new_aliases)}")

if __name__ == "__main__":
    main()
