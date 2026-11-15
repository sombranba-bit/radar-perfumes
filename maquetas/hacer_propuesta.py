"""Genera maquetas/propuesta.html: la página actual con todos los cambios de la auditoría del 15-nov.
Uso: python3 maquetas/hacer_propuesta.py"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
s = (ROOT / "index.html").read_text()


def rep(a, b, n=1):
    global s
    assert s.count(a) >= 1, a[:90]
    s = s.replace(a, b, n)


# ---------------------------------------------------------------- maqueta: rutas, aviso y selector
rep("<title>Estela · precios de perfume</title>", '<title>Estela · propuesta</title><meta name="robots" content="noindex">')
rep("""<script>document.write('<script src="maquetas/core.js?v='""", """<script>document.write('<script src="core.js?v='""")
rep("D=await R.load('data/');", "D=await R.load('../data/');")

# ---------------------------------------------------------------- CSS nuevo
CSS = """
/* ===== Propuesta (auditoría 15-nov) ===== */
.skip{position:absolute;left:12px;top:-60px;z-index:100;background:#fff;color:var(--text);padding:10px 14px;border-radius:8px;font-weight:600;text-decoration:none}
.skip:focus{top:10px}
/* tarjetas: 4 líneas (marca con punto de familia, nombre, precio + ahorro, tienda y nº de tiendas) */
.tfam{display:none!important}
.tile .br{display:flex;align-items:center;gap:6px;margin-top:10px}
.tile .br .fd{width:8px;height:8px;border-radius:50%;background:var(--fam);flex:none}
.tile .pr{justify-content:flex-start;gap:8px;align-items:center}
.save{font-size:12px;font-weight:600;color:#14532d;background:#e3f4e8;border-radius:999px;padding:2px 8px;white-space:nowrap}
.tile .cmp{white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.tile h2{margin:2px 0 6px}
/* cabecera del catálogo en una fila */
.head{align-items:center;flex-wrap:nowrap}
.head label{display:flex;align-items:center;gap:8px;white-space:nowrap;color:var(--muted);font-size:13px}
.head select{height:36px}
@media (max-width:860px){.head>div{min-width:0}.head .meta{white-space:nowrap}.head label{font-size:0;gap:0}.head select{max-width:52vw}}
.famt{flex-direction:column;align-items:flex-start;gap:2px}
.tchollos+.tchollos{margin-left:20px!important}
/* filtros como pastillas */
.fgroup:not(.fbrand){display:flex;flex-wrap:wrap;gap:6px}
.fgroup:not(.fbrand) legend{width:100%;padding:0 2px;margin-bottom:6px}
.fgroup:not(.fbrand) .opt{width:auto;min-height:32px;padding:0 12px;border-radius:999px;border:1px solid var(--border);background:#fff}
.fgroup:not(.fbrand) .opt[aria-pressed="true"]{background:var(--text);color:#fff;border-color:var(--text)}
/* familias: 2 columnas compactas en el móvil */
@media (max-width:860px){.famg{grid-template-columns:1fr 1fr;gap:8px}.famc{min-height:0;padding:12px 14px;gap:4px}.famph{display:none}.famt{flex-direction:column;align-items:flex-start;gap:0}.famn{font-size:16px}}
/* ficha */
.pdp-top{display:flex;justify-content:space-between;align-items:flex-start;gap:12px}
.fav{display:inline-flex;align-items:center;gap:6px;height:40px;padding:0 14px;border:1px solid var(--control);border-radius:999px;background:#fff;cursor:pointer;font:inherit;white-space:nowrap}
.fav[aria-pressed="true"]{background:var(--text);color:#fff;border-color:var(--text)}
.fav svg{flex:none}
.hist{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-top:12px}
.hist div{background:var(--raised);border-radius:8px;padding:10px 12px}
.hist small{display:block;color:var(--muted);font-size:12px}
.hist b{font-size:18px;font-weight:600}
.tstatus{margin:10px 0 0;font-size:14px;color:var(--muted)}
.tstatus.ok{color:var(--positive);font-weight:500}
.buybar{display:none}
@media (max-width:860px){
  .pdp .ph{aspect-ratio:4/3;max-height:34vh}
  .credit{display:none}
  .thumbs button{width:52px;height:52px}
  .pdp h1{font-size:30px}
  .buybar{display:flex;position:fixed;left:0;right:0;bottom:0;z-index:30;align-items:center;justify-content:space-between;gap:12px;padding:10px 16px calc(10px + env(safe-area-inset-bottom));background:#16150f;color:#f4efe6}
  .buybar b{font-size:20px;font-weight:600;display:block}
  .buybar small{font-size:12px;color:#c9c2b5}
  .buybar a{display:inline-flex;align-items:center;height:44px;padding:0 18px;background:#f4efe6;color:#16150f;border-radius:8px;text-decoration:none;font-weight:600;white-space:nowrap}
  .sheet.has-bar{padding-bottom:96px}
}
/* chollos */
.tabs{display:flex;gap:6px;margin:20px 0 4px}
.tabs button{height:36px;padding:0 14px;border-radius:999px;border:1px solid var(--border);background:#fff;cursor:pointer;font:inherit}
.tabs button[aria-pressed="true"]{background:var(--text);color:#fff;border-color:var(--text)}
.deals a{grid-template-columns:auto minmax(0,1fr) auto}
.deals .dph{width:56px;height:56px;border-radius:8px;display:grid;place-items:center;overflow:hidden;background:var(--raised)}
.deals .dph img{width:90%;height:90%;object-fit:contain;mix-blend-mode:multiply}
.deals .dph svg{height:70%;width:auto}
.deals .dt{display:block;font-weight:600;line-height:1.3;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
/* guardados */
.tsave{position:absolute;right:10px;bottom:10px;width:32px;height:32px;border-radius:50%;background:#fff;display:grid;place-items:center;color:var(--text)}
.tbelow{display:inline-block;margin-top:4px;font-size:12px;font-weight:600;color:#14532d}
.gcount{display:inline-grid;place-items:center;min-width:18px;height:18px;padding:0 5px;margin-left:6px;border-radius:9px;background:var(--accent);color:#fff;font-size:11px;font-weight:600}
/* pie */
.foot{margin-top:64px;padding-top:24px;border-top:1px solid var(--rule);display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:24px;color:var(--muted);font-size:14px}
.foot h2{font-size:14px;font-weight:600;color:var(--text);margin:0 0 6px}
.foot p{margin:0}
@media (max-width:860px){.foot{grid-template-columns:1fr}}
/* selector de maqueta */
.mq{position:fixed;left:50%;bottom:16px;transform:translateX(-50%);z-index:50;display:flex;gap:2px;padding:4px;background:#fff;border:1px solid #d9d8d3;border-radius:10px;box-shadow:0 4px 16px rgba(0,0,0,.12);font:500 13px/1 system-ui,sans-serif}
.mq a{padding:8px 12px;border-radius:7px;text-decoration:none;color:#3d3b36;white-space:nowrap}
.mq a[aria-current="page"]{background:#16150f;color:#fff}
@media (max-width:860px){.mq{bottom:calc(16px + env(safe-area-inset-bottom))}.sheet.has-bar~.mq,body:has(.has-bar) .mq{bottom:calc(84px + env(safe-area-inset-bottom))}}
"""
rep("</style>", CSS + "</style>")

# ---------------------------------------------------------------- marcado fijo: saltar al contenido, Guardados, selector
rep("<body>", '<body>\n<a class="skip" href="#sheet">Saltar al contenido</a>')
rep('<a class="tchollos" href="#chollos" data-sec="chollos">Chollos</a>',
    '<a class="tchollos" href="#guardados" data-sec="guardados">Guardados<span class="gcount" id="gc" hidden></span></a><a class="tchollos" href="#chollos" data-sec="chollos">Chollos</a>')
rep('<a href="#chollos" data-sec="chollos">Chollos de Chollometro</a></nav>',
    '<a href="#chollos" data-sec="chollos">Chollos de Chollometro</a><a href="#guardados" data-sec="guardados">Guardados</a></nav>')
rep("</body>", '<nav class="mq" aria-label="Maqueta"><a href="propuesta.html" aria-current="page">Propuesta</a><a href="../index.html">Actual</a></nav>\n</body>')

# ---------------------------------------------------------------- JS: fotos al tamaño justo
rep("""function pic(i,cls='',idx=0){
  const ph=R.photos(i),f=ph[idx];""", """// Tamaño justo: en tarjetas una foto mediana (las tiendas que lo permiten la sirven reducida); en ficha y portada la grande
const TILE_ORDER=['lookfantastic','arabicparfums','firstinfragrance','sabina','paco','parejo','laguna','brasty','perfumesclub','avenida','idealo','sephora','douglas','notino'];
function sized(u,w){
  if(/thgimages\\.com/.test(u))return u.replace(/width=\\d+/,'width='+w).replace(/height=\\d+/,'height='+w);
  if(/\\/cdn\\/shop\\//.test(u))return u.replace(/_\\d+x\\d+(\\.\\w+)/,`_${w}x${w}$1`).replace(/([?&])width=\\d+/,'$1width='+w);
  return u;
}
function photosFor(i,size){const ph=R.photos(i);if(size!=='s')return ph;
  return [...ph].sort((a,b)=>((TILE_ORDER.indexOf(a.s)+99)%99)-((TILE_ORDER.indexOf(b.s)+99)%99)).map(f=>({...f,url:sized(f.url,480)}))}
function pic(i,cls='',idx=0,size='s',eager=false){
  const ph=photosFor(i,size),f=ph[idx];""")
rep("""<img src="${esc(f.url)}" alt="${esc(i.brand+' '+i.name)}" loading="lazy" decoding="async" referrerpolicy="no-referrer">`;""",
    """<img src="${esc(f.url)}" alt="${esc(i.brand+' '+i.name)}" ${eager?'fetchpriority="high"':'loading="lazy"'} decoding="async" referrerpolicy="no-referrer">`;""")
rep("""<a class="feat" href="#p/${t.key}"><div class="featph">${pic(i)}</div>""", """<a class="feat" href="#p/${t.key}"><div class="featph">${pic(i,'',0,'l',true)}</div>""")
rep("""<div id="mainph">${pic(i)}</div>""", """<div id="mainph">${pic(i,'',0,'l',true)}</div>""")
rep("""$('mainph').innerHTML=pic(x.cur,'',k)+'</div>';""", """$('mainph').innerHTML=pic(x.cur,'',k,'l',true)+'</div>';""")
rep("""<img src="${esc(f.url)}" alt="" loading="lazy" referrerpolicy="no-referrer"></button>""", """<img src="${esc(sized(f.url,160))}" alt="" loading="lazy" referrerpolicy="no-referrer"></button>""")
rep("""const ph=m.map(x=>R.photos(x.cur)[0]).filter(Boolean).slice(0,3);""", """const ph=m.map(x=>photosFor(x.cur,'s')[0]).filter(Boolean).map(f=>({...f,url:sized(f.url,160)})).slice(0,3);""")

# ---------------------------------------------------------------- JS: guardados y objetivo
rep("let D=null,S=R.readState(),limit=24,sizeSel={},bq='';", """let D=null,S=R.readState(),limit=24,sizeSel={},bq='',FAM=new URLSearchParams(location.search).get('fam'),dealTab=null,dealLimit=20;
const favs=()=>{try{return JSON.parse(localStorage.getItem('rp-favs')||'[]')}catch(e){return []}};
function toggleFav(k){const f=favs(),on=!f.includes(k);const n=on?[...f,k]:f.filter(x=>x!==k);try{localStorage.setItem('rp-favs',JSON.stringify(n))}catch(e){}gcount();return on}
function below(i){const t=R.targets()[i.id];return t!=null&&i.b&&i.b.p<=t}
function gcount(){const n=favs().length;const g=$('gc');if(g){g.hidden=!n;g.textContent=n}}
const HEART='<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M19 14c1.5-1.5 3-3.3 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.8 0-3 .5-4.5 2-1.5-1.5-2.7-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4 3 5.5l7 7Z"/></svg>';""")

# ---------------------------------------------------------------- JS: tarjeta en 4 líneas
rep("""  return `<a class="tile" href="#p/${x.key}" style="--fam:${(famOf(i)||[])[2]||'#bbb'}">${pic(i)}${i.dr&&i.dr.pct<=-3?`<span class="badge">${R.pct(i.dr.pct)} hoy</span>`:''}${i.deals.length?'<span class="deal">Chollo</span>':''}</div>
  <div class="br">${esc(i.brand)} · ${i.ml} ml${x.vars.length>1?' · '+x.vars.length+' tamaños':''}</div><span class="tfam">${(famOf(i)||[])[1]||''}</span><h2>${esc(i.name)}</h2>
  <div class="pr"><b>${b?eur(b.p):'Sin precio'}</b><span>${b?esc(b.name):''}</span></div>
  ${sp?`<div class="cmp">en ${sp.n} tiendas${sp.save>=1?' · ahorras '+eur(sp.save,0):''}</div>`:''}</a>`;""",
"""  const f=famOf(i),fav=favs().includes(x.key);
  return `<a class="tile" href="#p/${x.key}" style="--fam:${(f||[])[2]||'#bbb'}">${pic(i)}${i.dr&&i.dr.pct<=-3?`<span class="badge">${R.pct(i.dr.pct)} hoy</span>`:''}${i.deals.length?'<span class="deal">Chollo</span>':''}${fav?`<span class="tsave" aria-label="Guardado">${HEART}</span>`:''}</div>
  <div class="br"><i class="fd" title="${(f||[])[1]||''}"></i>${esc(i.brand)} · ${i.ml} ml${x.vars.length>1?' · '+x.vars.length+' tamaños':''}</div><h2>${esc(i.name)}</h2>
  <div class="pr"><b>${b?eur(b.p):'Sin precio'}</b>${sp&&sp.save>=1?`<span class="save">ahorras ${eur(sp.save,0)}</span>`:''}</div>
  ${b?`<div class="cmp">en ${esc(b.name)}${sp?' · '+sp.n+' tiendas':''}</div>`:''}${below(i)?'<span class="tbelow">Por debajo de tu objetivo</span>':''}</a>`;""")

# ---------------------------------------------------------------- JS: filtro de familia de verdad
rep("""document.addEventListener('click',e=>{const b=e.target.closest('[data-fam]');if(!b)return;const n=FAMS.find(f=>f[0]===b.dataset.fam)[1];S.q=n.toLowerCase();$('q').value=n;limit=24;route();scrollTo(0,0)});""",
    """document.addEventListener('click',e=>{const b=e.target.closest('[data-fam]');if(!b)return;FAM=b.dataset.fam;limit=24;if(location.hash)location.hash='';else route();scrollTo(0,0)});""")
rep("""  const g=R.groups(D.items,S,sizeSel),dirty=['q','g','tier','season','brand'].filter(k=>S[k]!==R.DEFAULTS[k]);
  const lab={q:'«'+S.q+'»',g:S.g,tier:S.tier,season:S.season,brand:S.brand};""",
"""  const g=R.groups(D.items,S,sizeSel).filter(x=>!FAM||famOf(x.cur)?.[0]===FAM),dirty=['q','g','tier','season','brand'].filter(k=>S[k]!==R.DEFAULTS[k]);
  if(FAM)dirty.push('fam');
  const lab={q:'«'+S.q+'»',g:S.g,tier:S.tier,season:S.season,brand:S.brand,fam:'Familia '+(FAMS.find(f=>f[0]===FAM)||['',''])[1]};""")
rep("""  if(t.dataset.unset){setF(t.dataset.unset,R.DEFAULTS[t.dataset.unset]);if(t.dataset.unset==='q')$('q').value='';return}""",
    """  if(t.dataset.unset==='fam'){FAM=null;route();return}
  if(t.dataset.unset){setF(t.dataset.unset,R.DEFAULTS[t.dataset.unset]);if(t.dataset.unset==='q')$('q').value='';return}""")
rep("""  if(t.dataset.clearall!==undefined){S={...R.DEFAULTS,sort:S.sort};""", """  if(t.dataset.clearall!==undefined){S={...R.DEFAULTS,sort:S.sort};FAM=null;""")
rep("""<fieldset class="fgroup"><legend>Marca</legend>""", """<fieldset class="fgroup fbrand"><legend>Marca</legend>""")
# cabecera del catálogo compacta
rep("""<label>Ordenar <select id="sort">""", """<label>Ordenar<select id="sort" aria-label="Ordenar">""")
# pie con cómo funciona
rep("""   ${S.q.trim()?webLinks(S.q.trim()):''}`;
}""", """   ${S.q.trim()?webLinks(S.q.trim()):''}${foot()}`;
}
function foot(){return `<footer class="foot"><div><h2>Cómo funciona</h2><p>Varias veces al día leemos el precio de cada tamaño en ${stats().shops} perfumerías. Notino, Primor, Druni, Arenal y Perfumería Julia se leen a través de Idealo.</p></div>
  <div><h2>De dónde salen los datos</h2><p>Precios y fotos son los que publica cada tienda; las fotos se enseñan desde su web, sin copiarlas. No cobramos comisión por los enlaces.</p></div>
  <div><h2>Última lectura</h2><p>${R.agoTime(D.estado?.at)} · <a href="https://github.com/sombranba-bit/radar-perfumes/commits/main" target="_blank" rel="noopener">historial de cambios</a></p></div></footer>`}""")

# ---------------------------------------------------------------- JS: ficha
rep("""    <p class="meta">${esc(i.brand)} · ${esc(R.tierOf(i))}</p><h1>${esc(i.name)}</h1>
    <p class="lead">${esc(i.conc)}${p?' · '+p.g+' · '+esc(p.fam)+'. '+esc(p.notes):''}</p>""",
"""    <div class="pdp-top"><div><p class="meta">${esc(i.brand)} · ${esc(R.tierOf(i))}</p><h1>${esc(i.name)}</h1>
    <p class="lead">${esc(i.conc)}${p?' · '+p.g:''}</p></div><button class="fav" type="button" data-fav="${x.key}" aria-pressed="${favs().includes(x.key)}">${HEART}${favs().includes(x.key)?'Guardado':'Guardar'}</button></div>""")
rep("""    <h2>Mejor precio, día a día</h2>${R.lineChart(R.series(i),{stroke:'var(--accent)',grid:'#16150f'})}""",
"""    <h2>Mejor precio, día a día</h2>${R.lineChart(R.series(i),{stroke:'var(--accent)',grid:'#16150f'})}${hist(i)}""")
rep("""    <h2>Avísame si baja</h2><label class="target">Por debajo de <input type="number" inputmode="decimal" min="0" step="0.5" value="${t??''}" data-target="${i.id}" aria-label="Precio objetivo en euros"> €</label>""",
"""    <h2>Mi precio objetivo</h2><label class="target">Márcalo cuando baje de <input type="number" inputmode="decimal" min="0" step="0.5" value="${t??''}" data-target="${i.id}" aria-label="Precio objetivo en euros"> €</label>
    <p class="tstatus${below(i)?' ok':''}" id="tst" role="status">${t!=null?(below(i)?'Ya está por debajo de tu objetivo':'Guardado en este navegador. Lo verás marcado en el catálogo y en Guardados cuando baje.'):'Se guarda solo en este navegador.'}</p>""")
rep("""  </div></div>`;
  $('sheet').focus({preventScroll:true});scrollTo(0,0);""", """  </div></div>${b?`<div class="buybar"><span><b>${eur(b.p)}</b><small>en ${esc(b.name)}</small></span><a href="${esc(b.url)}" target="_blank" rel="noopener">Ver oferta</a></div>`:''}`;
  $('sheet').classList.toggle('has-bar',!!b);
  $('sheet').focus({preventScroll:true});scrollTo(0,0);""")
rep("function offerTable(o){", """function hist(i){const s=R.series(i).filter(x=>x.d>=new Date(Date.now()-30*864e5).toISOString().slice(0,10)).map(x=>x.p);if(s.length<3)return '';
  const avg=s.reduce((a,c)=>a+c,0)/s.length;
  return `<div class="hist" aria-label="Últimos 30 días"><div><small>Mínimo 30 días</small><b>${eur(Math.min(...s))}</b></div><div><small>Media</small><b>${eur(avg)}</b></div><div><small>Máximo</small><b>${eur(Math.max(...s))}</b></div></div>`}
function offerTable(o){""")
rep("""  if(e.target.dataset.target){const v=e.target.value===''?null:parseFloat(e.target.value);R.setTarget(e.target.dataset.target,v)}""",
"""  if(e.target.dataset.target){const v=e.target.value===''?null:parseFloat(e.target.value);R.setTarget(e.target.dataset.target,v);const it=D.items.find(x=>x.id===e.target.dataset.target),st=$('tst');
    if(st){st.className='tstatus'+(below(it)?' ok':'');st.textContent=v==null?'Objetivo quitado.':below(it)?'Ya está por debajo de tu objetivo':'Guardado. Lo verás marcado en el catálogo y en Guardados cuando baje de '+eur(v)+'.'}}""")

# ---------------------------------------------------------------- JS: chollos con pestañas, foto y títulos limpios
rep("""function chollos(){
  const mine=D.deals.filter(d=>D.items.some(i=>i.deals.includes(d))),rest=D.deals.filter(d=>!mine.includes(d));
  const rowD=d=>{const it=D.items.find(i=>i.deals.includes(d));return `<a href="${esc(d.url)}" target="_blank" rel="noopener"><span><b>${esc(d.t)}</b>${it?' <span class="mine">En tu lista</span>':''}<span class="sub">${esc(d.shop||'Chollometro')}</span></span><b>${d.p?eur(d.p):''}</b></a>`};
  $('sheet').innerHTML=`<h1>Chollos de Chollometro</h1><p class="meta">${D.deals.length} chollos de perfumes activos · ${mine.length} de perfumes de tu lista. Se revisan en cada pasada.</p>
  <div class="deals">${[...mine,...rest].map(rowD).join('')||'<p class="empty">No hay chollos activos ahora mismo.</p>'}</div>`;
}""", """const cleanT=t=>t.split(/\\s[|·–]\\s/)[0].replace(/\\s*[\\[(][^\\])]*?(env[ií]o|vendid|desde|gratis|oferta)[^\\])]*([\\])]|$)/gi,'').replace(/\\s*,\\s*(perfume|fragancia)\\b.*$/i,'').trim();
function chollos(){
  const mine=D.deals.filter(d=>D.items.some(i=>i.deals.includes(d))),rest=D.deals.filter(d=>!mine.includes(d));
  if(!dealTab)dealTab=mine.length?'mine':'all';
  const list=dealTab==='mine'?mine:D.deals;
  const rowD=d=>{const it=D.items.find(i=>i.deals.includes(d));return `<a href="${esc(d.url)}" target="_blank" rel="noopener"><span class="dph">${it?pic(it)+'</div>':''}</span><span><span class="dt">${esc(cleanT(d.t))}</span><span class="sub">${esc(d.shop||'Chollometro')}${it?' · <span class="mine">En tu lista</span>':''}</span></span><b>${d.p?eur(d.p):''}</b></a>`};
  $('sheet').innerHTML=`<h1>Chollos de Chollometro</h1><p class="meta">Se revisan en cada pasada.</p>
  <div class="tabs" role="group" aria-label="Qué chollos ver"><button type="button" data-dtab="mine" aria-pressed="${dealTab==='mine'}">De tu lista (${mine.length})</button><button type="button" data-dtab="all" aria-pressed="${dealTab==='all'}">Todos (${D.deals.length})</button></div>
  <div class="deals">${list.slice(0,dealLimit).map(rowD).join('')||'<p class="empty">No hay chollos activos ahora mismo.</p>'}</div>
  ${list.length>dealLimit?`<button class="more" type="button" data-dmore>Mostrar ${Math.min(20,list.length-dealLimit)} más</button>`:''}`;
}
function saved(){
  const f=favs(),tg=R.targets(),gs=R.groups(D.items,R.DEFAULTS,sizeSel).filter(x=>f.includes(x.key)||x.vars.some(v=>tg[v.id]!=null));
  $('sheet').innerHTML=`<h1>Guardados</h1><p class="meta">Los perfumes que guardas y los que tienen precio objetivo. Se guardan solo en este navegador.</p>
  ${gs.length?`<div class="grid">${gs.map(tile).join('')}</div>`:'<p class="empty">Aún no has guardado ningún perfume. En cada ficha tienes el botón Guardar.</p>'}`;
}""")
rep("""  if(m)detail(m[1]);else if(h==='#chollos')chollos();else catalog();""", """  if(!m)$('sheet').classList.remove('has-bar');
  if(m)detail(m[1]);else if(h==='#chollos')chollos();else if(h==='#guardados')saved();else catalog();""")
rep("""(a.dataset.sec==='chollos')===(h==='#chollos')&&!m?'page':'false'""", """(a.dataset.sec==='chollos'&&h==='#chollos')||(a.dataset.sec==='guardados'&&h==='#guardados')||(a.dataset.sec==='cat'&&!m&&h!=='#chollos'&&h!=='#guardados')?'page':'false'""")
rep("""document.addEventListener('click',e=>{
  const t=e.target.closest(""", """document.addEventListener('click',e=>{
  const fv=e.target.closest('[data-fav]');if(fv){const on=toggleFav(fv.dataset.fav);fv.setAttribute('aria-pressed',on);fv.innerHTML=HEART+(on?'Guardado':'Guardar');return}
  const dt=e.target.closest('[data-dtab]');if(dt){dealTab=dt.dataset.dtab;dealLimit=20;chollos();return}
  if(e.target.closest('[data-dmore]')){dealLimit+=20;chollos();return}
  const t=e.target.closest(""")
rep("""  $('q').value=S.q;filters();route();""", """  $('q').value=S.q;filters();gcount();route();""")

(ROOT / "maquetas" / "propuesta.html").write_text(s)
print("ok: maquetas/propuesta.html")
