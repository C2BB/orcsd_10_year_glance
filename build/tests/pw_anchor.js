const {chromium}=require('playwright');
(async()=>{
 const b=await chromium.launch(); const url=process.argv[2];
 for (const [w,h] of [[1200,'#att'],[390,'#town-shares'],[1200,'#notes-attendance'],[1200,'#sources']]){
  const p=await b.newPage({viewport:{width:w,height:800}}); const errs=[]; p.on('pageerror',e=>errs.push(String(e)));
  await p.goto(url+h); await p.waitForTimeout(2500);
  const r=await p.evaluate(()=>{const id=decodeURIComponent(location.hash.slice(1)); const el=document.getElementById(id==='sources'?'os-sources':id); const rc=el&&el.getBoundingClientRect(); const d=el&&el.closest('details'); return {found:!!el, top:rc&&Math.round(rc.top), open:d?d.open:null, ids:document.querySelectorAll('[data-anchor]').length, anchors:document.querySelectorAll('.os-anchor').length, toc:document.querySelectorAll('.os-toc a').length, dup:(()=>{const m={};document.querySelectorAll('[id]').forEach(e=>m[e.id]=(m[e.id]||0)+1);return Object.entries(m).filter(x=>x[1]>1)})(), lab:document.querySelector('section[data-k=att]').getAttribute('aria-labelledby'), name:(document.getElementById(document.querySelector('section[data-k=att]').getAttribute('aria-labelledby'))||{}).textContent}});
  console.log(w,h,JSON.stringify(r),JSON.stringify(errs.filter(e=>!/TUNNEL/.test(e))));
  await p.close();
 }
 // click anchor test
 const p=await b.newPage({viewport:{width:1200,height:800}}); await p.goto(url); await p.waitForTimeout(2000);
 await p.hover('section[data-k=ela] .os-name'); await p.click('section[data-k=ela] .os-anchor'); await p.waitForTimeout(600);
 console.log('after click', await p.evaluate(()=>location.hash));
 await p.screenshot({path:'/tmp/claude-0/-home-claude/fc466538-ee33-5166-af07-beda00a94393/scratchpad/shots/anchor.png'});
 await b.close();
})();
