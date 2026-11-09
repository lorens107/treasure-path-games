const { chromium } = require('/opt/npm-tools/node_modules/playwright');
const fs=require('fs');
(async()=>{const b=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});
const p=await b.newPage({viewport:{width:1100,height:1000}});
await p.goto('file://'+process.env.FILE,{waitUntil:'load',timeout:180000});await p.waitForTimeout(2000);
console.log(await p.evaluate(()=>[...document.querySelectorAll('#suSubj option')].map(o=>o.value).join(',')));
const out=[];
for(const lp of [6,7,8,9,10]){
 const r=await p.evaluate(async(lp)=>{const res=[];
 for(const g of ['TK','K','1','2']){for(const subj of ['ela','math','science','history','social']){
  try{await TP._debug.start({lp,grade:g,subj,check:'essential',lvOff:false});}catch(e){continue}
  for(const st of TP._debug.ROUTE){const parts=st.lv?[st]:st.parts;
   parts.forEach((pt,i)=>{let html='';try{html=pt.html?String(pt.html()):''}catch(e){}
    const dir=String(pt.dir||st.dir||'');
    res.push({lp,g,subj,stop:st.num||'LV',title:pt.title||st.title,std:(pt.std||st.std||[]).join(','),kind:pt.kind||'',dir,hasRead:!!pt.read,html:html.replace(/<svg[\s\S]*?<\/svg>/g,'').replace(/<[^>]+>/g,' ').replace(/\s+/g,' ').trim().slice(0,400),nq:(pt.qs||[]).length})})}}}
 return res},lp);out.push(...r)}
fs.writeFileSync(process.env.OUT,JSON.stringify(out));console.log(out.length);await b.close()})();
