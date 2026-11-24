# Prueba: buscador de Avenida (Shopify).
import json, re, sys, time
sys.path.insert(0, 'scraper')
from radar import make_session, best_link
get = make_session()
d = {i['id']: i for i in json.load(open('data/perfumes.json'))}
for pid in ['versace-eros-edp-100', 'dior-sauvage-edt-100', 'lancome-la-vie-est-belle-edp-100']:
    it = d[pid]
    q = '+'.join(f"{it['brand']} {it['name']}".split())
    for tpl in ['https://www.perfumeriasavenida.com/search?q={q}&type=product', 'https://www.perfumeriasavenida.com/search?q={q}',
                'https://www.perfumeriasavenida.com/search/suggest.json?q={q}&resources[type]=product&resources[limit]=10']:
        r = get(tpl.format(q=q))
        t = r.text or ''
        print('%%', pid, tpl[40:90], r.status_code, len(t) // 1024, 'kb', 'products:', len(re.findall(r'/products/', t)), re.findall(r'/products/[a-z0-9-]+', t)[:4], 'best', best_link(t, tpl, it), flush=True)
        time.sleep(1.5)
