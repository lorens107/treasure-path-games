const { chromium } = require('/opt/npm-tools/node_modules/playwright');
(async()=>{const b=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});
const p=await b.newPage({viewport:{width:1100,height:1000}});const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.goto('file://'+process.env.FILE,{waitUntil:'load',timeout:120000});await p.waitForTimeout(1500);
const out=await p.evaluate(async()=>{const res=[];
for(const [g,lp,subj] of [['1',1,'ela'],['1',1,'math'],['2',3,'ela'],['4',4,'math'],['K',1,'ela']]){
 try{await TP._debug.start({lp,grade:g,subj,check:'essential',lvOff:true});}catch(e){res.push(g+' start err');continue}
 TP._debug.S.ui=TP._debug.S.ui||{};TP._debug.S.ui.pics=true;let n=0,stops=0;
 for(const st of TP._debug.ROUTE.filter(s=>!s.lv)){TP._debug.openStop(st.id);await new Promise(r=>setTimeout(r,60));stops++;n+=document.querySelectorAll('#stopView .pw').length}
 res.push([g,lp,subj,'stops',stops,'word-pics',n])}
return res});
console.log(JSON.stringify(out),errs);await b.close()})();
