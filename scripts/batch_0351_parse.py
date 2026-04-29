#!/usr/bin/env python3
"""Batch 0351 parser-only step.

Parses the 8 ZMCC raw HTML+PDF pairs persisted by batch_0349_fetch.py
under the tightened parser_version 0.3.0 policy locked in at b0344
(frozen from b0348).

  * PRIMARY: ZambiaLII summary `<dd>` regex (extended for ConCourt phrasing).
  * SECONDARY: PDF order-anchor matches in 800-char window from a locked
    anchor list ("It is ordered" etc.). pdf-tail/full sweeps removed.
    Soft anchors rejected.
  * outcome_detail safety guards (word boundary, ≥12 alphabetic chars,
    cross-reference blacklist).

Per BRIEF.md non-negotiable #1, candidates that cannot meet these tests
are DEFERRED to gaps.md (no record written). No fabrication.
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

PARSER_VERSION = "0.3.0"
HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
RAW_DIR = ROOT / "raw" / "zambialii" / "judgments"
RECORDS_DIR = ROOT / "records" / "judgments"
WORK = ROOT / "_work" / "b0351"
WORK.mkdir(parents=True, exist_ok=True)
JUDGES_REG = ROOT / "judges_registry.yaml"


TARGETS = [
    ("zmcc", 2024, 5, "2024-03-15"),
    ("zmcc", 2024, 4, "2024-02-23"),
    ("zmcc", 2024, 3, "2024-02-09"),
    ("zmcc", 2024, 2, "2024-01-17"),
    ("zmcc", 2024, 1, "2024-01-25"),
]

# ----------------------------------------------------------------------
# Outcome inference (frozen from b0347 — parser_version 0.3.0)
# ----------------------------------------------------------------------

SUMMARY_PATTERNS = [
    (re.compile(r"\b(?:appeal|petition|application|action|matter)\s+(?:is\s+)?(?:hereby\s+)?dismissed\b", re.I), "dismissed"),
    (re.compile(r"\b(?:appeal|petition|application)\s+(?:is\s+)?(?:hereby\s+)?allowed\b", re.I), "allowed"),
    (re.compile(r"\bappeal\s+succeeds?\b", re.I), "allowed"),
    (re.compile(r"\bgrant(?:ed)?\s+the\s+(?:relief|application|petition)\b", re.I), "allowed"),
    (re.compile(r"\b(?:application|matter|petition|appeal)\s+(?:is\s+)?(?:hereby\s+)?withdrawn\b", re.I), "withdrawn"),
    (re.compile(r"\b(?:application|petition|appeal|matter)\s+(?:is\s+)?(?:hereby\s+)?struck\s+(?:out|off)\b", re.I), "struck-out"),
    (re.compile(r"\bremitted\b|\bremit(?:s|ted)?\s+to\b", re.I), "remitted"),
    (re.compile(r"\bappeal\s+(?:is\s+)?upheld\b|\bpetition\s+(?:is\s+)?upheld\b", re.I), "upheld"),
    (re.compile(r"\bApplication\s+for\s+\w+(?:\s+\w+){0,3}\s+dismissed\b", re.I), "dismissed"),
    (re.compile(r"\bCourt\s+dismissed\b", re.I), "dismissed"),
    (re.compile(r"\bCourt\s+(?:allowed|granted)\b", re.I), "allowed"),
    (re.compile(r"\bCourt\s+upheld\b", re.I), "upheld"),
    (re.compile(r"\bCourt\s+overturned\b", re.I), "overturned"),
    (re.compile(r"\bjoinder\s+granted\b|\bgranted\s+joinder\b", re.I), "allowed"),
    (re.compile(r"\bdeclar(?:e|es|ed)\s+(?:that\s+)?(?:the\s+|that\s+)?\w[\w\s,]+?\b(?:violat(?:e|es|ed)|breach(?:es|ed)?|inconsistent\s+with|unconstitutional)\b", re.I), "allowed"),
]

PDF_ORDER_ANCHORS = [
    "it is ordered",
    "it is hereby ordered",
    "it is accordingly ordered",
    "we accordingly order",
    "we hereby order",
    "we make the following order",
    "we therefore order",
    "we order as follows",
    "the order of the court",
    "the orders of the court",
    "the following orders",
    "the following order",
]

DETAIL_BLACKLIST_SUBSTRINGS = [
    "case supra",
    " supra",
    "another v ",
    "and another v ",
    "Generall4l",
    "Generall4]",
    "Mulonda",
]

MID_WORD_FRAGMENT_RE = re.compile(r"^[a-z](?:\s|$)")


def now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def slugify(name: str, max_len: int = 50) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return s[:max_len].rstrip("-")


# ----------------------------------------------------------------------
# Judges parsing (frozen from b0347)
# ----------------------------------------------------------------------

INITIAL_RE = re.compile(r"\b[A-Z]\.?\s*[A-Z]?\.?\b")


def parse_one_judge(alias_raw: str):
    s = alias_raw.strip(" ,\t-")
    if not s:
        return None
    title = ""
    m = re.search(r"\b(PC|DPC|CJ|DCJ|JCC|JJC|JC|JS|JA|J|JJ|JJA)\b\.?", s)
    if m:
        title = m.group(1)
    bare = s
    bare = re.sub(r"^HON\.?\s*", "", bare, flags=re.I).strip()
    bare = re.sub(r"^(?:Honourable|Hon\.?)\s+", "", bare, flags=re.I).strip()
    bare = re.sub(r"^(?:Lord|Lady)\s+", "", bare, flags=re.I).strip()
    bare = re.sub(r"^(?:Mr|Mrs|Ms)\.?\s+", "", bare, flags=re.I).strip()
    bare = re.sub(r"^Justice\s+", "", bare, flags=re.I).strip()
    bare = re.sub(r"\s+(?:PC|DPC|CJ|DCJ|JCC|JJC|JC|JS|JA|J|JJ|JJA)\.?$", "", bare).strip()
    bare = re.sub(r"\s+(?:PC|DPC|CJ|DCJ|JCC|JJC|JC|JS|JA|J|JJ|JJA)\.?\b", "", bare).strip()
    bare = INITIAL_RE.sub("", bare).strip()
    bare = re.sub(r"\s+", " ", bare).strip(" .,-")
    if " - " in bare or "-" in bare:
        parts = re.split(r"\s*-\s*", bare)
        bare = parts[-1].strip()
    if " " in bare:
        bare = bare.split()[-1]
    canonical = bare.strip().title() if bare else ""
    return canonical, title, False, s


def parse_judges(judges_text: str):
    if not judges_text:
        return []
    raw_parts = [p.strip(" ,\t") for p in re.split(r",", judges_text) if p.strip()]
    out = []
    for i, p in enumerate(raw_parts):
        parsed = parse_one_judge(p)
        if not parsed:
            continue
        canonical, title, dissented, alias = parsed
        if not canonical:
            continue
        role = "presiding" if i == 0 else "concurring"
        out.append({
            "name": canonical,
            "role": role,
            "dissented": dissented,
            "_alias": alias,
            "_title": title,
        })
    return out


# ----------------------------------------------------------------------
# Outcome inference helpers
# ----------------------------------------------------------------------

def _detail_is_safe(detail: str) -> bool:
    if not detail:
        return False
    if MID_WORD_FRAGMENT_RE.match(detail):
        return False
    if not re.search(r"[A-Za-z]{4,}", detail):
        return False
    for bad in DETAIL_BLACKLIST_SUBSTRINGS:
        if bad in detail:
            return False
    alpha = re.sub(r"[^A-Za-z]", "", detail)
    if len(alpha) < 12:
        return False
    return True


def _extract_detail_around(text: str, m: re.Match) -> str:
    start = m.start()
    end = m.end()
    i = start
    while i > 0 and text[i - 1] not in ".?!\n":
        i -= 1
    j = end
    while j < len(text) and text[j] not in ".?!\n":
        j += 1
    snippet = text[i:j].replace("\n", " ").strip()
    snippet = re.sub(r"\s+", " ", snippet).strip()
    if len(snippet) > 300:
        snippet = snippet[:300].rstrip() + "…"
    return snippet


def find_outcome_in_text(text: str):
    if not text:
        return None, None, None
    for pat, out in SUMMARY_PATTERNS:
        m = pat.search(text)
        if m:
            detail = _extract_detail_around(text, m)
            if _detail_is_safe(detail):
                return out, detail, pat.pattern
    return None, None, None


def find_outcome_in_pdf(pdf_text: str):
    if not pdf_text:
        return None, None, None
    lower = pdf_text.lower()
    best_idx = -1
    best_kw = None
    for kw in PDF_ORDER_ANCHORS:
        idx = lower.rfind(kw)
        if idx > best_idx:
            best_idx = idx
            best_kw = kw
    if best_idx < 0:
        return None, None, None
    window = pdf_text[best_idx: best_idx + 800]
    out, detail, _ = find_outcome_in_text(window)
    if out is None:
        return None, None, None
    return out, detail, best_kw


def infer_outcome(summary_para: str, pdf_text):
    out, detail, _ = find_outcome_in_text(summary_para or "")
    if out:
        return out, detail, "summary"
    if pdf_text:
        out, detail, kw = find_outcome_in_pdf(pdf_text)
        if out:
            return out, detail, f"pdf-anchor:{kw}"
    return None, None, "none"


# ----------------------------------------------------------------------
# Parse one judgment
# ----------------------------------------------------------------------

def extract_pdf_text(path: pathlib.Path):
    try:
        import pdfplumber
        text_parts = []
        with pdfplumber.open(str(path)) as pdf:
            for i, page in enumerate(pdf.pages):
                if i >= 80:
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

    citation = meta.get("Media Neutral Citation", "") or f"[{year}] ZMCC {num}"
    case_number = meta.get("Case number", "")
    court_full = "Constitutional Court of Zambia"
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

    pdf_text = extract_pdf_text(pdf_path)
    outcome, outcome_detail, src = infer_outcome(summary_para, pdf_text)
    if outcome is None:
        return None, {"reason": "outcome_not_inferable_under_tightened_policy",
                      "summary_head": (summary_para or "")[:300]}

    if not outcome_detail:
        return None, {"reason": "outcome_detail_missing", "src": src,
                      "summary_head": (summary_para or "")[:300]}

    cn = title
    cn = re.sub(r"\s*\([^)]*\)\s*\[[^\]]*\][^()]*\([^)]*\)\s*$", "", cn).strip()
    cn = re.sub(r"\s*\([^)]*\)\s*$", "", cn).strip()
    cn = re.sub(r"\s*\[[^\]]*\]\s*ZMCC.*$", "", cn).strip()

    judges = parse_judges(judges_text)
    if not judges:
        return None, {"reason": "no_judges_parsed",
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


# ----------------------------------------------------------------------
# Judges registry update (frozen from b0347)
# ----------------------------------------------------------------------

def update_judges_registry(new_judges_aliases):
    reg = yaml.safe_load(JUDGES_REG.read_text())
    by_name = {j["canonical_name"]: j for j in reg["judges"]}
    now = now_iso()
    changed = False
    for canonical, title, alias, fsi in new_judges_aliases:
        if not canonical:
            continue
        target_canon = None
        if canonical in by_name:
            target_canon = canonical
        else:
            for cn in by_name.keys():
                first = cn.split()[0] if cn else ""
                if first == canonical:
                    target_canon = cn
                    break
        if target_canon is not None:
            j = by_name[target_canon]
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
            new_entry = {
                "canonical_name": canonical,
                "titles": [{"title": title, "first_seen_in": fsi, "first_seen_at": now}] if title else [],
                "aliases": [alias] if alias else [],
                "first_seen": now,
            }
            reg["judges"].append(new_entry)
            by_name[canonical] = new_entry
            changed = True
    if changed:
        reg["judges"] = sorted(reg["judges"], key=lambda j: j["canonical_name"])
        JUDGES_REG.write_text(yaml.safe_dump(reg, sort_keys=False, allow_unicode=True))
    return changed


def lookup_in_registry(canonical: str):
    reg = yaml.safe_load(JUDGES_REG.read_text())
    by_name = {j["canonical_name"]: j for j in reg["judges"]}
    if canonical in by_name:
        return canonical
    for cn in by_name.keys():
        first = cn.split()[0] if cn else ""
        if first == canonical:
            return cn
    return None


# ----------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------

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
                             "summary": (debug.get("summary_head") or debug.get("summary_para") or "")[:300],
                             "html_url": html_url})
            continue

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
                      "deferred_count": len(deferred),
                      "deferred": [(d["court"], d["year"], d["num"], d["reason"]) for d in deferred],
                      "written_ids": [w["id"] for w in written]}, indent=2))


if __name__ == "__main__":
    main()
