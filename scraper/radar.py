"""Pasada de precios del Radar de Perfumes (se ejecuta en GitHub Actions).

Lee data/perfumes.json, visita las fichas guardadas (urls) de los perfumes
revisados hace más tiempo, saca el precio del tamaño exacto y actualiza
prices / history / checked. Después lee las categorías de perfumes de
Chollometro y guarda data/chollos.json. Deja un resumen en data/estado.json.
"""
import html as htmllib
import json
import os
import random
import re
import statistics
import sys
import time
import unicodedata
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
TZ = ZoneInfo("Europe/Madrid")
BATCH = int(os.environ.get("RADAR_BATCH", "35"))      # perfumes por pasada
MANUAL = {"coqueteo", "marvimundo", "arenal", "primor", "druni", "julia", "eci", "amazon"}

PRICE_RE = re.compile(r"(\d{1,4}(?:[.\s]\d{3})*(?:[.,]\d{1,2})?)\s*(?:€|&euro;|EUR)")
ML_RE = re.compile(r"(\d{2,3})\s?ml\b", re.I)


def now_iso():
    return datetime.now(TZ).isoformat(timespec="seconds")


def to_float(s):
    if isinstance(s, (int, float)):
        return float(s)
    s = str(s).strip().replace("\xa0", "").replace(" ", "")
    if "," in s and "." in s:          # 1.234,56 -> 1234.56
        s = s.replace(".", "").replace(",", ".")
    else:
        s = s.replace(",", ".")
    try:
        return float(s)
    except ValueError:
        return None


# ---------------------------------------------------------------- extracción
def _walk(o):
    if isinstance(o, dict):
        yield o
        for v in o.values():
            yield from _walk(v)
    elif isinstance(o, list):
        for v in o:
            yield from _walk(v)


def _types(o):
    t = o.get("@type", "")
    return {t} if isinstance(t, str) else set(t)


def _mls(text):
    return {int(m) for m in ML_RE.findall(text or "")}


def jsonld_offers(page):
    """Devuelve [(precio, texto_de_la_oferta, nombre_del_producto, disponible)] de los bloques JSON-LD."""
    out = []
    for raw in re.findall(r'<script[^>]+application/ld\+json[^>]*>(.*?)</script>', page, re.S | re.I):
        try:
            data = json.loads(htmllib.unescape(raw.strip()), strict=False)
        except Exception:
            continue
        for o in _walk(data):
            if not (_types(o) & {"Product", "ProductGroup"}):
                continue
            pname = " ".join(str(o.get(k, "")) for k in ("name", "sku", "size"))[:300]
            offers = o.get("offers")
            if isinstance(offers, dict) and "offers" in offers:
                offers = offers["offers"]
            if isinstance(offers, dict):
                offers = [offers]
            for of in offers or []:
                if not isinstance(of, dict):
                    continue
                p = to_float(of.get("price") or of.get("lowPrice") or "")
                if not p:
                    continue
                cur = of.get("priceCurrency", "EUR")
                if cur and cur.upper() != "EUR":
                    continue
                desc = " ".join(str(of.get(k, "")) for k in ("name", "sku", "size"))
                av = str(of.get("availability", ""))
                out.append((p, desc, pname, "OutOfStock" not in av and "SoldOut" not in av))
    return out


def magento_price(page, ml):
    """Tiendas Magento con tallas (p. ej. Avenida): etiqueta '100 ml' -> id de producto -> precio final."""
    m = re.search(r'"optionPrices"\s*:\s*', page)
    if not m:
        return None
    try:
        prices, _ = json.JSONDecoder().raw_decode(page[m.end():])
    except Exception:
        return None
    for label, prods in re.findall(r'"label"\s*:\s*"([^"]*)"\s*,\s*"products"\s*:\s*\[([^\]]*)\]', page):
        if ml in _mls(label):
            for pid in re.findall(r'"?(\d+)"?', prods):
                amt = ((prices.get(pid) or {}).get("finalPrice") or {}).get("amount")
                if amt:
                    return float(amt)
    return None


UNIT_RE = re.compile(r"(\d{1,4}[.,]\d{2})\s*(?:€|&euro;)\s*(?:<!--.*?-->|\s)*(?:/|por)\s*(?:<!--.*?-->|\s)*100\s*(?:<!--.*?-->|\s)*(?:ml|mililitro)"
                     r"|100\s*ml\s*(?:/|a)\s*(\d{1,4}[.,]\d{1,2})\s*(?:€|&euro;)", re.I)


def unit_price(page, ml):
    """Fichas con varios tamaños que muestran precio y precio por 100 ml (Douglas, Perfume's Club, Laguna):
    el tamaño sale de dividir uno entre otro."""
    hits = []
    units = list(UNIT_RE.finditer(page))
    starts = {u.start() for u in units} | {u.start(2) for u in units if u.group(2)}
    for u in units:
        unit = to_float(u.group(1) or u.group(2))
        lo = max(0, u.start() - 600)
        # los precios por 100 ml no cuentan como precio del frasco
        prices = [to_float(m.group(1)) for m in PRICE_RE.finditer(page, lo, u.start()) if m.start() not in starts]
        if not unit or not prices or not prices[-1]:
            continue
        p = prices[-1]
        if abs(p / unit * 100 - ml) <= 0.04 * ml:
            hits.append(p)
    return hits[0] if hits else None   # la primera es la del producto; las siguientes pueden ser relacionados


def child_price(page, ml):
    """Avenida: cada tamaño es un bloque data-child-id; la foto dice '| 100 ml' y otro bloque su precio."""
    for cid in dict.fromkeys(re.findall(r'data-child-id="(\d+)"', page)):
        alt = re.search(rf'data-child-id="{cid}".{{0,400}}?alt="[^"]*?(\d{{2,3}})\s?ml"', page, re.S)
        cur = re.search(rf'data-child-id="{cid}"[^>]*>(?:(?!data-child-id).){{0,600}}?current-price[^>]*>\s*([\d.,]+)\s*€', page, re.S)
        if alt and cur and int(alt.group(1)) == ml:
            return to_float(cur.group(1))
    return None


def text_window_price(page, ml):
    """Respaldo: busca '<ml> ml' en el texto y el primer precio en € justo detrás."""
    txt = re.sub(r"<script.*?</script>|<style.*?</style>", " ", page, flags=re.S | re.I)
    txt = htmllib.unescape(re.sub(r"<[^>]+>", " ", txt))
    txt = re.sub(r"\s+", " ", txt)
    for m in re.finditer(rf"\b{ml}\s?ml\b", txt, re.I):
        win = txt[m.end(): m.end() + 140]
        if ML_RE.search(win[:60]) or re.match(r"\s*(?:/|a\s)", win) or re.search(r"(?:los|por|/)\s*$", txt[max(0, m.start() - 12): m.start()]):
            continue                         # otro tamaño pegado, o es el precio por 100 ml
        pm = PRICE_RE.search(win)
        if pm:
            p = to_float(pm.group(1))
            if p and 3 <= p <= 2000:
                return p
    return None


def extract(page, ml, url):
    """(precio, en_stock, metodo) del tamaño ml, o (None, None, motivo)."""
    offers = jsonld_offers(page)
    own = [o for o in offers if ml in _mls(o[1])]                       # la oferta dice su tamaño
    if not own:
        own = [o for o in offers if not _mls(o[1]) and _mls(o[2]) == {ml}]  # producto de un solo tamaño
        if len({round(o[0], 2) for o in own}) != 1:
            own = []
    if own:
        p, _, _, st = min(own, key=lambda o: o[0])
        return p, st, "jsonld"
    url_ml = re.search(rf"(?<!\d){ml}[-_ ]?ml(?![a-z])|[-_/]{ml}(?:[-_/.]|$)", url, re.I)
    single = {round(o[0], 2) for o in offers if not _mls(o[1])}
    if url_ml and len(single) == 1:
        o = next(o for o in offers if not _mls(o[1]))
        return o[0], o[3], "jsonld-url"
    p = magento_price(page, ml) or child_price(page, ml)
    if p:
        return p, None, "variantes"
    p = unit_price(page, ml)
    if p:
        return p, None, "precio-100ml"
    p = text_window_price(page, ml)
    if p:
        return p, None, "texto"   # shortcut: sin stock fiable en texto libre; se asume disponible
    return None, None, "sin-precio"


def plausible(p, ref, how="jsonld"):
    if ref is None:
        return how != "texto"
    lo, hi = (0.75, 1.3) if how == "texto" else (0.55, 1.5)
    return lo * ref <= p <= hi * ref


def ref_price(prices, shop):
    """Precio de referencia: mediana de las otras tiendas; si no hay, el último de esta."""
    others = [v["p"] for k, v in prices.items() if k != shop and v and v.get("p") and v.get("stock") is not False]
    return statistics.median(others) if others else (prices.get(shop) or {}).get("p")


def clean_outliers(it, today):
    """Quita precios leídos por el programa que salen muy por encima de lo que marcan las demás tiendas."""
    prices = it.get("prices") or {}
    gone = []
    for shop, v in list(prices.items()):
        # solo lo que leyó este programa (gh), o lo del 25-oct, cuando aún no se marcaba
        if not v or not v.get("p") or not (v.get("gh") or (v.get("auto") and v.get("d") == "2026-10-25")):
            continue
        others = [w["p"] for k, w in prices.items() if k != shop and w and w.get("p") and w.get("stock") is not False]
        # solo por arriba: un precio bajo que coincide con otras tiendas suele ser una rebaja real
        if len(others) >= 2 and v["p"] > 1.5 * statistics.median(others):
            del prices[shop]
            it["history"] = [h for h in it.get("history", []) if not (h.get("s") == shop and h.get("p") == v["p"])]
            gone.append(shop)
    return gone


DEBUG = {}   # una muestra por tienda y pasada, para poder ajustar el extractor


def debug_sample(shop, url, page, ml, result):
    if shop in DEBUG:
        return
    blocks = re.findall(r'<script[^>]+application/ld\+json[^>]*>(.*?)</script>', page, re.S | re.I)
    ctx = [page[max(0, m.start() - 120): m.end() + 60].replace("\n", " ") for m in PRICE_RE.finditer(page)][:25]
    DEBUG[shop] = {"url": url, "ml": ml, "resultado": result, "jsonld": [b.strip()[:3000] for b in blocks[:4]], "precios_en_html": ctx,
                   "variantes": [page[m.start(): m.start() + 700] for m in re.finditer(r"data-child-id|swatch-option|\"optionPrices\"|\"jsonConfig\"", page)][:4]}


# shortcut: First in Fragrance publica en su JSON-LD el precio sin IVA alemán; si cambia, quitar esto.
VAT = {"firstinfragrance": 1.19}


# ---------------------------------------------------------------- red
def make_session():
    try:
        from curl_cffi import requests as cr
        s = cr.Session(impersonate="chrome")
        return lambda u: s.get(u, timeout=25, allow_redirects=True)
    except Exception:
        import urllib.request
        def get(u):
            req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128 Safari/537.36", "Accept-Language": "es-ES,es;q=0.9"})
            with urllib.request.urlopen(req, timeout=25) as r:
                class R: pass
                x = R(); x.status_code = r.status; x.text = r.read().decode("utf-8", "replace"); return x
        return get


# ---------------------------------------------------------------- buscar fichas nuevas
# Tiendas que dejan buscar desde GitHub: si a un perfume le falta su ficha, se busca y se guarda.
SEARCH = {
    "douglas": "https://www.douglas.es/es/search?q={q}",
    "idealo": "https://www.idealo.es/resultados.html?q={q}",
    "lookfantastic": "https://www.lookfantastic.es/search?q={q}",
}
DISCOVER_PER_RUN = int(os.environ.get("RADAR_DISCOVER", "20"))
CONC_WORDS = {"EDT": "eau de toilette", "EDP": "eau de parfum", "EDC": "eau de cologne", "Parfum": "parfum", "Elixir": "elixir"}
SKIP_PATH = re.compile(r"/search|/buscar|resultados|/c/|/brands?/|/marcas?/|/categor|login|cart|wishlist|\.(?:css|js|png|jpg|svg|webp)", re.I)


def words(t):
    t = "".join(c for c in unicodedata.normalize("NFD", t.lower()) if unicodedata.category(c) != "Mn")
    t = re.sub(r"[^a-z0-9]+", " ", t)
    return [w for w in t.split() if len(w) >= 3 and w not in {"eau", "the", "for", "pour", "men", "man", "edt", "edp", "parfum", "toilette"}]


# Versiones del mismo perfume que no hay que confundir (Bottled vs Bottled Night)
FLANKERS = {"night", "intense", "intenso", "elixir", "absolu", "absolute", "extreme", "infinite", "tonic", "beyond", "sport",
            "privee", "noir", "black", "gold", "platinum", "oud", "cologne", "fraiche", "aqua", "blue", "red", "flame", "royal",
            "set", "estuche", "lote", "pack", "tester", "recarga", "refill", "mini", "body", "deodorant", "desodorante", "gel"}


def best_link(page, base, it):
    """La ficha de la página de resultados que mejor encaja con el perfume (o None)."""
    host = re.match(r"https?://[^/]+", base).group(0)
    need = words(it["name"])
    brand = (words(it["brand"]) or [""])[0]
    conc = CONC_WORDS.get(it.get("conc"), "").replace(" ", "-")
    best, score = None, 0
    for m in re.finditer(r'href="([^"#]+)"', page):
        href = htmllib.unescape(m.group(1))
        ctx = page[m.end(): m.end() + 300].split("href=")[0]   # el texto de este enlace, sin pisar el siguiente
        if href.startswith("/"):
            href = host + href
        if not href.startswith(host) or SKIP_PATH.search(href[len(host):]) or len(href) - len(host) < 12:
            continue
        hay = (href + " " + re.sub(r"<[^>]+>", " ", ctx)).lower()
        hay_w = set(words(hay))
        if not need or not all(w in hay_w for w in need) or (FLANKERS & hay_w) - set(words(it["name"] + " " + it.get("conc", ""))):
            continue
        sc = 2 + (brand in hay_w) + (bool(conc) and conc in hay.replace(" ", "-")) + (str(it["ml"]) in hay)
        if sc > score:
            best, score = href, sc
    return best


def discover(it, get, today, budget):
    """Busca la ficha en las tiendas de SEARCH que aún no tiene. Devuelve cuántas búsquedas gastó."""
    urls = it.setdefault("urls", {})
    tried = it.setdefault("buscado", {})
    spent = 0
    for shop, tpl in SEARCH.items():
        if spent >= budget or urls.get(shop):
            continue
        if tried.get(shop) and (datetime.fromisoformat(today) - datetime.fromisoformat(tried[shop])).days < 7:
            continue
        q = "+".join(re.sub(r"[^\w]+", " ", f"{it['brand']} {it['name']} {CONC_WORDS.get(it.get('conc'), '')}").split())
        spent += 1
        tried[shop] = today
        try:
            r = get(tpl.format(q=q))
            if getattr(r, "status_code", 0) != 200:
                continue
            link = best_link(r.text, tpl, it)
            DEBUG.setdefault("busqueda_" + shop, {"perfume": it["id"], "encontrada": link,
                             "enlaces": re.findall(r'href="([^"#]{12,160})"', r.text)[200:240]})
            if link:
                urls[shop] = link
        except Exception:
            pass
        time.sleep(1.2)
    return spent


# ---------------------------------------------------------------- pasada
def update_perfume(it, get, stats, today):
    ml = it["ml"]
    prices = it.setdefault("prices", {})
    hist = it.setdefault("history", [])
    for shop, url in (it.get("urls") or {}).items():
        if shop in MANUAL or not url:
            continue
        st = stats.setdefault(shop, {"ok": 0, "bloqueada": 0, "sin_precio": 0, "dudoso": 0})
        try:
            r = get(url)
            code = getattr(r, "status_code", 0)
        except Exception:
            st["bloqueada"] += 1
            continue
        if code in (403, 429, 503) or code >= 500:
            st["bloqueada"] += 1
            continue
        if code == 404 or code == 410:
            st["sin_precio"] += 1
            continue
        p, stock, how = extract(r.text, ml, url)
        if p and how != "texto":
            p *= VAT.get(shop, 1)
        ref = ref_price(prices, shop)
        ok = bool(p) and plausible(p, ref, how)
        debug_sample(shop, url, r.text, ml, {"precio": p and round(p, 2), "metodo": how, "referencia": ref, "aceptado": ok})
        if not p:
            st["sin_precio"] += 1
            continue
        if not ok:
            st["dudoso"] += 1
            ej = st.setdefault("ejemplos", [])
            if len(ej) < 3:
                ej.append({"perfume": it.get("id"), "precio": round(p, 2), "referencia": ref, "metodo": how})
            continue
        st["ok"] += 1
        st[how] = st.get(how, 0) + 1
        entry = {"p": round(p, 2), "d": today, "auto": True, "gh": True}
        if stock is False:
            entry["stock"] = False
        prices[shop] = entry
        if stock is not False:
            hist[:] = [h for h in hist if not (h.get("d") == today and h.get("s") == shop)]
            hist.append({"d": today, "s": shop, "p": round(p, 2)})
        time.sleep(random.uniform(0.8, 1.8))
    if len(hist) > 800:
        del hist[: len(hist) - 800]
    it["checked"] = now_iso()


# ---------------------------------------------------------------- chollometro
CH_PAGES = ["https://www.chollometro.com/categorias/perfumes",
            "https://www.chollometro.com/categorias/perfumes-de-hombre",
            "https://www.chollometro.com/categorias/perfumes-de-mujer"]


def parse_chollos(page):
    """Hilos de una página de categoría de Chollometro: [{id,t,p,shop,url,expired}]."""
    found = {}
    for _, raw in re.findall(r'data-vue3=(["\'])(.*?)\1', page, re.S):
        try:
            data = json.loads(htmllib.unescape(raw))
        except Exception:
            continue
        for o in _walk(data):
            if "threadId" in o and "title" in o:
                tid = int(o["threadId"])
                link = o.get("shareableLink") or o.get("link") or o.get("url") or ""
                if not str(link).startswith("http"):
                    link = f"https://www.chollometro.com/ofertas/{o.get('titleSlug', 'oferta')}-{tid}"
                merchant = o.get("merchant") or {}
                found[tid] = {"id": tid, "t": str(o["title"])[:120], "p": to_float(o.get("price")) if o.get("price") not in (None, "", 0) else None,
                              "shop": merchant.get("merchantName") if isinstance(merchant, dict) else None,
                              "url": link, "expired": bool(o.get("isExpired"))}
    if not found:   # respaldo: enlaces /ofertas/<slug>-<id>
        for m in re.finditer(r'href="(https://www\.chollometro\.com/ofertas/([^"#?]+)-(\d+))"', page):
            tid = int(m.group(3))
            title = m.group(2).replace("-", " ").capitalize()
            found.setdefault(tid, {"id": tid, "t": title[:120], "p": None, "shop": None, "url": m.group(1), "expired": False})
    return list(found.values())


PERFUME_WORDS = re.compile(r"perfum|eau de|\bedt\b|\bedp\b|parfum|colonia|fragancia|\d{2,3}\s?ml", re.I)


def pass_chollos(get, estado, brands=()):
    path = DATA / "chollos.json"
    feed = json.loads(path.read_text()) if path.exists() else {"items": []}
    old = {x["id"]: x for x in feed.get("items", [])}
    today = datetime.now(TZ).date().isoformat()
    n = 0
    for u in CH_PAGES:
        try:
            r = get(u)
            if getattr(r, "status_code", 0) != 200:
                estado["chollometro"] = f"error {getattr(r, 'status_code', '?')}"
                continue
            found = parse_chollos(r.text)
            if not found and "chollometro" not in DEBUG:
                DEBUG["chollometro"] = {"url": u, "vue3": len(re.findall(r"data-vue3=", r.text)), "ofertas": re.findall(r'.{0,150}/ofertas/.{0,150}', r.text)[:15], "inicio": r.text[:3000]}
            if not found:
                estado["chollometro"] = "0 encontrados"
            found = [x for x in found if PERFUME_WORDS.search(x["t"]) or any(b.lower() in x["t"].lower() for b in brands)]
            for x in found:
                x["seen"] = today
                old[x["id"]] = {**old.get(x["id"], {}), **{k: v for k, v in x.items() if v is not None}}
                n += 1
        except Exception as e:
            estado["chollometro"] = f"error {type(e).__name__}"
        time.sleep(1.5)
    items = sorted(old.values(), key=lambda x: x["id"], reverse=True)[:80]
    if n:
        estado["chollometro"] = f"ok {n}"
        feed = {"items": items, "updated": now_iso()}
        path.write_text(json.dumps(feed, ensure_ascii=False, indent=1))
    return n


# ---------------------------------------------------------------- prueba de tiendas
# Una vez al día comprueba qué tiendas dejan entrar desde GitHub (data/probe.json).
PROBE = {
    "primor": "https://www.primor.eu/es_es/catalogsearch/result/?q=boss+bottled",
    "druni": "https://www.druni.es/catalogsearch/result/?q=boss+bottled",
    "julia": "https://www.perfumesjulia.com/es/buscar?q=boss+bottled",
    "douglas": "https://www.douglas.es/es/search?q=boss%20bottled",
    "eci": "https://www.elcorteingles.es/buscar/?s=boss+bottled",
    "amazon": "https://www.amazon.es/s?k=boss+bottled+edt+100+ml",
    "idealo": "https://www.idealo.es/resultados.html?q=boss+bottled",
    "bodybell": "https://www.bodybell.com/search?q=boss+bottled",
    "perfumes24h": "https://www.perfumes24h.com/es/buscar?q=boss+bottled",
    "marvimundo": "https://www.marvimundo.com/buscar?controller=search&s=boss+bottled",
    "arenal": "https://www.arenal.com/catalogsearch/result/?q=boss+bottled",
    "coqueteo": "https://www.perfumeriascoqueteo.com/buscar?search_query=boss+bottled",
    "mifarma": "https://www.mifarma.es/catalogsearch/result/?q=boss+bottled",
    "makeup": "https://makeup.es/search/?q=boss+bottled",
    "gotta": "https://www.perfumeriasgotta.com/buscar?q=boss+bottled",
    "notino": "https://www.notino.es/search.asp?exps=boss+bottled",
    "sephora": "https://www.sephora.es/buscar?q=boss%20bottled",
    "lookfantastic": "https://www.lookfantastic.es/search?q=boss+bottled",
    "perfumesclub": "https://www.perfumesclub.com/es/buscar/?q=boss+bottled",
}
BLOCK_RE = re.compile(r"captcha|cf-chl|challenge-platform|access denied|acceso denegado|are you a robot|robot check|px-captcha|datadome", re.I)


def probe_page(get, url):
    try:
        r = get(url)
    except Exception as e:
        return {"url": url, "estado": "error", "detalle": type(e).__name__}
    t = r.text or ""
    title = re.search(r"<title[^>]*>(.*?)</title>", t, re.S | re.I)
    info = {"url": url, "codigo": getattr(r, "status_code", 0), "kb": len(t) // 1024,
            "titulo": htmllib.unescape(title.group(1)).strip()[:90] if title else None,
            "precios_eur": len(PRICE_RE.findall(t)), "jsonld": len(re.findall(r"application/ld\+json", t)),
            "menciona_boss": len(re.findall(r"bottled", t, re.I))}
    blocked = info["codigo"] in (401, 403, 429, 503) or (BLOCK_RE.search(t[:20000]) and info["precios_eur"] < 3)
    info["estado"] = "bloqueada" if blocked else ("con precios" if info["precios_eur"] >= 3 and info["menciona_boss"] else "entra, sin precios")
    return info


def run_probe(get):
    path = DATA / "probe.json"
    if path.exists():
        try:
            last = json.loads(path.read_text()).get("at", "")
            if last and (datetime.now(TZ) - datetime.fromisoformat(last)).total_seconds() < 86400:
                return
        except Exception:
            pass
    res = {}
    for shop, url in PROBE.items():
        res[shop] = probe_page(get, url)
        print("prueba", shop, res[shop]["estado"], res[shop].get("codigo"), flush=True)
        time.sleep(1.2)
    path.write_text(json.dumps({"at": now_iso(), "tiendas": res}, ensure_ascii=False, indent=1))


def main():
    get = make_session()
    perfumes = json.loads((DATA / "perfumes.json").read_text())
    today = datetime.now(TZ).date().isoformat()
    limpiados = {i["id"]: g for i in perfumes if (g := clean_outliers(i, today))}
    order = sorted(perfumes, key=lambda i: i.get("checked") or "")
    stats = {}
    budget = DISCOVER_PER_RUN
    for it in order[:BATCH]:
        budget -= discover(it, get, today, budget)
        update_perfume(it, get, stats, today)
        got = ", ".join("%s:%s" % (k, v["p"]) for k, v in (it.get("prices") or {}).items() if v and v.get("d") == today)
        print("%s %s %s ml -> %s" % (it["brand"], it["name"], it["ml"], got or "-"), flush=True)
    (DATA / "perfumes.json").write_text(json.dumps(perfumes, ensure_ascii=False, indent=1, sort_keys=True))
    estado = {"at": now_iso(), "revisados": min(BATCH, len(perfumes)), "tiendas": stats, "limpiados": limpiados}
    pass_chollos(get, estado, {i["brand"] for i in perfumes})
    (DATA / "debug.json").write_text(json.dumps(DEBUG, ensure_ascii=False, indent=1))
    run_probe(get)
    (DATA / "estado.json").write_text(json.dumps(estado, ensure_ascii=False, indent=1))
    print(json.dumps(estado, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    sys.exit(main())
