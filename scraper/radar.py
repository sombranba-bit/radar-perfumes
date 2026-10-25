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
            data = json.loads(htmllib.unescape(raw.strip()))
        except Exception:
            continue
        for o in _walk(data):
            if not (_types(o) & {"Product", "ProductGroup"}):
                continue
            pname = " ".join(str(o.get(k, "")) for k in ("name", "sku", "size", "description"))[:400]
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
                desc = " ".join(str(of.get(k, "")) for k in ("name", "sku", "description", "size"))
                av = str(of.get("availability", ""))
                out.append((p, desc, pname, "OutOfStock" not in av and "SoldOut" not in av))
    return out


def text_window_price(page, ml):
    """Respaldo: busca '<ml> ml' en el texto y el primer precio en € justo detrás."""
    txt = re.sub(r"<script.*?</script>|<style.*?</style>", " ", page, flags=re.S | re.I)
    txt = htmllib.unescape(re.sub(r"<[^>]+>", " ", txt))
    txt = re.sub(r"\s+", " ", txt)
    for m in re.finditer(rf"\b{ml}\s?ml\b", txt, re.I):
        win = txt[m.end(): m.end() + 140]
        if ML_RE.search(win[:60]):          # otro tamaño pegado: no es este
            continue
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
    p = text_window_price(page, ml)
    if p:
        return p, None, "texto"   # shortcut: sin stock fiable en texto libre; se asume disponible
    return None, None, "sin-precio"


def plausible(p, ref):
    return ref is None or 0.45 * ref <= p <= 1.8 * ref


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


# ---------------------------------------------------------------- pasada
def update_perfume(it, get, stats, today):
    ml = it["ml"]
    prices = it.setdefault("prices", {})
    hist = it.setdefault("history", [])
    others = [v["p"] for v in prices.values() if v and v.get("p") and v.get("stock") is not False]
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
        if not p:
            st["sin_precio"] += 1
            continue
        last = (prices.get(shop) or {}).get("p")
        ref = last or (statistics.median(others) if others else None)
        if not plausible(p, ref) or (how == "texto" and ref is None):
            st["dudoso"] += 1
            continue
        st["ok"] += 1
        entry = {"p": round(p, 2), "d": today, "auto": True}
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
    for raw in re.findall(r'data-vue3="([^"]+)"', page):
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
        for m in re.finditer(r'href="(https://www\.chollometro\.com/ofertas/[^"#?]+-(\d+))"[^>]*title="([^"]+)"', page):
            tid = int(m.group(2))
            found.setdefault(tid, {"id": tid, "t": htmllib.unescape(m.group(3))[:120], "p": None, "shop": None, "url": m.group(1), "expired": False})
    return list(found.values())


def pass_chollos(get, estado):
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
            for x in parse_chollos(r.text):
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


def main():
    get = make_session()
    perfumes = json.loads((DATA / "perfumes.json").read_text())
    today = datetime.now(TZ).date().isoformat()
    order = sorted(perfumes, key=lambda i: i.get("checked") or "")
    stats = {}
    for it in order[:BATCH]:
        update_perfume(it, get, stats, today)
        got = ", ".join("%s:%s" % (k, v["p"]) for k, v in (it.get("prices") or {}).items() if v and v.get("d") == today)
        print("%s %s %s ml -> %s" % (it["brand"], it["name"], it["ml"], got or "-"), flush=True)
    (DATA / "perfumes.json").write_text(json.dumps(perfumes, ensure_ascii=False, indent=1, sort_keys=True))
    estado = {"at": now_iso(), "revisados": min(BATCH, len(perfumes)), "tiendas": stats}
    pass_chollos(get, estado)
    (DATA / "estado.json").write_text(json.dumps(estado, ensure_ascii=False, indent=1))
    print(json.dumps(estado, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    sys.exit(main())
