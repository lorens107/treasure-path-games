/* TPMARK: teacher tool for read-aloud stops. Timer plus tap-to-mark missed words. Shared by the generated parts. */
window.TPMARK=window.TPMARK||function(v,ctx,units,auto){
 var st=ctx.stop,part=ctx.part,pi=st.parts.indexOf(part),n=ctx.note;
 if(!v||pi<0||!n||v.querySelector('[data-tpmark="'+pi+'"]'))return;
 n.mk=n.mk||{};var M=n.mk[pi]=n.mk[pi]||{};
 var box=document.createElement("div");box.className="no-key tpmark";box.setAttribute("data-tpmark",pi);
 box.style.cssText="margin:14px 0;padding:10px 12px;border:2px dashed var(--line);border-radius:12px";
 var h='<p class="small" style="margin:0 0 6px"><b>Teacher:</b> tap each '+(units[0].noun==="sounds"?"sound":"word")+' the student missed (skipped, changed, or said wrong). Tap again to undo.'+(units.some(function(u){return u.timed})?" Use Start when the student reads the first word and Stop at the last word.":"")+'</p>';
 units.forEach(function(u,ui){
  var words=u.w||String(u.t).split(/\s+/).filter(Boolean);
  h+='<div class="tpm-u" data-u="'+ui+'" style="margin:8px 0;padding-top:6px;border-top:1px solid var(--line)"><b>'+u.l+'.</b> ';
  if(u.timed)h+='<span class="small">Timer</span> <button type="button" class="chip" data-a="go">Start</button> <button type="button" class="chip" data-a="stop">Stop</button> <button type="button" class="chip" data-a="reset">Reset</button> <strong data-r="show"></strong> ';
  h+='<div style="margin:6px 0;line-height:2.3">'+words.map(function(w,i){return'<span class="mw" data-i="'+i+'" role="button" tabindex="0" style="display:inline-block;margin:2px 4px 2px 0;padding:0 8px;border:2px solid var(--line);border-radius:8px;font-size:1.3rem;cursor:pointer">'+w+'</span>'}).join("")+'</div><span class="small" data-r="sum"></span></div>';
 });
 box.innerHTML=h;
 var ol=v.querySelector('ol.qlist[data-part="'+pi+'"]');
 if(ol&&ol.parentNode)ol.parentNode.insertBefore(box,ol.nextSibling);else{var card=v.querySelector(".card")||v;card.appendChild(box)}
 var ints={};
 function tag(line){n.gen=n.gen||{};var k="mk"+pi,old=n.gen[k]||"",t=n.text||"";if(old&&t.indexOf(old)>=0)t=t.replace(old,function(){return line});else if(line)t=(t.trim()?t.replace(/\s+$/,"")+"\n":"")+line;n.text=t.replace(/^\s+/,"").replace(/\n{3,}/g,"\n\n");n.gen[k]=line;var ft=document.getElementById("fText");if(ft)ft.value=n.text}
 function paint(quiet){
  var good=0,lines=[];
  units.forEach(function(u,ui){
   var words=u.w||String(u.t).split(/\s+/).filter(Boolean),r=M[ui]||{},miss=r.miss||[],row=box.querySelector('.tpm-u[data-u="'+ui+'"]');
   row.querySelectorAll(".mw").forEach(function(el){var on=miss.indexOf(+el.dataset.i)>=0;el.style.background=on?"#ffd1d1":"";el.style.textDecoration=on?"line-through":"";el.style.borderColor=on?"#c0392b":"";el.setAttribute("aria-pressed",on?"true":"false")});
   var right=words.length-miss.length,pct=Math.round(right*100/words.length),ok=miss.length<=(u.allow||0);if(ok)good++;
   var nn=u.noun||"words",txt=right+" of "+words.length+" "+nn+" correct ("+pct+"%)";
   var wc=r.secs?Math.round(right*60/r.secs):null;
   if(r.secs)txt+=", "+r.secs+" sec, "+wc+" "+nn+" correct per minute";
   if(u.allow!=null&&auto)txt+=ok?". Counts as correct.":". Does not count as correct.";
   row.querySelector('[data-r="sum"]').textContent=txt;
   var sh=row.querySelector('[data-r="show"]');if(sh&&!ints[ui])sh.textContent=r.secs?r.secs+" sec":"0 sec";
   lines.push(u.l+": "+right+" of "+words.length+" "+nn+" correct"+(r.secs?", "+wc+" WCPM":"")+(miss.length?" (missed: "+miss.map(function(i){return words[i]}).join(", ")+")":""));
  });
  if(quiet)return;
  tag(lines.join(". ")+".");
  if(auto){var inp=document.querySelector('#stopView [data-f="right"][data-pi="'+pi+'"]');if(inp){inp.value=String(good);if(n.p&&n.p[pi])n.p[pi].right=String(good);inp.dispatchEvent(new Event("input",{bubbles:true}))}}
  if(ctx.save)ctx.save();
 }
 box.addEventListener("click",function(e){
  var t=e.target;if(!t||!t.closest)return;
  var mw=t.closest(".mw");
  if(mw){var ui=+mw.closest(".tpm-u").dataset.u,i=+mw.dataset.i,r=M[ui]=M[ui]||{},a=(r.miss||[]).filter(function(x){return x!==i});if((r.miss||[]).indexOf(i)<0)a.push(i);r.miss=a;paint();return}
  var b=t.closest("button[data-a]");if(!b)return;
  var row=b.closest(".tpm-u"),ui=+row.dataset.u,r=M[ui]=M[ui]||{},sh=row.querySelector('[data-r="show"]'),a=b.dataset.a;
  if(a==="go"){clearInterval(ints[ui]);var t0=Date.now();sh.textContent="0 sec";ints[ui]=setInterval(function(){if(!sh.isConnected){clearInterval(ints[ui]);return}sh.textContent=Math.round((Date.now()-t0)/1e3)+" sec"},250);row._t0=t0}
  else if(a==="stop"){if(!ints[ui])return;clearInterval(ints[ui]);ints[ui]=0;r.secs=Math.max(1,Math.round((Date.now()-row._t0)/1e3));sh.textContent=r.secs+" sec";paint()}
  else if(a==="reset"){clearInterval(ints[ui]);ints[ui]=0;delete r.secs;sh.textContent="0 sec";paint()}
 });
 box.addEventListener("keydown",function(e){if((e.key==="Enter"||e.key===" ")&&e.target.classList&&e.target.classList.contains("mw")){e.preventDefault();e.target.click()}});
 paint(!Object.keys(M).length);
};

/* TPELK: sound boxes (Elkonin boxes). The student taps a box for each sound; tap again to clear. */
window.TPELK=window.TPELK||function(v){
 if(!v)return;
 v.querySelectorAll(".elk-box").forEach(function(b){
  if(b._elk)return;b._elk=1;
  var f=function(){var on=b.textContent==="";b.textContent=on?"\u25CF":"";b.style.background=on?"#bfe3ff":""};
  b.addEventListener("click",f);
  b.addEventListener("keydown",function(e){if(e.key==="Enter"||e.key===" "){e.preventDefault();f()}});
 });
};
