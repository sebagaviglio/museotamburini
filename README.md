# Museo Tamburini · Sitio (boceto v3)

## Estructura de URLs
- `/` Home
- `/muestras/` Listado (en cartel + archivo)
- `/muestras/<slug>/` Página propia de cada muestra (+ `index.md` para LLMs)
- `/sitemap.xml`, `/robots.txt`, `/llms.txt`

## Cómo cargar una muestra nueva
1. Agregar un bloque en `data/muestras.json` (slug, tipo, titulo, bajada, cuerpo, desde, hasta, img, gal...).
2. Ejecutar `python _src/build.py` (fuentes en `_src/`) → se regenera `dist/` completo.
3. Publicar `dist/`.

Cuando pasa la fecha `hasta`, la muestra sale del escenario y pasa sola al archivo, conservando su URL.

## Pendientes
- Definir `base_url` final en `data/muestras.json` (hoy: https://www.bancor.com.ar/museo-tamburini).
- Reemplazar `[ LOGO BANCOR ]` por el original del Kit Gráfico e imágenes de stock por fotos reales.
- Confirmar con Bezzapass si permite embeber (iframe) y obtener links directos por evento.
- Para comunicaciones, usar la URL de cada muestra con UTM (ej: `?utm_source=email&utm_campaign=noche-museos`).
