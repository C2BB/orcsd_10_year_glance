const {chromium}=require('playwright');
(async()=>{
 const b=await chromium.launch(); const p=await b.newPage({viewport:{width:1300,height:900}});
 const errs=[]; p.on('pageerror',e=>errs.push(String(e))); p.on('console',m=>{if(m.type()==='error')errs.push(m.text())});
 await p.goto('file://'+process.argv[2]); await p.waitForTimeout(2500);
 const rows=await p.evaluate(()=>document.querySelectorAll('[class*=row]').length);
 console.log('rows',rows,'errors',JSON.stringify(errs));
 await b.close();
})();
