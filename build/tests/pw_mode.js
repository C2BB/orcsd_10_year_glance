const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1200,height:900}});
await p.goto('file://'+process.argv[2]);await p.waitForTimeout(1500);
const keys=await p.evaluate(()=>[...document.querySelectorAll('section.os-row')].map(s=>s.dataset.k));
async function snap(){return p.evaluate(()=>{const o={};document.querySelectorAll('section.os-row').forEach(s=>{const k=s.dataset.k;o[k]=[(s.querySelector('[data-draw=label-'+k+']')||{}).innerText||'', (s.querySelector('.os-chart')||{}).innerText||'', (s.querySelector('.os-name')||{}).innerText||''].join(' ## ')});return o})}
const A=await snap();
await p.click('.os-md[data-m=cpi]');await p.waitForTimeout(800);const B=await snap();
await p.click('.os-md[data-m=eci]');await p.waitForTimeout(800);const C=await snap();
const rows=[];
for(const k of keys){const dollar=/\$/.test(A[k]);const ch=A[k]!==B[k];rows.push([k,A[k].split(' ## ')[2].slice(0,48),dollar?'$':'-',ch?'ADJ':'same',(A[k].split(' ## ')[0].replace(/\n/g,' ')).slice(0,60)])}
console.log(rows.filter(r=>r[2]==='$'||r[3]==='ADJ').map(r=>r.join(' | ')).join('\n'));
await b.close()})();
