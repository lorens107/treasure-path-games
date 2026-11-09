const { chromium } = require('/opt/npm-tools/node_modules/playwright');
(async()=>{const b=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});
const p=await b.newPage({viewport:{width:1100,height:1000}});
await p.goto('file://'+process.env.FILE,{waitUntil:'load',timeout:180000});await p.waitForTimeout(1500);
const r=await p.evaluate(async()=>{await TP._debug.start({lp:1,grade:'TK',subj:'ela',check:'essential',picked:[],lvOff:false});
const out=[];for(const st of TP._debug.ROUTE.slice(0,4)){TP._debug.openStop(st.id);await new Promise(r=>setTimeout(r,20));
const d=document.querySelector('#stopView details.teacher');out.push({t:st.title,html:d?d.innerHTML.slice(0,1500):null,parts:(st.parts||[]).length})}return out});
console.log(JSON.stringify(r,null,1));await b.close()})();
