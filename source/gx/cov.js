const { chromium } = require('/opt/npm-tools/node_modules/playwright');
(async()=>{const b=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});
const p=await b.newPage({viewport:{width:1100,height:1000}});const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.goto('file://'+process.env.FILE,{waitUntil:'load',timeout:180000});await p.waitForTimeout(2000);
const res=await p.evaluate(async(lps)=>{const out={checked:0,needs:0,missing:[],other:[]};
for(const lp of lps){for(const g of ['TK','K','1','2']){for(const subj of ['ela','math','science','social','writing']){
 try{await TP._debug.start({lp,grade:g,subj,check:'essential',lvOff:false});}catch(e){continue}
 for(const st of TP._debug.ROUTE){TP._debug.openStop(st.id);await new Promise(r=>setTimeout(r,10));
  const d=document.querySelector('#stopView details.teacher');if(!d)continue;d.open=true;const txt=d.innerText;
  const parts=st.lv?[st]:st.parts;
  parts.forEach(pt=>{out.checked++;
   if(window.GXreadsText(pt,g,fn=>fn())){out.needs++;
    const ok=/read the text on the screen aloud|Read aloud to the student|Say each prompt/.test(txt);
    if(!ok)out.missing.push([lp,g,subj,pt.title||st.title,(pt.dir||'').slice(0,60)])}
   if(/student reads the text on their own/.test(txt)&&!['RF'].some(x=>(pt.std||st.std||[]).join().includes(x)))out.other.push([lp,g,subj,pt.title||st.title,'silent-note'])})}}}}
 return out},JSON.parse(process.env.LPS));
console.log(res.checked,res.needs,'missing',res.missing.length,JSON.stringify(res.missing.slice(0,12)),'silent',res.other.length,JSON.stringify(res.other.slice(0,6)),errs.slice(0,2));await b.close()})();
