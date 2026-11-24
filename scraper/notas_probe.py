# Prueba: fichas de Makeup y El Corte Inglés (precio del tamaño exacto) y por qué fallan Avenida y Sephora.
import json, re, sys, time
sys.path.insert(0, 'scraper')
from radar import make_session, extract, jsonld_offers, CONC_WORDS, PRICE_RE
get = make_session()
d = {i['id']: i for i in json.load(open('data/perfumes.json'))}
IDS = ['versace-eros-edp-100', 'dior-sauvage-edt-100', 'lancome-la-vie-est-belle-edp-100', 'rabanne-1-million-edt-100', 'carolina-herrera-good-girl-edp-80']


def show(tag, url, ml):
    try:
        r = get(url)
    except Exception as e:
        print('%%', tag, url, 'error', type(e).__name__, flush=True)
        return
    t = r.text or ''
    got = extract(t, ml, url)
    print('%%', tag, url, r.status_code, len(t) // 1024, 'kb', getattr(r, 'url', '')[:120], '->', got, flush=True)
    if not got[0]:
        print('%%   jsonld', [(p, a[:60], b[:60]) for p, a, b, s in jsonld_offers(t)][:6])
        print('%%   euros', PRICE_RE.findall(t)[:12])
        for k in ('"price"', 'itemprop="price"', 'data-price', 'finalPrice', 'og:price'):
            i = t.find(k)
            if i >= 0:
                print('%%   ', k, re.sub(r'\s+', ' ', t[max(0, i - 150): i + 250]))
        print('%%   titulo', re.findall(r'<title[^>]*>(.*?)</title>', t, re.S)[:1], 'inicio', re.sub(r'\s+', ' ', t[:300]))
    time.sleep(1.5)


for pid in IDS:
    it = d[pid]
    q = '+'.join(re.sub(r'[^\w]+', ' ', f"{it['brand']} {it['name']} {CONC_WORDS.get(it.get('conc'), '')}").split())
    # Makeup: primera ficha del buscador
    try:
        t = get('https://makeup.es/search/?q=' + q).text
        m = re.search(r'href="(/product/\d+/)"', t)
        if m:
            show('makeup', 'https://makeup.es' + m.group(1), it['ml'])
    except Exception as e:
        print('%% makeup error', e)
    # El Corte Inglés: fichas del tamaño pedido
    try:
        t = get('https://www.elcorteingles.es/search-nwx/1/?s=' + q).text
        links = sorted(set(re.findall(r'href="(/perfumeria/A[^"]*?-%d-ml/?)"' % it['ml'], t)))
        print('%% eci enlaces %d ml' % it['ml'], pid, links[:5], flush=True)
        if links:
            show('eci', 'https://www.elcorteingles.es' + links[0], it['ml'])
    except Exception as e:
        print('%% eci error', e)
    for shop in ('avenida', 'sephora'):
        if it['urls'].get(shop):
            show(shop, it['urls'][shop], it['ml'])
