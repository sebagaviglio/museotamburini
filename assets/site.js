/* Museo Tamburini · site.js (boceto v3) */
(function(){
const S=window.SITE,$=s=>document.querySelector(s),$$=s=>[...document.querySelectorAll(s)];
const D=S.data,CFG=D.config,M=D.muestras;
const img=u=>u==='__VITREAUX__'?S.vit:u;
const href=slug=>S.preview?'#/muestras/'+slug+'/':S.root+'muestras/'+slug+'/';
const HOY=new Date();HOY.setHours(0,0,0,0);
const fmt=d=>new Date(d+'T12:00').toLocaleDateString('es-AR',{day:'numeric',month:'short',year:'numeric'});
const rango=m=>m.desde===m.hasta?fmt(m.desde):fmt(m.desde)+' — '+fmt(m.hasta);
const estado=m=>{const a=new Date(m.desde+'T00:00'),b=new Date(m.hasta+'T23:59');return HOY<a?'prox':HOY>b?'fin':'act'};
const EST={act:'En cartel',prox:'Próximamente',fin:'Finalizada'};
const toast=t=>{const e=$('#toast');if(!e)return;e.textContent=t;e.classList.add('on');setTimeout(()=>e.classList.remove('on'),2400)};
window.__toast=toast;

/* file:// → que los links limpios funcionen localmente */
function patchLinks(root){if(location.protocol!=='file:')return;(root||document).querySelectorAll('a[href]').forEach(a=>{const h=a.getAttribute('href');if(h&&!/^(https?:|#|mailto:)/.test(h)&&h.endsWith('/'))a.setAttribute('href',h+'index.html')})}

/* header + progreso */
const hdr=$('.hdr');
addEventListener('scroll',()=>{hdr&&hdr.classList.toggle('solid',scrollY>40);const p=$('#prog');if(p)p.style.width=(scrollY/(document.documentElement.scrollHeight-innerHeight)*100)+'%'},{passive:true});

/* reveal + contadores */
const io=new IntersectionObserver(es=>es.forEach(e=>{if(!e.isIntersecting)return;e.target.classList.add('in');
 const v=e.target.querySelector('[data-n]');if(v&&!v.dataset.done){v.dataset.done=1;const n=+v.dataset.n,t0=performance.now();
  (function tk(t){const p=Math.min(1,(t-t0)/1800),x=Math.round(n*(1-Math.pow(1-p,3)));v.textContent=n>=10000?x.toLocaleString('es-AR'):x;if(p<1)requestAnimationFrame(tk)})(t0)}
 io.unobserve(e.target)}),{threshold:.12});
const watch=r=>(r||document).querySelectorAll('.reveal:not(.in)').forEach(e=>io.observe(e));

/* ===== HERO: vitreaux que se ilumina ===== */
const hero=$('#hero');
if(hero){
 const tiles=hero.querySelector('.h-tiles'),C=12,R=8;
 for(let r=0;r<R;r++)for(let c=0;c<C;c++){const i=document.createElement('i');i.style.animationDelay=(0.15+(r+c)*0.055+Math.random()*.12)+'s';tiles.appendChild(i)}
 const light=hero.querySelector('.h-light');let tx=.5,ty=.42,x=.5,y=.42,idle=true,it;
 hero.addEventListener('pointermove',e=>{const b=hero.getBoundingClientRect();tx=(e.clientX-b.left)/b.width;ty=(e.clientY-b.top)/b.height;idle=false;clearTimeout(it);it=setTimeout(()=>idle=true,2500)});
 let t0=performance.now();
 (function loop(t){if(idle){const k=(t-t0)/1000;tx=.5+Math.sin(k*.35)*.28;ty=.45+Math.sin(k*.5)*.18}
  x+=(tx-x)*.07;y+=(ty-y)*.07;
  const r=Math.max(innerWidth,innerHeight)*(.24+Math.sin((t-t0)/1400)*.02);
  light.style.setProperty('--x',(x*100)+'%');light.style.setProperty('--y',(y*100)+'%');light.style.setProperty('--r',r+'px');
  const sy=Math.min(scrollY,innerHeight);hero.querySelectorAll('.h-layer').forEach(l=>l.style.translate=`0 ${sy*.25}px`);
  requestAnimationFrame(loop)})(t0);
}

/* marquee */
const mq=$('#mq');if(mq){const w=['1889','Patrimonio de Córdoba','Vitreaux','Eclecticismo','Francisco Tamburini','Nembrini Gonzaga','San Jerónimo 166'];let h='';for(let k=0;k<2;k++)w.forEach(t=>h+=`<span>${t}</span>`);mq.innerHTML=h}

/* ===== ESCENARIO: muestras activas ===== */
const stage=$('#stage');
if(stage){
 const act=M.filter(m=>estado(m)!=='fin').sort((a,b)=>a.desde.localeCompare(b.desde));
 const bars=stage.querySelector('.bars'),idx=$('#idx');let k=0,play=true,tm;
 act.forEach((m,i)=>{const d=document.createElement('div');d.className='slide';
  const w=m.titulo.split(' ').map((x,j)=>`<span class="w" style="animation-delay:${.2+j*.07}s">${x}</span>`).join(' ');
  d.innerHTML=(m.video?`<video src="${m.video}" muted loop playsinline></video>`:`<div class="bg" style="background-image:url('${img(m.img)}')"></div>`)+
  `<div class="sh"></div><div class="ct"><div class="lbl"><span class="dot ${estado(m)==='act'?'live':''}"></span><b>${EST[estado(m)]}</b> · ${m.tipo} · ${rango(m)}${m.ph?'<span class="ph">Datos a confirmar</span>':''}</div>
  <h3>${w}</h3><p>${m.bajada}</p><div class="acts"><a class="btn" href="${href(m.slug)}">Ver muestra <span class="ar">→</span></a>${m.cta?`<a class="btn acc" href="${m.cta.url}" target="_blank" rel="noopener">${m.cta.label} ↗</a>`:`<a class="btn acc" href="${CFG.bezzapass}" target="_blank" rel="noopener">Reservar ↗</a>`}</div></div>`;
  stage.insertBefore(d,bars);bars.insertAdjacentHTML('beforeend','<i><span></span></i>');
  idx.insertAdjacentHTML('beforeend',`<a href="${href(m.slug)}" data-i="${i}"><small>0${i+1} · ${m.tipo}</small>${m.titulo}</a>`)});
 idx.querySelectorAll('a').forEach(a=>a.addEventListener('mouseenter',()=>show(+a.dataset.i)));
 function show(i){k=(i+act.length)%act.length;
  stage.querySelectorAll('.slide').forEach((s,j)=>{s.classList.toggle('on',j===k);const v=s.querySelector('video');if(v)j===k?v.play():v.pause()});
  [...bars.children].forEach((b,j)=>{b.className=j<k?'done':'';if(j===k){void b.offsetWidth;b.className='cur'}});
  idx.querySelectorAll('a').forEach((a,j)=>a.classList.toggle('on',j===k));
  clearTimeout(tm);if(play)tm=setTimeout(()=>show(k+1),8000)}
 $('#sNext').onclick=()=>show(k+1);$('#sPrev').onclick=()=>show(k-1);
 $('#sPlay').onclick=e=>{play=!play;stage.classList.toggle('paused',!play);e.target.textContent=play?'Pausa':'Play';play?show(k):clearTimeout(tm)};
 let x0=null;stage.addEventListener('touchstart',e=>x0=e.touches[0].clientX,{passive:true});stage.addEventListener('touchend',e=>{if(x0==null)return;const dx=e.changedTouches[0].clientX-x0;if(Math.abs(dx)>50)show(k+(dx<0?1:-1));x0=null});
 if(act.length)show(0);
}

/* ===== ARCHIVO (se arma solo por fecha) ===== */
const ag=$('#agrid');
if(ag){
 const arc=M.filter(m=>estado(m)==='fin').sort((a,b)=>b.desde.localeCompare(a.desde));
 const lim=+ag.dataset.limit||0;let fy='Todos',ft='Todos';
 const Y=['Todos',...new Set(arc.map(m=>m.desde.slice(0,4)))],T=['Todos',...new Set(arc.map(m=>m.tipo))];
 const mk=(el,arr,g,s)=>{if(!el)return;el.innerHTML='';arr.forEach(v=>{const b=document.createElement('button');b.textContent=v;if(v===g())b.className='on';b.onclick=()=>{s(v);mk(el,arr,g,s);draw()};el.appendChild(b)})};
 mk($('#fYear'),Y,()=>fy,v=>fy=v);mk($('#fType'),T,()=>ft,v=>ft=v);
 function draw(){let L=arc.filter(m=>(fy==='Todos'||m.desde.startsWith(fy))&&(ft==='Todos'||m.tipo===ft));const tot=L.length;if(lim)L=L.slice(0,lim);
  const c=$('#aCount');if(c)c.innerHTML=`<span class="lbl">${tot} ${tot===1?'experiencia':'experiencias'} en el archivo</span>`;
  ag.innerHTML=L.map((m,i)=>`<a class="ai" href="${href(m.slug)}" style="animation-delay:${i*.07}s"><div class="im" style="background-image:url('${img(m.img)}')"></div>
  <div class="meta lbl"><span>${m.desde.slice(0,4)}</span><span>${m.tipo}</span></div><h4>${m.titulo}</h4><span class="go">${rango(m)} &nbsp;→</span></a>`).join('');patchLinks(ag)}
 draw();
}

/* ===== LÍNEA DE TIEMPO ===== */
const tly=$('#tlyears');
if(tly){const TL=[['1873','Nace el Banco Provincial de Córdoba','El 22 de septiembre inicia sus actividades con la misión de proporcionar dinero a bajo interés y a plazos razonables para fomentar el desarrollo de la provincia.'],
 ['1880','Primeras sucursales','Se abren sucursales en Río Cuarto, Villa María, San Pedro y Bell Ville.'],
 ['1887','La decisión de construir','El Directorio, presidido por Santiago Díaz, decide construir una sede central propia y convoca al arquitecto italiano Francisco Tamburini.'],
 ['1889','Inauguración','El 17 de mayo se inaugura la casa matriz, construida en sólo dos años bajo la dirección técnica del ingeniero José Franceschi.'],
 ['1941','El Banco de hoy','Nace el Banco como lo conocemos actualmente.'],
 ['1968','Crecimiento','La entidad atiende 130.000 cuentas corrientes y 155.000 cajas de ahorro.'],
 ['Hoy','Tradición y futuro','Bancor sostiene su apoyo a la cultura, la educación, el deporte y la acción emprendedora.']];
 let i=0,auto=true;TL.forEach((t,j)=>{const b=document.createElement('button');b.textContent=t[0];b.onclick=()=>{auto=false;set(j)};tly.appendChild(b)});
 function set(j){i=j;tly.querySelectorAll('button').forEach((b,n)=>b.classList.toggle('on',n===j));$('#tlcard').innerHTML=`<div class="tl-year sw">${TL[j][0]}</div><div class="tl-txt sw"><h3>${TL[j][1]}</h3><p>${TL[j][2]}</p></div>`}
 set(0);setInterval(()=>auto&&set((i+1)%TL.length),5000)}

/* ===== EDIFICIO ===== */
const fac=$('#facade');
if(fac){const HS=[[50,24,'Fachada','Estilo ecléctico','Tamburini siguió las tendencias de la arquitectura europea de su época, marcada por el eclecticismo y la armonización de estilos.'],
 [50,80,'Vestíbulo','La experiencia de entrar','Desde el ingreso, la opulencia de la decoración y la monumentalidad buscan transmitir una sensación de prestigio y poder.'],
 [37,50,'Vitreaux','El cielo del hall central','Un imponente vitreaux corona el hall central de las antiguas cajas de atención al público.'],
 [63,50,'Yesería','Nembrini Gonzaga','Molduras y yesería con gran variedad de simbolismos, obra de Arturo Nembrini Gonzaga, con decoración inspirada en Versalles.'],
 [20,68,'Símbolo','Progreso económico','La obra es símbolo del progreso de la nueva sociedad que se estaba gestando a fines del siglo XIX.']];
 let c=0;HS.forEach((h,i)=>{const b=document.createElement('button');b.className='hs';b.style.left=h[0]+'%';b.style.top=h[1]+'%';b.setAttribute('aria-label',h[2]);b.onclick=()=>set(i);fac.appendChild(b)});
 function set(i){c=(i+HS.length)%HS.length;fac.querySelectorAll('.hs').forEach((b,j)=>b.classList.toggle('on',j===c));const h=HS[c];
  $('#hsp').innerHTML=`<div class="n sw">0${c+1} / 0${HS.length} — ${h[2].toUpperCase()}</div><h3 class="sw">${h[3]}</h3><p class="sw">${h[4]}</p>`}
 set(0);$('#hsPrev').onclick=()=>set(c-1);$('#hsNext').onclick=()=>set(c+1)}

/* ===== VITREAUX propio (paleta tomada del vitreaux real) ===== */
const vg=$('#vgrid');
if(vg){const P=['#b3262a','#d9a23a','#2f6f8f','#3f7d5a','#e9dfc4','#7a3b2e','#c56b2c','#1d2f4f'];let col=P[0],pd=false;
 const pal=$('#pal');P.forEach((p,i)=>{const b=document.createElement('button');b.style.background=p;if(!i)b.className='on';b.onclick=()=>{col=p;pal.querySelectorAll('button').forEach(x=>x.classList.remove('on'));b.classList.add('on')};pal.appendChild(b)});
 for(let i=0;i<64;i++){const c=document.createElement('div');c.onpointerdown=()=>{pd=true;c.style.background=col};c.onpointerenter=()=>{if(pd)c.style.background=col};vg.appendChild(c)}
 addEventListener('pointerup',()=>pd=false);
 $('#rnd').onclick=()=>[...vg.children].forEach((c,i)=>setTimeout(()=>c.style.background=P[Math.floor(Math.random()*P.length)],i*10));
 $('#clr').onclick=()=>[...vg.children].forEach(c=>c.style.background='');
 $('#shr').onclick=()=>toast('Vitreaux listo para compartir · #MuseoTamburini')}

/* ===== TRIVIA ===== */
const qb=$('#qbox');
if(qb){const Q=[['¿En qué año se inauguró la casa matriz?',['1873','1889','1941','1910'],1,'Se inauguró el 17 de mayo de 1889.'],
 ['¿Cuánto tardó su construcción?',['Dos años','Diez años','Cinco años','Un año'],0,'Fue construida en sólo dos años.'],
 ['¿En qué palacio se inspira su decoración interior?',['Buckingham','Palacio Real de Madrid','Versalles','Schönbrunn'],2,'La decoración se inspira en el Palacio de Versalles.'],
 ['¿Quién realizó las molduras y la yesería?',['José Franceschi','Santiago Díaz','Arturo Nembrini Gonzaga','Tomás Garzón'],2,'Fueron obra de Arturo Nembrini Gonzaga.'],
 ['¿Qué otra obra lleva la firma de Tamburini?',['El Obelisco','Proyecto inicial del Teatro Colón','Cabildo de Córdoba','Catedral de La Plata'],1,'Tamburini realizó el proyecto inicial del Teatro Colón.']];
 let i=0,sc=0;window.__q=()=>{i=0;sc=0;q()};
 function q(){const pr=`<div class="qprog">${Q.map((_,j)=>`<i class="${j<i?'on':''}"></i>`).join('')}</div>`;
  if(i>=Q.length){qb.innerHTML=pr+`<h3 class="sw">${sc}/${Q.length} — ${sc>=4?'Sabés mucho del Tamburini.':'Te esperamos para descubrir el resto.'}</h3><div style="display:flex;gap:12px;flex-wrap:wrap"><a class="btn acc" href="${CFG.bezzapass}" target="_blank" rel="noopener">Reservar visita ↗</a><button class="btn" onclick="__q()">Jugar de nuevo</button></div>`;return}
  const [t,o,c,f]=Q[i];qb.innerHTML=pr+`<h3 class="sw">${t}</h3><div class="opts">${o.map((x,j)=>`<button data-i="${j}"><span>0${j+1}</span>${x}</button>`).join('')}</div><div class="qfb"></div>`;
  qb.querySelectorAll('.opts button').forEach(b=>b.onclick=()=>{const j=+b.dataset.i,bs=qb.querySelectorAll('.opts button');bs.forEach(x=>x.disabled=true);bs[c].classList.add('ok');if(j===c)sc++;else b.classList.add('ko');qb.querySelector('.qfb').textContent=f;setTimeout(()=>{i++;q()},1700)})}
 q()}

/* Bezzapass: si bloquea el embebido, acceso directo */
const bz=$('#bzif');if(bz){let ok=false;bz.addEventListener('load',()=>ok=true);setTimeout(()=>{if(!ok)$('#bzfb').classList.add('on')},6000)}

/* Abierto ahora (hora Córdoba) */
$$('[data-open]').forEach(el=>{const n=new Date(new Date().toLocaleString('en-US',{timeZone:'America/Argentina/Cordoba'})),d=n.getDay(),h=n.getHours();const o=d>=1&&d<=5&&h>=9&&h<16;el.innerHTML=`<span class="dot ${o?'live':''}" style="${o?'':'background:#555'}"></span>${o?'Abierto ahora':'Cerrado ahora'}`});

/* ===== DETALLE (página estática o vista previa) ===== */
function initDetail(root){
 const el=root.querySelector('[data-slug]');if(!el)return;const m=M.find(x=>x.slug===el.dataset.slug);if(!m)return;
 const e=estado(m);root.querySelectorAll('.st-badge').forEach(b=>b.innerHTML=`<span class="dot ${e==='act'?'live':''}" style="${e==='fin'?'background:#555':''}"></span>${EST[e]}`);
 root.querySelectorAll('[data-if-active]').forEach(x=>x.style.display=e==='fin'?'none':'');
 root.querySelectorAll('[data-if-ended]').forEach(x=>x.style.display=e==='fin'?'':'none');
 const url=CFG.base_url+'/muestras/'+m.slug+'/',tx=encodeURIComponent(m.titulo+' · Museo Tamburini'),u=encodeURIComponent(url);
 const sh=root.querySelector('.share');if(sh)sh.innerHTML=`<span class="lbl">Compartir</span><button data-copy>Copiar enlace</button><a target="_blank" rel="noopener" href="https://wa.me/?text=${tx}%20${u}">WhatsApp</a><a target="_blank" rel="noopener" href="https://www.linkedin.com/sharing/share-offsite/?url=${u}">LinkedIn</a><a target="_blank" rel="noopener" href="https://x.com/intent/post?text=${tx}&url=${u}">X</a><a target="_blank" rel="noopener" href="https://www.facebook.com/sharer/sharer.php?u=${u}">Facebook</a>`;
 const cp=root.querySelector('[data-copy]');if(cp)cp.onclick=()=>{navigator.clipboard&&navigator.clipboard.writeText(url);toast('Enlace copiado')};
 const lb=$('#lbx');root.querySelectorAll('.gal button').forEach(b=>b.onclick=()=>{lb.querySelector('img').src=b.dataset.src;lb.classList.add('on')});
 if(lb)lb.onclick=()=>lb.classList.remove('on');
 watch(root);patchLinks(root)}
if(S.page==='detail')initDetail(document);

/* Vista previa: router por hash que muestra la misma página de detalle generada */
if(S.preview){const pv=$('#pv');
 function route(){const mm=location.hash.match(/^#\/muestras\/([^/]+)\/?$/);
  if(mm){const t=document.getElementById('tpl-'+mm[1]);if(!t)return;pv.innerHTML=t.innerHTML;pv.classList.add('on');pv.scrollTop=0;document.body.style.overflow='hidden';
   pv.querySelectorAll('.d-hero .bg').forEach(b=>b.style.backgroundImage=b.style.backgroundImage.replace('__VITREAUX__',S.vit));
   pv.querySelectorAll('.gal button').forEach(b=>{if(b.dataset.src==='__VITREAUX__'){b.dataset.src=S.vit;b.style.backgroundImage=`url('${S.vit}')`}});
   pv.querySelectorAll('.ai .im').forEach(b=>b.style.backgroundImage=b.style.backgroundImage.replace('__VITREAUX__',S.vit));
   initDetail(pv);document.title=mm[1]}
  else{pv.classList.remove('on');pv.innerHTML='';document.body.style.overflow=''}}
 addEventListener('hashchange',route);route()}

watch();patchLinks();
})();
