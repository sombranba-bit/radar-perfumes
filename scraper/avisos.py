"""Avisos de precio objetivo (se ejecuta tras cada pasada).

Cada aviso es una incidencia abierta del repositorio con título «Aviso: …» y en el cuerpo
`id: <perfume>` y `precio: <euros>`. Si el mejor precio baja de ese objetivo, el bot comenta
en la incidencia (GitHub lo manda por email a quien la abrió) y, si hay TELEGRAM_TOKEN y
TELEGRAM_CHAT, también por Telegram. Solo vuelve a avisar si baja más que la última vez.
"""
import json
import os
import re
import subprocess
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data"
REPO = os.environ.get("GITHUB_REPOSITORY", "sombranba-bit/radar-perfumes")
WEB = "https://sombranba-bit.github.io/radar-perfumes/"
MARK = re.compile(r"<!-- aviso:([\d.]+) -->")


def best(it, today):
    """Igual que la web: el más barato en stock leído en los últimos 14 días."""
    ok = [(v["p"], s) for s, v in (it.get("prices") or {}).items()
          if v and v.get("p") and v.get("stock") is not False and v.get("d")
          and (today - date.fromisoformat(v["d"][:10])).days <= 14]
    return min(ok) if ok else None


def parse(body):
    m_id = re.search(r"^\s*id:\s*(\S+)", body or "", re.M)
    m_p = re.search(r"^\s*precio:\s*([\d.,]+)", body or "", re.M)
    if not (m_id and m_p):
        return None
    return m_id.group(1), float(m_p.group(1).replace(",", "."))


def decide(b, target, last):
    """¿Hay que avisar? Solo si está en el objetivo o por debajo y es más bajo que el último aviso."""
    return bool(b) and b[0] <= target + 0.005 and (last is None or b[0] < last - 0.005)


def gh(*args, data=None):
    cmd = ["gh", "api", *args]
    if data is not None:
        cmd += ["-X", "POST", "--input", "-"]
    out = subprocess.run(cmd, input=json.dumps(data) if data is not None else None,
                         capture_output=True, text=True, check=True).stdout
    return json.loads(out or "null")


def telegram(text):
    tok, chat = os.environ.get("TELEGRAM_TOKEN"), os.environ.get("TELEGRAM_CHAT")
    if not (tok and chat):
        return
    body = urllib.parse.urlencode({"chat_id": chat, "text": text}).encode()
    try:
        urllib.request.urlopen("https://api.telegram.org/bot%s/sendMessage" % tok, body, timeout=20)
    except Exception as e:
        print("telegram:", e)


def main():
    today = date.today()
    items = {i["id"]: i for i in json.loads((DATA / "perfumes.json").read_text())}
    issues = gh("repos/%s/issues?state=open&per_page=100" % REPO) or []
    sent = 0
    for iss in issues:
        if "pull_request" in iss or not iss["title"].lower().startswith("aviso"):
            continue
        got = parse(iss.get("body"))
        if not got or got[0] not in items:
            continue
        pid, target = got
        it = items[pid]
        b = best(it, today)
        comments = gh("repos/%s/issues/%d/comments?per_page=100" % (REPO, iss["number"])) or []
        marks = [float(m.group(1)) for c in comments for m in [MARK.search(c.get("body") or "")] if m]
        last = marks[-1] if marks else None
        if not decide(b, target, last):
            continue
        p, shop = b
        url = (it.get("urls") or {}).get(shop) or WEB
        name = "%s %s %s %s ml" % (it["brand"], it["name"], it["conc"], it["ml"])
        msg = "%s ha bajado a %.2f € en %s (tu objetivo: %.2f €).\n%s\nFicha: %sp/%s.html" % (name, p, shop, target, url, WEB, pid)
        gh("repos/%s/issues/%d/comments" % (REPO, iss["number"]), data={"body": msg + "\n<!-- aviso:%.2f -->" % p})
        telegram(msg)
        sent += 1
        print("aviso:", name, p)
    print("avisos enviados:", sent)


if __name__ == "__main__":
    main()
