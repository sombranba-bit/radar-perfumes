# Prueba: buscadores de tiendas que aún no buscan solas (Laguna, Avenida, Sabina, Douglas, Makeup, El Corte Inglés, Primor, Druni).
import json, sys, time
sys.path.insert(0, 'scraper')
from radar import make_session, best_link, CONC_WORDS
import re
get = make_session()
d = {i['id']: i for i in json.load(open('data/perfumes.json'))}
IDS = ['versace-eros-edp-100', 'dior-sauvage-edt-100', 'lancome-la-vie-est-belle-edp-100', 'paco-rabanne-1-million-edt-100' if 'paco-rabanne-1-million-edt-100' in d else 'rabanne-1-million-edt-100', 'carolina-herrera-good-girl-edp-80']
CAND = {
 'laguna': ['https://www.perfumeriaslaguna.com/catalogsearch/result/?q={q}'],
 'avenida': ['https://www.perfumeriasavenida.com/catalogsearch/result/?q={q}'],
 'sabina': ['https://www.sabina.com/search?q={q}', 'https://www.sabina.com/es/search?q={q}', 'https://www.sabina.com/catalogsearch/result/?q={q}'],
 'douglas': ['https://www.douglas.es/es/search?q={q}'],
 'makeup': ['https://makeup.es/search/?q={q}'],
 'eci': ['https://www.elcorteingles.es/search-nwx/1/?s={q}', 'https://www.elcorteingles.es/perfumeria/search-nwx/1/?s={q}'],
 'primor': ['https://www.primor.eu/es_es/catalogsearch/result/?q={q}'],
 'druni': ['https://www.druni.es/catalogsearch/result/?q={q}', 'https://www.druni.es/buscar?q={q}'],
}
for shop, tpls in CAND.items():
    for tpl in tpls:
        hits = 0
        for pid in IDS:
            it = d.get(pid)
            if not it:
                continue
            q = '+'.join(re.sub(r'[^\w]+', ' ', f"{it['brand']} {it['name']} {CONC_WORDS.get(it.get('conc'), '')}").split())
            try:
                r = get(tpl.format(q=q))
                code, t = r.status_code, r.text or ''
            except Exception as e:
                code, t = type(e).__name__, ''
            link = best_link(t, tpl, it) if code == 200 else None
            hits += bool(link)
            print('%%', shop, tpl.split('?')[0], pid, code, len(t) // 1024, 'kb', link, flush=True)
            time.sleep(1.2)
        print('%%=', shop, tpl, 'aciertos', hits, flush=True)
