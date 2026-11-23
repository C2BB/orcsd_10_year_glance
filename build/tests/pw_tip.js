const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1200,height:900}});const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.goto('file://'+process.argv[2]);await p.waitForTimeout(1500);
async function tip(k){return p.evaluate(k=>{const s=document.querySelector('[data-k='+k+']');const hs=s.querySelectorAll('rect.hit');hs[2].dispatchEvent(new PointerEvent('pointerenter'));const t=s.querySelector('.os-tip');return t.innerText.replace(/\n/g,' | ').slice(0,700)},k)}
for(const k of ['share','efa','cred','eff','local']){const a=await tip(k);await p.click('.os-md[data-m=cpi]');await p.waitForTimeout(500);const c=await tip(k);await p.click('.os-md[data-m=nom]');await p.waitForTimeout(300);console.log(k,'\n NOM',a,'\n CPI',c)}
console.log(errs);await b.close()})();
