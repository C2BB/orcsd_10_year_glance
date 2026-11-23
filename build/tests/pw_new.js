const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1200,height:900},deviceScaleFactor:1});
await p.goto('file://'+process.argv[2]+'#grad');await p.waitForTimeout(1500);
const t=await p.evaluate(()=>['grad','part'].map(k=>{const s=document.querySelector('[data-k='+k+']');return [k,s&&s.querySelector('[data-draw=label-'+k+']').innerText.replace(/\n/g,' | '),s&&s.querySelectorAll('svg circle, svg path').length]}));
console.log(JSON.stringify(t));
console.log(await p.evaluate(()=>document.querySelectorAll('section.os-row').length));
const el=await p.$('[data-k=grad]');await el.screenshot({path:process.argv[3]+'/grad.png'});
const el2=await p.$('[data-k=part]');await el2.screenshot({path:process.argv[3]+'/part.png'});
await b.close()})();
