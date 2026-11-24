const {chromium}=require('playwright');
(async()=>{
 const b=await chromium.launch();
 for (const f of process.argv.slice(2)) {
  const p=await b.newPage({viewport:{width:1300,height:1000}});
  await p.goto('file://'+f); await p.waitForTimeout(3000);
  console.log(f.slice(-45), JSON.stringify(await p.evaluate(()=>{const n=document.querySelector('details.os-notes');const chain=[];let e=n;while(e&&e!==document.body){chain.push(e.tagName+'.'+e.className);e=e.parentElement;}
   const os=document.querySelector('.os');return {chain,insideOs:os.contains(n),osChildren:[...os.children].map(c=>c.tagName+'.'+c.className).slice(-6),rowsInsideMore:document.querySelector('details.os-more')?document.querySelector('details.os-more').querySelectorAll('section.os-row').length:null,font:getComputedStyle(os).fontFamily.slice(0,30)}})));
  await p.close();
 }
 await b.close();
})();
