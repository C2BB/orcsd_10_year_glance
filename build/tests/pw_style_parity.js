const {chromium}=require('playwright');
(async()=>{
 const b=await chromium.launch();
 const props=['fontFamily','fontSize','fontWeight','color','marginTop','marginBottom','lineHeight','display','paddingTop'];
 const sel=['.os-name','.os-big','.os-sub','.os-delta','.os-tag','.os-src','.os-legend','.os-chip-row','.os-row','.os-label','.os-vis','.os-h2','.os-intro','.os-head','.os-notes','.os-adjust','.os-ctl','.os-toc'];
 async function grab(url){
  const p=await b.newPage({viewport:{width:1300,height:1000}});
  await p.goto(url); await p.waitForTimeout(3000);
  const r=await p.evaluate(([sel,props])=>{const o={};sel.forEach(s=>{const e=document.querySelector('[data-k="spend"] '+s)||document.querySelector(s);if(e){const c=getComputedStyle(e);o[s]=props.map(k=>c[k]).join(' | ');}});return o;},[sel,props]);
  await p.close(); return r;
 }
 const A=await grab('file://'+process.argv[2]), N=await grab('file://'+process.argv[3]);
 for (const s of sel) if (A[s]!==N[s]) console.log('DIFF',s,'\n   old:',A[s],'\n   new:',N[s]);
 console.log('compared',sel.length,'selectors');
 await b.close();
})();
