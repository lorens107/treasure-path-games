/* GX: fills gaps inside standards for grades 1 to 8. Adds parts to the stop that already holds the standard. */
(function(){
var D=window.GXD={};
window.GXtab=function(h,rows){return'<table class="tbl" style="margin:10px auto;font-size:1.3rem;border-collapse:collapse"><tr>'+h.map(function(x){return'<th style="border:2px solid var(--ink);padding:6px 14px">'+x+"</th>"}).join("")+"</tr>"+rows.map(function(r){return"<tr>"+r.map(function(x){return'<td style="border:2px solid var(--ink);padding:6px 14px;text-align:center">'+x+"</td>"}).join("")+"</tr>"}).join("")+"</table>"};

window.GXadd=function(grade,gap){(D[String(grade)]=D[String(grade)]||[]).push(gap)};
window.GXv=function(a,lp){return a[(lp-1)%a.length]};
window.GXqa=function(rows){return{qs:rows.map(function(r){return r[0]}),key:rows.map(function(r){return r[1]})}};
window.GXp=function(o){var p={gx:1,title:o.title,std:[o.std],dur:o.dur||90,dir:o.dir,desc:o.desc};
 if(o.rows){var q=GXqa(o.rows);p.qs=q.qs;p.key=q.key}else if(o.key)p.key=o.key;
 if(o.n)p.n=o.n;if(o.label)p.label=o.label;if(o.html)p.html=typeof o.html==="function"?o.html:function(){return o.html};
 if(o.fig)p.fig=o.fig;if(o.picSup)p.picSup=o.picSup;if(o.qfig)p.qfig=o.qfig;if(o.mats)p.mats=o.mats;if(o.kind)p.kind=o.kind;if(o.words)p.words=o.words;if(o.wordPics)p.wordPics=o.wordPics;if(o.read)p.read=o.read;return p};
var uid=9100;
window.GX=function(E,lp,grade,stops){
 (D[String(grade)]||[]).forEach(function(g){
  if(g.lps&&g.lps.indexOf(lp)<0)return;
  var host=null,hp=null,bi=-1;
  for(var i=0;i<stops.length;i++){var ps=stops[i].parts||[];for(var j=0;j<ps.length;j++){if((ps[j].std||[]).indexOf(g.std)>=0&&(!g.kinds||g.kinds.indexOf(ps[j].kind)>=0)){var hi=i;if(ps[j].gxHome!=null){for(var k=0;k<stops.length;k++)if(stops[k].id===ps[j].gxHome){hi=k;break}}if(bi<0||hi<bi){bi=hi;hp=ps[j]}}}}
  if(bi>=0)host=stops[bi];
  try{
   if(g.op==='keyAdd'){if(!hp)return;var ks=(hp.key||[]).join(' ');g.items.forEach(function(it){if(it.test.test(ks))return;hp.key=(hp.key||[]).concat([it.line]);ks+=' '+it.line;if(hp.n!=null)hp.n+=1});return}
   var p=g.make(lp,E,hp);if(!p)return;if(!p.std)p.std=[g.std];
   if(host)host.parts.push(p);else stops.push({id:++uid,title:p.title,short:p.title,parts:[p]});
  }catch(e){console.error("GX",grade,lp,g.std,e)}
 });
 return stops};
/* clone a read part for a second reading */
window.GXkeyAdd=function(std,items,lps){return{std:std,op:'keyAdd',items:items,lps:lps}};
window.GXreread=function(std,extra,anyKind){return{std:std,kinds:anyKind?null:["read","fable","fluency"],make:function(lp,E,hp){if(!hp)return null;
 var p=Object.assign({},hp);p.gx=1;p.title="Read It Again";p.dur=Math.max(60,(hp.dur||90)-20);
 p.dir="Read the same text one more time. Make it smoother and more expressive.";
 p.key=["Second reading of the same text. Count the words read correctly again and compare with the first reading. More words read correctly, fewer stops and rereads, and smoother phrasing show growth on successive readings."].concat(extra||[]);
 p.desc="reading the same on-level text orally a second time with accuracy, rate, and expression";return p}}};
})();

/* Teacher reads, grades TK to 2: the student is not asked to read unless the standard is a reading skill */
(function(){
var RFSTD=/(^|\.)RF\.|\.10$/;
function isReading(std){return (std||[]).some(function(c){return RFSTD.test(c)})}
function fixDir(d){
 if(!d)return d;
 d=d.replace(/Read the story if you have not read it yet\./,"Listen while your teacher reads the story again.");
 d=d.replace(/(^|[.!?] )Read ((?!each word|each line|each banner|each sign|the little book|the same text|the word |the story out loud in)[^.!?]*?)( out loud| with your teacher)?\./g,function(m,a,x){return a+"Listen while your teacher reads "+x+"."});
 d=d.replace(/hold it up or read it to your teacher/,"hold it up or tell your teacher what you wrote").replace(/Or read it to your teacher\./,"Or tell your teacher what you wrote.").replace(/read it to your teacher/g,"tell your teacher what you wrote");
 return d}
window.GXfixDir=fixDir;
window.GXdirs=function(grade,r){
 if(["1","2"].indexOf(String(grade))<0||!r)return;
 (r.stops||[]).forEach(function(st){(st.parts||[]).forEach(function(p){if(!isReading(p.std||st.std)&&p.dir)p.dir=fixDir(p.dir)})});
 var lv=r.levelups;if(lv)Object.keys(lv).forEach(function(k){var l=lv[k];if(l&&l.dir&&!isReading(l.std))l.dir=fixDir(l.dir)})};
window.GXlookBack=function(p,grade,call){
 if(["TK","K","1","2"].indexOf(String(grade))<0||!p)return false;
 if(isReading(p.std)||p.read||p.words||p.kind==="words"||p.kind==="read"||p.kind==="fable")return false;
 var h="";try{h=p.html?String(call(p.html)||""):""}catch(e){}
 return h.indexOf("look-back")>=0};
window.GXreadsText=function(p,grade,call){
 if(["TK","K","1","2"].indexOf(String(grade))<0||!p)return false;
 if(isReading(p.std)||p.read||p.words||p.kind==="words"||p.kind==="read"||p.kind==="fable")return false;
 var h="";try{h=p.html?String(call(p.html)||""):""}catch(e){}
 if(h.indexOf("look-back")>=0)return false;
 var allMath=(p.std||[]).length>0&&(p.std||[]).every(function(c){return /^(TK\.MATH\.|[K1-5]\.(CC|OA|NBT|MD|G|NF)\.)/.test(c)});
 if(!allMath&&p.fig){try{h+=" "+String(call(p.fig)||"")}catch(e){}}
 var words=h.replace(/<svg[\s\S]*?<\/svg>/g," ").replace(/<[^>]+>/g," ").replace(/\s+/g," ").trim();
 return words.split(" ").length>=6};
window.GXteach=function(p,t,grade,call){
 if(/marked "Read aloud|Read aloud to the student|Say each prompt|exactly as written|Say the prompt/i.test(t))return t;
 if(window.GXlookBack(p,grade,call))return t;
 if(!window.GXreadsText(p,grade,call))return t;
 return "Read the words on the screen aloud to the student, once, and again if they ask. "+t};
})();

window.TP_TIME={"RF.1.4":"Meant to assess successive readings (the same text read more than once). The game has one reading. You decide how to handle the reread, such as at home or at your next meeting.","RF.2.4":"Meant to assess successive readings (the same text read more than once). The game has one reading. You decide how to handle the reread, such as at home or at your next meeting.","RF.3.4":"Meant to assess successive readings (the same text read more than once). The game has one reading. You decide how to handle the reread, such as at home or at your next meeting.","RF.4.4":"Meant to assess successive readings (the same text read more than once). The game has one reading. You decide how to handle the reread, such as at home or at your next meeting.","RF.5.4":"Meant to assess successive readings (the same text read more than once). The game has one reading. You decide how to handle the reread, such as at home or at your next meeting.","SL.1.4":"The memorize and recite part cannot be checked in one meeting. Students need days of practice. Check it over the learning period.","SL.5.4":"The memorize and recite part cannot be checked in one meeting. Students need days of practice. Check it over the learning period."};

window.TP_BT={flat:"@@BTF@@",rod:"@@BTR@@",cube:"@@BTC@@"};

/* writing stops that use a story or text move right after the stop that reads it */
window.GXMOVES=[{"g": "2", "lp": 1, "id": 13, "after": 3}, {"g": "2", "lp": 1, "id": "13-facts1", "after": 4}, {"g": "3", "lp": 1, "id": "16-facts1", "after": 5}, {"g": "3", "lp": 1, "id": 16, "after": 3}, {"g": "4", "lp": 1, "id": "16-facts1", "after": 5}, {"g": "6", "lp": 1, "id": 8, "after": 4}, {"g": "6", "lp": 1, "id": "8-informative1", "after": 8}, {"g": "7", "lp": 1, "id": 13, "after": 8}, {"g": "7", "lp": 1, "id": "13-informative1", "after": 6}, {"g": "2", "lp": 4, "id": 13, "after": 3}, {"g": "2", "lp": 4, "id": "13-facts1", "after": 4}, {"g": "3", "lp": 4, "id": "16-facts1", "after": 5}, {"g": "4", "lp": 4, "id": "16-facts1", "after": 5}, {"g": "6", "lp": 4, "id": 8, "after": 4}, {"g": "6", "lp": 4, "id": "8-informative1", "after": 8}, {"g": "7", "lp": 4, "id": 13, "after": 8}, {"g": "7", "lp": 4, "id": "13-informative1", "after": 6}, {"g": "4", "lp": 2, "id": "10-facts1", "after": 8}, {"g": "5", "lp": 5, "id": 17, "after": 3}, {"g": "5", "lp": 8, "id": "17-facts1", "after": 4}, {"g": "6", "lp": 8, "id": "15-facts1", "after": 3}, {"g": "7", "lp": 8, "id": "9-facts1", "after": 3}, {"g": "3", "lp": 9, "id": "16-facts1", "after": 5}, {"g": "4", "lp": 9, "id": "16-facts1", "after": 5}, {"g": "6", "lp": 9, "id": 8, "after": 3}, {"g": "6", "lp": 10, "id": 13, "after": 3}, {"g": "7", "lp": 10, "id": 17, "after": 1}];

window.GXRoute=function(R,moves,clock){
 if(!moves||!moves.length)return clock;
 moves.forEach(function(m){
  var a=-1,b=-1,i;for(i=0;i<R.length;i++){if(!R[i].lv&&R[i].id===m.id)a=i}
  if(a<0)return;
  var cut=[R[a]];if(R[a+1]&&R[a+1].lv&&R[a+1].id==="L"+m.id)cut.push(R[a+1]);
  var tmp=R.slice();tmp.splice(a,cut.length);
  for(i=0;i<tmp.length;i++){if(!tmp[i].lv&&tmp[i].id===m.after)b=i}
  if(b<0)return;
  var e=b+1;while(tmp[e]&&tmp[e].lv)e++;
  Array.prototype.splice.apply(tmp,[e,0].concat(cut));
  R.length=0;tmp.forEach(function(x){R.push(x)})});
 var n=0,t=0;R.forEach(function(r){if(r.lv)return;r.num=++n;r.start=t;r.time=Math.floor(t/60)+":"+String(t%60).padStart(2,"0");t+=(r.parts||[]).reduce(function(a,p){return a+(p.dur||60)},0)});
 return t};
