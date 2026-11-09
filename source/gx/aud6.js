const { chromium } = require('/opt/npm-tools/node_modules/playwright');
const fs=require('fs');
(async()=>{const b=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});
const p=await b.newPage({viewport:{width:1100,height:1000}});
await p.goto('file://'+process.env.FILE,{waitUntil:'load',timeout:180000});await p.waitForTimeout(2000);
const out=[];
for(const lp of JSON.parse(process.env.LPS)){
 const r=await p.evaluate(async(lp)=>{const res=[];const seen=new Set();
 for(const g of ['TK','K','1','2']){
  for(const [check,subj] of [['essential','ela'],['essential','math'],['essential','science'],['essential','social'],['essential','writing']]){
   try{await TP._debug.start({lp,grade:g,subj,check,picked:[],lvOff:false})}catch(e){continue}
   for(const st of TP._debug.ROUTE){
    TP._debug.openStop(st.id);await new Promise(r=>setTimeout(r,8));
    const d=document.querySelector('#stopView details.teacher');const top=d?d.querySelector(':scope > .teach'):null;
    const ol=top?top.querySelector(':scope > ol'):null;const lis=ol?[...ol.querySelectorAll(':scope > li')]:[];
    const parts=st.lv?[st]:st.parts;
    parts.forEach((pt,i)=>{
     const key=[lp,g,st.id,pt.title||st.title].join('|');if(seen.has(key))return;seen.add(key);
     let html='',fig='';try{html=pt.html?pt.html():''}catch(e){}try{fig=pt.fig?pt.fig():''}catch(e){}
     const all=html+' '+fig;
     const sv=[...all.matchAll(/<text[^>]*>([\s\S]*?)<\/text>/g)].map(m=>m[1].replace(/<[^>]+>/g,' ')).join(' ').replace(/\s+/g,' ').trim();
     const ft=(fig).replace(/<svg[\s\S]*?<\/svg>/g,' ').replace(/<[^>]+>/g,' ').replace(/\s+/g,' ').trim();const panel=ol?(lis[i]?lis[i].textContent.replace(/\s+/g,' ').trim():''):(top?top.textContent.replace(/\s+/g,' ').trim():'');
     res.push({lp,g,stop:st.num,title:pt.title||st.title,std:(pt.std||st.std||[]),kind:pt.kind||'',dir:String(pt.dir||st.dir||''),svgwords:sv.split(' ').filter(Boolean).length,svg:sv.slice(0,200),figtext:ft.slice(0,200),figwords:ft.split(' ').filter(Boolean).length,panel:panel.slice(0,500)})})}}}
 return res},lp);out.push(...r)}
fs.writeFileSync(process.env.OUT,JSON.stringify(out));console.log(out.length);await b.close()})();
