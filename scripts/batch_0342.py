#!/usr/bin/env python3
"""Batch 0342 — Phase 5 ZMCC ingestion (continuation of b0341).

Targets:
  - Re-attempt the 2 deferred ZMCC 2026 records (6 Munir Zulu privilege; 7 Climate
    Action) by reading the PDF order paragraph for the disposition.
  - Continue down the ConCourt index: ZMCC 2026/1, 2026/2.
  - Then the most recent 4 ZMCC 2025 candidates (33, 32, 30, 31).

Bounded: max 8 records this tick (BRIEF Phase 5 batch_size).

Provenance: every record records source_url, source_hash (sha256 of HTML),
raw_sha256 (sha256 of source PDF), fetched_at (ISO 8601 UTC), parser_version.
"""

import hashlib
import json
import os
import pathlib
import re
import time
import urllib.request
from datetime import datetime, timezone

UA = "KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)"
PARSER_VERSION = "0.2.0"
RATE_LIMIT_S = 5  # zambialii_seconds_between_requests

ROOT = pathlib.Path("/sessions/friendly-brave-mendel/mnt/corpus")
RAW_DIR = ROOT / "raw" / "zambialii" / "judgments"
RECORDS_DIR = ROOT / "records" / "judgments"
WORK = ROOT / "_work" / "b0342"
WORK.mkdir(parents=True, exist_ok=True)


# 8 candidates for this batch.
TARGETS = [
    # (court, year, num, date, slug-suffix-hint)
    ("zmcc", 2026, 7,  "2026-03-25", "climate-action-professionals-zambia-v-the"),
    ("zmcc", 2026, 6,  "2026-03-19", "munir-zulu-v-the-attorney-general-and-anor"),
    ("zmcc", 2026, 2,  "2026-01-28", None),
    ("zmcc", 2026, 1,  "2026-01-20", None),
    ("zmcc", 2025, 33, "2025-12-18", None),
    ("zmcc", 2025, 32, "2025-12-16", None),
    ("zmcc", 2025, 30, "2025-12-11", None),
    ("zmcc", 2025, 31, "2025-12-10", None),
]


def now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def http_get(url: str, want_pdf: bool = False) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        body = r.read()
    return body


def slugify(name: str, max_len: int = 50) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return s[:max_len].rstrip("-")


def parse_judges_from_dd(judges_text: str):
    """Return list of {name,role,dissented} from a comma-list like:
       'Munalula PC , Shilimi DPC , Musaluke JCC , Chisunka JCC , ...'
    Convention used in b0341: judges[0].role='presiding'; rest='concurring'.
    Title is preserved for registry alias matching; canonical name is the surname.
    """
    raw = [p.strip(" ,\t") for p in re.split(r",| ", judges_text) if p.strip()]
    judges = []
    for i, p in enumerate(raw):
        # last token is the title (PC|DPC|JCC|JJC|J|CJ|JS|JA|DCJ|SC|CJC)
        m = re.match(r"^(.*?)\s+([A-Z]{1,4}\.?)$", p)
        if m:
            surname = m.group(1).strip()
            title = m.group(2).rstrip(".")
        else:
            surname = p.strip()
            title = ""
        role = "presiding" if i == 0 else "concurring"
        judges.append({
            "name": surname,
            "role": role,
            "dissented": False,
            "_alias": p.strip(),  # preserved for registry update
            "_title": title,
        })
    return judges


def infer_outcome(summary_para: str, pdf_text: str | None = None):
    """Return (outcome, outcome_detail, source) where source ∈ {'summary','pdf','none'}."""
    s = summary_para.strip()
    s_lower = s.lower()

    # Look for direct disposition keywords in summary first.
    patterns = [
        (re.compile(r"\bappeal (?:is )?dismissed\b", re.I), "dismissed"),
        (re.compile(r"\bpetition (?:is )?dismissed\b", re.I), "dismissed"),
        (re.compile(r"\baction (?:is )?dismissed\b", re.I), "dismissed"),
        (re.compile(r"\b(?:application|matter|petition|appeal) (?:is )?(?:hereby )?dismissed\b", re.I), "dismissed"),
        (re.compile(r"\bappeal (?:is )?allowed\b", re.I), "allowed"),
        (re.compile(r"\bapplication (?:is )?allowed\b", re.I), "allowed"),
        (re.compile(r"\b(?:granted|grant)(?:s|ed)?\b.{0,30}(?:relief|application|petition)\b", re.I), "allowed"),
        (re.compile(r"\b(?:appeal|matter|application) (?:is )?(?:hereby )?withdrawn\b", re.I), "withdrawn"),
        (re.compile(r"\bwithdrawn\b", re.I), "withdrawn"),
        (re.compile(r"\bstruck (?:out|off)\b|\bstruck-out\b", re.I), "struck-out"),
        (re.compile(r"\bremitted\b|\bsent back\b|\bremit(?:s|ted)? to\b", re.I), "remitted"),
        (re.compile(r"\bupheld\b", re.I), "upheld"),
        (re.compile(r"\boverturned\b|\bset aside\b", re.I), "overturned"),
        # Constitutional declarations as "allowed"
        (re.compile(r"\bunconstitutional\b|\border(?:s|ed)? to\b|\bdeclar(?:e|es|ed)\b.+\b(?:violat|breach|inconsistent|unconstitutional)\b", re.I), "allowed"),
    ]
    for pat, out in patterns:
        if pat.search(s):
            return out, s.split(".")[0].strip().rstrip(",;") + ".", "summary"

    # PDF order paragraph fallback (look near end for "We order:" or numbered orders).
    if pdf_text:
        # Take the last 4000 chars where final orders typically sit
        tail = pdf_text[-4000:].lower()
        # Try to find "We order" / "It is ordered" / "It is hereby ordered" sections
        for keyword in ["it is ordered", "it is hereby ordered", "we order", "we accordingly", "we therefore"]:
            idx = tail.rfind(keyword)
            if idx >= 0:
                slice_ = tail[idx: idx + 800]
                for pat, out in patterns:
                    if pat.search(slice_):
                        # extract original-case slice for outcome_detail
                        orig_idx = pdf_text.lower().rfind(keyword)
                        snippet = pdf_text[orig_idx: orig_idx + 400].replace("\n", " ")
                        # First sentence
                        first_sent = re.split(r"(?<=[.])\s", snippet, maxsplit=1)[0]
                        return out, first_sent.strip()[:300], "pdf"

    return None, None, "none"


def build_record(court_code, year, num, html_bytes, html_url, html_path,
                 pdf_bytes, pdf_url, pdf_path):
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(html_bytes.decode("utf-8", "ignore"), "html.parser")

    # Metadata from dt/dd lists
    meta = {}
    for dl in soup.find_all("dl"):
        items = dl.find_all(["dt", "dd"])
        for i in range(0, len(items) - 1, 2):
            if items[i].name == "dt" and items[i + 1].name == "dd":
                k = items[i].get_text(" ", strip=True)
                v = items[i + 1].get_text(" ", strip=True)
                if v.endswith(" Copy"):
                    v = v[:-5].strip()
                meta[k] = v

    title = ""
    h1 = soup.find("h1")
    if h1:
        title = h1.get_text(" ", strip=True)

    citation = meta.get("Media Neutral Citation", "")
    case_number = meta.get("Case number", "")
    court_full = meta.get("Court", "")
    judges_text = meta.get("Judges", "")
    judgment_date = meta.get("Judgment date", "")

    # date_decided in YYYY-MM-DD
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

    # Summary block — first paragraph + flynote
    summary_dd = None
    for dl in soup.find_all("dl"):
        items = dl.find_all(["dt", "dd"])
        for i in range(0, len(items) - 1, 2):
            if items[i].name == "dt" and items[i + 1].name == "dd":
                if items[i].get_text(" ", strip=True) == "Summary":
                    summary_dd = items[i + 1]
                    break

    summary_para = ""
    flynote_text = ""
    if summary_dd:
        # Find <div> children: index 0 = summary para; subsequent = flynote
        divs = [d for d in summary_dd.find_all("div", recursive=True) if d.get_text(" ", strip=True)]
        if divs:
            summary_para = divs[0].get_text(" ", strip=True)
        # flynote: scan text for "Flynote\n..."
        full_text = summary_dd.get_text("\n", strip=True)
        if "Flynote" in full_text:
            tail = full_text.split("Flynote", 1)[1]
            tail = tail.split("Read full summary", 1)[0]
            flynote_text = tail.strip()

    issue_tags = []
    if flynote_text:
        # Split on en-dash, em-dash, hyphen-with-spaces
        parts = re.split(r"\s+[–—\-]\s+", flynote_text)
        issue_tags = [p.strip() for p in parts if p and len(p.strip()) > 1]

    # Disposition: try summary first, then PDF body
    pdf_text = None
    try:
        import pdfplumber
        with pdfplumber.open(str(pdf_path)) as pdf:
            pages = []
            # Read all pages but cap at 60 (PDFs can be huge)
            for i, page in enumerate(pdf.pages):
                if i >= 60:
                    break
                pages.append(page.extract_text() or "")
            pdf_text = "\n".join(pages)
    except Exception as e:
        pdf_text = None

    outcome, outcome_detail, source = infer_outcome(summary_para, pdf_text)

    if outcome is None:
        return None, {"reason": "outcome_not_inferable", "summary": summary_para[:200]}

    if not outcome_detail:
        outcome_detail = (summary_para or pdf_text or "")[:300]

    # case_name = title without (case_number) [year] ZMCC N (date)
    cn = title
    cn = re.sub(r"\s*\([^)]*\)\s*\[[^\]]*\][^()]*\([^)]*\)\s*$", "", cn).strip()
    cn = re.sub(r"\s*\([^)]*\)\s*$", "", cn).strip()
    # remove leftover trailing citation
    cn = re.sub(r"\s*\[[^\]]*\]\s*ZMCC.*$", "", cn).strip()

    # Build judges
    judges = parse_judges_from_dd(judges_text)
    judges_clean = [{k: v for k, v in j.items() if not k.startswith("_")} for j in judges]

    slug = slugify(cn, 50)
    rec_id = f"judgment-zm-{year}-{court_code}-{num:02d}-{slug}"

    record = {
        "id": rec_id,
        "type": "judgment",
        "jurisdiction": "ZM",
        "title": title,
        "citation": citation or f"[{year}] ZMCC {num}",
        "court": court_full or "Constitutional Court of Zambia",
        "case_name": cn,
        "case_number": case_number,
        "date_decided": date_decided,
        "judges": judges_clean,
        "issue_tags": issue_tags or [cn[:80]],  # fallback to case name slice if no flynote
        "outcome": outcome,
        "outcome_detail": outcome_detail,
        "reasoning_tags": [],
        "key_statutes": [],
        "raw_sha256": sha256_bytes(pdf_bytes) if pdf_bytes else "",
        "source_url": html_url,
        "source_hash": "sha256:" + sha256_bytes(html_bytes),
        "fetched_at": now_iso(),
        "parser_version": PARSER_VERSION,
    }

    debug = {
        "outcome_source": source,
        "summary_para": summary_para,
        "judges_raw": [j["_alias"] for j in judges],
        "judges_titles": [j["_title"] for j in judges],
    }
    return record, debug


def main():
    fetches = 0
    written = []
    deferred = []
    for (court, year, num, dt, _hint) in TARGETS:
        # Skip the candidates already on disk in records/
        out_dir = RECORDS_DIR / court / str(year)
        out_dir.mkdir(parents=True, exist_ok=True)
        existing = list(out_dir.glob(f"judgment-zm-{year}-{court}-{num:02d}-*.json"))
        if existing:
            print(f"SKIP {court} {year}/{num}: already in corpus ({existing[0].name})")
            continue

        html_url = f"https://zambialii.org/akn/zm/judgment/{court}/{year}/{num}/eng@{dt}"
        pdf_url = html_url + "/source.pdf"

        # Fetch HTML
        try:
            html_bytes = http_get(html_url)
            fetches += 1
        except Exception as e:
            deferred.append({"court": court, "year": year, "num": num, "reason": f"html_fetch_fail: {e}"})
            continue
        time.sleep(RATE_LIMIT_S)

        # Get title preview to build slug for raw filename
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html_bytes.decode("utf-8", "ignore"), "html.parser")
        h1 = soup.find("h1")
        title_preview = h1.get_text(" ", strip=True) if h1 else f"zmcc-{year}-{num}"
        # Build a temp slug from case_name part
        cn_preview = re.sub(r"\s*\([^)]*\)\s*\[[^\]]*\][^()]*\([^)]*\)\s*$", "", title_preview).strip()
        cn_preview = re.sub(r"\s*\([^)]*\)\s*$", "", cn_preview).strip()
        slug_preview = slugify(cn_preview, 50)
        raw_base = f"judgment-zm-{year}-{court}-{num:02d}-{slug_preview}"

        # Persist HTML
        raw_year_dir = RAW_DIR / court / str(year)
        raw_year_dir.mkdir(parents=True, exist_ok=True)
        html_path = raw_year_dir / f"{raw_base}.html"
        html_path.write_bytes(html_bytes)

        # Fetch PDF
        try:
            pdf_bytes = http_get(pdf_url, want_pdf=True)
            fetches += 1
        except Exception as e:
            deferred.append({"court": court, "year": year, "num": num,
                             "reason": f"pdf_fetch_fail: {e}",
                             "html_url": html_url})
            continue
        time.sleep(RATE_LIMIT_S)

        pdf_path = raw_year_dir / f"{raw_base}.pdf"
        pdf_path.write_bytes(pdf_bytes)

        # Build record
        record, debug = build_record(court, year, num, html_bytes, html_url, html_path,
                                     pdf_bytes, pdf_url, pdf_path)
        if record is None:
            deferred.append({"court": court, "year": year, "num": num,
                             "reason": debug.get("reason", "build_failed"),
                             "summary": debug.get("summary", "")[:300],
                             "html_url": html_url})
            continue

        out_path = out_dir / f"{record['id']}.json"
        out_path.write_text(json.dumps(record, indent=2, ensure_ascii=False))
        written.append({"id": record["id"],
                        "citation": record["citation"],
                        "outcome": record["outcome"],
                        "date": record["date_decided"],
                        "case_name": record["case_name"],
                        "outcome_source": debug.get("outcome_source"),
                        "judges_raw": debug.get("judges_raw"),
                        "judges_titles": debug.get("judges_titles"),
                        "html_path": str(html_path),
                        "pdf_path": str(pdf_path),
                        "html_sha": record["source_hash"],
                        "raw_sha": record["raw_sha256"]})

    summary = {
        "fetches": fetches,
        "written": written,
        "deferred": deferred,
    }
    (WORK / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False))
    print(json.dumps({"fetches": fetches, "written_count": len(written),
                      "deferred_count": len(deferred)}, indent=2))


if __name__ == "__main__":
    main()
