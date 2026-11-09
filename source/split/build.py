import re,sys
src=open(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)),'..','work','patched.html')).read()
def build(lo,hi,out,label,suffix):
    s=src
    # drop modules of other LPs
    parts=[]
    pos=0
    for m in re.finditer(r'<script>TP\.register\(\{id:"lp(\d+)-',s):
        pass
    res=[];last=0
    for m in re.finditer(r'<script>TP\.register\(\{id:"lp(\d+)-[a-z0-9]+"',s):
        n=int(m.group(1))
        e=s.index('</script>',m.start())+len('</script>')
        if lo<=n<=hi:continue
        res.append(s[last:m.start()]);last=e
    res.append(s[last:]);s=''.join(res)
    if lo>5:
        s=re.sub(r'<script>window\.TP_IMG1=.*?</script>\n','',s,count=1,flags=re.S)
    # catalog trim
    cm=re.search(r'window\.TP_CATALOG=(\{.*?\}\});',s,re.S)
    import json
    cat=json.loads(cm.group(1))
    cat={k:v for k,v in cat.items() if lo<=int(k)<=hi}
    s=s[:cm.start(1)]+json.dumps(cat,separators=(',',':'))+s[cm.end(1):]
    # settings
    def rep(o,n,c=1):
        nonlocal s
        assert s.count(o)==c,(o[:60],s.count(o));s=s.replace(o,n)
    rep('const KEY="treasure-path-suite-v1";','const LPMIN=%d,LPMAX=%d;const KEY="treasure-path-suite-v1%s";'%(lo,hi,suffix))
    rep('const LKEY="treasure-path-suite-records-v1";','const LKEY="treasure-path-suite-records-v1%s";'%suffix)
    rep('lp:k.lp||1,','lp:k.lp||LPMIN,')
    rep('return s&&s.v===1?s:null}catch(e){return null}}','return s&&s.v===1&&s.lp>=LPMIN&&s.lp<=LPMAX?s:null}catch(e){return null}}')
    rep('$("lpRow").innerHTML=LPS.map(l=>{','$("lpRow").innerHTML=LPS.filter(l=>l.n>=LPMIN&&l.n<=LPMAX).map(l=>{')
    rep('<title>Treasure Path Games</title>','<title>Treasure Path Games, %s</title>'%label)
    open(out,'w').write(s);print(out,len(s))
import os
D=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','docs')+'/'
for n in range(1,11):
    build(n,n,D+'treasure-path-lp%d.html'%n,'LP %d'%n,'-lp%d'%n)
