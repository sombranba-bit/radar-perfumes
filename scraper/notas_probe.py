# Prueba de acceso a fuentes de notas (Fragrantica, Parfumo y buscadores) desde Actions; guarda el HTML para inspeccionarlo.
import os, re
from curl_cffi import requests
os.makedirs('probe', exist_ok=True)
s = requests.Session(impersonate='chrome')
urls = {
 'ddg': 'https://html.duckduckgo.com/html/?q=' + requests.utils.quote('site:fragrantica.es Dior Sauvage Eau de Parfum') if hasattr(requests,'utils') else '',
 'bing': 'https://www.bing.com/search?q=site%3Afragrantica.es+Dior+Sauvage+Eau+de+Parfum',
 'frag_es': 'https://www.fragrantica.es/perfume/Dior/Sauvage-Eau-de-Parfum-48100.html',
 'frag_com': 'https://www.fragrantica.com/perfume/Dior/Sauvage-Eau-de-Parfum-48100.html',
 'parfumo': 'https://www.parfumo.com/Perfumes/Dior/Sauvage_Eau_de_Parfum',
 'parfumo_s': 'https://www.parfumo.com/s_perfumes_x.php?in=1&filter=sauvage%20dior',
}
urls['ddg'] = 'https://html.duckduckgo.com/html/?q=site%3Afragrantica.es+Dior+Sauvage+Eau+de+Parfum'
for k, u in urls.items():
    try:
        r = s.get(u, timeout=30)
        open(f'probe/{k}.html', 'w').write(r.text)
        t = re.search(r'<title>(.*?)</title>', r.text, re.S)
        print(k, r.status_code, len(r.text), (t.group(1).strip()[:80] if t else ''), 'Salida' in r.text, 'accord-bar' in r.text)
    except Exception as e:
        print(k, 'ERROR', e)
