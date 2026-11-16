// Fragans — bloques olfativos al estilo Fragrantica: acordes principales, pirámide de notas y cuándo usarlo.
// shortcut: la pirámide y los acordes salen de clasificar las 3 notas de cada ficha por tipo de ingrediente; cuando haya datos reales de pirámide (Fragrantica/Parfumo) se sustituye notes().
(function(){
const E=window.E,R=E.R,esc=E.esc;
// tipo de cada nota: [categoría, color]
const CAT={
 citrus:['Cítrico','#f2e35b','top'],fruit:['Afrutado','#f08a5d','top'],aromatic:['Aromático','#2f7562','top'],marine:['Marino','#4aa3df','top'],green:['Verde','#6bbf59','top'],
 spice:['Especiado','#c0392b','heart'],floral:['Floral','#f19cbb','heart'],white:['Floral blanco','#efe3c8','heart'],powder:['Atalcado','#c9bdb5','heart'],alcohol:['Alcohólico','#a8323e','heart'],
 wood:['Amaderado','#8b5a2b','base'],earthy:['Terroso','#6d7b4b','base'],resin:['Ámbar','#9a5214','base'],smoky:['Ahumado','#6c6c6c','base'],vanilla:['Avainillado','#f6efb0','base'],
 sweet:['Dulce','#c8323d','base'],gourmand:['Caramelo','#a8743a','base'],musk:['Almizclado','#e6dbe6','base'],leather:['Cuero','#6b3e26','base'],tobacco:['Tabaco','#8c6a3c','base'],oud:['Oud','#5a3b2e','base']};
const N={};const put=(c,l)=>l.split(',').forEach(n=>N[n.trim()]=c);
put('citrus','bergamota,pomelo,limón,mandarina,naranja,neroli,naranja sanguina,mandarina verde,limón confitado,yuzu,mandarina sanguina,verbena');
put('fruit','manzana,piña,melocotón,pera,fresa,melón,casis,frambuesa,granada,ciruela,pitahaya,cereza,grosella roja,membrillo,higuera,mango,frutas,manzana verde,lichi,ruibarbo,dátil,tropical');
put('aromatic','lavanda,salvia,menta,romero,enebro,laurel,orégano');put('green','té,té verde,bambú,pino');put('marine','notas marinas,sal marina,algas');
put('spice','canela,cardamomo,jengibre,pimienta,azafrán,nuez moscada,pimienta rosa,pimienta negra,clavo,anís estrellado,regaliz');
put('floral','rosa,violeta,peonía,orquídea,loto,lirio,madreselva,osmanthus,amapola,orquídea negra,narciso,lirio del valle,rosa turca');
put('white','jazmín,azahar,tuberosa,ylang-ylang,gardenia,nardo,flor de azahar');put('powder','iris,aldehídos');put('alcohol','ron,whisky,coñac');
put('wood','sándalo,cedro,palo de rosa,cedro rojo,madera,ébano,notas amaderadas,cachemira,ciprés');put('earthy','vetiver,pachulí,musgo de roble,musgo,trufa');
put('resin','ámbar,benjuí,ámbar gris,ambergris,ambroxan');put('smoky','incienso,alquitrán,abedul');put('vanilla','vainilla,vainilla salada,haba tonka');
put('sweet','praliné,caramelo,miel,azúcar moreno,malvavisco,toffee,kulfi,coco');put('gourmand','cacao,café,almendra,castaña,almendra amarga,avellana');
put('musk','almizcle,ambrette');put('leather','cuero,ante');put('tobacco','tabaco');put('oud','oud');
// color propio de algunas notas (si no, el de su categoría)
const COL={rosa:'#e46b8c',violeta:'#8b6fc7',lavanda:'#9b88d3',iris:'#a99bd0',jazmín:'#f3edd8',limón:'#f4e04d',pomelo:'#f5916b',mandarina:'#f6a33a',naranja:'#f39a2e',
 bergamota:'#c8d65a',manzana:'#c7d94a',piña:'#f2c94c',fresa:'#e24a5b',frambuesa:'#d6336c',cereza:'#b0203a',ciruela:'#6b2f5f',casis:'#4a2047',menta:'#64c3a0',
 café:'#5b3a29',cacao:'#6a4232',canela:'#b0612b',cardamomo:'#8ea35a',azafrán:'#e0762b','pimienta rosa':'#e06a7a',vainilla:'#f6efb0','haba tonka':'#5a4637',
 almizcle:'#e6dbe6',sándalo:'#c49a6c',cedro:'#9a6b3f',vetiver:'#7a7a4a',pachulí:'#6b5a3a',incienso:'#9a9a9a',cuero:'#6b3e26',tabaco:'#8c6a3c',oud:'#5a3b2e',ron:'#a0522d','notas marinas':'#4aa3df',salvia:'#8fa58a',enebro:'#4f6d5a'};
const FAMW=[['floral','floral'],['amader','wood'],['orient','resin'],['ámbar','resin'],['ambar','resin'],['aromát','aromatic'],['aromat','aromatic'],['gourmand','sweet'],['cítric','citrus'],['citric','citrus'],
 ['acuát','marine'],['acuat','marine'],['especi','spice'],['frut','fruit'],['cuero','leather'],['fresc','green'],['almizc','musk'],['dulce','sweet'],['ahum','smoky'],['verde','green'],['atalc','powder']];
const lum=h=>{const n=parseInt(h.slice(1),16),r=(n>>16)/255,g=(n>>8&255)/255,b=(n&255)/255;return .2126*r+.7152*g+.0722*b};
const ink=h=>{const L=x=>{x=x<=.03928?x/12.92:((x+.055)/1.055)**2.4;return x},n=parseInt(h.slice(1),16),y=.2126*L((n>>16)/255)+.7152*L((n>>8&255)/255)+.0722*L((n&255)/255);return (y+.05)/.0545>1.05/(y+.05)?'#1d1b18':'#fff'};

const O={CAT};
O.notes=i=>(i.p?.notes||'').split(/,\s*/).filter(Boolean).map((n,k)=>{const key=n.toLowerCase().trim(),c=N[key]||'wood';return {n,key,cat:c,lvl:CAT[c][2],color:COL[key]||CAT[c][1],k}});
O.accords=i=>{const w={};const add=(c,v)=>{const a=CAT[c][0];w[a]=(w[a]||0)+v;w['@'+a]=CAT[c][1]};
  R.norm(i.p?.fam||'').split(/\s+/).forEach((x,k)=>{const m=FAMW.find(([p])=>x.startsWith(R.norm(p)));if(m)add(m[1],k?80:100)});
  O.notes(i).forEach(n=>add(n.cat,70-n.k*12));
  const list=Object.keys(w).filter(k=>k[0]!=='@').map(a=>({a,v:w[a],c:w['@'+a]})).sort((x,y)=>y.v-x.v).slice(0,7),mx=list[0]?.v||1;
  return list.map(x=>({...x,pct:Math.round(38+62*x.v/mx)}))};
O.when=i=>{const se=i.p?.se||[],u=R.norm(i.p?.use||'');
  return [['Invierno','snow','#8fd3f4',se.includes('Invierno')],['Primavera','leaf','#9be37a',se.includes('Primavera')],['Verano','umb','#f28b82',se.includes('Verano')],['Otoño','maple','#f4b46b',se.includes('Otoño')],
   ['Día','sun','#f6a623',/dia|diario|oficina|deporte/.test(u)],['Noche','moon','#8fb6e0',/noche|fiesta|cita|evento|tarde/.test(u)]].map(([l,ic,c,on])=>({l,ic,c,on}))};

// iconos de cuándo usarlo (trazo, a lo Fragrantica)
const W={snow:'<path d="M12 2v20M4.9 7l14.2 10M4.9 17 19.1 7"/><path d="m9 4 3 2 3-2M9 20l3-2 3 2M3.5 10.5 5 7.5 2.5 6M21.5 13.5 19 16.5l2.5 1.5M3.5 13.5l1.5 3-2.5 1.5M21.5 10.5 19 7.5 21.5 6"/>',
 leaf:'<path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.5 19 2c1 2 2 4.2 2 8 0 5.5-4.8 10-10 10Z"/><path d="M2 21c0-3 1.9-5.4 5.2-6.1C9.5 14.4 12 13 13 12"/>',
 umb:'<path d="M22 12a10 10 0 0 0-20 0Z"/><path d="M12 12v8a2 2 0 0 0 4 0"/><path d="M12 2v1"/>',
 maple:'<path d="M12 22v-6M12 16l-5 2 1-4-5-3 3-1-1-4 4 2 3-6 3 6 4-2-1 4 3 1-5 3 1 4Z"/>',
 sun:'<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>',
 moon:'<path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/><path d="M19 3v4M17 5h4"/>'};
const wic=k=>`<svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${W[k]}</svg>`;

// dibujo de cada nota: azulejo con el color de la nota y el trazo de su familia
const G={citrus:'<circle cx="24" cy="24" r="13"/><path d="M24 11v26M11 24h26M15 15l18 18M33 15 15 33"/>',fruit:'<circle cx="24" cy="27" r="12"/><path d="M24 15c0-4 2-6 5-7M24 15c-3-3-7-3-9-1 3 2 6 2 9 1"/>',
 aromatic:'<path d="M24 40V12"/><path d="M24 16c-5-1-7-4-7-6 4 0 7 2 7 6Zm0 8c5-1 7-4 7-6-4 0-7 2-7 6Zm0 8c-5-1-7-4-7-6 4 0 7 2 7 6Z"/>',green:'<path d="M14 36c0-14 8-22 22-24-1 14-9 22-22 24Z"/><path d="M14 36 28 20"/>',
 marine:'<path d="M8 20c4-4 8-4 12 0s8 4 12 0 6-3 8-1M8 28c4-4 8-4 12 0s8 4 12 0 6-3 8-1"/>',spice:'<path d="M24 8l3.5 10.5L38 22l-10.5 3.5L24 36l-3.5-10.5L10 22l10.5-3.5Z"/>',
 floral:'<circle cx="24" cy="24" r="4"/><path d="M24 20c-3-6-1-11 0-12 1 1 3 6 0 12Zm4 2c4-5 9-6 11-5-1 2-5 6-11 5Zm-1 6c6 1 9 5 9 7-2 0-7-1-9-7Zm-6 0c-2 6-7 7-9 7 0-2 3-6 9-7Zm-1-6c-6 1-10-3-11-5 2-1 7 0 11 5Z"/>',
 white:'<circle cx="24" cy="24" r="3.5"/><path d="M24 20.5V9M27.5 24H39M24 27.5V39M20.5 24H9M26.5 21.5l8-8M26.5 26.5l8 8M21.5 26.5l-8 8M21.5 21.5l-8-8"/>',powder:'<circle cx="18" cy="26" r="7"/><circle cx="29" cy="22" r="8"/><circle cx="27" cy="32" r="5"/>',
 alcohol:'<path d="M16 10h16l-2 16a6 6 0 0 1-12 0Z"/><path d="M24 32v7M18 39h12M17 18h14"/>',wood:'<ellipse cx="24" cy="24" rx="13" ry="13"/><ellipse cx="24" cy="24" rx="8" ry="8"/><ellipse cx="24" cy="24" rx="3" ry="3"/>',
 earthy:'<path d="M10 34c4-8 9-12 14-12s10 4 14 12Z"/><path d="M24 22V10M20 14l4-4 4 4"/>',resin:'<path d="M24 8c6 8 10 14 10 19a10 10 0 0 1-20 0c0-5 4-11 10-19Z"/>',smoky:'<path d="M18 40c-4-6 6-8 2-14s6-8 2-16M28 40c-4-6 6-8 2-14s4-8 2-12"/>',
 vanilla:'<path d="M14 38C20 30 28 18 34 10"/><path d="M17 36c6-7 13-17 17-24"/><path d="M30 10c3-1 6 0 7 2-2 2-5 2-7-2Z"/>',sweet:'<rect x="12" y="16" width="24" height="16" rx="4"/><path d="M12 24H6l3-4M36 24h6l-3-4"/>',
 gourmand:'<ellipse cx="24" cy="24" rx="10" ry="14" transform="rotate(30 24 24)"/><path d="M18 14c4 6 8 14 12 20"/>',musk:'<circle cx="24" cy="24" r="12"/><circle cx="24" cy="24" r="6" stroke-dasharray="2 3"/>',
 leather:'<rect x="11" y="11" width="26" height="26" rx="5"/><path d="M15 15h18v18H15Z" stroke-dasharray="2.5 2.5"/>',tobacco:'<path d="M24 40C12 32 12 16 24 8c12 8 12 24 0 32Z"/><path d="M24 12v26M24 20l-5-3M24 26l5-3M24 32l-5-3"/>',
 oud:'<path d="M16 38V14l8-6 8 6v24Z"/><path d="M16 22h16M16 30h16"/>'};
O.tile=(n,size=56,label=true)=>`<button class="note" type="button" data-note="${esc(n.n)}" title="Buscar perfumes con ${esc(n.n)}"><span class="nt" style="--nc:${n.color};--ni:${ink(n.color)};width:${size}px;height:${size}px"><svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${G[n.cat]||G.wood}</svg></span>${label?`<span class="nl">${esc(n.key)}</span>`:''}</button>`;

O.accordsHTML=i=>{const a=O.accords(i);if(!a.length)return '';
  return `<div class="acc" role="list" aria-label="Acordes principales">${a.map(x=>`<div class="ab" role="listitem" style="--w:${x.pct}%;--ac:${x.c};--ai:${ink(x.c)}"><span>${x.a}</span><b class="tr"><s></s></b><i>${x.pct} %</i></div>`).join('')}</div>
   <div class="accstack" aria-hidden="true">${a.map(x=>`<i style="flex:${x.v};background:${x.c}" title="${x.a}"></i>`).join('')}</div>
   <div class="acclegend" aria-hidden="true">${a.map(x=>`<span><i style="background:${x.c}"></i>${x.a}</span>`).join('')}</div>`};
O.pyramidHTML=i=>{const ns=O.notes(i),L=[['top','Notas de salida'],['heart','Corazón'],['base','Fondo']];
  return `<div class="pyr">${L.map(([k,l])=>{const g=ns.filter(n=>n.lvl===k);return g.length?`<div class="lv lv-${k}"><h3 class="lvh"><span>${l}</span></h3><div class="nts">${g.map((n,j)=>O.tile(n,j?52:68)).join('')}</div></div>`:''}).join('')}</div>`};
O.whenHTML=i=>`<div class="when">${O.when(i).map(w=>`<div class="wi${w.on?' on':''}" style="--wc:${w.c}">${wic(w.ic)}<span class="wl">${w.l}</span><span class="wb" role="img" aria-label="${w.l}: ${w.on?'recomendado':'poco indicado'}"><i style="width:${w.on?92:14}%"></i></span></div>`).join('')}</div>`;

// sección de inicio "Por cómo huelen": cada familia con sus notas más típicas
O.famSection=(gs,title='Por cómo huelen')=>{const rows=E.FAMS.map(([k,n,c])=>{const its=gs.filter(x=>E.famOf(x.cur)?.[0]===k);if(!its.length)return '';
   const cnt={};its.forEach(x=>O.notes(x.cur).forEach(t=>{(cnt[t.key]=cnt[t.key]||{t,c:0}).c++}));
   const top=Object.values(cnt).sort((a,b)=>b.c-a.c).slice(0,6);
   return `<div class="fr" style="--c:${c}"><h3><button type="button" data-fam="${k}"><i class="dot" style="--c:${c}"></i>${n}<small>${its.length} perfumes</small></button></h3><div class="nts">${top.map((o,j)=>O.tile(o.t,j<2?64:52)).join('')}</div></div>`}).join('');
  return `<section class="sec famsec" aria-labelledby="hFam"><div class="sec-h"><div><h2 id="hFam">${title}</h2><p>Toca una familia para ver sus perfumes, o una nota para buscarla</p></div></div><div class="frs">${rows}</div></section>`};

O.block=i=>`<div class="block olfb"><div class="olfp"><h2 class="ph">Acordes principales</h2>${O.accordsHTML(i)}</div>
  <div class="olfp"><h2 class="ph">Pirámide del perfume</h2>${O.pyramidHTML(i)}<p class="olfnote">Notas clasificadas por tipo de ingrediente. Toca una para buscar perfumes que la lleven.</p></div>
  <div class="olfp"><h2 class="ph">Cuándo usarlo</h2>${O.whenHTML(i)}</div>
  <p class="rmeta">Duración ${'●'.repeat(i.p.dur)}${'○'.repeat(5-i.p.dur)} · Estela ${'●'.repeat(i.p.sil)}${'○'.repeat(5-i.p.sil)} · ${esc(i.p.use)}</p></div>`;
E.olf=i=>O.block(i);
document.addEventListener('click',e=>{const b=e.target.closest('[data-note]');if(!b)return;E.S.q=b.dataset.note;document.querySelectorAll('#q,[data-q]').forEach(q=>q.value=E.S.q);E.FAM=null;location.hash='#catalogo'});
window.O=O;
})();
