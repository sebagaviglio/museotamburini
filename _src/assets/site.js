/* Museo Tamburini · site.js v5 */
(function(){
const S=window.SITE,$=s=>document.querySelector(s),$$=s=>[...document.querySelectorAll(s)];
const D=S.data,CFG=D.config,M=D.muestras;
const img=u=>!u?'':u==='__VITREAUX__'?S.vit:(S.imgs&&S.imgs[u])?S.imgs[u]:u.startsWith('assets/')?S.root+u:u;
const href=slug=>S.preview?'#/muestras/'+slug+'/':S.root+'muestras/'+slug+'/';
const HOY=new Date();HOY.setHours(0,0,0,0);
const MES=['ene','feb','mar','abr','may','jun','jul','ago','sep','oct','nov','dic'];
const dd=s=>new Date(s+'T12:00');
const fmt=s=>{const d=dd(s);return d.getDate()+' '+MES[d.getMonth()]+' '+d.getFullYear()};
const rango=m=>m.desde===m.hasta?fmt(m.desde):fmt(m.desde)+' — '+fmt(m.hasta);
const estado=m=>{const a=new Date(m.desde+'T00:00'),b=new Date(m.hasta+'T23:59');return HOY<a?'prox':HOY>b?'fin':'act'};
const EST={act:'En cartel',prox:'Próximamente',fin:'Finalizada'};
const toast=t=>{const e=$('#toast');if(!e)return;e.textContent=t;e.classList.add('on');setTimeout(()=>e.classList.remove('on'),2400)};
const split=(t,base=.15,step=.07)=>t.split(' ').map((w,j)=>`<span class="w" style="animation-delay:${base+j*step}s">${w}</span>`).join(' ');
function patchLinks(r){if(location.protocol!=='file:'||S.preview)return;(r||document).querySelectorAll('a[href]').forEach(a=>{const h=a.getAttribute('href');if(h&&!/^(https?:|#|mailto:|tel:)/.test(h)&&h.endsWith('/'))a.setAttribute('href',h+'index.html')})}

const hdr=$('.hdr');
addEventListener('scroll',()=>{hdr&&hdr.classList.toggle('solid',scrollY>40);const p=$('#prog');if(p)p.style.width=(scrollY/(document.documentElement.scrollHeight-innerHeight)*100)+'%'},{passive:true});
const io=new IntersectionObserver(es=>es.forEach(e=>{if(!e.isIntersecting)return;e.target.classList.add('in');
 e.target.querySelectorAll('[data-n]').forEach(v=>{if(v.dataset.done)return;v.dataset.done=1;const n=+v.dataset.n,t0=performance.now();
  (function tk(t){const p=Math.min(1,(t-t0)/1800),x=Math.round(n*(1-Math.pow(1-p,3)));v.textContent=n>=10000?x.toLocaleString('es-AR'):x;if(p<1)requestAnimationFrame(tk)})(t0)});
 io.unobserve(e.target)}),{threshold:.12});
const watch=r=>(r||document).querySelectorAll('.reveal:not(.in),.chap:not(.in)').forEach(e=>io.observe(e));

/* 01 · vitreaux con luz */
const hero=$('#hero');
if(hero){const tiles=hero.querySelector('.h-tiles');
 for(let r=0;r<8;r++)for(let c=0;c<12;c++){const i=document.createElement('i');i.style.animationDelay=(0.15+(r+c)*0.055+Math.random()*.12)+'s';tiles.appendChild(i)}
 const light=hero.querySelector('.h-light');let tx=.5,ty=.42,x=.5,y=.42,idle=true,it;const t0=performance.now();
 hero.addEventListener('pointermove',e=>{const b=hero.getBoundingClientRect();tx=(e.clientX-b.left)/b.width;ty=(e.clientY-b.top)/b.height;idle=false;clearTimeout(it);it=setTimeout(()=>idle=true,2500)});
 (function loop(t){if(idle){const k=(t-t0)/1000;tx=.5+Math.sin(k*.35)*.28;ty=.45+Math.sin(k*.5)*.18}
  x+=(tx-x)*.07;y+=(ty-y)*.07;const r=Math.max(innerWidth,innerHeight)*(.24+Math.sin((t-t0)/1400)*.02);
  light.style.setProperty('--x',(x*100)+'%');light.style.setProperty('--y',(y*100)+'%');light.style.setProperty('--r',r+'px');
  const sy=Math.min(scrollY,innerHeight);hero.querySelectorAll('.h-layer').forEach(l=>l.style.translate=`0 ${sy*.25}px`);
  requestAnimationFrame(loop)})(t0)}
const mq=$('#mq');if(mq){const w=['Arquitectura','Historia','Patrimonio','Arte contemporáneo','Infancias','Desde 1889','San Jerónimo 166'];let h='';for(let k=0;k<2;k++)w.forEach(t=>h+=`<span>${t}</span>`);mq.innerHTML=h}

/* 02-04 · capítulos */
$$('.chap h2[data-split]').forEach(h=>h.innerHTML=split(h.textContent,.1,.08));
const chaps=$$('.chap');
if(chaps.length){const vio=new IntersectionObserver(es=>es.forEach(e=>{const v=e.target.querySelector('video');if(v)e.isIntersecting?v.play().catch(()=>{}):v.pause()}),{threshold:.3});
 chaps.forEach(c=>vio.observe(c));
 addEventListener('scroll',()=>chaps.forEach(c=>{const r=c.getBoundingClientRect();if(r.bottom<0||r.top>innerHeight)return;const p=(r.top+r.height/2-innerHeight/2)/innerHeight;c.querySelector('.media').style.transform=`translateY(${p*-9}%)`}),{passive:true})}

/* 02 · historia */
const tly=$('#tlyears');
if(tly){const TL=[['1873','Nace el Banco Provincial de Córdoba','El 22 de septiembre inicia sus actividades. Su Carta Orgánica, redactada por el ministro Tomás Garzón y el legislador José Olmos, fija la misión de fomentar el desarrollo económico de la provincia.'],
 ['1880','Primeras sucursales','Se abren sucursales en Río Cuarto, Villa María, San Pedro y Bell Ville.'],
 ['1887','La decisión de construir','El Directorio, presidido por Santiago Díaz, decide construir una sede central propia y convoca al arquitecto italiano Francisco Tamburini.'],
 ['1889','Inauguración','El 17 de mayo se inaugura la casa matriz, construida en sólo dos años bajo la dirección técnica del ingeniero José Franceschi.'],
 ['1941','El Banco de hoy','Nace el Banco como lo conocemos actualmente.'],
 ['1968','Crecimiento','La entidad atiende 130.000 cuentas corrientes y 155.000 cajas de ahorro.'],
 ['Hoy','Un edificio por descubrir','El museo abre la casa matriz como espacio de patrimonio, arte y nuevas narrativas.']];
 let i=0,auto=true;TL.forEach((t,j)=>{const b=document.createElement('button');b.textContent=t[0];b.onclick=()=>{auto=false;set(j)};tly.appendChild(b)});
 function set(j){i=j;tly.querySelectorAll('button').forEach((b,n)=>b.classList.toggle('on',n===j));$('#tlcard').innerHTML=`<div class="tl-year sw">${TL[j][0]}</div><div class="tl-txt sw"><h3>${TL[j][1]}</h3><p>${TL[j][2]}</p></div>`}
 set(0);setInterval(()=>auto&&set((i+1)%TL.length),5000)}

/* 03 · escenario de arte */
const stage=$('#stage');
if(stage){const eje=stage.dataset.eje;const act=M.filter(m=>estado(m)!=='fin'&&(!eje||m.eje===eje)).sort((a,b)=>a.desde.localeCompare(b.desde));
 const bars=stage.querySelector('.bars'),idx=$('#idx');let k=0,play=true,tm;
 act.forEach((m,i)=>{const d=document.createElement('div');d.className='slide';
  d.innerHTML=(m.video?`<video src="${m.video}" muted loop playsinline></video>`:`<div class="bg" style="background-image:url('${img(m.img)}')"></div>`)+
  `<div class="sh"></div><div class="ct"><div class="lbl"><span class="dot ${estado(m)==='act'?'live':''}"></span><b>${EST[estado(m)]}</b> · ${m.tipo} · ${rango(m)}${m.ph?'<span class="ph">Datos a confirmar</span>':''}</div>
  <h3>${split(m.titulo,.2)}</h3><p>${m.bajada}</p><div class="acts"><a class="btn" href="${href(m.slug)}">Ver más <span class="ar">→</span></a>${m.cta?`<a class="btn acc" href="${m.cta.url}" target="_blank" rel="noopener">${m.cta.label} ↗</a>`:`<a class="btn acc" href="${CFG.bezzapass}" target="_blank" rel="noopener">Reservar ↗</a>`}</div></div>`;
  stage.insertBefore(d,bars);bars.insertAdjacentHTML('beforeend','<i><span></span></i>');
  idx.insertAdjacentHTML('beforeend',`<a href="${href(m.slug)}" data-i="${i}"><small>0${i+1} · ${EST[estado(m)]}</small>${m.titulo}</a>`)});
 idx.querySelectorAll('a').forEach(a=>a.addEventListener('mouseenter',()=>show(+a.dataset.i)));
 function show(i){if(!act.length)return;k=(i+act.length)%act.length;
  stage.querySelectorAll('.slide').forEach((s,j)=>{s.classList.toggle('on',j===k);const v=s.querySelector('video');if(v)j===k?v.play():v.pause()});
  [...bars.children].forEach((b,j)=>{b.className=j<k?'done':'';if(j===k){void b.offsetWidth;b.className='cur'}});
  idx.querySelectorAll('a').forEach((a,j)=>a.classList.toggle('on',j===k));clearTimeout(tm);if(play)tm=setTimeout(()=>show(k+1),8000)}
 $('#sNext').onclick=()=>show(k+1);$('#sPrev').onclick=()=>show(k-1);
 $('#sPlay').onclick=e=>{play=!play;stage.classList.toggle('paused',!play);e.target.textContent=play?'Pausa':'Play';play?show(k):clearTimeout(tm)};
 let x0=null;stage.addEventListener('touchstart',e=>x0=e.touches[0].clientX,{passive:true});stage.addEventListener('touchend',e=>{if(x0==null)return;const dx=e.changedTouches[0].clientX-x0;if(Math.abs(dx)>50)show(k+(dx<0?1:-1));x0=null});
 show(0)}

/* 04 · infancias */
const vg=$('#vgrid');
if(vg){const P=['#b3262a','#d9a23a','#2f6f8f','#3f7d5a','#e9dfc4','#7a3b2e','#c56b2c','#1d2f4f'];let col=P[0],pd=false;
 const pal=$('#pal');P.forEach((p,i)=>{const b=document.createElement('button');b.style.background=p;b.setAttribute('aria-label','Color '+(i+1));if(!i)b.className='on';b.onclick=()=>{col=p;pal.querySelectorAll('button').forEach(x=>x.classList.remove('on'));b.classList.add('on')};pal.appendChild(b)});
 for(let i=0;i<64;i++){const c=document.createElement('div');c.onpointerdown=()=>{pd=true;c.style.background=col};c.onpointerenter=()=>{if(pd)c.style.background=col};vg.appendChild(c)}
 addEventListener('pointerup',()=>pd=false);
 $('#rnd').onclick=()=>[...vg.children].forEach((c,i)=>setTimeout(()=>c.style.background=P[Math.floor(Math.random()*P.length)],i*10));
 $('#clr').onclick=()=>[...vg.children].forEach(c=>c.style.background='');
 $('#shr').onclick=()=>toast('Vitreaux listo para compartir · #MuseoTamburini')}
const qb=$('#qbox');
if(qb){const Q=[['¿En qué año se inauguró la casa matriz?',['1873','1889','1941','1910'],1,'Se inauguró el 17 de mayo de 1889.'],
 ['¿Cuánto tardó su construcción?',['Dos años','Diez años','Cinco años','Un año'],0,'Fue construida en sólo dos años.'],
 ['¿En qué palacio se inspira su decoración interior?',['Buckingham','Palacio Real de Madrid','Versalles','Schönbrunn'],2,'La decoración se inspira en el Palacio de Versalles.'],
 ['¿Quién realizó las molduras y la yesería?',['José Franceschi','Santiago Díaz','Arturo Nembrini Gonzaga','Tomás Garzón'],2,'Fueron obra de Arturo Nembrini Gonzaga.'],
 ['¿Qué otra obra lleva la firma de Tamburini?',['El Obelisco','Proyecto inicial del Teatro Colón','Cabildo de Córdoba','Catedral de La Plata'],1,'Tamburini realizó el proyecto inicial del Teatro Colón.']];
 let i=0,sc=0;window.__q=()=>{i=0;sc=0;q()};
 function q(){const pr=`<div class="qprog">${Q.map((_,j)=>`<i class="${j<i?'on':''}"></i>`).join('')}</div>`;
  if(i>=Q.length){qb.innerHTML=pr+`<h3 class="sw">${sc}/${Q.length} — ${sc>=4?'¡Sabés mucho del Tamburini!':'Te esperamos para descubrir el resto.'}</h3><div style="display:flex;gap:12px;flex-wrap:wrap"><a class="btn acc" href="${CFG.bezzapass}" target="_blank" rel="noopener">Reservar visita ↗</a><button class="btn" onclick="__q()">Jugar de nuevo</button></div>`;return}
  const [t,o,c,f]=Q[i];qb.innerHTML=pr+`<span class="lbl">Trivia · ${i+1}/${Q.length}</span><h3 class="sw" style="margin-top:20px">${t}</h3><div class="opts">${o.map((x,j)=>`<button data-i="${j}"><span>0${j+1}</span>${x}</button>`).join('')}</div><div class="qfb"></div>`;
  qb.querySelectorAll('.opts button').forEach(b=>b.onclick=()=>{const j=+b.dataset.i,bs=qb.querySelectorAll('.opts button');bs.forEach(x=>x.disabled=true);bs[c].classList.add('ok');if(j===c)sc++;else b.classList.add('ko');qb.querySelector('.qfb').textContent=f;setTimeout(()=>{i++;q()},1700)})}
 q()}

/* 05 · Explorá de otra manera */
const XP=[
 {t:'Hall de Caja',k:'Imagen explorable',img:'__VITREAUX__',d:'El corazón del edificio: el antiguo hall de atención al público, coronado por el vitreaux.',
  body:['Un imponente vitreaux corona el hall central de las antiguas cajas de atención al público.','Lo acompañan molduras y yesería con gran variedad de simbolismos, obra del artista Arturo Nembrini Gonzaga, en una decoración inspirada en el Palacio de Versalles.'],
  pins:[[34,40,'Escudo de Córdoba'],[62,22,'Ornamentos vegetales'],[80,62,'Paneles geométricos']]},
 {t:'Sala Tomás Garzón',k:'Recreación histórica',img:'assets/img/salas-recreacion/sala-tomas-garzon.jpg',d:'Los orígenes de una institución cordobesa, en una sala de época con piezas, retrato y tótem interactivo.',
  body:['Tomás Garzón, entonces ministro, redactó junto al legislador José Olmos la Carta Orgánica del Banco Provincial de Córdoba, que inició sus actividades el 22 de septiembre de 1873.','La sala propone una recreación de época para conocer cómo empezó todo: el retrato, el escritorio y el libro de actas fundacional.'],
  pins:[[9,22,'Retrato de Tomás Garzón'],[16,58,'Tótem interactivo'],[55,60,'Escritorio de época'],[48,82,'Libro de Actas Fundacional']],ph:true},
 {t:'Descubrí la bóveda',k:'Narrativa audiovisual',img:'assets/img/boveda/tesoro-secreto-boveda.jpg',d:'Bienvenido al tesoro secreto: un recorrido por el camino del dinero hasta la puerta de la bóveda.',
  body:['Un recorrido que sigue el camino del dinero: origen de la moneda, acuñación, imprenta y billetes, transporte de valores, custodia y seguridad, y llegada a las sucursales.','Al final del camino, la puerta de la bóveda.'],
  pins:[[12,48,'El camino del dinero'],[36,38,'La bóveda en el archivo'],[70,52,'Puerta de la bóveda'],[57,82,'Recorrido en el piso']],ph:true},
 {t:'Sala numismática',k:'Colección explorable',img:'assets/img/numismatica/sala-numismatica-numa.jpg',d:'NUMA · De la moneda al algoritmo: de la Antigüedad al siglo XXI.',
  body:['Un recorrido en cinco etapas: Mundo antiguo, Edad Media, Edad Moderna, Época contemporánea y Siglo XX y XXI.','Vitrinas y paneles por época para seguir la evolución del dinero de la moneda al algoritmo.'],
  pins:[[14,40,'Recorrido en 5 etapas'],[66,36,'Paneles por época'],[42,66,'Vitrinas centrales'],[30,32,'Medallas y monedas']],ph:true},
 {t:'Centro interactivo',k:'Experiencia inmersiva',img:'assets/img/innovacion/centro-interactivo-linea-de-tiempo.jpg',d:'Una pantalla envolvente para recorrer Córdoba y el Banco de 1889 a hoy.',
  body:['Una pantalla curva que recorre la ciudad y el Banco a través del tiempo, de 1889 a 2026.'],
  pins:[[12,62,'1889'],[48,62,'1970'],[80,62,'2026']],ph:true},
 {t:'Historia del dinero',k:'Interactivo',img:'',d:'Contenido e imagen a desarrollar con el equipo del museo.',body:['Contenido sujeto a desarrollo y validación.'],pins:[],ph:true},
 {t:'Salón de los Acuerdos',k:'Recorrido digital',img:'',d:'Contenido e imagen a desarrollar con el equipo del museo.',body:['Contenido sujeto a desarrollo y validación.'],pins:[],ph:true}];
const xl=$('#xpList');
if(xl){const view=$('#xpView');
 XP.forEach((x,i)=>{xl.insertAdjacentHTML('beforeend',`<button data-i="${i}"><span class="i">0${i+1}</span><span class="t">${x.t}</span><span class="k">${x.k} →</span></button>`);
  view.insertAdjacentHTML('beforeend',`<div class="pic${x.img?'':' empty'}" style="${x.img?`background-image:url('${img(x.img)}')`:''}"></div>`)});
 view.insertAdjacentHTML('beforeend','<div class="cap"><span class="lbl" id="xpK"></span><p id="xpD"></p></div>');
 const set=i=>{xl.querySelectorAll('button').forEach((b,j)=>b.classList.toggle('on',j===i));view.querySelectorAll('.pic').forEach((p,j)=>p.classList.toggle('on',j===i));$('#xpK').innerHTML=XP[i].k+(XP[i].ph?`<span class="ph">${XP[i].img?'Contenido a validar':'A desarrollar'}</span>`:'');$('#xpD').textContent=XP[i].d};
 xl.querySelectorAll('button').forEach(b=>{b.onmouseenter=()=>set(+b.dataset.i);b.onclick=()=>openX(+b.dataset.i)});set(0);
 const exo=$('#exo');
 function openX(i){const x=XP[i],u=img(x.img);
  exo.innerHTML=`<div class="bar"><span class="lbl"><b>05 · Explorá</b> &nbsp;/&nbsp; ${x.t}</span><button class="lbl" id="exoX" style="color:var(--fg)">Cerrar ✕</button></div>
  <div class="st${u?'':' nolens'}" id="exoSt"><div class="pan${u?'':' empty'}" id="exoPan" style="${u?`background-image:url('${u}')`:''}"></div><div class="lens" id="exoL" style="${u?`background-image:url('${u}')`:''}"></div>
  ${x.pins.map(p=>`<div class="pin" style="left:${p[0]}%;top:${p[1]}%"><span>${p[2]}</span></div>`).join('')}
  <div class="hint lbl">${u?'Mové el cursor para explorar · la lupa amplía el detalle':'Imagen pendiente'}</div></div>
  <div class="body"><div><span class="lbl">${x.k}${x.ph?`<span class="ph">${x.img?'Contenido a validar':'A desarrollar'}</span>`:''}</span><h3 style="margin-top:24px">${x.t}</h3></div><div>${x.body.map(p=>`<p>${p}</p>`).join('')}
  <div style="display:flex;gap:12px;flex-wrap:wrap;margin-top:30px"><a class="btn acc" href="${CFG.bezzapass}" target="_blank" rel="noopener">Vivilo en persona ↗</a>${i<XP.length-1?`<button class="btn" id="exoN">Siguiente: ${XP[i+1].t} →</button>`:''}</div></div></div>`;
  exo.classList.add('on');exo.scrollTop=0;document.body.style.overflow='hidden';
  const st=$('#exoSt'),pan=$('#exoPan'),L=$('#exoL'),Z=2.6;
  if(u)st.onpointermove=e=>{const r=st.getBoundingClientRect(),px=(e.clientX-r.left)/r.width,py=(e.clientY-r.top)/r.height;
   pan.style.transform=`scale(1.08) translate(${(.5-px)*5}%,${(.5-py)*5}%)`;
   L.style.left=(e.clientX-r.left)+'px';L.style.top=(e.clientY-r.top)+'px';L.style.backgroundSize=`${r.width*Z}px ${r.height*Z}px`;L.style.backgroundPosition=`${-(px*r.width*Z-120)}px ${-(py*r.height*Z-120)}px`};
  $('#exoX').onclick=closeX;const n=$('#exoN');if(n)n.onclick=()=>openX(i+1)}
 function closeX(){exo.classList.remove('on');document.body.style.overflow=''}
 addEventListener('keydown',e=>{if(e.key==='Escape')closeX()})}

/* 06 · espacios (imágenes resueltas) */
$$('[data-bg]').forEach(el=>el.style.backgroundImage=`url('${img(el.dataset.bg)}')`);

/* 06 · agenda */
const ag=$('#agenda');
if(ag){const TABS=[['Todo',m=>estado(m)!=='fin'],['Muestras',m=>m.tipo==='Muestra'&&estado(m)!=='fin'],['Actividades',m=>m.tipo==='Actividad'&&estado(m)!=='fin'],['Visitas guiadas',m=>m.tipo==='Visita guiada'&&estado(m)!=='fin'],['Archivo',m=>estado(m)==='fin']];
 const tabs=$('#tabs'),th=$('#evthumb');let cur=0;
 TABS.forEach((t,i)=>{const b=document.createElement('button');b.innerHTML=`${t[0]}<sup>${M.filter(t[1]).length}</sup>`;b.onclick=()=>{cur=i;draw()};tabs.appendChild(b)});
 function draw(){tabs.querySelectorAll('button').forEach((b,i)=>b.classList.toggle('on',i===cur));
  const L=M.filter(TABS[cur][1]).sort((a,b)=>cur===4?b.desde.localeCompare(a.desde):a.desde.localeCompare(b.desde));
  ag.innerHTML=L.length?L.map((m,i)=>{const d=dd(m.desde);return `<a class="ev" href="${href(m.slug)}" data-img="${img(m.img)}" style="animation-delay:${i*.06}s"><div class="dt"><b>${d.getDate()} ${MES[d.getMonth()]}</b>${m.desde!==m.hasta?'hasta '+fmt(m.hasta):d.getFullYear()}</div><h4>${m.titulo}</h4><span class="ty"><span class="dot ${estado(m)==='act'?'live':''}" style="${estado(m)==='fin'?'background:#555':''}"></span>${EST[estado(m)]} · ${m.tipo}</span><span class="go">Ver →</span></a>`}).join(''):'<div class="empty">No hay propuestas en esta categoría por ahora.</div>';
  ag.querySelectorAll('.ev').forEach(e=>{e.onmouseenter=()=>{th.style.backgroundImage=`url('${e.dataset.img}')`;th.classList.add('on')};e.onmouseleave=()=>th.classList.remove('on')});patchLinks(ag)}
 addEventListener('pointermove',e=>{th.style.left=e.clientX+'px';th.style.top=e.clientY+'px'});draw()}

const ga=$('#agrid');
if(ga){const arc=M.filter(m=>estado(m)==='fin').sort((a,b)=>b.desde.localeCompare(a.desde));let fy='Todos';
 const Y=['Todos',...new Set(arc.map(m=>m.desde.slice(0,4)))];
 const mk=()=>{const el=$('#fYear');el.innerHTML='';Y.forEach(v=>{const b=document.createElement('button');b.textContent=v;if(v===fy)b.className='on';b.onclick=()=>{fy=v;mk();draw()};el.appendChild(b)})};
 function draw(){const L=arc.filter(m=>fy==='Todos'||m.desde.startsWith(fy));ga.innerHTML=L.map(m=>`<a class="ai" href="${href(m.slug)}"><div class="im" style="background-image:url('${img(m.img)}')"></div><div class="meta lbl"><span>${m.desde.slice(0,4)}</span><span>${m.tipo}</span></div><h4>${m.titulo}</h4><span class="go">${rango(m)} →</span></a>`).join('');patchLinks(ga)}
 mk();draw()}

$$('[data-open]').forEach(el=>{const n=new Date(new Date().toLocaleString('en-US',{timeZone:'America/Argentina/Cordoba'})),d=n.getDay(),h=n.getHours();const o=d>=1&&d<=5&&h>=9&&h<16;el.innerHTML=`<span class="dot ${o?'live':''}" style="${o?'':'background:#555'}"></span>${o?'Abierto ahora':'Cerrado ahora'}`});

function initDetail(root){const el=root.querySelector('[data-slug]');if(!el)return;const m=M.find(x=>x.slug===el.dataset.slug);if(!m)return;const e=estado(m);
 root.querySelectorAll('.st-badge').forEach(b=>b.innerHTML=`<span class="dot ${e==='act'?'live':''}" style="${e==='fin'?'background:#555':''}"></span>${EST[e]}`);
 root.querySelectorAll('[data-if-active]').forEach(x=>x.style.display=e==='fin'?'none':'');root.querySelectorAll('[data-if-ended]').forEach(x=>x.style.display=e==='fin'?'':'none');
 const url=CFG.base_url+'/muestras/'+m.slug+'/',tx=encodeURIComponent(m.titulo+' · Museo Tamburini'),u=encodeURIComponent(url);
 const sh=root.querySelector('.share');if(sh)sh.innerHTML=`<span class="lbl">Compartir</span><button data-copy>Copiar enlace</button><a target="_blank" rel="noopener" href="https://wa.me/?text=${tx}%20${u}">WhatsApp</a><a target="_blank" rel="noopener" href="https://www.linkedin.com/sharing/share-offsite/?url=${u}">LinkedIn</a><a target="_blank" rel="noopener" href="https://x.com/intent/post?text=${tx}&url=${u}">X</a><a target="_blank" rel="noopener" href="https://www.facebook.com/sharer/sharer.php?u=${u}">Facebook</a>`;
 const cp=root.querySelector('[data-copy]');if(cp)cp.onclick=()=>{navigator.clipboard&&navigator.clipboard.writeText(url);toast('Enlace copiado')};
 const lb=$('#lbx');root.querySelectorAll('.gal button').forEach(b=>b.onclick=()=>{lb.querySelector('img').src=b.dataset.src;lb.classList.add('on')});if(lb)lb.onclick=()=>lb.classList.remove('on');
 watch(root);patchLinks(root)}
if(S.page==='detail')initDetail(document);
if(S.preview){const pv=$('#pv');
 function route(){const mm=location.hash.match(/^#\/muestras\/([^/]+)\/?$/);
  if(mm){const t=document.getElementById('tpl-'+mm[1]);if(!t)return;pv.innerHTML=t.innerHTML;
   pv.querySelectorAll('[data-bg]').forEach(el=>el.style.backgroundImage=`url('${img(el.dataset.bg)}')`);
   pv.querySelectorAll('.gal button[data-k]').forEach(b=>b.dataset.src=img(b.dataset.k));
   pv.classList.add('on');pv.scrollTop=0;document.body.style.overflow='hidden';initDetail(pv)}
  else if(pv.classList.contains('on')){pv.classList.remove('on');pv.innerHTML='';document.body.style.overflow=''}}
 addEventListener('hashchange',route);route()}
watch();patchLinks();
})();
