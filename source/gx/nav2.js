const { chromium } = require('/opt/npm-tools/node_modules/playwright');
(async()=>{const b=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});
const p=await b.newPage({viewport:{width:1000,height:900}});
await p.goto('file://'+process.env.FILE,{waitUntil:'load',timeout:120000});await p.waitForTimeout(1500);
await p.evaluate(async()=>{await TP._debug.start({lp:1,grade:'1',subj:'math',check:'essential',lvOff:true});TP._debug.openStop(TP._debug.ROUTE[2].id)});
await p.waitForTimeout(400);await p.locator('.stop-head').screenshot({path:process.env.OUT});await b.close()})();
