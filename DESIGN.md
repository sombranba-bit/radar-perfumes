# DESIGN.md — Fragans

Sistema visual de **Fragans**, comparador de precios de perfume (https://sombranba-bit.github.io/radar-perfumes/).
Sirve para replicarlo en otro comparador (por ejemplo, relojes): copia la estructura, los componentes y las reglas, y cambia solo lo marcado como **[cambiar]**.

Código de referencia: `app/estela.css` (base), los estilos dentro de `index.html` (marca, paleta y bloque olfativo) y `app/estela.js` / `app/olfato.js` (componentes).

---

## 1. Idea

- Una herramienta de compra, no una revista: **buscar, comparar y decidir**.
- Interfaz tranquila y cálida; el color y la riqueza van en el contenido: fotos de producto, la bajada del día, las familias y los bloques de la ficha.
- Un solo color de marca para acciones y precios destacados; el verde se reserva para ahorro y bajadas.
- Claro y oscuro, siguiendo al sistema, con botón para fijar uno u otro.
- Pensado igual para ordenador y móvil: en móvil hay barra inferior, la hoja de filtros sale desde abajo y el precio queda siempre visible.

## 2. Marca

| Elemento | Valor |
|---|---|
| Nombre | Fragans **[cambiar]** |
| Lema bajo el nombre | "Comparador de precios de perfume" **[cambiar]** |
| Logo | Lupa con una gota dentro (SVG 28×28, trazo `currentColor` 2 px, gota en `--accent`) **[cambiar el objeto de dentro]** |
| Favicon | Cuadrado redondeado en burdeos con la lupa en blanco |
| Titular de portada | "Encuentra tu perfume *al mejor precio*" (lo destacado en `--accent`) |

## 3. Tipografía

| Rol | Fuente | Uso |
|---|---|---|
| Titulares (`--serif`) | **Fraunces** 500/600 (Google Fonts, opsz 9..144) | h1, títulos de sección, nombre del producto, nombre de la marca |
| Interfaz (`--sans`) | **Geist** 400/500/600 | todo lo demás |
| Números | `font-variant-numeric: tabular-nums` en `body` | precios alineados |

Escala: portada 72 px (móvil 44), título de sección 34 (móvil 28), ficha 56 (móvil 40), cuerpo 15, metadatos 13, mínimo 12.
Mayúscula solo al principio: **nunca etiquetas en MAYÚSCULAS espaciadas** y **nunca emojis**.

## 4. Color (tokens)

Base neutra cálida (`app/estela.css`) + paleta de marca **burdeos**. Hay otras dos paletas guardadas: azul tinta `#2b4a9b` y verde botella `#1d5a43`.

### Claro
```css
--bg:#f7f2f2;          /* fondo, tinte burdeos muy suave */
--surface:#fff;        /* tarjetas y paneles elevados */
--surface-2:#f0e8e8;   /* rellenos, chips, cajas internas */
--plate:color-mix(in srgb,var(--accent) 4%,var(--surface-2)); /* fondo de la foto del producto (fundido) */
--panel:var(--plate);  /* paneles de la ficha y familias: mismo tono que las tarjetas */
--text:#141311; --muted:#69655d; --faint:#8f8a80;
--line:rgba(20,19,17,.09); --line-2:rgba(20,19,17,.16);
--accent:#8a2335; --accent-ink:#fff;     /* [cambiar] color de marca */
--pos:#17663f; --pos-bg:#e2f2e8;          /* ahorro y bajadas */
--neg:#a12a22;                             /* subidas */
```
### Oscuro
```css
--bg:#120c0d; --surface:#1c1516; --surface-2:#2a1e20;
--text:#f1eee8; --muted:#a7a196; --faint:#7f7a71;
--accent:#f3a3b1; --accent-ink:#2c0710;
--pos:#7fd6a3; --pos-bg:#173023; --neg:#f08a7f;
--plate:color-mix(in srgb,var(--accent) 14%,#e9e4dc);  /* la foto sigue sobre fondo claro (fotos con fondo blanco + mix-blend-mode:multiply) */
--panel:color-mix(in srgb,var(--accent) 9%,var(--surface));
```
Tema: `prefers-color-scheme` por defecto; `data-theme="light|dark"` en `<html>` lo fija; se guarda en `localStorage` (`estela-theme`).

### Colores con significado
- **Familias**, un punto o una tarjeta tintada por familia. Floral `#d4849a`, Amaderada `#8b6b4c`, Oriental `#9c4a3c`, Ámbar `#c98a2e`, Aromática `#7f9a6a`, Gourmand `#b0764a`, Cítrica `#d9ac2c`, Acuática `#5b9ab8` **[cambiar por las categorías del nuevo producto]**.
- **Acordes**, al estilo Fragrantica, con un color por acorde (Dulce `#c8323d`, Ámbar `#9a5214`, Aromático `#2f7562`…). El texto va en blanco o en negro según el contraste.
- **Estaciones**: invierno `#8fd3f4`, primavera `#9be37a`, verano `#f28b82`, otoño `#f4b46b`, día `#f6a623`, noche `#8fb6e0`.
- Todo el texto debe pasar **WCAG AA** (4,5:1); se comprueba con axe en cada cambio.

## 5. Forma, espacio y movimiento

- Radios: `--r-xl:24px` (paneles), `--r-lg:18px` (tarjetas y fotos), `--r-md:12px`, `--r-sm:8px`. Las pastillas son redondas del todo (999px).
- Ancho máximo `--w:1360px`; margen lateral de 24 px (16 px en móvil).
- Sombra solo en tarjetas flotantes y en la búsqueda de portada: `0 1px 2px rgba(..,.04), 0 8px 24px rgba(..,.06)`.
- Curva `--ease: cubic-bezier(.22,1,.36,1)`, con transiciones de 150 a 350 ms. La foto se amplía un 4 % al pasar el ratón, solo con `(hover:hover)`. Se respeta `prefers-reduced-motion`.
- Barras de desplazamiento finas (8 px, color `--line-2`); los carruseles no las muestran y llevan flechas en ordenador.

## 6. Estructura de páginas (sin barra lateral)

1. **Barra superior** fija y translúcida (68 px; 58 en móvil): logo y lema · búsqueda centrada (oculta en la portada hasta bajar) · Catálogo, Chollos, Guardados (con contador) · botón de tema.
2. **Portada**, por secciones, como una app:
   - titular grande y búsqueda grande;
   - accesos rápidos (Hombre, Mujer, Nicho, Árabe, Chollos);
   - "Tus guardados" (carrusel, si hay alguno);
   - **La bajada del día** (bloque grande con foto, tintado con el color de su familia);
   - **Bajan hoy** (carrusel);
   - **El mercado hoy** (frase con un índice y gráfica de 30 días);
   - **Por cómo huelen** (cada familia con sus notas típicas en azulejos) **[cambiar por la sección de categorías del nuevo producto]**;
   - **Donde más ahorras** (carrusel);
   - **Nicho al mejor precio** (carrusel);
   - pie.
3. **Catálogo** (`#catalogo`):
   - cabecera con nombre y número de resultados;
   - botón **Filtros**, que abre una hoja con Para, Tipo, Familia, Temporada, Ordenar y Marca (con buscador);
   - selector de orden y chips de filtros activos con "Quitar todo";
   - si hay una familia elegida, una franja de su color con su descripción;
   - rejilla de tarjetas (2 columnas en móvil) con "Mostrar 24 más".
4. **Ficha** (`#p/<clave>`):
   - en ordenador, dos columnas: foto fija con miniaturas a la izquierda y datos a la derecha;
   - datos: marca y tipo, nombre, concentración, tamaños (cada chip con su precio por 100 ml y "el mejor" en el más barato por ml);
   - **caja de compra**: precio grande, "frente a su media", tienda, precio por 100 ml, veredicto frente al mínimo de 30 días ("Es el precio más bajo de los últimos 30 días" en verde, o "X € por encima del mínimo"), "Ver en <tienda>", Guardar, **Compartir** (menú nativo del móvil; en ordenador copia el enlace) y mínimo, media y máximo de 30 días;
   - **Precio en cada tienda** (tabla; los precios de hace más de un mes, plegados);
   - gráfica diaria del mejor precio;
   - **bloque olfativo** (ver 7.4) **[cambiar]**;
   - **Avísame si baja**: precio objetivo guardado en el navegador y, debajo, el enlace "Avisarme por email cuando baje de X €" (abre una incidencia de GitHub ya rellena);
   - chollos publicados, **Huelen parecido** (por acordes y notas, de cualquier precio) y "Parecidos de precio";
   - en móvil, barra fija abajo con precio y "Ver oferta".
5. **Chollos** (pestañas "De tu lista" y "Todos") y **Guardados**.
6. **Móvil**: barra inferior con Inicio, Catálogo, Chollos y Guardados; búsqueda dentro de la página; `env(safe-area-inset-*)`.
7. **App instalable**: `manifest.webmanifest` (nombre corto "Fragans", color `#8a2335`), iconos en `app/icons/` (192, 512, maskable y apple-touch, la lupa con la gota sobre burdeos) y `sw.js` con red primero y la última copia si no hay conexión.
8. **Páginas para compartir** (`p/<id>.html`): una por producto, solo con título, precio, tiendas y foto para la vista previa (Open Graph) y una redirección a `#p/<clave>`.
9. **Búsqueda**: encuentra marca, nombre, familia y también las notas y acordes reales ("vainilla tabaco" encuentra los que llevan las dos).

## 7. Componentes

### 7.1 Tarjeta de producto
- Foto cuadrada sobre `--plate`, recortada al 78 % y con `mix-blend-mode:multiply` para que el fondo blanco de la foto desaparezca.
- Insignias arriba a la izquierda: bajada "−21 %" en verde, "Chollo" o "Mínimo de 30 días" (con al menos 7 días de lecturas).
- Corazón arriba a la derecha si está guardado.
- Debajo:
  - punto de familia · marca · tamaño;
  - nombre;
  - **precio** y la pastilla verde "−9 € entre tiendas";
  - "en <tienda> · N tiendas".
- Si no hay foto, se dibuja un frasco SVG.

### 7.2 Fila (listas de chollos y movimientos)
Foto de 88 px · nombre y metadatos · minigráfica de 30 días (verde si baja, roja si sube) · precio a la derecha.

### 7.3 Pastillas y chips
- Chip de 38 px con borde `--line-2`; seleccionado, se rellena de `--accent`.
- Pastilla de ahorro: fondo `--pos` al 14 % y texto `--pos`.

### 7.4 Bloque olfativo "Calco" (copia el patrón de Fragrantica)
- **Acordes principales**: barras de color que van menguando, con el nombre centrado dentro.
- **Pirámide del perfume**: separadores centrados ("Notas de salida", "Corazón", "Fondo", o "Notas" si la fuente no separa niveles).
  - Cada nota es un **azulejo**: cuadrado redondeado con degradado del color del ingrediente y un trazo SVG de su tipo (cítrico, flor, madera, especia, resina…).
  - El tamaño del azulejo depende del peso de la nota.
  - Al tocar una nota se ven los perfumes que la llevan.
- **Cuándo usarlo**: 6 iconos de trazo (invierno, primavera, verano, otoño, día, noche), cada uno con una barra de su color.
- Debajo, la fuente con enlace ("Pirámide y acordes según Parfumo").
- Paneles con fondo `--panel`, el mismo tono que las tarjetas.

**[cambiar]** Para relojes, el equivalente sería una **ficha técnica**: barras de "carácter" (deportivo, vestir, buceo, herramienta…), calibre y movimiento como azulejos, y pastillas de diámetro, grosor, hermeticidad, cristal y peso.

### 7.5 Gráficas
- SVG propio de línea, de 2 px y en `--accent`, sobre una rejilla tenue con 3 etiquetas.
- Nunca dos ejes.
- Minigráficas: verde si baja, rojo si sube.

## 8. Reglas de redacción

- Español, frases cortas y sin exclamaciones.
- Siempre con el término de comparación: "−18 % frente a su media", "−9 € entre tiendas".
- Botones con la acción: "Ver en Douglas", "Ver oferta", "Guardar", "Quitar todo".
- Sin cifras inventadas: si un dato no existe, no se muestra.
- La fuente de cada dato externo, citada con su enlace.

## 9. Lo que no se hace

- Barra lateral genérica de filtros (se sustituyó por la hoja de filtros).
- Etiquetas en MAYÚSCULAS espaciadas, emojis, degradados de color sobre superficies, brillos, texto con degradado.
- Copiar imágenes de otras webs: las fotos se enlazan desde la tienda y se piden a un tamaño razonable (≤1000 px en la ficha, 480 en tarjetas).
- Más de un color de acento en la interfaz.

## 10. Comprobación de cada cambio

- Playwright a 1440 px y en iPhone 13, en claro y en oscuro: sin errores en consola y sin desbordar el ancho.
- axe (WCAG 2 A/AA y buenas prácticas) en todas las vistas: portada, catálogo, ficha, chollos, guardados y hoja de filtros.
- Revisión en Chrome con la extensión, sobre la web publicada, con fotos y fuentes reales.
