const { chromium } = require('/opt/npm-tools/node_modules/playwright');
(async()=>{const b=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});
const p=await b.newPage({viewport:{width:1100,height:1000}});
await p.goto('file://'+process.env.FILE,{waitUntil:'load',timeout:120000});await p.waitForTimeout(1500);
const r=await p.evaluate(async()=>{const o=[];for(const subj of ['ela','math']){
await TP._debug.start({lp:1,grade:'1',subj,check:'essential',lvOff:true});
const R=TP._debug.ROUTE.filter(s=>!s.lv);o.push(subj+' stops: '+R.map(s=>s.num+'='+s.title).join(' | '));
const st=R.find(s=>s.num===7);if(!st)continue;
o.push(JSON.stringify(st.parts.map(p=>({title:p.title,std:p.std,kind:p.kind,dir:p.dir,desc:p.desc,teach:p.teach,qs:p.qs,html:p.html?String(p.html()).replace(/<[^>]+>/g,' ').slice(0,900):null,key:p.key})),null,1));
TP._debug.openStop(st.id);await new Promise(r=>setTimeout(r,300));
o.push('TEACHER NOTE: '+document.querySelector('#stopView details.teacher')?.innerText.slice(0,1800))}
return o});
r.forEach(x=>console.log(x));await b.close()})();
