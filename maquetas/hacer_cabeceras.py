"""Genera maquetas/cabecera-{a,b,c}.html a partir de index.html: misma página, distinta marca y parte de arriba.
Uso: python3 maquetas/hacer_cabeceras.py  (vuelve a generarlas si cambia index.html)"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = (ROOT / "index.html").read_text()

# Cifras del día, comunes a las tres maquetas (todo sale de los datos reales)
STATS_JS = r"""
function stats(){
  const gs=R.groups(D.items,R.DEFAULTS,sizeSel),drops=gs.filter(x=>x.cur.dr&&x.cur.dr.pct<=-3);
  const byDrop=[...drops].sort((a,b)=>a.cur.dr.pct-b.cur.dr.pct);
  const top=byDrop.find(x=>R.photos(x.cur).length)||byDrop[0]||null;
  let save=null;for(const x of gs){const s=R.spread(x.cur);if(s&&(!save||s.save>save.s.save))save={x,s}}
  const shops=new Set();for(const i of D.items)for(const o of R.offers(i))if(o.age!=null&&o.age<=2&&o.s!=='idealo')shops.add(o.s);   // Idealo compara, no vende
  return {n:gs.length,drops:drops.length,top,save,shops:shops.size,at:D.estado?.at};
}
"""

SWITCH_CSS = """
.mq{position:fixed;left:50%;bottom:16px;transform:translateX(-50%);z-index:50;display:flex;gap:2px;padding:4px;background:#fff;border:1px solid #d9d8d3;border-radius:10px;box-shadow:0 4px 16px rgba(0,0,0,.08);font:500 13px/1 system-ui,sans-serif}
.mq a{padding:8px 12px;border-radius:7px;text-decoration:none;color:#3d3b36;white-space:nowrap}
.mq a[aria-current="page"]{background:#16150f;color:#fff}
@media (max-width:560px){.mq{bottom:calc(8px + env(safe-area-inset-bottom))}.mq a{padding:8px 9px}.mq .long{display:none}}
"""
SWITCH = """<nav class="mq" aria-label="Maquetas de cabecera">{links}</nav>"""
PAGES = [("cabecera-a.html", "A", "Estela"), ("cabecera-b.html", "B", "Eau de Rebaja"), ("cabecera-c.html", "C", "Radar"), ("../index.html", "", "Actual")]


def switch(current):
    out = []
    for href, k, name in PAGES:
        cur = ' aria-current="page"' if href == current else ""
        label = f'{k}<span class="long"> · {name}</span>' if k else name
        out.append(f'<a href="{href}"{cur}>{label}</a>')
    return SWITCH.format(links="".join(out))


MOCKS = {
# ------------------------------------------------------------------ A · Estela (revista de lujo)
"cabecera-a.html": dict(
    title="Estela · precios de perfume",
    desc="Compara el precio de 200 perfumes en las perfumerías españolas y mira cuáles bajan hoy.",
    fonts="family=IBM+Plex+Sans:wght@400;500;600&family=Bodoni+Moda:opsz,wght@6..96,400;6..96,500",
    favicon="""<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'><rect width='32' height='32' rx='7' fill='%2316150f'/><path d='M7 23c5 0 6-9 11-9s4 5 8 3' fill='none' stroke='%23f4efe6' stroke-width='2' stroke-linecap='round'/><circle cx='7' cy='23' r='2.4' fill='%23c9a46a'/></svg>""",
    brand="""<a class="brandmark" href="#" aria-label="Estela, inicio"><svg class="mark" width="34" height="22" viewBox="0 0 34 22" aria-hidden="true"><path d="M3 17c6 0 8-11 15-11s6 7 13 4" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/><circle cx="3" cy="17" r="2.6" fill="var(--accent)"/></svg><span><b>Estela</b><small>precios de perfume</small></span></a>""",
    css="""
.brandmark{text-decoration:none;gap:12px}
.brandmark b{display:block;font:500 26px/1 var(--display)}
.brandmark small{display:block;font-size:11px;color:var(--muted);margin-top:3px;letter-spacing:.01em}
.mark{color:var(--text)}
.hero{display:grid;grid-template-columns:minmax(0,1.1fr) minmax(0,1fr);gap:48px;align-items:center;padding:16px 0 40px;border-bottom:1px solid var(--rule);margin-bottom:32px}
.hero .kick{font-size:13px;color:var(--accent);margin:0 0 16px}
.hero h1{font:400 56px/1.02 var(--display);letter-spacing:-.01em;margin:0;max-width:12ch}
.hero .lede{font-size:17px;line-height:1.55;color:var(--muted);max-width:44ch;margin:20px 0 0}
.hero .facts{display:grid;grid-template-columns:repeat(3,auto);justify-content:start;gap:8px 28px;margin:28px 0 0;padding:0;list-style:none}
.hero .facts li{font-size:13px;color:var(--muted)}
.hero .facts b{display:block;font:400 30px/1.1 var(--display);color:var(--text)}
.feat{display:grid;grid-template-columns:minmax(0,1fr);text-decoration:none;color:inherit}
.feat .ph{aspect-ratio:4/3;max-height:min(52vh,460px);width:100%;border-radius:12px}
.feat .ph img{width:70%;height:70%}
.feat .ph svg{height:72%;width:auto}
.feat figcaption{display:flex;justify-content:space-between;align-items:baseline;gap:16px;margin-top:14px}
.feat .nm{font:500 22px/1.15 var(--display)}
.feat .sub{display:block;font-size:13px;color:var(--muted);margin-top:4px}
.feat .pz{text-align:right;white-space:nowrap}
.feat .pz b{display:block;font-size:20px;font-weight:600}
.feat .pz span{font-size:13px;color:var(--positive)}
.feat .tag{position:absolute;left:16px;top:16px;background:#fff;border-radius:6px;padding:4px 10px;font-size:12px;color:var(--muted)}
.cat{font:500 26px/1.1 var(--display);margin:0}
@media (max-width:1100px){.hero{grid-template-columns:1fr;gap:32px}.hero h1{font-size:44px}}
@media (max-width:860px){.hero{padding:8px 0 28px;margin-bottom:24px}.hero h1{font-size:36px}.hero .lede{font-size:15px}.hero .facts{gap:8px 16px}.hero .facts b{font-size:24px}.hero .facts li{font-size:12px}
  .mbrand{display:flex!important}}
.mbrand{display:none;align-items:center;gap:8px;margin:0 0 20px;font:500 22px/1 var(--display);color:var(--text);text-decoration:none}
""",
    hero=r"""
function hero(st){
  const t=st.top,i=t&&t.cur;
  const feat=i?`<a class="feat" href="#p/${t.key}"><div style="position:relative">${pic(i)}</div><span class="tag">La bajada del día</span></div>
    <figcaption><span><span class="nm">${esc(i.name)}</span><span class="sub">${esc(i.brand)} · ${i.ml} ml · en ${esc(i.b.name)}</span></span>
    <span class="pz"><b>${eur(i.b.p)}</b><span>${R.pct(i.dr.pct)} frente a su media</span></span></figcaption></a>`:'';
  return `<section class="hero" aria-labelledby="hTitle"><div>
    <span class="mbrand"><svg width="30" height="20" viewBox="0 0 34 22" aria-hidden="true"><path d="M3 17c6 0 8-11 15-11s6 7 13 4" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/><circle cx="3" cy="17" r="2.6" fill="var(--accent)"/></svg>Estela</span>
    <p class="kick">Hoy, ${new Date().toLocaleDateString('es-ES',{weekday:'long',day:'numeric',month:'long'})}</p>
    <h1 id="hTitle">El precio que deja huella</h1>
    <p class="lede">Seguimos ${st.n} perfumes en ${st.shops} perfumerías españolas y te enseñamos dónde cuesta menos cada uno, y cuáles bajan hoy.</p>
    <ul class="facts"><li><b>${st.drops}</b>bajan hoy</li>${st.save?`<li><b>${eur(st.save.s.save,0)}</b>de ahorro en ${esc(st.save.x.cur.name)}</li>`:''}<li><b>${R.agoTime(st.at).replace('hace ','')}</b>desde la última lectura</li></ul>
  </div>${feat}</section>`;
}
"""),
# ------------------------------------------------------------------ B · Eau de Rebaja (panel de chollos)
"cabecera-b.html": dict(
    title="Eau de Rebaja · el perfume, al mejor precio",
    desc="Qué perfumes bajan hoy y dónde cuestan menos, en las perfumerías españolas.",
    fonts="family=IBM+Plex+Sans:wght@400;500;600&family=Bodoni+Moda:opsz,wght@6..96,500&family=Bricolage+Grotesque:opsz,wght@12..96,600",
    favicon="""<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'><rect width='32' height='32' rx='7' fill='%23b8400b'/><text x='16' y='22' text-anchor='middle' font-family='Georgia' font-size='17' fill='%23fff'>%25</text></svg>""",
    brand="""<a class="brandmark" href="#" aria-label="Eau de Rebaja, inicio"><span class="tagm" aria-hidden="true">%</span><span class="wm"><i>Eau de</i> Rebaja</span></a>""",
    css="""
:root{--accent:#b8400b;--hot:#b8400b;--hot-bg:#fbeee6}
.brandmark{text-decoration:none;gap:10px}
.tagm{display:grid;place-items:center;width:30px;height:30px;border-radius:8px;background:var(--hot);color:#fff;font:500 17px/1 var(--display)}
.wm{font:600 22px/1 "Bricolage Grotesque",var(--display);letter-spacing:-.01em;white-space:nowrap}
.wm i{font:500 17px/1 var(--display);font-style:normal;color:var(--muted);margin-right:2px}
.hero{background:var(--chrome);border-radius:12px;padding:32px;margin:0 0 32px}
.hero h1{font:600 40px/1.05 "Bricolage Grotesque",sans-serif;letter-spacing:-.02em;margin:0;max-width:20ch}
.hero h1 em{font-style:normal;color:var(--hot)}
.hero .lede{color:var(--muted);font-size:15px;margin:10px 0 24px}
.hs{display:flex;gap:8px;max-width:640px}
.hs input{flex:1;min-width:0;height:52px;border:1px solid var(--control);border-radius:10px;padding:0 16px;font-size:17px;background:#fff}
.hs button{height:52px;padding:0 20px;border:0;border-radius:10px;background:var(--text);color:#fff;font-weight:500;cursor:pointer}
.kpis{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;margin-top:24px}
.kpi{display:block;background:#fff;border:1px solid var(--border);border-radius:10px;padding:16px;text-decoration:none;color:inherit;text-align:left;font:inherit;cursor:pointer}
@media (hover:hover) and (pointer:fine){.kpi:hover{border-color:var(--text)}}
.kpi small{display:block;font-size:13px;color:var(--muted)}
.kpi b{display:block;font:600 32px/1.1 "Bricolage Grotesque",sans-serif;margin-top:6px;letter-spacing:-.01em}
.kpi b.hot{color:var(--hot)}
.kpi span{display:block;font-size:13px;color:var(--muted);margin-top:4px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.badge{background:var(--hot-bg)!important;color:var(--hot)!important}
.cat{font:600 22px/1.1 "Bricolage Grotesque",sans-serif;margin:0}
@media (max-width:1100px){.kpis{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:860px){.hero{padding:20px 16px;margin:0 0 24px}.hero h1{font-size:30px}.kpi b{font-size:26px}.hs{display:none}.kpis{margin-top:4px}
  .mbrand{display:flex!important}}
.mbrand{display:none;align-items:center;gap:8px;margin:0 0 16px}
""",
    hero=r"""
function hero(st){
  const t=st.top,i=t&&t.cur,sv=st.save;
  return `<section class="hero" aria-labelledby="hTitle">
    <span class="mbrand"><span class="tagm" aria-hidden="true">%</span><span class="wm"><i>Eau de</i> Rebaja</span></span>
    <h1 id="hTitle">Hoy bajan <em>${st.drops} perfumes</em>. Mira dónde cuestan menos</h1>
    <p class="lede">${st.n} perfumes comparados en ${st.shops} perfumerías · precios leídos ${R.agoTime(st.at)}</p>
    <form class="hs" role="search" data-hs><input name="q" type="search" placeholder="Busca tu perfume o marca" aria-label="Buscar perfume" autocomplete="off"><button type="submit">Buscar</button></form>
    <div class="kpis">
      <button class="kpi" type="button" data-sortdrop><small>Bajan hoy</small><b class="hot">${st.drops}</b><span>frente a su media</span></button>
      ${i?`<a class="kpi" href="#p/${t.key}"><small>Mayor bajada</small><b class="hot">${R.pct(i.dr.pct)}</b><span>${esc(i.name)} · ${eur(i.b.p)}</span></a>`:''}
      ${sv?`<a class="kpi" href="#p/${sv.x.key}"><small>Más ahorro entre tiendas</small><b>${eur(sv.s.save,0)}</b><span>${esc(sv.x.cur.name)}</span></a>`:''}
      <a class="kpi" href="#chollos"><small>Chollos en Chollometro</small><b>${D.deals.length}</b><span>${D.items.filter(x=>x.deals.length).length} de tu lista</span></a>
    </div></section>`;
}
document.addEventListener('submit',e=>{if(!e.target.matches('[data-hs]'))return;e.preventDefault();const v=e.target.q.value.trim();if(!v)return;$('q').value=v;S.q=v;limit=24;route();$('q').focus()});
"""),
# ------------------------------------------------------------------ C · Radar (mezcla: elegante con cifras)
"cabecera-c.html": dict(
    title="Radar · comparador de precios de perfume",
    desc="Radar vigila el precio de 200 perfumes en las perfumerías españolas y te dice cuáles bajan hoy.",
    fonts="family=IBM+Plex+Sans:wght@400;500;600&family=Bodoni+Moda:opsz,wght@6..96,500&family=IBM+Plex+Mono:wght@400;500",
    favicon="""<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'><rect width='32' height='32' rx='7' fill='%2316150f'/><g fill='none' stroke='%23f4f4f2' stroke-width='1.6'><circle cx='16' cy='16' r='10' opacity='.45'/><circle cx='16' cy='16' r='5.5' opacity='.7'/><path d='M16 16 24 9' stroke-linecap='round'/></g><circle cx='21.5' cy='11' r='2.4' fill='%23d4a056'/></svg>""",
    brand="""<a class="brandmark" href="#" aria-label="Radar, inicio"><svg class="mark" width="30" height="30" viewBox="0 0 32 32" aria-hidden="true"><g fill="none" stroke="currentColor" stroke-width="1.4"><circle cx="16" cy="16" r="13" opacity=".25"/><circle cx="16" cy="16" r="8.5" opacity=".5"/><circle cx="16" cy="16" r="4" opacity=".8"/><path d="M16 16 26 7" stroke-linecap="round"/></g><circle cx="22.5" cy="10.5" r="2.6" fill="var(--accent)"/></svg><span><b>Radar</b><small>de perfumes</small></span></a>""",
    css="""
.brandmark{text-decoration:none;gap:10px}
.brandmark b{display:block;font:500 24px/1 var(--display)}
.brandmark small{display:block;font:400 11px/1 "IBM Plex Mono",monospace;color:var(--muted);margin-top:4px}
.mark{color:var(--text)}
.live{display:inline-flex;align-items:center;gap:8px;font:400 12px/1 "IBM Plex Mono",monospace;color:var(--muted);white-space:nowrap;margin-left:auto}
.live i{width:8px;height:8px;border-radius:50%;background:var(--positive);box-shadow:0 0 0 3px #e3f4e8}
.topbar{justify-content:flex-start;gap:24px}
.topbar .search{margin:0 auto}
.hero{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:32px;align-items:end;padding:8px 0 28px;border-bottom:1px solid var(--rule);margin-bottom:28px}
.hero h1{font:500 40px/1.08 var(--display);margin:0;max-width:18ch}
.hero .lede{color:var(--muted);font-size:15px;margin:12px 0 0;max-width:52ch}
.figs{display:flex;gap:0;margin:0;padding:0;list-style:none}
.figs li{padding:0 24px;border-left:1px solid var(--rule)}
.figs li:first-child{border-left:0;padding-left:0}
.figs b{display:block;font:500 36px/1 var(--display);white-space:nowrap}
.figs b.dn{color:var(--positive)}
.figs small{display:block;font-size:12px;line-height:1.35;color:var(--muted);margin-top:8px;max-width:18ch}
.figs a{text-decoration:none;color:inherit}
.cat{font:500 26px/1.1 var(--display);margin:0}
@media (max-width:1180px){.hero{grid-template-columns:1fr;align-items:start}}
@media (max-width:860px){.live{display:none}.hero h1{font-size:30px}.figs b{font-size:28px}.figs li{padding:0 14px}
  .mbrand{display:flex!important}}
.mbrand{display:none;align-items:center;gap:10px;margin:0 0 16px}
""",
    hero=r"""
function hero(st){
  const t=st.top,i=t&&t.cur,sv=st.save;
  return `<section class="hero" aria-labelledby="hTitle"><div>
    <span class="mbrand"><svg width="26" height="26" viewBox="0 0 32 32" aria-hidden="true"><g fill="none" stroke="currentColor" stroke-width="1.4"><circle cx="16" cy="16" r="13" opacity=".25"/><circle cx="16" cy="16" r="8.5" opacity=".5"/><circle cx="16" cy="16" r="4" opacity=".8"/><path d="M16 16 26 7" stroke-linecap="round"/></g><circle cx="22.5" cy="10.5" r="2.6" fill="var(--accent)"/></svg><b style="font:500 22px/1 var(--display)">Radar</b></span>
    <h1 id="hTitle">${st.n} perfumes vigilados en ${st.shops} perfumerías</h1>
    <p class="lede">Leemos el precio de cada tamaño varias veces al día y te avisamos de lo que baja. Precios leídos ${R.agoTime(st.at)}.</p></div>
    <ul class="figs">
      <li><button type="button" data-sortdrop style="all:unset;cursor:pointer"><b class="dn">${st.drops}</b><small>bajan hoy frente a su media</small></button></li>
      ${i?`<li><a href="#p/${t.key}"><b class="dn">${R.pct(i.dr.pct)}</b><small>${esc(i.name)}, la mayor bajada</small></a></li>`:''}
      ${sv?`<li><a href="#p/${sv.x.key}"><b>${eur(sv.s.save,0)}</b><small>de ahorro en ${esc(sv.x.cur.name)}</small></a></li>`:''}
    </ul></section>`;
}
"""),
}


def build(name, m):
    s = BASE
    def rep(a, b):
        nonlocal s
        assert a in s, (name, a[:70])
        s = s.replace(a, b, 1)
    rep("<title>Radar de Perfumes</title>", f'<title>{m["title"]}</title>\n<meta name="description" content="{m["desc"]}">\n'
        f'<meta property="og:title" content="{m["title"]}"><meta property="og:description" content="{m["desc"]}">\n'
        f'<link rel="icon" href="data:image/svg+xml,{m["favicon"]}">\n<meta name="robots" content="noindex">')
    rep("family=IBM+Plex+Sans:wght@400;500;600&family=Bodoni+Moda:opsz,wght@6..96,500", m["fonts"])
    rep("</style>", m["css"] + SWITCH_CSS + "</style>")
    rep('<header class="brandmark"><i>Radar</i> de Perfumes</header>', f'<header style="display:contents">{m["brand"]}</header>')
    if name == "cabecera-c.html":
        rep('<a class="tchollos" href="#chollos" data-sec="chollos">Chollos</a>',
            '<a class="tchollos" href="#chollos" data-sec="chollos">Chollos</a><span class="live" id="live"><i></i>en directo</span>')
    rep("""<script>document.write('<script src="maquetas/core.js?v='""", """<script>document.write('<script src="core.js?v='""")
    rep("D=await R.load('data/');", "D=await R.load('../data/');" + (
        "$('live')&&($('live').lastChild.textContent='leído '+R.agoTime(D.estado?.at));" if name == "cabecera-c.html" else ""))
    rep("$('sheet').innerHTML=`<div class=\"head\"><div><h1>Perfumes</h1>",
        "$('sheet').innerHTML=`${dirty.length?'':hero(stats())}<div class=\"head\"><div>${dirty.length?'<h1>Perfumes</h1>':'<h2 class=\"cat\">Catálogo</h2>'}")
    rep("· precios leídos ${R.agoTime(D.estado?.at)}</p></div>", "${dirty.length?' · precios leídos '+R.agoTime(D.estado?.at):''}</p></div>")
    rep("function catalog(){", STATS_JS + m["hero"] + "\nfunction catalog(){")
    rep("</body>", switch(name) + "\n</body>")
    (ROOT / "maquetas" / name).write_text(s)


for n, m in MOCKS.items():
    build(n, m)
print("ok:", ", ".join(MOCKS))
