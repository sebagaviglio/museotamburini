# Museo Tamburini · Etapa 1 (boceto v6)

## Imágenes incorporadas (assets/img/)
| Archivo | Uso en la web |
|---|---|
| tamburini/fachada-tamburini-noche.jpg | 02 Descubrí Tamburini · imagen para redes (og) · Noche de los Museos |
| innovacion/innovacion.jpg | 03 Arte, tecnología y nuevas narrativas · muestra arte contemporáneo |
| infancias/espacio-infancias.jpg | 04 Infancias · taller de infancias |
| salas-recreacion/sala-tomas-garzon.jpg | 05 Explorá · Sala Tomás Garzón |
| boveda/tesoro-secreto-boveda.jpg | 05 Explorá · Descubrí la bóveda |
| numismatica/sala-numismatica-numa.jpg | 05 Explorá · Sala numismática |
| innovacion/centro-interactivo-linea-de-tiempo.jpg | 05 Explorá · Centro interactivo · experiencia inmersiva |
| biblioteca-terzaga/biblioteca-terzaga.jpg | 06 Espacios · Biblioteca Terzaga |
| cultura/cultura.jpg | 06 Espacios · Cultura |

## Sumar o reemplazar imágenes
1. Guardar en `_src/assets/img/<seccion>/` (minúsculas, sin tildes ni espacios, JPG ~1600–2400 px).
2. Referenciar como `assets/img/<seccion>/<archivo>.jpg` en `data/muestras.json`, en CHAPS/ESPACIOS (`build.py`) o en XP (`assets/site.js`).
3. Ejecutar `python _src/build.py` y publicar `dist/`.
