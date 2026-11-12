# Radar de Perfumes

## Qué es
Comparador y rastreador de precios de perfumes de diseñador, nicho y árabes en perfumerías online de España y Europa, con los chollos de Chollometro. Una pasada automática en GitHub Actions lee los precios cada 30 minutos.

## Para quién
Una persona (Carlos) que quiere comprar perfumes al mejor precio: mira qué ha bajado, compara tiendas y se pone precios objetivo. Lo consulta sobre todo en el móvil y también en el ordenador.

## Lo que la página tiene que hacer
- Decir en segundos qué ha bajado hoy y dónde está más barato cada perfume.
- Comparar el precio de un perfume en todas las tiendas, por tamaño.
- Filtrar por hombre, mujer o unisex, tipo (diseñador, nicho, árabe), temporada y marca.
- Mostrar la evolución del mejor precio y avisar cuando baja de un objetivo.
- Ser honesta con los datos: indicar la antigüedad de cada precio y las tiendas agotadas.

## Restricciones
- Página estática en GitHub Pages; datos en `data/*.json` generados por `scraper/radar.py`.
- Sin emojis, sin mayúsculas espaciadas; botones de 44 px en el móvil.
