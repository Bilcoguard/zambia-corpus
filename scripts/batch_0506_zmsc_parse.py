#!/usr/bin/env python3
"""Batch 0506 ZMSC parser — judgment-ingestion-worker tick.

Adapts parser_v0.3.2 (scripts/batch_0498_parse.py) to ZMSC (Supreme
Court of Zambia) judgments. The HTML structure on ZambiaLII is
identical to ZMCC (same dl/dt/dd metadata block, h1 title, optional
Summary dd with flynote). Only the court label and citation suffix
differ.

This wrapper imports the v0.3.2 parser module and calls its
`infer_outcome_v032` and `parse_judges_v032` functions on a ZMSC-
specific build_record path.
"""

import hashlib
import json
import os
import pathlib
import re
import sys
from datetime import datetime, timezone

import yaml
from bs4 import BeautifulSoup

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
import batch_0498_parse as v032  # noqa: E402
import batch_0360_parse as v031  # noqa: E402

PARSER_VERSION = "0.3.2"
RAW_DIR = ROOT / "raw" / "zambialii" / "judgments"
RECORDS_DIR = ROOT / "records" / "judgments"
WORK = ROOT / "_work" / "b0504"
WORK.mkdir(parents=True, exist_ok=True)
JUDGES_REG = ROOT / "judges_registry.yaml"
TARGETS_JSON = WORK / "targets.json"

# Reuse helpers
sha_bytes = v031.sha_bytes
slugify = v031.slugify
now_iso = v031.now_iso
extract_pdf_text = v031.extract_pdf_text
update_judges_registry = v031.update_judges_registry
parse_judges_v032 = v032.parse_judges_v032
infer_outcome_v032 = v032.infer_outcome_v032


def build_record_zmsc(court_code, year, num, html_path, pdf_path, html_url, pdf_url):
    """Build a Phase 5-schema judgment record for a ZMSC ruling."""
    html_bytes = html_path.read_bytes()
    pdf_bytes = pdf_path.read_bytes()
    soup = BeautifulSoup(html_bytes.decode("utf-8", "ignore"), "html.parser")

    meta = {}
    summary_dd = None
    for dl in soup.find_all("dl"):
        items = dl.find_all(["dt", "dd"])
        for i in range(0, len(items) - 1, 2):
            if items[i].name == "dt" and items[i + 1].name == "dd":
                k = items[i].get_text(" ", strip=True)
                v = items[i + 1].get_text(" ", strip=True)
                if v.endswith(" Copy"):
                    v = v[:-5].strip()
                meta[k] = v
                if k == "Summary":
                    summary_dd = items[i + 1]

    h1 = soup.find("h1")
    title = h1.get_text(" ", strip=True) if h1 else ""
    citation = meta.get("Media Neutral Citation", "") or f"[{year}] ZMSC {num}"
    case_number = meta.get("Case number", "")
    court_full = "Supreme Court of Zambia"
    judges_text = meta.get("Judges", "")
    judgment_date = meta.get("Judgment date", "")

    date_decided = None
    m = re.match(r"^(\d{1,2})\s+([A-Za-z]+)\s+(\d{4})$", judgment_date)
    if m:
        d, mo, y = m.groups()
        months = "January February March April May June July August September October November December".split()
        try:
            mn = months.index(mo) + 1
            date_decided = f"{y}-{mn:02d}-{int(d):02d}"
        except ValueError:
            pass

    summary_para = ""
    flynote_text = ""
    if summary_dd:
        divs = [d for d in summary_dd.find_all("div", recursive=True) if d.get_text(" ", strip=True)]
        if divs:
            summary_para = divs[0].get_text(" ", strip=True)
        full_text = summary_dd.get_text("\n", strip=True)
        if "Flynote" in full_text:
            tail = full_text.split("Flynote", 1)[1]
            tail = tail.split("Read full summary", 1)[0]
            flynote_text = tail.strip()

    issue_tags = []
    if flynote_text:
        parts = re.split(r"\s+[–—\-]\s+", flynote_text)
        issue_tags = [p.strip() for p in parts if p and len(p.strip()) > 1]

    pdf_text, pdf_tail_text = extract_pdf_text(pdf_path)
    if pdf_text is None and pdf_tail_text is None:
        return None, {"reason": "pdf_extraction_empty_likely_scanned",
                      "summary_head": (summary_para or "")[:300]}
    if pdf_text and len(pdf_text.strip()) < 200:
        return None, {"reason": "pdf_extraction_empty_likely_scanned",
                      "summary_head": (summary_para or "")[:300]}

    outcome, outcome_detail, src = infer_outcome_v032(summary_para, pdf_text, pdf_tail_text)
    if outcome is None:
        return None, {"reason": "html_no_summary_pdf_no_match",
                      "summary_head": (summary_para or "")[:300]}
    if not outcome_detail:
        return None, {"reason": "outcome_inferred_but_detail_unsafe",
                      "src": src,
                      "summary_head": (summary_para or "")[:300]}

    cn = title
    cn = re.sub(r"\s*\([^)]*\)\s*\[[^\]]*\][^()]*\([^)]*\)\s*$", "", cn).strip()
    cn = re.sub(r"\s*\([^)]*\)\s*$", "", cn).strip()
    cn = re.sub(r"\s*\[[^\]]*\]\s*ZMSC.*$", "", cn).strip()

    judges = parse_judges_v032(judges_text)
    if not judges:
        return None, {"reason": "parser_v0.3.2_token_unhandled",
                      "judges_text": judges_text}
    judges_clean = [{k: v for k, v in j.items() if not k.startswith("_")} for j in judges]

    slug = slugify(cn, 50)
    rec_id = f"judgment-zm-{year}-{court_code}-{num:02d}-{slug}"

    record = {
        "id": rec_id,
        "type": "judgment",
        "jurisdiction": "ZM",
        "title": title,
        "citation": citation,
        "court": court_full,
        "case_name": cn,
        "case_number": case_number,
        "date_decided": date_decided,
        "judges": judges_clean,
        "issue_tags": issue_tags or [cn[:80]],
        "outcome": outcome,
        "outcome_detail": outcome_detail,
        "reasoning_tags": [],
        "key_statutes": [],
        "raw_sha256": sha_bytes(pdf_bytes),
        "source_url": html_url,
        "source_hash": "sha256:" + sha_bytes(html_bytes),
        "fetched_at": now_iso(),
        "parser_version": PARSER_VERSION,
    }
    debug = {
        "outcome_source": src,
        "summary_para": summary_para[:500],
        "judges_raw": [j["_alias"] for j in judges],
        "judges_titles": [j["_title"] for j in judges],
    }
    return record, debug


def load_targets():
    raw = json.loads(TARGETS_JSON.read_text())
    return [(t["court"], int(t["year"]), int(t["num"]), t.get("date_decided")) for t in raw]


def main():
    targets = load_targets()
    written = []
    deferred = []
    new_aliases = []

    for (court, year, num, dt) in targets:
        out_dir = RECORDS_DIR / court / str(year)
        out_dir.mkdir(parents=True, exist_ok=True)
        existing = list(out_dir.glob(f"judgment-zm-{year}-{court}-{num:02d}-*.json"))
        if existing:
            print(f"SKIP {court}/{year}/{num}: already in corpus")
            continue
        raw_year_dir = RAW_DIR / court / str(year)
        html_files = list(raw_year_dir.glob(f"judgment-zm-{year}-{court}-{num:02d}-*.html"))
        pdf_files = list(raw_year_dir.glob(f"judgment-zm-{year}-{court}-{num:02d}-*.pdf"))
        if not html_files or not pdf_files:
            deferred.append({"court": court, "year": year, "num": num,
                             "reason": "raw_bytes_not_on_disk"})
            continue
        html_path = html_files[0]
        pdf_path = pdf_files[0]

        if not dt:
            html_bytes = html_path.read_bytes()
            url_pat = re.compile(
                rf"/akn/zm/judgment/{re.escape(court)}/{year}/{num}/eng@(\d{{4}}-\d{{2}}-\d{{2}})".encode()
            )
            mm = url_pat.search(html_bytes)
            if mm:
                dt = mm.group(1).decode("utf-8", "ignore")
            else:
                mm = re.search(rb"eng@(\d{4}-\d{2}-\d{2})", html_bytes)
                if mm:
                    dt = mm.group(1).decode("utf-8", "ignore")
        if not dt:
            deferred.append({"court": court, "year": year, "num": num,
                             "reason": "canonical_url_date_unrecoverable"})
            continue

        html_url = f"https://zambialii.org/akn/zm/judgment/{court}/{year}/{num}/eng@{dt}"
        pdf_url = html_url + "/source.pdf"

        try:
            record, debug = build_record_zmsc(court, year, num, html_path, pdf_path, html_url, pdf_url)
        except Exception as e:
            deferred.append({"court": court, "year": year, "num": num,
                             "reason": f"parser_exception: {type(e).__name__}: {str(e)[:200]}"})
            continue

        if record is None:
            deferred.append({"court": court, "year": year, "num": num,
                             "reason": debug.get("reason"),
                             "summary": (debug.get("summary_head") or debug.get("summary_para") or "")[:300],
                             "html_url": html_url})
            continue

        for alias, title, j_clean in zip(debug["judges_raw"], debug["judges_titles"], record["judges"]):
            new_aliases.append((j_clean["name"], title, alias, record["id"]))

        out_path = out_dir / f"{record['id']}.json"
        out_path.write_text(json.dumps(record, indent=2, ensure_ascii=False))
        written.append({
            "id": record["id"],
            "citation": record["citation"],
            "outcome": record["outcome"],
            "outcome_detail": record["outcome_detail"],
            "outcome_source": debug.get("outcome_source"),
            "date": record["date_decided"],
            "case_name": record["case_name"],
            "judges": [j["name"] for j in record["judges"]],
            "judges_raw": debug.get("judges_raw"),
            "html_path": str(html_path),
            "pdf_path": str(pdf_path),
            "html_sha": record["source_hash"],
            "raw_sha": record["raw_sha256"],
            "html_url": html_url,
        })

    if new_aliases:
        update_judges_registry(new_aliases)

    summary = {
        "parser_version": PARSER_VERSION,
        "parser_baseline": "scripts/batch_0498_parse.py",
        "v031_baseline_imported": "scripts/batch_0360_parse.py",
        "ts_utc": now_iso(),
        "targets_count": len(targets),
        "written": written,
        "deferred": deferred,
        "judges_added": new_aliases,
    }
    (WORK / "parse_summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False))
    print(json.dumps({
        "parser_version": PARSER_VERSION,
        "targets_count": len(targets),
        "written_count": len(written),
        "deferred_count": len(deferred),
        "deferred": [(d["court"], d["year"], d["num"], d.get("reason")) for d in deferred],
        "written_ids": [w["id"] for w in written],
    }, indent=2))


if __name__ == "__main__":
    main()
