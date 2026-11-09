const { chromium } = require('/opt/npm-tools/node_modules/playwright');
const fs=require('fs');
(async()=>{const b=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});
const p=await b.newPage({viewport:{width:1100,height:1000}});const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.goto('file://'+process.env.FILE,{waitUntil:'load',timeout:180000});await p.waitForTimeout(2000);
const out=[];
for(const lp of JSON.parse(process.env.LPS)){
 const r=await p.evaluate(async(lp)=>{const res=[];const seen=new Set();
 const strip=h=>String(h||'').replace(/<svg[\s\S]*?<\/svg>/g,' ').replace(/<img[^>]*>/g,' ').replace(/<[^>]+>/g,' ').replace(/&nbsp;/g,' ').replace(/\s+/g,' ').trim();
 for(const g of ['TK','K','1','2']){
  const modes=[['essential','ela'],['essential','math'],['essential','science'],['essential','social'],['essential','writing'],['pick','both']];
  for(const [check,subj] of modes){
   try{
    let picked=[];
    if(check==='pick'){await TP._debug.start({lp,grade:g,subj,check:'pick',picked:[],lvOff:false});picked=[...document.querySelectorAll('#pickList [data-std]')].map(e=>e.dataset.std)}
    await TP._debug.start({lp,grade:g,subj,check,picked,lvOff:false});
   }catch(e){continue}
   for(const st of TP._debug.ROUTE){
    TP._debug.openStop(st.id);await new Promise(r=>setTimeout(r,8));
    const d=document.querySelector('#stopView details.teacher');const lis=d?[...d.querySelectorAll(':scope > .teach > ol > li')]:[];
    const parts=st.lv?[st]:st.parts;
    parts.forEach((pt,i)=>{
     const key=[lp,g,st.id,pt.title||st.title,(pt.std||st.std||[]).join()].join('|');if(seen.has(key))return;seen.add(key);
     let html='';try{html=pt.html?pt.html():''}catch(e){}
     let fig='';try{fig=pt.fig?pt.fig():''}catch(e){}
     const li=lis[i];const lines=li?[...li.querySelectorAll(':scope > ul > li')].map(x=>x.textContent.trim()):[];
     res.push({lp,g,subj,check,stop:st.lv?'LV':st.num,title:pt.title||st.title,std:(pt.std||st.std||[]),kind:pt.kind||'',dir:String(pt.dir||st.dir||''),
       text:strip(html),qs:(pt.qs||[]).map(strip),words:(pt.words||[]).slice(0,40).map(String),hasRead:!!pt.read,read:strip(pt.read&&typeof pt.read==='function'?pt.read():pt.read).slice(0,100),
       hasRender:!!pt.render,teach:lines.slice(0,4)})})}}}
 return res},lp);out.push(...r);console.log('lp',lp,r.length)}
fs.writeFileSync(process.env.OUT,JSON.stringify(out));console.log(out.length,errs.slice(0,3));await b.close()})();
