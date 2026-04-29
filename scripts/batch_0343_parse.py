#!/usr/bin/env python3
"""Batch 0343 parser-only step.

Reads raw HTML+PDF persisted by batch_0343_fetch.py and builds judgment
records under records/judgments/zmcc/{year}/. Updates judges_registry.yaml.
Defers any candidate whose disposition cannot be safely inferred (no
fabrication).
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

PARSER_VERSION = "0.2.0"
ROOT = pathlib.Path("/sessions/charming-dreamy-cori/mnt/corpus")
RAW_DIR = ROOT / "raw" / "zambialii" / "judgments"
RECORDS_DIR = ROOT / "records" / "judgments"
WORK = ROOT / "_work" / "b0343"
JUDGES_REG = ROOT / "judges_registry.yaml"


# (court, year, num, dt) — same as fetcher
TARGETS = [
    ("zmcc", 2026, 1,  "2026-01-20"),
    ("zmcc", 2025, 33, "2025-12-18"),
    ("zmcc", 2025, 32, "2025-12-16"),
    ("zmcc", 2025, 31, "2025-12-10"),
    ("zmcc", 2025, 30, "2025-12-11"),
    ("zmcc", 2025, 29, "2025-12-08"),
    ("zmcc", 2025, 28, "2025-12-05"),
    ("zmcc", 2025, 27, "2025-12-05"),
]

OUTCOME_PATTERNS = [
    (re.compile(r"\b(?:appeal|petition|application|action|matter)\s+(?:is\s+)?(?:hereby\s+)?dismissed\b", re.I), "dismissed"),
    (re.compile(r"\b(?:appeal|petition|application)\s+(?:is\s+)?(?:hereby\s+)?allowed\b", re.I), "allowed"),
    (re.compile(r"\bappeal\s+succeeds?\b", re.I), "allowed"),
    (re.compile(r"\bgrant(?:ed)?\s+the\s+(?:relief|application|petition)\b", re.I), "allowed"),
    (re.compile(r"\b(?:application|matter|petition|appeal)\s+(?:is\s+)?(?:hereby\s+)?withdrawn\b", re.I), "withdrawn"),
    (re.compile(r"\b(?:application|petition|appeal|matter)\s+(?:is\s+)?(?:hereby\s+)?struck\s+(?:out|off)\b", re.I), "struck-out"),
    (re.compile(r"\bremitted\b|\bremit(?:s|ted)?\s+to\b", re.I), "remitted"),
    (re.compile(r"\bappeal\s+(?:is\s+)?upheld\b|\bpetition\s+(?:is\s+)?upheld\b", re.I), "upheld"),
    (re.compile(r"\boverturned\b|\bset\s+aside\b", re.I), "overturned"),
    (re.compile(r"\bdeclar(?:e|es|ed)\s+.+\b(?:violat|breach|inconsistent|unconstitutional)\b", re.I), "allowed"),
]

PDF_KEYWORDS = [
    "it is ordered",
    "it is hereby ordered",
    "it is accordingly ordered",
    "we order",
    "we accordingly",
    "we therefore",
    "for the foregoing",
    "in conclusion",
    "accordingly,",
    "we conclude",
]


def now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def slugify(name: str, max_len: int = 50) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return s[:max_len].rstrip("-")


def parse_judges(judges_text: str):
    raw = [p.strip(" ,\t") for p in re.split(r",", judges_text) if p.strip()]
    judges = []
    for i, p in enumerate(raw):
        m = re.match(r"^(.*?)\s+([A-Z]{1,4}\.?)$", p.strip())
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
            "_alias": p.strip(),
            "_title": title,
        })
    return judges


def find_outcome_in_text(text: str):
    for pat, out in OUTCOME_PATTERNS:
        m = pat.search(text)
        if m:
            # one-sentence detail around the match
            start = max(0, m.start() - 80)
            end = min(len(text), m.end() + 200)
            snippet = text[start:end].replace("\n", " ").strip()
            # First sentence in snippet
            sent = re.split(r"(?<=[.])\s+", snippet, maxsplit=2)
            detail = sent[0] if sent else snippet
            return out, detail.strip()[:300]
    return None, None


def infer_outcome(summary_para: str, pdf_text: str | None):
    # Try summary first (cheap)
    out, detail = find_outcome_in_text(summary_para or "")
    if out:
        return out, detail, "summary"

    if pdf_text:
        # Look near tail / order paragraphs first.
        tail = pdf_text[-6000:]
        out, detail = find_outcome_in_text(tail)
        if out:
            return out, detail, "pdf-tail"

        # Look around explicit order keywords
        lower = pdf_text.lower()
        for kw in PDF_KEYWORDS:
            idx = lower.rfind(kw)
            if idx >= 0:
                slice_ = pdf_text[idx: idx + 1500]
                out, detail = find_outcome_in_text(slice_)
                if out:
                    return out, detail, f"pdf-kw:{kw}"

        # Whole-document fallback (last resort)
        out, detail = find_outcome_in_text(pdf_text)
        if out:
            return out, detail, "pdf-full"

    return None, None, "none"


def extract_pdf_text(path: pathlib.Path) -> str | None:
    try:
        import pdfplumber
        text_parts = []
        with pdfplumber.open(str(path)) as pdf:
            for i, page in enumerate(pdf.pages):
                if i >= 80:  # cap
                    break
                t = page.extract_text() or ""
                text_parts.append(t)
        return "\n".join(text_parts)
    except Exception as e:
        print(f"pdfplumber error on {path}: {e}", file=sys.stderr)
        return None


def build_record(court_code, year, num, html_path, pdf_path, html_url, pdf_url):
    html_bytes = html_path.read_bytes()
    pdf_bytes = pdf_path.read_bytes()
    soup = BeautifulSoup(html_bytes.decode("utf-8", "ignore"), "html.parser")

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

    h1 = soup.find("h1")
    title = h1.get_text(" ", strip=True) if h1 else ""

    citation = meta.get("Media Neutral Citation", "") or f"[{year}] ZMCC {num}"
    case_number = meta.get("Case number", "")
    court_full = meta.get("Court", "") or "Constitutional Court of Zambia"
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

    # Summary block
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

    pdf_text = extract_pdf_text(pdf_path)
    outcome, outcome_detail, src = infer_outcome(summary_para, pdf_text)
    if outcome is None:
        return None, {"reason": "outcome_not_inferable",
                      "summary_head": (summary_para or "")[:300]}

    if not outcome_detail:
        outcome_detail = (summary_para or pdf_text or "")[:300]

    # case_name = title without trailing citation/case-number suffix
    cn = title
    cn = re.sub(r"\s*\([^)]*\)\s*\[[^\]]*\][^()]*\([^)]*\)\s*$", "", cn).strip()
    cn = re.sub(r"\s*\([^)]*\)\s*$", "", cn).strip()
    cn = re.sub(r"\s*\[[^\]]*\]\s*ZMCC.*$", "", cn).strip()

    judges = parse_judges(judges_text)
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


def update_judges_registry(new_judges_aliases):
    """new_judges_aliases: list of (canonical_name, title, alias, first_seen_in)"""
    reg = yaml.safe_load(JUDGES_REG.read_text())
    by_name = {j["canonical_name"]: j for j in reg["judges"]}
    now = now_iso()
    changed = False
    for canonical, title, alias, fsi in new_judges_aliases:
        if canonical in by_name:
            j = by_name[canonical]
            existing_titles = {t["title"] for t in j.get("titles", [])}
            if title and title not in existing_titles:
                j.setdefault("titles", []).append(
                    {"title": title, "first_seen_in": fsi, "first_seen_at": now}
                )
                changed = True
            existing_aliases = set(j.get("aliases", []))
            if alias and alias not in existing_aliases:
                j.setdefault("aliases", []).append(alias)
                changed = True
        else:
            reg["judges"].append({
                "canonical_name": canonical,
                "titles": [{"title": title, "first_seen_in": fsi, "first_seen_at": now}] if title else [],
                "aliases": [alias] if alias else [],
                "first_seen": now,
            })
            by_name[canonical] = reg["judges"][-1]
            changed = True
    if changed:
        reg["judges"] = sorted(reg["judges"], key=lambda j: j["canonical_name"])
        JUDGES_REG.write_text(yaml.safe_dump(reg, sort_keys=False, allow_unicode=True))
    return changed


def main():
    written = []
    deferred = []
    new_aliases = []

    for (court, year, num, dt) in TARGETS:
        out_dir = RECORDS_DIR / court / str(year)
        out_dir.mkdir(parents=True, exist_ok=True)
        existing = list(out_dir.glob(f"judgment-zm-{year}-{court}-{num:02d}-*.json"))
        if existing:
            print(f"SKIP {court} {year}/{num}: already in corpus ({existing[0].name})")
            continue

        raw_year_dir = RAW_DIR / court / str(year)
        html_files = list(raw_year_dir.glob(f"judgment-zm-{year}-{court}-{num:02d}-*.html"))
        pdf_files = list(raw_year_dir.glob(f"judgment-zm-{year}-{court}-{num:02d}-*.pdf"))
        if not html_files or not pdf_files:
            deferred.append({"court": court, "year": year, "num": num,
                             "reason": "raw bytes not on disk"})
            continue
        html_path = html_files[0]
        pdf_path = pdf_files[0]

        html_url = f"https://zambialii.org/akn/zm/judgment/{court}/{year}/{num}/eng@{dt}"
        pdf_url = html_url + "/source.pdf"

        record, debug = build_record(court, year, num, html_path, pdf_path, html_url, pdf_url)
        if record is None:
            deferred.append({"court": court, "year": year, "num": num,
                             "reason": debug.get("reason"),
                             "summary": debug.get("summary_head", "")[:300],
                             "html_url": html_url})
            continue

        # Collect judges for registry update from debug aliases/titles.
        for alias, title, j_clean in zip(debug["judges_raw"], debug["judges_titles"], record["judges"]):
            new_aliases.append((j_clean["name"], title, alias, record["id"]))

        out_path = out_dir / f"{record['id']}.json"
        out_path.write_text(json.dumps(record, indent=2, ensure_ascii=False))
        written.append({"id": record["id"],
                        "citation": record["citation"],
                        "outcome": record["outcome"],
                        "date": record["date_decided"],
                        "case_name": record["case_name"],
                        "outcome_source": debug.get("outcome_source"),
                        "judges_raw": debug.get("judges_raw"),
                        "html_path": str(html_path),
                        "pdf_path": str(pdf_path),
                        "html_sha": record["source_hash"],
                        "raw_sha": record["raw_sha256"]})

    if new_aliases:
        update_judges_registry(new_aliases)

    summary = {"written": written, "deferred": deferred,
               "judges_added": new_aliases}
    (WORK / "parse_summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False))
    print(json.dumps({"written_count": len(written),
                      "deferred_count": len(deferred)}, indent=2))


if __name__ == "__main__":
    main()
