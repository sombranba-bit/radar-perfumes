# Prueba: por qué Sephora no da precio en muchas fichas (se imprime lo que ve el lector).
import json, re, sys, time
sys.path.insert(0, 'scraper')
from radar import make_session, extract, SEPHORA_RE
get = make_session()
d = json.load(open('data/perfumes.json'))
today = time.strftime('%Y-%m-%d')
bad = [i for i in d if i.get('urls', {}).get('sephora') and (i['prices'].get('sephora') or {}).get('d', '') < '2026-11-18'][:8]
good = [i for i in d if (i['prices'].get('sephora') or {}).get('d', '') >= '2026-11-19'][:2]
print('sin leer', len([i for i in d if i.get('urls', {}).get('sephora') and (i['prices'].get('sephora') or {}).get('d', '') < '2026-11-18']), 'de', len([i for i in d if i.get('urls', {}).get('sephora')]))
for it in good + bad:
    u = it['urls']['sephora']
    r = get(u)
    t = r.text.replace('\\"', '"')
    fm = re.findall(r'"format":"(\w+)"', t)
    ppu = re.findall(r'"pricePerUnit":"([^"]+)"', t)[:6]
    sizes = re.findall(r'(\d{2,3})\s?ml', t, re.I)
    print('##', it['id'], r.status_code, len(r.text), 'final=', getattr(r, 'url', '')[:90], 'extract=', extract(r.text, it['ml'], u), 'formats=', sorted(set(fm)), 'ppu=', ppu, 'ml=', sorted(set(sizes))[:10], 'matches=', SEPHORA_RE.findall(t)[:4])
    k = t.find('"pricePerUnit"')
    print('   ', re.sub(r'\s+', ' ', t[max(0, k - 600):k + 200]) if k >= 0 else re.sub(r'\s+', ' ', t[:300]))
    time.sleep(1.5)
