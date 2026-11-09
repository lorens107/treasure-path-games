const { chromium } = require('/opt/npm-tools/node_modules/playwright');
(async()=>{const b=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});
const p=await b.newPage({viewport:{width:1100,height:600}});const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.goto('file://'+process.env.FILE,{waitUntil:'load',timeout:120000});await p.waitForTimeout(1500);
await p.evaluate(async()=>{await TP._debug.start({lp:1,grade:'1',subj:'math',check:'essential'})});await p.waitForTimeout(600);
await p.screenshot({path:process.env.OUT+'1.png'});
await p.evaluate(()=>{const S=TP._debug.S;S.done=TP._debug.ROUTE.filter(s=>!s.lv).map(s=>s.id);TP._debug.drawMap&&TP._debug.drawMap()});
await p.evaluate(()=>{document.getElementById('mapBtn').click()});await p.waitForTimeout(600);
await p.screenshot({path:process.env.OUT+'2.png'});console.log(errs);await b.close()})();
