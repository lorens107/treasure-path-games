const { chromium } = require('/opt/npm-tools/node_modules/playwright');
const fs=require('fs');
(async()=>{const b=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});
const p=await b.newPage({viewport:{width:1100,height:1000}});
await p.goto('file://'+process.env.FILE,{waitUntil:'load',timeout:180000});await p.waitForTimeout(2000);
const out=[];
for(const lp of JSON.parse(process.env.LPS)){
 const r=await p.evaluate(async(lp)=>{const res=[];const seen=new Set();
 const strip=h=>String(h||'').replace(/<svg[\s\S]*?<\/svg>/g,' ').replace(/<img[^>]*>/g,' ').replace(/<[^>]+>/g,' ').replace(/&nbsp;/g,' ').replace(/\s+/g,' ').trim();
 for(const g of ['TK','K','1','2','3','4','5','6','7','8']){
  for(const subj of ['ela','math','science','social','writing']){
   try{await TP._debug.start({lp,grade:g,subj,check:'essential',picked:[],lvOff:false})}catch(e){continue}
   for(const st of TP._debug.ROUTE){
    const parts=st.lv?[st]:st.parts;
    parts.forEach(pt=>{
     const key=[g,(pt.std||st.std||[]).join(),pt.title||st.title,pt.desc||''].join('|');if(seen.has(key))return;seen.add(key);
     let html='';try{html=pt.html?pt.html():''}catch(e){}
     res.push({lp,g,lv:!!st.lv,title:pt.title||st.title,std:(pt.std||st.std||[]),kind:pt.kind||'',desc:String(pt.desc||''),dir:String(pt.dir||st.dir||''),text:strip(html).slice(0,160),qs:(pt.qs||[]).slice(0,2).map(strip),key:(pt.key||[]).slice(0,2).map(x=>String(x).slice(0,200))})})}}}
 return res},lp);out.push(...r)}
fs.writeFileSync(process.env.OUT,JSON.stringify(out));console.log(out.length);await b.close()})();
