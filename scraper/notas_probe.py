# Prueba: candidatos de Parfumo para los perfumes que siguen sin notas, con varias búsquedas.
import re, sys, time
sys.path.insert(0, 'scraper')
from notas import get as pget
from urllib.parse import quote
Q = ['Fakhar Rose', 'Fakhar Lattafa', 'Opium Yves Saint Laurent', 'Opium 2009', 'Opium Eau de Parfum', 'Carolina Herrera Eau de Toilette',
     'Carolina Herrera 1988', 'K by Dolce Gabbana Eau de Parfum', 'K Dolce Gabbana', 'Le Male Lover', 'Pistachio Gelato', 'Musk Therapy']
for q in Q:
    h = pget('https://www.parfumo.com/s_perfumes_x.php?in=1&filter=' + quote(q)) or ''
    res = re.findall(r'<div class="name">\s*<a href="https://www\.parfumo\.com/Perfumes/([^"]+)">(.*?)</a>\s*<span class="brand">.*?<a [^>]*>(.*?)</a>', h, re.S)
    print('%%', q, '->', [(u, re.sub(r'<[^>]+>', ' ', n).strip()[:50], b) for u, n, b in res[:8]], flush=True)
    time.sleep(1.2)
