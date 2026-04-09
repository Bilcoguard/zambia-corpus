#!/usr/bin/env python3
"""Parse a saved acts-of-parliament page and report year range + Companies Act hits."""
import re, sys, json
from html.parser import HTMLParser
from urllib.parse import urljoin

BASE = "https://www.parliament.gov.zm/"

class P(HTMLParser):
    def __init__(self):
        super().__init__()
        self.rows = []           # (href, text)
        self.year_headings = []  # ints
        self._a = False; self._h = None; self._t = []
        self._h3 = False; self._h3_text = []
    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag.lower() == "a":
            href = d.get("href")
            if href:
                self._a = True; self._h = href; self._t = []
        elif tag.lower() == "h3":
            self._h3 = True; self._h3_text = []
    def handle_endtag(self, tag):
        if tag.lower() == "a" and self._a:
            t = re.sub(r"\s+", " ", "".join(self._t)).strip()
            self.rows.append((self._h, t))
            self._a = False
        elif tag.lower() == "h3" and self._h3:
            t = re.sub(r"\s+", " ", "".join(self._h3_text)).strip()
            m = re.fullmatch(r"(\d{4})", t)
            if m: self.year_headings.append(int(m.group(1)))
            self._h3 = False
    def handle_data(self, data):
        if self._a: self._t.append(data)
        if self._h3: self._h3_text.append(data)

def main():
    path = sys.argv[1]
    with open(path, "rb") as f:
        html = f.read().decode("utf-8", errors="replace")
    p = P()
    p.feed(html)

    # Filter rows that look like Acts (link text contains "Act No." or pattern)
    acts = []
    for href, text in p.rows:
        if not href or not text:
            continue
        if not href.startswith("/node/"):
            continue
        # Must look like an Act listing entry
        if "act no." in text.lower() or re.search(r"act\s*no\.?\s*\d+", text, re.I):
            # Extract year and act number
            year_m = re.search(r"of\s*(\d{4})", text)
            num_m = re.search(r"act\s*no\.?\s*(\d+)\s*of\s*(\d{4})", text, re.I)
            year = int(year_m.group(1)) if year_m else None
            act_num = int(num_m.group(1)) if num_m else None
            acts.append({
                "href": urljoin(BASE, href),
                "text": text,
                "year": year,
                "act_num": act_num,
            })

    years_in_acts = sorted({a["year"] for a in acts if a["year"]})
    out = {
        "path": path,
        "act_count": len(acts),
        "year_range": [years_in_acts[0], years_in_acts[-1]] if years_in_acts else None,
        "year_headings_h3": p.year_headings,
        "companies_hits": [a for a in acts if "companies" in a["text"].lower()],
        "acts_2017": [a for a in acts if a["year"] == 2017],
        "all_acts": acts,
    }
    print(json.dumps(out, indent=2))

if __name__ == "__main__":
    main()
