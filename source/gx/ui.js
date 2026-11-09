const { chromium } = require('/opt/npm-tools/node_modules/playwright');
(async()=>{const b=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});
const p=await b.newPage({viewport:{width:1100,height:900}});
await p.goto('file://'+process.env.FILE,{waitUntil:'load',timeout:120000});await p.waitForTimeout(1500);
await p.evaluate(async()=>{await TP._debug.start({lp:1,grade:'1',subj:'math',check:'essential'})});
await p.waitForTimeout(500);
const info=await p.evaluate(()=>{const m=document.getElementById('mapView');return {vis:!m.hidden&&getComputedStyle(m).display,btns:[...m.querySelectorAll('button,[role=button],a,g[data-id],[data-stop]')].slice(0,12).map(e=>e.tagName+':'+(e.textContent||'').trim().slice(0,25)+':'+(e.dataset.id||e.dataset.stop||''))}});
console.log(JSON.stringify(info));
await p.screenshot({path:process.env.OUT});await b.close()})();
