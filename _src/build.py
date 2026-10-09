#!/usr/bin/env python3
"""Genera el sitio estático del Museo Tamburini a partir de data/muestras.json.
Uso: python build.py  ->  dist/ (sitio publicable) + preview.html (vista previa en un solo archivo)
Cada muestra obtiene su URL propia: /muestras/<slug>/  (+ index.md para LLMs)"""
import json, os, shutil, base64, datetime, html
from pathlib import Path
B=Path(__file__).parent; DIST=B/'dist'
D=json.loads((B/'data/muestras.json').read_text(encoding='utf-8')); C=D['config']; M=D['muestras']
CSS=(B/'assets/site.css').read_text(encoding='utf-8'); JS=(B/'assets/site.js').read_text(encoding='utf-8')
HOY=datetime.date.today()
e=lambda s:html.escape(str(s),quote=True)
MES=['ene','feb','mar','abr','may','jun','jul','ago','sep','oct','nov','dic']
def fd(s): d=datetime.date.fromisoformat(s); return f"{d.day} {MES[d.month-1]} {d.year}"
def rango(m): return fd(m['desde']) if m['desde']==m['hasta'] else f"{fd(m['desde'])} — {fd(m['hasta'])}"
def estado(m):
    a,b=datetime.date.fromisoformat(m['desde']),datetime.date.fromisoformat(m['hasta'])
    return 'prox' if HOY<a else 'fin' if HOY>b else 'act'
EST={'act':'En cartel','prox':'Próximamente','fin':'Finalizada'}
URL=lambda slug:f"{C['base_url']}/muestras/{slug}/"
def absimg(u): return C['base_url']+'/assets/vitreaux.jpg' if u=='__VITREAUX__' else u
def relimg(u,root): return root+'assets/vitreaux.jpg' if u=='__VITREAUX__' else u

FONTS='<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Public+Sans:ital,wght@0,100;0,200;0,300;0,400;0,500;1,200;1,300&display=swap" rel="stylesheet">'

def head(title,desc,canon,og,jsonld,root,css_inline=None,extra=''):
    css=f'<style>{css_inline}</style>' if css_inline else f'<link rel="stylesheet" href="{root}assets/site.css">'
    ld=''.join(f'<script type="application/ld+json">{json.dumps(j,ensure_ascii=False)}</script>' for j in jsonld)
    return f'''<!DOCTYPE html><html lang="es-AR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title><meta name="description" content="{e(desc)}"><link rel="canonical" href="{canon}">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta property="og:type" content="website"><meta property="og:locale" content="es_AR"><meta property="og:site_name" content="{e(C['museo'])}">
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{canon}"><meta property="og:image" content="{og}">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{e(title)}"><meta name="twitter:description" content="{e(desc)}"><meta name="twitter:image" content="{og}">
<meta name="theme-color" content="#000000">{extra}{FONTS}{css}{ld}</head><body>'''

def header(L):
    return f'''<div id="prog"></div><header class="hdr"><a class="brand" href="{L['home']}"><span class="logo">[ LOGO BANCOR ]</span><span>Museo Tamburini</span></a>
<nav><a href="{L['list']}">Muestras</a><a href="{L['home_s']}#historia">Historia</a><a href="{L['home_s']}#edificio">Edificio</a><a href="{L['home_s']}#tamburini">Tamburini</a><a href="{L['home_s']}#visita">Visita</a>
<a class="cta ln" href="{C['bezzapass']}" target="_blank" rel="noopener"><span class="dot"></span>Entradas</a></nav></header>'''

def footer(L):
    return f'''<footer><div><div class="big">Museo<br><em style="color:var(--mute);font-style:italic">Tamburini</em></div><p class="lbl" style="margin-top:30px">[ LOGO BANCOR ] · Banco de la Provincia de Córdoba S.A.</p></div>
<div><span class="lbl">Visitanos</span><a href="https://maps.google.com/?q={C['lat']},{C['lng']}" target="_blank" rel="noopener">{e(C['direccion'])}, {e(C['ciudad'])}</a><a>{e(C['horario'])}</a><a href="tel:{C['telefono'].replace(' ','')}">{e(C['telefono'])}</a></div>
<div><span class="lbl">Explorar</span><a href="{L['list']}">Muestras</a><a href="{C['bezzapass']}" target="_blank" rel="noopener">Entradas · Bezzapass</a><a href="https://www.bancor.com.ar/institucional/museo-tamburini/premio-pintura" target="_blank" rel="noopener">Premio de Pintura</a></div></footer>
<div class="toast" id="toast"></div><div class="note">Boceto v3 · logo e imágenes a reemplazar</div>'''

def site_js(page,root,vit,preview=False,inline=False):
    s=json.dumps({'page':page,'root':root,'vit':vit,'preview':preview,'data':D},ensure_ascii=False)
    js=f'<script>{JS}</script>' if inline else f'<script src="{root}assets/site.js"></script>'
    return f'<script>window.SITE={s}</script>{js}</body></html>'

ORG={"@type":"Organization","name":"Banco de la Provincia de Córdoba S.A.","url":"https://www.bancor.com.ar/"}
PLACE={"@type":"Museum","name":C['museo'],"url":C['base_url']+'/',"telephone":C['telefono'],
 "address":{"@type":"PostalAddress","streetAddress":C['direccion'],"addressLocality":C['ciudad'],"postalCode":C['cp'],"addressRegion":"Córdoba","addressCountry":C['pais']},
 "geo":{"@type":"GeoCoordinates","latitude":C['lat'],"longitude":C['lng']}}

def ld_event(m):
    j={"@context":"https://schema.org","@type":"ExhibitionEvent" if m['tipo'] in ('Muestra','Visita guiada') else "Event",
       "name":m['titulo'],"description":m['bajada'],"url":URL(m['slug']),"startDate":m['desde'],"endDate":m['hasta'],
       "eventStatus":"https://schema.org/EventScheduled","eventAttendanceMode":"https://schema.org/OfflineEventAttendanceMode",
       "image":[absimg(m['img'])]+[absimg(g) for g in m.get('gal',[])],"location":PLACE,"organizer":ORG,"inLanguage":"es-AR"}
    if m.get('keywords'): j['keywords']=', '.join(m['keywords'])
    if m.get('gratis'): j['isAccessibleForFree']=True
    if estado(m)!='fin': j['offers']={"@type":"Offer","url":(m.get('cta') or {}).get('url',C['bezzapass']),"availability":"https://schema.org/InStock",**({"price":"0","priceCurrency":"ARS"} if m.get('gratis') else {})}
    return j
def ld_crumb(items): return {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":i+1,"name":n,"item":u} for i,(n,u) in enumerate(items)]}

# ---------- DETALLE ----------
def card(m,href,root):
    return f'''<a class="ai" href="{href}"><div class="im" style="background-image:url('{relimg(m['img'],root)}')"></div><div class="meta lbl"><span>{m['desde'][:4]}</span><span>{e(m['tipo'])}</span></div><h4>{e(m['titulo'])}</h4><span class="go">{rango(m)} &nbsp;→</span></a>'''

def detail_main(m,L,root):
    st=estado(m); words=' '.join(f'<span class="w" style="animation-delay:{.25+i*.08:.2f}s">{e(w)}</span>' for i,w in enumerate(m['titulo'].split()))
    cta=m.get('cta') or {'label':'Reservar en Bezzapass','url':C['bezzapass']}
    rows=[('Tipo',m['tipo']),('Fechas',rango(m))]+([('Horario',m['horario'])] if m.get('horario') else [])+([('Entrada',m['entrada'])] if m.get('entrada') else [])+[('Lugar',f"{C['museo']} · {C['direccion']}, {C['ciudad']}")]
    dl=''.join(f'<div><span class="k">{k}</span><span>{e(v)}</span></div>' for k,v in rows)
    body=''.join(f'<p>{e(p)}</p>' for p in m['cuerpo'])
    prog=('<div class="prog"><span class="lbl" style="display:block;padding:0 0 18px">Programación</span>'+''.join(f'<div><span>{e(a)}</span>{e(b)}</div>' for a,b in m['programa'])+'</div>') if m.get('programa') else ''
    gal=''
    if m.get('gal'):
        gal='<div class="lbl" style="padding:0 6vw 30px">Galería</div><div class="gal">'+''.join(f'<button data-src="{relimg(g,root)}" style="background-image:url(\'{relimg(g,root)}\')" aria-label="Ampliar imagen"></button>' for g in m['gal'])+'</div>'
    rel=[x for x in M if x['slug']!=m['slug']][:3]
    ph='<span class="ph">Datos a confirmar</span>' if m.get('ph') else ''
    return f'''<main data-slug="{m['slug']}">
<section class="d-hero"><div class="bg" style="background-image:url('{relimg(m['img'],root)}')"></div><div class="sh"></div>
<div class="top"><nav class="crumb" aria-label="Breadcrumb"><a href="{L['home']}">Museo Tamburini</a><span>/</span><a href="{L['list']}">Muestras</a><span>/</span><span>{e(m['titulo'])}</span></nav></div>
<div class="ct"><div class="lbl"><span class="st-badge">{EST[st]}</span> &nbsp;·&nbsp; {e(m['tipo'])} &nbsp;·&nbsp; {rango(m)}{ph}</div><h1>{words}</h1></div></section>
<section class="d-body"><aside class="sticky"><div class="dl">{dl}</div>
<div style="display:flex;gap:12px;flex-wrap:wrap;margin-top:36px"><a data-if-active class="btn acc" href="{cta['url']}" target="_blank" rel="noopener">{e(cta['label'])} ↗</a><a data-if-ended class="btn" href="{L['list']}">Ver otras muestras <span class="ar">→</span></a></div>
<div class="share"></div></aside>
<article class="d-txt"><p class="bajada">{e(m['bajada'])}</p>{body}{prog}</article></section>
{gal}
<section class="related"><div class="s-head"><span class="lbl">Más en el Tamburini</span><h2 style="font-size:clamp(34px,4vw,60px)">Otras <em>experiencias</em></h2></div>
<div class="agrid">{''.join(card(x,L['m'](x['slug']),root) for x in rel)}</div></section></main>'''

def md_page(m):
    t=[f"# {m['titulo']}",'',f"> {m['bajada']}",'',f"- Tipo: {m['tipo']}",f"- Fechas: {rango(m)} ({m['desde']} a {m['hasta']})",f"- Estado: {EST[estado(m)]}"]
    if m.get('horario'): t.append(f"- Horario: {m['horario']}")
    if m.get('entrada'): t.append(f"- Entrada: {m['entrada']}")
    t+= [f"- Lugar: {C['museo']}, {C['direccion']}, {C['ciudad']}, Argentina",f"- Reservas: {(m.get('cta') or {}).get('url',C['bezzapass'])}",f"- URL: {URL(m['slug'])}",'']+m['cuerpo']
    if m.get('programa'): t+=['','## Programación']+[f"- {a}: {b}" for a,b in m['programa']]
    return '\n'.join(t)+'\n'

# ---------- HOME ----------
def home_main(L):
    return f'''<section id="hero" aria-label="Vitreaux del hall central"><div class="h-layer h-base"></div><div class="h-layer h-light"></div><div class="h-tiles"></div><div class="h-fade"></div>
<div class="h-top lbl"><span>Córdoba · Desde 1889</span><span data-open></span></div>
<div class="h-txt"><h1><span class="l"><span>Museo</span></span><span class="l"><span style="animation-delay:.18s"><em>Tamburini</em></span></span></h1>
<div class="h-side"><span class="lbl">Arq. Francisco Tamburini</span><p>Uno de los primeros edificios proyectados para una entidad financiera en América Latina. Mové el cursor: la luz atraviesa el vitreaux.</p>
<div style="display:flex;gap:10px;flex-wrap:wrap"><a class="btn acc" href="#muestras">En cartel <span class="ar">↓</span></a><a class="btn" href="{C['bezzapass']}" target="_blank" rel="noopener">Reservar ↗</a></div></div></div><div class="scroll-ln"></div></section>
<div class="marq"><div class="tr" id="mq"></div></div>

<section class="s" id="muestras"><div class="s-head"><span class="lbl reveal">01 — Muestras</span><div><h2 class="reveal">En <em>cartel</em></h2>
<p class="lead reveal">Cada muestra tiene su propia página para compartir desde cualquier comunicación. <a class="ln" style="color:var(--fg)" href="{L['list']}">Ver todas →</a></p></div></div>
<div class="stage" id="stage"><div class="bars"></div><div class="ctrl"><button id="sPrev">Anterior</button><button id="sPlay">Pausa</button><button id="sNext">Siguiente</button></div></div>
<div class="idx" id="idx"></div>
<div id="archivo" style="padding-top:140px"><div class="s-head" style="margin-bottom:20px"><span class="lbl reveal">Archivo vivo</span><div><h2 class="reveal">Lo que <em>pasó</em></h2>
<p class="lead reveal">Cuando una muestra termina, pasa sola al archivo y conserva su URL.</p><div class="filters" id="fYear"></div><div class="filters" id="fType"></div><div class="count" id="aCount"></div></div></div>
<div class="agrid" id="agrid" data-limit="6"></div></div></section>

<section class="s" id="historia"><div class="s-head"><span class="lbl reveal">02 — Historia</span><h2 class="reveal">150 años en un <em>solo edificio</em></h2></div>
<div class="reveal"><div class="tl-years" id="tlyears"></div><div class="tl-card" id="tlcard"></div></div>
<div class="stats"><div class="stat reveal"><div class="v" data-n="1873">0</div><div class="l">Inicio de actividades del Banco Provincial de Córdoba</div></div>
<div class="stat reveal"><div class="v"><span data-n="2">0</span> años</div><div class="l">Tiempo de construcción de la casa matriz</div></div>
<div class="stat reveal"><div class="v" data-n="130000">0</div><div class="l">Cuentas corrientes en 1968</div></div>
<div class="stat reveal"><div class="v" data-n="155000">0</div><div class="l">Cajas de ahorro en 1968</div></div></div></section>

<section class="s" id="edificio"><div class="s-head"><span class="lbl reveal">03 — El edificio</span><h2 class="reveal">Recorré la <em>casa matriz</em></h2></div>
<div class="exp"><div class="facade reveal" id="facade"><svg viewBox="0 0 400 320" fill="none" stroke="rgba(255,255,255,.7)" stroke-width=".8">
<path class="dr" d="M40 110H360V290H40Z"/><path class="dr" d="M30 110L200 40L370 110Z"/><path class="dr" d="M30 104H370V112H30Z"/><circle class="dr" cx="200" cy="82" r="16"/>
<path class="dr" d="M60 130h14v160H60zM110 130h14v160h-14zM276 130h14v160h-14zM326 130h14v160h-14z"/><path class="dr" d="M170 290V215a30 30 0 0 1 60 0V290"/>
<path class="dr" d="M140 190V156a17 17 0 0 1 34 0V190ZM226 190V156a17 17 0 0 1 34 0V190Z"/><path class="dr" d="M80 250V222a12 12 0 0 1 24 0V250ZM296 250V222a12 12 0 0 1 24 0V250Z"/><path class="dr" d="M20 290H380V300H20Z"/></svg></div>
<div class="hs-p reveal"><div id="hsp"></div><div class="hs-nav"><button class="btn" id="hsPrev">←</button><button class="btn" id="hsNext">→</button></div></div></div></section>

<section class="s" id="tamburini"><div class="s-head"><span class="lbl reveal">04 — El arquitecto</span><div><h2 class="reveal">Francisco <em>Tamburini</em></h2>
<p class="lead reveal">Arquitecto italiano convocado en 1887 por el Directorio del Banco de Córdoba para proyectar su sede central. Su firma está en algunas de las obras más emblemáticas del país.</p></div></div>
<div class="list reveal">{''.join(f'<div class="row"><span class="i">0{i+1}</span><span class="t">{t}</span><span class="d">{d}</span><span class="c">{c}</span><span class="a">→</span></div>' for i,(t,d,c) in enumerate([('Casa Rosada','Ampliación','Buenos Aires'),('Teatro Colón','Proyecto inicial','Buenos Aires'),('Teatro Rivera Indarte','Hoy Libertador San Martín','Córdoba'),('Hospital de Clínicas','Obra pública','Córdoba'),('Penitenciaría San Martín','Obra pública','Córdoba'),('Casa matriz Banco de Córdoba','Inaugurada en 1889','Córdoba')]))}</div></section>

<section class="s" id="vitreaux"><div class="maker"><div><span class="lbl reveal">05 — Participá</span><h2 class="reveal" style="margin-top:30px">Diseñá tu <em>vitreaux</em></h2>
<p class="lead reveal">Con la paleta del vitreaux original: elegí un color, pintá los paneles y compartí tu obra.</p><div class="pal" id="pal"></div>
<div style="display:flex;gap:10px;flex-wrap:wrap"><button class="btn acc" id="rnd">Sorprendeme</button><button class="btn" id="clr">Limpiar</button><button class="btn" id="shr">Compartir</button></div></div>
<div class="vgrid reveal" id="vgrid"></div></div></section>

<section class="s" id="trivia"><div class="s-head"><span class="lbl reveal">06 — Trivia</span><h2 class="reveal">¿Cuánto sabés del <em>Tamburini</em>?</h2></div><div class="qbox reveal" id="qbox"></div></section>

<section class="s" id="hoy"><div class="s-head"><span class="lbl reveal">07 — El museo hoy</span><h2 class="reveal">Un espacio <em>vivo</em></h2></div>
<div class="list reveal"><a class="row" href="https://www.bancor.com.ar/institucional/museo-tamburini/premio-pintura" target="_blank" rel="noopener"><span class="i">01</span><span class="t">Premio de Pintura</span><span class="d">Ediciones, bases e inscripción</span><span class="c">Arte</span><span class="a">↗</span></a>
<div class="row"><span class="i">02</span><span class="t">Biblioteca</span><span class="d">Acervo abierto a la comunidad</span><span class="c">Lectura</span><span class="a">→</span></div>
<a class="row" href="#visita"><span class="i">03</span><span class="t">Visitas guiadas</span><span class="d">Individuos, escuelas y grupos</span><span class="c">Reservas</span><span class="a">→</span></a></div></section>

<section class="s" id="visita"><div class="s-head"><span class="lbl reveal">08 — Visitanos</span><div><h2 class="reveal">Reservá tu <em>visita</em></h2><p class="lead reveal">Entradas y reservas a través de Bezzapass, la plataforma oficial de acceso.</p></div></div>
<div class="bz"><div class="bzframe reveal"><div class="bzbar"><span class="lbl">bezzapass.com.ar</span><a class="lbl ln" style="color:var(--fg)" href="{C['bezzapass']}" target="_blank" rel="noopener">Abrir ↗</a></div>
<iframe id="bzif" src="{C['bezzapass']}" title="Bezzapass · Reservas Museo Tamburini" loading="lazy" allow="payment"></iframe>
<div class="bzfb" id="bzfb"><span class="lbl">Reservas</span><h3 style="font-size:clamp(30px,3vw,46px)">Reservá en <em>Bezzapass</em></h3><a class="btn acc" href="{C['bezzapass']}" target="_blank" rel="noopener">Ir a Bezzapass ↗</a></div></div>
<div class="reveal"><div class="dl"><div><span class="k">Dirección</span><span>{e(C['direccion'])}, {e(C['ciudad'])}</span></div><div><span class="k">Horario</span><span>{e(C['horario'])}<br><span class="lbl" data-open></span></span></div>
<div><span class="k">Teléfono</span><span>{e(C['telefono'])}</span></div><div><span class="k">Entradas</span><span><a class="ln" href="{C['bezzapass']}" target="_blank" rel="noopener">Bezzapass ↗</a></span></div></div>
<div class="map"><iframe loading="lazy" title="Mapa" src="https://www.openstreetmap.org/export/embed.html?bbox=-64.1864%2C-31.4200%2C-64.1784%2C-31.4155&amp;layer=mapnik&amp;marker={C['lat']}%2C{C['lng']}"></iframe></div></div></div></section>'''

def list_main(L):
    return f'''<main><section class="s" style="padding-top:180px;border:0"><nav class="crumb reveal"><a href="{L['home']}">Museo Tamburini</a><span>/</span><span>Muestras</span></nav>
<h1 class="reveal" style="font-size:clamp(60px,11vw,180px);margin:40px 0 0">Muestras</h1><p class="lead reveal">Lo que está en cartel y todo lo que pasó por el Museo Tamburini.</p></section>
<section class="s" id="muestras" style="padding-top:60px"><span class="lbl">En cartel</span><div class="stage" id="stage" style="margin-top:30px"><div class="bars"></div><div class="ctrl"><button id="sPrev">Anterior</button><button id="sPlay">Pausa</button><button id="sNext">Siguiente</button></div></div><div class="idx" id="idx"></div></section>
<section class="s"><div class="s-head" style="margin-bottom:20px"><span class="lbl">Archivo</span><div><h2>Lo que <em>pasó</em></h2><div class="filters" id="fYear"></div><div class="filters" id="fType"></div><div class="count" id="aCount"></div></div></div>
<div class="agrid" id="agrid"></div>
<noscript><ul>{''.join(f'<li><a href="{x["slug"]}/">{e(x["titulo"])}</a></li>' for x in M)}</ul></noscript></section></main>'''

# ---------- BUILD ----------
if DIST.exists(): shutil.rmtree(DIST)
(DIST/'assets').mkdir(parents=True); (DIST/'data').mkdir()
shutil.copy(B/'assets/site.css',DIST/'assets'); shutil.copy(B/'assets/site.js',DIST/'assets'); shutil.copy(B/'assets/vitreaux.jpg',DIST/'assets')
shutil.copy(B/'data/muestras.json',DIST/'data')
OGH=C['base_url']+'/assets/vitreaux.jpg'
act=[m for m in M if estado(m)!='fin']
ld_home={"@context":"https://schema.org",**PLACE,"description":"Museo en la casa matriz histórica del Banco de Córdoba, obra del arquitecto Francisco Tamburini inaugurada en 1889.","openingHours":"Mo-Fr 09:00-16:00","image":OGH,"parentOrganization":ORG,
 "event":[{"@type":"Event","name":m['titulo'],"url":URL(m['slug']),"startDate":m['desde'],"endDate":m['hasta']} for m in act]}

# home
L0={'home':'./','home_s':'','list':'muestras/','m':lambda s:f'muestras/{s}/'}
desc_home="Museo en la histórica casa matriz del Banco de Córdoba (1889), obra de Francisco Tamburini. Muestras en cartel, archivo, vitreaux y reservas."
(DIST/'index.html').write_text(head("Museo Tamburini · Córdoba | Bancor",desc_home,C['base_url']+'/',OGH,[ld_home],'')+header(L0)+home_main(L0)+footer(L0)+site_js('home','','assets/vitreaux.jpg'),encoding='utf-8')
# listado
L1={'home':'../','home_s':'../','list':'./','m':lambda s:f'{s}/'}
ld_list={"@context":"https://schema.org","@type":"CollectionPage","name":"Muestras · Museo Tamburini","url":C['base_url']+'/muestras/',
 "mainEntity":{"@type":"ItemList","itemListElement":[{"@type":"ListItem","position":i+1,"url":URL(m['slug']),"name":m['titulo']} for i,m in enumerate(M)]}}
(DIST/'muestras').mkdir()
(DIST/'muestras/index.html').write_text(head("Muestras · Museo Tamburini | Bancor","Muestras en cartel y archivo histórico del Museo Tamburini, Córdoba.",C['base_url']+'/muestras/',OGH,[ld_list,ld_crumb([('Museo Tamburini',C['base_url']+'/'),('Muestras',C['base_url']+'/muestras/')])],'../')+header(L1)+list_main(L1)+footer(L1)+site_js('list','../','../assets/vitreaux.jpg'),encoding='utf-8')
# detalles
L2={'home':'../../','home_s':'../../','list':'../','m':lambda s:f'../{s}/'}
for m in M:
    p=DIST/'muestras'/m['slug']; p.mkdir()
    t=f"{m['titulo']} · Museo Tamburini | Bancor"; d=f"{m['bajada']} {rango(m)}. {C['museo']}, {C['ciudad']}."
    lds=[ld_event(m),ld_crumb([('Museo Tamburini',C['base_url']+'/'),('Muestras',C['base_url']+'/muestras/'),(m['titulo'],URL(m['slug']))])]
    (p/'index.html').write_text(head(t,d,URL(m['slug']),absimg(m['img']),lds,'../../',extra='<link rel="alternate" type="text/markdown" href="index.md">')+header(L2)+detail_main(m,L2,'../../')+'<div class="lbx" id="lbx"><span class="x">Cerrar</span><img alt=""></div>'+footer(L2)+site_js('detail','../../','../../assets/vitreaux.jpg'),encoding='utf-8')
    (p/'index.md').write_text(md_page(m),encoding='utf-8')
# sitemap / robots / llms
urls=[C['base_url']+'/',C['base_url']+'/muestras/']+[URL(m['slug']) for m in M]
(DIST/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'  <url><loc>{u}</loc><lastmod>{HOY.isoformat()}</lastmod></url>\n' for u in urls)+'</urlset>\n',encoding='utf-8')
(DIST/'robots.txt').write_text(f"User-agent: *\nAllow: /\n\n# Asistentes de IA bienvenidos\nUser-agent: GPTBot\nAllow: /\nUser-agent: ClaudeBot\nAllow: /\nUser-agent: PerplexityBot\nAllow: /\nUser-agent: Google-Extended\nAllow: /\n\nSitemap: {C['base_url']}/sitemap.xml\n",encoding='utf-8')
li=lambda m:f"- [{m['titulo']}]({URL(m['slug'])}index.md): {m['bajada']} ({rango(m)})"
(DIST/'llms.txt').write_text(f"""# {C['museo']}

> Museo ubicado en la histórica casa matriz del Banco de Córdoba (Bancor), {C['direccion']}, {C['ciudad']}, Argentina. El edificio, obra del arquitecto italiano Francisco Tamburini, fue inaugurado el 17 de mayo de 1889 y conserva un vitreaux en el techo del hall central y yesería de Arturo Nembrini Gonzaga.

- Horario: {C['horario']}
- Teléfono: {C['telefono']}
- Entradas y reservas: {C['bezzapass']}

## Muestras en cartel
{chr(10).join(li(m) for m in act) or '- (sin muestras activas)'}

## Archivo
{chr(10).join(li(m) for m in M if estado(m)=='fin')}

## Optional
- [Listado de muestras]({C['base_url']}/muestras/)
- [Datos estructurados]({C['base_url']}/data/muestras.json)
""",encoding='utf-8')

# ---------- PREVIEW (un solo archivo) ----------
vit='data:image/jpeg;base64,'+base64.b64encode((B/'assets/vitreaux.jpg').read_bytes()).decode()
LP={'home':'#','home_s':'','list':'#archivo','m':lambda s:f'#/muestras/{s}/'}
tpls=''.join(f'<template id="tpl-{m["slug"]}">{detail_main(m,LP,"")}</template>' for m in M).replace("assets/vitreaux.jpg","__VITREAUX__")
pv=head("Museo Tamburini · Vista previa",desc_home,C['base_url']+'/',OGH,[ld_home],'',css_inline=CSS.replace('--vit:url(vitreaux.jpg)','--vit:none'))+header(LP)+home_main(LP)+'<div id="pv"></div>'+tpls+'<div class="lbx" id="lbx"><span class="x">Cerrar</span><img alt=""></div>'+footer(LP)
pv=pv.replace('</head>',f'<style>:root{{--vit:url({vit})}}</style></head>',1)+site_js('home','',vit,preview=True,inline=True)
(B/'preview.html').write_text(pv,encoding='utf-8')
print('OK',len(M),'muestras ·',len(urls),'URLs')
