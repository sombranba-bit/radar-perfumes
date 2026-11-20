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
# Fichas de Parfumo que el buscador no empareja solo (otro nombre, año o "Emporio Armani -" delante), revisadas a mano
P = 'https://www.parfumo.com/Perfumes/'
PARFUMO_URL = {k: P + v for k, v in {
    'Armani|Acqua di Giò Profondo|EDP': 'Giorgio_Armani/acqua-di-gio-profondo-2024-eau-de-parfum',
    'Armani|Code|EDT': 'Giorgio_Armani/Armani_Code_Black_Code_Eau_de_Toilette',
    'Armani|Stronger With You Absolutely|Parfum': 'Giorgio_Armani/emporio-armani-stronger-with-you-absolutely',
    'Bvlgari|Man in Black|EDP': 'Bvlgari/Bvlgari_Man_In_Black',
    'Chanel|Chanel Nº5|EDP': 'Chanel/N5_Eau_de_Parfum',
    'Chanel|Gabrielle|EDP': 'Chanel/Gabrielle_Chanel',
    'Chanel|Égoïste Platinum|EDT': 'Chanel/Platinum_Egoiste_Eau_de_Toilette',
    'Givenchy|Gentleman Reserve Privée|EDP': 'Givenchy/gentleman-givenchy-reserve-privee',
    'Hugo Boss|Boss The Scent Le Parfum|Parfum': 'Hugo_Boss/the-scent-le-parfum-for-him',
    'Lancôme|La Nuit Trésor|EDP': 'Lancome/La_Nuit_Tresor',
    'Maison Francis Kurkdjian|Baccarat Rouge 540 Extrait|Parfum': 'Maison_Francis_Kurkdjian/Baccarat_Rouge_540_Extrait_de_Parfum',
    'Narciso Rodriguez|Bleu Noir|EDP': 'Narciso_Rodriguez/For_Him_Bleu_Noir_Eau_de_Parfum',
    'Valentino|Uomo Born in Roma Intense|EDP': 'Valentino/valentino-uomo-born-in-roma-intense',
    'Yves Saint Laurent|Libre Intense|EDP': 'Yves_Saint_Laurent/libre-eau-de-parfum-intense',
    'Yves Saint Laurent|Y|EDT': 'Yves_Saint_Laurent/Y_2017',
    'Armani|Stronger With You|EDT': 'Giorgio_Armani/Emporio_Armani_Stronger_With_You',
    'Valentino|Born in Roma Coral Fantasy Uomo|EDT': 'Valentino/valentino-uomo-born-in-roma-coral-fantasy',
    'Dolce & Gabbana|Light Blue Eau Intense pour Homme|EDP': 'Dolce_Gabbana/Light_Blue_pour_Homme_Eau_Intense',
    'Lattafa|Badee Al Oud Oud for Glory|EDP': 'Lattafa/oud-for-glory',
    'Dior|Miss Dior Blooming Bouquet|EDT': 'Dior/miss-dior-blooming-bouquet-2023-eau-de-toilette',
    'Valentino|Born in Roma Donna Intense|EDP': 'Valentino/valentino-donna-born-in-roma-intense',
    'Rabanne|Fame Parfum|Parfum': 'Rabanne/fame-parfum',
    'Mugler|Alien Goddess|EDP': 'mugler/alien-goddess-eau-de-parfum',
    'Prada|Paradoxe Intense|EDP': 'Prada/paradoxe-intense',
    'Kayali|Vanilla 28|EDP': 'Kayali/vanilla-28-eau-de-parfum',
    'Jo Malone|English Pear & Freesia|EDC': 'Jo_Malone/english-pear-freesia-cologne',
    'Maison Margiela|Replica Lazy Sunday Morning|EDT': 'Maison_Margiela/lazy-sunday-morning-eau-de-toilette',
    'Byredo|Mojave Ghost|EDP': 'Byredo/Mojave_Ghost_Eau_de_Parfum',
    'Narciso Rodriguez|For Her Pure Musc|EDP': 'Narciso_Rodriguez/for-her-pure-musc-eau-de-parfum',
    'Chloé|Chloé|EDP': 'Chloe/Chloe',
    'Dolce & Gabbana|Q|EDP': 'Dolce_Gabbana/q-eau-de-parfum',
    "Hermès|Terre d'Hermès Parfum|Parfum": 'Hermes/Terre_d_Hermes_Parfum',
    'Yves Saint Laurent|Y Elixir|Elixir': 'Yves_Saint_Laurent/y-l-elixir',
    'Bvlgari|Man Wood Essence|EDP': 'Bvlgari/bvlgari-man-wood-essence',
    'Xerjoff|Alexandria II|EDP': 'Xerjoff/alexandria-ii-parfum',
    'Nishane|Ani|Parfum': 'Nishane/Ani',
    "Chanel|Nº5 L'Eau|EDT": 'Chanel/N5_L_Eau',
    'Mugler|Alien Goddess Intense|EDP': 'mugler/alien-goddess-eau-de-parfum-intense',
    'Gucci|Flora Gorgeous Jasmine|EDP': 'Gucci/flora-gorgeous-jasmine',
    'Viktor&Rolf|Good Fortune|EDP': 'Viktor_Rolf/good-fortune',
    'Jean Paul Gaultier|La Belle Le Parfum|EDP': 'Jean_Paul_Gaultier/la-belle-le-parfum',
    'Ariana Grande|Thank U, Next|EDP': 'Ariana_Grande/thank-u-next-eau-de-parfum',
    'Kayali|Yum Pistachio Gelato 33|EDP': 'Kayali/pistachio-gelato-33-eau-de-parfum',
    'Marc Jacobs|Daisy Love|EDT': 'Marc_Jacobs/Daisy_Love',
    'Elie Saab|Le Parfum|EDP': 'Elie_Saab/Le_Parfum',
    'Tous|Tous|EDT': 'Tous/Tous',
    'Loewe|001 Woman|EDP': 'Loewe/Loewe_001_Woman',
    'Loewe|Solo Loewe|EDT': 'Loewe/Solo_Loewe',
    'Halloween|Halloween|EDT': 'Halloween/Halloween',
}.items()}
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
        url = PARFUMO_URL.get(k) or (old.get('url') if old.get('src') == 'parfumo' else parfumo_search(it))
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
