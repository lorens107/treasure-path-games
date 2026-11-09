const { chromium } = require('/opt/npm-tools/node_modules/playwright');
(async()=>{const b=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});
const p=await b.newPage({viewport:{width:1100,height:1000}});const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.goto('file://'+process.env.FILE,{waitUntil:'load',timeout:120000});await p.waitForTimeout(1500);
const out=[];
for(const pics of [false,true]){
out.push(await p.evaluate(async(pics)=>{await TP._debug.start({lp:1,grade:'1',subj:'ela',check:'essential',lvOff:true});
const st=TP._debug.ROUTE.find(s=>!s.lv&&s.title==='Story Questions');if(!st)return 'no stop';
TP._debug.S.ui=TP._debug.S.ui||{};TP._debug.S.ui.pics=pics;TP._debug.openStop(st.id);await new Promise(r=>setTimeout(r,500));
const ss=document.querySelector('#stopView .scene-sup');return {stop:st.num,pics,has:!!ss,hidden:ss&&ss.hidden,vis:ss&&ss.getBoundingClientRect().height}},pics));
if(pics){await p.waitForTimeout(500);await p.screenshot({path:process.env.OUT})}}
console.log(JSON.stringify(out),errs);await b.close()})();
