"""Genera maquetas/tema-1..6.html a partir de index.html: la misma página (datos y funciones reales) con seis
direcciones de diseño. Uso: python3 maquetas/hacer_temas.py"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = (ROOT / "index.html").read_text()

# ------------------------------------------------------------------ piezas comunes (cada tema las dibuja a su manera)
COMMON_JS = r"""
const FAMS=[['floral','Floral','#d4849a'],['amaderada','Amaderada','#8b6b4c'],['oriental','Oriental','#9c4a3c'],['ambar','Ámbar','#c98a2e'],
  ['aromatica','Aromática','#7f9a6a'],['gourmand','Gourmand','#b0764a'],['citrica','Cítrica','#d9ac2c'],['acuatica','Acuática','#5b9ab8']];
function famOf(i){const f=R.norm(i?.p?.fam||'');const w=f.split(' ')[0];return FAMS.find(([k])=>w.startsWith(k))||FAMS.find(([k])=>f.includes(k))||null}
function famsSection(){
  const gs=R.groups(D.items,R.DEFAULTS,sizeSel);
  const cards=FAMS.map(([k,n,c])=>{const m=gs.filter(x=>famOf(x.cur)?.[0]===k);if(!m.length)return '';
    const ph=m.map(x=>R.photos(x.cur)[0]).filter(Boolean).slice(0,3);
    return `<button class="famc" type="button" data-fam="${k}" style="--fam:${c}"><span class="famt"><span class="famn">${n}</span><span class="famk">${m.length} perfumes</span></span><span class="famph">${ph.map(f=>`<img src="${esc(f.url)}" alt="" loading="lazy" referrerpolicy="no-referrer" onerror="this.remove()">`).join('')}</span></button>`}).join('');
  return `<section class="fams" aria-labelledby="hFams"><h2 id="hFams" class="sec">Por familia olfativa</h2><div class="famg">${cards}</div></section>`;
}
document.addEventListener('click',e=>{const b=e.target.closest('[data-fam]');if(!b)return;const n=FAMS.find(f=>f[0]===b.dataset.fam)[1];S.q=n.toLowerCase();$('q').value=n;limit=24;route();scrollTo(0,0)});
function olf(i){
  const p=i.p;if(!p)return '';const f=famOf(i),notes=p.notes.split(/,\s*/);
  return `<section class="olf" style="--fam:${f?f[2]:'var(--accent)'}" aria-label="Cómo huele">
    <div class="olf-fam"><i aria-hidden="true"></i><span><small>Familia</small><b>${esc(p.fam)}</b></span></div>
    <ul class="olf-notes" aria-label="Notas">${notes.map((n,k)=>`<li style="--k:${k}">${esc(n)}</li>`).join('')}</ul>
    <div class="olf-se" aria-label="Temporada">${R.SEASONS.map(s=>`<span class="${p.se.includes(s)?'on':''}">${s}</span>`).join('')}</div></section>`;
}
function stats(){
  const gs=R.groups(D.items,R.DEFAULTS,sizeSel),drops=gs.filter(x=>x.cur.dr&&x.cur.dr.pct<=-3);
  const byDrop=[...drops].sort((a,b)=>a.cur.dr.pct-b.cur.dr.pct);
  const withPh=byDrop.filter(x=>R.photos(x.cur).length);
  let save=null;for(const x of gs){const s=R.spread(x.cur);if(s&&(!save||s.save>save.s.save))save={x,s}}
  const shops=new Set();for(const i of D.items)for(const o of R.offers(i))if(o.age!=null&&o.age<=2&&o.s!=='idealo')shops.add(o.s);
  return {n:gs.length,drops:drops.length,top:withPh[0]||byDrop[0]||null,tops:withPh.slice(0,3),save,shops:shops.size,at:D.estado?.at};
}
const today=()=>new Date().toLocaleDateString('es-ES',{weekday:'long',day:'numeric',month:'long'});
function featCard(t,label='La bajada del día'){const i=t&&t.cur;if(!i)return '';
  return `<a class="feat" href="#p/${t.key}"><div class="featph">${pic(i)}</div><span class="tag">${label}</span></div>
    <span class="featcap"><span><span class="nm">${esc(i.name)}</span><span class="sub">${esc(i.brand)} · ${i.ml} ml · en ${esc(i.b.name)}</span></span>
    <span class="pz"><b>${eur(i.b.p)}</b><span>${R.pct(i.dr.pct)} frente a su media</span></span></span></a>`}
function factsList(st){return `<ul class="facts"><li><b>${st.drops}</b><span>bajan hoy</span></li>${st.save?`<li><b>${eur(st.save.s.save,0)}</b><span>de ahorro en ${esc(st.save.x.cur.name)}</span></li>`:''}<li><b>${st.shops}</b><span>perfumerías comparadas</span></li></ul>`}
"""

COMMON_CSS = """
.tfam{display:none}
.famg{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:12px}
.famc{display:flex;flex-direction:column;justify-content:space-between;gap:12px;min-height:150px;padding:16px;border:0;border-radius:12px;text-align:left;cursor:pointer;font:inherit;color:inherit;overflow:hidden}
.famt{display:flex;justify-content:space-between;align-items:baseline;gap:8px}
.famn{font-size:18px;font-weight:600}
.famk{font-size:13px;opacity:.75;white-space:nowrap}
.famph{display:flex;gap:6px;align-items:flex-end}
.famph img{width:56px;height:64px;object-fit:contain;mix-blend-mode:multiply}
.fams{margin-top:48px}
.sec{font-size:18px;font-weight:600;margin:0 0 16px}
.olf{margin-top:28px;padding:20px;border-radius:12px;display:grid;gap:16px}
.olf-fam{display:flex;align-items:center;gap:12px}
.olf-fam i{width:36px;height:36px;border-radius:50%;background:var(--fam);flex:none}
.olf-fam small{display:block;font-size:12px;opacity:.7}
.olf-fam b{font-weight:600}
.olf-notes{display:flex;flex-wrap:wrap;gap:8px;margin:0;padding:0;list-style:none}
.olf-notes li{padding:6px 12px;border-radius:999px;font-size:14px;background:color-mix(in srgb,var(--fam) 18%,transparent);border:1px solid color-mix(in srgb,var(--fam) 35%,transparent)}
.olf-se{display:grid;grid-template-columns:repeat(4,1fr);gap:4px}
.olf-se span{text-align:center;font-size:12px;padding:6px 0;border-radius:6px;color:var(--muted);background:color-mix(in srgb,currentColor 6%,transparent)}
.olf-se span.on{color:var(--text);background:color-mix(in srgb,var(--fam) 22%,transparent);font-weight:500}
.featph{position:relative}
.feat{display:block;text-decoration:none;color:inherit}
.feat .ph{aspect-ratio:4/3;max-height:min(52vh,460px);width:100%}
.feat .ph img{width:70%;height:70%}
.feat .ph svg{height:72%;width:auto}
.featcap{display:flex;justify-content:space-between;align-items:baseline;gap:16px;margin-top:14px}
.feat .nm{font-size:22px;display:block}
.feat .sub{display:block;font-size:13px;opacity:.7;margin-top:4px}
.feat .pz{text-align:right;white-space:nowrap}
.feat .pz b{display:block;font-size:20px;font-weight:600}
.feat .pz span{font-size:13px}
.feat .tag{position:absolute;left:16px;top:16px;border-radius:6px;padding:4px 10px;font-size:12px}
.facts{display:flex;flex-wrap:wrap;gap:12px 32px;margin:28px 0 0;padding:0;list-style:none}
.facts b{display:block;font-size:30px;line-height:1.1;font-weight:500}
.facts span{font-size:13px;opacity:.75}
.mbrand{display:none}
@media (max-width:860px){.mbrand{display:flex}.facts{gap:12px 20px}.facts b{font-size:24px}.famc{min-height:120px}}
.mq{position:fixed;left:50%;bottom:16px;transform:translateX(-50%);z-index:50;display:flex;gap:2px;padding:4px;background:#fff;border:1px solid #d9d8d3;border-radius:10px;box-shadow:0 4px 16px rgba(0,0,0,.12);font:500 13px/1 system-ui,sans-serif;max-width:calc(100vw - 16px);overflow-x:auto}
.mq a{padding:8px 11px;border-radius:7px;text-decoration:none;color:#3d3b36;white-space:nowrap}
.mq a[aria-current="page"]{background:#16150f;color:#fff}
@media (max-width:620px){.mq{bottom:calc(8px + env(safe-area-inset-bottom))}.mq .long{display:none}}
"""

ESTELA_MARK = """<svg class="mark" width="34" height="22" viewBox="0 0 34 22" aria-hidden="true"><path d="M3 17c6 0 8-11 15-11s6 7 13 4" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/><circle cx="3" cy="17" r="2.6" fill="var(--accent)"/></svg>"""


def brand(name="Estela", sub="precios de perfume", mark=ESTELA_MARK):
    return f'<a class="brandmark" href="#" aria-label="{name}, inicio">{mark}<span><b>{name}</b><small>{sub}</small></span></a>'


def mbrand(name="Estela", mark=ESTELA_MARK):
    return f'<span class="mbrand">{mark}<b>{name}</b></span>'


THEMES = [
# ------------------------------------------------------------------ 1 · Noche: perfumería de lujo nocturna (fondo oscuro, atrevido)
dict(file="tema-1.html", short="Noche", title="Estela · Noche",
 idea="Escaparate nocturno: fondo de tinta, cada frasco en su vitrina iluminada y detalles en oro",
 fonts="family=Cormorant+Garamond:wght@400;500;600&family=Jost:wght@400;500;600",
 css="""
:root{--chrome:#0e0c0a;--sheet:#15120f;--raised:#1d1915;--active:#2a241e;--border:#2c261f;--rule:#2a241e;--control:#4a4036;
 --text:#efe6d8;--muted:#a99b87;--accent:#c9a46a;--positive:#9fd2a6;--pos-bg:#1f3326;--pos-ink:#bfe8c5;--display:"Cormorant Garamond",Georgia,serif;--r-card:4px}
body{font-family:Jost,system-ui,sans-serif;background:var(--chrome)}
.sheet{border-color:var(--border)}
.brandmark b{font:500 30px/1 var(--display);color:var(--accent);display:block}
.brandmark small{display:block;font-size:11px;color:var(--muted);margin-top:2px}
.brandmark{text-decoration:none;gap:12px}.mark{color:var(--accent)}
.search input,.bsearch,.head select,.sizes button,.target input,.more{background:var(--raised);border-color:var(--border);color:var(--text)}
.tile .ph,.pdp .ph,.feat .ph{background:radial-gradient(120% 90% at 50% 0%,#f6ecdc 0%,#e7d8c0 55%,#cdb796 100%)!important;border-radius:4px}
.tile .ph img,.pdp .ph img,.feat .ph img{mix-blend-mode:multiply}
.tile h2,h1,.feat .nm{font-family:var(--display);font-weight:500}
.tile h2{font-size:22px}
.tile .badge{background:#1a1510;color:var(--accent);border:1px solid #4a3b26}
.tile .deal{background:#1a1510;color:var(--text)}
.cta{background:var(--accent);color:#16120c}
.hero{position:relative;text-align:center;padding:40px 0 56px;margin:-24px -32px 40px;background:radial-gradient(80% 70% at 50% 30%,#2a2118 0%,#15120f 70%);border-bottom:1px solid var(--border)}
.hero .kick{color:var(--accent);font-size:13px;margin:0 0 12px}
.hero h1{font:500 64px/1 var(--display);margin:0 auto;max-width:14ch}
.hero .lede{color:var(--muted);max-width:52ch;margin:16px auto 0;font-size:16px}
.hero .feat{max-width:480px;margin:32px auto 0;text-align:left}
.hero .feat .ph{aspect-ratio:16/11;max-height:340px}
.hero .feat .tag{background:#16120c;color:var(--accent)}
.hero .facts{justify-content:center}
.hero .facts b{font-family:var(--display);color:var(--accent);font-size:38px}
.feat .pz span{color:var(--positive)}
.famc{background:var(--raised);color:var(--text);border:1px solid var(--border)}
.famc .famn{font-family:var(--display);font-size:24px;font-weight:500;color:color-mix(in srgb,var(--fam) 60%,#fff)}
.famph img{background:#efe4d2;border-radius:3px;padding:2px}
.olf{background:var(--raised);border:1px solid var(--border)}
.sec,.strip>h2,.sr{font-family:var(--display);font-weight:500;font-size:26px}
.offers td{border-color:var(--rule)}
.thumbs button{background:#efe4d2}
.mbrand{align-items:center;gap:10px;justify-content:center;color:var(--accent);margin-bottom:16px}.mbrand b{font:500 26px/1 var(--display)}
@media (max-width:860px){.hero{margin:-16px -16px 32px;padding:28px 16px 40px}.hero h1{font-size:42px}}
""",
 hero=r"""function hero(st){return `<section class="hero" aria-labelledby="hTitle">__MB__<p class="kick">${today()}</p><h1 id="hTitle">El precio que deja huella</h1>
   <p class="lede">Seguimos ${st.n} perfumes en ${st.shops} perfumerías y te enseñamos dónde cuesta menos cada uno, y cuáles bajan hoy.</p>
   ${featCard(st.top)}${factsList(st)}</section>`}"""),

# ------------------------------------------------------------------ 2 · Revista: moda editorial (papel crema, intermedio)
dict(file="tema-2.html", short="Revista", title="Estela · Revista",
 idea="Revista de moda: papel crema, cabecera de cabecero editorial con número del día y una rejilla con ritmo (piezas grandes)",
 fonts="family=Playfair+Display:wght@400;500;600&family=Instrument+Sans:wght@400;500;600",
 css="""
:root{--chrome:#efe8dc;--sheet:#f7f2e9;--raised:#ece4d6;--active:#e3d9c8;--border:#ddd2bf;--rule:#e2d8c7;--control:#c9bca5;
 --text:#1d1a15;--muted:#5f574b;--accent:#a3361f;--display:"Playfair Display",Georgia,serif;--r-card:2px}
body{font-family:"Instrument Sans",system-ui,sans-serif}
.brandmark{text-decoration:none;gap:10px}.brandmark b{font:600 28px/1 var(--display);display:block}.brandmark small{display:block;font-size:11px;color:var(--muted);margin-top:3px}
.mark{color:var(--accent)}
.tile h2,h1{font-family:var(--display)}
.tile .ph{border-radius:2px}
.grid > .tile:nth-child(7n+1){grid-column:span 2;grid-row:span 2}
.grid > .tile:nth-child(7n+1) .ph{aspect-ratio:auto;height:calc(100% - 96px);min-height:420px}
.grid > .tile:nth-child(7n+1) h2{font-size:30px}
.tile .badge{background:var(--accent);color:#fff;border-radius:2px}
.tfam{display:block;font-size:12px;font-weight:600;margin-top:10px;padding-left:8px;border-left:3px solid var(--fam)}
.tile .br{margin-top:2px}
.cta{background:var(--accent)}
.hero{margin:-24px -32px 40px;padding:0 32px 40px;border-bottom:2px solid var(--text)}
.mast{display:flex;justify-content:space-between;align-items:baseline;gap:16px;border-bottom:1px solid var(--text);padding:20px 0 12px;font-size:13px;color:var(--muted)}
.mast b{font:600 64px/1 var(--display);color:var(--text)}
.hgrid{display:grid;grid-template-columns:minmax(0,1.25fr) minmax(0,1fr);gap:48px;margin-top:32px;align-items:center}
.hero h1{font:500 58px/1.02 var(--display);margin:0}
.hero h1 em{font-style:italic;color:var(--accent)}
.hero .lede{font-size:17px;color:var(--muted);margin:20px 0 0;max-width:44ch}
.hero .feat .ph{aspect-ratio:4/5;max-height:58vh}
.feat .nm{font-family:var(--display);font-size:26px}
.feat .tag{background:var(--accent);color:#fff}
.feat .pz span{color:var(--accent)}
.facts b{font-family:var(--display)}
.famc{background:var(--sheet);border:1px solid var(--border);border-top:6px solid var(--fam);border-radius:2px}
.famn{font-family:var(--display);font-size:24px;font-weight:500}
.olf{background:var(--raised)}
.sec,.strip>h2,.sr{font-family:var(--display);font-weight:500;font-size:30px;border-top:1px solid var(--text);padding-top:12px}
.mbrand{align-items:center;gap:8px}.mbrand b{font:600 28px/1 var(--display)}
@media (max-width:1100px){.hgrid{grid-template-columns:1fr}.mast b{font-size:44px}}
@media (max-width:860px){.hero{margin:-16px -16px 32px;padding:0 16px 32px}.hero h1{font-size:38px}.mast b{font-size:40px}
 .grid > .tile:nth-child(7n+1){grid-column:span 2;grid-row:auto}.grid > .tile:nth-child(7n+1) .ph{height:auto;min-height:0;aspect-ratio:1}}
""",
 hero=r"""function hero(st){const n=Math.floor((Date.now()-new Date('2026-10-01'))/864e5);
  return `<section class="hero" aria-labelledby="hTitle"><div class="mast"><b>Estela</b><span>Número ${n} · ${today()} · ${st.drops} perfumes bajan hoy</span></div>
  <div class="hgrid"><div><h1 id="hTitle">El precio que <em>deja huella</em></h1>
  <p class="lede">Seguimos ${st.n} perfumes en ${st.shops} perfumerías españolas. Cada día, lo que baja, dónde cuesta menos y cómo huele.</p>${factsList(st)}</div>
  ${featCard(st.top,'Portada de hoy')}</div></section>`}"""),

# ------------------------------------------------------------------ 3 · Botánica: materias primas (salvia y ámbar, intermedio)
dict(file="tema-3.html", short="Botánica", title="Estela · Botánica",
 idea="Herbario: se entra por lo que te gusta oler; cada familia tiene su color de ingrediente y las notas son los protagonistas",
 fonts="family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600&family=Work+Sans:wght@400;500;600",
 css="""
:root{--chrome:#e9ebdf;--sheet:#f6f5ee;--raised:#ecebe0;--active:#dfe2d2;--border:#d8dbc9;--rule:#e1e3d5;--control:#b9bea6;
 --text:#1f2a1f;--muted:#5d6656;--accent:#9a5b22;--positive:#2f6b3a;--pos-bg:#dcebd6;--pos-ink:#1f4a28;--display:"Fraunces",Georgia,serif;--r-card:14px}
body{font-family:"Work Sans",system-ui,sans-serif}
.brandmark{text-decoration:none;gap:10px}.brandmark b{font:500 28px/1 var(--display);display:block}.brandmark small{display:block;font-size:11px;color:var(--muted);margin-top:3px}
.mark{color:#2f6b3a}
h1,.tile h2{font-family:var(--display);font-weight:500}
.tile .ph{background:color-mix(in srgb,var(--fam) 16%,#f6f5ee)!important;border-radius:14px}
.tfam{display:inline-flex;align-items:center;gap:6px;font-size:12px;color:var(--muted);margin-top:10px}
.tfam::before{content:"";width:10px;height:10px;border-radius:50%;background:var(--fam)}
.tile .br{margin-top:2px}
.cta{background:#2f4a2f}
.hero{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:40px;align-items:center;padding:8px 0 40px}
.hero .kick{font-size:13px;color:#2f6b3a;margin:0 0 12px}
.hero h1{font:400 54px/1.04 var(--display);margin:0;max-width:14ch}
.hero .lede{font-size:17px;color:var(--muted);max-width:44ch;margin:18px 0 0}
.chips{display:flex;flex-wrap:wrap;gap:8px;margin-top:24px}
.fchip{display:inline-flex;align-items:center;gap:8px;height:40px;padding:0 14px;border-radius:999px;border:1px solid color-mix(in srgb,var(--fam) 45%,transparent);background:color-mix(in srgb,var(--fam) 14%,#fff);cursor:pointer;font:inherit;color:var(--text)}
.fchip i{width:12px;height:12px;border-radius:50%;background:var(--fam)}
.feat .ph{border-radius:20px}
.feat .tag{background:#fff;color:#2f6b3a}
.feat .nm{font-family:var(--display);font-size:24px}
.feat .pz span{color:var(--positive)}
.facts b{font-family:var(--display);color:#2f4a2f}
.fams{order:-1}
.famc{background:color-mix(in srgb,var(--fam) 22%,#f6f5ee);border-radius:18px}
.famn{font-family:var(--display);font-size:24px;font-weight:500}
.olf{background:color-mix(in srgb,var(--fam) 10%,#fff);border:1px solid color-mix(in srgb,var(--fam) 30%,transparent)}
.olf-notes li{font-family:var(--display);font-size:16px;padding:8px 14px}
.sec,.strip>h2,.sr{font-family:var(--display);font-weight:500;font-size:26px}
.mbrand{align-items:center;gap:8px;margin-bottom:12px}.mbrand b{font:500 26px/1 var(--display)}
@media (max-width:1100px){.hero{grid-template-columns:1fr}}
@media (max-width:860px){.hero h1{font-size:36px}}
""",
 hero=r"""function hero(st){return `<section class="hero" aria-labelledby="hTitle"><div>__MB__<p class="kick">${today()}</p>
   <h1 id="hTitle">Empieza por lo que te gusta oler</h1>
   <p class="lede">${st.n} perfumes, ordenados por sus materias primas y comparados en ${st.shops} perfumerías. Elige una familia:</p>
   <div class="chips">${FAMS.map(([k,n,c])=>`<button class="fchip" type="button" data-fam="${k}" style="--fam:${c}"><i></i>${n}</button>`).join('')}</div>
   ${factsList(st)}</div>${featCard(st.top)}</section>`}"""),

# ------------------------------------------------------------------ 4 · Viva: tienda moderna (bloques de color por familia, color por secciones)
dict(file="tema-4.html", short="Viva", title="Estela · Viva",
 idea="Tienda viva: cabecera de color fuerte, las tres mayores bajadas como carteles y cada tarjeta teñida con el color de su familia",
 fonts="family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,600&family=DM+Sans:opsz,wght@9..40,400;9..40,500;9..40,600",
 css="""
:root{--chrome:#fff;--sheet:#fff;--raised:#f4f2ee;--active:#ebe8e2;--border:#e8e4dc;--rule:#eeebe5;--control:#cfc9be;
 --text:#141210;--muted:#5f5a52;--accent:#c63a15;--display:"Bricolage Grotesque",system-ui,sans-serif;--r-card:18px}
body{font-family:"DM Sans",system-ui,sans-serif}
.sheet{border:0;border-radius:0}
.brandmark{text-decoration:none;gap:10px}.brandmark b{font:600 26px/1 var(--display);letter-spacing:-.02em;display:block}.brandmark small{display:block;font-size:11px;color:var(--muted)}
.mark{color:var(--accent)}
.tile h2,h1{font-family:var(--display);font-weight:600;letter-spacing:-.01em}
.tile .ph{background:color-mix(in srgb,var(--fam) 34%,#fff)!important;border-radius:18px}
.tile .badge{background:var(--text);color:#fff;border-radius:999px;padding:3px 10px}
.tile .deal{border-radius:999px}
.tfam{display:inline-block;margin-top:10px;font-size:12px;font-weight:600;padding:2px 8px;border-radius:999px;background:color-mix(in srgb,var(--fam) 25%,#fff)}
.tile .br{margin-top:4px}
.cta{background:var(--accent);border-radius:999px}
.hero{margin:-24px -32px 40px;padding:36px 32px 40px;background:#c63a15;color:#fff}
.hero .kick{font-size:14px;margin:0 0 8px}
.hero h1{font:600 60px/.98 var(--display);letter-spacing:-.03em;margin:0;max-width:16ch}
.hero .lede{font-size:17px;margin:14px 0 0;max-width:52ch;opacity:.95}
.posters{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px;margin-top:28px}
.poster{display:grid;grid-template-rows:auto 1fr;background:#fff;color:var(--text);border-radius:22px;overflow:hidden;text-decoration:none}
.poster .ph{aspect-ratio:4/3;border-radius:0}
.poster .pinfo{padding:14px 16px 16px;display:flex;justify-content:space-between;gap:12px;align-items:end}
.poster .pinfo b{display:block;font:600 20px/1.1 var(--display)}
.poster .pinfo small{font-size:13px;color:var(--muted)}
.poster .pct{font:600 34px/1 var(--display);color:var(--accent);white-space:nowrap}
.hero .facts b{font-family:var(--display);font-weight:600}
.hero .facts span{opacity:.9}
.famc{background:color-mix(in srgb,var(--fam) 55%,#fff);color:#141210;border-radius:22px}
.famn{font-family:var(--display);font-size:26px}
.famph img{background:#fff;border-radius:10px;padding:4px;mix-blend-mode:normal}
.olf{background:color-mix(in srgb,var(--fam) 20%,#fff);border-radius:20px}
.sec,.strip>h2,.sr{font-family:var(--display);font-weight:600;font-size:28px;letter-spacing:-.01em}
.mbrand{align-items:center;gap:8px;margin-bottom:14px;color:#fff}.mbrand b{font:600 26px/1 var(--display)}.mbrand .mark{color:#fff}
@media (max-width:1100px){.posters{grid-template-columns:1fr 1fr}.posters .poster:nth-child(3){display:none}}
@media (max-width:860px){.hero{margin:-16px -16px 28px;padding:24px 16px 28px}.hero h1{font-size:38px}.posters{grid-template-columns:1fr}.posters .poster:nth-child(n+2){display:none}}
""",
 hero=r"""function hero(st){return `<section class="hero" aria-labelledby="hTitle">__MB__<p class="kick">${today()}</p>
   <h1 id="hTitle">Hoy bajan ${st.drops} perfumes</h1><p class="lede">Comparamos ${st.n} perfumes en ${st.shops} perfumerías. Estas son las bajadas más fuertes:</p>
   <div class="posters">${st.tops.map(t=>`<a class="poster" href="#p/${t.key}" style="--fam:${(famOf(t.cur)||[])[2]||'#ccc'}">${pic(t.cur)}</div><span class="pinfo"><span><b>${esc(t.cur.name)}</b><small>${esc(t.cur.brand)} · ${eur(t.cur.b.p)} en ${esc(t.cur.b.name)}</small></span><span class="pct">${R.pct(t.cur.dr.pct)}</span></span></a>`).join('')}</div>
   ${factsList(st)}</section>`}"""),

# ------------------------------------------------------------------ 5 · Clara: la página actual con alma (contenida)
dict(file="tema-5.html", short="Clara", title="Estela · Clara",
 idea="La página de ahora con alma: base clara cálida, barra superior en tinta, foto destacada a sangre y ritmo de secciones",
 fonts="family=IBM+Plex+Sans:wght@400;500;600&family=Bodoni+Moda:opsz,wght@6..96,400;6..96,500",
 css="""
:root{--chrome:#16150f;--sheet:#fbf9f5;--raised:#f2eee6;--active:#ebe6dc;--border:#e6e0d4;--rule:#ece7dd;--accent:#8a5a1c}
.shell{background:#16150f}
.brandmark{text-decoration:none;gap:12px;color:#f4efe6}.brandmark b{font:500 28px/1 var(--display);display:block}.brandmark small{display:block;font-size:11px;color:#b9b2a5;margin-top:3px}
.mark{color:#f4efe6}
.topbar .search input{background:#26241d;border-color:#36332a;color:#f4efe6}
.topbar .search .ic,.menu,.tchollos{color:#f4efe6}
aside{background:#fbf9f5}
.sheet{border:0;border-radius:0}
@media (min-width:861px){aside{border-top-left-radius:0}.shell{grid-template-rows:64px minmax(0,1fr)}}
.tfam{display:inline-flex;align-items:center;gap:6px;font-size:12px;color:var(--muted);margin-top:10px}
.tfam::before{content:"";width:8px;height:8px;border-radius:50%;background:var(--fam)}
.tile .br{margin-top:2px}
.hero{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.1fr);margin:-24px -32px 40px;min-height:440px}
.hero .txt{padding:48px 40px;display:flex;flex-direction:column;justify-content:center;background:var(--raised)}
.hero .kick{font-size:13px;color:var(--accent);margin:0 0 14px}
.hero h1{font:400 56px/1.02 var(--display);margin:0;max-width:12ch}
.hero .lede{font-size:16px;color:var(--muted);margin:18px 0 0;max-width:44ch}
.hero .feat{position:relative;display:block}
.hero .feat .ph{aspect-ratio:auto;height:100%;max-height:none;border-radius:0}
.hero .featcap{position:absolute;left:24px;right:24px;bottom:20px;background:#fbf9f5;border-radius:10px;padding:14px 16px;margin:0}
.feat .nm{font-family:var(--display)}
.feat .tag{background:#16150f;color:#f4efe6}
.feat .pz span{color:var(--positive)}
.facts b{font-family:var(--display);font-weight:400}
.famc{background:#fff;border:1px solid var(--border)}
.famc .famn::before{content:"";display:inline-block;width:10px;height:10px;border-radius:50%;background:var(--fam);margin-right:8px}
.olf{background:var(--raised)}
.sec,.strip>h2,.sr{font-family:var(--display);font-weight:500;font-size:26px}
.mbrand{align-items:center;gap:8px;margin-bottom:12px}.mbrand b{font:500 26px/1 var(--display)}.mbrand .mark{color:var(--text)}
@media (max-width:1100px){.hero{grid-template-columns:1fr}.hero .feat .ph{aspect-ratio:4/3}}
@media (max-width:860px){.hero{margin:-16px -16px 28px}.hero .txt{padding:24px 16px}.hero h1{font-size:36px}.topbar{background:#16150f}}
""",
 hero=r"""function hero(st){return `<section class="hero" aria-labelledby="hTitle"><div class="txt">__MB__<p class="kick">${today()}</p>
   <h1 id="hTitle">El precio que deja huella</h1><p class="lede">Seguimos ${st.n} perfumes en ${st.shops} perfumerías españolas y te enseñamos dónde cuesta menos cada uno, y cuáles bajan hoy.</p>
   ${factsList(st)}</div>${featCard(st.top)}</section>`}"""),

# ------------------------------------------------------------------ 6 · Mediterráneo: idea propia (terracota y cobalto, atrevido)
dict(file="tema-6.html", short="Mediterráneo", title="Estela · Mediterráneo",
 idea="Verano mediterráneo: arena, terracota y azul cobalto; un friso de azulejo como firma y el sol de la tarde en las fotos",
 fonts="family=DM+Serif+Display&family=Manrope:wght@400;500;600",
 css="""
:root{--chrome:#efe2cc;--sheet:#f7eedf;--raised:#ede0c9;--active:#e4d4b8;--border:#ddcaa9;--rule:#e3d3b7;--control:#c8b18c;
 --text:#22201c;--muted:#6b5f4d;--accent:#1f3c88;--positive:#1f3c88;--pos-bg:#dfe6f6;--pos-ink:#1f3c88;--display:"DM Serif Display",Georgia,serif;--r-card:10px}
body{font-family:Manrope,system-ui,sans-serif}
.brandmark{text-decoration:none;gap:10px}.brandmark b{font:400 30px/1 var(--display);color:#9e4423;display:block}.brandmark small{display:block;font-size:11px;color:var(--muted)}
.mark{color:#9e4423}
h1,.tile h2{font-family:var(--display);font-weight:400}
.tile .ph{background:linear-gradient(180deg,#f8e9d2,#ecd3ae)!important}
.tile .badge{background:var(--accent);color:#fff}
.tfam{display:block;font-size:12px;color:#9e4423;font-weight:600;margin-top:10px}
.tile .br{margin-top:2px}
.cta{background:var(--accent)}
.friso{height:14px;margin:-24px -32px 0;background:
  conic-gradient(from 45deg at 50% 50%,#1f3c88 0 25%,transparent 0 50%,#1f3c88 0 75%,transparent 0) 0 0/14px 14px,#f7eedf}
.hero{margin:0 -32px 40px;background:#1f3c88;color:#f7eedf;display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:40px;padding:40px 32px 44px;align-items:center}
.hero .kick{font-size:13px;color:#f2b98f;margin:0 0 12px}
.hero h1{font:400 60px/1 var(--display);margin:0;max-width:13ch}
.hero .lede{font-size:16px;margin:18px 0 0;max-width:44ch;color:#dbe2f2}
.hero .feat .ph{background:radial-gradient(90% 80% at 70% 20%,#ffd9a8,#e9a46f 60%,#c8643b)!important;border-radius:200px 200px 12px 12px}
.hero .feat .tag{background:#f7eedf;color:#1f3c88;left:50%;transform:translateX(-50%)}
.feat .nm{font-family:var(--display);font-size:26px}
.hero .feat .pz span{color:#f2b98f}
.hero .feat .sub{color:#dbe2f2;opacity:1}
.hero .facts b{font-family:var(--display);font-weight:400;color:#f2b98f}
.famc{background:var(--sheet);border:2px solid var(--fam);border-radius:12px}
.famn{font-family:var(--display);font-size:24px;font-weight:400}
.olf{background:#fff7ea;border:2px solid var(--accent)}
.sec,.strip>h2,.sr{font-family:var(--display);font-weight:400;font-size:28px;color:#9e4423}
.mbrand{align-items:center;gap:8px;margin-bottom:12px;color:#f2b98f}.mbrand b{font:400 28px/1 var(--display)}.mbrand .mark{color:#f2b98f}
@media (max-width:1100px){.hero{grid-template-columns:1fr}}
@media (max-width:860px){.hero{margin:0 -16px 28px;padding:24px 16px 28px}.hero h1{font-size:38px}.friso{margin:-16px -16px 0}}
""",
 hero=r"""function hero(st){return `<div class="friso" aria-hidden="true"></div><section class="hero" aria-labelledby="hTitle"><div>__MB__<p class="kick">${today()}</p>
   <h1 id="hTitle">El precio que deja huella</h1><p class="lede">Seguimos ${st.n} perfumes en ${st.shops} perfumerías españolas y te enseñamos dónde cuesta menos cada uno, y cuáles bajan hoy.</p>
   ${factsList(st)}</div>${featCard(st.top,'Bajada del día')}</section>`}"""),
]


def switch(current):
    out = []
    for t in THEMES:
        k = t["file"][5]
        cur = ' aria-current="page"' if t["file"] == current else ""
        out.append(f'<a href="{t["file"]}"{cur}>{k}<span class="long"> · {t["short"]}</span></a>')
    out.append('<a href="../index.html">Actual</a>')
    return '<nav class="mq" aria-label="Maquetas de diseño">' + "".join(out) + "</nav>"


def build(t):
    s = BASE
    def rep(a, b, n=1):
        nonlocal s
        assert a in s, (t["file"], a[:80])
        s = s.replace(a, b, n)
    # cabecera de la página
    i0 = s.index("<title>"); i1 = s.index("</title>")
    s = s[:i0] + f'<title>{t["title"]}</title><meta name="robots" content="noindex">' + s[i1 + 8:]
    s = s.replace('family=IBM+Plex+Sans:wght@400;500;600&family=Bodoni+Moda:opsz,wght@6..96,400;6..96,500', t["fonts"])
    # fuera el estilo de la portada de Estela (cada tema trae la suya)
    a = s.index(".hero{display:grid;grid-template-columns:minmax(0,1.1fr) minmax(0,1fr)")
    b = s.index("\n", s.index(".mbrand{display:none;align-items:center;gap:8px;margin:0 0 20px")) + 1
    s = s[:a] + ".cat{font:500 26px/1.1 var(--display);margin:0}\n" + s[b:]
    rep("</style>", COMMON_CSS + t["css"] + "</style>")
    # marca: la de Estela con la tipografía de cada tema
    a = s.index('<a class="brandmark"'); b = s.index("</a>", a) + 4
    s = s[:a] + brand() + s[b:]
    # rutas desde /maquetas
    rep("""<script>document.write('<script src="maquetas/core.js?v='""", """<script>document.write('<script src="core.js?v='""")
    rep("D=await R.load('data/');", "D=await R.load('../data/');")
    # el hero de Estela se sustituye por el del tema
    a = s.index("\nfunction hero(st){"); b = s.index("\nfunction catalog(){")
    s = s[:a] + "\n" + t["hero"].replace("__MB__", mbrand()) + s[b:]
    # stats del tema (más datos que la de producción)
    a = s.index("\nfunction stats(){"); b = s.index("\n}\n", a) + 3
    s = s[:a] + "\n" + COMMON_JS + s[b:]
    # familia en tarjetas, sección por familia y "cómo huele" en la ficha
    rep('<a class="tile" href="#p/${x.key}">', '<a class="tile" href="#p/${x.key}" style="--fam:${(famOf(i)||[])[2]||\'#bbb\'}">')
    rep('<h2>${esc(i.name)}</h2>', '<span class="tfam">${(famOf(i)||[])[1]||\'\'}</span><h2>${esc(i.name)}</h2>')
    rep("${g.length?`${drops.length?'<h2 class=\"sr\">Todos</h2>':''}", "${dirty.length?'':famsSection()}${g.length?`${drops.length?'<h2 class=\"sr\">Todos</h2>':''}")
    rep("<h2>Precio en cada tienda</h2>", "${olf(i)}<h2>Precio en cada tienda</h2>")
    rep("</body>", switch(t["file"]) + "\n</body>")
    (ROOT / "maquetas" / t["file"]).write_text(s)


for t in THEMES:
    build(t)
print("ok:", ", ".join(t["file"] for t in THEMES))
