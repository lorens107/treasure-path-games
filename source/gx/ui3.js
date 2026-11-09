const { chromium } = require('/opt/npm-tools/node_modules/playwright');
(async()=>{const b=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});
const p=await b.newPage({viewport:{width:1100,height:900}});
await p.goto('file://'+process.env.FILE,{waitUntil:'load',timeout:120000});await p.waitForTimeout(1500);
await p.evaluate(async()=>{await TP._debug.start({lp:1,grade:'1',subj:'math',check:'essential'})});
await p.waitForTimeout(500);
await p.mouse.click(397,176);await p.waitForTimeout(800);await p.getByRole('button',{name:'Student screen'}).click();await p.waitForTimeout(800);
console.log(JSON.stringify(await p.evaluate(()=>({prev:!!document.getElementById('prevBtn'),r:document.getElementById('prevBtn')?.getBoundingClientRect().toJSON(),h:document.querySelector('#stopView h2')?.textContent,view:[...document.querySelectorAll('.view')].filter(v=>!v.hidden&&getComputedStyle(v).display!=='none').map(v=>v.id)}))));
await p.screenshot({path:process.env.OUT});await b.close()})();
