(function(){
 window.TPNLon=window.TPNLon||{};
 function css(){if(document.getElementById("tpnl-css"))return;var st=document.createElement("style");st.id="tpnl-css";
  st.textContent=".nl20{overflow-x:auto;padding:4px 0 8px;scrollbar-width:thin}.nl20 .ln{position:relative;display:grid;grid-template-columns:repeat(21,minmax(1.35rem,1fr));min-width:29rem}"+
  ".nl20 .ln:before{content:\"\";position:absolute;left:calc(100%/42);right:calc(100%/42);top:14px;height:5px;background:var(--ink);border-radius:3px}"+
  ".nl20 button{position:relative;display:flex;flex-direction:column;align-items:center;gap:4px;background:none;border:0;padding:0 0 4px;cursor:pointer;color:var(--ink);font-family:\"Andika\",Verdana,sans-serif;font-weight:700;font-size:1.05rem;min-width:0}"+
  ".nl20 .tw{display:flex;align-items:center;height:34px}.nl20 .tk{display:block;width:4px;height:20px;background:var(--ink);border-radius:2px}.nl20 .tk.big{height:34px;width:6px}"+
  ".nl20 .num{display:block;min-width:1.7em;line-height:1.7em;border-radius:50%;border:2px solid transparent}.nl20 button.on .num{background:var(--gold);color:var(--gold-ink);border-color:var(--ink)}";
  document.head.appendChild(st)}
 window.TPNL20=function(){css();var h='<div class="nl20"><div class="ln">';
  for(var i=0;i<=20;i++){var big=(i%5===0);h+='<button data-n="'+i+'" class="'+(window.TPNLon[i]?"on":"")+'" aria-label="'+i+'"><span class="tw"><span class="tk'+(big?" big":"")+'"></span></span><span class="num">'+i+'</span></button>'}
  return h+'</div></div><p class="small" style="text-align:center">Tap a number to mark it. Tap again to clear it. Slide the line if you cannot see 20.</p>'};
 window.TPNL20Bind=function(b,r){b.querySelectorAll("[data-n]").forEach(function(x){x.onclick=function(){window.TPNLon[x.dataset.n]=!window.TPNLon[x.dataset.n];r()}})};
})();
window.TP_BASKET0="<svg x='25' y='-35' width='170' height='175' viewBox='0 0 350 360' overflow='visible'>"+
 "<path d='M55 190 C40 60 310 60 295 190' fill='none' stroke='#7A4A22' stroke-width='34' stroke-linecap='round'/>"+
 "<path d='M55 190 C40 60 310 60 295 190' fill='none' stroke='#F2B84B' stroke-width='22' stroke-linecap='round'/>"+
 "<ellipse cx='175' cy='188' rx='158' ry='38' fill='#8A5428' stroke='#7A4A22' stroke-width='6'/>"+
 "<path d='M22 200 Q20 330 130 346 L220 346 Q330 330 328 200 Q175 240 22 200 Z' fill='#F6C25B' stroke='#7A4A22' stroke-width='6' stroke-linejoin='round'/>"+
 "<path d='M80 232 Q70 300 98 342 M135 244 L132 346 M175 248 L175 346 M220 244 L224 346 M270 232 Q280 300 252 342 M60 326 Q175 352 290 326' fill='none' stroke='#C98E36' stroke-width='5' stroke-linecap='round'/>"+
 "<path d='M16 188 Q175 250 334 188 Q340 218 328 230 Q175 276 22 230 Q10 216 16 188 Z' fill='#F9D27A' stroke='#7A4A22' stroke-width='6' stroke-linejoin='round'/>"+
 "<ellipse cx='128' cy='282' rx='15' ry='19' fill='#3A2318'/><ellipse cx='222' cy='282' rx='15' ry='19' fill='#3A2318'/>"+
 "<circle cx='133' cy='275' r='5' fill='#fff'/><circle cx='227' cy='275' r='5' fill='#fff'/>"+
 "<ellipse cx='92' cy='306' rx='22' ry='15' fill='#F58FA0'/><ellipse cx='258' cy='306' rx='22' ry='15' fill='#F58FA0'/>"+
 "<path d='M155 304 Q175 336 195 304 Z' fill='#E5586B' stroke='#3A2318' stroke-width='4' stroke-linejoin='round'/></svg>";
