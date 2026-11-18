/* TPMARK: teacher tool for read-aloud stops. Timer plus tap-to-mark missed words. Shared by the generated parts. */
window.TPMARK=window.TPMARK||function(v,ctx,units,auto,find){
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
 var ol=v.querySelector('ol.qlist[data-part="'+pi+'"]'),anc=null;
 if(!ol&&find){var norm=function(e){var c=e.cloneNode(true);c.querySelectorAll("br").forEach(function(b){b.replaceWith(" ")});return c.textContent.replace(/\s+/g," ").trim()};v.querySelectorAll(".passage").forEach(function(e){if(e.closest("details,.tbar,.tb-pass")||e.getAttribute("data-tdup"))return;if(norm(e)===find)anc=e})}
 if(ol&&ol.parentNode)ol.parentNode.insertBefore(box,ol.nextSibling);else if(anc&&anc.parentNode)anc.parentNode.insertBefore(box,anc.nextSibling);else{var card=v.querySelector(".card")||v;card.appendChild(box)}
 var ints={};
 function tag(line){n.gen=n.gen||{};var k="mk"+pi,old=n.gen[k]||"",t=n.text||"";if(old&&t.indexOf(old)>=0)t=t.replace(old,function(){return line});else if(line)t=(t.trim()?t.replace(/\s+$/,"")+"\n":"")+line;n.text=t.replace(/^\s+/,"").replace(/\n{3,}/g,"\n\n");n.gen[k]=line;var ft=document.getElementById("fText");if(ft)ft.value=n.text}
 function paint(quiet){
  var good=0,lines=[];
  units.forEach(function(u,ui){
   var words=u.w||String(u.t).split(/\s+/).filter(Boolean),r=M[ui]||{},miss=r.miss||[],row=box.querySelector('.tpm-u[data-u="'+ui+'"]');
   row.querySelectorAll(".mw").forEach(function(el){var on=miss.indexOf(+el.dataset.i)>=0;el.style.background=on?"#ffd1d1":"";el.style.textDecoration=on?"line-through":"";el.style.borderColor=on?"#c0392b":"";el.setAttribute("aria-pressed",on?"true":"false")});
   var right=words.length-miss.length;if(auto==="words")good+=right;var pct=Math.round(right*100/words.length),ok=miss.length<=(u.allow||0);if(ok&&auto!=="words")good++;
   var nn=u.noun||"words",txt=right+" of "+words.length+" "+nn+" correct ("+pct+"%)";
   var wc=r.secs?Math.round(right*60/r.secs):null;
   if(r.secs)txt+=", "+r.secs+" sec, "+wc+" "+nn+" correct per minute";
   if(u.allow!=null&&auto===true)txt+=ok?". Counts as correct.":". Does not count as correct.";
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

/* TPELK: sound boxes (Elkonin boxes), an optional support. Hidden until the teacher turns them on. Tap a box per sound; tap again to clear. */
window.TPELK=window.TPELK||function(v){
 if(!v)return;
 var rows=v.querySelectorAll(".elk");
 if(rows.length&&!v.querySelector(".elk-tog")){
  var bar=document.createElement("div");bar.className="elk-tog no-print";bar.style.cssText="margin:8px 0";
  var btn=document.createElement("button");btn.type="button";btn.className="btn ghost";btn.setAttribute("aria-pressed","false");
  var show=function(on){rows.forEach(function(r){r.style.display=on?"flex":"none"});btn.textContent=on?"Hide sound boxes":"Show sound boxes (optional support)";btn.setAttribute("aria-pressed",on?"true":"false")};
  btn.addEventListener("click",function(){show(btn.getAttribute("aria-pressed")!=="true")});
  bar.appendChild(btn);rows[0].parentNode.insertBefore(bar,rows[0]);show(false);
 }
 v.querySelectorAll(".elk-box").forEach(function(b){
  if(b._elk)return;b._elk=1;
  var f=function(){var on=b.textContent==="";b.textContent=on?"\u25CF":"";b.style.background=on?"#bfe3ff":""};
  b.addEventListener("click",f);
  b.addEventListener("keydown",function(e){if(e.key==="Enter"||e.key===" "){e.preventDefault();f()}});
 });
};
/* TPQS: for parts the teacher reads, student-facing text (passages, choice cards) is bigger than the small teacher question list. */
if(!document.getElementById("tp-qs-css")){var st=document.createElement("style");st.id="tp-qs-css";
 st.textContent=".tqm .qlist{font-size:1.2rem;line-height:1.35;color:var(--muted,#555)}.tqm .qlist li{margin-bottom:8px}.tqm .passage{font-size:2.7rem;line-height:1.7;max-width:none}.tqm .stu-card{font-size:2.6rem;line-height:1.6;font-weight:700;margin:10px 0;padding:6px 14px;border-left:6px solid var(--sea,#4a7ab5)}.tqm .stu-card .n{display:inline-block;min-width:1.4em;color:var(--sea,#4a7ab5)}.ex-card{border:3px dashed var(--sea,#4a7ab5);border-radius:14px;padding:10px 16px;margin:10px 0;background:var(--sea-soft,#eef5ff)}.ex-card .ex-h{font-size:1rem;font-weight:700;margin:0 0 4px}.ex-card .ex-say{font-size:1.1rem;margin:4px 0}.ex-card .stu-ex{font-size:2rem;font-weight:700;line-height:1.5;margin:6px 0}@media print{.elk-tog{display:none}}";
 document.head.appendChild(st)}
window.TPQS=window.TPQS||function(v){if(v&&v.classList)v.classList.add("tqm")};

/* TPLEX: every Language (L) part gets an "example first" card the teacher shows and talks through before the scored questions. */
window.TP_LEX=window.TP_LEX||[
 ["K",/printing uppercase|write each letter/i,{say:"Teacher says: Watch me first. I write the letter B. I start at the top, go straight down, then make two bumps. Now you write the letter I say."}],
 ["K",/position words|picture/i,{say:"Teacher points to the picture and says: The cat is under the table. Say it with me. Now I will ask you about the picture, and you answer in a whole sentence."}],
 ["K",/spoken grammar/i,{say:"Teacher says: Listen. One dog, two dogs. When there is more than one, the word changes. Your turn: one cat, two ____? Then go on to the scored items."}],
 ["TK",/./,{say:"Teacher points to one picture and says: This is a ball. What is this? Ball. Now I will point to other pictures, and you tell me what each one is."}],
 ["2",/say it right/i,{q:"One tooth, two ____.",a:"Teeth.",say:"Some words change in a special way when there is more than one."}],
 ["2",/write it right/i,{q:"Fix this sentence: the cats play in ohio",a:"The cats play in Ohio.",say:"The first word and the name of a place start with a capital letter. Then it ends with a period."}],
 ["2",/capital letters/i,{q:"Fix the capital letters: on monday i saw my friend sam.",a:"On Monday I saw my friend Sam.",say:"Days, the word I, and names all start with a capital letter."}],
 ["2",/dictionary/i,{q:"Put these words in ABC order the way a dictionary does: dog, cat, bird.",a:"Bird, cat, dog.",say:"Look at the first letter of each word and think of the alphabet song."}],
 ["2",/group words/i,{q:"Which word fits? A group of wolves is called a ___. (pack / drop)",a:"Pack.",say:"Animals that live together in a group have a special group name."}],
 ["2",/adjective or adverb/i,{q:"Which word tells how the turtle walks: slow or slowly? \u201CThe turtle walks ___.\u201D",a:"Slowly.",say:"A word that tells how someone does something usually ends in ly."}],
 ["3",/fix the message/i,{q:"The cat runned home.",a:"The cat ran home.",say:"Run is a special word. The past is ran, not runned."}],
 ["3",/field note/i,{q:"Join these two sentences with and: We packed food. We packed water.",a:"We packed food and water.",say:"And joins two ideas that go together into one sentence."}],
 ["3",/each other/i,{q:"The two puppies licked ___. (each other / one another)",a:"Each other.",say:"Use each other for two. Use one another for more than two."}],
 ["3",/cursive|joined writing/i,{say:"Teacher writes the sentence The sun is up. in cursive on paper, saying: I start each letter on the line and join the letters with a smooth line. Then the student writes the sentence on the screen."}],
 ["3",/what does the word do/i,{q:"Read: \u201CThe small dog barked loudly.\u201D What does the word small do? What kind of word is it?",a:"It tells what kind of dog. It is an adjective.",say:"Look at what the word is telling about."}],
 ["3",/grammar|correct word/i,{q:"Yesterday the boys ____ to the park. (walk)",a:"Walked.",say:"Yesterday already happened, so the word ends in ed."}],
 ["4",/cursive/i,{say:"Teacher writes the sentence The sun is up. in cursive on paper, saying: I keep my letters joined and the same size. Then the student writes the real sentence."}],
 ["4",/./,{q:"The tree ____ fell was old. (who or which)",a:"Which.",say:"Use who for people. Use which for things. A tree is a thing."}],
 ["5",/what does the word do/i,{q:"Read: \u201CSam ran to the park.\u201D What does the word to do?",a:"It is a preposition. It tells where Sam ran.",say:"Ask what job the word has in the sentence."}],
 ["5",/logbook|needs a fix/i,{q:"Yesterday the cook baked bread and eats it.",a:"Yesterday the cook baked bread and ate it.",say:"Both parts happened yesterday, so both verbs need the past tense."}],
 ["5",/./,{q:"Finish it: \u201CBy the time I woke up, the sun ____ (rise).\u201D",a:"Had risen.",say:"The sun rose before I woke up, so we use had and the past form."}],
 ["6",/vague pronoun/i,{q:"Fix the vague pronoun: \u201CRita gave Dee her coat.\u201D Who does her mean? Rewrite so it is clear.",a:"Rita gave Dee Rita\u2019s coat. (Or: Rita gave Dee Dee\u2019s coat.)",say:"If a pronoun could mean two people, use the name instead."}],
 ["6",/whole sentence|which is right/i,{q:"Which is right, and why? \u201CThe gift is for Ben and I\u201D or \u201CThe gift is for Ben and me.\u201D",a:"For Ben and me.",say:"Take Ben out. You would say the gift is for me, not for I."}],
 ["6",/./,{q:"Fix the mistake in this sentence: \u201CHim and Sam went home.\u201D",a:"He and Sam went home.",say:"Try each person alone. You would say He went home, not Him went home."}],
 ["7",/signals|phrase or a clause|phrase/i,{q:"\u201CThe cat sat <u>on the warm rug</u>.\u201D Is the underlined part a phrase or a clause? What job does it do?",a:"A phrase. It has no subject and verb. It tells where the cat sat.",say:"A clause has a subject and a verb. A phrase does not."}],
 ["7",/./,{q:"\u201CThe hikers were famished after the long climb, so they ate everything.\u201D What does famished mean? Which words are your clue?",a:"Very hungry. The clue is they ate everything.",say:"Look at the words around the hard word for clues."}],
 ["8",/./,{q:"\u201CSwimming is good exercise.\u201D Which word is the verbal? What kind is it, and what job does it do?",a:"Swimming. It is a gerund, and it is the subject.",say:"A verbal looks like a verb but does a different job."}]
];
window.TPLEX=window.TPLEX||function(p,v,pi,st){
 var stds=p&&p.std||[];if(!stds.length)return;
 var m=null;for(var i=0;i<stds.length;i++){var c=stds[i];var x=/^(?:TK\.ELA\.)?L\.(K|\d)\./.exec(c);if(!x){return}m=x[1]}
 if(!m||m==="1"&&stds[0].indexOf("TK.")!==0)return;
 var g=stds[0].indexOf("TK.")===0?"TK":m;
 var txt=[p.title||"",p.dir||"",p.desc||"",(p.qs&&p.qs[0])||"",(p.rows&&p.rows[0]&&p.rows[0][0])||""].join(" | ");
 var ex=null;for(var j=0;j<window.TP_LEX.length;j++){var r=window.TP_LEX[j];if(r[0]===g&&r[1].test(txt)){ex=r[2];break}}
 if(!ex)return;
 if(v.querySelector('.ex-card[data-lex="'+pi+'"]'))return;
 var d=document.createElement("div");d.className="ex-card";d.setAttribute("data-lex",pi);
 var h='<p class="ex-h">Example first (not scored). Show this to the student and think out loud.</p>';
 if(ex.q)h+='<div class="stu-ex">'+ex.q+'</div><p class="ex-say"><b>Answer: '+ex.a+'</b> '+ex.say+'</p>';else h+='<p class="ex-say">'+ex.say+'</p>';
 d.innerHTML=h;
 var ol=v.querySelector('ol.qlist[data-part="'+pi+'"]');
 if(ol){ol.parentNode.insertBefore(d,ol);return}
 var slot=v.querySelector('.pic-slot[data-pic-part="'+pi+'"]');
 if(slot){var a=slot.nextElementSibling;if(a&&a.className&&/dir/.test(a.className))a.parentNode.insertBefore(d,a.nextSibling);else slot.parentNode.insertBefore(d,slot.nextSibling)}
};
