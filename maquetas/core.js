// Núcleo compartido por las maquetas: datos, perfiles y cálculos de precio. Sin estilos.
(function(){
const SHOPS=[
  {id:'notino',n:'Notino',auto:true,s:q=>'https://www.notino.es/search.asp?exps='+q},
  {id:'perfumesclub',n:"Perfume's Club",auto:true,s:q=>'https://www.google.com/search?q=site%3Aperfumesclub.com+'+q},
  {id:'sephora',n:'Sephora',auto:true,s:q=>'https://www.google.com/search?q=site%3Asephora.es+'+q},
  {id:'lookfantastic',n:'Lookfantastic',auto:true,s:q=>'https://www.google.com/search?q=site%3Alookfantastic.es+'+q},
  {id:'laguna',n:'Perfumerías Laguna',auto:true,s:q=>'https://www.google.com/search?q=site%3Aperfumeriaslaguna.com+'+q},
  {id:'paco',n:'Paco Perfumerías',auto:true,s:q=>'https://www.google.com/search?q=site%3Apacoperfumerias.com+'+q},
  {id:'sabina',n:'Sabina',auto:true,s:q=>'https://www.google.com/search?q=site%3Asabina.com+'+q},
  {id:'parejo',n:'Joyería Parejo',auto:true,s:q=>'https://www.google.com/search?q=site%3Ajoyeriaparejo.com+'+q},
  {id:'avenida',n:'Perfumerías Avenida',auto:true,s:q=>'https://www.google.com/search?q=site%3Aperfumeriasavenida.com+'+q},
  {id:'brasty',n:'Brasty',auto:true,s:q=>'https://www.google.com/search?q=site%3Abrasty.es+'+q},
  {id:'beautinow',n:'Beautinow',auto:true,eu:'Países Bajos',s:q=>'https://www.google.com/search?q=site%3Abeautinow.com+'+q},
  {id:'arabicparfums',n:'Arabic Parfums',auto:true,s:q=>'https://arabicparfums.com/search?q='+q},
  {id:'douglas',n:'Douglas',auto:true,s:q=>'https://www.douglas.es/es/search?q='+q},
  {id:'idealo',n:'Idealo (comparador)',auto:true,s:q=>'https://www.idealo.es/resultados.html?q='+q},
  {id:'firstinfragrance',n:'First in Fragrance',auto:true,eu:'Alemania',s:q=>'https://www.google.com/search?q=site%3Aausliebezumduft.de+'+q},
  {id:'coqueteo',n:'Perfumerías Coqueteo',s:q=>'https://www.google.com/search?q=site%3Aperfumeriascoqueteo.com+'+q},
  {id:'marvimundo',n:'Marvimundo',s:q=>'https://www.google.com/search?q=site%3Amarvimundo.com+'+q},
  {id:'arenal',n:'Arenal',s:q=>'https://www.google.com/search?q=site%3Aarenal.com+'+q},
  {id:'primor',n:'Primor',s:q=>'https://www.google.com/search?q=site%3Aprimor.eu+'+q},
  {id:'druni',n:'Druni',s:q=>'https://www.google.com/search?q=site%3Adruni.es+'+q},
  {id:'julia',n:'Perfumes Julia',s:q=>'https://www.google.com/search?q=site%3Aperfumesjulia.com+'+q},
  {id:'eci',n:'El Corte Inglés',s:q=>'https://www.google.com/search?q=site%3Aelcorteingles.es+'+q},
  {id:'amazon',n:'Amazon',s:q=>'https://www.amazon.es/s?k='+q},
];
const SHOP=Object.fromEntries(SHOPS.map(s=>[s.id,s]));
const SEASONS=['Primavera','Verano','Otoño','Invierno'];
// Reference profiles: family, key notes, seasons, use, duration and sillage (1-5), illustration shape and colors.
const P=(g,fam,notes,se,use,dur,sil,shape,liq,cap)=>({g,fam,notes,se,use,dur,sil,shape,liq,cap});
const PROFILES={
 'burberry-goddess-edp-100':P("Mujer","Gourmand aromática","Lavanda, vainilla, cacao",["Otoño", "Invierno"],"Diario y noche",4,4,'tall','#d8b98a','#c9a24e'),
 'carolina-herrera-la-bomba-edp-80':P("Mujer","Floral","Pitahaya, peonía, vainilla",["Primavera", "Otoño"],"Noche",4,3,'bust','#c8344a','#c9a24e'),
 'rabanne-olympea-edp-80':P("Mujer","Oriental salada","Mandarina verde, vainilla salada, jazmín",["Otoño", "Invierno"],"Noche",4,4,'bust','#e9e2d6','#c9a24e'),
 'rabanne-invictus-victory-elixir-parfum-100':P("Hombre","Ámbar especiada","Cardamomo, incienso, vainilla",["Invierno"],"Noche y frío",5,5,'flask','#2a2a2e','#c9a24e'),
 'prada-luna-rossa-ocean-edt-100':P("Hombre","Aromática","Bergamota, iris, ante",["Primavera", "Verano"],"Diario",3,3,'flask','#2f4f7a','#c0c4c8'),
 'prada-candy-edp-80':P("Mujer","Gourmand","Caramelo, almizcle, benjuí",["Otoño", "Invierno"],"Noche",4,4,'block','#d98a9a','#c9a24e'),
 'gucci-bloom-edp-100':P("Mujer","Floral","Nardo, jazmín, madreselva",["Primavera", "Verano"],"Diario",4,3,'block','#efc6cf','#d9d9d9'),
 'gucci-guilty-pour-homme-edt-90':P("Hombre","Aromática","Lavanda, limón, cedro",["Primavera", "Verano"],"Diario",3,3,'block','#3a3c44','#c0c4c8'),
 'gucci-flora-gorgeous-gardenia-edp-100':P("Mujer","Floral frutal","Pera, gardenia, azúcar moreno",["Primavera", "Verano"],"Diario",4,3,'bust','#f2d6dc','#c9a24e'),
 'dolce-gabbana-devotion-edp-100':P("Mujer","Gourmand floral","Azahar, limón confitado, vainilla",["Otoño", "Invierno"],"Noche",4,3,'bust','#e6d2b0','#c9a24e'),
 'dolce-gabbana-the-one-edp-75':P("Mujer","Floral oriental","Melocotón, lirio, vainilla",["Otoño", "Invierno"],"Noche",4,3,'block','#e2c26a','#c9a24e'),
 'armani-acqua-di-gio-parfum-parfum-125':P("Hombre","Aromática acuática","Notas marinas, salvia, incienso",["Primavera", "Verano", "Otoño"],"Diario",4,4,'flask','#1f2f4a','#c0c4c8'),
 'armani-stronger-with-you-absolutely-parfum-100':P("Hombre","Ámbar gourmand","Ron, castaña, vainilla",["Invierno"],"Noche y frío",5,4,'block','#5a2a20','#7a7c82'),
 'hugo-boss-boss-the-scent-for-her-edp-100':P("Mujer","Floral frutal","Melocotón, osmanthus, cacao",["Otoño", "Invierno"],"Noche",4,3,'bust','#e9c2a8','#c9a24e'),
 'hugo-boss-boss-orange-man-edt-100':P("Hombre","Amaderada especiada","Manzana, vainilla, incienso",["Primavera", "Otoño"],"Diario",3,3,'block','#d9732a','#3a3c44'),
 'dior-sauvage-parfum-parfum-100':P("Hombre","Amaderada ámbar","Mandarina, sándalo, haba tonka",["Otoño", "Invierno"],"Noche",5,4,'block','#1d2a44','#3a3c44'),
 'dior-dior-homme-edt-100':P("Hombre","Amaderada","Iris, vetiver, cuero",["Primavera", "Otoño"],"Oficina",4,3,'block','#2b2b30','#c0c4c8'),
 'dior-hypnotic-poison-edt-100':P("Mujer","Oriental gourmand","Almendra, jazmín, vainilla",["Otoño", "Invierno"],"Noche",5,4,'bust','#8a1f2a','#c0c4c8'),
 'yves-saint-laurent-mon-paris-edp-90':P("Mujer","Chipre frutal","Fresa, peonía, pachulí",["Primavera", "Otoño"],"Noche",4,4,'bust','#efc6cf','#2b2a2a'),
 'yves-saint-laurent-l-homme-edt-100':P("Hombre","Amaderada especiada","Jengibre, bergamota, cedro",["Primavera", "Otoño"],"Oficina",3,3,'block','#3a3c44','#c0c4c8'),
 'yves-saint-laurent-libre-intense-edp-90':P("Mujer","Floral oriental","Lavanda, orquídea, vainilla",["Otoño", "Invierno"],"Noche",5,4,'tall','#d9a640','#2b2a2a'),
 'chanel-bleu-de-chanel-parfum-parfum-100':P("Hombre","Amaderada aromática","Limón, sándalo, cedro",["Primavera", "Verano", "Otoño", "Invierno"],"Diario y noche",5,4,'block','#1f2a44','#1d1d1f'),
 'chanel-gabrielle-edp-100':P("Mujer","Floral","Tuberosa, jazmín, ylang-ylang",["Primavera", "Verano"],"Diario",4,3,'block','#efe6d6','#c9a24e'),
 'chanel-chance-edt-100':P("Mujer","Chipre floral","Pimienta rosa, jazmín, pachulí",["Primavera", "Verano", "Otoño"],"Diario",4,3,'flask','#efc6cf','#d9d9d9'),
 'lancome-la-nuit-tresor-edp-100':P("Mujer","Gourmand oriental","Frambuesa, rosa, vainilla",["Otoño", "Invierno"],"Noche",5,4,'bust','#2a1a2a','#c9a24e'),
 'givenchy-irresistible-edp-80':P("Mujer","Floral frutal","Pera, rosa, almizcle",["Primavera", "Verano"],"Diario",3,3,'bust','#f2c6cf','#c0c4c8'),
 'givenchy-pi-edt-100':P("Hombre","Oriental amaderada","Mandarina, almendra, vainilla",["Otoño", "Invierno"],"Noche",4,3,'flask','#2a3f6a','#c0c4c8'),
 'marc-jacobs-daisy-edt-100':P("Mujer","Floral frutal","Fresa, violeta, almizcle",["Primavera", "Verano"],"Día",3,2,'bust','#f2e9e0','#d9d9d9'),
 'nina-ricci-nina-edt-80':P("Mujer","Floral frutal","Manzana, praliné, almizcle",["Primavera", "Verano"],"Diario",3,3,'bust','#c8202c','#c0c4c8'),
 'calvin-klein-euphoria-edp-100':P("Mujer","Oriental floral","Granada, orquídea, ámbar",["Otoño", "Invierno"],"Noche",4,3,'flask','#6a2a5a','#c0c4c8'),
 'versace-eros-pour-femme-edp-100':P("Mujer","Floral amaderada","Limón, jazmín, sándalo",["Primavera", "Otoño"],"Noche",4,3,'tall','#e9e2d6','#c9a24e'),
 'versace-crystal-noir-edt-90':P("Mujer","Oriental floral","Gardenia, coco, ámbar",["Otoño", "Invierno"],"Noche",4,3,'bust','#1d1d1f','#c9a24e'),
 'kenzo-flower-by-kenzo-edp-100':P("Mujer","Floral atalcada","Amapola, violeta, vainilla",["Primavera", "Otoño"],"Diario",4,3,'tall','#e9c2cf','#d9d9d9'),
 'hermes-twilly-d-hermes-edp-85':P("Mujer","Floral especiada","Jengibre, tuberosa, sándalo",["Primavera", "Otoño"],"Diario",4,3,'bust','#e9a24e','#d9d9d9'),
 'tom-ford-black-orchid-edp-100':P("Unisex","Oriental floral","Trufa, orquídea negra, pachulí",["Otoño", "Invierno"],"Noche",5,4,'block','#1d1d1f','#c9a24e'),
 'tom-ford-lost-cherry-edp-50':P("Unisex","Gourmand frutal","Cereza, almendra, haba tonka",["Otoño", "Invierno"],"Noche",4,4,'block','#7a1020','#1d1d1f'),
 'creed-viking-edp-100':P("Hombre","Aromática especiada","Pimienta rosa, menta, sándalo",["Primavera", "Otoño"],"Diario",4,3,'tall','#3a3f44','#c0c4c8'),
 'parfums-de-marly-herod-edp-125':P("Hombre","Oriental especiada","Tabaco, canela, vainilla",["Invierno"],"Noche y frío",5,4,'tall','#7a4a24','#c9a24e'),
 'maison-francis-kurkdjian-baccarat-rouge-540-extrait-parfum-70':P("Unisex","Ámbar floral","Almendra amarga, azafrán, ámbar",["Primavera", "Verano", "Otoño", "Invierno"],"Noche",5,5,'block','#b0202c','#c9a24e'),
 'nishane-hacivat-parfum-50':P("Unisex","Chipre frutal","Piña, pomelo, musgo de roble",["Primavera", "Verano"],"Diario",5,4,'block','#2b2b30','#c9a24e'),
 'amouage-guidance-edp-100':P("Unisex","Floral ámbar","Pera, avellana, incienso",["Otoño", "Invierno"],"Noche",5,5,'flask','#d9c9a8','#c9a24e'),
 'jo-malone-wood-sage-sea-salt-edc-100':P("Unisex","Amaderada marina","Salvia, sal marina, ambrette",["Primavera", "Verano"],"Día",2,2,'block','#efeae2','#1d1d1f'),
 'ariana-grande-cloud-edp-100':P("Mujer","Gourmand","Lavanda, coco, praliné",["Primavera", "Verano", "Otoño", "Invierno"],"Diario",4,3,'bust','#cfe0f0','#d9d9d9'),
 'lattafa-khamrah-qahwa-edp-100':P("Unisex","Gourmand especiada","Café, canela, praliné",["Otoño", "Invierno"],"Noche y frío",4,4,'bust','#4a2a1a','#c9a24e'),
 'lattafa-fakhar-black-edp-100':P("Hombre","Aromática","Manzana, lavanda, haba tonka",["Primavera", "Otoño"],"Diario",3,3,'block','#1d1d1f','#c0c4c8'),
 'afnan-9-pm-edp-100':P("Hombre","Ámbar gourmand","Manzana, canela, vainilla",["Otoño", "Invierno"],"Noche",4,4,'block','#2a2a2e','#c9a24e'),
 'rasasi-hawas-for-him-edp-100':P("Hombre","Aromática acuática","Manzana, ciruela, ámbar gris",["Primavera", "Verano"],"Verano",4,4,'flask','#2f6f8f','#c0c4c8'),
 'al-haramain-amber-oud-gold-edition-edp-120':P("Unisex","Ámbar dulce","Bergamota, melón, ámbar",["Primavera", "Verano", "Otoño", "Invierno"],"Diario",5,5,'block','#d9a640','#c9a24e'),
 'armani-acqua-di-gio-profondo-edp-75':P("Hombre","Aromática acuática","Notas marinas, bergamota, romero",["Primavera", "Verano"],"Día y verano",4,3,'flask','#1f4f7a','#c0c4c8'),
 'armani-my-way-edp-90':P("Mujer","Floral","Bergamota, tuberosa, vainilla",["Primavera", "Otoño"],"Diario",4,3,'tall','#e9c9b9','#2b2a2a'),
 'azzaro-wanted-by-night-edp-100':P("Hombre","Oriental especiada","Canela, tabaco, cedro rojo",["Otoño", "Invierno"],"Noche",4,4,'flask','#7a1f1f','#2b2a2a'),
 'burberry-london-for-men-edt-100':P("Hombre","Oriental especiada","Canela, cuero, tabaco",["Otoño", "Invierno"],"Diario y oficina",3,3,'block','#6a4a2e','#3a3c44'),
 'bvlgari-aqva-pour-homme-edt-100':P("Hombre","Acuática","Mandarina, algas, cedro",["Primavera", "Verano"],"Verano",3,3,'flask','#2f6f8f','#c0c4c8'),
 'bvlgari-omnia-crystalline-edt-65':P("Mujer","Floral acuática","Bambú, loto, té",["Primavera", "Verano"],"Día",2,2,'flask','#dfe9ec','#c0c4c8'),
 'calvin-klein-obsession-for-men-edt-125':P("Hombre","Oriental especiada","Mandarina, lavanda, ámbar",["Otoño", "Invierno"],"Noche",4,4,'block','#7a4a24','#2b2a2a'),
 'carolina-herrera-212-men-edt-100':P("Hombre","Amaderada aromática","Jengibre, pimienta, almizcle",["Primavera", "Verano"],"Diario",3,3,'flask','#c6ccd2','#3a3c44'),
 'carolina-herrera-very-good-girl-edp-80':P("Mujer","Floral frutal","Grosella roja, rosa, vainilla",["Otoño", "Invierno"],"Noche",4,4,'tall','#b0202c','#c9a24e'),
 'chanel-egoiste-platinum-edt-100':P("Hombre","Aromática fougère","Lavanda, romero, vetiver",["Primavera", "Otoño"],"Oficina",3,3,'block','#cfd3d6','#3a3c44'),
 'chanel-chance-eau-tendre-edt-100':P("Mujer","Floral frutal","Membrillo, jazmín, almizcle",["Primavera", "Verano"],"Diario",3,3,'flask','#efc6cf','#d9d9d9'),
 'creed-green-irish-tweed-edp-100':P("Hombre","Aromática verde","Verbena, iris, sándalo",["Primavera", "Verano"],"Diario",4,3,'tall','#3f6b3a','#c0c4c8'),
 'creed-silver-mountain-water-edp-100':P("Unisex","Cítrica aromática","Bergamota, té verde, casis",["Primavera", "Verano"],"Día",3,3,'tall','#c8d4dc','#c0c4c8'),
 'davidoff-the-game-edt-100':P("Hombre","Amaderada aromática","Enebro, lirio, madera",["Primavera", "Otoño"],"Diario",3,3,'block','#3a3c44','#c0c4c8'),
 'dior-fahrenheit-edt-100':P("Hombre","Amaderada aromática","Violeta, cuero, nuez moscada",["Otoño", "Invierno"],"Diario y noche",4,4,'block','#b0502a','#1d1d1f'),
 'dior-miss-dior-edp-100':P("Mujer","Floral","Rosa, iris, almizcle",["Primavera", "Verano"],"Diario",4,3,'bust','#efb6c3','#d9d9d9'),
 'diptyque-philosykos-edt-100':P("Unisex","Amaderada verde","Higuera, coco, cedro",["Primavera", "Verano"],"Día",3,2,'tall','#dfe6cf','#1d1d1f'),
 'dolce-gabbana-k-by-dolce-gabbana-edt-100':P("Hombre","Aromática","Naranja sanguina, enebro, vetiver",["Primavera", "Verano"],"Diario",3,3,'block','#2b2b30','#c9a24e'),
 'givenchy-gentleman-reserve-privee-edp-100':P("Hombre","Amaderada","Whisky, iris, ámbar",["Otoño", "Invierno"],"Noche",4,3,'block','#6a4428','#1d1d1f'),
 'guerlain-shalimar-edp-90':P("Mujer","Oriental","Bergamota, iris, vainilla",["Otoño", "Invierno"],"Noche",5,4,'bust','#2f5a9a','#c9a24e'),
 'hermes-h24-edt-100':P("Hombre","Aromática","Salvia, narciso, palo de rosa",["Primavera", "Verano"],"Diario",3,2,'block','#bfc7cc','#3a3c44'),
 'hugo-boss-boss-bottled-tonic-edt-100':P("Hombre","Cítrica amaderada","Pomelo, jengibre, vetiver",["Primavera", "Verano"],"Día",3,3,'block','#e3c86a','#b9bcc0'),
 'hugo-boss-boss-bottled-beyond-edp-100':P("Hombre","Amaderada especiada","Jengibre, cuero, cedro",["Otoño", "Invierno"],"Noche",4,4,'block','#2a2a2e','#c9a24e'),
 'hugo-boss-boss-alive-edp-80':P("Mujer","Frutal amaderada","Ciruela, canela, vainilla",["Otoño", "Invierno"],"Diario y noche",4,3,'bust','#e9c9c0','#c9a24e'),
 'initio-side-effect-edp-90':P("Unisex","Ámbar especiada","Ron, tabaco, vainilla",["Invierno"],"Noche y frío",5,4,'block','#5a1f2a','#c9a24e'),
 'issey-miyake-l-eau-d-issey-edt-100':P("Mujer","Floral acuática","Loto, melón, almizcle",["Primavera", "Verano"],"Día",3,2,'tall','#e5e9ee','#c0c4c8'),
 'jean-paul-gaultier-le-male-elixir-absolu-parfum-125':P("Hombre","Ámbar","Lavanda, haba tonka, ámbar",["Invierno"],"Noche y frío",5,5,'bust','#8a4a1a','#c9a24e'),
 'kilian-love-don-t-be-shy-edp-50':P("Unisex","Gourmand floral","Azahar, malvavisco, vainilla",["Otoño", "Invierno"],"Noche",4,4,'flask','#f0d2c4','#c9a24e'),
 'lancome-tresor-edp-100':P("Mujer","Floral oriental","Rosa, melocotón, vainilla",["Otoño", "Invierno"],"Noche",4,4,'bust','#e9b6a8','#c9a24e'),
 'lattafa-asad-edp-100':P("Hombre","Ámbar especiada","Pimienta negra, piña, vainilla",["Otoño", "Invierno"],"Noche",4,4,'block','#2a2a2e','#c9a24e'),
 'lattafa-yara-edp-100':P("Mujer","Gourmand floral","Orquídea, tropical, vainilla",["Primavera", "Verano"],"Diario",4,3,'bust','#efb6c8','#c9a24e'),
 'le-labo-another-13-edp-100':P("Unisex","Almizclada","Ambroxan, almizcle, musgo",["Primavera", "Verano", "Otoño", "Invierno"],"Diario",4,2,'tall','#efeae2','#1d1d1f'),
 'maison-francis-kurkdjian-aqua-universalis-edt-70':P("Unisex","Cítrica floral","Bergamota, lirio del valle, almizcle",["Primavera", "Verano"],"Día",3,2,'block','#eef2f4','#c0c4c8'),
 'maison-margiela-replica-by-the-fireplace-edt-100':P("Unisex","Amaderada ahumada","Castaña, clavo, vainilla",["Invierno"],"Frío",3,3,'tall','#8a5a3a','#e4ddd2'),
 'mancera-instant-crush-edp-120':P("Unisex","Ámbar","Azafrán, ámbar, rosa",["Otoño", "Invierno"],"Noche",5,5,'tall','#8a2a3a','#c9a24e'),
 'montblanc-legend-spirit-edt-100':P("Hombre","Aromática acuática","Pomelo, lavanda, almizcle",["Primavera", "Verano"],"Diario",3,3,'block','#e3e6ea','#3a3c44'),
 'mugler-a-men-edt-100':P("Hombre","Gourmand oriental","Café, pachulí, alquitrán",["Otoño", "Invierno"],"Noche",5,5,'flask','#2a2f5a','#3a3c44'),
 'mugler-angel-edp-100':P("Mujer","Gourmand","Pachulí, caramelo, vainilla",["Otoño", "Invierno"],"Noche",5,5,'bust','#3a4f9a','#c9a24e'),
 'narciso-rodriguez-bleu-noir-edp-100':P("Hombre","Amaderada almizclada","Nuez moscada, almizcle, ébano",["Otoño", "Invierno"],"Noche",4,3,'block','#1f2a44','#1d1d1f'),
 'parfums-de-marly-pegasus-edp-125':P("Hombre","Ámbar","Almendra, vainilla, sándalo",["Otoño", "Invierno"],"Noche",5,4,'tall','#2f3f6a','#c9a24e'),
 'prada-l-homme-edt-100':P("Hombre","Floral amaderada","Iris, neroli, ámbar",["Primavera", "Verano", "Otoño"],"Oficina",4,3,'tall','#e2dfda','#1d1d1f'),
 'rabanne-1-million-elixir-parfum-100':P("Hombre","Ámbar","Manzana, rosa, haba tonka",["Invierno"],"Noche",5,5,'block','#7a1f1f','#c9a24e'),
 'rabanne-fame-edp-80':P("Mujer","Floral","Mango, jazmín, incienso",["Otoño", "Invierno"],"Noche",4,4,'bust','#e2c26a','#c9a24e'),
 'ralph-lauren-polo-red-edt-125':P("Hombre","Amaderada especiada","Pomelo, azafrán, café",["Otoño", "Invierno"],"Noche",3,3,'flask','#b0202c','#3a3c44'),
 'tom-ford-tobacco-vanille-edp-50':P("Unisex","Oriental especiada","Tabaco, vainilla, cacao",["Invierno"],"Noche y frío",5,4,'block','#7a4a24','#1d1d1f'),
 'tom-ford-noir-extreme-edp-100':P("Hombre","Oriental amaderada","Cardamomo, kulfi, sándalo",["Otoño", "Invierno"],"Noche",4,4,'block','#2a2420','#c9a24e'),
 'valentino-uomo-born-in-roma-intense-edp-100':P("Hombre","Amaderada","Vainilla, lavanda, vetiver",["Otoño", "Invierno"],"Noche",4,4,'block','#1f2a44','#7a7c82'),
 'versace-pour-homme-edt-100':P("Hombre","Aromática acuática","Neroli, cedro, almizcle",["Primavera", "Verano"],"Diario",3,2,'tall','#3f6fb0','#c9a24e'),
 'versace-eros-flame-edp-100':P("Hombre","Amaderada especiada","Naranja sanguina, pimienta, vainilla",["Otoño", "Invierno"],"Noche",4,4,'tall','#b03a1f','#c9a24e'),
 'viktor-rolf-flowerbomb-edp-100':P("Mujer","Floral oriental","Té, rosa, pachulí",["Otoño", "Invierno"],"Noche",4,4,'bust','#efb6c8','#d9d9d9'),
 'xerjoff-erba-pura-edp-100':P("Unisex","Frutal ámbar","Frutas, almizcle, vainilla",["Primavera", "Verano", "Otoño", "Invierno"],"Diario",5,5,'block','#d9a640','#c9a24e'),
 'yves-saint-laurent-y-edt-100':P("Hombre","Aromática fougère","Jengibre, salvia, cedro",["Primavera", "Verano"],"Diario",3,3,'tall','#3a5f9a','#c0c4c8'),
 'yves-saint-laurent-myslf-edp-100':P("Hombre","Amaderada floral","Bergamota, azahar, pachulí",["Primavera", "Otoño"],"Diario",4,3,'tall','#2b2b30','#c0c4c8'),
 'amouage-reflection-man-edp-100':P("Hombre","Floral amaderada","Neroli, jazmín, sándalo",["Primavera", "Verano"],"Diario",4,3,'flask','#e7e2d6','#c9a24e'),
 'byredo-bal-d-afrique-edp-100':P("Unisex","Amaderada floral","Neroli, violeta, vetiver",["Primavera", "Verano"],"Día",3,2,'tall','#efe6d6','#1d1d1f'),
 'armaf-club-de-nuit-milestone-edp-105':P("Unisex","Acuática","Notas marinas, violeta, sándalo",["Primavera", "Verano"],"Día",4,4,'tall','#cfd9df','#c0c4c8'),
 'hugo-boss-boss-bottled-edt-100':P('Hombre','Amaderada especiada','Manzana, canela, sándalo',['Primavera','Otoño','Invierno'],'Diario y oficina',3,3,'block','#d8c3a0','#b9bcc0'),
 'hugo-boss-boss-bottled-edp-100':P('Hombre','Amaderada especiada','Manzana, canela, vetiver',['Otoño','Invierno'],'Diario y tarde',4,3,'block','#c79b5b','#4b4b4d'),
 'hugo-boss-boss-bottled-parfum-parfum-100':P('Hombre','Amaderada aromática','Mandarina, salvia, cuero',['Otoño','Invierno'],'Tarde y noche',4,3,'block','#9d7a4e','#2f2f31'),
 'hugo-boss-boss-bottled-elixir-elixir-100':P('Hombre','Ámbar amaderada','Incienso, cardamomo, pachulí',['Otoño','Invierno'],'Noche y eventos',5,4,'block','#5b3b25','#1d1d1f'),
 'hugo-boss-boss-bottled-infinite-edp-100':P('Hombre','Aromática fougère','Mandarina, lavanda, sándalo',['Primavera','Otoño'],'Diario y oficina',3,3,'block','#3e5f86','#b9bcc0'),
 'hugo-boss-boss-bottled-absolu-parfum-100':P('Hombre','Amaderada intensa','Cuero, incienso, pachulí',['Invierno'],'Noche',4,4,'block','#3a2c26','#1d1d1f'),
 'hugo-boss-boss-bottled-night-edt-100':P('Hombre','Amaderada aromática','Abedul, lavanda, cardamomo',['Otoño','Invierno'],'Noche',3,2,'block','#2c2a33','#6a6c72'),
 'hugo-boss-boss-the-scent-edt-100':P('Hombre','Oriental especiada','Jengibre, maninka, cuero',['Otoño','Invierno'],'Citas y noche',3,3,'tall','#a8642a','#2b2a2a'),
 'hugo-boss-boss-the-scent-le-parfum-parfum-100':P('Hombre','Oriental especiada','Jengibre, lavanda, cuero',['Otoño','Invierno'],'Noche',4,3,'tall','#6d3c1e','#1d1d1f'),
 'hugo-boss-hugo-man-edt-125':P('Hombre','Aromática verde','Manzana verde, menta, abeto',['Primavera','Verano'],'Diario e informal',2,3,'flask','#6f9b4f','#9fa3a8'),
 'jean-paul-gaultier-le-male-edt-125':P('Hombre','Oriental fougère','Lavanda, menta, vainilla',['Primavera','Otoño','Invierno'],'Diario y noche',4,4,'bust','#7fa8c9','#c0c4c8'),
 'jean-paul-gaultier-le-male-elixir-parfum-125':P('Hombre','Ámbar fougère','Lavanda, miel, haba tonka',['Otoño','Invierno'],'Noche y frío',5,5,'bust','#c9922f','#c9a24e'),
 'jean-paul-gaultier-le-male-le-parfum-edp-125':P('Hombre','Oriental amaderada','Cardamomo, lavanda, vainilla',['Otoño','Invierno'],'Tarde y noche',4,4,'bust','#3b4a6b','#c9a24e'),
 'jean-paul-gaultier-le-beau-edt-125':P('Hombre','Amaderada aromática','Coco, bergamota, haba tonka',['Primavera','Verano'],'Día y vacaciones',3,3,'bust','#86b98a','#9d7f53'),
 'jean-paul-gaultier-le-beau-le-parfum-edp-125':P('Hombre','Amaderada aromática','Piña, iris, coco',['Primavera','Verano'],'Día y noches de verano',4,4,'bust','#4f7f5a','#9d7f53'),
 'jean-paul-gaultier-scandal-pour-homme-edt-100':P('Hombre','Ámbar fougère','Caramelo, salvia, haba tonka',['Otoño','Invierno'],'Noche',4,4,'flask','#a3622f','#b8a06a'),
 'jean-paul-gaultier-ultra-male-edt-125':P('Hombre','Oriental fougère','Pera, lavanda, vainilla negra',['Otoño','Invierno'],'Noche y fiesta',4,5,'bust','#2d2f38','#3a3c44'),
 'jean-paul-gaultier-la-belle-edp-100':P('Mujer','Oriental vainilla','Pera, bergamota, vainilla',['Otoño','Invierno'],'Diario y noche',4,4,'bust','#7fb26a','#c9a24e'),
 'jean-paul-gaultier-scandal-edp-80':P('Mujer','Chipre floral','Miel, gardenia, pachulí',['Otoño','Invierno'],'Noche',4,4,'flask','#d39a3a','#c8a7b7'),
 'jean-paul-gaultier-gaultier-divine-edp-100':P('Mujer','Floral salina','Lirio, notas marinas, merengue',['Primavera','Verano','Otoño'],'Diario',4,3,'bust','#e7d8c4','#c9a24e'),
 'dior-sauvage-edt-100':P("Hombre","Aromática fougère","Bergamota, pimienta, ambroxan",["Primavera", "Verano", "Otoño"],"Diario",4,4,'flask','#3b5a8a','#1d1d1f'),
 'dior-sauvage-edp-100':P("Hombre","Ámbar fougère","Bergamota, nuez moscada, vainilla",["Otoño", "Invierno"],"Diario y noche",4,4,'flask','#26385e','#1d1d1f'),
 'dior-sauvage-elixir-elixir-60':P("Hombre","Ámbar especiada","Canela, lavanda, regaliz",["Invierno"],"Noche y frío",5,5,'flask','#5a2e1e','#1d1d1f'),
 'dior-dior-homme-intense-edp-100':P("Hombre","Amaderada floral","Iris, ámbar, vetiver",["Otoño", "Invierno"],"Tarde y noche",4,3,'tall','#6b5a62','#2b2a2a'),
 'dior-j-adore-edp-100':P("Mujer","Floral","Ylang-ylang, rosa, jazmín",["Primavera", "Verano"],"Diario y eventos",4,3,'bust','#e6c46a','#c9a24e'),
 'chanel-bleu-de-chanel-edp-100':P("Hombre","Amaderada aromática","Pomelo, incienso, sándalo",["Primavera", "Verano", "Otoño", "Invierno"],"Diario y oficina",4,3,'block','#1f2f4f','#1d1d1f'),
 'chanel-allure-homme-sport-edt-100':P("Hombre","Amaderada cítrica","Naranja, notas marinas, haba tonka",["Primavera", "Verano"],"Día y deporte",3,3,'tall','#c7cbd1','#3a3c44'),
 'chanel-coco-mademoiselle-edp-100':P("Mujer","Chipre floral","Naranja, rosa, pachulí",["Primavera", "Otoño"],"Diario y noche",4,4,'block','#e7a99a','#c9a24e'),
 'chanel-chanel-n-5-edp-100':P("Mujer","Floral aldehídica","Aldehídos, ylang-ylang, sándalo",["Otoño", "Invierno"],"Eventos",4,3,'block','#e9d6a6','#d9d9d9'),
 'yves-saint-laurent-y-edp-100':P("Hombre","Aromática fougère","Manzana, salvia, haba tonka",["Primavera", "Otoño"],"Diario y noche",4,4,'tall','#2b3e66','#c0c4c8'),
 'yves-saint-laurent-la-nuit-de-l-homme-edt-100':P("Hombre","Oriental especiada","Cardamomo, lavanda, cedro",["Otoño", "Invierno"],"Citas y noche",2,2,'tall','#2a2a2e','#3a3c44'),
 'yves-saint-laurent-libre-edp-90':P("Mujer","Floral lavanda","Lavanda, azahar, vainilla",["Otoño", "Invierno"],"Diario y noche",4,4,'block','#d8b46a','#1d1d1f'),
 'yves-saint-laurent-black-opium-edp-90':P("Mujer","Oriental vainilla","Café, vainilla, flor de azahar",["Otoño", "Invierno"],"Noche",4,4,'tall','#2a1f2e','#c9a24e'),
 'rabanne-1-million-edt-100':P("Hombre","Ámbar especiada","Mandarina sanguina, canela, cuero",["Otoño", "Invierno"],"Noche y fiesta",4,4,'block','#d9a640','#c9a24e'),
 'rabanne-invictus-edt-100':P("Hombre","Aromática acuática","Pomelo, notas marinas, laurel",["Primavera", "Verano"],"Día y deporte",3,4,'flask','#a9c3d9','#c0c4c8'),
 'rabanne-phantom-edt-100':P("Hombre","Aromática","Lavanda, limón, vainilla",["Primavera", "Otoño"],"Diario",3,3,'flask','#b9bec6','#3a3c44'),
 'rabanne-lady-million-edp-80':P("Mujer","Floral amaderada","Miel, jazmín, pachulí",["Otoño", "Invierno"],"Noche",4,4,'block','#e2b348','#c9a24e'),
 'carolina-herrera-bad-boy-edt-100':P("Hombre","Oriental especiada","Pimienta, cacao, haba tonka",["Otoño", "Invierno"],"Noche",4,4,'tall','#2c2c34','#b1832f'),
 'carolina-herrera-212-vip-men-edt-100':P("Hombre","Oriental especiada","Menta, jengibre, ámbar",["Otoño", "Invierno"],"Fiesta",3,4,'flask','#3a3a40','#c0c4c8'),
 'carolina-herrera-ch-men-edt-100':P("Hombre","Amaderada especiada","Pomelo, ante, ámbar",["Otoño", "Invierno"],"Diario y oficina",4,3,'block','#8a5a35','#3a3c44'),
 'carolina-herrera-good-girl-edp-80':P("Mujer","Oriental floral","Tuberosa, cacao, haba tonka",["Otoño", "Invierno"],"Noche",4,4,'tall','#2b2f5e','#c9a24e'),
 'armani-acqua-di-gio-edt-100':P("Hombre","Acuática","Notas marinas, bergamota, romero",["Primavera", "Verano"],"Día y verano",3,3,'flask','#cfd9df','#d9d9d9'),
 'armani-stronger-with-you-intensely-edp-100':P("Hombre","Ámbar fougère","Castaña, vainilla, canela",["Otoño", "Invierno"],"Noche y frío",5,4,'flask','#6a3a2a','#2b2a2a'),
 'armani-code-edt-75':P("Hombre","Oriental","Bergamota, anís estrellado, haba tonka",["Otoño", "Invierno"],"Citas",3,3,'flask','#262628','#3a3c44'),
 'armani-si-edp-100':P("Mujer","Chipre","Casis, rosa, vainilla",["Otoño", "Invierno"],"Diario y noche",4,4,'block','#e3b9a7','#2b2a2a'),
 'versace-eros-edt-100':P("Hombre","Aromática fougère","Menta, manzana verde, vainilla",["Otoño", "Invierno"],"Noche y fiesta",4,5,'tall','#4aa3a0','#c9a24e'),
 'versace-dylan-blue-edt-100':P("Hombre","Aromática acuática","Bergamota, pimienta, incienso",["Primavera", "Verano", "Otoño"],"Diario",3,3,'tall','#1f3f7a','#1d1d1f'),
 'versace-bright-crystal-edt-90':P("Mujer","Floral frutal","Granada, peonía, loto",["Primavera", "Verano"],"Diario",3,3,'flask','#efb9c4','#d9d9d9'),
 'dolce-gabbana-light-blue-pour-homme-edt-125':P("Hombre","Cítrica aromática","Pomelo, enebro, romero",["Verano"],"Verano",3,3,'tall','#8fb8d9','#1f2f4f'),
 'dolce-gabbana-the-one-for-men-edp-100':P("Hombre","Oriental especiada","Pomelo, tabaco, ámbar",["Otoño", "Invierno"],"Tarde y noche",4,3,'block','#9a6a3a','#b1832f'),
 'dolce-gabbana-light-blue-edt-100':P("Mujer","Floral frutal","Limón, manzana, cedro",["Primavera", "Verano"],"Día y verano",3,3,'block','#b9d6ee','#1f2f4f'),
 'azzaro-the-most-wanted-edp-100':P("Hombre","Ámbar fougère","Toffee, cardamomo, ámbar",["Otoño", "Invierno"],"Noche",4,5,'flask','#8c1f22','#2b2a2a'),
 'azzaro-chrome-edt-100':P("Hombre","Aromática acuática","Limón, notas marinas, almizcle",["Primavera", "Verano"],"Día",3,2,'flask','#c4ccd3','#c0c4c8'),
 'azzaro-wanted-edt-100':P("Hombre","Amaderada especiada","Jengibre, limón, cardamomo",["Primavera", "Otoño"],"Diario",3,3,'flask','#7a4a26','#c0c4c8'),
 'valentino-born-in-roma-uomo-edt-100':P("Hombre","Amaderada aromática","Violeta, salvia, vetiver",["Otoño", "Invierno"],"Noche",4,4,'block','#2d2d33','#7a7c82'),
 'valentino-born-in-roma-donna-edp-100':P("Mujer","Floral amaderada","Jazmín, vainilla, notas amaderadas",["Otoño", "Invierno"],"Noche",4,4,'block','#e8b7c0','#c9a24e'),
 'prada-luna-rossa-carbon-edt-100':P("Hombre","Aromática fougère","Lavanda, bergamota, ambroxan",["Primavera", "Otoño"],"Diario",3,3,'tall','#3a3d44','#c41e2a'),
 'prada-paradoxe-edp-90':P("Mujer","Ámbar floral","Neroli, ámbar, almizcle",["Primavera", "Otoño"],"Diario",4,3,'bust','#e5c9a8','#c9a24e'),
 'givenchy-gentleman-edp-100':P("Hombre","Amaderada floral","Iris, lavanda, pachulí",["Otoño", "Invierno"],"Tarde y noche",4,3,'block','#5a4636','#1d1d1f'),
 'givenchy-l-interdit-edp-80':P("Mujer","Floral","Tuberosa, azahar, pachulí",["Otoño", "Invierno"],"Noche",4,3,'block','#2b2b30','#1d1d1f'),
 'lancome-la-vie-est-belle-edp-100':P("Mujer","Gourmand","Iris, praliné, vainilla",["Otoño", "Invierno"],"Diario y noche",5,4,'bust','#e8b9c6','#d9d9d9'),
 'lancome-idole-edp-50':P("Mujer","Chipre floral","Rosa, jazmín, almizcle",["Primavera", "Verano"],"Diario",3,3,'tall','#efd4cf','#d9d9d9'),
 'calvin-klein-ck-one-edt-200':P("Unisex","Cítrica aromática","Bergamota, té verde, almizcle",["Primavera", "Verano"],"Día",2,2,'flask','#dfe6e3','#9fa3a8'),
 'calvin-klein-eternity-for-men-edt-100':P("Hombre","Aromática fougère","Lavanda, mandarina, sándalo",["Primavera", "Otoño"],"Diario",3,3,'block','#c9cdd2','#5a5c62'),
 'tom-ford-ombre-leather-edp-100':P("Unisex","Cuero","Cardamomo, cuero, jazmín",["Otoño", "Invierno"],"Noche",5,4,'block','#3a2a22','#1d1d1f'),
 'tom-ford-oud-wood-edp-50':P("Unisex","Amaderada oriental","Oud, palo de rosa, cardamomo",["Otoño", "Invierno"],"Noche y eventos",4,3,'block','#4a3426','#1d1d1f'),
 'creed-aventus-edp-100':P("Hombre","Chipre frutal","Piña, abedul, almizcle",["Primavera", "Verano", "Otoño"],"Diario y eventos",4,4,'tall','#2e2e33','#c0c4c8'),
 'montblanc-explorer-edp-100':P("Hombre","Amaderada aromática","Bergamota, vetiver, pachulí",["Primavera", "Otoño"],"Diario",4,3,'flask','#7a5a3c','#3a3c44'),
 'montblanc-legend-edt-100':P("Hombre","Aromática fougère","Lavanda, piña, haba tonka",["Primavera", "Verano"],"Diario y oficina",3,3,'block','#2b2b30','#c0c4c8'),
 'issey-miyake-l-eau-d-issey-pour-homme-edt-125':P("Hombre","Amaderada acuática","Yuzu, nuez moscada, sándalo",["Primavera", "Verano"],"Día y verano",3,3,'tall','#b9c4cc','#c0c4c8'),
 'hermes-terre-d-hermes-edt-100':P("Hombre","Amaderada cítrica","Naranja, pimienta, vetiver",["Primavera", "Verano", "Otoño"],"Diario y oficina",4,3,'block','#c47a3a','#7a5a3c'),
 'burberry-hero-edt-100':P("Hombre","Amaderada","Bergamota, enebro, cedro",["Primavera", "Otoño"],"Diario",3,3,'block','#4a4d55','#9fa3a8'),
 'burberry-her-edp-100':P("Mujer","Frutal gourmand","Fresa, frambuesa, almizcle",["Primavera", "Verano"],"Diario",4,3,'block','#e9b6c3','#c9a24e'),
 'narciso-rodriguez-for-her-edp-100':P("Mujer","Floral almizclada","Rosa, melocotón, almizcle",["Primavera", "Otoño"],"Diario y noche",4,3,'block','#e6b8b0','#c9a24e'),
 'guerlain-l-homme-ideal-edp-100':P("Hombre","Ámbar amaderada","Almendra, cuero, haba tonka",["Otoño", "Invierno"],"Tarde y noche",4,3,'block','#7a4a2a','#2b2a2a'),
 'mugler-alien-edp-60':P("Mujer","Amaderada floral","Jazmín, cachemira, ámbar",["Otoño", "Invierno"],"Noche",5,5,'bust','#5b3f8a','#c9a24e'),
 'viktor-rolf-spicebomb-extreme-edp-90':P("Hombre","Oriental especiada","Tabaco, vainilla, pimienta",["Invierno"],"Noche y frío",5,4,'block','#3a1f1f','#1d1d1f'),
 'bvlgari-man-in-black-edp-100':P("Hombre","Oriental especiada","Ron, cuero, haba tonka",["Otoño", "Invierno"],"Noche",4,4,'flask','#2a2626','#3a3c44'),
 'davidoff-cool-water-edt-125':P("Hombre","Aromática acuática","Menta, lavanda, notas marinas",["Primavera", "Verano"],"Día y verano",3,3,'tall','#3c86c4','#3a3c44'),
 'ralph-lauren-polo-blue-edp-125':P("Hombre","Aromática acuática","Melón, salvia, ante",["Primavera", "Verano"],"Diario",3,3,'flask','#2c4f8a','#c0c4c8'),
 'maison-francis-kurkdjian-baccarat-rouge-540-edp-70':P("Unisex","Ámbar floral","Azafrán, jazmín, ambergris",["Otoño", "Invierno"],"Eventos",5,5,'block','#c43a3a','#c9a24e'),
 'maison-francis-kurkdjian-grand-soir-edp-70':P("Unisex","Ámbar","Ámbar, benjuí, vainilla",["Otoño", "Invierno"],"Noche y frío",5,4,'block','#9a5a2a','#c9a24e'),
 'parfums-de-marly-layton-edp-125':P("Hombre","Ámbar floral","Manzana, lavanda, vainilla",["Otoño", "Invierno"],"Noche",5,4,'tall','#2b2b30','#c9a24e'),
 'parfums-de-marly-delina-edp-75':P("Mujer","Floral","Rosa turca, lichi, ruibarbo",["Primavera", "Otoño"],"Diario y eventos",4,4,'bust','#efb6c8','#c9a24e'),
 'xerjoff-naxos-edp-100':P("Unisex","Ámbar aromática","Miel, tabaco, lavanda",["Otoño", "Invierno"],"Noche",5,4,'block','#b07a2a','#c9a24e'),
 'initio-oud-for-greatness-edp-90':P("Unisex","Amaderada oud","Oud, azafrán, nuez moscada",["Otoño", "Invierno"],"Noche",5,5,'block','#3a2a3a','#c9a24e'),
 'amouage-interlude-man-edp-100':P("Hombre","Ámbar especiada","Incienso, oud, orégano",["Invierno"],"Noche y frío",5,5,'flask','#1f3f6a','#c9a24e'),
 'byredo-gypsy-water-edp-100':P("Unisex","Amaderada aromática","Bergamota, pino, vainilla",["Primavera", "Verano", "Otoño"],"Diario",3,2,'tall','#e4ddd2','#1d1d1f'),
 'le-labo-santal-33-edp-100':P("Unisex","Amaderada","Sándalo, cardamomo, cuero",["Primavera", "Otoño"],"Diario",4,3,'tall','#d9cbb4','#1d1d1f'),
 'kilian-angels-share-edp-50':P("Unisex","Gourmand","Coñac, canela, haba tonka",["Otoño", "Invierno"],"Noche",4,4,'flask','#8a4a1f','#c9a24e'),
 'diptyque-tam-dao-edt-100':P("Unisex","Amaderada","Sándalo, ciprés, cedro",["Primavera", "Otoño"],"Diario",3,2,'tall','#e7dccb','#1d1d1f'),
 'acqua-di-parma-colonia-edc-100':P("Unisex","Cítrica aromática","Bergamota, lavanda, rosa",["Primavera", "Verano"],"Día y verano",2,2,'block','#e9c46a','#1d1d1f'),
 'maison-margiela-replica-jazz-club-edt-100':P("Hombre","Amaderada especiada","Ron, tabaco, vainilla",["Otoño", "Invierno"],"Noche",3,3,'tall','#c08a4a','#e4ddd2'),
 'mancera-cedrat-boise-edp-120':P("Unisex","Cítrica amaderada","Limón, casis, cuero",["Primavera", "Verano", "Otoño"],"Diario",4,4,'tall','#2f6b3a','#c9a24e'),
 'lattafa-khamrah-edp-100':P("Unisex","Gourmand especiada","Canela, dátil, praliné",["Otoño", "Invierno"],"Noche y frío",4,4,'bust','#8a3a1f','#c9a24e'),
 'armaf-club-de-nuit-intense-man-edt-105':P("Hombre","Chipre frutal","Piña, abedul, almizcle",["Primavera", "Verano", "Otoño"],"Diario",4,4,'tall','#1d1d1f','#c0c4c8'),
};
const norm=s=>String(s||'').toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g,'');
const esc=s=>String(s??'').replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const eur=(n,d=2)=>n==null?'—':n.toLocaleString('es-ES',{minimumFractionDigits:d,maximumFractionDigits:d})+' €';
const base=id=>id.replace(/-\d+$/,'');
const PROF_BASE=Object.fromEntries(Object.entries(PROFILES).map(([k,v])=>[base(k),v]));
const prof=it=>PROFILES[it.id]||PROF_BASE[base(it.id)];
const tierOf=it=>it.tier||'Diseñador';
const shopName=id=>(SHOP[id]?.n||id).replace(' (comparador)','');
const DAY=864e5,todayISO=()=>new Date().toISOString().slice(0,10);
const ageDays=d=>d?Math.max(0,Math.round((Date.now()-new Date(d.slice(0,10)+'T12:00'))/DAY)):null;
// Precios en vigor: con precio, en stock y leídos hace 14 días o menos
function offers(it){
  return Object.entries(it.prices||{}).filter(([,v])=>v&&v.p!=null).map(([s,v])=>({s,name:shopName(s),p:v.p,d:v.d,age:ageDays(v.d),stock:v.stock!==false,note:v.note||'',url:(it.urls||{})[s]||(SHOP[s]?.s?.(encodeURIComponent(it.brand+' '+it.name+' '+it.ml+' ml')))})).sort((a,b)=>(b.stock-a.stock)||(a.p-b.p));
}
function best(it){const o=offers(it).filter(x=>x.stock);return o[0]||null}
const per100=it=>{const b=best(it);return b?b.p/it.ml*100:null};
function series(it){const m={};for(const h of it.history||[])if(m[h.d]==null||h.p<m[h.d])m[h.d]=h.p;return Object.entries(m).sort().map(([d,p])=>({d,p}))}
// Bajada: mejor precio de hoy frente a la media de los mejores precios diarios de los 30 días anteriores
function drop(it){
  const s=series(it),b=best(it);if(!b||s.length<3)return null;
  const cut=new Date(Date.now()-30*DAY).toISOString().slice(0,10),last=s[s.length-1].d;
  const prev=s.filter(x=>x.d>=cut&&x.d<last).map(x=>x.p);if(prev.length<2)return null;
  const avg=prev.reduce((a,c)=>a+c,0)/prev.length;
  return {avg,pct:(b.p-avg)/avg*100,min:Math.min(...s.map(x=>x.p))};
}
function valueScores(items){
  const r=items.map(it=>{const p=prof(it),c=per100(it);return p&&c?{id:it.id,v:(p.dur+p.sil)/c}:null}).filter(Boolean).sort((a,b)=>a.v-b.v);
  const out={};r.forEach((x,i)=>out[x.id]=r.length===1?3:1+Math.round(i/(r.length-1)*4));return out;
}
function bottle(p){
  const L=p?.liq||'#cbbfae',C=p?.cap||'#8c8c8c',sh=p?.shape||'block';
  const glass='fill-opacity=".9"';
  const body={
    block:`<rect x="18" y="38" width="64" height="74" rx="6" fill="${L}" ${glass}/><rect x="24" y="44" width="10" height="60" rx="4" fill="#fff" fill-opacity=".28"/><rect x="38" y="16" width="24" height="24" rx="3" fill="${C}"/>`,
    tall:`<rect x="27" y="30" width="46" height="84" rx="4" fill="${L}" ${glass}/><rect x="32" y="36" width="7" height="72" rx="3" fill="#fff" fill-opacity=".25"/><rect x="34" y="10" width="32" height="22" rx="2" fill="${C}"/>`,
    flask:`<path d="M30 40 h40 q10 0 10 12 v50 q0 12 -12 12 h-36 q-12 0 -12 -12 v-50 q0 -12 10 -12z" fill="${L}" ${glass}/><rect x="27" y="48" width="8" height="54" rx="4" fill="#fff" fill-opacity=".26"/><rect x="40" y="18" width="20" height="24" rx="10" fill="${C}"/>`,
    bust:`<path d="M50 34 c18 0 26 10 26 26 c0 16 -8 22 -8 34 c0 10 6 16 6 20 h-48 c0 -4 6 -10 6 -20 c0 -12 -8 -18 -8 -34 c0 -16 8 -26 26 -26z" fill="${L}" ${glass}/><path d="M34 52 c-2 14 4 24 2 40" stroke="#fff" stroke-opacity=".3" stroke-width="6" fill="none" stroke-linecap="round"/><rect x="42" y="12" width="16" height="24" rx="3" fill="${C}"/>`
  }[sh];
  return `<svg viewBox="0 0 100 124" role="img" aria-label="Ilustración del frasco">${body}</svg>`;
}
function lineChart(pts,{w=560,h=160,stroke='currentColor',fill='none',grid='currentColor'}={}){
  if(pts.length<2)return '<p class="chart-empty">Aún no hay historial suficiente para dibujar la evolución.</p>';
  const ps=pts.map(x=>x.p),lo=Math.min(...ps),hi=Math.max(...ps),pad=(hi-lo)*.15||1,y0=lo-pad,y1=hi+pad,L=44,B=22,T=8;
  const X=i=>L+i*(w-L-8)/(pts.length-1),Y=p=>T+(1-(p-y0)/(y1-y0))*(h-T-B);
  const ticks=[y0+(y1-y0)*.15,(y0+y1)/2,y1-(y1-y0)*.15];
  const line=pts.map((x,i)=>X(i).toFixed(1)+','+Y(x.p).toFixed(1)).join(' ');
  const lab=[0,Math.floor((pts.length-1)/2),pts.length-1];
  const fd=d=>new Date(d+'T12:00').toLocaleDateString('es-ES',{day:'numeric',month:'short'});
  return `<svg class="chart" viewBox="0 0 ${w} ${h}" role="img" aria-label="Mejor precio diario de ${fd(pts[0].d)} a ${fd(pts[pts.length-1].d)}: mínimo ${eur(lo)}, máximo ${eur(hi)}">
${ticks.map(t=>`<line x1="${L}" x2="${w-8}" y1="${Y(t)}" y2="${Y(t)}" stroke="${grid}" stroke-opacity=".12"/><text x="${L-6}" y="${Y(t)+4}" text-anchor="end">${Math.round(t)} €</text>`).join('')}
${lab.map(i=>`<text x="${X(i)}" y="${h-4}" text-anchor="${i===0?'start':i===pts.length-1?'end':'middle'}">${fd(pts[i].d)}</text>`).join('')}
<polyline points="${line}" fill="none" stroke="${stroke}" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"/>
<circle cx="${X(pts.length-1)}" cy="${Y(ps[ps.length-1])}" r="4" fill="${stroke}"/></svg>`;
}

const ICONS={
 search:'<circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/>',
 x:'<path d="M18 6 6 18"/><path d="m6 6 12 12"/>',
 chevron:'<path d="m9 18 6-6-6-6"/>',
 back:'<path d="m12 19-7-7 7-7"/><path d="M19 12H5"/>',
 drop:'<polyline points="22 17 13.5 8.5 8.5 13.5 2 7"/><polyline points="16 17 22 17 22 11"/>',
 ext:'<path d="M15 3h6v6"/><path d="M10 14 21 3"/><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/>',
 home:'<path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/>',
 compass:'<circle cx="12" cy="12" r="10"/><polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"/>',
 tag:'<path d="M12.586 2.586A2 2 0 0 0 11.172 2H4a2 2 0 0 0-2 2v7.172a2 2 0 0 0 .586 1.414l8.704 8.704a2.426 2.426 0 0 0 3.42 0l6.58-6.58a2.426 2.426 0 0 0 0-3.42z"/><circle cx="7.5" cy="7.5" r="1"/>',
 target:'<circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/>',
 sliders:'<line x1="21" x2="14" y1="4" y2="4"/><line x1="10" x2="3" y1="4" y2="4"/><line x1="21" x2="12" y1="12" y2="12"/><line x1="8" x2="3" y1="12" y2="12"/><line x1="21" x2="16" y1="20" y2="20"/><line x1="12" x2="3" y1="20" y2="20"/><line x1="14" x2="14" y1="2" y2="6"/><line x1="8" x2="8" y1="10" y2="14"/><line x1="16" x2="16" y1="18" y2="22"/>',
 list:'<path d="M3 12h18M3 6h18M3 18h18"/>',
 grid:'<rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/>',
 clock:'<circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>'
};
const icon=(n,s=18)=>`<svg class="ic" width="${s}" height="${s}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${ICONS[n]}</svg>`;
const STATE_KEYS=['q','g','tier','season','brand','sort'];
const DEFAULTS={q:'',g:'Todos',tier:'Todos',season:'Todas',brand:'Todas',sort:'drop'};
// Filtros en la URL: se pueden compartir y sobreviven a recargar
function readState(){const u=new URLSearchParams(location.search),s={...DEFAULTS};for(const k of STATE_KEYS)if(u.get(k))s[k]=u.get(k);return s}
function writeState(s){const u=new URLSearchParams();for(const k of STATE_KEYS)if(s[k]&&s[k]!==DEFAULTS[k])u.set(k,s[k]);history.replaceState(null,'',location.pathname+(u.toString()?'?'+u:'')+location.hash)}
// Agrupa los tamaños de un mismo perfume y aplica filtros y orden
function groups(items,s,sizeSel={}){
  const by={};for(const it of items)(by[it.key]=by[it.key]||[]).push(it);
  const words=norm(s.q).split(/\s+/).filter(Boolean);
  let out=Object.values(by).map(vars=>{vars.sort((a,b)=>a.ml-b.ml);const cur=vars.find(v=>v.id===sizeSel[vars[0].key])||vars.find(v=>v.b)||vars[0];return {key:vars[0].key,vars,cur}});
  out=out.filter(({cur:i})=>{const p=i.p,hay=norm(`${i.brand} ${i.name} ${i.conc} ${p?.fam||''} ${p?.notes||''}`);
    return (s.g==='Todos'||p?.g===s.g)&&(s.tier==='Todos'||tierOf(i)===s.tier)&&(s.brand==='Todas'||i.brand===s.brand)&&(s.season==='Todas'||p?.se.includes(s.season))&&words.every(w=>hay.includes(w))});
  const K={drop:x=>x.cur.dr?x.cur.dr.pct:99,price:x=>x.cur.b?.p??1e9,ml:x=>per100(x.cur)??1e9,value:x=>-(x.cur.v||0)*1e4+(per100(x.cur)??9e3),name:x=>norm(x.cur.brand+x.cur.name)};
  const k=K[s.sort]||K.drop;out.sort((a,b)=>{const x=k(a),y=k(b);return x<y?-1:x>y?1:0});
  return out;
}
const SORTS=[['drop','Mayor bajada'],['price','Precio más bajo'],['ml','Precio por 100 ml'],['value','Mejor calidad/precio'],['name','Nombre']];
function targets(){try{return JSON.parse(localStorage.getItem('rp-targets')||'{}')}catch(e){return {}}}
function setTarget(id,v){const t=targets();if(v==null)delete t[id];else t[id]=v;try{localStorage.setItem('rp-targets',JSON.stringify(t))}catch(e){}}
const ago=d=>{const n=ageDays(d);return n==null?'':n===0?'hoy':n===1?'ayer':'hace '+n+' días'};
const agoTime=t=>{if(!t)return '';const m=Math.round((Date.now()-new Date(t))/6e4);return m<60?'hace '+m+' min':m<1440?'hace '+Math.round(m/60)+' h':'hace '+Math.round(m/1440)+' d'};
const pct=x=>(x>0?'+':x<0?'−':'')+Math.abs(x).toLocaleString('es-ES',{maximumFractionDigits:0})+' %';
async function load(){
  const get=f=>fetch('../data/'+f+'?t='+Date.now(),{cache:'no-store'}).then(r=>r.ok?r.json():null).catch(()=>null);
  const [items,ch,estado]=await Promise.all([get('perfumes.json'),get('chollos.json'),get('estado.json')]);
  if(!items)return null;
  const vs=valueScores(items);
  for(const it of items){it.p=prof(it);it.b=best(it);it.v=vs[it.id]||0;it.dr=drop(it);it.key=base(it.id)}
  // Chollo de un perfume: título con su marca y su nombre
  const deals=(ch?.items||[]).filter(x=>!x.expired);
  for(const it of items){const n=norm(it.name),bw=norm(it.brand).split(' ')[0];it.deals=deals.filter(d=>{const t=norm(d.t);return t.includes(n)&&t.includes(bw)})}
  return {items,deals,estado};
}
window.RP={icon,readState,writeState,groups,SORTS,DEFAULTS,targets,setTarget,ago,agoTime,pct,tierOf:it=>it.tier||'Diseñador',SHOPS,SHOP,SEASONS,PROFILES,norm,esc,eur,prof,tierOf,shopName,ageDays,offers,best,per100,series,drop,bottle,lineChart,load,base};
})();
