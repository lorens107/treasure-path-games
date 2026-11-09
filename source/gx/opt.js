const { chromium } = require('/opt/npm-tools/node_modules/playwright');
(async()=>{const b=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});
const p=await b.newPage();await p.goto('file://'+process.env.FILE,{waitUntil:'load',timeout:120000});await p.waitForTimeout(1500);
console.log(await p.evaluate(()=>({check:[...document.querySelectorAll('#suCheck option')].map(o=>o.value+':'+o.textContent.trim()),keys:Object.keys(TP._debug),startSrc:String(TP._debug.start).slice(0,700)})));await b.close()})();
