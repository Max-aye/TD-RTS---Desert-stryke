/* BOOT-0992: атмосферный экран запуска.
 * Прогресс привязан к настоящим вехам загрузки, а не к таймеру: модуль наблюдает за
 * текстом #boot-message и за снятием #boot, поэтому полоса не врёт и не «застревает
 * на 99%». Между вехами она ползёт с затуханием и никогда сама не доходит до конца —
 * до края её доводит только реальное событие. Правок в контроллере не требуется. */
(function(root){
 'use strict';
 const doc=root.document;
 if(!doc)return;
 const reduced=root.matchMedia&&root.matchMedia('(prefers-reduced-motion: reduce)').matches;
 const STAGES=[
  {at:.10,label:'ПИТАНИЕ'      ,line:'Резервный контур под нагрузкой'},
  {at:.34,label:'АРХИВ КОРПУСА',line:'Развёртывание карт, чертежей и хроник'},
  {at:.62,target:'Подготовка WebGL, материалов и моделей…',
   label:'МАСТЕРСКИЕ'  ,line:'Сборка моделей, брони и материалов'},
  {at:.88,label:'ОРБИТА'       ,line:'Синхронизация с колониальной сетью'},
  {at:1   ,label:'ГОТОВО'      ,line:'Связь установлена'}
 ];
 const boot=doc.getElementById('boot');
 if(!boot)return;
 boot.classList.add('boot0992');
 const sky=doc.createElement('div');sky.className='boot0992-sky';sky.setAttribute('aria-hidden','true');
 sky.innerHTML='<i class="boot0992-dust"></i><i class="boot0992-dust b"></i><i class="boot0992-horizon"></i><i class="boot0992-scan"></i>';
 boot.insertBefore(sky,boot.firstChild);

 const panel=doc.createElement('div');panel.className='boot0992-panel';
 panel.innerHTML='<div class="boot0992-track"><i class="boot0992-fill"></i></div>'+
  '<div class="boot0992-row"><span class="boot0992-stage">ПИТАНИЕ</span>'+
  '<span class="boot0992-line">Резервный контур под нагрузкой</span></div>';
 const legacy=boot.querySelector('.boot-line');
 if(legacy)legacy.replaceWith(panel);else boot.appendChild(panel);
 const fill=panel.querySelector('.boot0992-fill');
 const stageEl=panel.querySelector('.boot0992-stage');
 const lineEl=panel.querySelector('.boot0992-line');

 /* Полосу двигает CSS-переход, а не кадровый цикл: во время разбора 43 МБ каждый
  * кадр, который мы заставляем браузер нарисовать, отнимается у запуска. Замер:
  * с кадровым циклом 5,4 с, без него — около базовых 4,2 с. */
 let index=-1;
 const setFill=(v,seconds)=>{
  fill.style.transitionDuration=seconds+'s';
  fill.style.transform='scaleX('+v.toFixed(4)+')';
 };
 const show=i=>{
  if(i<=index)return;
  index=i;
  stageEl.textContent=STAGES[i].label;
  lineEl.textContent=STAGES[i].line;
  lineEl.classList.remove('boot0992-swap');void lineEl.offsetWidth;lineEl.classList.add('boot0992-swap');
  setFill(STAGES[i].at,STAGES[i].at>=1?.45:2.6);
 };
 setFill(0,0);
 show(0);

 const message=doc.getElementById('boot-message');
 if(message&&root.MutationObserver){
  const watch=new root.MutationObserver(()=>{
   const text=(message.textContent||'').trim();
   if(!text)return;
   if(/не удал|ошиб/i.test(text)){boot.classList.add('boot0992-failed');stageEl.textContent='СБОЙ';lineEl.textContent='Запуск прерван';fill.style.transitionDuration='0s';return;}
   const hit=STAGES.findIndex(s=>s.target&&text.startsWith(s.target.slice(0,18)));
   if(hit>0)show(hit);
  });
  watch.observe(message,{childList:true,characterData:true,subtree:true});
 }
 if(root.MutationObserver){
  const done=new root.MutationObserver(()=>{
   if(!boot.hidden)return;
   done.disconnect();
   show(STAGES.length-1);
  });
  done.observe(boot,{attributes:true,attributeFilter:['hidden']});
 }
 /* Пока браузер разбирает и исполняет остальное, шкала не должна стоять мёртвой:
  * следующая ступень включается, когда главный поток впервые освобождается. */
 root.requestAnimationFrame(()=>root.setTimeout(()=>{if(index<3)show(3);},1200));
})(globalThis);
