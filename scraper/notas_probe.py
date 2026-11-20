# Prueba: buscadores de Paco, Laguna, Avenida y Parejo; y Parfumo para los perfumes nuevos sin notas.
import json, re, sys, time
sys.path.insert(0, 'scraper')
from radar import make_session, best_link
from notas import get as pget, norm, key
from urllib.parse import quote
get = make_session()
d = json.load(open('data/perfumes.json'))
it = next(i for i in d if i['id'] == 'versace-eros-edp-100')
CAND = {
 'paco': ['https://www.pacoperfumerias.com/search?q={q}', 'https://www.pacoperfumerias.com/buscar?q={q}'],
 'laguna': ['https://www.perfumeriaslaguna.com/catalogsearch/result/?q={q}', 'https://www.perfumeriaslaguna.com/search?q={q}'],
 'avenida': ['https://www.perfumeriasavenida.com/busqueda?controller=search&s={q}', 'https://www.perfumeriasavenida.com/search?q={q}', 'https://www.perfumeriasavenida.com/catalogsearch/result/?q={q}'],
 'parejo': ['https://www.joyeriaparejo.com/busqueda?s={q}', 'https://www.joyeriaparejo.com/search?q={q}', 'https://www.joyeriaparejo.com/catalogsearch/result/?q={q}', 'https://www.joyeriaparejo.com/?s={q}'],
}
n = json.load(open('data/notas.json'))
for i in d:
    k = key(i)
    if k in n and n[k].get('src') or i['id'] < '':
        continue
    if k not in n:
        continue
    h = pget('https://www.parfumo.com/s_perfumes_x.php?in=1&filter=' + quote(norm(i['name']) + ' ' + norm(i['brand']))) or ''
    res = re.findall(r'<div class="name">\s*<a href="https://www\.parfumo\.com/Perfumes/([^"]+)">(.*?)</a>\s*<span class="brand">.*?<a [^>]*>(.*?)</a>', h, re.S)
    print('%%', k, '->', [(u, re.sub(r'<[^>]+>', ' ', nn).strip(), b) for u, nn, b in res[:5]])
    time.sleep(1.2)
