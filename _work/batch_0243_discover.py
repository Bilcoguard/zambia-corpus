"""Batch 0243 discovery - robots reverify + alphabet G probe.

Surfaces modern (>=2017) novel SIs starting with G, plus carries forward 2
unprocessed residuals from batch 0242's year=2025 listing cache:
  1985/45 Air Services (Aerial Application Permit) Regulations, 1985
  1992/9  Air Passenger Service Charge (Charging) Order, 1992
(both pre-2017 — sis_transport coverage extension under year=2025 listing scope)
"""
import os, json, hashlib, time, urllib.request, re, glob
from datetime import datetime, timezone
from bs4 import BeautifulSoup

UA = "KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)"
HEADERS = {"User-Agent": UA}
CRAWL = 6.0
TODAY = datetime.now(timezone.utc).strftime('%Y-%m-%d')

# 1) Robots reverify
ROBOTS_URL = "https://zambialii.org/robots.txt"
time.sleep(CRAWL)
req = urllib.request.Request(ROBOTS_URL, headers=HEADERS)
robots = urllib.request.urlopen(req, timeout=30).read()
robots_sha = hashlib.sha256(robots).hexdigest()
ts = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
robots_path = f'_work/batch_0243_robots_{ts}.txt'
with open(robots_path,'wb') as f: f.write(robots)
print(f"ROBOTS sha256_prefix={robots_sha[:16]} (expect fce67b697ee4ef44 unchanged)")
with open('costs.log','a') as f:
    f.write(json.dumps({'date': TODAY, 'url': ROBOTS_URL, 'bytes': len(robots), 'batch': '0243', 'fetch_n': 1}) + '\n')

# 2) Existing IDs
existing = set()
for fp in glob.glob('records/sis/*/si-zm-*.json'):
    fn = os.path.basename(fp)
    parts = fn.split('-')
    if len(parts) >= 4:
        try:
            yr = int(parts[2]); num = int(parts[3])
            existing.add((yr, num))
        except: pass
print(f"existing SI ids on disk: {len(existing)}")

# 3) Probe alphabet G
fetch_n = 2
def probe_alphabet(letter, fn):
    global fetch_n
    url = f"https://zambialii.org/legislation/?alphabet={letter}"
    print(f"GET {url}")
    time.sleep(CRAWL)
    req = urllib.request.Request(url, headers=HEADERS)
    html = urllib.request.urlopen(req, timeout=45).read()
    p = f'_work/batch_0243_alphabet_{letter}.html'
    with open(p,'wb') as f: f.write(html)
    with open('costs.log','a') as f:
        f.write(json.dumps({'date': TODAY, 'url': url, 'bytes': len(html), 'batch': '0243', 'fetch_n': fetch_n}) + '\n')
    fetch_n += 1
    soup = BeautifulSoup(html, 'html.parser')
    si_links = []; seen=set()
    for a in soup.find_all('a', href=True):
        m = re.match(r'/akn/zm/act/si/(\d{4})/(\d+)(?:/eng@(\d{4}-\d{2}-\d{2}))?', a['href'])
        if m:
            yr = int(m.group(1)); num = int(m.group(2)); eng = m.group(3)
            if (yr,num) in seen: continue
            seen.add((yr,num))
            si_links.append({'yr': yr, 'num': num, 'href': a['href'], 'eng_date': eng, 'title': a.get_text(strip=True)})
    modern = [s for s in si_links if s['yr'] >= 2017]
    novel = [s for s in modern if (s['yr'], s['num']) not in existing]
    print(f"  alphabet={letter}: total={len(si_links)} modern={len(modern)} novel={len(novel)}")
    for n in novel[:20]:
        print(f"    {n['yr']}/{n['num']:>3} ({n['eng_date']}) {n['title'][:80]}")
    out = {'alphabet': letter, 'total_unique': len(si_links), 'modern': len(modern), 'novel': novel}
    with open(f'_work/batch_0243_{letter.lower()}_probe.json','w') as f:
        json.dump(out, f, indent=2)
    return novel

novel_G = probe_alphabet('G', 'g')

# If G sparse, probe U as backup
extra = []
if len(novel_G) < 6:
    print(f"G yielded {len(novel_G)} — probing U as backup")
    extra = probe_alphabet('U', 'u')

print(f"\nfinal counts: G novel={len(novel_G)} U novel={len(extra)}")
print(f"plus 2 year=2025 residuals (1985/45 + 1992/9)")
