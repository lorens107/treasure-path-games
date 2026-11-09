const { chromium } = require('/opt/npm-tools/node_modules/playwright');
(async()=>{const b=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});
const p=await b.newPage({viewport:{width:1100,height:1300}});const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.goto('file://'+process.env.FILE,{waitUntil:'load',timeout:120000});await p.waitForTimeout(1500);
const r=await p.evaluate(async([g,lp,subj,title])=>{await TP._debug.start({lp,grade:g,subj,check:'essential',lvOff:true});
const st=TP._debug.ROUTE.find(s=>!s.lv&&(s.title===title||s.parts.some(p=>p.title===title)));TP._debug.openStop(st.id);await new Promise(r=>setTimeout(r,300));
const d=document.querySelector('#stopView details.teacher');d.open=true;
return {dir:[...document.querySelectorAll('#stopView .dir')].map(x=>x.textContent.trim()),teacher:d.innerText.slice(0,900)}},JSON.parse(process.env.ARGS));
console.log(JSON.stringify(r,null,1),errs);await p.screenshot({path:process.env.OUT});await b.close()})();
