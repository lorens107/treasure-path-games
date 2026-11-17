/* GREAD: RF.x.4 split into accuracy and fluency parts for grades 2 to 5 (grade 1 is built in g1.js) */
(function(){
window.TP_STRANDS=window.TP_STRANDS||{};
[2,3,4,5].forEach(function(g){window.TP_STRANDS["RF."+g+".4"]={desc:"reading with accuracy and fluency to support comprehension",parts:[{id:"acc",label:"Read with accuracy",desc:"Reading on-level text with sufficient accuracy"},{id:"flu",label:"Read with fluency",desc:"Reading on-level text with sufficient fluency (smooth, with expression)"}]}});
window.TP_TIME_PARTS=window.TP_TIME_PARTS||{};
[2,3,4,5].forEach(function(g){window.TP_TIME_PARTS["RF."+g+".4"]={flu:"Successive readings may need to be completed to fully measure this part."}});
window.GXrtext=function(h){var d=document.createElement("div");d.innerHTML=typeof h==="function"?h():(h||"");d.querySelectorAll("br").forEach(function(b){b.replaceWith(" ")});d.querySelectorAll("h3,.part-title,details").forEach(function(e){e.remove()});var e=d.querySelector(".passage");return(e?e.textContent:d.textContent).replace(/\s+/g," ").trim()};
window.GXfluTool=function(p){var h=p.html;p.after=function(v,ctx){var t=GXrtext(h);if(!t||!window.TPMARK)return;var wc=t.split(" ").length;TPMARK(v,ctx,[{l:"Reading",t:t,timed:true,allow:wc-Math.round(wc*0.95+0.4)}],"words",t)}};
window.GXacc=function(hp,flu){var a=Object.assign({},hp);a.gx=1;a.strand="acc";a.title=hp.title||"Read the Story";a.desc="reading on-level text orally with sufficient accuracy";return[a,flu]};
GXadd(2,{std:"RF.2.4",op:"strands",make:function(lp,E,hp){if(!hp)return null;var f=Object.assign({},hp);f.gx=1;f.strand="flu";f.title="Read It Again";f.dur=Math.max(60,(hp.dur||90)-20);f.dir="Read the same story one more time. Make it smoother and more expressive.";f.desc="reading the same on-level text orally a second time with appropriate rate and expression";f.key=["Second reading of the same story. Use the timer under the passage and tap each missed word. Compare the words correct with the first reading.","Listen for phrasing, pauses at punctuation, and a voice that fits the story. Reading word by word is not yet fluent."];GXfluTool(f);return GXacc(hp,f)}});
})();
