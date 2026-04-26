#!/usr/bin/env python3
"""Batch 0284 - Phase 4 bulk ingest. acts_in_force chronological-first.

Per next-tick plan in batch 0283:
- Refreshed pool inherited from _work/batch_0283_remaining.json (46 items).
- Sweep next 8 chronologically-earliest from refreshed pool.
- Robots.txt re-verified at start of tick.

First 8 chronological from inherited pool:
  2014/5  Supplementary Appropriation (2012) Act, 2014              (alpha S, fiscal)
  2014/6  Excess Expenditure Appropriation (2011) Act, 2014         (alpha E, fiscal)
  2014/14 Appropriation Act, 2014                                   (alpha A, fiscal)
  2015/9  Supplementary Appropriation (2013) Act, 2015              (alpha S, fiscal)
  2015/10 Excess Expenditure Appropriation (2012) Act, 2015         (alpha E, fiscal)
  2015/23 Appropriation Act, 2015                                   (alpha A, fiscal)
  2016/7  Court of Appeal Act, 2016                                 (alpha C, NON-FISCAL)
  2016/15 Public Protector Act, 2016                                (alpha P, NON-FISCAL)

NOTE: 6 fiscal-series + 2 NON-FISCAL (Court of Appeal Act, Public Protector Act).
Yield expected to improve with non-fiscal acts. Some fiscal "Appropriation Act" PDFs
in this era can exceed MAX_PDF_BYTES (4.5 MB); those will be deferred to the
oversize-PDF host-side queue per established pattern (see 2009/10, 2009/30 in b0282
and 2012/16 in b0283).

Pre-flight on-disk dedup: each pick verified absent via slug_glob_exists on
records/acts/<yr>/act-zm-<yr>-<num:03d>-*.json. None of the 8 are present.

Reuses parser from batches 0269..0283 (PARSER_VERSION 0.6.0-act-zambialii-2026-04-26).
"""
import os, sys, re, time, json, hashlib, io, glob
from datetime import datetime, timezone
import urllib.request

BATCH_NUM = "0284"
USER_AGENT = "KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)"
CRAWL = 6
PARSER_VERSION = "0.6.0-act-zambialii-2026-04-26"
MAX_PDF_BYTES = 4_500_000

PICKS = [
    {"yr":"2014","num":"5","title":"Supplementary Appropriation (2012) Act, 2014",
     "slug":"supplementary-appropriation-2012-act","sub_phase":"acts_in_force","alpha":"S"},
    {"yr":"2014","num":"6","title":"Excess Expenditure Appropriation (2011) Act, 2014",
     "slug":"excess-expenditure-appropriation-2011-act","sub_phase":"acts_in_force","alpha":"E"},
    {"yr":"2014","num":"14","title":"Appropriation Act, 2014",
     "slug":"appropriation-act","sub_phase":"acts_in_force","alpha":"A"},
    {"yr":"2015","num":"9","title":"Supplementary Appropriation (2013) Act, 2015",
     "slug":"supplementary-appropriation-2013-act","sub_phase":"acts_in_force","alpha":"S"},
    {"yr":"2015","num":"10","title":"Excess Expenditure Appropriation (2012) Act, 2015",
     "slug":"excess-expenditure-appropriation-2012-act","sub_phase":"acts_in_force","alpha":"E"},
    {"yr":"2015","num":"23","title":"Appropriation Act, 2015",
     "slug":"appropriation-act","sub_phase":"acts_in_force","alpha":"A"},
    {"yr":"2016","num":"7","title":"Court of Appeal Act, 2016",
     "slug":"court-of-appeal-act","sub_phase":"acts_in_force","alpha":"C"},
    {"yr":"2016","num":"15","title":"Public Protector Act, 2016",
     "slug":"public-protector-act","sub_phase":"acts_in_force","alpha":"P"},
]


def fetch(url, sleep=True):
    if sleep:
        time.sleep(CRAWL)
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read(), r.geturl()


def utc_now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def parse_html_sections(html_text):
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html_text, "html.parser")
    h1 = soup.find("h1")
    title = h1.get_text(strip=True) if h1 else ""
    sections = []
    akn = soup.find_all(["section", "div"], class_=re.compile(r"akn-section"))
    if not akn:
        akn = soup.find_all(id=re.compile(r"sec_|chp_"))
    for sec in akn:
        num_el = sec.find(class_=re.compile(r"akn-num"))
        heading_el = sec.find(class_=re.compile(r"akn-heading"))
        num = num_el.get_text(strip=True).rstrip(".") if num_el else ""
        heading = heading_el.get_text(strip=True) if heading_el else ""
        parts = []
        for child in sec.find_all(class_=re.compile(r"akn-content|akn-intro|akn-paragraph|akn-subsection")):
            t = child.get_text(" ", strip=True)
            if t and t not in parts:
                parts.append(t)
        if not parts:
            text = sec.get_text(" ", strip=True)
            if heading and text.startswith(heading):
                text = text[len(heading):].strip()
            if num and text.startswith(num):
                text = text[len(num):].strip()
        else:
            text = "\n".join(parts)
        if num or heading or text:
            sections.append({"number": num, "heading": heading, "text": text[:5000]})
    return title, sections


def parse_pdf_sections(pdf_bytes):
    import pdfplumber
    full_text = ""
    try:
        with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
            for page in pdf.pages:
                pt = page.extract_text()
                if pt:
                    full_text += pt + "\n"
    except Exception:
        return "", [], 0
    if not full_text.strip():
        return "", [], 0
    lines = full_text.strip().split("\n")
    title = lines[0].strip() if lines else ""
    secs = []
    pat = re.compile(r"^(\d+)\.\s+(.+?)(?:\n|$)(.*?)(?=^\d+\.\s|\Z)", re.MULTILINE | re.DOTALL)
    for m in pat.finditer(full_text):
        secs.append({
            "number": m.group(1),
            "heading": m.group(2).strip()[:300],
            "text": m.group(3).strip()[:5000],
        })
    return title, secs, len(full_text)


def append_costs(rec):
    with open("costs.log", "a") as f:
        f.write(json.dumps(rec) + "\n")


def append_provenance(rec):
    with open("provenance.log", "a") as f:
        f.write(json.dumps(rec) + "\n")


def slug_glob_exists(yr, num):
    """Slug-suffix-agnostic on-disk dedup."""
    pat = f"records/acts/{yr}/act-zm-{yr}-{int(num):03d}-*.json"
    return bool(glob.glob(pat))


def ingest_one(pick):
    yr = pick["yr"]; num = pick["num"]
    if slug_glob_exists(yr, num):
        return None, "duplicate_existing_pre_flight"
    base = f"https://zambialii.org/akn/zm/act/{yr}/{num}"
    try:
        html_body, final_html_url = fetch(base, sleep=True)
    except Exception as e:
        return None, f"html_err_{type(e).__name__}_{getattr(e,'code','')}"
    h_sha = hashlib.sha256(html_body).hexdigest()
    append_costs({"date": utc_now()[:10], "url": base, "bytes": len(html_body),
                  "batch": BATCH_NUM, "kind": "record"})
    raw_html_path = f"raw/zambialii/act/{yr}/{yr}-{int(num):03d}.html"
    os.makedirs(os.path.dirname(raw_html_path), exist_ok=True)
    with open(raw_html_path, "wb") as f:
        f.write(html_body)

    title, sections = parse_html_sections(html_body.decode("utf-8", errors="replace"))
    final_title = title or pick["title"]
    final_url = final_html_url

    pdf_path = None
    pdf_sha = None
    if len(sections) < 2:
        pdf_match = re.search(r'href="(/akn/zm/act/[0-9]+/[0-9]+/eng@[0-9-]+/source\.pdf)"',
                              html_body.decode("utf-8", errors="replace"))
        if pdf_match:
            pdf_url = "https://zambialii.org" + pdf_match.group(1)
            try:
                pdf_body, _ = fetch(pdf_url, sleep=True)
                if len(pdf_body) > MAX_PDF_BYTES:
                    return None, f"pdf_too_large_{len(pdf_body)}"
                pdf_sha = hashlib.sha256(pdf_body).hexdigest()
                append_costs({"date": utc_now()[:10], "url": pdf_url, "bytes": len(pdf_body),
                              "batch": BATCH_NUM, "kind": "record"})
                pdf_raw_path = f"raw/zambialii/act/{yr}/{yr}-{int(num):03d}.pdf"
                with open(pdf_raw_path, "wb") as f:
                    f.write(pdf_body)
                pdf_path = pdf_raw_path
                ptitle, psecs, _ = parse_pdf_sections(pdf_body)
                if psecs:
                    sections = psecs
                if ptitle and not title:
                    final_title = ptitle
            except Exception as e:
                return None, f"pdf_err_{type(e).__name__}"

    if not sections:
        return None, "no_sections"

    rid = f"act-zm-{yr}-{int(num):03d}-{pick['slug']}"
    rec = {
        "id": rid,
        "type": "act",
        "jurisdiction": "ZM",
        "title": final_title,
        "citation": f"Act No. {int(num)} of {yr}",
        "enacted_date": None,
        "commencement_date": None,
        "in_force": True,
        "amended_by": [],
        "repealed_by": None,
        "cited_authorities": [],
        "sections": sections,
        "source_url": final_url,
        "source_hash": f"sha256:{h_sha}",
        "fetched_at": utc_now(),
        "parser_version": PARSER_VERSION,
    }
    out_path = f"records/acts/{yr}/{rid}.json"
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(rec, f, indent=2, ensure_ascii=False)

    append_provenance({
        "id": rid, "source_url": final_url,
        "source_hash": f"sha256:{h_sha}", "fetched_at": rec["fetched_at"],
        "parser_version": PARSER_VERSION, "batch": BATCH_NUM,
        "raw_html": raw_html_path, "raw_pdf": pdf_path,
        "sections": len(sections),
    })
    return rec, "ok"


def main():
    indices = None
    if len(sys.argv) > 1:
        a = sys.argv[1]
        if ":" in a:
            i,j = a.split(":")
            i = int(i) if i else 0
            j = int(j) if j else len(PICKS)
            indices = list(range(i,j))
        else:
            indices = [int(a)]
    else:
        indices = list(range(len(PICKS)))

    results = []
    for idx in indices:
        pick = PICKS[idx]
        rec, status = ingest_one(pick)
        results.append({
            "idx": idx,
            "yr": pick["yr"], "num": pick["num"], "title": pick["title"],
            "alpha": pick["alpha"],
            "status": status, "id": (rec["id"] if rec else None),
            "sections": (len(rec["sections"]) if rec else 0),
            "source_hash": (rec["source_hash"] if rec else None),
            "source_url": (rec["source_url"] if rec else None),
        })
        print(f"  [{idx}] {pick['yr']}/{pick['num']} -> {status}", flush=True)

    os.makedirs("_work", exist_ok=True)
    suffix = sys.argv[1].replace(":","_") if len(sys.argv) > 1 else "all"
    with open(f"_work/batch_{BATCH_NUM}_run_{suffix}.json", "w") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()
