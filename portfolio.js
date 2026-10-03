'use strict';
const projects=JSON.parse(document.getElementById('portfolio-data').textContent);
const cases=JSON.parse(document.getElementById('case-data').textContent);
const cards=[...document.querySelectorAll('.work-card')];
const search=document.getElementById('project-search');
const filters=[...document.querySelectorAll('[data-filter]')];
const more=document.getElementById('show-more');
const reset=document.getElementById('reset-filters');
let category='All projects',expanded=false;
function updateGallery(){
 const term=search.value.trim().toLowerCase();
 const matched=cards.filter(card=>{const data=projects.find(p=>p.id===card.dataset.project);return(category==='All projects'||data.category===category)&&[data.title,data.description,...data.tags].join(' ').toLowerCase().includes(term)});
 const limit=expanded||category!=='All projects'||term?matched.length:6;
 cards.forEach(card=>card.hidden=!matched.includes(card)||matched.indexOf(card)>=limit);
 const visible=Math.min(limit,matched.length);
 document.getElementById('result-count').textContent=`Showing ${visible} of ${matched.length} projects`;
 document.getElementById('no-results').hidden=matched.length>0;
 more.hidden=visible===matched.length;
 more.textContent=`Show all ${matched.length} projects ↓`;
 reset.hidden=!term&&category==='All projects';
 filters.forEach(button=>{const active=button.dataset.filter===category;button.classList.toggle('active',active);button.setAttribute('aria-pressed',String(active))});
}
filters.forEach(b=>b.addEventListener('click',()=>{category=b.dataset.filter;expanded=false;updateGallery()}));
search.addEventListener('input',()=>{expanded=false;updateGallery()});
more.addEventListener('click',()=>{expanded=true;updateGallery()});
reset.addEventListener('click',()=>{category='All projects';search.value='';expanded=false;updateGallery();search.focus()});
updateGallery();
const menu=document.getElementById('menu-toggle'),nav=document.getElementById('navigation');
function closeMenu(){nav.classList.remove('open');menu.setAttribute('aria-expanded','false');menu.setAttribute('aria-label','Open menu');menu.textContent='☰'}
menu.addEventListener('click',()=>{const open=nav.classList.toggle('open');menu.setAttribute('aria-expanded',String(open));menu.setAttribute('aria-label',open?'Close menu':'Open menu');menu.textContent=open?'×':'☰'});
nav.querySelectorAll('a').forEach(a=>a.addEventListener('click',closeMenu));
document.addEventListener('keydown',e=>{if(e.key==='Escape')closeMenu()});
const theme=document.getElementById('theme-toggle');
function updateThemeLabel(){theme.setAttribute('aria-label',document.documentElement.dataset.theme==='dark'?'Switch to light theme':'Switch to dark theme')}
theme.addEventListener('click',()=>{const next=document.documentElement.dataset.theme==='dark'?'light':'dark';document.documentElement.dataset.theme=next;try{localStorage.setItem('portfolio-theme',next)}catch(e){}updateThemeLabel()});updateThemeLabel();
const dialog=document.getElementById('project-dialog'),content=document.getElementById('dialog-content');let opener;
function el(tag,text,cls){const node=document.createElement(tag);if(text)node.textContent=text;if(cls)node.className=cls;return node}
function image(src,alt,cls){const node=el('img',null,cls);node.src=src;node.alt=alt;return node}
function link(label,url){const node=el('a',label+' ↗','button secondary');node.href=url;if(url.startsWith('http')){node.target='_blank';node.rel='noopener noreferrer'}return node}
function showDetails(data,trigger,isCase=false){
 opener=trigger;content.replaceChildren();document.getElementById('dialog-category').textContent=isCase?'Professional case study':data.category;
 const heading=el('h2',data.title);heading.id='dialog-title';content.append(heading);
 if(data.image)content.append(image(data.image,data.alt,isCase?'case-dialog-image':''));
 if(isCase){content.append(el('p',data.description));content.append(el('p','A selected map from professional work. Project facts shown here follow the existing portfolio; client-sensitive details are omitted.','evidence-note'));const actions=el('div',null,'dialog-links');actions.append(link('Open full-resolution map',data.image));content.append(actions)}
 else{
  data.paragraphs.forEach(text=>content.append(el('p',text)));
  if(data.points.length){const list=el('ul');data.points.forEach(text=>list.append(el('li',text)));content.append(list)}
  const actions=el('div',null,'dialog-links');data.links.forEach(item=>actions.append(link(item.label,item.url)));content.append(actions);
 }
 const tags=el('div',null,'tags');data.tags.forEach(tag=>tags.append(el('span',tag)));content.append(tags);dialog.showModal();document.getElementById('dialog-close').focus();
}
document.querySelectorAll('[data-detail]').forEach(button=>button.addEventListener('click',()=>showDetails(projects.find(p=>p.id===button.dataset.detail),button)));
document.querySelectorAll('[data-case]').forEach(button=>button.addEventListener('click',()=>showDetails(cases.find(p=>p.id===button.dataset.case),button,true)));
document.getElementById('dialog-close').addEventListener('click',()=>dialog.close());
dialog.addEventListener('click',event=>{const r=dialog.getBoundingClientRect();if(event.target===dialog&&(event.clientX<r.left||event.clientX>r.right||event.clientY<r.top||event.clientY>r.bottom))dialog.close()});
dialog.addEventListener('close',()=>{if(opener)opener.focus()});
document.getElementById('print-portfolio').addEventListener('click',()=>window.print());
const navObserver=new IntersectionObserver(entries=>{entries.forEach(entry=>{if(entry.isIntersecting){nav.querySelectorAll('a').forEach(a=>{const current=a.hash==='#'+entry.target.id;a.classList.toggle('active',current);if(current)a.setAttribute('aria-current','location');else a.removeAttribute('aria-current')})}})},{rootMargin:'-15% 0px -60% 0px'});['work','about','experience','contact'].forEach(id=>navObserver.observe(document.getElementById(id)));
document.querySelectorAll('.work-image img').forEach(img=>img.addEventListener('error',()=>{const label=el('div',img.alt||'Project preview','project-placeholder');img.replaceWith(label)}));
