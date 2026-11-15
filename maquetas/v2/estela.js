// Estela v2 — lógica común de las maquetas de estructura. Cada página llama a E.start({home, catalog, ...}).
(function(){
const R=window.RP,$=id=>document.getElementById(id),esc=R.esc,eur=R.eur;
const E={R,$,esc,eur,S:R.readState(),FAM:null,sizeSel:{},limit:24,bq:'',D:null,dealTab:null};

// iconos (lucide, 1.5)
const I=(d,s=18)=>`<svg class="ic" width="${s}" height="${s}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${d}</svg>`;
E.ic={
  search:s=>I('<circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/>',s),
  heart:s=>I('<path d="M19 14c1.5-1.5 3-3.3 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.8 0-3 .5-4.5 2-1.5-1.5-2.7-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4 3 5.5l7 7Z"/>',s),
  home:s=>I('<path d="M3 10.5 12 3l9 7.5"/><path d="M5 9.5V21h14V9.5"/>',s),
  tag:s=>I('<path d="M12.6 2.6A2 2 0 0 0 11.2 2H4a2 2 0 0 0-2 2v7.2a2 2 0 0 0 .6 1.4l8.7 8.7a2.4 2.4 0 0 0 3.4 0l6.6-6.6a2.4 2.4 0 0 0 0-3.4Z"/><circle cx="7.5" cy="7.5" r="1"/>',s),
  grid:s=>I('<rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/>',s),
  sliders:s=>I('<path d="M4 6h10M18 6h2M4 12h4M12 12h8M4 18h12M20 18h0"/><circle cx="16" cy="6" r="2"/><circle cx="10" cy="12" r="2"/><circle cx="18" cy="18" r="2"/>',s),
  x:s=>I('<path d="M18 6 6 18"/><path d="m6 6 12 12"/>',s),
  back:s=>I('<path d="m12 19-7-7 7-7"/><path d="M19 12H5"/>',s),
  ext:s=>I('<path d="M15 3h6v6"/><path d="M10 14 21 3"/><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/>',s),
  chev:s=>I('<path d="m9 18 6-6-6-6"/>',s),
  chevl:s=>I('<path d="m15 18-6-6 6-6"/>',s),
  moon:s=>I('<path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/>',s),
  sun:s=>I('<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>',s),
  auto:s=>I('<circle cx="12" cy="12" r="9"/><path d="M12 3v18" /><path d="M12 3a9 9 0 0 1 0 18Z" fill="currentColor" stroke="none"/>',s),
  down:s=>I('<path d="M12 5v14"/><path d="m19 12-7 7-7-7"/>',s),
};
E.MARK=`<svg width="30" height="20" viewBox="0 0 34 22" aria-hidden="true"><path d="M3 17c6 0 8-11 15-11s6 7 13 4" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/><circle cx="3" cy="17" r="2.8" fill="var(--accent)"/></svg>`;

// tema: Automático (sigue al sistema) / Claro / Oscuro, recordado en este navegador
const THEMES=['auto','light','dark'],TLAB={auto:'Tema automático',light:'Tema claro',dark:'Tema oscuro'};
function theme(){try{return localStorage.getItem('estela-theme')||'auto'}catch(e){return 'auto'}}
function applyTheme(t){if(t==='auto')document.documentElement.removeAttribute('data-theme');else document.documentElement.dataset.theme=t;
  const b=$('themeb');if(b){b.innerHTML=E.ic[t==='auto'?'auto':t==='light'?'sun':'moon']();b.setAttribute('aria-label',TLAB[t]+'. Cambiar');b.title=TLAB[t]}
  const dark=t==='dark'||(t==='auto'&&matchMedia('(prefers-color-scheme: dark)').matches);
  document.querySelector('meta[name=theme-color]')?.setAttribute('content',getComputedStyle(document.documentElement).getPropertyValue('--bg').trim()||(dark?'#0e0e0d':'#f5f4f0'))}
E.cycleTheme=()=>{const n=THEMES[(THEMES.indexOf(theme())+1)%3];try{localStorage.setItem('estela-theme',n)}catch(e){}applyTheme(n)};
matchMedia('(prefers-color-scheme: dark)').addEventListener?.('change',()=>applyTheme(theme()));

// guardados y objetivos
E.favs=()=>{try{return JSON.parse(localStorage.getItem('rp-favs')||'[]')}catch(e){return []}};
E.toggleFav=k=>{const f=E.favs(),on=!f.includes(k);try{localStorage.setItem('rp-favs',JSON.stringify(on?[...f,k]:f.filter(x=>x!==k)))}catch(e){}E.gcount();return on};
E.below=i=>{const t=R.targets()[i.id];return t!=null&&i.b&&i.b.p<=t};
E.gcount=()=>{const n=E.favs().length;document.querySelectorAll('[data-gc]').forEach(g=>{g.hidden=!n;g.textContent=n})};

// familias
E.FAMS=[['floral','Floral','#d4849a'],['amaderada','Amaderada','#8b6b4c'],['oriental','Oriental','#9c4a3c'],['ambar','Ámbar','#c98a2e'],
  ['aromatica','Aromática','#7f9a6a'],['gourmand','Gourmand','#b0764a'],['citrica','Cítrica','#d9ac2c'],['acuatica','Acuática','#5b9ab8']];
E.famOf=i=>{const f=R.norm(i?.p?.fam||''),w=f.split(' ')[0];return E.FAMS.find(([k])=>w.startsWith(k))||E.FAMS.find(([k])=>f.includes(k))||null};
const SEASON_C={Primavera:'#5f8f3e',Verano:'#c58a12',Otoño:'#b0532a',Invierno:'#3f6f9c'};

// fotos al tamaño justo
const TILE_ORDER=['lookfantastic','arabicparfums','firstinfragrance','sabina','paco','parejo','laguna','brasty','perfumesclub','avenida','idealo','sephora','douglas','notino'];
E.sized=(u,w)=>/thgimages\.com/.test(u)?u.replace(/width=\d+/,'width='+w).replace(/height=\d+/,'height='+w):/\/cdn\/shop\//.test(u)?u.replace(/_\d+x\d+(\.\w+)/,`_${w}x${w}$1`).replace(/([?&])width=\d+/,'$1width='+w):u;
E.photosFor=(i,size)=>{const ph=R.photos(i);if(size!=='s')return ph;return [...ph].sort((a,b)=>((TILE_ORDER.indexOf(a.s)+99)%99)-((TILE_ORDER.indexOf(b.s)+99)%99)).map(f=>({...f,url:E.sized(f.url,480)}))};
E.pic=(i,{idx=0,size='s',eager=false,cls=''}={})=>{const f=E.photosFor(i,size)[idx];
  return `<span class="plate ${cls}" data-fb="${i.id}">${f?`<img src="${esc(f.url)}" alt="${esc(i.brand+' '+i.name)}" ${eager?'fetchpriority="high"':'loading="lazy"'} decoding="async" referrerpolicy="no-referrer">`:R.bottle(i.p)}`};
document.addEventListener('error',e=>{const im=e.target;if(im.tagName!=='IMG')return;const box=im.closest('[data-fb]');
  if(box){const it=E.D.items.find(x=>x.id===box.dataset.fb);im.replaceWith(document.createRange().createContextualFragment(R.bottle(it?.p)))}
  else{const b=im.closest('.thumbs button'),g=b&&b.parentNode;if(b)b.remove();if(g&&g.children.length<2)g.remove();if(!b)im.remove()}},true);

// grupos y cifras
E.all=()=>R.groups(E.D.items,R.DEFAULTS,E.sizeSel);
E.list=(s=E.S)=>R.groups(E.D.items,s,E.sizeSel).filter(x=>!E.FAM||E.famOf(x.cur)?.[0]===E.FAM);
E.dirty=()=>{const d=['q','g','tier','season','brand'].filter(k=>E.S[k]!==R.DEFAULTS[k]);if(E.FAM)d.push('fam');return d};
E.drops=()=>R.groups(E.D.items,{...R.DEFAULTS,sort:'drop'},E.sizeSel).filter(x=>x.cur.dr&&x.cur.dr.pct<=-3);
E.bySave=()=>E.all().map(x=>({x,s:R.spread(x.cur)})).filter(o=>o.s&&o.s.save>=1).sort((a,b)=>b.s.save-a.s.save).map(o=>o.x);
E.stats=()=>{const gs=E.all(),dr=E.drops(),sv=E.bySave()[0];const shops=new Set();
  for(const i of E.D.items)for(const o of R.offers(i))if(o.age!=null&&o.age<=2&&o.s!=='idealo')shops.add(o.s);
  return {n:gs.length,drops:dr.length,top:dr.find(x=>R.photos(x.cur).length)||dr[0]||null,save:sv?{x:sv,s:R.spread(sv.cur)}:null,shops:shops.size,at:E.D.estado?.at,
    prices:E.D.items.reduce((a,i)=>a+R.offers(i).filter(o=>o.age!=null&&o.age<=2).length,0)}};
// Índice Estela: precio de cada día frente a la media de 30 días de cada perfume, promediado
E.index=()=>{const from=new Date(Date.now()-30*864e5).toISOString().slice(0,10),day={};
  for(const x of E.all()){const s=R.series(x.cur).filter(p=>p.d>=from);if(s.length<5)continue;const avg=s.reduce((a,c)=>a+c.p,0)/s.length;
    for(const p of s)(day[p.d]=day[p.d]||[]).push(p.p/avg*100)}
  const mx=Math.max(0,...Object.values(day).map(v=>v.length));return Object.entries(day).filter(([,v])=>v.length>=mx*.6).sort().slice(1).map(([d,v])=>{v.sort((a,b)=>a-b);return {d,p:v[v.length>>1]}}) /* el primer día del historial es una sola lectura y se dispara */};
E.labels=()=>({q:'«'+E.S.q+'»',g:E.S.g,tier:E.S.tier,season:E.S.season,brand:E.S.brand,fam:(E.FAMS.find(f=>f[0]===E.FAM)||['',''])[1]});
E.today=()=>new Date().toLocaleDateString('es-ES',{weekday:'long',day:'numeric',month:'long'});

// minigráfica de 30 días
E.spark=(i,w=96,h=28)=>{const from=new Date(Date.now()-30*864e5).toISOString().slice(0,10),s=R.series(i).filter(p=>p.d>=from);if(s.length<3)return '';
  const v=s.map(p=>p.p),mn=Math.min(...v),mx=Math.max(...v),r=mx-mn||1,pts=v.map((p,k)=>`${(k/(v.length-1)*(w-4)+2).toFixed(1)},${(h-3-(p-mn)/r*(h-6)).toFixed(1)}`);
  const up=v[v.length-1]>v[0];return `<svg class="spark" width="${w}" height="${h}" viewBox="0 0 ${w} ${h}" role="img" aria-label="Precio de 30 días: de ${eur(v[0])} a ${eur(v[v.length-1])}"><polyline points="${pts.join(' ')}" fill="none" stroke="${up?'var(--neg)':'var(--pos)'}" stroke-width="1.6" stroke-linejoin="round" stroke-linecap="round"/></svg>`};

// piezas
E.badges=i=>{const b=[];if(i.dr&&i.dr.pct<=-3)b.push(`<span class="pill down">${R.pct(i.dr.pct)}</span>`);if(i.deals.length)b.push('<span class="pill">Chollo</span>');return b.length?`<span class="cbadges">${b.join('')}</span>`:''};
E.card=x=>{const i=x.cur,b=i.b,sp=R.spread(i),f=E.famOf(i);
  return `<a class="card" href="#p/${x.key}">${E.pic(i)}${E.badges(i)}${E.favs().includes(x.key)?`<span class="cfav" aria-label="Guardado">${E.ic.heart(15)}</span>`:''}</span>
  <span class="cbody"><span class="cmeta">${f?`<i class="dot" style="--c:${f[2]}" title="${f[1]}"></i>`:''}${esc(i.brand)} · ${i.ml} ml</span><span class="cname">${esc(i.name)}</span>
  <span class="cprice"><b>${b?eur(b.p):'Sin precio'}</b>${sp&&sp.save>=1?`<span class="save">−${eur(sp.save,0)} entre tiendas</span>`:''}</span>
  ${b?`<span class="cshop">en ${esc(b.name)}${sp?' · '+sp.n+' tiendas':''}</span>`:''}${E.below(i)?'<span class="tbelow">Por debajo de tu objetivo</span>':''}</span></a>`};
E.row=x=>{const i=x.cur,b=i.b,sp=R.spread(i),o=R.offers(i).filter(z=>z.stock&&z.age!=null&&z.age<=14),f=E.famOf(i);
  return `<a class="row" href="#p/${x.key}">${E.pic(i)}</span><span class="rmid"><span class="rmeta">${esc(i.brand)} · ${esc(i.conc)} · ${i.ml} ml</span><span class="rname">${esc(i.name)}</span>
  <span class="rline">${f?`<span><i class="dot" style="--c:${f[2]}"></i> ${f[1]}</span>`:''}${o.length>1?`<span>${o.length} tiendas, de ${eur(o[0].p,0)} a ${eur(o[o.length-1].p,0)}</span>`:b?`<span>solo en ${esc(b.name)}</span>`:''}${E.spark(i)}</span></span>
  <span class="rright"><b>${b?eur(b.p):'—'}</b>${i.dr&&i.dr.pct<=-3?`<span class="pill down">${R.pct(i.dr.pct)}</span>`:sp&&sp.save>=1?`<span class="save">−${eur(sp.save,0)}</span>`:''}${b?`<small class="rmeta">en ${esc(b.name)}</small>`:''}</span></a>`};
E.rail=(id,title,sub,items,more='')=>items.length?`<section class="sec" aria-labelledby="${id}"><div class="sec-h"><div><h2 id="${id}">${title}</h2>${sub?`<p>${sub}</p>`:''}</div>${more}</div>
  <div class="railwrap"><button class="rnav prev" type="button" data-rail="-1" aria-label="Anteriores">${E.ic.chevl()}</button><div class="rail">${items.map(E.card).join('')}</div><button class="rnav next" type="button" data-rail="1" aria-label="Siguientes">${E.ic.chev()}</button></div></section>`:'';
E.famTiles=(cls='fams')=>{const gs=E.all();return `<div class="${cls}">${E.FAMS.map(([k,n,c])=>{const m=gs.filter(x=>E.famOf(x.cur)?.[0]===k).length;if(!m)return '';
  return cls==='famcircles'?`<button class="famcircle" type="button" data-fam="${k}" style="--c:${c}"><span class="sw"></span><span>${n}</span></button>`
  :`<button class="fam" type="button" data-fam="${k}" style="--c:${c}"><span class="sw"></span><span><b>${n}</b><br><span>${m} perfumes</span></span></button>`}).join('')}</div>`};
E.activeChips=()=>{const d=E.dirty(),L=E.labels();return d.length?`<div class="active">${d.map(k=>`<button class="chip" type="button" data-unset="${k}" aria-label="Quitar filtro ${esc(L[k])}">${esc(L[k])}${E.ic.x(14)}</button>`).join('')}<button class="chip" type="button" data-clearall>Quitar todo</button></div>`:''};
E.sortSel=()=>`<label class="sr-only" for="sort">Ordenar</label><select class="select" id="sort">${R.SORTS.map(([k,l])=>`<option value="${k}" ${k===E.S.sort?'selected':''}>${l}</option>`).join('')}</select>`;
E.filterBtn=(lab='Filtros')=>{const n=E.dirty().filter(k=>k!=='q').length;return `<button class="chip" type="button" data-openf aria-haspopup="dialog">${E.ic.sliders(16)}${lab}${n?` <span class="count">${n}</span>`:''}</button>`};
E.more=(n)=>n>E.limit?`<button class="btn ghost more" type="button" id="more">Mostrar ${Math.min(24,n-E.limit)} más</button>`:'';
E.empty=()=>`<p class="empty">Ningún perfume cumple estos filtros. <button class="chip" type="button" data-clearall>Quitar todos los filtros</button></p>`;

// hoja de filtros (diálogo nativo)
function sheetBody(){const opt=(k,v,l,ex='')=>`<button class="chip" type="button" data-f="${k}" data-v="${esc(v)}" aria-pressed="${E.S[k]===v}">${ex}${esc(l)}</button>`;
  const brands=[...new Set(E.D.items.map(i=>i.brand))].sort((a,b)=>a.localeCompare(b,'es')).filter(b=>R.norm(b).includes(R.norm(E.bq)));
  return `<div class="fg"><h3>Para</h3><div class="chips">${['Todos','Hombre','Mujer','Unisex'].map(v=>opt('g',v,v)).join('')}</div></div>
  <div class="fg"><h3>Tipo</h3><div class="chips">${['Todos','Diseñador','Nicho','Árabe'].map(v=>opt('tier',v,v==='Todos'?'Todos':v)).join('')}</div></div>
  <div class="fg"><h3>Familia</h3><div class="chips"><button class="chip" type="button" data-fam="" aria-pressed="${!E.FAM}">Todas</button>${E.FAMS.map(([k,n,c])=>`<button class="chip" type="button" data-fam="${k}" aria-pressed="${E.FAM===k}"><i class="dot" style="--c:${c}"></i>${n}</button>`).join('')}</div></div>
  <div class="fg"><h3>Temporada</h3><div class="chips">${['Todas',...R.SEASONS].map(v=>opt('season',v,v==='Todas'?'Todo el año':v)).join('')}</div></div>
  <div class="fg"><h3>Ordenar</h3><div class="chips">${R.SORTS.map(([k,l])=>opt('sort',k,l)).join('')}</div></div>
  <div class="fg"><h3>Marca</h3><div class="search" style="margin-bottom:10px">${E.ic.search(16)}<input id="bq" type="search" placeholder="Buscar marca" aria-label="Buscar marca" value="${esc(E.bq)}" style="height:40px"></div>
  <div class="blist">${opt('brand','Todas','Todas')}${brands.map(b=>opt('brand',b,b)).join('')}</div></div>`}
function sheetRefresh(){const d=$('fsheet');if(!d?.open)return;const y=$('fsb').scrollTop;$('fsb').innerHTML=sheetBody();$('fsb').scrollTop=y;$('fsn').textContent=`Ver ${E.list().length} perfumes`}
E.openSheet=()=>{let d=$('fsheet');if(!d){d=document.createElement('dialog');d.id='fsheet';d.className='sheet';d.setAttribute('aria-labelledby','fsh');
  d.innerHTML=`<div class="sheet-h"><b id="fsh">Filtros</b><button class="tbtn" type="button" data-closef aria-label="Cerrar">${E.ic.x()}</button></div><div class="sheet-b" id="fsb"></div>
  <div class="sheet-f"><button class="btn ghost" type="button" data-clearall>Quitar todo</button><button class="btn" type="button" data-closef id="fsn"></button></div>`;
  d.addEventListener('click',e=>{if(e.target===d)d.close()});document.body.append(d)}
  d.showModal();d.open&&($('fsb').innerHTML=sheetBody());$('fsn').textContent=`Ver ${E.list().length} perfumes`};

// ficha
function hist(i){const s=R.series(i).filter(x=>x.d>=new Date(Date.now()-30*864e5).toISOString().slice(0,10)).map(x=>x.p);if(s.length<3)return '';
  const avg=s.reduce((a,c)=>a+c,0)/s.length;return `<div class="hist" aria-label="Últimos 30 días"><div><small>Mínimo 30 días</small><b>${eur(Math.min(...s))}</b></div><div><small>Media</small><b>${eur(avg)}</b></div><div><small>Máximo</small><b>${eur(Math.max(...s))}</b></div></div>`}
function offerRows(o,best){return `<table class="offers"><caption class="sr-only">Precio en cada tienda</caption><tbody>${o.map(z=>`<tr class="${z===best?'best':''}"><td><a href="${esc(z.url)}" target="_blank" rel="noopener">${esc(z.name)}</a><br><span class="when">${z.stock?R.ago(z.d):'agotado'}${z.via?' · vía '+esc(R.shopName(z.via)):''}</span></td><td class="n">${eur(z.p)}</td></tr>`).join('')}</tbody></table>`}
E.detail=key=>{const x=E.all().find(g=>g.key===key);if(!x){location.hash='';return}
  const i=x.cur,p=i.p,o=R.offers(i),b=i.b,t=R.targets()[i.id],ph=R.photos(i),f=E.famOf(i),fav=E.favs().includes(x.key);
  const meter=(n,l)=>`<div><small class="rmeta">${l}</small><div class="meter" role="img" aria-label="${l}: ${n} de 5">${[1,2,3,4,5].map(k=>`<i class="${k<=n?'f':''}"></i>`).join('')}</div></div>`;
  const recent=o.filter(z=>z.age==null||z.age<=30),old=o.filter(z=>z.age!=null&&z.age>30);
  const sim=E.all().filter(y=>y.key!==x.key&&E.famOf(y.cur)?.[0]===f?.[0]&&y.cur.b).sort((a,c)=>Math.abs(a.cur.b.p-(b?.p||0))-Math.abs(c.cur.b.p-(b?.p||0))).slice(0,8);
  E.main(`<div class="wrap"><a class="back" href="#">${E.ic.back(16)}Volver</a>
  <div class="pdp"><div class="pdp-media"><div id="mainph">${E.pic(i,{size:'l',eager:true})}</span></div>
    ${ph.length>1?`<div class="thumbs" role="group" aria-label="Fotos">${ph.map((q,k)=>`<button type="button" aria-pressed="${k===0}" data-ph="${k}" aria-label="Foto de ${esc(R.shopName(q.s))}"><img src="${esc(E.sized(q.url,160))}" alt="" loading="lazy" referrerpolicy="no-referrer"></button>`).join('')}</div>`:''}
    ${ph.length?`<p class="rmeta" id="credit">Foto: ${esc(R.shopName(ph[0].s))}</p>`:''}</div>
  <div class="pdp-info"><p class="kick">${esc(i.brand)} · ${esc(R.tierOf(i))}</p><h1>${esc(i.name)}</h1><p class="rmeta">${esc(i.conc)}${p?' · '+p.g:''}</p>
    <div class="sizes" role="group" aria-label="Tamaño">${x.vars.map(v=>`<button class="chip" type="button" aria-pressed="${v.id===i.id}" data-size="${v.id}">${v.ml} ml</button>`).join('')}</div>
    <div class="buy"><div class="bp"><b>${b?eur(b.p):'Sin precio'}</b>${i.dr&&i.dr.pct<=-3?`<span class="pill down">${R.pct(i.dr.pct)} frente a su media</span>`:''}</div>
      ${b?`<p class="bsub" style="margin:0">en ${esc(b.name)}${b.age>7?' (leído '+R.ago(b.d)+')':''} · ${eur(b.p/i.ml*100)} los 100 ml</p>`:''}
      <div class="bact">${b?`<a class="btn" href="${esc(b.url)}" target="_blank" rel="noopener">Ver en ${esc(b.name)}${E.ic.ext(16)}</a>`:''}<button class="btn ghost" type="button" data-fav="${x.key}" aria-pressed="${fav}">${E.ic.heart(16)}${fav?'Guardado':'Guardar'}</button></div>
      ${hist(i)}</div>
    <div class="block"><h2>Precio en cada tienda</h2>${recent.length?offerRows(recent,b):'<p class="rmeta">Aún no hay precios recientes</p>'}${old.length?`<details class="oldp"><summary>${old.length} ${old.length===1?'precio leído':'precios leídos'} hace más de un mes</summary>${offerRows(old)}</details>`:''}</div>
    <div class="block"><h2>Mejor precio, día a día</h2>${R.lineChart(R.series(i),{stroke:'var(--accent)',grid:'currentColor'})}</div>
    ${p?`<div class="block"><h2>Cómo huele</h2><div class="olf" style="--c:${f?f[2]:'var(--accent)'}"><div class="olf-fam"><span class="sw"></span><span><small>Familia</small><b>${esc(p.fam)}</b></span></div>
      <ul class="notes" aria-label="Notas">${p.notes.split(/,\s*/).map(n=>`<li>${esc(n)}</li>`).join('')}</ul>
      <div class="seasons" aria-label="Temporada">${R.SEASONS.map(s=>`<span class="${p.se.includes(s)?'on':''}" style="--c:${SEASON_C[s]}">${s}</span>`).join('')}</div>
      <div class="meters">${meter(p.dur,'Duración')}${meter(p.sil,'Estela')}</div><p class="rmeta" style="margin:0">Mejor para: ${esc(p.use)}</p></div></div>`:''}
    <div class="block"><h2>Avísame si baja</h2><div class="target"><label for="tg">Marcarlo cuando baje de</label><input id="tg" type="number" inputmode="decimal" min="0" step="0.5" value="${t??''}" data-target="${i.id}"> €</div>
      <p class="tstatus${E.below(i)?' ok':''}" id="tst" role="status">${t!=null?(E.below(i)?'Ya está por debajo de tu objetivo':'Guardado en este navegador.'):'Se guarda solo en este navegador.'}</p></div>
    ${i.deals.length?`<div class="block"><h2>Chollos publicados</h2>${i.deals.slice(0,4).map(d=>`<p><a href="${esc(d.url)}" target="_blank" rel="noopener">${esc(d.t)}</a><br><span class="rmeta">${d.p?eur(d.p)+' · ':''}${esc(d.shop||'Chollometro')}</span></p>`).join('')}</div>`:''}
  </div></div>${E.rail('hSim','Parecidos de precio',f?'Misma familia: '+f[1].toLowerCase():'',sim)}</div>
  ${b?`<div class="buybar"><span><b>${eur(b.p)}</b><small>en ${esc(b.name)}</small></span><a href="${esc(b.url)}" target="_blank" rel="noopener">Ver oferta</a></div>`:''}`);
  document.body.classList.toggle('has-bar',!!b)};

E.dealsView=()=>{const D=E.D,mine=D.deals.filter(d=>D.items.some(i=>i.deals.includes(d)));if(!E.dealTab)E.dealTab=mine.length?'mine':'all';
  const list=E.dealTab==='mine'?mine:D.deals,clean=t=>t.split(/\s[|·–]\s/)[0].replace(/\s*[\[(][^\])]*?(env[ií]o|vendid|desde|gratis|oferta)[^\])]*([\])]|$)/gi,'').trim();
  E.main(`<div class="wrap"><div class="rhead"><h1>Chollos</h1><div class="chips" role="group" aria-label="Qué chollos ver"><button class="chip" type="button" data-dtab="mine" aria-pressed="${E.dealTab==='mine'}">De tu lista · ${mine.length}</button><button class="chip" type="button" data-dtab="all" aria-pressed="${E.dealTab==='all'}">Todos · ${D.deals.length}</button></div></div>
  <p class="rmeta">Publicados en Chollometro y revisados en cada pasada.</p><div class="rows">${list.slice(0,40).map(d=>{const it=D.items.find(i=>i.deals.includes(d));
    return `<a class="row" href="${esc(d.url)}" target="_blank" rel="noopener">${it?E.pic(it)+'</span>':'<span class="plate"></span>'}<span class="rmid"><span class="rname">${esc(clean(d.t))}</span><span class="rmeta">${esc(d.shop||'Chollometro')}${it?' · En tu lista':''}</span></span><span class="rright"><b>${d.p?eur(d.p):''}</b></span></a>`}).join('')||'<p class="empty">No hay chollos activos ahora mismo.</p>'}</div></div>`)};
E.savedView=()=>{const f=E.favs(),tg=R.targets(),gs=E.all().filter(x=>f.includes(x.key)||x.vars.some(v=>tg[v.id]!=null));
  E.main(`<div class="wrap"><div class="rhead"><h1>Guardados</h1></div><p class="rmeta">Los que guardas y los que tienen precio objetivo. Se guardan solo en este navegador.</p>
  ${gs.length?`<div class="grid" style="margin-top:20px">${gs.map(E.card).join('')}</div>`:'<p class="empty">Aún no has guardado ninguno. En cada ficha tienes el botón Guardar.</p>'}</div>`)};

E.foot=()=>{const st=E.stats();return `<footer class="wrap"><div class="foot"><div><b>Estela</b><p>Comparamos ${st.n} perfumes en ${st.shops} perfumerías españolas varias veces al día. No cobramos comisión por los enlaces.</p></div>
  <div><b>Datos</b><p>Precios y fotos de cada tienda. Notino, Primor, Druni, Arenal y Julia se leen a través de Idealo.</p></div>
  <div><b>Última lectura</b><p>${R.agoTime(st.at)}</p></div><div><b>Código</b><p><a href="https://github.com/sombranba-bit/radar-perfumes/commits/main" target="_blank" rel="noopener">Historial de cambios</a></p></div></div></footer>`};

// armazón
E.main=html=>{const m=$('main');m.innerHTML=html;document.body.classList.remove('has-bar')};
E.shell=({name,variants,catalog})=>{const nav=[['','Inicio','home'],...(catalog?[['#catalogo','Catálogo','grid']]:[]),['#chollos','Chollos','tag'],['#guardados','Guardados','heart']];
  document.body.insertAdjacentHTML('afterbegin',`<a class="skip" href="#main">Saltar al contenido</a>
  <header class="top"><div class="wrap"><a class="brand" href="#" aria-label="Estela, inicio">${E.MARK}<b>Estela</b></a>
  <div class="search">${E.ic.search(18)}<input id="q" type="search" placeholder="Busca perfume, marca o nota" aria-label="Buscar perfume" autocomplete="off"></div>
  <nav class="tools" aria-label="Menú">${nav.slice(1).map(([h,l,ic])=>`<a class="tbtn" href="${h||'#'}" data-sec="${h}">${E.ic[ic](18)}<span class="tlabel">${l}</span>${ic==='heart'?'<span class="count" data-gc hidden></span>':''}</a>`).join('')}
  <button class="tbtn themebtn" id="themeb" type="button"></button></nav></div></header>
  <main id="main" tabindex="-1"></main><div id="foot"></div>
  <nav class="tabbar" aria-label="Barra de secciones">${nav.map(([h,l,ic])=>`<a href="${h||'#'}" data-sec="${h}">${E.ic[ic](22)}<span>${l}</span></a>`).join('')}</nav>
  <nav class="mq" aria-label="Maquetas">${variants.map(([f,l,s])=>`<a href="${f}" ${f===name?'aria-current="page"':''}>${l}<span class="long"> ${s}</span></a>`).join('')}<a href="../propuesta.html">Antes</a></nav>`);
  applyTheme(theme())};
E.msearch=()=>`<div class="msearch"><div class="search">${E.ic.search(18)}<input data-q type="search" placeholder="Busca perfume, marca o nota" aria-label="Buscar perfume" value="${esc(E.S.q)}" autocomplete="off"></div></div>`;

let V={};
E.route=()=>{const h=location.hash,m=h.match(/^#p\/(.+)$/),sec=m?'#p':['#chollos','#guardados','#catalogo'].includes(h)?h:'';
  const cur=sec===''&&E.dirty().length&&V.catalog?'#catalogo':(sec==='#catalogo'&&!V.catalog?'':sec);
  document.querySelectorAll('[data-sec]').forEach(a=>a.setAttribute('aria-current',a.dataset.sec===cur?'page':'false'));
  if(m)E.detail(m[1]);else if(h==='#chollos')E.dealsView();else if(h==='#guardados')E.savedView();
  else if(V.catalog&&(h==='#catalogo'||E.dirty().length))V.catalog();else V.home();
  document.body.dataset.view=m?'p':h?h.slice(1):V.catalog&&E.dirty().length?'catalogo':'home';
  $('foot').innerHTML=m?'':E.foot();R.writeState(E.S);sheetRefresh()};
E.rerender=()=>{const y=scrollY;E.route();scrollTo(0,y)};
function goList(){E.limit=24;if(location.hash.startsWith('#p/')||['#chollos','#guardados'].includes(location.hash))location.hash=V.catalog?'#catalogo':'';else E.rerender()}

document.addEventListener('click',e=>{const t=e.target.closest('button,a');if(!t)return;
  if(t.id==='themeb')return E.cycleTheme();
  if(t.dataset.fav){const on=E.toggleFav(t.dataset.fav);t.setAttribute('aria-pressed',on);t.innerHTML=E.ic.heart(16)+(on?'Guardado':'Guardar');return}
  if(t.dataset.dtab){E.dealTab=t.dataset.dtab;E.dealsView();return}
  if(t.dataset.rail){const r=t.parentNode.querySelector('.rail');r.scrollBy({left:+t.dataset.rail*r.clientWidth*.9,behavior:'smooth'});return}
  if(t.hasAttribute('data-openf'))return E.openSheet();
  if(t.hasAttribute('data-closef'))return $('fsheet').close();
  if(t.dataset.fam!==undefined){const k=t.dataset.fam||null;E.FAM=(!t.closest('#fsheet')&&E.FAM===k)?null:k;E.limit=24;
    if(t.closest('.famcircles,.fams')&&V.catalog&&location.hash!=='#catalogo'){location.hash='#catalogo';return}goList();return}
  if(t.dataset.f){E.S[t.dataset.f]=t.dataset.v;goList();return}
  if(t.dataset.unset){if(t.dataset.unset==='fam')E.FAM=null;else E.S[t.dataset.unset]=R.DEFAULTS[t.dataset.unset];if(t.dataset.unset==='q')document.querySelectorAll('#q,[data-q]').forEach(q=>q.value='');goList();return}
  if(t.hasAttribute('data-clearall')){E.S={...R.DEFAULTS,sort:E.S.sort};E.FAM=null;document.querySelectorAll('#q,[data-q]').forEach(q=>q.value='');goList();return}
  if(t.dataset.size){const it=E.D.items.find(x=>x.id===t.dataset.size);E.sizeSel[it.key]=it.id;E.route();return}
  if(t.dataset.ph){const k=+t.dataset.ph,x=E.all().find(g=>g.key===location.hash.slice(3));$('mainph').innerHTML=E.pic(x.cur,{idx:k,size:'l',eager:true})+'</span>';
    document.querySelectorAll('[data-ph]').forEach(b=>b.setAttribute('aria-pressed',b===t));$('credit').textContent='Foto: '+R.shopName(R.photos(x.cur)[k].s);return}
  if(t.id==='more'){E.limit+=24;E.rerender();return}
  if(t.dataset.sortdrop!==undefined){E.S.sort='drop';location.hash='#catalogo';return}
});
document.addEventListener('input',e=>{const t=e.target;
  if(t.id==='bq'){E.bq=t.value;sheetRefresh();const q=$('bq');q.focus();q.setSelectionRange(E.bq.length,E.bq.length);return}
  if(t.id==='q'||t.hasAttribute('data-q')){E.S.q=t.value;document.querySelectorAll('#q,[data-q]').forEach(q=>{if(q!==t)q.value=t.value});
    E.limit=24;if(location.hash.startsWith('#p/')||['#chollos','#guardados'].includes(location.hash))location.hash=V.catalog?'#catalogo':'';else E.route();
    if(!document.contains(t)){const n=[...document.querySelectorAll('[data-q],#q')].find(q=>q.offsetParent!==null&&getComputedStyle(q).visibility!=='hidden');if(n){n.focus();n.setSelectionRange(t.value.length,t.value.length)}}}});
document.addEventListener('change',e=>{const t=e.target;
  if(t.id==='sort'){E.S.sort=t.value;E.rerender()}
  if(t.dataset.target){const v=t.value===''?null:parseFloat(t.value);R.setTarget(t.dataset.target,v);const it=E.D.items.find(x=>x.id===t.dataset.target),st=$('tst');
    st.className='tstatus'+(E.below(it)?' ok':'');st.textContent=v==null?'Objetivo quitado.':E.below(it)?'Ya está por debajo de tu objetivo':'Guardado. Lo verás marcado cuando baje de '+eur(v)+'.'}});
addEventListener('hashchange',()=>{E.route();scrollTo(0,0);$('main').focus({preventScroll:true})});

E.start=async views=>{V=views;E.shell(views);
  E.D=await R.load('../../data/');
  if(!E.D){E.main('<div class="wrap"><p class="empty">No se han podido cargar los precios. Revisa la conexión y <a href="">vuelve a intentarlo</a>.</p></div>');return}
  $('q').value=E.S.q;E.gcount();E.route()};
window.E=E;
})();
