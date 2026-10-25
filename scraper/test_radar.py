"""Pruebas del extractor con páginas de ejemplo (python scraper/test_radar.py)."""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from radar import extract, parse_chollos, to_float, plausible

def ld(o): return '<script type="application/ld+json">' + json.dumps(o) + '</script>'

# 1. Varias ofertas, cada una con su tamaño
multi = ld({"@type": "Product", "name": "Boss Bottled EDT", "offers": [
    {"@type": "Offer", "name": "50 ml", "price": "39.95", "priceCurrency": "EUR", "availability": "https://schema.org/InStock"},
    {"@type": "Offer", "name": "100 ml", "price": "52.50", "priceCurrency": "EUR", "availability": "https://schema.org/OutOfStock"},
    {"@type": "Offer", "name": "200 ml", "price": "74.90", "priceCurrency": "EUR"}]})
assert extract(multi, 100, "https://x.es/boss") == (52.5, False, "jsonld")
assert extract(multi, 200, "https://x.es/boss")[0] == 74.9

# 2. ProductGroup con variantes
group = ld({"@type": "ProductGroup", "name": "Sauvage", "hasVariant": [
    {"@type": "Product", "name": "Sauvage EDT 60 ml", "offers": {"@type": "Offer", "price": 89, "priceCurrency": "EUR"}},
    {"@type": "Product", "name": "Sauvage EDT 100 ml", "offers": {"@type": "Offer", "price": 112.5, "priceCurrency": "EUR"}}]})
assert extract(group, 100, "https://x.es/sauvage")[0] == 112.5

# 3. Un solo producto sin tamaño en la oferta: solo vale si la URL lo dice
one = ld({"@type": "Product", "name": "Le Male", "offers": {"@type": "Offer", "price": "61,95", "priceCurrency": "EUR"}})
assert extract(one, 125, "https://brasty.es/le-male-edt-125-ml")[0] == 61.95
assert extract(one, 125, "https://x.es/le-male")[0] is None

# 4. Respaldo por texto: "100 ml" seguido de precio; no confundir con el tamaño vecino
txt = "<div>Tamaño <b>50 ml</b> 41,20 €</div><div><b>100 ml</b> <span>58,90&nbsp;€</span></div>"
assert extract(txt, 100, "https://x.es/p")[:1] == (58.9,)
assert extract(txt, 200, "https://x.es/p")[0] is None

# 5. Moneda distinta se ignora
usd = ld({"@type": "Product", "name": "Aventus 100 ml", "offers": {"price": 300, "priceCurrency": "USD"}})
assert extract(usd, 100, "https://x.com/a")[0] is None

# 6. Números y control de saltos absurdos
assert to_float("1.234,56") == 1234.56 and to_float("44,6") == 44.6
assert plausible(50, 48) and not plausible(10, 48) and not plausible(200, 48) and plausible(30, None)

# 7. Chollometro (formato data-vue3 de Pepper)
import html
th = {"props": {"thread": {"threadId": 123, "title": "Boss Bottled 200 ml", "price": 49.9, "isExpired": False,
      "merchant": {"merchantName": "Notino"}, "shareableLink": "https://www.chollometro.com/ofertas/boss-123"}}}
page = '<article data-vue3="%s"></article>' % html.escape(json.dumps(th), quote=True)
assert parse_chollos(page) == [{"id": 123, "t": "Boss Bottled 200 ml", "p": 49.9, "shop": "Notino", "url": "https://www.chollometro.com/ofertas/boss-123", "expired": False}]
fb = '<a href="https://www.chollometro.com/ofertas/yara-lattafa-100ml-456" title="Yara 100 ml">x</a>'
assert parse_chollos(fb)[0]["id"] == 456
print("OK: todas las pruebas pasan")

# 8. Pasada completa de un perfume con respuestas simuladas
import radar
radar.time.sleep = lambda s: None
class R:
    def __init__(s, code, text): s.status_code, s.text = code, text
pages = {"https://a.es/boss": R(200, multi), "https://b.es/boss": R(403, ""),
         "https://c.es/boss-100ml": R(200, ld({"@type": "Product", "offers": {"price": "9.99", "priceCurrency": "EUR"}}))}
it = {"brand": "Hugo Boss", "name": "Boss Bottled", "ml": 100, "urls": {"notino": "https://a.es/boss", "sephora": "https://b.es/boss", "laguna": "https://c.es/boss-100ml", "primor": "https://p.es"},
      "prices": {"laguna": {"p": 45.0, "d": "2026-10-01"}}, "history": []}
stats = {}
radar.update_perfume(it, lambda u: pages[u], stats, "2026-10-25")
assert it["prices"]["notino"] == {"p": 52.5, "d": "2026-10-25", "auto": True, "stock": False}
assert it["prices"]["laguna"]["p"] == 45.0          # 9,99 € descartado por absurdo
assert stats["sephora"]["bloqueada"] == 1 and stats["laguna"]["dudoso"] == 1 and "primor" not in stats
assert it["history"] == [] and it["checked"]        # agotado no entra en el histórico
print("OK: pasada simulada")
