const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1100,height:900}});const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.goto('file://'+process.argv[2]);await p.waitForTimeout(1500);
for(const k of ['cslr','cert','swd']){const el=await p.$('[data-k='+k+']');console.log(k,(await p.evaluate(k=>document.querySelector('[data-k='+k+'] [data-draw=label-'+k+']').innerText.replace(/\n/g,' | '),k)));await el.screenshot({path:process.argv[3]+'/n_'+k+'.png'})}
console.log(await p.evaluate(()=>document.querySelectorAll('section.os-row').length),errs);await b.close()})();
