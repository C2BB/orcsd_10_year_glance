const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1100,height:900}});const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.goto('file://'+process.argv[2]);await p.waitForTimeout(1500);
const el=await p.$('[data-k=cpay]');
for(const i of [0,4,7,8,9]){await p.click('.os-yr[data-i="'+i+'"]');await p.waitForTimeout(200);console.log(i,await p.evaluate(()=>document.querySelector('[data-k=cpay] [data-draw=label-cpay]').innerText.replace(/\n/g,' | ')));}
await p.click('.os-yr[data-i="6"]');await el.scrollIntoViewIfNeeded();const box=await el.boundingBox();await p.mouse.move(box.x+box.width*0.6,box.y+box.height*0.5);await p.waitForTimeout(400);
console.log(await p.evaluate(()=>document.querySelector('.os-tip')?document.querySelector('.os-tip').innerText:'no tip'));
await el.screenshot({path:'/tmp/w/shots/cpay.png'});console.log(await p.evaluate(()=>document.querySelectorAll('section.os-row').length),errs);await b.close()})();
