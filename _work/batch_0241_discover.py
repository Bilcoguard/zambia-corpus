"""Batch 0241 alphabet H probe — discover modern (>=2017) SIs starting with H,
filter out HEAD-existing IDs.
"""
import sys, os, json, hashlib, time, urllib.request, re
from datetime import datetime, timezone
from bs4 import BeautifulSoup

UA = "KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)"
HEADERS = {"User-Agent": UA}
CRAWL = 6.0

PROBE_URL = "https://zambialii.org/legislation/?alphabet=H"
print(f"GET {PROBE_URL}")
time.sleep(CRAWL)
req = urllib.request.Request(PROBE_URL, headers=HEADERS)
html = urllib.request.urlopen(req, timeout=45).read()
sha = hashlib.sha256(html).hexdigest()
out = '_work/batch_0241_alphabet_H.html'
with open(out,'wb') as f: f.write(html)
print(f"saved {out} sha256={sha[:16]} len={len(html)}")

# Append to costs.log
with open('costs.log','a') as f:
    f.write(json.dumps({'date': datetime.now(timezone.utc).strftime('%Y-%m-%d'), 'url': PROBE_URL, 'bytes': len(html), 'batch': '0241', 'fetch_n': 691}) + '\n')

soup = BeautifulSoup(html, 'html.parser')
# Find all akn/zm/act/si/ links
si_links = []
seen_yr_num = set()
for a in soup.find_all('a', href=True):
    h = a['href']
    m = re.match(r'/akn/zm/act/si/(\d{4})/(\d+)(?:/eng@(\d{4}-\d{2}-\d{2}))?', h)
    if m:
        yr = int(m.group(1)); num = int(m.group(2)); eng = m.group(3)
        key = (yr, num)
        if key in seen_yr_num: continue
        seen_yr_num.add(key)
        title = a.get_text(strip=True)
        si_links.append({'yr': yr, 'num': num, 'href': h, 'eng_date': eng, 'title': title})

# Filter modern (>=2017) and dedupe vs HEAD
import glob
existing = set()
for f in glob.glob('records/sis/*/si-zm-*.json'):
    fn = os.path.basename(f)
    parts = fn.split('-')
    if len(parts) >= 4:
        try:
            yr = int(parts[2]); num = int(parts[3])
            existing.add((yr, num))
        except: pass

modern = [s for s in si_links if s['yr'] >= 2017]
novel = [s for s in modern if (s['yr'], s['num']) not in existing]
print(f"Total SI links: {len(si_links)}, modern: {len(modern)}, novel: {len(novel)}")
for n in novel[:15]:
    print(f"  {n['yr']}/{n['num']:>3} ({n['eng_date']}) {n['title'][:80]}")

with open('_work/batch_0241_h_probe.json','w') as f:
    json.dump({'alphabet':'H','total_unique':len(si_links),'modern':len(modern),'novel':novel,'existing_in_corpus_total':len(existing)}, f, indent=2)
print("saved _work/batch_0241_h_probe.json")
