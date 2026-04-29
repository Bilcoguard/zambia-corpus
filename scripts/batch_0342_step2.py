#!/usr/bin/env python3
"""Batch 0342 step 2 — parse already-fetched ZMCC raw files into records.

Earlier in this tick, the b0342 fetcher was killed mid-run after persisting raw
HTML+PDF for ZMCC 2026/02, 2026/06, 2026/07 (in addition to the 6 already-ingested
records from b0341). Records were not written before the kill. We now process those
three from the persisted raw files so the tick yields records without re-fetching.
"""

import hashlib
import json
import pathlib
import re
import sys
from datetime import datetime, timezone

PARSER_VERSION = "0.2.0"
ROOT = pathlib.Path("/sessions/friendly-brave-mendel/mnt/corpus")
RAW_DIR = ROOT / "raw" / "zambialii" / "judgments"
RECORDS_DIR = ROOT / "records" / "judgments"
WORK = ROOT / "_work" / "b0342"
WORK.mkdir(parents=True, exist_ok=True)

CANDIDATES = [
    # (court, year, num, raw_basename, html_url)
    ("zmcc", 2026, 2, "judgment-zm-2026-zmcc-02-morgan-ng-ona-suing-as-secretary-general-of-the-pa",
     "https://zambialii.org/akn/zm/judgment/zmcc/2026/2/eng@2026-01-28"),
    ("zmcc", 2026, 6, "judgment-zm-2026-zmcc-06-munir-zulu-v-attorney-general-and-anor",
     "https://zambialii.org/akn/zm/judgment/zmcc/2026/6/eng@2026-03-19"),
    ("zmcc", 2026, 7, "judgment-zm-2026-zmcc-07-climate-action-professionals-zambia-v-attorney-gen",
     "https://zambialii.org/akn/zm/judgment/zmcc/2026/7/eng@2026-03-25"),
]


def now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def slugify(name: str, max_len: int = 50) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return s[:max_len].rstrip("-")


def parse_judges(judges_text: str):
    raw = [p.strip(" ,\t") for p in re.split(r",", judges_text) if p.strip()]
    judges = []
    for i, p in enumerate(raw):
        m = re.match(r"^(.+?)\s+([A-Z]{1,4}\.?)$", p.strip())
        if m:
            surname = m.group(1).strip()
            title = m.group(2).rstrip(".")
        else:
            surname = p.strip()
            title = ""
        judges.append({
            "name": surname,
            "role": "presiding" if i == 0 else "concurring",
            "dissented": False,
            "_alias": p.strip(),
            "_title": title,
        })
    return judges


def infer_outcome(summary_para: str, pdf_text):
    s = summary_para.strip()

    # Strict patterns first (PDF order paragraph priority).
    # Allow up to 4 modifier words between subject and verb (e.g., "Petition is therefore dismissed").
    DIS_MODS = r"(?:\s+(?:is|stands?|has been|therefore|hereby|accordingly)){0,4}"
    pat_pairs = [
        (re.compile(r"\bappeal" + DIS_MODS + r"\s+dismissed\b", re.I), "dismissed"),
        (re.compile(r"\bpetition" + DIS_MODS + r"\s+dismissed\b", re.I), "dismissed"),
        (re.compile(r"\bapplication" + DIS_MODS + r"\s+dismissed\b", re.I), "dismissed"),
        (re.compile(r"\b(?:matter|action)" + DIS_MODS + r"\s+dismissed\b", re.I), "dismissed"),
        (re.compile(r"\bought to be dismissed\b", re.I), "dismissed"),
        (re.compile(r"\b(?:petition|appeal|application|matter|claim|action) (?:therefore )?fails (?:for )?\b", re.I), "dismissed"),
        (re.compile(r"\bfails for lack of merit\b", re.I), "dismissed"),
        (re.compile(r"\bpetition is devoid of merit\b", re.I), "dismissed"),
        (re.compile(r"\bappeal (?:is )?(?:hereby )?allowed\b", re.I), "allowed"),
        (re.compile(r"\bapplication (?:is )?(?:hereby )?allowed\b", re.I), "allowed"),
        (re.compile(r"\bpetition (?:is )?(?:hereby )?allowed\b", re.I), "allowed"),
        (re.compile(r"\b(?:granted|grant)(?:s|ed)?\b.{0,30}(?:relief|application|petition)\b", re.I), "allowed"),
        (re.compile(r"\b(?:appeal|matter|application|petition) (?:is )?(?:hereby )?withdrawn\b", re.I), "withdrawn"),
        (re.compile(r"\bstruck (?:out|off)\b|\bstruck-out\b", re.I), "struck-out"),
        (re.compile(r"\bremitted\b|\bsent back\b", re.I), "remitted"),
        (re.compile(r"\bupheld\b", re.I), "upheld"),
        (re.compile(r"\boverturned\b|\bset aside\b", re.I), "overturned"),
        (re.compile(r"\bunconstitutional\b|\bdeclar(?:e|ed|es)\b.+\b(?:violat|breach|inconsistent|unconstitutional)\b", re.I), "allowed"),
    ]

    # Try summary first.
    for pat, out in pat_pairs:
        if pat.search(s):
            first_sent = re.split(r"(?<=[.])\s+", s, maxsplit=1)[0]
            return out, first_sent.rstrip(",;"), "summary"

    if not pdf_text:
        return None, None, "none"

    # Search PDF body. Strategy: find the disposition by anchoring on order-style
    # markers, falling back to scanning the second half of the PDF.
    body_lower = pdf_text.lower()

    anchor_keywords = [
        "we therefore order", "we order as follows", "we accordingly order",
        "it is ordered", "it is hereby ordered", "we accordingly", "we therefore",
        "the order of this court", "accordingly,", "for the foregoing reasons",
        "for these reasons", "in conclusion", "conclusion",
    ]

    # 1. Try anchored search — for each anchor keyword position (last occurrence),
    #    inspect a 1200-char window for disposition pattern.
    anchor_hits = []
    for kw in anchor_keywords:
        idx = body_lower.rfind(kw)
        if idx >= 0:
            anchor_hits.append((idx, kw))
    anchor_hits.sort()

    for idx, kw in anchor_hits:
        window = pdf_text[idx: idx + 1500]
        for pat, out in pat_pairs:
            m = pat.search(window)
            if m:
                # Take a reasonable disposition sentence.
                sent_start = max(0, m.start() - 100)
                sent_end = min(len(window), m.end() + 200)
                snippet = window[sent_start:sent_end].replace("\n", " ").strip()
                first_sent = re.split(r"(?<=[.])\s+", snippet, maxsplit=1)[0]
                # Pick the cleanest substring — the matched phrase itself
                clean = m.group(0)
                detail = first_sent[:300] if first_sent else clean
                return out, detail, f"pdf-anchor:{kw}"

    # 2. Fallback — scan the second half of the PDF for any disposition pattern.
    second_half = pdf_text[len(pdf_text) // 2:]
    for pat, out in pat_pairs:
        m = pat.search(second_half)
        if m:
            offset = len(pdf_text) // 2 + m.start()
            sent_start = max(0, offset - 100)
            sent_end = min(len(pdf_text), offset + 200)
            snippet = pdf_text[sent_start:sent_end].replace("\n", " ").strip()
            first_sent = re.split(r"(?<=[.])\s+", snippet, maxsplit=1)[0]
            return out, first_sent[:300], "pdf-second-half"

    return None, None, "none"


def build_record(court, year, num, raw_base):
    from bs4 import BeautifulSoup

    raw_dir = RAW_DIR / court / str(year)
    html_path = raw_dir / f"{raw_base}.html"
    pdf_path = raw_dir / f"{raw_base}.pdf"

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

    title = soup.find("h1").get_text(" ", strip=True) if soup.find("h1") else ""
    citation = meta.get("Media Neutral Citation", f"[{year}] ZMCC {num}")
    case_number = meta.get("Case number", "")
    court_full = meta.get("Court", "Constitutional Court of Zambia")
    judges_text = meta.get("Judges", "")
    judgment_date = meta.get("Judgment date", "")

    # date_decided
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

    # Summary content
    summary_para = ""
    flynote_text = ""
    if summary_dd:
        divs = [d for d in summary_dd.find_all("div") if d.get_text(" ", strip=True)]
        if divs:
            summary_para = divs[0].get_text(" ", strip=True)
        full_text = summary_dd.get_text("\n", strip=True)
        if "Flynote" in full_text:
            tail = full_text.split("Flynote", 1)[1]
            tail = tail.split("Read full summary", 1)[0]
            flynote_text = tail.strip()

    issue_tags = []
    if flynote_text:
        parts = re.split(r"\s*[–—]\s*|\s+-\s+", flynote_text)
        issue_tags = [p.strip() for p in parts if p and len(p.strip()) > 2]

    # PDF body for outcome inference
    pdf_text = None
    try:
        import pdfplumber
        with pdfplumber.open(str(pdf_path)) as pdf:
            pages = []
            for i, page in enumerate(pdf.pages):
                if i >= 80:
                    break
                pages.append(page.extract_text() or "")
            pdf_text = "\n".join(pages)
    except Exception:
        pdf_text = None

    outcome, outcome_detail, source = infer_outcome(summary_para, pdf_text)

    if outcome is None:
        return None, {
            "reason": "outcome_not_inferable",
            "summary_para": summary_para,
            "pdf_extractable": bool(pdf_text and len(pdf_text) > 200),
            "pdf_tail_lower": (pdf_text[-2000:] if pdf_text else "")[:2000],
        }

    if not outcome_detail:
        outcome_detail = (summary_para or "")[:300] or "Disposition recorded from PDF order paragraph."

    # case_name from title
    cn = re.sub(r"\s*\([^)]*\)\s*\[[^\]]*\][^()]*\([^)]*\)\s*$", "", title).strip()
    cn = re.sub(r"\s*\([^)]*\)\s*$", "", cn).strip()
    cn = re.sub(r"\s*\[[^\]]*\]\s*ZMCC.*$", "", cn).strip()

    judges = parse_judges(judges_text)
    judges_clean = [{k: v for k, v in j.items() if not k.startswith("_")} for j in judges]

    slug = slugify(cn, 50)
    rec_id = f"judgment-zm-{year}-{court}-{num:02d}-{slug}"

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
        "raw_sha256": sha256_bytes(pdf_bytes),
        "source_url": next(c[4] for c in CANDIDATES if c[0] == court and c[1] == year and c[2] == num),
        "source_hash": "sha256:" + sha256_bytes(html_bytes),
        "fetched_at": now_iso(),
        "parser_version": PARSER_VERSION,
    }

    return record, {
        "outcome_source": source,
        "summary_para": summary_para,
        "judges_raw": [j["_alias"] for j in judges],
        "judges_titles": [j["_title"] for j in judges],
    }


def main():
    written = []
    deferred = []
    for (court, year, num, raw_base, _url) in CANDIDATES:
        out_dir = RECORDS_DIR / court / str(year)
        out_dir.mkdir(parents=True, exist_ok=True)
        existing = list(out_dir.glob(f"judgment-zm-{year}-{court}-{num:02d}-*.json"))
        if existing:
            print(f"SKIP {court} {year}/{num}: already in corpus")
            continue

        record, debug = build_record(court, year, num, raw_base)
        if record is None:
            deferred.append({
                "court": court, "year": year, "num": num,
                "reason": debug.get("reason", "build_failed"),
                "summary_para": debug.get("summary_para", ""),
                "pdf_extractable": debug.get("pdf_extractable"),
                "raw_basename": raw_base,
            })
            continue

        out_path = out_dir / f"{record['id']}.json"
        out_path.write_text(json.dumps(record, indent=2, ensure_ascii=False))
        written.append({
            "id": record["id"],
            "citation": record["citation"],
            "outcome": record["outcome"],
            "outcome_detail": record["outcome_detail"],
            "date": record["date_decided"],
            "case_name": record["case_name"],
            "outcome_source": debug.get("outcome_source"),
            "judges_raw": debug.get("judges_raw"),
            "judges_titles": debug.get("judges_titles"),
            "raw_basename": raw_base,
            "source_hash": record["source_hash"],
            "raw_sha256": record["raw_sha256"],
        })

    summary = {"written": written, "deferred": deferred}
    (WORK / "step2_summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False))
    print(json.dumps({"written": len(written), "deferred": len(deferred)}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
