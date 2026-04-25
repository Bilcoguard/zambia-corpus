"""Batch 0243 discovery 2 - probe X/Y/Z + year=2024 listings.

Carries the existing-set forward and adds further probe coverage.
"""
import os, json, hashlib, time, urllib.request, re, glob
from datetime import datetime, timezone
from bs4 import BeautifulSoup

UA = "KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)"
HEADERS = {"User-Agent": UA}
CRAWL = 6.0
TODAY = datetime.now(timezone.utc).strftime('%Y-%m-%d')

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

fetch_n = 4  # continuing from batch_0243_discover.py (used 1 robots + 2 alphabet)

def probe_url(url, key, save_name):
    global fetch_n
    print(f"GET {url}")
    time.sleep(CRAWL)
    req = urllib.request.Request(url, headers=HEADERS)
    html = urllib.request.urlopen(req, timeout=45).read()
    p = f'_work/batch_0243_{save_name}.html'
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
    print(f"  {key}: total={len(si_links)} modern={len(modern)} novel={len(novel)}")
    for n in novel[:20]:
        print(f"    {n['yr']}/{n['num']:>3} ({n['eng_date']}) {n['title'][:80]}")
    out = {'key': key, 'total_unique': len(si_links), 'modern': len(modern), 'novel': novel}
    with open(f'_work/batch_0243_{save_name}_probe.json','w') as f:
        json.dump(out, f, indent=2)
    return novel

candidates = []
for letter in ('X','Y','Z'):
    nv = probe_url(f"https://zambialii.org/legislation/?alphabet={letter}", f"alphabet={letter}", f"alphabet_{letter}")
    candidates += [(letter, n) for n in nv]

# Year listings - try 2024 (most recent unprobed year)
nv = probe_url("https://zambialii.org/legislation/?year=2024", "year=2024", "year2024")
candidates += [('y2024', n) for n in nv]

# Also try 2023 if needed
if len(candidates) < 6:
    nv = probe_url("https://zambialii.org/legislation/?year=2023", "year=2023", "year2023")
    candidates += [('y2023', n) for n in nv]

# Also try 2026 to be thorough
if len(candidates) < 6:
    nv = probe_url("https://zambialii.org/legislation/?year=2026", "year=2026", "year2026")
    candidates += [('y2026', n) for n in nv]

print(f"\ntotal cumulative candidates: {len(candidates)}")
for src, n in candidates:
    print(f"  [{src}] {n['yr']}/{n['num']:>3} ({n['eng_date']}) {n['title'][:80]}")
