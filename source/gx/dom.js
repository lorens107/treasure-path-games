const { chromium } = require('/opt/npm-tools/node_modules/playwright');
(async()=>{const b=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});
const p=await b.newPage({viewport:{width:1100,height:1000}});
await p.goto('file://'+process.env.FILE,{waitUntil:'load',timeout:120000});await p.waitForTimeout(1500);
const r=await p.evaluate(async()=>{await TP._debug.start({lp:1,grade:'1',subj:'ela',check:'essential',lvOff:true});
const st=TP._debug.ROUTE.find(s=>s.title==='Animal Facts');TP._debug.openStop(st.id);await new Promise(r=>setTimeout(r,300));
return document.querySelector('#stopView details.teacher').innerHTML.slice(0,3500)});
console.log(r);await b.close()})();
