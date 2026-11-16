"""Pirámide olfativa de cada perfume, una sola vez, en data/notas.json.

Fuente principal: Parfumo (notas con su peso y acordes principales). Si Parfumo no separa
salida, corazón y fondo, se busca la pirámide en el texto de las fichas de las tiendas que ya
seguimos (Laguna, Avenida, Parejo, Sabina, Paco). Nada se inventa: lo que no se encuentra queda vacío.
"""
import html, json, os, re, sys, time, unicodedata
from curl_cffi import requests

DATA = os.path.join(os.path.dirname(__file__), '..', 'data')
OUT = os.path.join(DATA, 'notas.json')
S = requests.Session(impersonate='chrome')
CONC = {'EDP': 'eau de parfum', 'EDT': 'eau de toilette', 'EDC': 'eau de cologne', 'Parfum': 'parfum', 'Extrait': 'extrait', 'Elixir': 'elixir'}
SIZE = {'xl': 100, 'l': 85, 'm': 65, 's': 45, 'xs': 30}
BRAND = {'Armani': 'Giorgio Armani', 'YSL': 'Yves Saint Laurent', 'Paco Rabanne': 'Rabanne', 'Hugo Boss': 'Hugo Boss', 'CH': 'Carolina Herrera', 'D&G': 'Dolce & Gabbana', 'Lattafa': 'Lattafa Perfumes', 'Afnan': 'Afnan Perfumes', 'Rasasi': 'Rasasi'}
STORE_ORDER = ('laguna', 'avenida', 'parejo', 'sabina', 'paco')


def norm(s):
    s = unicodedata.normalize('NFKD', html.unescape(s or '')).encode('ascii', 'ignore').decode().lower()
    return re.sub(r'[^a-z0-9]+', ' ', s).strip()


def key(it):
    return f"{it['brand']}|{it['name']}|{it['conc']}"


def get(url):
    for t in range(3):
        try:
            r = S.get(url, timeout=30)
            if r.status_code == 200:
                return r.text
            if r.status_code in (403, 404):
                return None
        except Exception:
            pass
        time.sleep(3 + t * 3)
    return None


def parfumo_search(it):
    """URL de Parfumo del perfume: misma marca, mismo nombre y, si se puede, misma concentración."""
    from urllib.parse import quote
    h = get('https://www.parfumo.com/s_perfumes_x.php?in=1&filter=' + quote(f"{it['name']} {it['brand']}"))
    if not h:
        return None
    best, score = None, -1
    for m in re.finditer(r'<div class="name">\s*<a href="(https://www\.parfumo\.com/Perfumes/[^"]+)">(.*?)</a>\s*<span class="brand">.*?<a [^>]*>(.*?)</a>', h, re.S):
        url, raw, brand = m.groups()
        label = re.search(r'<span class="label_a[^"]*">(.*?)</span>', raw)
        name = norm(re.sub(r'<span.*?</span>', '', raw))
        conc = norm(label.group(1)) if label else ''
        b1, b2 = norm(brand), norm(BRAND.get(it['brand'], it['brand']))
        if not (b1 == b2 or b1.startswith(b2 + ' ') or b2.startswith(b1 + ' ') or b1.endswith(' ' + b2)):
            continue
        sc = 0
        if name == norm(it['name']):
            sc += 10
        elif norm(it['name']) in name:
            sc += 4 - min(3, len(name.split()) - len(norm(it['name']).split()))
        else:
            continue
        want = CONC.get(it['conc'], norm(it['conc']))
        if conc == want:
            sc += 5
        elif not conc and it['conc'] in ('EDT', 'EDP'):
            sc += 1
        elif conc:
            sc -= 6  # otra concentración: no vale
        if sc > score:
            best, score = url, sc
    return best if score >= 10 else None


NOTE = re.compile(r'<span class="clickable_note\w*(?: notefont(\d))?[^"]*"[^>]*>\s*<span class="nowrap pointer">\s*(?:<img[^>]*>)?\s*([^<]+?)\s*</span>', re.S)


def parfumo_page(url):
    h = get(url)
    if not h:
        return None
    out = {'src': 'parfumo', 'url': url, 'levels': {}, 'flat': [], 'accords': []}
    i = h.find('notes_list')
    if i >= 0:
        j = h.find('<h2', i)
        seg = h[i:j if j > 0 else i + 20000]
        marks = [(m.start(), m.group(1)) for m in re.finditer(r'class="[^"]*\bnb_([tmbn])\b', seg)]
        for k, (pos, lv) in enumerate(marks):
            end = marks[k + 1][0] if k + 1 < len(marks) else len(seg)
            notes = [[html.unescape(n).strip(), int(w or 1)] for w, n in NOTE.findall(seg[pos:end])]
            if lv == 'n':
                out['flat'] += notes
            else:
                out['levels'][{'t': 'top', 'm': 'heart', 'b': 'base'}[lv]] = notes
    a = h.find('Main accords')
    if a >= 0:
        for size, name in re.findall(r's-circle_(\w+)[^"]*"[^>]*>\s*</div>\s*<div class="text-xs grey">([^<]+)</div>', h[a:a + 6000]):
            out['accords'].append([html.unescape(name).strip(), SIZE.get(size, 50)])
    return out


def clean_text(h):
    h = re.sub(r'<script.*?</script>|<style.*?</style>', ' ', h, flags=re.S)
    t = html.unescape(re.sub(r'<[^>]+>', ' ', h))
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]*>?|https?://\S+', ' ', t))


LV = re.compile(r'(?i)notas? de salida\s*(?::|son)\s*(.{3,220}?)\s*[.;]?\s*(?:las\s+)?notas? de coraz[oó]n\s*(?::|son)\s*(.{3,220}?)\s*[.;]?\s*(?:las\s+)?notas? de fondo\s*(?::|son)\s*(.{3,220}?)(?:\.|;| {2}|$)')

# Paco y otras lo cuentan en prosa: "En las notas de salida de X se encuentran ... En su corazón, ... Finalizan en un fondo de ..."
LV2 = re.compile(r'(?i)notas? de salida[^.:]{0,45}?(?:se encuentran|incluyen|destacan|:|son)\s*(.{3,260}?)\.\s*[^.]{0,30}?coraz[oó]n[^.:,]{0,30}?(?:,|:|se encuentran|incluyen|destacan|son)\s*(.{3,260}?)\.\s*[^.]{0,40}?fondo(?: de)?[^.:,]{0,20}?(?:,|:|de|son)?\s*(.{3,260}?)\.')


def split_notes(s):
    s = re.sub(r'(?i)\b(las|los|la|el|y unas?|con)\b', ' ', s)
    parts = re.split(r',|\s+y\s+|\s+e\s+|/', s)
    out = []
    for p in parts:
        p = re.sub(r'\(.*?\)', '', p).strip(' .:-')
        if re.fullmatch(r"[A-Za-zÁÉÍÓÚÜÑáéíóúüñ' -]{3,28}", p) and len(p.split()) <= 5:
            out.append([p.capitalize(), 1])
    return out


def total(levels):
    return sum(len(v) for v in (levels or {}).values())


def store_pyramid(it):
    """La pirámide más completa entre las fichas de las tiendas (no la primera que aparezca)."""
    best = None
    for shop in STORE_ORDER:
        u = (it.get('urls') or {}).get(shop)
        if not u:
            continue
        h = get(u)
        time.sleep(1)
        if not h:
            continue
        t = clean_text(h)
        for rx in (LV, LV2):
            m = rx.search(t)
            if not m:
                continue
            top, heart, base = (split_notes(g) for g in m.groups())
            if top and heart and base:
                lv = {'top': top, 'heart': heart, 'base': base}
                if not best or total(lv) > total(best['levels']):
                    best = {'src': 'tienda:' + shop, 'url': u, 'levels': lv}
    return best


def choose(rec, sp):
    """Se queda con la pirámide más completa; si la única pirámide es mucho más pobre que la lista de Parfumo, enseña la lista."""
    if sp and total(sp['levels']) > total(rec.get('levels')):
        rec = {**rec, 'levels': sp['levels'], 'levels_src': sp['src'], 'levels_url': sp['url']}
        rec.setdefault('src', sp['src'])
        if not rec.get('src'):
            rec['src'] = sp['src']
    if rec.get('levels') and rec.get('flat') and total(rec['levels']) < 0.6 * len(rec['flat']):
        rec['levels'] = {}
        rec.pop('levels_src', None)
        rec.pop('levels_url', None)
    return rec


def main():
    items = json.load(open(os.path.join(DATA, 'perfumes.json')))
    done = json.load(open(OUT)) if os.path.exists(OUT) else {}
    limit = int(os.environ.get('NOTAS_LIMITE', '250'))
    seen, n = set(), 0
    for it in items:
        k = key(it)
        old = done.get(k) or {}
        redo = os.environ.get('NOTAS_REHACER') == 'escasas' and old.get('src') and total(old.get('levels')) <= 5
        if k in seen or (old.get('src') and not redo):
            continue
        seen.add(k)
        if n >= limit:
            break
        n += 1
        rec = {'src': None}
        url = old.get('url') if old.get('src') == 'parfumo' else parfumo_search(it)
        time.sleep(1.5)
        if url:
            rec = parfumo_page(url) or rec
            time.sleep(1.5)
        if total(rec.get('levels')) <= 5:
            rec = choose(rec, store_pyramid(it))
        rec['checked'] = time.strftime('%Y-%m-%d')
        done[k] = rec
        lv = rec.get('levels') or {}
        print(f"{k}: {rec.get('src')} niveles={'/'.join(str(len(lv.get(x, []))) for x in ('top', 'heart', 'base'))} planas={len(rec.get('flat', []))} acordes={len(rec.get('accords', []))}", flush=True)
        if n % 10 == 0:
            json.dump(done, open(OUT, 'w'), ensure_ascii=False, indent=0, sort_keys=True)
    json.dump(done, open(OUT, 'w'), ensure_ascii=False, indent=0, sort_keys=True)
    found = sum(1 for v in done.values() if v.get('levels') or v.get('flat'))
    print(f'Hecho: {found} de {len(done)} con notas')


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        # comprobación rápida del lector de la pirámide en texto de tienda
        t = 'Familia Olfativa : Oriental. Notas de Salida : Almendra y Café. Notas de Corazón : Jazmín Sambac y Nardos. Notas de Fondo : Haba Tonka y Cacao. Productos'
        m = LV.search(t)
        assert m and [x[0] for x in split_notes(m.group(1))] == ['Almendra', 'Café'], m and m.groups()
        assert [x[0] for x in split_notes(m.group(3))] == ['Haba tonka', 'Cacao']
        h = '<div class="nb_n"><span class="clickable_note_img notefont5" data-nt="n"><span class="nowrap pointer"><img src="x" alt="Ambroxan">Ambroxan</span></span></div>'
        assert NOTE.findall(h) == [('5', 'Ambroxan')], NOTE.findall(h)
        g = 'En las notas de salida de Good Girl se encuentran la almendra, el café, la bergamota y el limón. En su corazón, jazmín sambac, nardos, raíz de lirio, rosa de Bulgaria y flor de azahar del naranjo. Finalizan en un fondo de haba tonka, cacao, sándalo, vainilla, praliné, canela, cedro y pachulí. “Una mujer'
        m = LV2.search(g)
        assert m and [x[0] for x in split_notes(m.group(1))] == ['Almendra', 'Café', 'Bergamota', 'Limón'], m and m.groups()
        assert len(split_notes(m.group(2))) == 5 and split_notes(m.group(3))[0][0] == 'Haba tonka', m.groups()
        r = choose({'src': 'parfumo', 'levels': {'top': [['a', 1]], 'heart': [['b', 1]], 'base': [['c', 1]]}, 'flat': [['x', 1]] * 9}, None)
        assert r['levels'] == {}, r
        print('ok')
    else:
        main()
