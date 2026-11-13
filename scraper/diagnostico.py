"""Prueba a mano: qué navegador simulado deja entrar en Notino y Sephora desde GitHub."""
import json
from curl_cffi import requests as cr

URLS = {
    "notino": "https://www.notino.es/versace/eros-eau-de-toilette-para-hombre/p-11536/",
    "notino_api": "https://www.notino.es/api/navigation/navigation/search?query=versace%20eros",
    "sephora": "https://www.sephora.es/p/eros---eau-de-toilette-P3195008.html",
    "sephora_busca": "https://www.sephora.es/buscar/?q=versace%20eros",
}
out = {}
for imp in ["chrome", "chrome131", "chrome_android", "safari", "safari_ios", "edge", "firefox"]:
    for k, u in URLS.items():
        try:
            r = cr.get(u, impersonate=imp, timeout=25, headers={"Accept-Language": "es-ES,es;q=0.9"})
            t = r.text
            out[f"{imp} {k}"] = f"{r.status_code} {len(t)//1024}kB ld={t.count('application/ld+json')} eur={t.count('€')}"
        except Exception as e:
            out[f"{imp} {k}"] = "error " + type(e).__name__
print(json.dumps(out, indent=1))
