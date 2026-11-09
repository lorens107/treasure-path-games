const { chromium } = require('/opt/npm-tools/node_modules/playwright');
const fs=require('fs');
(async()=>{const b=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});
const p=await b.newPage({viewport:{width:1100,height:1000}});const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.goto('file://'+process.env.FILE,{waitUntil:'load',timeout:180000});await p.waitForTimeout(2000);
const out=[];
for(const lp of JSON.parse(process.env.LPS)){
 const r=await p.evaluate(async(lp)=>{const res=[];
 for(const g of ['TK','K','1','2']){for(const subj of ['ela','math','science','social','writing']){
  try{await TP._debug.start({lp,grade:g,subj,check:'essential',lvOff:false});}catch(e){continue}
  for(const st of TP._debug.ROUTE){
   TP._debug.openStop(st.id);await new Promise(r=>setTimeout(r,15));
   const notes=[...document.querySelectorAll('#stopView details.teacher .tn-grid, #stopView details.teacher')].map(x=>x.innerText).join('\n').slice(0,3000);
   const parts=st.lv?[st]:st.parts;
   parts.forEach(pt=>res.push({lp,g,subj,title:pt.title||st.title,std:(pt.std||st.std||[]).join(','),dir:String(pt.dir||st.dir||''),teach:(notes.match(/The student is not expected[^.]*\./)||[''])[0]?1:0}))}}}
 return res},lp);out.push(...r)}
fs.writeFileSync(process.env.OUT,JSON.stringify(out));console.log(out.length,errs.slice(0,3));await b.close()})();
