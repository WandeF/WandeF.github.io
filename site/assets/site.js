(function(){
'use strict';
const side = document.getElementById('doc-nav');
const menu = document.getElementById('menu-button');
if (menu && side) menu.addEventListener('click',function(){
 const show = side.classList.toggle('open'); menu.setAttribute('aria-expanded',String(show));
});
const field = document.getElementById('search');
const results = document.getElementById('search-results');
const lang = document.body.dataset.lang || 'zh';
let allPages = [];
fetch('../../search-index.json').then(r=>r.ok?r.json():[]).then(v=>{allPages=v.filter(x=>x.lang===lang); if(field && field.value) present(field.value)}).catch(()=>{});
function present(q){
 if (!field || !results) return;
 q=q.toLocaleLowerCase().trim();
 if (!q){results.hidden=true;return;}
 const hits=allPages.filter(p=>(p.title+' '+p.description+' '+p.slug+' '+p.text).toLocaleLowerCase().includes(q)).slice(0,7);
 results.hidden=false;
 if (!hits.length){results.innerHTML='<div class="empty">'+(lang==='zh'?'未找到页面':'No matching pages')+'</div>';return;}
 results.replaceChildren();
 hits.forEach(p=>{
   const a=document.createElement('a');a.href=p.slug+'.html';a.textContent=p.title;
   const small=document.createElement('small');small.textContent=p.description.slice(0,68);a.appendChild(small);
   results.appendChild(a);
 });
}
if(field){field.addEventListener('input',()=>present(field.value));
 document.addEventListener('keydown',e=>{if(e.key==='/'&&!['INPUT','TEXTAREA'].includes(document.activeElement.tagName)){e.preventDefault();field.focus()};if(e.key==='Escape'){field.blur();results.hidden=true}})
}
// Shared image viewer for both documentation languages.
const pictures = document.querySelectorAll('.content figure img');
if (pictures.length) {
 const labels = lang === 'zh'
  ? {open:'查看大图', close:'关闭', zoom:'原始大小', fit:'适应屏幕'}
  : {open:'View image', close:'Close', zoom:'Original size', fit:'Fit to screen'};
 const viewer = document.createElement('dialog');
 viewer.className = 'image-viewer';
 viewer.setAttribute('aria-label', labels.open);
 const toolbar = document.createElement('div'); toolbar.className = 'image-viewer-toolbar';
 const caption = document.createElement('span'); caption.className = 'image-viewer-caption';
 toolbar.appendChild(caption);
 function control(label) {
  const button = document.createElement('button'); button.type = 'button'; button.textContent = label;
  toolbar.appendChild(button); return button;
 }
 const zoom = control(labels.zoom), close = control(labels.close);
 const stage = document.createElement('div'); stage.className = 'image-viewer-stage';
 stage.tabIndex = 0; stage.setAttribute('aria-label', labels.open);
 const image = document.createElement('img'); stage.appendChild(image);
 viewer.append(toolbar, stage); document.body.appendChild(viewer);
 let trigger;
 function setZoom(expanded) {
  viewer.classList.toggle('image-viewer-zoomed', expanded);
  zoom.textContent = expanded ? labels.fit : labels.zoom;
  zoom.setAttribute('aria-pressed', String(expanded));
  stage.scrollTop = 0; stage.scrollLeft = 0;
 }
 zoom.addEventListener('click', () => setZoom(!viewer.classList.contains('image-viewer-zoomed')));
 close.addEventListener('click', () => viewer.close());
 viewer.addEventListener('close', () => {
  document.body.classList.remove('image-viewer-open');
  image.removeAttribute('src');
  if (trigger) trigger.focus();
 });
 pictures.forEach(picture => {
  let opener = picture.closest('a');
  if (!opener) {
   opener = document.createElement('button'); opener.type = 'button';
   picture.parentNode.insertBefore(opener, picture); opener.appendChild(picture);
  }
  opener.classList.add('image-opener');
  opener.setAttribute('aria-label', labels.open + (picture.alt ? ': ' + picture.alt : ''));
  opener.setAttribute('aria-haspopup', 'dialog'); opener.title = labels.open;
  opener.addEventListener('click', event => {
   event.preventDefault(); trigger = opener;
   image.src = picture.currentSrc || picture.src; image.alt = picture.alt;
   caption.textContent = picture.alt || labels.open;
   setZoom(false); viewer.showModal(); document.body.classList.add('image-viewer-open'); close.focus();
  });
 });
}
})();
