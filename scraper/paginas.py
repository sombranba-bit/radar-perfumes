"""Una página pequeña por perfume (p/<id>.html) para compartir el enlace: WhatsApp, Telegram y redes
leen su título, precio y foto, y quien la abre pasa a la ficha de la web."""
import html
import json
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WEB = "https://sombranba-bit.github.io/radar-perfumes/"
NO_PHOTO = re.compile(r"placeholder|no[-_]?image|logo", re.I)
PHOTO = ["lookfantastic", "sephora", "douglas", "notino", "paco", "sabina", "laguna", "parejo", "avenida", "idealo"]


def page(it, today):
    from avisos import best
    b = best(it, today)
    name = "%s %s %s %s ml" % (it["brand"], it["name"], it["conc"], it["ml"])
    imgs = {k: u for k, u in (it.get("images") or {}).items() if u and not NO_PHOTO.search(u)}
    img = next((imgs[k] for k in PHOTO if k in imgs), next(iter(imgs.values()), ""))
    n = len([1 for v in (it.get("prices") or {}).values() if v and v.get("p")])
    desc = ("Desde %s € hoy · %d tiendas comparadas en Fragans" % (("%.2f" % b[0]).replace(".", ","), n)) if b else "Compara su precio en las perfumerías españolas con Fragans"
    key = re.sub(r"-\d+$", "", it["id"])
    dest = "../#p/" + key
    e = lambda s: html.escape(s, quote=True)
    return f"""<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(name)} · Fragans</title><meta name="description" content="{e(desc)}">
<meta property="og:type" content="product"><meta property="og:site_name" content="Fragans"><meta property="og:title" content="{e(name)}">
<meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{WEB}p/{it['id']}.html">{f'<meta property="og:image" content="{e(img)}">' if img else ''}
<meta name="twitter:card" content="{'summary_large_image' if img else 'summary'}"><link rel="canonical" href="{WEB}#p/{key}">
<meta http-equiv="refresh" content="0;url={dest}"><script>location.replace({json.dumps(dest)})</script>
<style>body{{font:16px system-ui,sans-serif;background:#f5f4f0;color:#1d1b18;margin:0;padding:24px}}a{{color:#8a2335}}</style></head>
<body><p><a href="{dest}">Ver {e(name)} en Fragans</a></p></body></html>
"""


def main():
    today = date.today()
    out = ROOT / "p"
    out.mkdir(exist_ok=True)
    items = json.loads((ROOT / "data/perfumes.json").read_text())
    keep = set()
    for it in items:
        f = out / (it["id"] + ".html")
        keep.add(f.name)
        txt = page(it, today)
        if not f.exists() or f.read_text() != txt:
            f.write_text(txt)
    for f in out.glob("*.html"):
        if f.name not in keep:
            f.unlink()
    print("páginas:", len(keep))


if __name__ == "__main__":
    import sys
    sys.path.insert(0, str(Path(__file__).parent))
    main()
