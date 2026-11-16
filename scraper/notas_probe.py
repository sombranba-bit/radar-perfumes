# Prueba: qué tiendas publican la pirámide (notas de salida, corazón y fondo) en sus fichas.
import json, re
from curl_cffi import requests
s = requests.Session(impersonate='chrome')
d = json.load(open('data/perfumes.json'))
picks = [i for i in d if i['name'] in ('Sauvage', 'Bleu de Chanel', 'Good Girl', 'Aventus', 'Libre')][:5]
def txt(h):
    h = re.sub(r'<script.*?</script>|<style.*?</style>', ' ', h, flags=re.S)
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', h))
for it in picks:
    for shop, u in it['urls'].items():
        if shop in ('idealo', 'notino'): continue
        try:
            r = s.get(u, timeout=25)
            t = txt(r.text)
            m = re.search(r'(?i)notas? de salida|notas? altas|salida:', t)
            print('##', it['brand'], it['name'], shop, r.status_code, bool(m), (t[max(0, m.start()-80):m.start()+420] if m else ''))
        except Exception as e:
            print('##', it['name'], shop, 'ERR', e)
