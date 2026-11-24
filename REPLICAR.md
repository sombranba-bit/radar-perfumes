# REPLICAR.md — cómo montar otro comparador como Fragans (por ejemplo, de relojes)

Este archivo y `DESIGN.md` bastan para que otra conversación levante un comparador nuevo con la misma arquitectura, el mismo diseño y las lecciones ya aprendidas.

- Proyecto de referencia: https://github.com/sombranba-bit/radar-perfumes
- Web: https://sombranba-bit.github.io/radar-perfumes/

---

## 1. Qué es

Un comparador y rastreador de precios **que funciona solo en GitHub y sin servidor**:

- **GitHub Pages** publica una web estática (`index.html` + `app/` + `maquetas/core.js`) que lee los datos JSON del propio repositorio.
- **GitHub Actions** lanza un lector en Python cada 30 minutos. El lector visita las fichas de cada tienda, guarda precio, existencias y foto en `data/*.json` y hace commit.
- Todo es gratis y no hay nada que mantener encendido.

## 2. Estructura del repositorio

```
index.html              portada (se genera desde la maqueta elegida con maquetas/hacer_produccion.py)
anterior.html           portada previa, para volver atrás
app/estela.css          sistema visual (ver DESIGN.md)
app/estela.js           vistas: portada, catálogo, ficha, chollos, guardados, filtros, tema
app/olfato.js           bloque propio del producto (en relojes: ficha técnica)
maquetas/core.js        datos y cálculos: carga, agrupar tamaños, mejor precio, bajadas, series, gráficas
maquetas/v2/*.html      maquetas para comparar diseños antes de pasarlos a producción
data/perfumes.json      catálogo + URLs por tienda + precios + historial + fotos   (relojes: relojes.json)
data/estado.json        resumen de la última pasada (por tienda: ok, bloqueada, sin precio, dudoso)
data/chollos.json       chollos de Chollometro
data/notas.json         datos enriquecidos, cargados una sola vez (relojes: ficha técnica)
data/debug.json         una muestra por tienda y pasada, para ajustar el lector
scraper/radar.py        lector de precios (pasada)
scraper/notas.py        lector de datos enriquecidos (una vez)
scraper/test_radar.py   pruebas del lector (se ejecutan antes de cada pasada), incluidas las fichas reales de scraper/fixtures/
scraper/fixtures.py     guarda una ficha real por tienda con su precio (regresión: el lector debe seguir sacando ese precio)
scraper/avisos.py       avisos de precio objetivo: comenta en la incidencia de GitHub (email) y, si hay secretos, Telegram
scraper/test_avisos.py  pruebas de los avisos
scraper/informe.py      informe semanal como incidencia de GitHub
scraper/paginas.py      genera p/<id>.html (una página por producto para compartir)
p/<id>.html             páginas para compartir (Open Graph + redirección a la ficha)
manifest.webmanifest    app instalable; sw.js: service worker (red primero, copia sin conexión)
scraper/diagnostico.py  prueba de acceso a tiendas nuevas
.github/workflows/radar.yml       pasada cada 30 min (input "perfumes": 70 normal, 250 todos)
.github/workflows/notas.yml       datos enriquecidos (modo probe|notas|fichas, limite, rehacer)
.github/workflows/informe.yml     informe semanal (lunes 7:41), abre una incidencia
.github/workflows/diagnostico.yml prueba manual de tiendas
```

## 3. Modelo de datos (un elemento por producto y tamaño)

```json
{
  "id": "dior-sauvage-edp-100", "brand": "Dior", "name": "Sauvage", "conc": "EDP", "ml": 100,
  "tier": "Diseñador",
  "urls":   { "douglas": "https://…", "idealo": "https://…", "sabina": "https://…" },
  "prices": { "sabina": {"p": 89.95, "d": "2026-11-16", "auto": true, "gh": true, "stock": false, "via": "idealo"} },
  "history": [ {"d": "2026-11-16", "s": "sabina", "p": 89.95} ],
  "images": { "lookfantastic": "https://…" },
  "buscado": { "douglas": "2026-11-16" },
  "descartadas": [ "https://url-de-producto-equivocado" ],
  "deals": [], "target": null, "checked": "2026-11-16T13:03:53+01:00"
}
```

- La ficha descriptiva (familia, notas, estaciones, duración) vive en `maquetas/core.js` (`PROFILES`), indexada por el `id` sin tamaño.
- Los tamaños del mismo producto se agrupan por `brand|name|conc`.
- **Relojes**:
  - El producto se identifica por la **referencia del fabricante** (`ref`: "SRPD55K1", "GA-2100-1A1ER"). Es mucho más fiable que el nombre para emparejar tiendas.
  - Las variantes son la correa o brazalete y el color de esfera, en lugar de los ml.
  - Los campos `conc` y `ml` se sustituyen por `ref`, `caja_mm` y `correa`.

## 4. El lector de precios (`scraper/radar.py`), lo que ya funciona

1. **Sesión**:
   - `curl_cffi` con `impersonate="chrome"`, para parecer un navegador real.
   - Tiendas que solo dejan entrar a móviles (Sephora): `safari_ios`.
   - Pausa aleatoria de 0,8 a 1,8 s entre peticiones.
2. **Extracción del precio**, por orden:
   1. JSON-LD (`Product` / `Offer`, eligiendo la variante del tamaño o, mejor, el código de la URL);
   2. Shopify (`"variants"` con el tamaño en `title` y el precio en céntimos) y Magento;
   3. precio por 100 ml;
   4. variantes hijas;
   5. específico de la tienda (Sephora `pricePerUnit`);
   6. ventana de texto alrededor de "€" (el último recurso, marcado `texto`).
3. **Idealo** como puerta trasera de tiendas que bloquean (Notino, Primor, Druni, Arenal, Julia):
   - se leen los enlaces `/relocator/relocate?...price=X&sid=SHOPID` de la lista de ofertas;
   - el número de tienda se traduce con `IDEALO_SHOPS`;
   - el precio se guarda con `via:"idealo"`.
4. **Control de calidad**, que es lo más importante:
   - `plausible(p, ref)`: se rechaza un precio que se aleje mucho del de referencia del producto. Las tiendas a precio completo (Sephora, Douglas) tienen margen hasta 1,8×.
   - `clean_outliers`: limpia del historial los precios absurdos; por arriba, y **por abajo** cuando un precio queda por debajo de la mitad de la mediana de al menos 3 tiendas (casi siempre es otro producto): se quita y su ficha pasa a `descartadas`.
   - En `best_link`, un enlace que dice otro tamaño en la dirección (`-30-ml`) se descarta: algunas tiendas (El Corte Inglés) tienen una ficha por tamaño.
   - `moved_to_listing`: si la ficha redirige a un listado (categoría, `/collections/…` de Shopify) se retira; así se detectó el cambio de Avenida a Shopify.
   - `BUNDLE_RE`: descarta estuches, sets, testers, muestras y packs.
   - `best_link` (al descubrir URLs nuevas):
     - exige marca y nombre;
     - rechaza versiones parecidas (Intense, Elixir, Absolu…) si el producto no lo es;
     - comprueba la concentración;
     - respeta la lista `descartadas` de cada producto.
5. **Descubrimiento**: si una tienda no tiene URL, la busca en su buscador (`SEARCH`), con un tope por pasada (`RADAR_DISCOVER`).
6. **Fotos**: guarda la dirección de la foto (`og:image` o JSON-LD), nunca la copia. Filtra marcadores vacíos (`NO_PHOTO`).
7. **Lotes**: cada pasada revisa los 70 productos que llevan más tiempo sin revisar, así que la lista completa se recorre cada ~3 h.
8. **Chollometro**: lee la categoría y empareja los chollos con productos del catálogo.
9. **Después de guardar**: `paginas.py` regenera las páginas para compartir y `avisos.py` revisa las incidencias "Aviso: …" (cuerpo con `id:` y `precio:`) y comenta si el mejor precio baja del objetivo. Solo vuelve a avisar si baja más que la vez anterior (marca `<!-- aviso:X -->` en el comentario). Necesita `issues: write`. Telegram opcional con los secretos `TELEGRAM_TOKEN` y `TELEGRAM_CHAT`.
10. **Commit** en el workflow: `git add data/ && git commit && git pull --rebase --autostash && git push`, con `concurrency: radar` para no pisarse.

**Relojes**:
- El JSON-LD suele traer `gtin13` y `mpn`; empareja por la referencia (`mpn` o "Ref.") y no por el nombre.
- `BUNDLE_RE` cambia a: "reacondicionado", "segunda mano", "usado", "outlet", "correa de repuesto", "caja vacía".
- `FLANKERS` cambia a las variantes de color de esfera y de brazalete.
- La comprobación de precio absurdo es aún más importante: los relojes de segunda mano y las réplicas distorsionan mucho.

## 5. Datos enriquecidos, una sola vez (`scraper/notas.py`)

- Fuente principal: **Parfumo**, que deja leer desde GitHub. Fragrantica bloquea con Cloudflare.
  - El buscador `s_perfumes_x.php?filter=` empareja marca, nombre y concentración.
  - De la ficha se sacan las notas con su peso y los acordes.
- Plan B: la pirámide escrita en las fichas de las tiendas (expresiones para "Notas de salida: … Corazón: … Fondo: …" y para la prosa de Paco). Se elige la versión **más completa**.
- Si el buscador no empareja, se fija la URL a mano (`PARFUMO_URL`).
- Nada se inventa: la web dice de dónde sale cada dato, con su enlace.
- **Relojes**: la fuente equivalente para la ficha técnica sería una base de datos de referencias. Hay que probar el acceso con el modo `probe` antes de escribir el lector, y como plan B usar la ficha técnica de las tiendas.

## 6. La web (`app/`, `maquetas/core.js`)

- Todo en JavaScript sin frameworks.
- `RP.load(dir)` carga los JSON. `groups()` agrupa tamaños. `best()` da el mejor precio con ≤14 días. `drop()` da la bajada frente a la media de 30 días. `spread()` da el ahorro entre tiendas. `series()` da el historial diario. `lineChart()` dibuja la gráfica.
- `E.start({home, catalog})` monta la barra, el enrutado por `#hash` (`#catalogo`, `#p/<clave>`, `#chollos`, `#guardados`), los filtros, el tema y el pie.
- `E.pre` sirve para cargar datos extra a la vez (notas). `E.DATA` indica dónde está `data/`.
- **Guardados** y **precio objetivo** se guardan en `localStorage` (`rp-favs` y los objetivos de `RP`). El aviso por email no necesita servidor: el enlace abre una incidencia de GitHub ya rellena, y GitHub manda el email cuando el bot comenta en ella.
- `E.min30` / `E.atMin` (mínimo de 30 días), tamaños con precio por 100 ml, `E.simOlf` ("Huelen parecido": coseno entre acordes y notas) y la búsqueda por notas (`it.nx`, que rellena `olfato.js`).
- **Producción**:
  - `python3 maquetas/hacer_produccion.py` copia `app/`, convierte la maqueta elegida en `index.html` y añade `?v=<fecha>` a los archivos para que el navegador no use versiones viejas;
  - `maquetas/core.js` se carga con `?v=<hora>`.
- **Fotos al tamaño justo** (`E.sized`): Lookfantastic (`width=`), Shopify (`_NxN`) y Demandware (`?sw=`). 480 px en tarjetas y 1000 px en la ficha.

## 7. Lecciones aprendidas (no repetirlas)

- **Lookfantastic** pone el mismo nombre a todos los tamaños: hay que elegir la variante por el **código del producto en la URL**, no "la más barata en stock".
- Las **URLs de producto equivocado** (Intense en vez de normal, EDT en vez de EDP) son el error más frecuente. Por eso existen `best_link` con comprobación de concentración y la lista `descartadas`.
- La **gráfica del mercado** salía con caídas falsas los días con pocas lecturas: solo cuentan los días con ≥85 % de los productos.
- El navegador se quedaba con **JavaScript viejo**: siempre versión en la URL de cada archivo.
- **Contraste**: los colores de acentos y estaciones se oscurecieron hasta pasar AA; se comprueba con axe en cada cambio.
- La extensión de Chrome **no hace capturas si la ventana está minimizada o tapada**: hay que pedir que esté visible.
- `gh` sin GraphQL en estas sesiones: los workflows se lanzan con `gh api -X POST repos/<owner>/<repo>/actions/workflows/<archivo>/dispatches -f ref=main -f 'inputs[x]=y'`.
- Los artefactos de Actions no se pueden descargar desde la sesión: para inspeccionar HTML de tiendas, imprimir fragmentos en el registro del workflow.
- Las tiendas **cambian de plataforma sin avisar** (Avenida pasó de Magento a Shopify en nov-2026) y el lector se queda en "sin precio" en silencio. El informe semanal lista las tiendas con más fallos que aciertos para verlo a tiempo.
- **Sephora** (Akamai), **Primor**, **Druni** y **Makeup** (AWS WAF) bloquean a los robots; Primor y Druni llegan vía Idealo.
- `gh issue create` usa GraphQL y falla en estas sesiones: las incidencias se crean con `gh api repos/<owner>/<repo>/issues -f title=… -f body=…`.

## 8. Plan para el comparador de relojes

1. **Nombre e identidad**: entrevistar sobre el nombre y elegirlo con maquetas (en Fragans se hicieron 3 identidades y 3 paletas). Partir de DESIGN.md y cambiar los puntos marcados **[cambiar]**.
2. **Catálogo inicial** (`data/relojes.json`): 100–200 referencias populares (Seiko, Casio G-Shock, Citizen, Tissot, Hamilton, Orient, Garmin…) con `ref`, `brand`, `name`, `caja_mm`, `tier` (Asequible, Gama media, Lujo, Smartwatch) y `tipo` (Buceo, Cronógrafo, Vestir, Piloto, GMT, Campo, Digital, Smartwatch).
3. **Tiendas**: comprobar primero el acceso con el diagnóstico (`.github/workflows/diagnostico.yml`). Candidatas que hay que verificar: Idealo (agregador, muy útil), Amazon.es, El Corte Inglés, joyerías y relojerías online españolas y tiendas oficiales de cada marca. Usar solo las que respondan sin bloqueo; el resto, vía Idealo si aparecen allí.
4. **Lector**: copiar `scraper/radar.py` y adaptar `extract`, `BUNDLE_RE`, `FLANKERS`, `best_link` (emparejar por `ref`), `plausible` e `IDEALO_SHOPS`.
5. **Web**: copiar `app/` y `maquetas/core.js`:
   - cambiar `PROFILES` por la ficha técnica;
   - cambiar el bloque olfativo por una **ficha técnica** (movimiento, calibre, diámetro, grosor, hermeticidad, cristal, peso, reserva de marcha);
   - cambiar las familias por **tipos de reloj**, cada uno con su color;
   - cambiar "Por cómo huelen" por "Por estilo".
6. **Comprobación**: Playwright, axe y Chrome, como en DESIGN.md §10.
7. **Publicación**: GitHub Pages desde `main` y Actions con permisos `contents: write`.

## 9. Mensaje para empezar la conversación nueva

> Quiero un comparador y rastreador de precios de relojes en España, igual que mi proyecto Fragans (https://github.com/sombranba-bit/radar-perfumes). Lee `DESIGN.md` y `REPLICAR.md` de ese repositorio y replica la arquitectura (GitHub Pages + Actions + curl_cffi), el diseño y las comprobaciones. Crea un repositorio nuevo. Antes de construir, entrevístame sobre el nombre, las marcas, el presupuesto de los relojes y las tiendas, y hazme maquetas para elegir.
