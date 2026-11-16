# Prueba: qué devuelve el buscador de Parfumo para los perfumes sin notas.
import json, re, time, sys
sys.path.insert(0, 'scraper')
from notas import get, norm, key
from urllib.parse import quote
d = json.load(open('data/notas.json'))
items = {key(i): i for i in json.load(open('data/perfumes.json'))}
for k, v in d.items():
    if v.get('src'):
        continue
    it = items[k]
    for q in (f"{it['name']} {it['brand']}", norm(it['name']), f"{it['brand']} {it['name']}"):
        h = get('https://www.parfumo.com/s_perfumes_x.php?in=1&filter=' + quote(q)) or ''
        res = re.findall(r'<div class="name">\s*<a href="(https://www\.parfumo\.com/Perfumes/[^"]+)">(.*?)</a>\s*<span class="brand">.*?<a [^>]*>(.*?)</a>', h, re.S)
        print('##', k, '|', q, '->', [(u.split('/Perfumes/')[1], re.sub(r'<[^>]+>', ' ', n).strip(), b) for u, n, b in res[:6]])
        time.sleep(1.2)
