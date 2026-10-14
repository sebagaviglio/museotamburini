#!/usr/bin/env python3
"""Museo Tamburini · generador estático v5 (Etapa 1: Edificio Tamburini).
python build.py -> dist/ (sitio publicable) + preview.html (vista previa en un archivo)
Imágenes: assets/img/<seccion>/<nombre>.jpg  ·  en datos se referencian como 'assets/img/...'"""
import json, shutil, base64, datetime, html
from pathlib import Path
B=Path(__file__).parent; DIST=B/'dist'
D=json.loads((B/'data/muestras.json').read_text(encoding='utf-8')); C=D['config']; M=D['muestras']
CSS=(B/'assets/site.css').read_text(encoding='utf-8'); JS=(B/'assets/site.js').read_text(encoding='utf-8')
HOY=datetime.date.today(); e=lambda s:html.escape(str(s),quote=True)
MES=['ene','feb','mar','abr','may','jun','jul','ago','sep','oct','nov','dic']
def fd(s): d=datetime.date.fromisoformat(s); return f"{d.day} {MES[d.month-1]} {d.year}"
def rango(m): return fd(m['desde']) if m['desde']==m['hasta'] else f"{fd(m['desde'])} — {fd(m['hasta'])}"
def estado(m):
    a,b=datetime.date.fromisoformat(m['desde']),datetime.date.fromisoformat(m['hasta']); return 'prox' if HOY<a else 'fin' if HOY>b else 'act'
EST={'act':'En cartel','prox':'Próximamente','fin':'Finalizada'}
URL=lambda s:f"{C['base_url']}/muestras/{s}/"
def absimg(u): return C['base_url']+'/assets/vitreaux.jpg' if u=='__VITREAUX__' else (C['base_url']+'/'+u if u.startswith('assets/') else u)
def relimg(u,root): return root+'assets/vitreaux.jpg' if u=='__VITREAUX__' else (root+u if u.startswith('assets/') else u)
PREVIEW=False
def bg(u,root):
    """atributo de fondo: en dist ruta relativa; en preview lo resuelve el JS (imagen embebida una sola vez)"""
    return f'data-bg="{u}"' if PREVIEW else f'style="background-image:url(\'{relimg(u,root)}\')"'

CHAPS=[
 dict(id='descubri',n='02',lbl='Patrimonio y arquitectura',t='Descubrí Tamburini',sub='Patrimonio y arquitectura de una casa matriz pensada en 1889 para transmitir progreso.',
      tags=[('Hall de Caja','#explora'),('Historia','#historia'),('Colecciones','#explora'),('Recorrido patrimonial','#explora')],
      img='assets/img/tamburini/fachada-tamburini-noche.jpg',video=''),
 dict(id='arte',n='03',lbl='Muestras y experiencias',t='Arte, tecnología y nuevas narrativas',sub='Exposiciones de arte contemporáneo, instalaciones, experiencias inmersivas y audiovisuales.',
      tags=[('En cartel','#en-cartel'),('Agenda','#museo-hoy'),('Premio de Pintura','https://www.bancor.com.ar/institucional/museo-tamburini/premio-pintura')],
      img='assets/img/innovacion/innovacion.jpg',video=''),
 dict(id='infancias',n='04',lbl='Para chicos y chicas',t='Infancias',sub='Arte, juego, exploración, creatividad y aprendizaje.',
      tags=[('Diseñá tu vitreaux','#juego'),('Trivia','#trivia'),('Talleres','#museo-hoy')],
      img='assets/img/infancias/espacio-infancias.jpg',video=''),
]
ESPACIOS=[('Biblioteca Terzaga','Lectura y consulta','assets/img/biblioteca-terzaga/biblioteca-terzaga.jpg'),
          ('Cultura','Encuentros, charlas, talleres, programas y comunidad','assets/img/cultura/cultura.jpg')]
FONTS='<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Public+Sans:ital,wght@0,100;0,200;0,300;0,400;0,500;1,200;1,300&display=swap" rel="stylesheet">'
def head(title,desc,canon,og,jsonld,root,css_inline=None,extra=''):
    css=f'<style>{css_inline}</style>' if css_inline else f'<link rel="stylesheet" href="{root}assets/site.css">'
    ld=''.join(f'<script type="application/ld+json">{json.dumps(j,ensure_ascii=False)}</script>' for j in jsonld)
    return f'''<!DOCTYPE html><html lang="es-AR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title><meta name="description" content="{e(desc)}"><link rel="canonical" href="{canon}"><meta name="robots" content="index,follow,max-image-preview:large">
<meta property="og:type" content="website"><meta property="og:locale" content="es_AR"><meta property="og:site_name" content="{e(C['museo'])}"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{canon}"><meta property="og:image" content="{og}">
<meta name="twitter:card" content="summary_large_image"><meta name="theme-color" content="#000000">{extra}{FONTS}{css}{ld}</head><body>'''
def header(L):
    return f'''<div id="prog"></div><header class="hdr"><a class="brand" href="{L['home']}"><span class="logo">[ LOGO ]</span><span>Museo Tamburini</span></a>
<nav><a href="{L['hs']}#descubri">Descubrí</a><a href="{L['hs']}#arte">Arte</a><a href="{L['hs']}#infancias">Infancias</a><a href="{L['hs']}#explora">Explorá</a><a href="{L['hs']}#museo-hoy">Agenda</a>
<a class="cta ln" href="{C['bezzapass']}" target="_blank" rel="noopener"><span class="dot"></span>Reservas</a></nav></header>'''
def footer(L):
    return f'''<footer><div><div class="big">Tamburini,<br><em style="color:var(--mute)">un edificio por descubrir.</em></div><p class="lbl" style="margin-top:30px">Etapa 1 · Edificio Tamburini</p></div>
<div><span class="lbl">Visitanos</span><a href="https://maps.google.com/?q={C['lat']},{C['lng']}" target="_blank" rel="noopener">{e(C['direccion'])}, {e(C['ciudad'])}</a><a>{e(C['horario'])}</a><a href="tel:{C['telefono'].replace(' ','')}">{e(C['telefono'])}</a></div>
<div><span class="lbl">Explorar</span><a href="{L['list']}">Muestras y actividades</a><a href="{C['bezzapass']}" target="_blank" rel="noopener">Reservas · Bezzapass</a></div></footer>
<div class="toast" id="toast"></div><div class="note">Boceto v6 · imágenes de referencia del proyecto</div>'''
def site_js(page,root,vit,preview=False,inline=False,imgs=None):
    s=json.dumps({'page':page,'root':root,'vit':vit,'preview':preview,'imgs':imgs or {},'data':D},ensure_ascii=False)
    return f'<script>window.SITE={s}</script>'+(f'<script>{JS}</script>' if inline else f'<script src="{root}assets/site.js"></script>')+'</body></html>'
ORG={"@type":"Organization","name":"Banco de la Provincia de Córdoba S.A.","url":"https://www.bancor.com.ar/"}
PLACE={"@type":"Museum","name":C['museo'],"url":C['base_url']+'/',"telephone":C['telefono'],"address":{"@type":"PostalAddress","streetAddress":C['direccion'],"addressLocality":C['ciudad'],"postalCode":C['cp'],"addressRegion":"Córdoba","addressCountry":C['pais']},"geo":{"@type":"GeoCoordinates","latitude":C['lat'],"longitude":C['lng']}}
def ld_event(m):
    j={"@context":"https://schema.org","@type":"ExhibitionEvent" if m['tipo']=='Muestra' else "Event","name":m['titulo'],"description":m['bajada'],"url":URL(m['slug']),"startDate":m['desde'],"endDate":m['hasta'],
       "eventStatus":"https://schema.org/EventScheduled","eventAttendanceMode":"https://schema.org/OfflineEventAttendanceMode","image":[absimg(m['img'])],"location":PLACE,"organizer":ORG,"inLanguage":"es-AR"}
    if m.get('keywords'): j['keywords']=', '.join(m['keywords'])
    if m.get('gratis'): j['isAccessibleForFree']=True
    if estado(m)!='fin': j['offers']={"@type":"Offer","url":(m.get('cta') or {}).get('url',C['bezzapass']),"availability":"https://schema.org/InStock"}
    return j
def ld_crumb(items): return {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":i+1,"name":n,"item":u} for i,(n,u) in enumerate(items)]}

def chap(c,L,root):
    media=(f'<video src="{relimg(c["video"],root)}" muted loop playsinline preload="none"></video>' if c['video'] else f'<div class="bg" {bg(c["img"],root)}></div>')
    tags=''.join(f'<a href="{u if u.startswith("http") else L["hs"]+u}"{" target=_blank rel=noopener" if u.startswith("http") else ""}>{t}</a>' for t,u in c['tags'])
    return f'''<section class="chap" id="{c['id']}"><div class="media">{media}</div><div class="grain"></div><div class="sh"></div><div class="num">{c['n']}</div>
<div class="top"><span class="lbl"><b>{c['n']}</b> · {c['lbl']}</span><span class="lbl">{'Video' if c['video'] else 'Imagen'} full screen</span></div>
<div class="ct"><h2 data-split>{c['t']}</h2><p class="sub">{c['sub']}</p><div class="tags">{tags}</div></div></section>'''

def home_main(L,root=''):
    c1,c2,c3=CHAPS
    esp=''.join(f'<div class="space reveal"><div class="im" {bg(u,root)}></div><div class="tx"><span class="lbl">Espacios del museo</span><h4>{t}</h4><p>{d}</p></div></div>' for t,d,u in ESPACIOS)
    return f'''<section id="hero" aria-label="Apertura audiovisual"><div class="h-layer h-base"></div><div class="h-layer h-light"></div><div class="h-tiles"></div><div class="h-fade"></div>
<div class="h-top lbl"><span><b>01</b> · Apertura · Córdoba, desde 1889</span><span data-open></span></div>
<nav class="h-chap" aria-label="Capítulos"><a href="#descubri">02 Descubrí Tamburini</a><a href="#arte">03 Arte y nuevas narrativas</a><a href="#infancias">04 Infancias</a><a href="#explora">05 Explorá</a><a href="#museo-hoy">06 El museo hoy</a></nav>
<div class="h-txt"><h1><span class="l"><span>Tamburini,</span></span><span class="l"><span style="animation-delay:.15s">un edificio</span></span><span class="l"><span style="animation-delay:.3s"><em>por descubrir.</em></span></span></h1>
<div class="h-side"><span class="lbl">Arquitectura · Historia · Patrimonio</span><p>Arquitectura, historia y patrimonio en una experiencia de exploración. Mové el cursor: la luz atraviesa el vitreaux.</p>
<div style="display:flex;gap:10px;flex-wrap:wrap"><a class="btn acc" href="#descubri">Explorar <span class="ar">↓</span></a><a class="btn" href="{C['bezzapass']}" target="_blank" rel="noopener">Reservar ↗</a></div></div></div><div class="scroll-ln"></div></section>
<div class="marq"><div class="tr" id="mq"></div></div>
{chap(c1,L,root)}
<div class="branch" id="historia"><div class="s-head"><span class="lbl reveal">02 · Historia</span><h2 class="reveal" style="font-size:clamp(34px,4.6vw,72px)">150 años en un <em>solo edificio</em></h2></div>
<div class="reveal"><div class="tl-years" id="tlyears"></div><div class="tl-card" id="tlcard"></div></div>
<div class="stats"><div class="stat reveal"><div class="v" data-n="1873">0</div><div class="l">Inicio de actividades del Banco Provincial de Córdoba</div></div>
<div class="stat reveal"><div class="v"><span data-n="2">0</span> años</div><div class="l">Tiempo de construcción de la casa matriz</div></div>
<div class="stat reveal"><div class="v" data-n="130000">0</div><div class="l">Cuentas corrientes en 1968</div></div><div class="stat reveal"><div class="v" data-n="155000">0</div><div class="l">Cajas de ahorro en 1968</div></div></div></div>
{chap(c2,L,root)}
<div class="branch" id="en-cartel"><div class="s-head"><span class="lbl reveal">03 · En cartel</span><div><h2 class="reveal" style="font-size:clamp(34px,4.6vw,72px)">Muestras y <em>experiencias</em></h2>
<p class="lead reveal">Cada propuesta tiene su propia página para compartir. <a class="ln" style="color:var(--fg)" href="{L['list']}">Ver todas →</a></p></div></div>
<div class="stage" id="stage" data-eje="arte"><div class="bars"></div><div class="ctrl"><button id="sPrev">Anterior</button><button id="sPlay">Pausa</button><button id="sNext">Siguiente</button></div></div><div class="idx" id="idx"></div></div>
{chap(c3,L,root)}
<div class="branch" id="juego"><div class="kids"><div><span class="lbl reveal">04 · Jugá</span><h2 class="reveal" style="margin-top:30px;font-size:clamp(34px,4.6vw,72px)">Diseñá tu <em>vitreaux</em></h2>
<p class="lead reveal">Con la paleta del vitreaux original: elegí un color, pintá los paneles y compartí tu obra.</p><div class="pal" id="pal"></div>
<div style="display:flex;gap:10px;flex-wrap:wrap"><button class="btn acc" id="rnd">Sorprendeme</button><button class="btn" id="clr">Limpiar</button><button class="btn" id="shr">Compartir</button></div></div><div class="vgrid reveal" id="vgrid"></div></div>
<div class="qbox reveal" id="trivia"><div id="qbox"></div></div></div>
<section class="s" id="explora"><div class="s-head"><span class="lbl reveal">05 · Explorá de otra manera</span><div><h2 class="reveal">Recorridos y experiencias <em>interactivas</em></h2></div></div>
<div class="xp"><div><div class="xp-list reveal" id="xpList"></div><p class="xp-note">Recorridos digitales, imágenes explorables, narrativas audiovisuales e interactividad. Contenidos y accesos sujetos a desarrollo y validación.</p></div><div class="xp-view reveal" id="xpView"></div></div></section>
<section class="s" id="museo-hoy"><div class="s-head"><span class="lbl reveal">06 · El museo hoy</span><div><h2 class="reveal">Muestras, actividades y <em>visitas</em></h2><p class="lead reveal">Agenda actualizable y accesos directos para planificar tu visita.</p></div></div>
<div class="tabs reveal" id="tabs"></div><div id="agenda"></div><div id="evthumb"></div>
<div class="spaces">{esp}</div>
<div class="res-strip reveal"><div><span class="lbl">Dirección</span><div class="big">{e(C['direccion'])}<br>{e(C['ciudad'])}</div></div>
<div><span class="lbl">Horario</span><div class="big">{e(C['horario'])}</div><p class="lbl" style="margin-top:16px" data-open></p></div>
<a class="bzl" href="{C['bezzapass']}" target="_blank" rel="noopener"><span class="lbl">Reservas · Visitas guiadas</span><div class="big">Reservá en Bezzapass ↗</div></a></div>
<div class="map reveal"><iframe loading="lazy" title="Mapa" src="https://www.openstreetmap.org/export/embed.html?bbox=-64.1864%2C-31.4200%2C-64.1784%2C-31.4155&amp;layer=mapnik&amp;marker={C['lat']}%2C{C['lng']}"></iframe></div></section>
<div class="exo" id="exo"></div>'''

def card(m,h,root): return f'''<a class="ai" href="{h}"><div class="im" {bg(m['img'],root)}></div><div class="meta lbl"><span>{m['desde'][:4]}</span><span>{e(m['tipo'])}</span></div><h4>{e(m['titulo'])}</h4><span class="go">{rango(m)} →</span></a>'''
def detail_main(m,L,root):
    words=' '.join(f'<span class="w" style="animation-delay:{.25+i*.08:.2f}s">{e(w)}</span>' for i,w in enumerate(m['titulo'].split()))
    cta=m.get('cta') or {'label':'Reservar en Bezzapass','url':C['bezzapass']}
    rows=[('Tipo',m['tipo']),('Fechas',rango(m))]+([('Horario',m['horario'])] if m.get('horario') else [])+([('Entrada',m['entrada'])] if m.get('entrada') else [])+[('Lugar',f"{C['museo']} · {C['direccion']}, {C['ciudad']}")]
    prog=('<div class="prog"><span class="lbl" style="display:block;padding:0 0 18px">Programación</span>'+''.join(f'<div><span>{e(a)}</span>{e(b)}</div>' for a,b in m['programa'])+'</div>') if m.get('programa') else ''
    gb=lambda g:(f'<button data-k="{g}" {bg(g,root)}></button>' if PREVIEW else f'<button data-src="{relimg(g,root)}" {bg(g,root)}></button>')
    gal=('<div class="lbl" style="padding:0 6vw 30px">Galería</div><div class="gal">'+''.join(gb(g) for g in m['gal'])+'</div>') if m.get('gal') else ''
    rel=[x for x in M if x['slug']!=m['slug']][:3]
    return f'''<main data-slug="{m['slug']}"><section class="d-hero"><div class="bg" {bg(m['img'],root)}></div><div class="sh"></div>
<div class="top"><nav class="crumb"><a href="{L['home']}">Museo Tamburini</a><span>/</span><a href="{L['list']}">Muestras y actividades</a><span>/</span><span>{e(m['titulo'])}</span></nav></div>
<div class="ct"><div class="lbl"><span class="st-badge">{EST[estado(m)]}</span> · {e(m['tipo'])} · {rango(m)}{'<span class="ph">Datos a confirmar</span>' if m.get('ph') else ''}</div><h1>{words}</h1></div></section>
<section class="d-body"><aside class="sticky"><div class="dl">{''.join(f'<div><span class="k">{k}</span><span>{e(v)}</span></div>' for k,v in rows)}</div>
<div style="display:flex;gap:12px;flex-wrap:wrap;margin-top:36px"><a data-if-active class="btn acc" href="{cta['url']}" target="_blank" rel="noopener">{e(cta['label'])} ↗</a><a data-if-ended class="btn" href="{L['list']}">Ver otras propuestas →</a></div><div class="share"></div></aside>
<article class="d-txt"><p class="bajada">{e(m['bajada'])}</p>{''.join(f'<p>{e(p)}</p>' for p in m['cuerpo'])}{prog}</article></section>{gal}
<section class="related"><div class="s-head"><span class="lbl">Más en el Tamburini</span><h2 style="font-size:clamp(34px,4vw,60px)">Otras <em>propuestas</em></h2></div><div class="agrid">{''.join(card(x,L['m'](x['slug']),root) for x in rel)}</div></section></main>'''
def md_page(m):
    t=[f"# {m['titulo']}",'',f"> {m['bajada']}",'',f"- Tipo: {m['tipo']}",f"- Fechas: {rango(m)} ({m['desde']} a {m['hasta']})",f"- Estado: {EST[estado(m)]}"]
    if m.get('horario'): t.append(f"- Horario: {m['horario']}")
    if m.get('entrada'): t.append(f"- Entrada: {m['entrada']}")
    t+=[f"- Lugar: {C['museo']}, {C['direccion']}, {C['ciudad']}, Argentina",f"- Reservas: {(m.get('cta') or {}).get('url',C['bezzapass'])}",f"- URL: {URL(m['slug'])}",'']+m['cuerpo']
    if m.get('programa'): t+=['','## Programación']+[f"- {a}: {b}" for a,b in m['programa']]
    return '\n'.join(t)+'\n'
def list_main(L):
    return f'''<main><section class="s" style="padding-top:180px;border:0"><nav class="crumb reveal"><a href="{L['home']}">Museo Tamburini</a><span>/</span><span>Muestras y actividades</span></nav>
<h1 class="reveal" style="font-size:clamp(56px,10vw,170px);margin:40px 0 0">El museo <em>hoy</em></h1></section>
<section class="s" id="museo-hoy" style="padding-top:40px"><div class="tabs" id="tabs"></div><div id="agenda"></div><div id="evthumb"></div></section>
<section class="s"><div class="s-head" style="margin-bottom:20px"><span class="lbl">Archivo</span><div><h2>Lo que <em>pasó</em></h2><div class="filters" id="fYear"></div></div></div><div class="agrid" id="agrid"></div>
<noscript><ul>{''.join(f'<li><a href="{x["slug"]}/">{e(x["titulo"])}</a></li>' for x in M)}</ul></noscript></section></main>'''

# ---------- DIST ----------
if DIST.exists(): shutil.rmtree(DIST)
shutil.copytree(B/'assets',DIST/'assets'); (DIST/'data').mkdir(); (DIST/'muestras').mkdir()
shutil.copy(B/'data/muestras.json',DIST/'data')
OGH=absimg('assets/img/tamburini/fachada-tamburini-noche.jpg'); act=[m for m in M if estado(m)!='fin']
ld_home={"@context":"https://schema.org",**PLACE,"description":"Tamburini, un edificio por descubrir. Arquitectura, historia y patrimonio en la casa matriz del Banco de Córdoba (1889).","openingHours":"Mo-Fr 09:00-16:00","image":[OGH,absimg('__VITREAUX__')],"parentOrganization":ORG,
 "event":[{"@type":"Event","name":m['titulo'],"url":URL(m['slug']),"startDate":m['desde'],"endDate":m['hasta']} for m in act]}
DESC="Tamburini, un edificio por descubrir. Arquitectura, historia y patrimonio en una experiencia de exploración. Muestras, infancias, recorridos interactivos y reservas."
L0={'home':'./','hs':'','list':'muestras/','m':lambda s:f'muestras/{s}/'}
(DIST/'index.html').write_text(head("Museo Tamburini · Un edificio por descubrir | Córdoba",DESC,C['base_url']+'/',OGH,[ld_home],'')+header(L0)+home_main(L0,'')+footer(L0)+site_js('home','','assets/vitreaux.jpg'),encoding='utf-8')
L1={'home':'../','hs':'../','list':'./','m':lambda s:f'{s}/'}
ld_list={"@context":"https://schema.org","@type":"CollectionPage","name":"Muestras y actividades · Museo Tamburini","url":C['base_url']+'/muestras/',"mainEntity":{"@type":"ItemList","itemListElement":[{"@type":"ListItem","position":i+1,"url":URL(m['slug']),"name":m['titulo']} for i,m in enumerate(M)]}}
(DIST/'muestras/index.html').write_text(head("Muestras y actividades · Museo Tamburini","Agenda de muestras, actividades y visitas guiadas del Museo Tamburini, Córdoba.",C['base_url']+'/muestras/',OGH,[ld_list],'../')+header(L1)+list_main(L1)+footer(L1)+site_js('list','../','../assets/vitreaux.jpg'),encoding='utf-8')
L2={'home':'../../','hs':'../../','list':'../','m':lambda s:f'../{s}/'}
for m in M:
    p=DIST/'muestras'/m['slug']; p.mkdir()
    lds=[ld_event(m),ld_crumb([('Museo Tamburini',C['base_url']+'/'),('Muestras',C['base_url']+'/muestras/'),(m['titulo'],URL(m['slug']))])]
    (p/'index.html').write_text(head(f"{m['titulo']} · Museo Tamburini",f"{m['bajada']} {rango(m)}. {C['museo']}, {C['ciudad']}.",URL(m['slug']),absimg(m['img']),lds,'../../',extra='<link rel="alternate" type="text/markdown" href="index.md">')+header(L2)+detail_main(m,L2,'../../')+'<div class="lbx" id="lbx"><span class="x">Cerrar</span><img alt=""></div>'+footer(L2)+site_js('detail','../../','../../assets/vitreaux.jpg'),encoding='utf-8')
    (p/'index.md').write_text(md_page(m),encoding='utf-8')
urls=[C['base_url']+'/',C['base_url']+'/muestras/']+[URL(m['slug']) for m in M]
(DIST/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'  <url><loc>{u}</loc><lastmod>{HOY}</lastmod></url>\n' for u in urls)+'</urlset>\n',encoding='utf-8')
(DIST/'robots.txt').write_text(f"User-agent: *\nAllow: /\n\nUser-agent: GPTBot\nAllow: /\nUser-agent: ClaudeBot\nAllow: /\nUser-agent: PerplexityBot\nAllow: /\nUser-agent: Google-Extended\nAllow: /\n\nSitemap: {C['base_url']}/sitemap.xml\n",encoding='utf-8')
li=lambda m:f"- [{m['titulo']}]({URL(m['slug'])}index.md): {m['bajada']} ({rango(m)})"
(DIST/'llms.txt').write_text(f"""# {C['museo']}

> Tamburini, un edificio por descubrir. Museo en la histórica casa matriz del Banco de Córdoba (Bancor), {C['direccion']}, {C['ciudad']}, Argentina. Obra del arquitecto italiano Francisco Tamburini, inaugurada el 17 de mayo de 1889, con un vitreaux en el techo del Hall de Caja y yesería de Arturo Nembrini Gonzaga.

Ejes: Descubrí Tamburini (patrimonio y arquitectura) · Arte, tecnología y nuevas narrativas · Infancias · Recorridos interactivos (Hall de Caja, Sala Tomás Garzón, bóveda, sala numismática, centro interactivo) · Biblioteca Terzaga · Cultura.

- Horario: {C['horario']}
- Teléfono: {C['telefono']}
- Reservas: {C['bezzapass']}

## Agenda
{chr(10).join(li(m) for m in act) or '- (sin propuestas activas)'}

## Archivo
{chr(10).join(li(m) for m in M if estado(m)=='fin')}
""",encoding='utf-8')

# ---------- PREVIEW (un archivo; cada imagen embebida una sola vez) ----------
PREVIEW=True
b64=lambda p:'data:image/jpeg;base64,'+base64.b64encode(p.read_bytes()).decode()
vit=b64(B/'assets/vitreaux.jpg')
IM={str(p.relative_to(B)).replace('\\','/'):b64(p) for p in sorted((B/'assets/img').rglob('*.jpg'))}
LP={'home':'#','hs':'','list':'#museo-hoy','m':lambda s:f'#/muestras/{s}/'}
tpls=''.join(f'<template id="tpl-{m["slug"]}">{detail_main(m,LP,"")}</template>' for m in M)
pv=head("Museo Tamburini · Vista previa v6",DESC,C['base_url']+'/',OGH,[ld_home],'',css_inline=CSS.replace('--vit:url(vitreaux.jpg)','--vit:url('+vit+')'))+header(LP)+home_main(LP,'')+'<div id="pv"></div>'+tpls+'<div class="lbx" id="lbx"><span class="x">Cerrar</span><img alt=""></div>'+footer(LP)+site_js('home','',vit,preview=True,inline=True,imgs=IM)
(B/'preview.html').write_text(pv,encoding='utf-8')
print('OK',len(M),'propuestas ·',len(urls),'URLs ·',len(IM),'imágenes · preview',round(len(pv)/1e6,1),'MB')
