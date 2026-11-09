import glob,os,sys,subprocess
B=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/'
s=open(B+'work/patched_base.html').read()
old='(window.TP_PENDING=window.TP_PENDING||[]).push(m)}};'
assert s.count(old)==1
new='if(m&&/^[1-8]$/.test(String(m.grade))&&typeof m.build==="function"&&!m.gxd){m.gxd=1;var ob3=m.build;m.build=function(E){var r=ob3.call(this,E);try{if(window.GX&&r&&r.stops)r.stops=window.GX(E,m.lp,String(m.grade),r.stops);r.gxMoves=(window.GXMOVES||[]).filter(function(x){return x.g===String(m.grade)&&x.lp===m.lp});if(window.GXdirs)window.GXdirs(String(m.grade),r)}catch(e){console.error("GX",e)}return r}}'+old
s=s.replace(old,new)
DI='<img class="dir-img" alt="" aria-hidden="true" height="34" src="data:image/webp;base64,${PIC_IMG.tap}"> '
assert s.count(DI)==1
s=s.replace(DI,'')
import json as _j
GI=_j.load(open(B+'gem/gems.json'))
def must(a,b,n=1,first=False):
    global s
    assert s.count(a)==n,(a[:50],s.count(a))
    s=s.replace(a,b,1) if first else s.replace(a,b)
must('const TREASURE={key:"treasure"','const GEMIMG='+_j.dumps(GI)+';const gemPic=(i,w)=>`<image href="data:image/webp;base64,${GEMIMG[i%6]}" x="${-w/2}" y="${-w/2}" width="${w}" height="${w}"/>`;const GEMKEY={"#E57373":0,"#4FC3F7":1,"#81C784":2,"#BA68C8":3,"#FFD54F":4,"#F48FB1":5};const TREASURE={key:"treasure"')
must('itemSvg:c=>sv(gem(-32,10,c||gemCols[0],2)),itemSmall:i=>`<svg viewBox="-2 -20 36 30" width="22" height="18" aria-hidden="true">${gem(0,0,gemCols[i%5])}</svg>`','itemSvg:c=>sv(gemPic(GEMKEY[c]==null?1:GEMKEY[c],76)),itemSmall:i=>`<svg viewBox="-12 -12 24 24" width="24" height="24" aria-hidden="true">${gemPic(i,24)}</svg>`')
must('T.itemSvg(["#4FC3F7","#E57373","#81C784","#BA68C8","#FFD54F"][c%5])','T.itemSvg(T.key==="treasure"?["#E57373","#4FC3F7","#81C784","#BA68C8","#FFD54F","#F48FB1"][c%6]:["#4FC3F7","#E57373","#81C784","#BA68C8","#FFD54F"][c%5])')
must('<div class="stop-foot"><button class="btn ghost" id="backMap">Back to map</button>','<div class="stop-foot" style="justify-content:flex-end">')
must('<span class="row">${st.lv?`<button class="btn ghost" id="skipBtn">','<span class="row">${(()=>{const pv=ROUTE[ROUTE.indexOf(st)-1];return pv?`<button class="btn ghost" id="prevBtn">&larr; Back to ${pv.lv?"Level Up":"stop "+pv.num}</button>`:""})()}${st.lv?`<button class="btn ghost" id="skipBtn">')
must('$("backMap").onclick=()=>{current=null;drawMap();show("mapView")};','{const pb=$("prevBtn");if(pb)pb.onclick=()=>go(ROUTE[ROUTE.indexOf(st)-1])};')
must('["mapBtn","teacherBtn","newBtn","backMap","gemBtn","skipBtn"]','["mapBtn","teacherBtn","newBtn","prevBtn","gemBtn","skipBtn"]',s.count('["mapBtn","teacherBtn","newBtn","backMap","gemBtn","skipBtn"]'))
FD=open(B+'gem/foxduck.b64').read()
must('id:3,title:"Read the Story",parts:[{std:["RF.1.4"],kind:"fable",n:73,label:"words read correctly",dur:120,html:()=>`<p class="passage">${FABLE}</p>`,','id:3,title:"Read the Story",parts:[{std:["RF.1.4"],kind:"fable",n:73,label:"words read correctly",dur:120,html:()=>`<p class="passage">${FABLE}</p>`,picSup:true,fig:()=>`<div class="figure"><img alt="Fox waves up at Duck, who holds his red hat on a tree branch" style="max-width:100%;width:560px;height:auto;border-radius:14px" src="data:image/webp;base64,'+FD+'"></div>`,')
FG=open(B+'gem/frogcycle.b64').read()
must('{title:"Frog Facts",std:["RI.1.1"],dur:75,html:()=>`<p class="passage">${FROG}</p>`,','{title:"Frog Facts",std:["RI.1.1"],dur:75,html:()=>`<p class="passage">${FROG}</p>`,picSup:true,fig:()=>`<div class="figure"><img alt="A frog in a pond catching a bug with its tongue. Below it, five steps in a row: egg, tadpole, tadpole with legs, young frog, adult frog." style="max-width:100%;width:700px;height:auto;border-radius:14px" src="data:image/webp;base64,'+FG+'"></div>`,')
BP=open(B+'gem/beepic.b64').read()
must('{title:"Listen Up",std:["SL.1.2"],n:4,dur:75,read:BEES,html:()=>`<p class="huge" aria-hidden="true">${ico("bee",96)}</p>`,','{title:"Listen Up",std:["SL.1.2"],n:4,dur:75,read:BEES,picSup:true,html:()=>"",fig:()=>`<div class="figure"><img alt="Bees by a hive in a tree. One bee dances in a figure eight and a speech bubble shows flowers. Another bee has yellow pollen on its legs." style="max-width:100%;width:700px;height:auto;border-radius:14px" src="data:image/webp;base64,'+BP+'"></div>`,')
WA=open(B+'gem/wp_ana.b64').read();WE=open(B+'gem/wp_eli.b64').read()
must('{id:9,title:"Word Problems",parts:[{title:"Word Problems",std:["1.OA.A.1"],dur:60,','{id:9,title:"Word Problems",parts:[{title:"Word Problems",std:["1.OA.A.1"],dur:60,picSup:true,fig:()=>"",qfig:[()=>`<div class="figure" style="margin:10px 0"><img alt="Eli has 9 shells and finds some more to make 15. Shell groups of 9 and 6 make 15, shown with 9 cubes plus 6 cubes equals 1 ten and 5 ones. The number sentence reads 9 plus a box equals 15." style="max-width:100%;width:640px;height:auto;border-radius:14px" src="data:image/webp;base64,'+WE+'"></div>`,()=>`<div class="figure" style="margin:10px 0"><img alt="Ana has 12 stickers shown as stars and Ben has 8. Blocks show a ten and 2 ones above 8 ones. The number sentence reads 12 minus 8 equals a box." style="max-width:100%;width:640px;height:auto;border-radius:14px" src="data:image/webp;base64,'+WA+'"></div>`],')
BA=open(B+'gem/ba_a.b64').read();BB=open(B+'gem/ba_b.b64').read();BC=open(B+'gem/ba_c.b64').read()
must('{id:10,title:"Big Adding",parts:[{title:"Big Adding",std:["1.NBT.C.4"],dur:60,','{id:10,title:"Big Adding",parts:[{title:"Big Adding",std:["1.NBT.C.4"],dur:60,picSup:true,fig:()=>"",qfig:[()=>`<div class="figure" style="margin:6px 0 12px"><img alt="Base ten blocks: 3 tens rods and 4 ones cubes, plus 5 ones cubes." style="max-width:100%;width:520px;height:auto;border-radius:14px" src="data:image/webp;base64,'+BC+'"></div>`,()=>`<div class="figure" style="margin:6px 0 12px"><img alt="Base ten blocks: 4 tens rods and 6 ones cubes, plus 2 tens rods." style="max-width:100%;width:520px;height:auto;border-radius:14px" src="data:image/webp;base64,'+BB+'"></div>`,()=>`<div class="figure" style="margin:6px 0 12px"><img alt="Base ten blocks: 2 tens rods and 7 ones cubes, plus 8 ones cubes." style="max-width:100%;width:520px;height:auto;border-radius:14px" src="data:image/webp;base64,'+BA+'"></div>`],')
must('if(p.fig)h+=sceneSup(p)?','if(p.fig&&!p.qfig)h+=sceneSup(p)?')
must('p.qs.map(q=>`<li>${q}</li>`).join("")','p.qs.map((q,qi)=>`<li>${q}${p.qfig&&p.qfig[qi]&&sceneSup(p)?`<div class="scene-sup"${ui().pics?"":" hidden"}>${call(p.qfig[qi])}</div>`:""}</li>`).join("")')
T7=open(B+'gem/ta_70.b64').read();T9=open(B+'gem/ta_90.b64').read()
must('{title:"Take Away Tens",std:["1.NBT.C.6"],dur:30,','{title:"Take Away Tens",std:["1.NBT.C.6"],dur:30,picSup:true,fig:()=>"",qfig:[()=>`<div class="figure" style="margin:6px 0 12px"><img alt="Base ten blocks: 7 tens rods minus 3 tens rods." style="max-width:100%;width:520px;height:auto;border-radius:14px" src="data:image/webp;base64,'+T7+'"></div>`,()=>`<div class="figure" style="margin:6px 0 12px"><img alt="Base ten blocks: 9 tens rods minus 5 tens rods." style="max-width:100%;width:520px;height:auto;border-radius:14px" src="data:image/webp;base64,'+T9+'"></div>`],')
ME=open(B+'gem/me.b64').read()
must('{title:"Measure It",std:["1.MD.A.2"],dur:30,fig:()=>measureFig(),','{title:"Measure It",std:["1.MD.A.2"],dur:30,fig:()=>`<div class="figure" style="margin:6px 0 12px"><img alt="Question 1: How many paper clips long is the pencil? A pencil is lined up above a row of paper clips. Question 2: Is the crayon measured the right way? A crayon is lined up above three paper clips with gaps between them." style="max-width:100%;width:640px;height:auto;border-radius:14px" src="data:image/webp;base64,'+ME+'"></div>`,',2,True)
must('if(p.fig&&!p.qfig)h+=sceneSup(p)?','if(p.fig&&!p.qfig)h+=sceneSup(p)&&!p.supfig?')
must('function sceneSup(p){return!!(p&&p.fig&&p.picSup||','function sceneSup(p){return!!(p&&p.supfig||p&&p.fig&&p.picSup||')
must('if(p.render)h+=`<div data-custom="${pi}">','if(p.supfig&&(sceneSup(p)||p._sf))h+=`<div class="scene-sup"${ui().pics?"":" hidden"}>${call(p.supfig)}</div>`;if(p.render)h+=`<div data-custom="${pi}">')
for _x in ("60","100"):
    must('<rect x="5" y="5" width="190" height="110" rx="12" fill="#FDF6E6" stroke="${INK}" stroke-width="4"/><line x1="%s" y1="5"'%_x,'<rect x="5" y="5" width="190" height="110" fill="#FDF6E6" stroke="${INK}" stroke-width="4" stroke-linejoin="miter"/><line x1="%s" y1="5"'%_x)
PZ=open(B+'gem/pizza.b64').read()
must('{title:"Fair Shares",std:["1.G.A.3"],dur:70,fig:()=>sharesFig(),','{title:"Fair Shares",std:["1.G.A.3"],dur:70,fig:()=>sharesFig(),qsup:[null,null,()=>`<div class="figure" style="margin:6px 0 12px"><img alt="A half of a pizza and a fourth of the same pizza, side by side." style="max-width:100%;width:420px;height:auto" src="data:image/webp;base64,'+PZ+'"></div>`],',1,True)
must('if(p.fig&&!p.qfig)h+=sceneSup(p)&&!p.supfig?','if(p.fig&&!p.qfig)h+=sceneSup(p)&&!p.supfig&&!p.qsup?')
must('function sceneSup(p){return!!(p&&p.supfig||','function sceneSup(p){return!!(p&&(p.supfig||p.qsup)||')
must('${p.qfig&&p.qfig[qi]&&sceneSup(p)?`<div class="scene-sup"${ui().pics?"":" hidden"}>${call(p.qfig[qi])}</div>`:""}','${(p.qfig&&p.qfig[qi]||p.qsup&&p.qsup[qi])&&sceneSup(p)?`<div class="scene-sup"${ui().pics?"":" hidden"}>${call(p.qfig&&p.qfig[qi]||p.qsup[qi])}</div>`:""}')
OP=open(B+'gem/op.b64').read()
must('{wt:"opinion",title:"Opinion Writing",std:["W.1.1","W.1.8","L.1.1"],n:7,label:"checks met",dur:180,','{wt:"opinion",title:"Opinion Writing",std:["W.1.1","W.1.8","L.1.1"],n:7,label:"checks met",dur:180,picSup:true,fig:()=>`<div class="figure" style="margin:10px 0"><img alt="A fox looks up at a tree. A duck on a branch holds the fox\'s red hat in her beak. Wind blows the leaves." style="max-width:100%;width:600px;height:auto;border-radius:14px" src="data:image/webp;base64,'+OP+'"></div>`,',2,True)
FL=open(B+'gem/flags.b64').read()
must('{title:"Flag Line Up",std:["TK.MATH.3.2"],n:3,dur:45,dir:"Look at the flag poles. Say them in order from shortest to tallest.",desc:"ordering 5 objects by height",fig:()=>F.row(polesFig()),','{title:"Flag Line Up",std:["TK.MATH.3.2"],n:3,dur:45,dir:"Look at the flag poles. Say them in order from shortest to tallest.",desc:"ordering 5 objects by height",fig:()=>`<div class="figure"><img alt="Five flag poles of different heights: blue, yellow, green, red, purple" style="max-width:100%;width:760px;height:auto" src="data:image/webp;base64,'+FL+'"></div>`,')
# --- LP1: tropical birds (parrots) instead of bluebird / cardinal ---
must('"parrot","bluebird","butterfly","cardinal","star","rainbow","cloud","sun"],paths:[[["palm","Jungle trail"]','"parrot","starfish","butterfly","seahorse","star","rainbow","cloud","sun"],paths:[[["palm","Jungle trail"]')
must('[["map","Follow the map"],["bluebird","Follow the bird"]]','[["map","Follow the map"],["parrot","Follow the bird"]]')
def _lp1(mod,pairs):
    global s
    i=s.index('TP.register({id:"%s"'%mod);j=s.index('TP.register({id:"',i+10)
    seg=s[i:j]
    for o,n,c in pairs:
        assert seg.count(o)==c,(mod,o,seg.count(o))
        seg=seg.replace(o,n)
    s=s[:i]+seg+s[j:]
_lp1("lp1-g3",[('F.icon("bluebird",96)','F.icon("parrot",96)',1),('A gull lands behind her.','A parrot lands behind her.',1),('information about the gull?','information about the parrot?',1),('ear or hears the gull,','ear or hears the parrot,',1)])
_lp1("lp1-g6",[('ico("bluebird",74)','ico("parrot",74)',2)])
_lp1("lp1-gk",[('ico("bluebird",88)','ico("parrot",88)',1),('ico("bluebird",80)','ico("parrot",80)',1)])
must('MAIN=ROUTE.filter(r=>!r.lv);LV=ROUTE.filter(r=>r.lv);return clockSec}','if(window.GXRoute&&C.gxMoves)clockSec=window.GXRoute(ROUTE,C.gxMoves,clockSec);if(window.KLApply)window.KLApply(ROUTE);MAIN=ROUTE.filter(r=>!r.lv);LV=ROUTE.filter(r=>r.lv);return clockSec}')
must('sw:["shell","shell"]','sw:["star","star"]')
must('sw:["sheep","sheep"]','sw:["sun","sun"]')
_s=s.index('out.push(S(103,"Letter Sounds"');_e=s.index('out.push(S(104,"Book Skills"')
s=s[:_s].rstrip(' ')+' var LSX={1:["n","l",["parrot","parrot","p"],["dog","dog","d"]],2:["m","n",["turtle","turtle","t"],["rabbit","rabbit","r"]],3:["s","f",["bee","bee","b"],["turtle","turtle","t"]],4:["m","t",["deer","deer","d"],["rabbit","rabbit","r"]],5:["n","l",["penguin","penguin","p"],["hen","hen","h"]],6:["n","r",["dog","dog","d"],["watermelon","watermelon","w"]],7:["t","n",["pig","pig","p"],["rabbit","rabbit","r"]],8:["p","n",["hen","hen","h"],["watermelon","watermelon","w"]],9:["n","h",["rabbit","rabbit","r"],["watermelon","watermelon","w"]],10:["t","n",["dog","dog","d"],["fish","fish","f"]]}[lp]||["n","l",["parrot","parrot","p"],["dog","dog","d"]];\n var LSD=["m","s","t","b","f","n","h","p","d","r","k","l","w","j","v"];\n var lsOpts=function(t,k){var o=LSD.filter(function(x){return x!==t&&x!==LSX[0]&&x!==LSX[1]&&x!==LSX[2][2]&&x!==LSX[3][2]||x===t});o=o.filter(function(x,i){return x===t||true});var d=LSD.filter(function(x){return x!==t});var a=d[(k*3)%d.length],b=d[(k*3+4)%d.length];if(a===b)b=d[(k*3+5)%d.length];var r=[a,b];r.splice(k%3,0,t);return r};\n out.push(S(103,"Letter Sounds","Sounds",{title:"Sound to Letter",std:["TK.ELA.FLS.2.5"],n:4,dur:110,\n  dir:"Listen to your teacher. Point to the letter that makes the sound.",\n  desc:"matching a spoken sound to its letter and a picture\'s first sound to its letter",\n  fig:function(){return nrow(1,rowf(lsOpts(LSX[0],0).map(lett)))+nrow(2,rowf(lsOpts(LSX[1],1).map(lett)))+nrow(3,rowf([cell(ic(LSX[2][0],100),LSX[2][1])].concat(lsOpts(LSX[2][2],2).map(lett))))+nrow(4,rowf([cell(ic(LSX[3][0],100),LSX[3][1])].concat(lsOpts(LSX[3][2],3).map(lett))))},\n  key:["Row 1. Say the sound /"+LSX[0]+"/ (not the letter name). Say: Point to the letter that says /"+LSX[0]+"/. ("+LSX[0]+")","Row 2. Say the sound /"+LSX[1]+"/. Say: Point to the letter that says /"+LSX[1]+"/. ("+LSX[1]+")","Row 3. Point to the "+LSX[2][1]+". Say: "+cap(LSX[2][1])+". What is the first sound? (/"+LSX[2][2]+"/) Now point to the letter that makes that sound. ("+LSX[2][2]+")","Row 4. Point to the "+LSX[3][1]+". Say: "+cap(LSX[3][1])+". What is the first sound? (/"+LSX[3][2]+"/) Now point to the letter that makes that sound. ("+LSX[3][2]+")","The letter name does not count in place of the sound. If the child says the letter name, ask: What sound does it make?"]}));\n '+' '+s[_e:]
must("fig:function(){var cover=function(up){return '<div class=\"tkx-card\" style=\"width:150px;text-align:center;'","fig:function(){var cover=function(up){if(lp===1)return '<img alt=\"Book cover: Pete the Pirate Finds the Treasure\" src=\"data:image/webp;base64,'+window.TP_IMG1.book+'\" style=\"width:190px;height:auto;display:inline-block;margin:4px;'+(up?'':'transform:rotate(180deg);')+'\">';return '<div class=\"tkx-card\" style=\"width:150px;text-align:center;'")
must("tkx-pg\">Pip can see the '+esc(nm(KK[0]))+'.<br>Pip can run to it.</div>'","tkx-pg\">'+(lp===1?'Pete':'Pip')+' can see the '+esc(nm(KK[0]))+'.<br>'+(lp===1?'Pete':'Pip')+' can run to it.</div>'")
must('(the words at the top, "+T.pip+")','(the words at the top, "+(lp===1?"Pete the Pirate Finds the Treasure":T.pip)+")')
must('(the first word, top left, \\"Pip\\")','(the first word, top left, \\""+(lp===1?"Pete":"Pip")+"\\")')
must("fig:function(){return '<div class=\"figure\" style=\"margin:8px 0\"><div class=\"tkx-card\" style=\"padding:14px 24px;text-align:center\">","fig:function(){if(lp===1)return '<div class=\"figure\" style=\"margin:8px 0\"><img alt=\"Pirate name tag that says My name is, with a line to write on\" src=\"data:image/webp;base64,'+window.TP_IMG1.tag+'\" style=\"width:420px;max-width:100%;height:auto\"></div>';return '<div class=\"figure\" style=\"margin:8px 0\"><div class=\"tkx-card\" style=\"padding:14px 24px;text-align:center\">")
_cm=open("../gem/cmp.b64").read().strip();_cb=open("../gem/catbook.b64").read().strip();_cl=open("../gem/catlines.b64").read().strip();_bs=open("../gem/bearstory.b64").read().strip();_cs=open("../gem/catstory.b64").read().strip();_pl=open("../gem/places.b64").read().strip();_dk=open("../gem/ducks.b64").read().strip();_wf=open("../gem/wordfun.b64").read().strip();_at=open("../gem/addtake.b64").read().strip();_fs=open("../gem/flatsolid.b64").read().strip();_pr=open("../gem/parrot.b64").read().strip();import json as _js;_tj=_js.dumps(_js.load(open("../gem/trees.json")),separators=(",",":"));_pj=_js.dumps(_js.load(open("../gem/props.json")),separators=(",",":"));_cl=""
_bk2=open("../gem/book_pete.b64").read().strip();_nt2=open("../gem/nametag.b64").read().strip()
assert s.count('<script>TP.register({id:"lp1-gtk"')==1
_kl=open('klisten.js').read()+'\n'+open('nline.js').read()
s=s.replace('<script>TP.register({id:"lp1-gtk"','<script>'+_kl+'</script>\n<script>TP.register({id:"lp1-gtk"',1)
s=s.replace('<script>TP.register({id:"lp1-gtk"','<script>window.TP_IMG1={book:"'+_bk2+'",tag:"'+_nt2+'",cmp:"'+_cm+'",cats:"'+_cb+'",lines:"'+_cl+'",bear:"'+_bs+'",story:"'+_cs+'",places:"'+_pl+'",ducks:"'+_dk+'",wordfun:"'+_wf+'",addtake:"'+_at+'",flatsolid:"'+_fs+'",parrot:"'+_pr+'",cover2:"'+open("../gem/cover2.b64").read().strip()+'",trees:'+_tj+',props:'+_pj+',crate10:"'+open("../gem/crate10.b64").read().strip()+'",rhymecard:"'+open("../gem/rhymecard.b64").read().strip()+'",clapset:"'+open("../gem/clapset.b64").read().strip()+'",squirrel:"'+open("../gem/squirrel.b64").read().strip()+'",cidersteps:"'+open("../gem/cidersteps.b64").read().strip()+'",farmstand:"'+open("../gem/farmstand.b64").read().strip()+'",saybee:"'+open("../gem/saybee.b64").read().strip()+'",beepos:"'+open("../gem/beepos.b64").read().strip()+'",beefacts:"'+open("../gem/beefacts.b64").read().strip()+'",littlebook:"'+open("../gem/littlebook.b64").read().strip()+'",cider2:"'+open("../gem/cider2.b64").read().strip()+'",pick2:"'+open("../gem/pick2.b64").read().strip()+'",flat4:"'+open("../gem/flat4.b64").read().strip()+'",g1sounds:"'+open("../gem/g1sounds.b64").read().strip()+'",g1vowels:"'+open("../gem/g1vowels.b64").read().strip()+'",wp:'+open("../gem/wp.json").read().strip()+',wp2:'+open("../gem/wp2.json").read().strip()+',wp3:'+open("../gem/wp3.json").read().strip()+',redtruck:"'+open("../gem/redtruck.b64").read().strip()+'",s6a:"'+open("../gem/s6a.b64").read().strip()+'",s6b:"'+open("../gem/s6b.b64").read().strip()+'",s6c:"'+open("../gem/s6c.b64").read().strip()+'",s6d:"'+open("../gem/s6d.b64").read().strip()+'",s6e:"'+open("../gem/s6e.b64").read().strip()+'",plop:"'+open("../gem/plop.b64").read().strip()+'",treats:"'+open("../gem/treats.b64").read().strip()+'",applefacts:"'+open("../gem/applefacts.b64").read().strip()+'",petsgraph:"'+open("../gem/petsgraph.b64").read().strip()+'",henfacts:"'+open("../gem/henfacts.b64").read().strip()+'",orchnews:"'+open("../gem/orchnews.b64").read().strip()+'",twostep:"'+open("../gem/twostep.b64").read().strip()+'",twigs:"'+open("../gem/twigs.b64").read().strip()+'",pies24:"'+open("../gem/pies24.b64").read().strip()+'",crate4:"'+open("../gem/crate4.b64").read().strip()+'",piehalf:"'+open("../gem/piehalf.b64").read().strip()+'",lnpilot:"'+open("../gem/lnpilot.b64").read().strip()+'",lntable:"'+open("../gem/lntable.b64").read().strip()+'",ladder:"'+open("../gem/ladder.b64").read().strip()+'",sqhog:"'+open("../gem/sqhog.b64").read().strip()+'",beepoll:"'+open("../gem/beepoll.b64").read().strip()+'",apples:'+_js.dumps(_js.load(open("../gem/apples.json")),separators=(",",":"))+'};</script>\n<script>TP.register({id:"lp1-gtk"',1)
must("fig:function(){return nrow(1,'<div style=\"display:flex;flex-direction:column;gap:10px\">'+C.tapeBar(150","fig:function(){if(lp===1)return '<div class=\"figure\" style=\"margin:8px 0\"><div style=\"position:relative;display:inline-block;margin-left:46px;max-width:calc(100% - 46px)\"><b class=\"tkx-n\" style=\"position:absolute;left:-46px;top:10%\">1</b><b class=\"tkx-n\" style=\"position:absolute;left:-46px;top:46%\">2</b><b class=\"tkx-n\" style=\"position:absolute;left:-46px;top:78%\">3</b><img alt=\"Row 1: a short purple ribbon above a long red ribbon. Row 2: a rock and a feather. Row 3: a big blue bucket and a small red bucket.\" src=\"data:image/webp;base64,'+window.TP_IMG1.cmp+'\" style=\"width:560px;max-width:100%;height:auto;border-radius:18px;display:block\"></div></div>';return nrow(1,'<div style=\"display:flex;flex-direction:column;gap:10px\">'+C.tapeBar(150")
must("Which one can hold more? (the big bucket)","Which one can hold more? (the big blue bucket)")
must('{id:2,title:"Sound Games",short:"Sounds",parts:[{std:["RF.K.2"],n:6,dur:90,','{id:2,title:"Sound Games",short:"Sounds",parts:[{std:["RF.K.2"],n:6,dur:90,picSup:true,fig:()=>`<div class="figure" style="gap:14px;flex-wrap:wrap">${["cat","topHat","ladybug","butterfly","sun","map","dog"].map(n=>`<div>${ico(n,84)}</div>`).join("")}</div>`,')
must('(p.std||[]).some(c=>/FLS\\.2\\.4$/.test(c))','(p.std||[]).some(c=>/FLS\\.2\\.4$|^RF\\.K\\.[13]$/.test(c))')
must('dir:"Look at the page. Point or answer out loud.",desc:"print concepts','dir:(lp===1?"Look at the book. Point or answer out loud.":"Look at the page. Point or answer out loud."),desc:"print concepts')
must("html:function(){return'<div style=\"text-align:center\"><div class=\"kx-pg\"><div class=\"kx-ti\">'","html:function(){if(lp===1)return'<div style=\"text-align:center\"><img alt=\"Book cover: Pete the Pirate Finds the Treasure\" src=\"data:image/webp;base64,'+window.TP_IMG1.book+'\" style=\"width:230px;max-width:100%;height:auto;display:inline-block;margin:4px 0 14px\"></div><div style=\"text-align:center\"><div class=\"kx-pg\"><div class=\"kx-ln\">'+W(d.a)+'</div><div class=\"kx-ln\">'+W(d.b)+'</div></div></div>';return'<div style=\"text-align:center\"><div class=\"kx-pg\"><div class=\"kx-ti\">'")
must('key:["Say: This is a page from a book. Point to the title. (the big words in the banner at the top: "+d.t+". If the student cannot point on the screen, they can tell you where it is.)","Ask: Where do I start reading?','key:[lp===1?"Say: This is the cover of a book. Point to the title. (the big words on the banner at the top: Pete the Pirate Finds the Treasure. If the student cannot point on the screen, they can tell you where it is.)":"Say: This is a page from a book. Point to the title. (the big words in the banner at the top: "+d.t+". If the student cannot point on the screen, they can tell you where it is.)",(lp===1?"Say: Now look at the page under the cover. ":"")+"Ask: Where do I start reading?')
must('desc:"reading a short emergent-reader book",html:()=>`<p class="passage" style="font-size:2.2rem;line-height:1.9">I see a cat.<br>I see the cat.<br>I like the cat.','desc:"reading a short emergent-reader book",picSup:true,fig:()=>\'<div class="figure" style="margin:10px 0"><img alt="Eight small picture cards of a cat, each with the same sentence as the book" src="data:image/webp;base64,\'+window.TP_IMG1.cats+\'" style="width:640px;max-width:100%;height:auto"></div>\',html:()=>`<p class="passage" style="font-size:2.2rem;line-height:1.9">I see a cat.<br>I see the cat.<br>I like the cat.')
must('desc:"asking and answering key detail questions about story lines read aloud to the student",html:()=>`<p class="huge" aria-hidden="true" style="margin:6px 0">${ico("cat",96)}</p>','desc:"asking and answering key detail questions about story lines read aloud to the student",picSup:true,fig:()=>\'<div class="figure" style="margin:10px 0"><img alt="Three picture cards: a cat on a mat, a big bug on a leaf, and a cat about to get the bug" src="data:image/webp;base64,\'+window.TP_IMG1.lines+\'" style="width:680px;max-width:100%;height:auto"></div>\',html:()=>`<p class="huge" aria-hidden="true" style="margin:6px 0">${ico("cat",96)}</p>')
must('html:()=>`<p class="huge" aria-hidden="true" style="margin:6px 0">${ico("cat",96)}</p><p class="passage" style="font-size:2.2rem;line-height:1.9;margin:0 auto;width:fit-content">The cat sat on my mat.','html:()=>`<p class="passage" style="font-size:2.2rem;line-height:1.9;margin:0 auto;width:fit-content">The cat sat on my mat.')
must('desc:"answering key detail questions about a story read aloud",html:()=>`<p class="huge" aria-hidden="true" style="margin:6px 0">${ico("bear",96)}</p>','desc:"answering key detail questions about a story read aloud",picSup:true,fig:()=>\'<div class="figure" style="margin:10px 0"><img alt="Four picture cards of the story: Ben the bear cannot find his red hat, he looks under his bed, he looks in the kitchen, and his mom points at the hat on his head" src="data:image/webp;base64,\'+window.TP_IMG1.bear+\'" style="width:680px;max-width:100%;height:auto"></div>\',html:()=>`<p class="huge" aria-hidden="true" style="margin:6px 0">${ico("bear",96)}</p>')
must('desc:"describing a favorite place with details",html:()=>`<p class="big">Tell me about your favorite place to play.</p>`','desc:"describing a favorite place with details",picSup:true,fig:()=>\'<div class="figure" style="margin:10px 0"><img alt="Six picture cards of places to play: a playground, a park with a bench and a ball, a beach with a sand castle, a yard with a tricycle, a playroom with a teddy bear and blocks, and a snowy hill with a sled" src="data:image/webp;base64,\'+window.TP_IMG1.places+\'" style="width:720px;max-width:100%;height:auto"></div>\',html:()=>`<p class="big">Tell me about your favorite place to play.</p>`')
must('desc:"spoken grammar items (plural nouns, question words, complete sentences)",html:()=>`<p class="huge" aria-hidden="true">${ico("speak",96)}</p>`','desc:"spoken grammar items (plural nouns, question words, complete sentences)",picSup:true,fig:()=>\'<div class="figure" style="margin:10px 0"><img alt="Four picture cards: two dogs with One dog, two blank; a girl wishing on one star and two stars with One wish, two blank; a girl asking Where is the ball with a ball nearby; and blue shoes with My shoes are blue" src="data:image/webp;base64,\'+window.TP_IMG1.wordfun+\'" style="width:720px;max-width:100%;height:auto"></div>\',html:()=>`<p class="huge" aria-hidden="true">${ico("speak",96)}</p>`')
must('desc:"addition and subtraction word problems and facts within 10",qs:["3 frogs sit on a log.','desc:"addition and subtraction word problems and facts within 10",picSup:true,fig:()=>\'<div class="figure" style="margin:10px 0"><img alt="Four picture cards: 3 frogs on a log and 2 more hopping on; 6 birds in a tree and 2 flying away; 4 apples plus 1 apple; and 7 stars with 3 crossed out" src="data:image/webp;base64,\'+window.TP_IMG1.addtake+\'" style="width:720px;max-width:100%;height:auto"></div>\',qs:["3 frogs sit on a log.')
must('sv(228,100,cl(oa,12),"A group of "+oa)','sv(228,100,cl(oa,22),"A group of "+oa)')
must('html:function(){if(lp===1)return\'<div style="text-align:center"><img alt="Book cover: Pete the Pirate Finds the Treasure" src="data:image/webp;base64,\'+window.TP_IMG1.book+\'"','html:function(){if(lp===1||lp===2)return\'<div style="text-align:center"><img alt="\'+(lp===2?"Book cover: A Visit to the Apple Orchard":"Book cover: Pete the Pirate Finds the Treasure")+\'" src="data:image/webp;base64,\'+(lp===2?window.TP_IMG1.cover2:window.TP_IMG1.book)+\'"')
must('dir:(lp===1?"Look at the book. Point or answer out loud.":','dir:(lp<3?"Look at the book. Point or answer out loud.":')
must('key:[lp===1?"Say: This is the cover of a book. Point to the title. (the big words on the banner at the top: Pete the Pirate Finds the Treasure.','key:[lp<3?"Say: This is the cover of a book. Point to the title. (the big words on the banner at the top: "+(lp===2?"A Visit to the Apple Orchard":"Pete the Pirate Finds the Treasure")+".')
must('(lp===1?"Say: Now look at the page under the cover. ":"")','(lp<3?"Say: Now look at the page under the cover. ":"")')
must('function apple(x,y,s,col){','function appleImg(i,c){const T=window.TP_IMG1&&window.TP_IMG1.apples;if(!T||!T.length)return sv(apple(0,0,1.25,c));const k=T[i%T.length],h=76*k[2]/k[1];return sv(`<image href="data:image/webp;base64,${k[0]}" x="-38" y="${-h/2}" width="76" height="${h}"/>`,"-40 -40 80 80")}function appleSm(i){const T=window.TP_IMG1&&window.TP_IMG1.apples;if(!T||!T.length)return`<svg viewBox="-32 -32 64 64" width="22" height="22" aria-hidden="true">${apple(0,0,1)}</svg>`;const k=T[i%T.length],h=60*k[2]/k[1];return`<svg viewBox="-32 -32 64 64" width="24" height="24" aria-hidden="true"><image href="data:image/webp;base64,${k[0]}" x="-30" y="${-h/2}" width="60" height="${h}"/></svg>`}function apple(x,y,s,col){')
must('itemSvg:c=>sv(apple(0,0,1.25,c)),itemSmall:i=>`<svg viewBox="-32 -32 64 64" width="22" height="22" aria-hidden="true">${apple(0,0,1,["#F4796F","#F7D08A","#A8D49A"][i%3])}</svg>`,','itemSvg:(c,n)=>appleImg(n||0,c),itemSmall:i=>appleSm(0),')
must('html:()=>`<div class="figure" style="align-items:center">${ladder()}${F.pic(TREE,"","9rem")}</div>`,key:["Say: Climb the ladder','key:["Say: Climb the ladder')
must('["#4FC3F7","#E57373","#81C784","#BA68C8","#FFD54F"][c%5])}</div>','["#4FC3F7","#E57373","#81C784","#BA68C8","#FFD54F"][c%5],c)}</div>')
must('<p class="big" style="text-align:center">10 apples in every crate</p>`,key:["Say: Every crate holds 10 apples.','<p class="big" style="text-align:center">10 apples in every crate</p>`,picSup:true,fig:()=>\'<div style="display:flex;flex-wrap:wrap;justify-content:center;gap:8px 12px;max-width:560px;margin:8px auto" role="img" aria-label="10 crates of apples, each crate labeled 10">\'+Array(10).fill(\'<img alt="" src="data:image/webp;base64,\'+window.TP_IMG1.crate10+\'" style="width:100px;height:auto">\').join("")+\'</div>\',key:["Say: Every crate holds 10 apples.')
must('html:()=>`<div style="text-align:center">${grp(CRATE,10,5,"3.4rem")}</div><p class="big" style="text-align:center">10 apples','html:()=>`<p class="big" style="text-align:center">10 apples')
must('html:()=>`<div class="figure">${F.pic(BEE,"bee")}${F.pic(TREE,"tree")}${F.pic(AP,"apple")}${F.pic(CRATE,"crate")}</div>`','html:()=>\'<div style="text-align:center;margin:8px 0"><img alt="Rhyming Words picture card: bee and tree, apple and crate, weed and log for seed, stem and stick for pick, and a pie" src="data:image/webp;base64,\'+window.TP_IMG1.rhymecard+\'" style="width:720px;max-width:100%;height:auto;border-radius:16px"></div>\'')
must('html:()=>`<div class="figure">${F.pic(CLAP)}${F.pic(EAR)}${F.pic(LADYBUG)}</div>`,key:["Say: Clap the parts in apple.','html:()=>\'<div style="text-align:center;margin:8px 0"><img alt="Six pictures: apple, tree, ladybug, beehive, bee, and barn" src="data:image/webp;base64,\'+window.TP_IMG1.clapset+\'" style="width:600px;max-width:100%;height:auto"></div>\',key:["Say: Clap the parts in apple.')
must('html:()=>`<div class="figure">${F.pic(SQUIRREL,"","6rem")}${F.pic(AP,"","6rem")}${F.pic(BIRD,"","6rem")}</div>`,read:STORY','picSup:true,fig:()=>\'<div style="text-align:center;margin:8px 0"><img alt="Six story pictures in order: a squirrel looks up at an apple, jumps for it, shakes the branch, a bluebird flies over, the apple falls, and the squirrel and bluebird share the apple" src="data:image/webp;base64,\'+window.TP_IMG1.squirrel+\'" style="width:720px;max-width:100%;height:auto;border-radius:16px"></div>\',read:STORY')
must('html:()=>`<div class="figure" style="align-items:center">${F.pic(AP,"","6rem")}${F.pic(DROP,"","4rem")}${F.pic(HOTDRINK,"","6rem")}</div>`,read:CIDER','picSup:true,fig:()=>\'<div style="text-align:center;margin:8px 0"><img alt="Five pictures in order: children pick apples, the apples are washed in a tub, a press squeezes the apples and cider pours into a jug, the jug of cider sits next to a warm mug, and the children drink cider" src="data:image/webp;base64,\'+window.TP_IMG1.cidersteps+\'" style="width:720px;max-width:100%;height:auto;border-radius:16px"></div>\',read:CIDER')
must('fig:()=>`<div class="figure">${standFig()}</div>`,qs:["What shape is the roof?"','fig:()=>\'<div style="text-align:center;margin:8px 0"><img alt="A farm stand with a red triangle roof, a green rectangle door, and a round window. A bee sits above the roof. A barrel of sunflowers and a crate of apples are beside the stand, and an apple is below the window." src="data:image/webp;base64,\'+window.TP_IMG1.farmstand+\'" style="width:600px;max-width:100%;height:auto;border-radius:16px"></div>\',qs:["What shape is the roof?"')
must('"Triangle","Rectangle","Circle","The bee","The crate","Below the window','"Triangle","Rectangle","Circle","The bee","The crate. Also accept the barrel of sunflowers.","Below the window')
must('html:()=>`<div class="figure">${F.pic(BEE,"","6rem")}${F.pic(TALK,"","6rem")}</div>`,key:["Say: One apple, two ____. (apples)"','picSup:true,fig:()=>\'<div style="text-align:center;margin:8px 0"><img alt="Picture cards: one apple and two apples, one peach and two peaches, a girl thinking of a question, a tree, and a bee flying to a flower" src="data:image/webp;base64,\'+window.TP_IMG1.saybee+\'" style="width:600px;max-width:100%;height:auto;border-radius:16px"></div>\',key:["Say: One apple, two ____. (apples)"')
must('html:()=>`<div class="figure">${F.pic(PENCIL,"","6rem")}</div>`,key:["Say: Write the first letter','key:["Say: Write the first letter')
must('desc:"asking and answering questions about key details in an informational text read aloud",html:()=>`<div class="figure">${F.pic(BEE,"","6rem")}${F.pic(FLOWER,"","6rem")}${F.pic(HONEY,"","6rem")}</div>`,key:["Read the facts out loud once.','desc:"asking and answering questions about key details in an informational text read aloud",html:()=>`<div class="figure">${F.pic(BEE,"","6rem")}${F.pic(FLOWER,"","6rem")}${F.pic(HONEY,"","6rem")}</div>`,picSup:true,fig:()=>\'<div style="text-align:center;margin:8px 0"><img alt="How an apple grows with help from bees: a bee with pollen on a blossom, the bee drinking from the blossom, a small green apple, and a ripe red apple. A bee flies near a hive, honey sits on a table, and a farmer gives a thumbs up." src="data:image/webp;base64,\'+window.TP_IMG1.beefacts+\'" style="width:600px;max-width:100%;height:auto;border-radius:16px"></div>\',key:["Read the facts out loud once.')
must('html:()=>bookFig(),key:["Count the words the student reads correctly, out of 31','html:()=>\'<div style="text-align:center;margin:8px 0"><img alt="Little book page: I see an apple. It is red. I see a pear. It is not red. The apple is big. The pear is little. I can get an apple. I like it. A farm stand with an apple, a pear, and a basket of apples is beside the words." src="data:image/webp;base64,\'+window.TP_IMG1.littlebook+\'" style="width:680px;max-width:100%;height:auto;border-radius:18px"></div>\',key:["Count the words the student reads correctly, out of 31')
must('html:()=>`<div class="figure">${F.pic(AP,"","5rem")}${F.pic(HOTDRINK,"","5rem")}</div><p class="big">Which do you like better','html:()=>`<div style="display:flex;flex-wrap:wrap;justify-content:center;gap:14px;margin:8px 0"><img alt="Four children pick red apples from a tree and hold a basket of apples" src="data:image/webp;base64,${window.TP_IMG1.pick2}" style="width:340px;max-width:100%;height:auto;border-radius:16px"><img alt="Five children smile and drink warm apple cider from mugs with apples on them" src="data:image/webp;base64,${window.TP_IMG1.cider2}" style="width:340px;max-width:100%;height:auto;border-radius:16px"></div><p class="big">Which do you like better')
must('three dimensional shapes",fig:()=>`<div class="figure">${flatSolidFig()}</div>`,','three dimensional shapes",fig:()=>`<div style="text-align:center;margin:8px 0"><img alt="Four shape cards: 1 a yellow circle, 2 a purple square, 3 a blue cube, 4 a red can shape" src="data:image/webp;base64,${window.TP_IMG1.flat4}" style="width:760px;max-width:100%;height:auto;border-radius:16px"></div>`,')
must('spots:{sky:[[100,54],[150,16],[160,58],[196,62],[138,40],[252,22],[172,36]],air:[[100,86],[198,84],[148,76],[160,96],[120,100],[200,100]],ground:[[120,128],[160,124],[200,128],[100,142],[140,140],[180,140],[220,142],[120,156],[160,154],[200,156],[110,174],[210,174],[160,196],[90,210],[230,210],[160,228]]}','spots:{sky:[[150,34],[112,48],[205,50]],air:[[112,72],[208,76],[160,90],[130,100],[190,100]],ground:[[155,178],[65,200],[245,198],[100,150],[215,152],[38,170],[285,172],[130,224],[195,220],[95,182],[225,178],[160,150],[40,224],[280,224],[155,202],[105,206]]},zoneOf:{bluebird:"air"}')
must('const z=stickerZone(st),a=pick(z);','const z=theme.zoneOf&&theme.zoneOf[st]||stickerZone(st),a=pick(z);')
must('const PIC=(e,px)=>{if(typeof e!=="string"||!window.TP_ICON)return null;','const PIC=(e,px)=>{if(typeof e==="string"&&/^apple:\\d$/.test(e)&&window.TP_IMG1&&window.TP_IMG1.apples){const k=window.TP_IMG1.apples[+e.slice(6)%10],h=px*k[2]/k[1];return`<svg viewBox="0 0 ${px} ${px}" width="${px}" height="${px}" aria-hidden="true"><image href="data:image/webp;base64,${k[0]}" x="0" y="${(px-h)/2}" width="${px}" height="${h}"/></svg>`}if(typeof e!=="string"||!window.TP_ICON)return null;')
must('const PICXY=(x,y,e,px)=>typeof e==="string"&&window.TP_ICON_G?','const PICXY=(x,y,e,px)=>typeof e==="string"&&/^apple:\\d$/.test(e)&&window.TP_IMG1&&window.TP_IMG1.apples?(()=>{const k=window.TP_IMG1.apples[+e.slice(6)%10],h=px*k[2]/k[1];return`<image href="data:image/webp;base64,${k[0]}" x="${x-px/2}" y="${y-h/2}" width="${px}" height="${h}"/>`})():typeof e==="string"&&window.TP_ICON_G?')
must('grp(AP,5,5)+VS+grp(LEMON,5,5)','grp("apple:2",5,5)+VS+grp(LEMON,5,5)')
must('grp(CRATE,7,4)+VS+grp(AP,8,4)','grp(CRATE,7,4)+VS+grp("apple:4",8,4)')
must('grp(PEAR,9,5)+VS+grp(AP,10,5)','grp(PEAR,9,5)+VS+grp("apple:5",10,5)')
must('${grp(AP,7,7,"2.6rem")}','${grp("apple:6",7,7,"2.6rem")}')
must('${grp(AP,5,5,"2.6rem")}','${grp("apple:8",5,5,"2.6rem")}')
must('${grp(AP,3,3,"2.6rem")}','${grp("apple:8",3,3,"2.6rem")}')
must('${grp(AP,10,5,"2.4rem")}','${grp("apple:2",10,5,"2.4rem")}')
must('${grp(AP,4,4,"2.4rem")}','${grp("apple:2",4,4,"2.4rem")}')
must('${grp(AP,3,3,"2.4rem")}','${grp("apple:4",3,3,"2.4rem")}')
must('${grp(AP,8,4,"2.4rem")}','${grp("apple:4",8,4,"2.4rem")}')
must('${grp(AP,7,7,"3rem")}','${grp("apple:9",7,7,"3rem")}')
must('${F.pic(AP,"","6rem")}</div><p class="big">Draw an apple.','${F.pic("apple:2","","6rem")}</div><p class="big">Draw an apple.')
must('html:()=>`<div class="figure">${F.pic(BEE,"","6rem")}${F.pic(FLOWER,"","6rem")}${F.pic(HONEY,"","6rem")}</div>`,picSup:true,','picSup:true,')
must('html:()=>`<p class="huge" aria-hidden="true">${ico("ear",96)} ${ico(BEE,96)}</p><p class="big" style="text-align:center">Listen. Then say it.</p>`,','html:()=>`<div style="text-align:center;margin:8px 0"><img alt="Six pictures: a ladybug on leaves, a garden shed, a jar of strawberry jam, a walnut, a girl picking apples, and a dripping faucet" src="data:image/webp;base64,${window.TP_IMG1.g1sounds}" style="width:680px;max-width:100%;height:auto;border-radius:16px"></div><p class="big" style="text-align:center">Listen. Then say it.</p>`,')
must('dir:"Count out loud like a hopping bee. Say each answer."','dir:"Listen to each question. Count on or count back. Use your fingers if you want. Say each answer out loud."')
must('function letterPicHtml(p,w){if(!ui().pics||!isLetterWords(p))return"";','function letterPicHtml(p,w){if(p.wordPics&&ui().pics){const mp=window.TP_IMG1&&(p.wordPics===2?window.TP_IMG1.wp2:window.TP_IMG1.wp),k=mp&&mp[w];return k?`<div class="letter-pic" style="display:flex;justify-content:center;margin:-4px 0 10px"><img alt="" src="data:image/webp;base64,${k}" style="height:150px;width:auto"></div>`:""}if(!ui().pics||!isLetterWords(p))return"";')
_k='std:["RF.1.3"],kind:"words",words:WORDS,n:12,'
_i=s.index('TP.register({id:"lp3-g1"');_j=s.index(_k,_i)
assert _j<s.index('TP.register({id:"lp3-g2"')
s=s[:_j]+'std:["RF.1.3"],kind:"words",words:WORDS,wordPics:1,n:12,'+s[_j+len(_k):]
must('const pi=+box.dataset.words,p=ps[pi];if(p&&isLetterWords(p)){box.innerHTML=wordsHtml(p,pi);','const pi=+box.dataset.words,p=ps[pi];if(p&&(isLetterWords(p)||p.wordPics)){box.innerHTML=wordsHtml(p,pi);')
must('html:()=>`<p class="huge" style="font-size:3rem;margin:0" aria-hidden="true">${ico("truck",48)}</p>${story("The Red Truck",TRUCK)}`','html:()=>`<p style="text-align:center;margin:0 0 8px"><img alt="A red pickup truck with a smiling windshield" src="data:image/webp;base64,${window.TP_IMG1.redtruck}" style="height:120px;width:auto"></p>${story("The Red Truck",TRUCK)}`')
must('fig:()=>`<div class="figure">${F.objects(APPLE,4)}${F.objects("apple",3)}</div>`,qs:["There are 4 red apples and 3 green apples','qon:[()=>`<div style="text-align:center;margin:6px 0 4px"><img alt="A basket with 4 red apples and 3 green apples" src="data:image/webp;base64,${window.TP_IMG1.s6a}" style="width:300px;max-width:100%;height:auto"></div>`,()=>`<div style="text-align:center;margin:6px 0 4px"><img alt="A boy with 6 apples, then 3 more apples, and an empty answer box" src="data:image/webp;base64,${window.TP_IMG1.s6b}" style="width:640px;max-width:100%;height:auto"></div>`,()=>`<div style="text-align:center;margin:6px 0 4px"><img alt="A girl by a flower with 8 bees on it, 5 bees flying away, and an empty answer box" src="data:image/webp;base64,${window.TP_IMG1.s6d}" style="width:560px;max-width:100%;height:auto"></div>`,()=>`<div style="text-align:center;margin:6px 0 4px"><img alt="A girl making jam: 5 jars, plus a question mark, equals 9 jars" src="data:image/webp;base64,${window.TP_IMG1.s6e}" style="width:640px;max-width:100%;height:auto"></div>`,()=>`<div style="text-align:center;margin:6px 0 4px"><img alt="Two cider stands: one stand has 8 jugs and the other has 7 jugs" src="data:image/webp;base64,${window.TP_IMG1.s6c}" style="width:680px;max-width:100%;height:auto"></div>`],qs:["There are 4 red apples and 3 green apples')
must('Lee sells 9 jugs of cider.','Lee sells 8 jugs of cider.')
must('"16 jugs. Writes 9 + 7 = 16"','"15 jugs. Writes 8 + 7 = 15"')
must('<li>${q}${(p.qfig&&p.qfig[qi]||p.qsup&&p.qsup[qi])&&sceneSup(p)?','<li>${q}${p.qon&&p.qon[qi]?call(p.qon[qi]):""}${(p.qfig&&p.qfig[qi]||p.qsup&&p.qsup[qi])&&sceneSup(p)?')
must('html:()=>story("Plop!",PLOP),qs:[','html:()=>story("Plop!",PLOP),picSup:true,fig:()=>`<div style="text-align:center;margin:8px 0"><img alt="A girl kneels by a metal tub of plums under a plum tree while a pink pig eats a plum" src="data:image/webp;base64,${window.TP_IMG1.plop}" style="width:600px;max-width:100%;height:auto;border-radius:16px"></div>`,qs:[')
must('fig:()=>`<div class="figure" style="align-items:center">${tens(2,3)}${plus()}${tens(0,4)}</div>`,qs:["Look at the blocks. What is 23 + 4?"','qon:[()=>`<div class="figure" style="align-items:center">${tens(2,3)}${plus()}${tens(0,4)}</div>`,()=>`<div class="figure" style="align-items:center">${tens(4,1)}${plus()}${tens(0,5)}</div>`,()=>`<div class="figure" style="align-items:center">${tens(1,5)}${plus()}${tens(1,0)}</div>`,()=>`<div class="figure" style="align-items:center">${tens(3,2)}${plus()}${tens(2,0)}</div>`,()=>`<div class="figure" style="align-items:center">${tens(1,8)}${plus()}${tens(0,5)}</div>`],qs:["Look at the blocks. What is 23 + 4?"')
must('${pics([["cake","apple cake"],["cocoa","apple cider"],[APPLE,"a fresh apple"]])}${TWO}`,key:["Names the topic: apple treats','<div style="text-align:center;margin:14px 0"><img alt="An apple cake slice, a mug of apple cider with a red apple, and a caramel apple" src="data:image/webp;base64,${window.TP_IMG1.treats}" style="width:760px;max-width:100%;height:auto"></div>${TWO}`,key:["Names the topic: apple treats')
must('<p class="big">Write about apples. Tell 2 facts you know.</p>${pics([[APPLE,"colors"],["tree","where they grow"],["face","how they taste"]])}${TWO}`,key:','<p class="big">Write about apples. Tell 2 facts you know.</p>${TWO}`,picSup:true,fig:()=>`<div style="text-align:center;margin:8px 0"><img alt="Apple colors: red, green, yellow. Where they grow: on a tree. How they taste: sweet, tart, crisp" src="data:image/webp;base64,${window.TP_IMG1.applefacts}" style="width:620px;max-width:100%;height:auto;border-radius:16px"></div>`,key:')
must('html:()=>`<p class="huge" style="font-size:3rem;margin:0" aria-hidden="true">${ico("hen",48)} ${ico("egg",48)} ${ico("hatchChick",48)}</p>${story("Hens",HENS)}`','html:()=>`<div style="text-align:center;margin:6px 0 12px"><img alt="A hen sits on a nest of five eggs. Three chicks hatch from eggs. A wet chick dries and turns fluffy. Five chicks follow the hen across the yard." src="data:image/webp;base64,${window.TP_IMG1.henfacts}" style="width:640px;max-width:100%;height:auto;border-radius:16px"></div>${story("Hens",HENS)}`')
must('"Six eggs","Peck and run"','"Five eggs","Peck and run"')
must('html:()=>`<p class="huge" style="font-size:3rem;margin:0" aria-hidden="true">${ico("ear",48)} ${ico("tractor",48)}</p><p class="big" style="text-align:center">Listen only. The news is not on your screen.</p>`','picSup:true,html:()=>"",fig:()=>`<div style="text-align:center;margin:8px 0"><img alt="A Hill Top Orchard news sign: picking starts Saturday at nine, bring your own basket, the wagon ride leaves from the big red barn every hour, the cider press runs all day, and a cup of cold cider is free for anyone who picks a full basket" src="data:image/webp;base64,${window.TP_IMG1.orchnews}" style="width:720px;max-width:100%;height:auto;border-radius:16px"></div>`')
must('dir:"Look at the blocks. Answer out loud.",fig:()=>`<div class="figure">${tens(4,6)}</div>`,qs:["How many tens','dir:"Look at the blocks. Answer out loud.",qs:["How many tens')
must('dir:"Subtract. Say each answer out loud.",fig:()=>`<div class="figure">${tens(6,0)}</div>`,qs:["60 - 20"','dir:"Subtract. Say each answer out loud.",qs:["60 - 20"')
must('qs:["How many tens and how many ones? What number is this?"','qon:[()=>`<div class="figure" style="align-items:center;margin:6px 0 10px">${tens(4,6)}</div>`],qsup:[null,()=>`<div class="figure" style="align-items:center;margin:6px 0 10px">${tens(4,6)}</div>`,()=>`<div class="figure" style="align-items:center;margin:6px 0 10px">${tens(3,0)}</div>`],qs:["How many tens and how many ones? What number is this?"')
must('qs:["60 - 20","90 - 40","70 - 70"]','qsup:[()=>`<div class="figure" style="align-items:center;margin:6px 0 10px">${tens(6,0)}</div>`,()=>`<div class="figure" style="align-items:center;margin:6px 0 10px">${tens(9,0)}</div>`,()=>`<div class="figure" style="align-items:center;margin:6px 0 10px">${tens(7,0)}</div>`],qs:["60 - 20","90 - 40","70 - 70"]')
must('qs:["You know 4 + 9 = 13. So what is 9 + 4?','qsup:[()=>`<div class="figure" style="align-items:center;margin:6px 0 10px">${tens(0,9)}${plus()}${tens(0,4)}</div>`,()=>`<div class="figure" style="align-items:center;margin:6px 0 10px">${tens(0,8)}${plus()}${tens(0,2)}${plus()}${tens(0,6)}</div>`],qs:["You know 4 + 9 = 13. So what is 9 + 4?')
must('fig:()=>`<div class="figure">${unitMeasure()}</div>`,qs:["The apple cards','fig:()=>`<div style="text-align:center;margin:8px 0"><img alt="Twig A is as long as 6 apple cards. Twig B is as long as 4 apple cards." src="data:image/webp;base64,${window.TP_IMG1.twigs}" style="width:720px;max-width:100%;height:auto;border-radius:16px"></div>`,qs:["The apple cards')
must('fig:()=>`<div class="figure" style="align-items:center;gap:30px">${F.fracCircle(2,1,180)}${F.gridRect(1,4,1,{cell:56})}</div>`,qs:["The pie is cut','fig:()=>`<div style="display:flex;align-items:center;justify-content:center;gap:30px;flex-wrap:wrap;margin:8px 0"><img alt="A pie cut into 2 equal parts. One part is cherry and one part is crust." src="data:image/webp;base64,${window.TP_IMG1.piehalf}" style="height:190px;width:auto;max-width:100%"><img alt="A wooden crate top cut into 4 equal parts" src="data:image/webp;base64,${window.TP_IMG1.crate4}" style="width:380px;max-width:100%;height:auto"></div>`,qsup:[null,null,()=>`<div style="text-align:center;margin:6px 0 10px"><img alt="Two pies. One is cut into 2 equal parts. The other is cut into 4 equal parts." src="data:image/webp;base64,${window.TP_IMG1.pies24}" style="width:520px;max-width:100%;height:auto"></div>`],qs:["The pie is cut')
must('dir:"Look at the apple pie and the crate top. Answer out loud."','dir:"Look at the pie and the crate top. Answer out loud."')
must('.board{grid-template-columns:minmax(0,1fr) 290px;align-items:start}','.board{grid-template-columns:minmax(0,1fr) 400px;align-items:start}')
must('.scene-card{max-width:420px}','.scene-card{max-width:680px}')
must('stickerSvg(st,a[0],a[1],theme.stickerSize||30,a[2])','stickerSvg(st,a[0],a[1],(theme.stickerSize||30)*1.3,a[2])')
must('id="sceneBig" viewBox="0 0 320 240" role="img" aria-label="${T.sceneTitle}" style="max-width:520px;margin:10px auto"','id="sceneBig" viewBox="0 0 320 240" role="img" aria-label="${T.sceneTitle}" style="max-width:800px;width:100%;margin:10px auto"')

_i=s.index('function sceneStickers(theme,list){');_j=s.index('function drawScene(svg){')
_NEW=r"""function sceneStickers(theme,list){const spots=theme.spots||{},used={},sz=theme.stickerSize?theme.stickerSize:39,pts=[];const pick=z=>{let k=z;if(!(spots[k]&&spots[k].length))k=z==="air"?"sky":"ground";if(!(spots[k]&&spots[k].length))k="ground";const list2=spots[k]&&spots[k].length?spots[k]:[[160,160]];const n=used[k]||0;used[k]=n+1;const p=list2[n%list2.length],lap=Math.floor(n/list2.length);return[p[0]+(lap%2?14:-14)*Math.ceil(lap/2),p[1]-(lap?4:0),k!=="sky"&&k!=="air",k]};const TL=[-11,8,-6,13,-9,5,-14,10,-4,12,-8,6,-13,9,-5,11,-10,7];list.forEach((st,ix)=>{const z=theme.zoneOf&&theme.zoneOf[st]||stickerZone(st),a=pick(z);pts.push({st,ix,x:a[0],y:a[1],g:a[2],k:a[3]})});const bb={};Object.keys(spots).forEach(k=>{const L=spots[k];if(!L||!L.length)return;let x0=1e9,x1=-1e9,y0=1e9,y1=-1e9;L.forEach(p=>{x0=Math.min(x0,p[0]);x1=Math.max(x1,p[0]);y0=Math.min(y0,p[1]);y1=Math.max(y1,p[1])});bb[k]=[x0-24,x1+24,y0-12,y1+12]});const D=sz*0.95;for(let it=0;it<80;it++){let moved=0;for(let i=0;i<pts.length;i++)for(let j=i+1;j<pts.length;j++){const A=pts[i],B=pts[j];let dx=B.x-A.x,dy=B.y-A.y,d=Math.hypot(dx,dy);if(d>=D)continue;if(d<.01){dx=(i%2?1:-1)*.5;dy=.3;d=Math.hypot(dx,dy)}const pu=(D-d)/2*.5,ux=dx/d,uy=dy/d;A.x-=ux*pu;A.y-=uy*pu;B.x+=ux*pu;B.y+=uy*pu;moved=1}pts.forEach(p=>{const b=bb[p.k];if(b){p.x=Math.min(b[1],Math.max(b[0],p.x));p.y=Math.min(b[3],Math.max(b[2],p.y))}else{p.x=Math.min(300,Math.max(20,p.x));p.y=Math.min(225,Math.max(20,p.y))}});if(!moved)break}let s="";pts.forEach(p=>{let o=stickerSvg(p.st,p.x,p.y,sz,p.g);if(theme.tilt)o=`<g transform="rotate(${TL[p.ix%TL.length]} ${p.x} ${p.y})">${o}</g>`;s+=o});return s}"""
s=s[:_i]+_NEW+s[_j:]
must('p_bunting p_lights p_disco".split(" ").forEach(n=>ZONE_BY_NAME[n]="sky");','p_bunting p_lights p_disco".split(" ").forEach(n=>ZONE_BY_NAME[n]="sky");ZONE_BY_NAME.bluebird="air";ZONE_BY_NAME.cardinal="air";')
must('std:["RF.2.3"],kind:"words",words:WORDS,n:12,dur:90,dir:"Read each word out loud. The last two are silly words.','std:["RF.2.3"],kind:"words",wordPics:2,words:WORDS,n:12,dur:90,dir:"Read each word out loud. The last two are silly words.')
must('title:"Story Questions",std:["RL.2.1"],dur:105,',"title:\"Story Questions\",std:[\"RL.2.1\"],dur:105,picSup:true,fig:()=>'<div style=\"text-align:center;margin:8px 0\"><img alt=\"Nell reaches for a big apple from a ladder while Omar holds it. Farmer Jo takes an apple from a girl, with a pie on a table by the red barn\" style=\"max-width:100%;width:640px;height:auto;border-radius:14px\" src=\"data:image/webp;base64,'+window.TP_IMG1.ladder+'\"></div>',")
must('I.apple=s=>SV(s,"apple",`','I.apple=s=>(window.TP_IMG1&&window.TP_IMG1.apples)?SV(s,"apple",(k=>`<image href="data:image/webp;base64,${k[0]}" x="-42" y="${-42*k[2]/k[1]}" width="84" height="${84*k[2]/k[1]}"/>`)(window.TP_IMG1.apples[0])):SV(s,"apple",`')
must('I.greenApple=s=>SV(s,"green apple",`','I.greenApple=s=>(window.TP_IMG1&&window.TP_IMG1.apples)?SV(s,"green apple",(k=>`<image href="data:image/webp;base64,${k[0]}" x="-42" y="${-42*k[2]/k[1]}" width="84" height="${84*k[2]/k[1]}"/>`)(window.TP_IMG1.apples[2])):SV(s,"green apple",`')
must('html:()=>passage("Squirrel and Hedgehog",FABLE),qs:["Tell what happened at the beginning',"html:()=>passage(\"Squirrel and Hedgehog\",FABLE),picSup:true,fig:()=>'<div style=\"text-align:center;margin:8px 0\"><img alt=\"Six pictures of Squirrel and Hedgehog with their apples: both with piles, Hedgehog walking with a basket, Squirrel carrying a big armful, apples rolling into the pond, Squirrel sitting sadly, and Hedgehog sharing apples with Squirrel\" style=\"max-width:100%;width:760px;height:auto;border-radius:14px\" src=\"data:image/webp;base64,'+window.TP_IMG1.sqhog+'\"></div>',qs:[\"Tell what happened at the beginning")
must('desc:"a short narrative with events in order, details, time words, and an ending",html:()=>`<p class="big">Think of a time you made, picked, or cooked something to eat.','desc:"a short narrative with events in order, details, time words, and an ending",picSup:true,fig:()=>(function(rows){var h=\'<div style="display:flex;flex-direction:column;align-items:flex-start;gap:10px;margin:10px 0">\';rows.forEach(function(r){h+=\'<div style="display:flex;align-items:center;flex-wrap:wrap;gap:10px;padding:8px 18px;border:3px dashed var(--line);border-radius:16px;background:var(--card,#fff);font-size:1.8rem;font-weight:700">\';r.forEach(function(w){h+=w.charAt(0)==="_"?\'<span style="display:inline-block;min-width:150px;border-bottom:4px solid var(--ink,#333);height:1.5em"></span>\':\'<span>\'+w+\'</span>\'});h+=\'</div>\'});return h+\'</div>\'})([["First, I", "_____", "."], ["Next, I", "_____", "."], ["Last, I", "_____", "."], ["I felt", "_____", "."]]),html:()=>`<p class="big">Think of a time you made, picked, or cooked something to eat.')
must('desc:"a short informative piece with a topic sentence, facts, and a closing",html:()=>`<p class="big">Write to teach a friend about apples.','desc:"a short informative piece with a topic sentence, facts, and a closing",picSup:true,fig:()=>(function(rows){var h=\'<div style="display:flex;flex-direction:column;align-items:flex-start;gap:10px;margin:10px 0">\';rows.forEach(function(r){h+=\'<div style="display:flex;align-items:center;flex-wrap:wrap;gap:10px;padding:8px 18px;border:3px dashed var(--line);border-radius:16px;background:var(--card,#fff);font-size:1.8rem;font-weight:700">\';r.forEach(function(w){h+=w.charAt(0)==="_"?\'<span style="display:inline-block;min-width:150px;border-bottom:4px solid var(--ink,#333);height:1.5em"></span>\':\'<span>\'+w+\'</span>\'});h+=\'</div>\'});return h+\'</div>\'})([["This is about", "_____", "."], ["One fact is", "_____", "."], ["Another fact is", "_____", "."], ["Now you know", "_____", "."]]),html:()=>`<p class="big">Write to teach a friend about apples.')
must('html:()=>passage("Bees in the Orchard",BEES),qs:["What do bees drink','html:()=>passage("Bees in the Orchard",BEES),picSup:true,fig:()=>\'<div style="text-align:center;margin:8px 0"><img alt="In spring, a bee visits apple blossoms, pollen sticks to its leg, it moves pollen to the next flower, and the flower grows into an apple. Spring flowers on the left, fall apples on the right" style="max-width:100%;width:760px;height:auto;border-radius:14px" src="data:image/webp;base64,\'+window.TP_IMG1.beepoll+\'"></div>\',qs:["What do bees drink')
must('std:["SL.2.2"],n:4,dur:90,read:CIDER,','std:["SL.2.2"],n:4,dur:90,read:CIDER,picSup:true,fig:()=>\'<div style="text-align:center;margin:8px 0"><img alt="Five pictures in order: children pick apples, the apples are washed in a tub, a press squeezes the apples and cider pours into a jug, the jug of cider sits next to a warm mug, and the children drink cider" src="data:image/webp;base64,\'+window.TP_IMG1.cidersteps+\'" style="width:720px;max-width:100%;height:auto;border-radius:16px"></div>\',')
must('<p class="huge" aria-hidden="true">${ico("apple",96)}${ico("cocoa",96)}</p><p class="big" style="text-align:center">Listen carefully. Your teacher will read about how apple cider is made.</p>','<p class="big" style="text-align:center">Listen carefully. Your teacher will read about how apple cider is made.</p>')
must('3/4 × 8/1 = 24/8 = 6','3/4 × 8/1 = 24/4 = 6')
must('a pumpkin growing on a vine")}const NIB','a pumpkin growing on a vine",900)}const NIB')
must('const poemHtml=()=>`<div class="poem" style="font-size:1.12rem;padding:10px 12px;white-space:nowrap">','const poemHtml=()=>`<div class="poem" style="font-size:1.12rem;padding:10px 12px;white-space:normal">',2)
must('{id:4,title:"Story Questions",parts:[{title:"Story Questions",std:["RL.1.1"],dur:90,qs:["What did the wind','{id:4,title:"Story Questions",parts:[{title:"Story Questions",std:["RL.1.1"],dur:90,dir:"Read the story out loud. Then listen to each question and answer out loud.",html:()=>`<p class="passage">${FABLE}</p>`,qs:["What did the wind')
must('{title:"Story Questions",std:["RL.1.1"],dur:90,qs:["Where was Nico','{title:"Story Questions",std:["RL.1.1"],dur:90,dir:"Read the story out loud. Then listen to each question and answer out loud.",html:()=>`<p class="passage">${STORY}</p>`,qs:["Where was Nico')
must('.lp-card b{font-family:var(--font-display);font-size:clamp(.92rem,1.7vw,1.15rem);line-height:1.15;overflow-wrap:anywhere;min-width:0}','.lp-card b{font-family:var(--font-display);font-size:clamp(.8rem,1.35vw,.95rem);line-height:1.15;overflow-wrap:break-word;min-width:0}')
must('wordCards(["we","go","is","me","he","and","topHat","log","pup"])','wordCards(["we","go","is","me","he","and","hat","log","pup"])')
must('[emo("purpleFlower"),"purpleFlower"]','[emo("purpleFlower"),"flower"]')
must('html:()=>story("A Big Job",JOB),qs:[','html:()=>story("A Big Job",JOB),picSup:true,fig:()=>`<div style="text-align:center;margin:8px 0"><img alt="Jill hugs a huge pumpkin, then tries to lift it. She runs to get Russ and his red wagon. They roll it up a ramp, pull the wagon up the hill, and win a blue ribbon" src="data:image/webp;base64,${window.TP_IMG1.wp.wagonpump}" style="width:720px;max-width:100%;height:auto;border-radius:16px"></div>`,qs:[')
must('html:()=>`<p class="huge" aria-hidden="true">${ico("ear",96)} ${ico(CORN,96)}</p><p class="big" style="text-align:center">Listen. Then say it.</p>`,key:["Blend: /v/','html:()=>`<div style="text-align:center;margin:8px 0"><img alt="Six pictures: a vine, a stack of books, a seed sprouting, corn growing in a row, a hay bale, and a straw hat" src="data:image/webp;base64,${window.TP_IMG1.wp.cornsounds}" style="width:680px;max-width:100%;height:auto"></div><p class="big" style="text-align:center">Listen. Then say it.</p>`,key:["Blend: /v/')
must('function pumpkin(x,y,s){s=s||1;return`<g transform="translate(${x},${','function pumpkin(x,y,s){s=s||1;const PI=window.TP_IMG1&&window.TP_IMG1.wp&&window.TP_IMG1.wp.pumpkinS;if(PI)return`<image href="data:image/webp;base64,${PI}" x="${x-34*s}" y="${y-34*s}" width="${68*s}" height="${68*s}"/>`;return pumpkinOld(x,y,s)}function pumpkinOld(x,y,s){s=s||1;return`<g transform="translate(${x},${')
must('std:["RF.1.3"],kind:"words",words:WORDS,n:12,dur:95,dir:"Read each word out loud. The last one is a silly word. Just sound it out.",','std:["RF.1.3"],kind:"words",words:WORDS,wordPics:1,n:12,dur:95,dir:"Read each word out loud. The last one is a silly word. Just sound it out.",')
must('${story("Frost",FROST)}`,key:["72 words,','${story("Frost",FROST)}`,picSup:true,fig:()=>`<div style="text-align:center;margin:8px 0"><img alt="Val runs up a frosty hill toward the pumpkin patch, stops to look at a chipmunk with a nut on a log, watches it run off, then carries a pumpkin up the steps at home" src="data:image/webp;base64,${window.TP_IMG1.wp.frost}" style="width:760px;max-width:100%;height:auto;border-radius:16px"></div>`,key:["72 words,')
_i3=s.index('TP.register({id:"lp3-g1"');_j3=s.index('TP.register({id:',_i3+10);_m3=s[_i3:_j3]
for _a,_b in [('dir:"Look at the chart. Write 1 sentence on your paper and hold it up."','dir:"Look at the pictures. Write 1 sentence on your paper and hold it up."'),
('What comes next? Use the chart.','What comes next? Use the pictures.'),
('fig:()=>growChart(),','fig:()=>`<div style="text-align:center;margin:8px 0"><img alt="Six pictures with arrows: a seed in soil, a sprout with roots, a vine with a flower, a small green pumpkin, a big orange pumpkin, and a happy ripe pumpkin in the sun" src="data:image/webp;base64,${window.TP_IMG1.wp.pumpgrow}" style="width:760px;max-width:100%;height:auto;border-radius:16px"></div>`,'),
('Finds the answer on the chart. Your help is fine','Finds the answer in the pictures. Your help is fine'),
('Writes an answer that uses the chart:','Writes an answer that uses the pictures:'),
('using a picture chart to answer','using pictures to answer'),('point to step 1 and read','point to the first picture and read')]:
    assert _a in _m3,_a
    _m3=_m3.replace(_a,_b)
s=s[:_i3]+_m3+s[_j3:]
_a='${story("Pumpkins",PUMP)}`,qs:["What kind of skin does a pumpkin have?"'
assert s_ if False else True
_i4=s.index('TP.register({id:"lp3-g1"');_j4=s.index('TP.register({id:',_i4+10);_m4=s[_i4:_j4]
_a='${story("Pumpkins",PUMP)}`,qs:['
assert _m4.count(_a)==1
_m4=_m4.replace(_a,'${story("Pumpkins",PUMP)}`,picSup:true,fig:()=>`<div style="text-align:center;margin:8px 0"><img alt="A smiling pumpkin on a vine with labels: it grows on a long stem, it has thick skin, sun and wet mud help it get big, it can get as big as a dog, and a cut pumpkin has wet pulp and seeds inside" src="data:image/webp;base64,${window.TP_IMG1.wp.pumpfacts}" style="width:760px;max-width:100%;height:auto;border-radius:16px"></div>`,qs:[')
s=s[:_i4]+_m4+s[_j4:]
must('function hay(x,y,s){s=s||1;return`<g transform="translate(${x},${y}) scale(${s})">','function hay(x,y,s){s=s||1;const HI=window.TP_IMG1&&window.TP_IMG1.wp&&window.TP_IMG1.wp.hayS;if(HI)return`<image href="data:image/webp;base64,${HI}" x="${x-32*s}" y="${y-30*s}" width="${64*s}" height="${60*s}"/>`;return hayOld(x,y,s)}function hayOld(x,y,s){s=s||1;return`<g transform="translate(${x},${y}) scale(${s})">')
must('function wagon(n,full){if(full)return','function wagon(n,full){if(!full&&window.TP_IMG1&&window.TP_IMG1.wp&&window.TP_IMG1.wp.wagonEmpty)return`<image href="data:image/webp;base64,${window.TP_IMG1.wp.wagonEmpty}" x="6" y="-4" width="252" height="134" preserveAspectRatio="xMidYMid meet"/>`;if(full)return')
_i5=s.index('TP.register({id:"lp3-g1"');_j5=s.index('TP.register({id:',_i5+10);_m5=s[_i5:_j5]
_a='${TWO}`,key:["Names the topic: fall (W.1.2)"'
assert _m5.count(_a)==1
_m5=_m5.replace(_a,'${TWO}`,picSup:true,fig:()=>`<div style="text-align:center;margin:8px 0"><img alt="Four fall pictures: a tree with falling red and orange leaves, a cold frosty field with a thermometer and snowflake sign, a basket of red apples under an apple tree, and a big pumpkin and a little pumpkin on the vine" src="data:image/webp;base64,${window.TP_IMG1.wp.fallfacts}" style="width:640px;max-width:100%;height:auto;border-radius:16px"></div>`,key:["Names the topic: fall (W.1.2)"')
s=s[:_i5]+_m5+s[_j5:]
_i6=s.index('TP.register({id:"lp3-g1"');_j6=s.index('TP.register({id:',_i6+10);_m6=s[_i6:_j6]
_a='Listen.</p>`,key:["Ask: What does a young sunflower'
assert _m6.count(_a)==1
_m6=_m6.replace(_a,'Listen.</p>`,picSup:true,fig:()=>`<div style="text-align:center;margin:8px 0"><img alt="Six sunflower pictures with short labels: sunflowers are tall with big yellow flowers, a young sunflower turns to face the sun, each flower is full of seeds, birds and people eat the seeds, farmers plant seeds in spring, and flowers bloom in late summer and fall" src="data:image/webp;base64,${window.TP_IMG1.wp.sunfacts}" style="width:760px;max-width:100%;height:auto;border-radius:16px"></div>`,key:["Ask: What does a young sunflower')
s=s[:_i6]+_m6+s[_j6:]
_i7=s.index('TP.register({id:"lp3-g1"');_j7=s.index('TP.register({id:',_i7+10);_m7x=s[_i7:_j7]
_a='${pics([["leaf","leaf"],["wind","the air"],[CORN,"the harvest"]])}'
assert _m7x.count(_a)==1
s=s[:_i7]+_m7x.replace(_a,'')+s[_j7:]
must('<option value="elamath">Reading and math</option>','<option value="all">All subjects (reading, writing, math, science, social studies)</option><option value="elamath">Reading and math</option>')
must('const SUBJ_SETS={elamath:["ela","math"],','const SUBJ_SETS={all:["ela","math","science","social"],elamath:["ela","math"],')
import re as _re
must('goalBox:"-10 -40 280 180",mapDeco(rows,spare,G){let d="";','goalBox:"-10 -40 280 180",mapDeco(rows,spare,G){window.__fl=0;let d="";')
_n=len(_re.findall(r'Pc\(leaf,24,[^)]*\)',s)); assert _n==6,_n
s=_re.sub(r'Pc\(leaf,24,[^)]*\)','Pc(fleaf,28,1.5,-12)',s)
must('function leaf(x,y,s,col,rot){','function fleaf(x,y,s){const W=window.TP_IMG1&&window.TP_IMG1.wp;const k=W&&W["fl"+(1+((window.__fl=(window.__fl||0)+1)-1)%12)];if(!k)return leaf(x,y,s,"#F0A86A",0);return`<image href="data:image/webp;base64,${k}" x="${x-23*s}" y="${y-23*s}" width="${46*s}" height="${46*s}"/>`}function leaf(x,y,s,col,rot){')

NS_JS=r"""function nsBox(v){return'<span style="display:inline-block;width:58px;height:58px;line-height:52px;text-align:center;border:3px solid var(--line,#6B4A3C);border-radius:12px;background:var(--surface,#fff);vertical-align:middle;font:700 1.8rem Andika,sans-serif">'+(v==null?"":v)+'</span>'}
function nsOp(c){return'<span style="font:700 2rem Andika,sans-serif;margin:0 10px;vertical-align:middle">'+c+'</span>'}
function nsRow(op,n,tot){var h=nsBox();for(var i=1;i<n;i++)h+=nsOp(op)+nsBox();return'<div style="margin:4px 0">'+h+nsOp("=")+nsBox(tot)+'</div>'}
function nsFrame(kind,tot){var cap="Put one number in each box.";var h;if(kind==="add")h=nsRow("+",2,tot);else if(kind==="sub")h=nsRow("&minus;",2,tot);else if(kind==="dbl"){h=nsRow("+",2,tot);cap="The two boxes get the same number."}else if(kind==="grp"){h=nsRow("+",3,tot);cap="Make one box for each row. Add more boxes if you need them."}else{h=nsRow("+",2,tot)+nsRow("&minus;",2,tot);cap="Put together uses plus. Take away uses minus. Pick the row that fits."}return'<div class="figure" style="display:block;text-align:center;margin:6px 0 12px">'+h+'<p class="fig-label" style="margin:4px 0 0">'+cap+'</p></div>'}
function nsMat(){var c=function(x,y){return'<circle cx="'+x+'" cy="'+y+'" r="26" fill="#fff" stroke="#6B4A3C" stroke-width="4" stroke-dasharray="7 6"/>'};return'<div class="figure" style="display:block;text-align:center;margin:6px 0 12px"><svg viewBox="0 0 360 150" width="340" role="img" aria-label="A mat with two small circles that join into one big box. Put some counters in each circle, then count all of them in the big box.">'+c(60,45)+c(60,105)+'<path d="M100 45 L150 70 M100 105 L150 80" stroke="#6B4A3C" stroke-width="4" fill="none" stroke-linecap="round"/><rect x="160" y="30" width="170" height="90" rx="20" fill="#fff" stroke="#6B4A3C" stroke-width="4"/></svg></div>'}
function nsKind(q){var t=String(q).replace(/<[^>]*>/g," ");if(/two equal addends|doubles/i.test(t))return"dbl";if(/equal addends|adds the rows|for the rows|matches the rows|for the tray|for Tray/i.test(t))return"grp";var sub=/take[s]?\s+away|taking away|subtraction|fly away|flew|left\b|ate\b|gave\b|lost\b|fewer/i.test(t),add=/adding sentence|addition|\bmore\b|in all|altogether|together|hop on|come\b|\bplus\b|add\b/i.test(t);if(/adding sentence|addition|add\b/i.test(t)&&!/take[s]?\s+away|taking away|subtraction/i.test(t))return"add";if(/take[s]?\s+away|taking away|subtraction/i.test(t))return"sub";return sub&&!add?"sub":add&&!sub?"add":"both"}
window.NSDecor=function(C,grade){var g=String(grade);if(!/^(TK|K|1|2)$/.test(g)||!C||C._ns)return;C._ns=1;var SENT=/(number sentence|adding sentence|addition sentence|take[s]? away sentence|taking away sentence|subtraction sentence|subtraction fact|addition fact|equation|doubles adding)/i;(C.stops||[]).forEach(function(st){(st.parts||[]).forEach(function(p){var sd=(p.std||[]).join(",");if(p.full||p._nsd)return;var did=false;if(Array.isArray(p.qs)&&(g==="1"||g==="2"||/K\.OA\./.test(sd))){var qs=(p.qsup||[]).slice(),qf=p.qfig?p.qfig.slice():null;p.qs.forEach(function(q,i){var txt=String(q);var ok=/K\.OA\./.test(sd)?true:(SENT.test(txt)&&!/numeral|as one number/i.test(txt));if(!ok)return;var kd=/K\.OA\.A\.3/.test(sd)?"add":nsKind(txt),tm=/K\.OA\.A\.3/.test(sd)?(/make (\d+)/i.exec(txt)||[])[1]:null;var o=qf&&qf[i]?"f":qs[i]?"s":"";var orig=o==="f"?qf[i]:o==="s"?qs[i]:null;var fn=function(){var h=orig?(typeof orig==="function"?orig():orig||""):"";return h+nsFrame(kd,tm)};did=true;if(o==="f")qf[i]=fn;else qs[i]=fn});if(did){p.qsup=qs;if(qf)p.qfig=qf}}else if(!Array.isArray(p.qs)&&/(K\.OA\.A\.[1-5]|TK\.MATH\.2\.3)/.test(sd)){var kd2=/TK\.MATH\.2\.3/.test(sd)?"mat":/K\.OA\.A\.3/.test(sd)?"add":"both";var o2=p.supfig;p.supfig=function(){var h=o2?(typeof o2==="function"?o2():o2||""):"";return h+(kd2==="mat"?nsMat():nsFrame(kd2))};did=true;p._sf=1}if(did){if(p._figSup==null)p._figSup=sceneSup(p);p._bt=1;p._ns=1;p._nsd=1}})})}
"""
BT_JS=r"""function btNums(q){var t=String(q).replace(/<[^>]*>/g," ");var stand=/stand for|does the \d|digit|the \d+ in /i.test(t);var out=[],re=/(\$)?(\d+(?:,\d{3})*)(:\d\d)?((?:\s+(?:whole\s+|full\s+)?(?:[a-z]+\s+of\s+ten|strings?|ropes?|spools?|trays?|bundles?)\b)|(?:\s*(?:o.clock|cents?|dollars?|%|st\b|nd\b|rd\b|th\b|tens?\b|ones?\b|hundreds?\b|minutes?|hours?|inch|feet|foot|numbers?\b|kinds?\b|clocks?\b)))?/gi,m;while((m=re.exec(t))){if(m[1]||m[3])continue;var n=+m[2].replace(/,/g,"");if(m[4]){if(/^\s+(whole\s+|full\s+)?([a-z]+\s+of\s+ten|strings?|ropes?|spools?|trays?|bundles?)/i.test(m[4]))n*=10;else continue}if(!(n>=1&&n<=120))continue;if(stand&&n<10)continue;if(out.indexOf(n)<0)out.push(n)}return out.slice(0,3)}
function btFig(nums){var F=window.TP_F;if(!F||!nums.length)return"";return'<div class="figure" style="align-items:flex-end;gap:26px;margin:6px 0 12px">'+nums.map(function(n){var h=n>=100?1:0,r=n-h*100;return'<div style="text-align:center">'+F.blocks(h,Math.floor(r/10),r%10)+'<p class="fig-label" style="margin:4px 0 0">'+n+'</p></div>'}).join("")+"</div>"}
window.BTDecor=function(C,grade){if(String(grade)!=="1"||!C||C._bt)return;C._bt=1;(C.stops||[]).forEach(function(st){(st.parts||[]).forEach(function(p){var sd=(p.std||[])[0]||"";if(!/^1\./.test(sd)||/^1\.(MD\.(B\.3|C\.4|A\.2)|G\.)/.test(sd)||!Array.isArray(p.qs)||p.full||p._btd)return;var qs=(p.qsup||[]).slice(),qf=p.qfig?p.qfig.slice():null,any=false;p.qs.forEach(function(q,i){var ns=btNums(q);if(!ns.length)return;var o=qf&&qf[i]?"f":qs[i]?"s":"";var orig=o==="f"?qf[i]:o==="s"?qs[i]:null;var fn=function(){var h=orig?(typeof orig==="function"?orig():orig||""):"";if(String(h).indexOf('class="bt"')>=0)return h;return h+btFig(ns)};any=true;if(o==="f")qf[i]=fn;else qs[i]=fn});if(!any)return;if(p._figSup==null)p._figSup=sceneSup(p);p._bt=1;p._btd=1;p.qsup=qs;if(qf)p.qfig=qf})})}
"""
must('function buildRoute(){ROUTE=[];let clockSec=0,num=0;if(!C)return 0;',BT_JS+NS_JS+'function buildRoute(){ROUTE=[];let clockSec=0,num=0;if(!C)return 0;if(window.NSDecor)window.NSDecor(C,S.grade);if(window.BTDecor)window.BTDecor(C,S.grade);')
must('function sceneSup(p){return!!(','function sceneSup(p){if(p&&p._bt)return!!p._figSup;return!!(')
must('sceneSup(p)&&!p.supfig&&!p.qsup?','(p._bt?p._figSup:sceneSup(p))&&(!p.supfig||p._sf)&&(!p.qsup||p._bt)?')
must('p.qsup&&p.qsup[qi])&&sceneSup(p)?','p.qsup&&p.qsup[qi])&&(sceneSup(p)||p._bt)?')
must('function picCavHtml(used){','function picCavHtml(used){const _r=picCavHtml0(used);if(!used.includes("pics")||!current)return _r;const _p=current.lv?[current]:current.parts;let _o=_r;if(_p.some(p=>p._btd))_o+="<br>Base-ten block pictures of the numbers in the questions were shown. The questions are the same, but note the child could see each number as tens and ones.";if(_p.some(p=>p._nsd))_o+="<br>A number sentence frame (empty boxes) was shown. It does not give any numbers, but note the child had the shape of the sentence to fill in.";return _o}function picCavHtml0(used){')
must('var S=function(id,title,short,part){return {id:id,pickOnly:true,title:tag+" "+title,short:short,parts:[P(part)]}};','var S=function(id,title,short,part){var sci=id>=110&&id<=129;var q=P(part);if(sci)q.pickOnly=false;return {id:id,pickOnly:!sci,title:tag+" "+title,short:short,parts:[q]}};')
_i8=s.index('TP.register({id:"lp3-g1"');_j8=s.index('TP.register({id:',_i8+10);_m8=s[_i8:_j8]
_a='Look at them go!</p>`,qs:["How many sentences do you see?'
assert _m8.count(_a)==1
_m8=_m8.replace(_a,'Look at them go!</p>`,picSup:true,fig:()=>`<div style="text-align:center;margin:8px 0"><img alt="A mother duck and three ducklings swimming in a pond with autumn trees" src="data:image/webp;base64,${window.TP_IMG1.wp.ducks}" style="width:560px;max-width:100%;height:auto;border-radius:16px"></div>`,qs:["How many sentences do you see?')
s=s[:_i8]+_m8+s[_j8:]
_i9=s.index('TP.register({id:"lp3-g1"');_j9=s.index('TP.register({id:',_i9+10);_m9=s[_i9:_j9]
_a='<p class="huge" aria-hidden="true">${ico(SUNFL,96)}</p><p class="big" style="text-align:center">Listen.</p>'
assert _m9.count(_a)==1
s=s[:_i9]+_m9.replace(_a,'')+s[_j9:]
must('const many=rows.length>1;const lis=r=>teachDirs(st,parts[r.pi]||{},"screen").filter(x=>x.k!=="extra").map(x=>`<li>${esc(x.t)}</li>`).join("");','const many=rows.length>1;const _seen=new Set;const lis=r=>teachDirs(st,parts[r.pi]||{},"screen").filter(x=>x.k!=="extra").filter(x=>{const key=x.k+"|"+(x.k==="score"?String(x.t).replace(/\\d+/g,"#"):x.t);if(_seen.has(key))return false;_seen.add(key);return true}).map(x=>`<li>${esc(x.t)}</li>`).join("");')
must('<ol>${rows.map(r=>`<li>${r.label?`<b>${esc(r.label)}</b>`:""}<ul>${lis(r)}</ul>${ans(r)}</li>`).join("")}</ol>','<ol>${rows.map(r=>{const _l=lis(r);return`<li>${r.label?`<b>${esc(r.label)}</b>`:""}${_l?`<ul>${_l}</ul>`:""}${ans(r)}</li>`}).join("")}</ol>')
must('let k=1,h="";const multi=st.parts.length>1;st.parts.forEach((p,pi)=>{','let k=1,h="";const _sd=new Set;const multi=st.parts.length>1;st.parts.forEach((p,pi)=>{')
must('h+=`<div class="pic-slot" data-pic-part="${pi}"></div>`;if(p.dir)h+=dirHtml(p.dir);','h+=`<div class="pic-slot" data-pic-part="${pi}"></div>`;if(p.dir&&!_sd.has(p.dir)){_sd.add(p.dir);h+=dirHtml(p.dir)}')
CLOCKLAB_JS='F.clockLab=(h,m)=>{const cx=190,cy=190,R=150,pad=n=>String(n).padStart(2,"0");let s=`<svg viewBox="0 0 380 380" width="360" style="max-width:100%;height:auto" role="img" aria-label="Clock face with the hour hand and the minute hand labeled, showing ${h}:${pad(m)}">`;s+=`<circle cx="${cx}" cy="${cy}" r="${R+8}" fill="#F3DCC4" stroke="var(--fig-ink)" stroke-width="4"/><circle cx="${cx}" cy="${cy}" r="${R}" fill="var(--surface)" stroke="var(--fig-ink)" stroke-width="3"/>`;for(let i=0;i<60;i++){const a=i*Math.PI/30,l=i%5?6:13;s+=`<line x1="${cx+Math.sin(a)*(R-3)}" y1="${cy-Math.cos(a)*(R-3)}" x2="${cx+Math.sin(a)*(R-3-l)}" y2="${cy-Math.cos(a)*(R-3-l)}" stroke="var(--ink)" stroke-width="${i%5?1.3:2.6}"/>`}for(let i=1;i<=12;i++){const a=i*Math.PI/6;s+=`<text x="${cx+Math.sin(a)*108}" y="${cy-Math.cos(a)*108}" font-size="30" font-family="Andika,sans-serif" font-weight="700" fill="var(--ink)" text-anchor="middle" dominant-baseline="central">${i}</text>`}for(let i=0;i<12;i++){const a=i*Math.PI/6;s+=`<text x="${cx+Math.sin(a)*(R+23)}" y="${cy-Math.cos(a)*(R+23)}" font-size="16" font-family="Andika,sans-serif" font-weight="700" fill="var(--sea)" text-anchor="middle" dominant-baseline="central">${i*5}</text>`}const ha=(h%12+m/60)*Math.PI/6,ma=m*Math.PI/30,hl=66,ml=90;s+=`<line x1="${cx}" y1="${cy}" x2="${cx+Math.sin(ha)*hl}" y2="${cy-Math.cos(ha)*hl}" stroke="var(--ink)" stroke-width="11" stroke-linecap="round"/><line x1="${cx}" y1="${cy}" x2="${cx+Math.sin(ma)*ml}" y2="${cy-Math.cos(ma)*ml}" stroke="var(--sea)" stroke-width="6" stroke-linecap="round"/><circle cx="${cx}" cy="${cy}" r="8" fill="var(--ink)"/>`;const tag=(ang,r,txt,col)=>{let d=ang*180/Math.PI-90;if(d>90||d<-90)d+=180;const x=cx+Math.sin(ang)*r,y=cy-Math.cos(ang)*r;return`<text transform="translate(${x.toFixed(1)} ${y.toFixed(1)}) rotate(${d.toFixed(1)})" y="-12" font-size="14" font-weight="700" font-family="Andika,sans-serif" fill="${col}" stroke="var(--surface)" stroke-width="3" paint-order="stroke" text-anchor="middle" dominant-baseline="central">${txt}</text>`};s+=tag(ha,38,"hour hand","var(--ink)")+tag(ma,51,"minute hand","var(--sea)");return s+`</svg>`};'
must('function tpsClockHtml(){return F.row([F.clock(3,0,170),"3:00, three o\'clock"],[F.clock(7,30,170),"7:30, half past seven"])+',CLOCKLAB_JS+'function tpsClockHtml(){return F.row([F.clockLab(3,0),"3:00, three o\'clock"],[F.clockLab(7,30),"7:30, half past seven"])+`<ul class="frames"><li><b>Short hand = hours.</b> Read the big numbers, 1 to 12.</li><li><b>Long hand = minutes.</b> Read the small numbers around the edge. They count by 5s.</li></ul>`+',10)

must('if(paper)add("run","The student needs paper and a pencil.");','')
must('if(p.mats&&p.mats.length)add("run","Have ready: "+listOf(p.mats)+".");','')
must('F.row(F.ruler({length:6,px:70,parts:1,unit:"in",item:4,itemLabel:"pencil"}))','F.row(F.ruler({length:6,px:96,parts:1,unit:"in",item:4,itemLabel:"pencil"}))',10)
must('width="${Math.min(W,680)}" role="img" aria-label="Ruler measuring an object">','width="${Math.min(W,680)}" style="max-width:100%;height:auto" role="img" aria-label="Ruler measuring an object">')
_i10=s.index('TP.register({id:"lp3-g1"');_j10=s.index('TP.register({id:',_i10+10);_m10=s[_i10:_j10]
_a='fig:()=>F.row(unitsFig()),qs:["How many blocks long is vine A?"'
assert _m10.count(_a)==1
_m10=_m10.replace(_a,'fig:()=>`<div style="text-align:center;margin:8px 0"><img alt="Two vines with same-size blocks laid end to end. The top vine has 5 yellow blocks. The bottom vine has 3 purple blocks." src="data:image/webp;base64,${window.TP_IMG1.wp.blocks19}" style="width:560px;max-width:100%;height:auto;border-radius:16px"></div>`,qs:["How many blocks long is vine A?"')
_a='fig:()=>F.row([F.clock(3,0,200),"A"],[F.clock(7,30,200),"B"]),qs:["Clock A:'
assert _m10.count(_a)==1
_m10=_m10.replace(_a,'fig:()=>F.row([F.clock(3,0,200),"A"],[F.clock(7,30,200),"B"]),supfig:()=>`<div style="text-align:center;margin:8px 0"><img alt="A clock face. The short red hour hand points to the 10. The long blue minute hand points to the 12. Big numbers 1 to 12 are the hours. Small labels around the edge count minutes by fives, from :00 to :55." src="data:image/webp;base64,${window.TP_IMG1.wp.clocklab}" style="width:340px;max-width:100%;height:auto"></div>`,qs:["Clock A:')
s=s[:_i10]+_m10+s[_j10:]
_i11=s.index('TP.register({id:"lp3-g1"');_j11=s.index('TP.register({id:',_i11+10);_m11=s[_i11:_j11]
_a='fig:()=>F.row([F.fracCircle(2,1,150),"1"],[F.gridRect(1,4,1,{cell:56}),"2"],[unequalCircle(),"3"]),key:'
assert _m11.count(_a)==1
_m11=_m11.replace(_a,'fig:()=>F.row([F.fracCircle(2,1,150),"1"],[F.gridRect(1,4,1,{cell:56}),"2"],[unequalCircle(),"3"]),supfig:()=>`<div style="text-align:center;margin:8px 0"><img alt="Two pumpkin pies. The left pie is cut into 2 equal parts with 1 part colored orange. The right pie is cut into 4 equal parts with 1 part colored orange." src="data:image/webp;base64,${window.TP_IMG1.wp.pies20}" style="width:640px;max-width:100%;height:auto;border-radius:16px"></div>`,key:')
s=s[:_i11]+_m11+s[_j11:]
must('function matsFor(){','window.matClean=function(m){let x=String(m).trim();if(/computer/.test(x))return"a computer, if they prefer";x=x.replace(/^a pencil and /,"").replace(/^a pencil, /,"").replace(/^paper, and /,"a ").replace(/^ruler, and /,"a ruler and ");return x==="paper"?"":x};function matsFor(){')
must('src.forEach(p=>(p.mats||[]).forEach(m=>{if(!out.includes(m))out.push(m)}))','src.forEach(p=>(p.mats||[]).forEach(m0=>{const m=window.matClean(m0);if(m&&!out.includes(m))out.push(m)}))')
must('${S.bonus?`, plus ${S.bonus} bonus ${T.bonusName[S.bonus===1?0:1]}`:""}.`}</p>','${S.bonus?`, plus ${S.bonus} bonus ${T.bonusName[S.bonus===1?0:1]}`:""}.`}</p>${!older()&&S.bonus&&T.key==="pumpkin"&&window.TP_IMG1&&window.TP_IMG1.wp.seed?`<div role="img" aria-label="${S.bonus} bonus sunflower ${S.bonus===1?"seed":"seeds"}" style="display:flex;flex-wrap:wrap;gap:8px;justify-content:center;margin:6px auto 4px;max-width:760px">${Array.from({length:S.bonus},()=>`<img alt="" width="52" height="66" style="width:52px;height:auto" src="data:image/webp;base64,${window.TP_IMG1.wp.seed}">`).join("")}</div>`:""}')
_i12=s.index('TP.register({id:"lp3-g1"');_j12=s.index('TP.register({id:',_i12+10);_m12=s[_i12:_j12]
for _a,_b in [('const row=(y,n,fill)=>{','const row=(y,n,fill,bc)=>{'),('height="34" fill="#F2DC9A"','height="34" fill="${bc||\'#F2DC9A\'}"'),('s+=`<text x="48" y="68" font-size="26" font-weight="800" fill="var(--ink)">A</text>`+row(50,5,"#A8D49A");','s+=row(50,5,"#A8D49A","#F2C01E");'),('s+=`<text x="48" y="186" font-size="26" font-weight="800" fill="var(--ink)">B</text>`+row(168,3,"#A8D49A");','s+=row(168,3,"#A8D49A","#8E5BC9");'),('aria-label="Two vines, each measured with square blocks laid end to end"','aria-label="Two vines measured with square blocks laid end to end. One vine has yellow blocks. One vine has purple blocks."'),('"How many blocks long is vine A?","How many blocks long is vine B?","How much longer is vine A than vine B?"','"How many blocks long is the yellow vine?","How many blocks long is the purple vine?","How much longer is the yellow vine than the purple vine?"'),('Someone writes 10:00.','Someone writes 4:00.'),('The hour hand points at the 10 and the minute hand points at the 12.','The hour hand points at the 4 and the minute hand points at the 12.')]:
    assert _m12.count(_a)==1,_a
    _m12=_m12.replace(_a,_b)
s=s[:_i12]+_m12+s[_j12:]
_i13=s.index('TP.register({id:"lp3-g1"');_j13=s.index('TP.register({id:',_i13+10);_m13=s[_i13:_j13]
_a='{title:"Scarecrow Fix It",std:["L.1.1"],dur:70,dir:"Listen to your teacher read each one. Say your answer out loud.",qs:['
assert _m13.count(_a)==1
_qf='(function(){var FR=function(a,end,lab){var h=\'<div style="display:inline-flex;align-items:center;flex-wrap:wrap;gap:10px;margin:8px 0 4px;padding:10px 20px;border:3px dashed var(--line);border-radius:16px;background:var(--card,#fff);font-size:2rem;font-weight:700">\';a.forEach(function(w){h+=w.charAt(0)==="_"?\'<span style="display:inline-block;min-width:110px;border-bottom:4px solid var(--ink,#333);height:1.6em"></span>\':\'<span>\'+w+\'</span>\'});if(end)h+=\'<span style="display:inline-flex;flex-direction:column;align-items:center;line-height:1"><span style="font-size:3.6rem;color:#c0392b">\'+end+\'</span><span style="font-size:.7rem;font-weight:600">\'+lab+\'</span></span>\';return function(){return\'<div style="margin:2px 0 6px">\'+h+\'</div></div>\'}};return[FR(["Yesterday I","_____","a pumpkin"],".","period"),FR(["_____","pumpkins are big"],".","period"),FR(["_____","see a duck"],".","period"),FR(["I put on a coat because","_____"],".","period"),FR(["The scarecrow stands","_____","the corn"],".","period"),FR(["Where","_____","_____"],"?","question mark")]})()'
_m13=_m13.replace(_a,'{title:"Scarecrow Fix It",std:["L.1.1"],dur:70,dir:"Listen to your teacher read each one. Say your answer out loud.",picSup:true,fig:function(){return""},qfig:'+_qf+',qs:[')
s=s[:_i13]+_m13+s[_j13:]
import re as _re9
_dec=_re9.compile(r'html:\(\)=>`<p[^>]*aria-hidden="true"[^>]*>(?:\$\{ico\([^)]*\)\}\s*)+</p>`,(?=qs:)')
_M9=_re9.compile(r'^(K|[1-8])\.(OA|NBT|MD|G|NF|CC|NS|RP|EE|F|SP)\b')
def _sub9(m):
    ctx=s[max(0,m.start()-400):m.start()];ss=_re9.findall(r'std:\["([^"]+)"',ctx)
    r='' if ss and _M9.match(ss[-1]) else m.group(0)
    print('dec',ss[-1:] ,'removed' if r=='' else 'kept')
    return r
_n9=len(_dec.findall(s));s=_dec.sub(_sub9,s);print('removed math decorations',_n9-len(_dec.findall(s)))
must('const A=()=>[Pc(hay,54,1.3,12),Ps(vine,98,-6),Pc(fleaf,28,1.5,-12),Pc(hay,54,1.25,12),Ps(vine,98,-2),Pc(fleaf,28,1.5,-12),Pc(hay,54,1.2,12),Ps(vine,98,-6)],B=()=>[Ps(vine,98,-4),Pc(fleaf,28,1.5,-12),Pc(hay,54,1.3,12),Ps(vine,98,-8),Pc(hay,54,1.2,12),Pc(fleaf,28,1.5,-12),Ps(vine,98,-2),Pc(fleaf,28,1.5,-12)];','const A=()=>[Pc(hay,54,1.3,12),Pc(fleaf,28,1.5,-12),Ps(vine,98,-6),Pc(hay,54,1.25,12),Pc(fleaf,28,1.5,-12),Pc(hay,54,1.2,12)],B=()=>[Pc(fleaf,28,1.5,-12),Pc(hay,54,1.3,12),Ps(vine,98,-4),Pc(fleaf,28,1.5,-12),Pc(hay,54,1.2,12),Pc(fleaf,28,1.5,-12)];')
must('(p.wordPics===2?window.TP_IMG1.wp2:window.TP_IMG1.wp)','(p.wordPics===3?window.TP_IMG1.wp3:p.wordPics===2?Object.assign({},window.TP_IMG1.wp2,window.TP_IMG1.wp3):window.TP_IMG1.wp)')
_i14=s.index('TP.register({id:"lp3-g2"');_j14=s.index('TP.register({id:',_i14+10);_m14=s[_i14:_j14]
_a='{std:["RF.2.3"],kind:"words",words:'
assert _m14.count(_a)>=1,_m14.count(_a)
_m14=_m14.replace(_a,'{std:["RF.2.3"],kind:"words",wordPics:3,words:',1)
s=s[:_i14]+_m14+s[_j14:]
_i15=s.index('TP.register({id:"lp3-g2"');_j15=s.index('TP.register({id:',_i15+10);_m15=s[_i15:_j15]
_a='html:()=>`<p class="passage g2-fluency">${STORY}</p>`,key:["97 words.'
assert _m15.count(_a)==1
_m15=_m15.replace(_a,'html:()=>`<p class="passage g2-fluency">${STORY}</p>`,supfig:()=>`<div style="text-align:center;margin:10px 0"><img alt="Six picture panels that tell the story. A strong wind blows over the pumpkin patch. The wind lifts the straw hat off the scarecrow. Jada watches the hat spin over the corn rows. The hat lands in the mud and Jada runs after it in rubber boots. The wet hat hangs on the fence to dry in the sun. Jada climbs a hay bale and ties the hat back on the scarecrow with string." src="data:image/webp;base64,${window.TP_IMG1.wp3.hatstory}" style="width:760px;max-width:100%;height:auto;border-radius:16px"></div>`,key:["97 words.')
s=s[:_i15]+_m15+s[_j15:]
must('items.forEach((li,i)=>{li.hidden=i!==qIdx});const cur=items[qIdx],curList=cur.parentNode;','items.forEach((li,i)=>{li.hidden=i!==qIdx});const cur=items[qIdx],curList=cur.parentNode;{let g=[];[...card.children].forEach(e=>{if(e.tagName==="OL"&&e.classList.contains("qlist")){g.forEach(x=>{x.hidden=e!==curList});g=[]}else g.push(e)})}')
must('items.forEach(li=>{li.hidden=false});card.querySelectorAll(".part-fig2")','items.forEach(li=>{li.hidden=false});[...card.children].forEach(e=>{if(e.tagName!=="OL"&&e.hidden)e.hidden=false});card.querySelectorAll(".part-fig2")')
must('else if(q)add("score",where==="screen"?`Keep track of which answers are right, then type the number right in the box for this part (out of ${n}).`:`Mark each answer right or not yet as you go. Write the number right in the box for this part (out of ${n}).`);','else if(q){}')
must('else if(p.inventory)add("score",where==="screen"?`Keep track of each ${unit} the student gets right, then type the number right in the box for this part.`:`Mark each ${unit} the student gets on the boxes ${here}, and circle the ones missed. Write the number right in the box for this part.`);else if(cards)add("score",where==="screen"?`Keep track of each ${unit} the student reads correctly, then type the number right in the box for this part.`:`Mark each ${unit} as the student reads it. Write the number right in the box for this part.`);','else if(p.inventory||cards){}')
_i16=s.index('TP.register({id:"lp3-g2"');_j16=s.index('TP.register({id:',_i16+10);_m16=s[_i16:_j16]
_a='html:()=>passage("Goat and the Bag of Seeds",FABLE),qs:'
assert _m16.count(_a)==1
_m16=_m16.replace(_a,'html:()=>passage("Goat and the Bag of Seeds",FABLE),supfig:()=>`<div style="text-align:center;margin:10px 0"><img alt="Nine picture panels that tell the story. Goat finds a bag of sunflower seeds by the fence. Hen dropped it on her way home. Goat is hungry and thinks no one saw him find it. He looks at the seeds for a long time. He walks to Hen\'s coop and knocks. He asks if the bag is hers. Hen claps her wings and says the seeds are for her chicks. She pours some into Goat\'s hat to say thank you. Goat walks home feeling full and glad." src="data:image/webp;base64,${window.TP_IMG1.wp3.barnstory}" style="width:760px;max-width:100%;height:auto;border-radius:16px"></div>`,qs:')
s=s[:_i16]+_m16+s[_j16:]
_i17=s.index('TP.register({id:"lp3-g2"');_j17=s.index('TP.register({id:',_i17+10);_m17=s[_i17:_j17]
_a='html:()=>`<p class="big">Write to teach a friend about fall.'
assert _m17.count(_a)==1
_m17=_m17.replace(_a,'supfig:()=>`<div style="text-align:center;margin:10px 0"><img alt="Four fall pictures. Colorful leaves falling from a tree. A cold thermometer and a frost sign over frosty grass. A basket of red apples under an apple tree. A big pumpkin and a small pumpkin growing on the vine." src="data:image/webp;base64,${window.TP_IMG1.wp3.fallpics}" style="width:620px;max-width:100%;height:auto;border-radius:16px"></div>`,'+_a)
s=s[:_i17]+_m17+s[_j17:]
_i18=s.index('TP.register({id:"lp3-g2"');_j18=s.index('TP.register({id:',_i18+10);_m18=s[_i18:_j18]
_a='html:()=>passage("How a Pumpkin Grows",GROW),qs:'
assert _m18.count(_a)==1
_m18=_m18.replace(_a,'html:()=>passage("How a Pumpkin Grows",GROW),supfig:()=>`<div style="text-align:center;margin:10px 0"><img alt="Eight picture panels that show how a pumpkin grows. A flat white seed in the soil. A farmer plants the seed in late spring when the soil is warm. A green sprout pushes up in about a week. Long vines spread across the ground. Big yellow flowers open on the vines. After bees visit the flowers, tiny green pumpkins begin to grow. They need lots of sun and water all summer. By fall the pumpkins are orange with hard shells, and a farmer cuts the stem and leaves a short handle." src="data:image/webp;base64,${window.TP_IMG1.wp3.growstory}" style="width:760px;max-width:100%;height:auto;border-radius:16px"></div>`,qs:')
s=s[:_i18]+_m18+s[_j18:]
must('function fence(x,y,s){return`<g transform="translate(${x},${y}) scale(${s||1})" opacity=".95">','function hayA(x,y,s){s=s||1;const T=window.TP_IMG1&&window.TP_IMG1.props;if(!T||!T.length)return hay(x,y,s);const k=T[Math.abs(Math.round(x*5+y*0.37))%T.length],w=Math.min(62,40*k[1]/k[2]),h=w*k[2]/k[1];return`<image href="data:image/webp;base64,${k[0]}" x="${x-w*s/2}" y="${y+17*s-h*s}" width="${w*s}" height="${h*s}"/>`}function fence(x,y,s){return`<g transform="translate(${x},${y}) scale(${s||1})" opacity=".95">')
must('function tree(x,y,s){s=s||1;return`<g transform="translate(${x},${y}) scale(${s})"><rect x="-6" y="-2" width="12" height="28"','function tree(x,y,s){s=s||1;const T=window.TP_IMG1&&window.TP_IMG1.trees;if(T&&T.length){const k=T[Math.abs(Math.round(x*7+y*0.31))%T.length],w=76,h=w*k[2]/k[1];return`<image href="data:image/webp;base64,${k[0]}" x="${x-w*s/2}" y="${y+26*s-h*s}" width="${w*s}" height="${h*s}"/>`}return treeOld(x,y,s)}function treeOld(x,y,s){s=s||1;return`<g transform="translate(${x},${y}) scale(${s})"><rect x="-6" y="-2" width="12" height="28"')
must("function basket(n,full){return`<image href='data:image/webp;base64,","function basket(n,full){if(!full)return window.TP_BASKET0;return`<image href='data:image/webp;base64,")
must('desc:"using in, on, and under to tell where something is",\n html:function(){return\'<div style="text-align:center">\'+[p1,p2,p3]','desc:"using in, on, and under to tell where something is",\n html:function(){if(lp===1)return\'<div style="text-align:center"><img alt="Three numbered pictures of a parrot: 1 in a box, 2 on a table, 3 under a table" src="data:image/webp;base64,\'+window.TP_IMG1.parrot+\'" style="width:760px;max-width:100%;height:auto"></div>\';return\'<div style="text-align:center">\'+[p1,p2,p3]')
must('html:function(){if(lp===1)return\'<div style="text-align:center"><img alt="Three numbered pictures of a parrot','html:function(){if(lp===2)return\'<div style="text-align:center"><img alt="Three numbered pictures of a bee: 1 in a box, 2 on a table, 3 under a table" src="data:image/webp;base64,\'+window.TP_IMG1.beepos+\'" style="width:760px;max-width:100%;height:auto"></div>\';if(lp===1)return\'<div style="text-align:center"><img alt="Three numbered pictures of a parrot')
must('desc:"telling flat shapes from solid shapes",qs:["Is a ball flat or solid?"','desc:"telling flat shapes from solid shapes",picSup:true,fig:()=>\'<div class="figure" style="margin:10px 0"><img alt="Three pictures: a beach ball, a flat purple circle, and a taped box" src="data:image/webp;base64,\'+window.TP_IMG1.flatsolid+\'" style="width:620px;max-width:100%;height:auto;background:#FFFDF8;border-radius:12px;padding:8px"></div>\',qs:["Is a ball flat or solid?"')
must('<rect x="108" y="122" width="84" height="84" rx="11" fill="#8ECBE8"','<rect x="108" y="122" width="84" height="84" fill="#8ECBE8"')
must('<rect x="240" y="138" width="150" height="54" rx="11" fill="#D7EDF3"','<rect x="240" y="138" width="150" height="54" fill="#D7EDF3"')
must('<rect x="${x-30}" y="${y-30}" width="60" height="60" rx="9" fill="#8ECBE8"','<rect x="${x-30}" y="${y-30}" width="60" height="60" fill="#8ECBE8"')
must('<rect x="108" y="130" width="84" height="84" rx="8" fill="#8ECBE8" ${st}/>','<rect x="108" y="130" width="84" height="84" fill="#8ECBE8" stroke="${INK}" stroke-width="4"/>')
must('<rect x="244" y="146" width="140" height="52" rx="8" fill="#B8E3A8" ${st}/>','<rect x="244" y="146" width="140" height="52" fill="#B8E3A8" stroke="${INK}" stroke-width="4"/>')
must('sv=function(w,h,inner,alt){return\'<svg viewBox="0 0 \'+w+\' \'+h+\'" width="\'+w+\'" height="\'+h+\'" role="img" aria-label="\'+alt+\'">\'+inner+\'</svg>\'}','sv=function(w,h,inner,alt){return\'<svg viewBox="0 0 \'+w+\' \'+h+\'" width="\'+w+\'" height="\'+h+\'" style="max-width:100%;height:auto" role="img" aria-label="\'+alt+\'">\'+inner+\'</svg>\'}')
must('<p class="huge" aria-hidden="true" style="margin:6px 0">${ico("bear",96)}</p><p class="big">Listening time. Your teacher will read you a story about a bear and his hat.</p>`,read:BEAR','<p class="big">Listening time. Your teacher will read you a story about a bear and his hat.</p>`,read:BEAR')
exec(open('g12fix.py').read())
exec(open('nline.py').read())
must('function picWordsAllowed(st,p){if(!p)return false;','function picWordsAllowed(st,p){return false;if(!p)return false;')
must('{id:4,title:"Story Questions",parts:[{title:"Story Questions",std:["RL.1.1"],dur:90,','{id:4,title:"Story Questions",parts:[{title:"Story Questions",std:["RL.1.1"],dur:90,picSup:true,fig:()=>`<div class="figure"><img alt="Fox waves up at Duck, who holds his red hat on a tree branch" style="max-width:100%;width:560px;height:auto;border-radius:14px" src="data:image/webp;base64,'+FD+'"></div>`,')
import re
_m=re.search(r"goalClosed:closedChest,goalOpen:\(\)=>`<image href='data:image/webp;base64,([A-Za-z0-9+/=]+)' x='4' y='-30' width='213' height='160'/>`",s)
assert _m and s.count('goalClosed:closedChest')==1
_new="goalClosed:()=>`<image href='data:image/webp;base64,${CHESTIMG}' x='4' y='-30' width='213' height='160'/>`,goalOpen:()=>`<image href='data:image/webp;base64,${CHESTIMG}' x='4' y='-30' width='213' height='160'/>`"
s=s[:_m.start()]+_new+s[_m.end():]
s=s.replace('const GEMIMG=','const CHESTIMG="'+_m.group(1)+'";window.TPCHEST=CHESTIMG;const GEMIMG=',1)
must('return svg(420,280,b,"A closed treasure chest with question marks")','return svg(420,280,`<image href="data:image/webp;base64,'+open("../gem/chest_new.b64").read().strip()+'" x="55" y="15" width="311" height="250"/>`+em(52,60,X.q,44)+em(368,60,X.q,44),"A treasure chest with question marks")')
must('function teachFor(p){if(p.teach)return p.teach;','function teachFor(p){var t0=teachFor0(p);return window.GXteach?window.GXteach(p,t0,S.grade,call):t0}function teachFor0(p){if(p.teach)return p.teach;')
must('else if(q)add("run",young?"Read the directions aloud, then each question, one at a time.":','else if(q)add("run",young?(window.GXlookBack&&window.GXlookBack(p,S.grade,call)?"Read the directions aloud. The story is on the screen under Look back. Then read each question, one at a time. If a question needs the story, read the sentence it asks about. If the student struggled to read the story in the last stop, read the whole story aloud first.":window.GXreadsText&&window.GXreadsText(p,S.grade,call)?"Read the directions aloud. Then read the text on the screen aloud, once, and again if the student asks. Then read each question, one at a time.":"Read the directions aloud, then each question, one at a time."):')
must('else add("run",young?"Read the directions aloud.":','else add("run",young?(window.GXreadsText&&window.GXreadsText(p,S.grade,call)?"Read the directions aloud. Then read the text on the screen aloud, once, and again if the student asks.":"Read the directions aloud."):')
import re
CS=CS='function candleShape(x,y,s,c){const k=s/26;return`<g transform="translate(${n1(x)} ${n1(y+2*k)}) scale(${n1(k)})">${candleArt(c)}</g>`}'
for mid in ['lp10-g1','lp10-g2','lp10-gk']:
    m=re.search(r'<script>TP\.register\(\{id:"%s"'%mid,s);e=s.index('</script>',m.start());t=s[m.start():e]
    assert t.count('function candleArt(c){')==1 and 'function candleShape' not in t,mid
    t=t.replace('function candleArt(c){',CS+'function candleArt(c){')
    s=s[:m.start()]+t+s[e:]
_i=s.index('F.blocks=(h,t,o)=>{');_j=s.index('F.tens=(t,o)=>F.blocks(0,t,o);')
_nb=r"""F.blocks=(h,t,o)=>{h=h||0;t=t||0;o=o||0;const B=window.TP_BT||{};const im=(k,w,hh)=>`<img src="data:image/webp;base64,${B[k]}" alt="" width="${w}" height="${hh}" style="display:block;max-width:none">`;const rep=(n,f)=>Array.from({length:n},f).join("");let s=`<div class="bt" role="img" aria-label="${h?h+" hundreds, ":""}${t} tens and ${o} ones" style="display:inline-flex;align-items:flex-end;justify-content:center;flex-wrap:wrap;gap:16px;vertical-align:bottom">`;if(h)s+=`<div style="display:flex;gap:10px;align-items:flex-end">${rep(h,()=>im("flat",120,120))}</div>`;if(t)s+=`<div style="display:flex;gap:5px;align-items:flex-end">${rep(t,()=>im("rod",23,122))}</div>`;if(o)s+=`<div style="display:grid;grid-template-columns:repeat(5,28px);gap:5px;align-items:end">${rep(o,()=>im("cube",28,27))}</div>`;return s+"</div>"};"""
s=s[:_i]+_nb+s[_j:]
def _fend(t,i):
    # i = index of '{' ; return index just after matching '}' (JS aware: strings, templates)
    d=0;k=i;n=len(t);stack=[]
    while k<n:
        c=t[k]
        if c in '"\'':
            q=c;k+=1
            while t[k]!=q:
                if t[k]=='\\': k+=1
                k+=1
        elif c=='`':
            stack.append(d);d=0;k+=1
            while True:
                if t[k]=='\\': k+=2;continue
                if t[k]=='`':
                    d=stack.pop();break
                if t[k]=='$' and t[k+1]=='{':
                    # nested expression: recurse
                    e=_fend(t,k+1);k=e;continue
                k+=1
        elif c=='{': d+=1
        elif c=='}':
            d-=1
            if d==0: return k+1
        k+=1
    raise Exception('unbalanced')
import re as _re2
_cnt=0
for _nm,_arg,_body in (('tens','t,o','F.blocks(0,t,o)'),('matSvg','h,t,o','F.blocks(h,t,o)'),('tpsMatSvg','h,t,o','F.blocks(h,t,o)')):
    _pat='function %s(%s){'%(_nm,_arg);_pos=0
    while True:
        _i=s.find(_pat,_pos)
        if _i<0: break
        _b=s.index('{',_i);_e=_fend(s,_b)
        if 'tens' in s[_i:_e] and 'ones' in s[_i:_e] and '<svg' in s[_i:_e]:
            s=s[:_i]+'function %s(%s){return %s}'%(_nm,_arg,_body)+s[_e:];_cnt+=1;_pos=_i+10
        else: _pos=_e
# --- LP1 grade 1: move Opinion Writing after Story Questions, Facts Writing after Frog Facts ---
_m0=s.index('TP.register({id:"lp1-g1"');_m1=s.index('TP.register({id:"lp1-g2"')
_seg=s[_m0:_m1]
def _cut(seg,a_,b_):
    i=seg.index(a_);j=seg.index(b_,i);return seg[:i]+seg[j+1:],seg[i:j]   # drops the comma before b_
_seg,_op=_cut(_seg,'{wt:"opinion",',',{wt:"facts",')
_seg,_fa=_cut(_seg,'{wt:"facts",',',{wt:"story",')
for _a in ('{title:"Sentence Detective",','{title:"Listen Up",'):
    assert _seg.count(','+_a)==1,_a
_op=_op.replace('{wt:"opinion",','{wt:"opinion",gxHome:13,',1);_fa=_fa.replace('{wt:"facts",','{wt:"facts",gxHome:13,',1)
_seg=_seg.replace(',{title:"Sentence Detective",',','+_op+',{title:"Sentence Detective",',1)
_seg=_seg.replace(',{title:"Listen Up",',','+_fa+',{title:"Listen Up",',1)
import re as _re
def _remap_keys(seg,name):
    i=seg.index('const %s={'%name)+len('const %s='%name);e=_fend(seg,i)
    obj=seg[i:e]
    for old,new in (("7.2","7.3"),("7.1","7.2"),("4.1","4.2"),("13.0","4.1"),("13.1","7.1"),("13.2","13.0")):
        obj=obj.replace('"%s":'%old,'"%s":'%new)
    return seg[:i]+obj+seg[e:]
_seg=_remap_keys(_seg,'DIRS');_seg=_remap_keys(_seg,'DESC')
s=s[:_m0]+_seg+s[_m1:]
# --- LP4 grade 1: same move ---
_m0=s.index('TP.register({id:"lp4-g1"');_m1=s.index('TP.register({id:"lp4-g2"')
_seg=s[_m0:_m1]
_seg,_op=_cut(_seg,'{wt:"opinion",',',{wt:"facts",')
_seg,_fa=_cut(_seg,'{wt:"facts",',',{wt:"story",')
_op=_op.replace('{wt:"opinion",','{wt:"opinion",gxHome:13,',1);_fa=_fa.replace('{wt:"facts",','{wt:"facts",gxHome:13,',1)
assert _seg.count(']},{id:5,title:"Fix the Frost"')==1 and _seg.count(',{title:"Frozen Pond",')==1
_seg=_seg.replace(']},{id:5,title:"Fix the Frost"',','+_op+']},{id:5,title:"Fix the Frost"',1)
_seg=_seg.replace(',{title:"Frozen Pond",',','+_fa+',{title:"Frozen Pond",',1)
def _remap4(seg,name):
    i=seg.index('const %s={'%name)+len('const %s='%name);e=_fend(seg,i)
    obj=seg[i:e]
    for old,new in (("7.1","7.2"),("13.0","4.2"),("13.1","7.1"),("13.2","13.0")):
        obj=obj.replace('"%s":'%old,'"%s":'%new)
    return seg[:i]+obj+seg[e:]
_seg=_remap4(_seg,'DIRS');_seg=_remap4(_seg,'DESC')
s=s[:_m0]+_seg+s[_m1:]
print("moved writing parts")
print('base ten local drawers replaced',_cnt)
assert _cnt==13,_cnt
files=[B+'gx/core.js']+sorted(glob.glob(B+'gx/g[1-8].js'))
js='\n'.join(open(f).read() for f in files)
for _n in (1,2,3): js=js.replace('@@SD%d@@'%_n,open(B+'gem/sd%d.b64'%_n).read())
for _n in (1,2): js=js.replace('@@WS%d@@'%_n,open(B+'gem/ws%d.b64'%_n).read())
js=js.replace('@@MG@@',open(B+'gem/mg.b64').read())
for _k,_f in (('BTF','flat'),('BTR','rod'),('BTC','cube')): js=js.replace('@@%s@@'%_k,open(B+'gem/bt_%s.b64'%_f).read())
assert '—' not in js
blk='<script>'+js+'</script>'
i=s.index('<script>TP.register(')
s=s[:i]+blk+s[i:]
import re as _re,base64,io,hashlib,json,os
from PIL import Image
CP=B+'gx/imgcache.json'
cache=json.load(open(CP)) if os.path.exists(CP) else {}
def recomp(m):
    b=m.group(1)
    if len(b)<80000: return m.group(0)
    k=hashlib.md5(b.encode()).hexdigest()
    if k not in cache:
        raw=base64.b64decode(b);im=Image.open(io.BytesIO(raw));o=io.BytesIO();im.save(o,'WEBP',quality=74,method=6)
        nb=base64.b64encode(o.getvalue()).decode()
        cache[k]=nb if len(nb)<len(b)*0.92 else b
    return 'data:image/webp;base64,'+cache[k]
n0=len(s);s=_re.sub(r'data:image/webp;base64,([A-Za-z0-9+/=]+)',recomp,s)
json.dump(cache,open(CP,'w'))
print('image recompress saved chars',n0-len(s))

# make baked-in black corners and backgrounds transparent
import numpy as _np
from scipy import ndimage as _ndi
_fixc={}
def _unblack(m):
    b=m.group(0)
    if b in _fixc: return _fixc[b]
    out=b
    try:
        raw=base64.b64decode(b);im=Image.open(io.BytesIO(raw));fmt=im.format;im.load()
        a=_np.array(im.convert('RGBA')).astype(int)
        if (a[:,:,3]>250).mean()>0.97 and im.size[0]>=300:
            mx=a[:,:,:3].max(axis=2)
            cs=[mx[0,0],mx[0,-1],mx[-1,0],mx[-1,-1]]
            if max(cs)<=12:
                lab,n=_ndi.label(mx<60)
                ids=set(lab[0,:])|set(lab[-1,:])|set(lab[:,0])|set(lab[:,-1]);ids.discard(0)
                bg=_np.isin(lab,list(ids))
                if 0.002<bg.mean()<0.45:
                    sub=_ndi.binary_fill_holes(~bg)
                    sub=_ndi.binary_opening(sub,iterations=1)
                    al=Image.fromarray((sub*255).astype(_np.uint8)).filter(ImageFilter.GaussianBlur(0.7))
                    o=im.convert('RGBA');o.putalpha(al);bio=io.BytesIO()
                    if fmt=='PNG': o.save(bio,'PNG',optimize=True)
                    else: o.save(bio,'WEBP',quality=88,method=6)
                    out=base64.b64encode(bio.getvalue()).decode()
                    print('unblacked',fmt,im.size,round(bg.mean(),3))
    except Exception as e: pass
    _fixc[b]=out
    return out
from PIL import ImageFilter
s=_re.sub(r'[A-Za-z0-9+/]{3000,}={0,2}',_unblack,s)

# American spellings
_us=[("millilitre","milliliter"),("centimetre","centimeter"),("kilometre","kilometer"),("millimetre","millimeter"),("metre","meter"),("centre","center"),
("colour","color"),("favour","favor"),("behaviour","behavior"),("defence","defense"),("programme","program"),("organise","organize"),
("recognise","recognize"),("neighbouring","neighboring"),("neighbour","neighbor"),("labelled","labeled"),("travelled","traveled"),("travelling","traveling")]
def _usfix(m):
    w=m.group(0);lw=w.lower()
    if lw.startswith('labelledby'): return w
    for a,b in _us:
        if lw.startswith(a):
            r=b+lw[len(a):]
            if lw.startswith("organise") and lw[len(a):] not in("","d","s","r","rs"): continue
            return (r[0].upper()+r[1:]) if w[0].isupper() else r
    return w
_n=len(_re.findall(r"\b(?:millilitre|centimetre|kilometre|millimetre|metre|centre|colour|favour|behaviour|defence|programme|organise|recognise|neighbour|labelled|travelled|travelling)\w*",s,_re.I))
s=_re.sub(r"\b(?:millilitre|centimetre|kilometre|millimetre|metre|centre|colour|favour|behaviour|defence|programme|organise|recognise|neighbour|labelled|travelled|travelling)\w*",_usfix,s,flags=_re.I)
print('american spellings',_n)

# LP3 grade 1 and 3: use the new pumpkin sticker instead of the old drawn pumpkin
def _newpump(s):
    for mid in ('lp3-g1',):
        a=s.find('TP.register({id:"%s"'%mid)
        assert a>=0
        b=s.find('</script>',a)
        seg=s[a:b]
        seg2=_re.sub(r'(?<![\w.])pumpkin\((\d+)\)',lambda m:'ico("pumpkin",%s)'%m.group(1),seg)
        print('new pumpkins',mid,len(_re.findall(r'(?<![\w.])pumpkin\((\d+)\)',seg)))
        s=s[:a]+seg2+s[b:]
    return s
s=_newpump(s)

# more American spellings (whole words, with endings)
_us2=[("organisation","organization"),("organising","organizing"),("reorganised","reorganized"),("analysing","analyzing"),("criticise","criticize"),("crystallise","crystallize"),
("fertilise","fertilize"),("fertiliser","fertilizer"),("fibre","fiber"),("harbour","harbor"),("honour","honor"),("judgement","judgment"),("kerb","curb"),("labour","labor"),
("licence","license"),("litre","liter"),("mould","mold"),("plough","plow"),("practise","practice"),("recognising","recognizing"),("summarise","summarize"),
("theatre","theater"),("tonne","ton"),("vapour","vapor"),("aluminium","aluminum"),("armouring","armoring"),("authorised","authorized"),("characterised","characterized"),
("magnetised","magnetized"),("memorising","memorizing"),("paralysed","paralyzed"),("patronise","patronize"),("standardised","standardized"),("encyclopaedia","encyclopedia"),
("snowplough","snowplow"),("ploughshare","plowshare"),("labourer","laborer"),("fulfil","fulfill"),("maths","math"),("grey","gray"),("unfertilised","unfertilized")]
_us2.sort(key=lambda x:-len(x[0]))
_pat2=r"\b(?:"+"|".join(a for a,b in _us2)+r")(?:s|d|es|ed|ing|r|rs)?\b"
def _usfix2(m):
    w=m.group(0);lw=w.lower()
    nx=s[m.end():m.end()+1]
    if lw=='grey' and s[m.start()-1:m.start()] not in (' ','>'): return w
    for a,b in _us2:
        if lw.startswith(a):
            r=b+lw[len(a):]
            if a=='fulfil' and lw[len(a):]=='l': return w
            r=r.replace('tons','tons')
            return (r[0].upper()+r[1:]) if w[0].isupper() else r
    return w
_n2=len(_re.findall(_pat2,s,_re.I))
s=_re.sub(_pat2,_usfix2,s,flags=_re.I)
print('american spellings 2',_n2)
# LP7 grade 7: old British money to US money (quarter = old threepence, dollars = old shillings)
_i7=s.index('TP.register({id:"lp7-g7"'); _j7=s.index('TP.register({id:',_i7+10); _m7=s[_i7:_j7]
_R7=[('["threepence","three old British pennies. Twelve pennies made one shilling."],',''),
('["shilling","an old British coin worth twelve pence"],',''),
('such as steward, shilling, ledger','such as steward, Institute, ledger'),
('Threepence. She stood up in front of a full hall over threepence.','A quarter. She stood up in front of a full hall over a quarter.'),
('"Threepence a Week"','"A Quarter a Week"'),
('"Pence paid, p","3","12","24","156"','"Dollars paid, p","0.25","1","2","13"'),
('(0, 0) and (1, 3) would','(0, 0) and (1, 0.25) would'),
('3 divided by 1, 12 divided by 4, 24 divided by 8, and 156 divided by 52 are all 3.','0.25 divided by 1, 1 divided by 4, 2 divided by 8, and 13 divided by 52 are all 0.25.'),
('"3, meaning 3 pence for every week paid.','"0.25, meaning $0.25 (a quarter) for every week paid.'),
('p = 3w. The point (0, 0)','p = 0.25w. The point (0, 0)'),
('(1, 3) means one week costs 3 pence,','(1, 0.25) means one week costs $0.25,'),
('0.28, or 28 pence.','0.28, or 28 cents.'),('another 3 pence each','another 3 cents each'),
('ten shillings','ten dollars'),('eleven shillings','eleven dollars'),
('the threepence','the quarter'),('our threepence','our quarter'),('threepence','a quarter')]
for _a,_b in _R7:
    assert _a in _m7,('lp7 missing',_a)
    _m7=_m7.replace(_a,_b)
s=s[:_i7]+_m7+s[_j7:]
_np=s.count('\u00a3'); s=s.replace('\u00a3','$'); s=s.replace('&pound;','$'); print('pound signs to dollars',_np)
s=s.replace('The eight draws, in pounds','The eight draws, in dollars').replace('costs k pounds','costs k dollars')
_n9=len(_dec.findall(s));s=_dec.sub(_sub9,s);print('removed math decorations (final)',_n9-len(_dec.findall(s)))
open(B+'work/patched.html','w').write(s)
print('patched',len(s),'gx bytes',len(js))
