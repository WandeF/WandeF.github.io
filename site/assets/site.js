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
})();
