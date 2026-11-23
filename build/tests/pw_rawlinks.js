// Every "repo copy" link on the page (all ten years) must point at a file listed in raw/MANIFEST.csv.
// usage: node pw_rawlinks.js <dist html> <MANIFEST.csv>
const {chromium}=require('playwright'); const fs=require('fs');
// stored_as is column 5; parse CSV with quotes
function parse(t){const rows=[];let r=[],f='',q=false;for(let i=0;i<t.length;i++){const c=t[i];if(q){if(c==='"'){if(t[i+1]==='"'){f+='"';i++}else q=false}else f+=c}else if(c==='"')q=true;else if(c===','){r.push(f);f=''}else if(c==='\n'){r.push(f);rows.push(r);r=[];f=''}else f+=c}return rows}
const man=new Set(parse(fs.readFileSync(process.argv[3],'utf8')).slice(1).map(r=>r[4]));
(async()=>{
 const b=await chromium.launch(); const p=await b.newPage({viewport:{width:1300,height:900}});
 const errs=[]; p.on('pageerror',e=>errs.push(String(e)));
 await p.goto('file://'+process.argv[2]); await p.waitForTimeout(2500);
 const seen=new Set(); let bad=0, total=0;
 for(let i=0;i<10;i++){
  await p.click('.os-yr[data-i="'+i+'"]'); await p.waitForTimeout(500);
  const hrefs=await p.evaluate(()=>[...document.querySelectorAll('a.rawcopy')].map(a=>a.getAttribute('href')));
  for(const h of hrefs){ total++; const f=h.split('/raw/')[1]; seen.add(f); if(!man.has(f)){bad++; console.log('NOT IN MANIFEST',i,f);} }
 }
 console.log('repo-copy links',total,'distinct files',seen.size,'missing from manifest',bad,'errors',JSON.stringify(errs));
 await b.close(); process.exit(bad||errs.length?1:0);
})();
