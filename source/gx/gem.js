const { chromium } = require('/opt/npm-tools/node_modules/playwright');
(async()=>{const b=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});
const p=await b.newPage({viewport:{width:900,height:500}});
await p.goto('file://'+process.env.FILE,{waitUntil:'load',timeout:120000});await p.waitForTimeout(1500);
const r=await p.evaluate(()=>{const T=window.TP_THEMES.treasure;const d=document.createElement('div');d.style.cssText='position:fixed;inset:0;background:#f6e8c8;z-index:99999;padding:20px';
let h='<div style="display:flex;gap:10px">';["#E57373","#4FC3F7","#81C784","#BA68C8","#FFD54F","#F48FB1"].forEach(c=>h+='<div style="width:120px">'+T.itemSvg(c)+'</div>');h+='</div><p>'+[0,1,2,3,4,5].map(i=>T.itemSmall(i)).join(' ')+'</p>';d.innerHTML=h;document.body.appendChild(d);return !!T});
await p.waitForTimeout(300);await p.screenshot({path:process.env.OUT});console.log(r);await b.close()})();
