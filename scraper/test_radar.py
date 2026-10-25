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
assert it["prices"]["notino"] == {"p": 52.5, "d": "2026-10-25", "auto": True, "gh": True, "stock": False}
assert it["prices"]["laguna"]["p"] == 45.0          # 9,99 € descartado por absurdo
assert stats["sephora"]["bloqueada"] == 1 and stats["laguna"]["dudoso"] == 1 and "primor" not in stats
assert it["history"] == [] and it["checked"]        # agotado no entra en el histórico
print("OK: pasada simulada")

# 9. Limpieza de precios disparatados y bandas por método
it = {"prices": {"a": {"p": 75.95, "auto": True}, "b": {"p": 74.0, "auto": True}, "c": {"p": 132.1, "auto": True, "gh": True}, "n": {"p": 130, "auto": True, "d": "2026-10-12"}, "m": {"p": 76, "auto": False}},
      "history": [{"d": "x", "s": "c", "p": 132.1}, {"d": "x", "s": "a", "p": 75.95}]}
assert radar.clean_outliers(it, "x") == ["c"] and "c" not in it["prices"] and "m" in it["prices"] and "n" in it["prices"] and len(it["history"]) == 1
assert not plausible(64.95, 94.95, "texto") and plausible(64.95, 94.95, "jsonld") and not plausible(30, None, "texto")
print("OK: limpieza")

# 10. Prueba de tiendas
ok = radar.probe_page(lambda u: R(200, "<title>Boss</title>" + "Boss Bottled 49,95 € " * 4), "https://t.es")
bl = radar.probe_page(lambda u: R(403, "Access denied"), "https://t.es")
cap = radar.probe_page(lambda u: R(200, "<div class=g-recaptcha>captcha</div>"), "https://t.es")
assert ok["estado"] == "con precios" and bl["estado"] == "bloqueada" and cap["estado"] == "bloqueada"
print("OK: prueba de tiendas")

# 11. Casos reales vistos en GitHub
lf = ld({"@type": "ProductGroup", "hasVariant": [{"@type": "Product", "name": "Bleu Noir Eau de Parfum - 100ml",
      "description": "Disponible también en 50 ml", "offers": {"@type": "Offer", "price": "66.90", "priceCurrency": "EUR"}}]})
assert extract(lf + "<span>Coste de entrega: 3,99€</span>", 100, "https://www.lookfantastic.es/x/12127921.html")[0] == 66.9
mag = ('<script>{"attributes":{"93":{"options":[{"id":"1","label":"50 ml","products":["126295"]},{"id":"2","label":"100 ml","products":["126294"]}]}},'
       '"optionPrices":{"126295":{"finalPrice":{"amount":47.95}},"126294":{"finalPrice":{"amount":59.95}}}}</script>')
assert extract(ld({"@type": "Product", "name": "Explorer EDP", "offers": [{"price": 47.95, "priceCurrency": "EUR"}]}) + mag, 100, "https://www.perfumeriasavenida.com/explorer-edp-mont-blanc") == (59.95, None, "variantes")
th1 = '<div data-vue3=\'%s\'></div>' % json.dumps({"props": {"thread": {"threadId": "77", "title": "Hugo Man EDT 125 ml", "price": 29.9, "isExpired": True}}})
assert parse_chollos(th1)[0]["expired"] is True and parse_chollos(th1)[0]["id"] == 77
assert parse_chollos('<a href="https://www.chollometro.com/ofertas/hugo-man-edt-125ml-2042605" data-t=\'threadLink\'>')[0]["t"] == "Hugo man edt 125ml"
print("OK: casos reales")

# 12. Buscar la ficha en una página de resultados
res = ('<a href="/es/c/perfumes/01">Perfumes</a><a href="/es/p/5010218001">BOSS Bottled Night Eau de Toilette</a>'
       '<a href="/es/p/3001055018">HUGO BOSS Boss Bottled Eau de Toilette 100 ml</a><a href="https://otra.com/p/boss-bottled">x</a>')
it = {"id": "hb", "brand": "Hugo Boss", "name": "Boss Bottled", "conc": "EDT", "ml": 100}
assert radar.best_link(res, "https://www.douglas.es/es/search?q={q}", it) == "https://www.douglas.es/es/p/3001055018"
assert radar.best_link('<a href="/es/p/1">Boss Bottled Night 100 ml</a>', "https://www.douglas.es/es/search?q={q}", it) is None
assert radar.best_link("<a href='/x'>nada</a>", "https://www.douglas.es/es/search?q={q}", it) is None
seen = []
it2 = dict(it, urls={"lookfantastic": "https://ya.es/x"})
n = radar.discover(it2, lambda u: (seen.append(u), R(200, res))[1], "2026-10-25", 2)
assert n == 2 and it2["urls"]["douglas"].endswith("3001055018") and "lookfantastic" not in seen[0] and len(seen) == 2
assert radar.discover(it2, lambda u: R(200, res), "2026-10-26", 5) == 0 or it2["buscado"]
print("OK: buscar fichas")

# 13. Precio + precio por 100 ml (tamaño deducido)
douglas = ('<span aria-label="precio de venta recomendado 78,99 €">78,99 €</span><span aria-label="Actualmente 45,99 €">45,99 €</span>'
           '<span aria-label="Precio 153,30 € por 100 mililitro">153,30 €<!-- --> / <!-- -->100<!-- --> <!-- -->ml</span>'
           '<span>97,00 €</span><span aria-label="Actualmente 55,99 €">55,99 €</span><span>111,98 € / 100 ml</span>')
assert extract(douglas, 30, "https://www.douglas.es/es/p/1")[:1] == (45.99,) and extract(douglas, 50, "https://www.douglas.es/es/p/1")[0] == 55.99
pc = ('<div class="contPrecioNuevo"> 74,81 € </div><div class="pricePer100">100 ml / 37,40 €</div>'
      '<div class="contPrecioNuevo"> 50,55 € </div><div class="pricePer100">100 ml / 50,55 €</div>'
      '<div class="contPrecioNuevo"> 37,81 € </div><div class="pricePer100">100 ml / 126,03 €</div>')
assert extract(ld({"@type": "Product", "name": "BOSS BOTTLED", "offers": [{"price": "74.81", "priceCurrency": "EUR"}]}) + pc, 100, "https://www.perfumesclub.com/es/x/p_23010/")[0] == 50.55
assert extract(pc, 30, "https://x")[0] == 37.81 and extract(pc, 200, "https://x")[0] == 74.81
assert extract('<b>100 ml / 126,03 €</b>', 100, "https://x")[0] is None
print("OK: precio por 100 ml")

# 14. Douglas: el precio por 100 ml aparece dos veces y no debe pasar por precio de frasco
dg = ('<span aria-label="Actualmente 51,29 €">51,29 €</span><span aria-label="Precio 341,93 € por 100 mililitro">341,93 €<!-- --> / <!-- -->100<!-- --> <!-- -->ml</span>'
      '<span aria-label="Actualmente 77,00 €">77,00 €</span><span aria-label="Precio 102,67 € por 100 mililitro">102,67 €<!-- --> / <!-- -->100<!-- --> <!-- -->ml</span>')
assert extract(dg, 100, "https://www.douglas.es/es/p/1")[0] is None and extract(dg, 75, "https://www.douglas.es/es/p/1")[0] == 77.0 and extract(dg, 15, "https://x")[0] == 51.29
# 15. Avenida: bloques por tamaño
av = ''.join('<div class="g" data-child-id="%s" style="display: none;"><div class="main-image"><img src="x.jpg" alt="Terre D&#039;Hermès EDT | %s ml"></div></div>' % (c, m) for c, m in (("126350", 50), ("126349", 100)))
av += ''.join('<div class="prices" data-child-id="%s" style="display: none;"><span class="original-price">%s€</span><span class="current-price">%s€</span></div>' % x for x in (("126350", "79,00", "61,95"), ("126349", "112,00", "87,95")))
assert extract(av, 100, "https://www.perfumeriasavenida.com/terre-d-hermes-edt-hermes")[:1] == (87.95,) and extract(av, 50, "https://x")[0] == 61.95
print("OK: Douglas y Avenida")
