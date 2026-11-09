const { chromium } = require('/opt/npm-tools/node_modules/playwright');
(async()=>{const b=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});
const p=await b.newPage({viewport:{width:1100,height:600}});const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.goto('file://'+process.env.FILE,{waitUntil:'load',timeout:120000});await p.waitForTimeout(1500);
const res=await p.evaluate(async()=>{const out=[];
for(const g of ['TK','K','1','2','3','4','5','6','7','8']){for(const subj of ['ela','math']){
 try{await TP._debug.start({lp:1,grade:g,subj,check:'essential'});}catch(e){out.push([g,subj,'ERR '+e.message]);continue}
 await new Promise(r=>setTimeout(r,80));
 const goal=document.querySelector('#goal');const im=goal&&goal.querySelector('image');
 out.push([g,subj,!!goal,im?im.getAttribute('href').slice(0,60)+'..'+im.getAttribute('href').length:'NO IMAGE', goal?goal.querySelectorAll('path,rect').length:0]);
 TP._debug.S.done=TP._debug.ROUTE.filter(s=>!s.lv).map(s=>s.id);document.getElementById('mapBtn').click();await new Promise(r=>setTimeout(r,80));
 const g2=document.querySelector('#goal image');out.push(['  alldone',g2?g2.getAttribute('href').length:'NO IMAGE'])}}
return out});
res.forEach(r=>console.log(JSON.stringify(r)));console.log(errs);await b.close()})();
