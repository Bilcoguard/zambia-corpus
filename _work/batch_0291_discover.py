"""Batch 0291 — Phase 4 / sis_corporate sub-phase probe.

Inherited from b0290: acts_in_force chronological-first sweep at upstream
steady-state through 2026/11. Per priority_order, next sub-phase is
sis_corporate. Discovery target: zambialii alphabet=C SIs (Companies,
Corporate Insolvency, Co-operative, Citizens Economic Empowerment) plus
alphabet=B (Banking), I (Insurance), P (Pensions), S (Securities), with
hierarchical preference toward Companies/Corporate Insolvency since the
on-disk sis_corporate cluster (6 records) already has 3 Companies-Act
children + 1 Corporate-Insolvency Act child. Modern (>=2017) only.

Probe-only — no record writes. Output: _work/batch_0291_corporate_probe.json
"""
import sys, os, json, hashlib, time, urllib.request, re, glob
from datetime import datetime, timezone
from bs4 import BeautifulSoup

UA = "KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)"
HEADERS = {"User-Agent": UA}
CRAWL = 6.0  # zambialii robots Crawl-delay 5s + 1s margin

# Robots re-verify first
ROBOTS_URL = "https://zambialii.org/robots.txt"
time.sleep(CRAWL)
req = urllib.request.Request(ROBOTS_URL, headers=HEADERS)
robots = urllib.request.urlopen(req, timeout=30).read()
robots_sha = hashlib.sha256(robots).hexdigest()
print(f"robots.txt sha256={robots_sha}")
expected = "fce67b697ee4ef44e0694134e23108c2701b5e7661eed885013efb9b75dcd8f0"
assert robots_sha == expected, f"robots.txt drift: {robots_sha} != {expected}"
with open('costs.log','a') as f:
    f.write(json.dumps({'date': datetime.now(timezone.utc).strftime('%Y-%m-%d'), 'url': ROBOTS_URL, 'bytes': len(robots), 'batch':'0291','kind':'probe'}) + '\n')

# Build existing on-disk SI key set
existing = set()
for f in glob.glob('records/sis/**/si-zm-*.json', recursive=True) + glob.glob('records/sis/si-zm-*.json'):
    fn = os.path.basename(f)
    parts = fn.split('-')
    if len(parts) >= 4:
        try:
            yr = int(parts[2]); num = int(parts[3])
            existing.add((yr, num))
        except: pass
print(f"existing SI keys on disk: {len(existing)}")

# Probe alphabet=C (priority for sis_corporate)
ALPHABETS = ['C']
all_results = {}
for alpha in ALPHABETS:
    url = f"https://zambialii.org/legislation/?alphabet={alpha}"
    print(f"GET {url}")
    time.sleep(CRAWL)
    req = urllib.request.Request(url, headers=HEADERS)
    html = urllib.request.urlopen(req, timeout=45).read()
    sha = hashlib.sha256(html).hexdigest()
    out = f'_work/batch_0291_alphabet_{alpha}.html'
    with open(out,'wb') as f: f.write(html)
    print(f"  saved {out} sha256={sha[:16]} len={len(html)}")
    with open('costs.log','a') as f:
        f.write(json.dumps({'date': datetime.now(timezone.utc).strftime('%Y-%m-%d'), 'url': url, 'bytes': len(html), 'batch':'0291','kind':'probe'}) + '\n')

    soup = BeautifulSoup(html, 'html.parser')
    si_links = []
    seen = set()
    for a in soup.find_all('a', href=True):
        h = a['href']
        m = re.match(r'/akn/zm/act/si/(\d{4})/(\d+)(?:/eng@(\d{4}-\d{2}-\d{2}))?', h)
        if m:
            yr = int(m.group(1)); num = int(m.group(2)); eng = m.group(3)
            key = (yr, num)
            if key in seen: continue
            seen.add(key)
            title = a.get_text(strip=True)
            si_links.append({'yr': yr, 'num': num, 'href': h, 'eng_date': eng, 'title': title})
    # Filter modern + novel
    modern = [s for s in si_links if s['yr'] >= 2017]
    novel = [s for s in modern if (s['yr'], s['num']) not in existing]
    print(f"  alphabet={alpha}: total={len(si_links)} modern={len(modern)} novel={len(novel)}")
    all_results[alpha] = {
        'total': len(si_links),
        'modern': len(modern),
        'novel': novel,
    }
    # Show top novel candidates by year desc
    novel_sorted = sorted(novel, key=lambda x: (-x['yr'], x['num']))
    for n in novel_sorted[:25]:
        print(f"    {n['yr']}/{n['num']:>3} ({n['eng_date']}) {n['title'][:90]}")

# Identify "corporate-themed" novel picks: titles that mention
# Companies, Corporate, Co-operative, Citizens Economic Empowerment.
CORP_PAT = re.compile(r'\b(Companies|Corporate|Co-operative|Cooperative|Citizens Economic Empowerment)\b', re.I)
candidates = []
for alpha, data in all_results.items():
    for n in data['novel']:
        if CORP_PAT.search(n['title']):
            candidates.append({**n, 'alpha':alpha})
candidates_sorted = sorted(candidates, key=lambda x: (-x['yr'], x['num']))

print()
print(f"sis_corporate candidates (modern, novel, corporate-themed): {len(candidates_sorted)}")
for c in candidates_sorted[:25]:
    print(f"  {c['yr']}/{c['num']:>3} {c['title'][:100]}")

with open('_work/batch_0291_corporate_probe.json','w') as f:
    json.dump({
        'alphabets': all_results,
        'corporate_candidates': candidates_sorted,
        'existing_count': len(existing),
        'robots_sha': robots_sha,
    }, f, indent=2)
print("saved _work/batch_0291_corporate_probe.json")
