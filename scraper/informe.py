"""Informe semanal: abre una incidencia con lo que ha cambiado en 7 días (GitHub la manda por email).

Compara data/perfumes.json con la versión de hace una semana (historial de git).
"""
import json
import subprocess
import sys
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from avisos import best, gh, REPO, WEB

ROOT = Path(__file__).resolve().parent.parent


def old_items(days=7):
    rev = subprocess.run(["git", "rev-list", "-1", "--before=%d days ago" % days, "HEAD"], cwd=ROOT,
                         capture_output=True, text=True).stdout.strip()
    if not rev:
        return {}
    txt = subprocess.run(["git", "show", rev + ":data/perfumes.json"], cwd=ROOT, capture_output=True, text=True).stdout
    return {i["id"]: i for i in json.loads(txt or "[]")}


def report(now, old, estado, today):
    then = today - timedelta(days=7)
    name = lambda i: "%s %s %s ml" % (i["brand"], i["name"], i["ml"])
    priced = [i for i in now if best(i, today)]
    new = [i for i in now if i["id"] not in old]
    gained = [i for i in priced if not (old.get(i["id"]) and best(old[i["id"]], then))]
    drops = []
    for i in priced:
        o = old.get(i["id"])
        b0 = o and best(o, then)
        b1 = best(i, today)
        if b0 and b1[0] < b0[0] * 0.95:
            drops.append((b1[0] / b0[0] - 1, i, b0[0], b1))
    drops.sort(key=lambda x: x[0])
    desc = sum(len(i.get("descartadas") or []) - len((old.get(i["id"]) or {}).get("descartadas") or []) for i in now)
    shops = estado.get("tiendas") or {}
    bad = sorted(s for s, v in shops.items() if v.get("bloqueada", 0) + v.get("sin_precio", 0) > v.get("ok", 0))
    L = ["Semana hasta el %s." % today.strftime("%d-%m-%Y"), "",
         "- Perfumes: **%d**, con precio **%d** (%+d nuevos con precio esta semana)" % (len(now), len(priced), len(gained)),
         "- Añadidos al catálogo: %d" % len(new),
         "- Fichas de tienda descartadas por erróneas: %d" % max(desc, 0),
         "- Tiendas con más fallos que aciertos en la última pasada: %s" % (", ".join(bad) or "ninguna"), ""]
    if drops:
        L += ["**Mayores bajadas de la semana**", ""]
        L += ["- [%s](%sp/%s.html): %.2f € → %.2f € en %s (%.0f %%)" % (name(i), WEB, i["id"], p0, b[0], b[1], d * 100) for d, i, p0, b in drops[:10]]
        L.append("")
    sin = [i for i in now if not best(i, today)]
    if sin:
        L += ["**Sin precio (%d):** %s" % (len(sin), ", ".join(name(i) for i in sin[:20])), ""]
    L.append("Web: " + WEB)
    return "\n".join(L)


def main():
    today = date.today()
    now = json.loads((ROOT / "data/perfumes.json").read_text())
    estado = json.loads((ROOT / "data/estado.json").read_text())
    body = report(now, old_items(), estado, today)
    print(body)
    if "--publicar" in sys.argv:
        gh("repos/%s/issues" % REPO, data={"title": "Informe semanal %s" % today.strftime("%d-%m-%Y"), "body": body})


if __name__ == "__main__":
    main()
