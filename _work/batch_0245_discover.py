"""Phase 4 batch 0245 discovery - probe year listings for novel SIs.
Targets: year=2024 p4, year=2023 p2, year=2023 p3, year=2022 p1.
First re-verify robots.txt. Honour 6s crawl-delay.
"""
import sys, os, json, hashlib, time, urllib.request, re
from datetime import datetime, timezone
from bs4 import BeautifulSoup

UA = "KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)"
HEADERS = {"User-Agent": UA}
CRAWL = 6.0
BATCH = "0245"

def fetch(url, sleep=True):
    if sleep: time.sleep(CRAWL)
    req = urllib.request.Request(url, headers=HEADERS)
    return urllib.request.urlopen(req, timeout=45).read()

# 1) robots.txt re-verify
robots_url = "https://zambialii.org/robots.txt"
robots = fetch(robots_url, sleep=False).decode('utf-8', 'replace')
robots_sha = hashlib.sha256(robots.encode()).hexdigest()
ts = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
robots_path = f"_work/batch_{BATCH}_robots_{ts}.txt"
with open(robots_path, 'w') as f: f.write(robots)
print(f"robots sha256 prefix: {robots_sha[:16]}  saved: {robots_path}")

# verify Disallow patterns we already know
disallowed = re.findall(r'Disallow:\s*(\S+)', robots)
print(f"Disallow rules: {disallowed}")

# Verify SI path is allowed (not in Disallow)
si_test_paths = ["/akn/zm/act/si/", "/akn/zm/act/si/2024/", "/akn/zm/act/si/2023/"]
for p in si_test_paths:
    blocked = any(p.startswith(d) for d in disallowed if d != "/")
    print(f"  {p}: {'BLOCKED' if blocked else 'allowed'}")

# 2) Probe year listings
PROBES = [
    ("year2024p4", "https://zambialii.org/legislation/subsidiary?years=2024&page=4"),
    ("year2023p2", "https://zambialii.org/legislation/subsidiary?years=2023&page=2"),
    ("year2023p3", "https://zambialii.org/legislation/subsidiary?years=2023&page=3"),
    ("year2022p1", "https://zambialii.org/legislation/subsidiary?years=2022&page=1"),
]

# Build set of ingested SI ids by scanning records/sis/
ingested = set()
for root, dirs, files in os.walk('records/sis'):
    for fn in files:
        if fn.endswith('.json'):
            m = re.match(r'si-zm-(\d{4})-(\d{3})-', fn)
            if m: ingested.add(f"{m.group(1)}/{int(m.group(2))}")
print(f"ingested SI count (by yr/num): {len(ingested)}")

results = {}
for name, url in PROBES:
    try:
        b = fetch(url)
        path = f"_work/batch_{BATCH}_{name}.html"
        with open(path,'wb') as f: f.write(b)
        soup = BeautifulSoup(b, 'html.parser')
        candidates = []
        # Find table rows with SI links
        for a in soup.find_all('a', href=True):
            href = a['href']
            m = re.match(r'^/akn/zm/act/si/(\d{4})/(\d+)$', href) or \
                re.match(r'^/akn/zm/act/si/(\d{4})/(\d+)/?', href)
            if m:
                yr, num = m.group(1), m.group(2)
                yn = f"{yr}/{int(num)}"
                if yn not in ingested:
                    title = a.get_text(strip=True)
                    if title and len(title) > 5:
                        candidates.append({'yr_num': yn, 'year': yr, 'num': num,
                                           'title': title, 'href': href})
        # dedupe by yr_num
        seen=set(); deduped=[]
        for c in candidates:
            if c['yr_num'] in seen: continue
            seen.add(c['yr_num']); deduped.append(c)
        results[name] = {'url': url, 'candidates': deduped, 'count': len(deduped)}
        print(f"  {name}: {len(deduped)} novel candidates")
    except Exception as e:
        results[name] = {'url': url, 'error': str(e)}
        print(f"  {name}: ERROR {e}")

with open(f'_work/batch_{BATCH}_discover.json', 'w') as f:
    json.dump({
        'robots_sha256_prefix': robots_sha[:16],
        'robots_path': robots_path,
        'disallow': disallowed,
        'ingested_count': len(ingested),
        'probes': results,
    }, f, indent=2)
print("\nDiscovery complete.")
