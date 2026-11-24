"""Guarda una ficha real por tienda con el precio que se leyó de ella, para las pruebas de regresión.

Para cada tienda busca un perfume cuyo precio de hoy salió de su propia ficha, la vuelve a leer y, si el
extractor da ese mismo precio, guarda la página (comprimida) en scraper/fixtures/. test_radar.py comprueba
después que el extractor sigue sacando el mismo precio de cada una.
"""
import gzip
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from radar import make_session, extract, MANUAL

ROOT = Path(__file__).resolve().parent.parent
OUT = Path(__file__).parent / "fixtures"


def main():
    get = make_session()
    OUT.mkdir(exist_ok=True)
    exp_path = OUT / "expected.json"
    expected = json.loads(exp_path.read_text()) if exp_path.exists() else {}
    items = json.loads((ROOT / "data/perfumes.json").read_text())
    cand = {}
    for it in sorted(items, key=lambda i: i.get("checked") or "", reverse=True):
        for shop, v in (it.get("prices") or {}).items():
            url = (it.get("urls") or {}).get(shop)
            if shop in MANUAL or shop == "idealo" or not url or not v or v.get("via") or not v.get("gh"):
                continue
            cand.setdefault(shop, []).append((it, url, v["p"]))
    for shop, lst in sorted(cand.items()):
        for it, url, p in lst[:4]:
            try:
                r = get(url)
            except Exception as e:
                print(shop, "error", type(e).__name__)
                continue
            if getattr(r, "status_code", 0) != 200:
                print(shop, r.status_code)
                continue
            got = extract(r.text, it["ml"], url)
            if got[0] and abs(got[0] - p) <= 0.02 * p:
                (OUT / (shop + ".html.gz")).write_bytes(gzip.compress(r.text.encode()))
                expected[shop] = {"perfume": it["id"], "url": url, "ml": it["ml"], "precio": got[0], "stock": got[1], "metodo": got[2]}
                print(shop, "guardada", it["id"], got)
                break
            print(shop, "no cuadra", it["id"], got, p)
    exp_path.write_text(json.dumps(expected, ensure_ascii=False, indent=1, sort_keys=True))


if __name__ == "__main__":
    main()
