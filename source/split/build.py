import re,os,shutil
HERE=os.path.dirname(os.path.abspath(__file__))
src=open(os.path.join(HERE,'..','work','patched.html')).read()
DOCS=os.path.join(HERE,'..','..','docs')
DATA=os.path.join(DOCS,'data')
shutil.rmtree(DATA,ignore_errors=True);os.makedirs(DATA)
for f in os.listdir(DOCS):
    if f.startswith('treasure-path-lp') and f.endswith('.html'):os.remove(os.path.join(DOCS,f))
# 1. pull every game module (one per grade per LP) out of the page into docs/data/<id>.js
res=[];last=0;n=0
for m in re.finditer(r'<script>TP\.register\(\{id:"(lp\d+-[a-z0-9]+)"',src):
    e=src.index('</script>',m.start())
    code=src[m.start()+len('<script>'):e]
    open(os.path.join(DATA,m.group(1)+'.js'),'w').write(code)
    res.append(src[last:m.start()]);last=e+len('</script>');n+=1
res.append(src[last:]);s=''.join(res)
# 2. late-loaded modules still need the same wrappers the early ones get
old='TP.register=function(m){TP.mods[m.id]=m;'
assert s.count(old)==1
s=s.replace(old,'TP.register=function(m){try{window.TP_PREREG&&window.TP_PREREG(m)}catch(e){console.error(e)}TP.mods[m.id]=m;')
old2='<script>(function(){"use strict";const $=id=>document.getElementById(id);const THEMES=window.TP_THEMES'
assert s.count(old2)==1
s=s.replace(old2,'<script>window.TP_PREREG=window.TP&&window.TP.register;</script>\n'+old2)
assert s.count('<title>Treasure Path Games</title>')==1
open(os.path.join(DOCS,'index.html'),'w').write(s)
print('index.html',len(s),'bytes; modules',n)
