const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1100,height:900}});const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.goto('file://'+process.argv[2]);await p.waitForTimeout(1500);
for(const i of [7,8]){console.log(await p.evaluate(i=>{const s=document.querySelector('[data-k=susp]');s.querySelectorAll('rect.hit')[i].dispatchEvent(new PointerEvent('pointerenter'));return s.querySelector('.os-tip').innerText.replace(/\n/g,' | ')},i))}
await p.click('.os-yr[data-i="8"]');await p.waitForTimeout(500);console.log(await p.evaluate(()=>document.querySelector('[data-draw=label-susp]').innerText.replace(/\n/g,' | ')),errs);await b.close()})();
