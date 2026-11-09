# Kindergarten: replace the number path (1 to 10/15/16/20/40) with one number line from 0 to 20, all LPs
import re as _re
_tool=_re.compile(r'np:\{name:"Number path 1 to \d+",std:\[([^\]]*)\],html:(?:npHtml|tpsNpHtml),bind:\(b,r\)=>b\.querySelectorAll\("\[data-n\]"\)\.forEach\(x=>x\.onclick=\(\)=>\{(?:npOn|tpsNpOn)\[x\.dataset\.n\]=!(?:npOn|tpsNpOn)\[x\.dataset\.n\];r\(\)\}\)\}')
_starts=[(m.start(),m.group(1)) for m in _re.finditer(r'TP\.register\(\{id:"(lp\d+-g[a-z0-9]+)"',s)]
_out=[];_last=0;_n=0
for _k,(_p,_id) in enumerate(_starts):
    _e=_starts[_k+1][0] if _k+1<len(_starts) else len(s)
    _seg=s[_p:_e]
    if _id.endswith('-gk'):
        _seg,_c=_tool.subn(lambda m:'np:{name:"Number line 0 to 20",std:['+m.group(1)+'],html:()=>window.TPNL20(),bind:(b,r)=>window.TPNL20Bind(b,r)}',_seg)
        assert _c==1,(_id,_c); _n+=_c
        _seg=_seg.replace('number path','number line').replace('Number path','Number line')
    _out.append(s[_last:_p]);_out.append(_seg);_last=_e
_out.append(s[_last:]);s=''.join(_out)
assert _n==10,_n

_i=s.find('goalClosed:()=>basket(0,false)');_j=s.find('goalMark:',_i);assert _i>0 and _j>_i
_seg=s[_i:_j];assert _seg.count('Pc(hay,')==6,_seg.count('Pc(hay,')
s=s[:_i]+_seg.replace('Pc(hay,','Pc(hayA,')+s[_j:]

import re as _re
def _tl(m):
    dur=int(round(int(m.group(2))*3/5/5)*5)
    return m.group(1)+'n:3,dur:'+str(dur)+m.group(3)+'desc:"print concepts (counting words and letters)"'+m.group(4)
_pat=_re.compile(r'(title:"Two Lines",std:\["RF\.K\.1"\],)n:5,dur:(\d+)(,dir:"[^"]*",)desc:"print concepts \(where to start, where to go at the end of a line, counting words and letters\)"(,html:\(\)=>linesFig\(\),key:\[)"(?:[^"\\]|\\.)*","(?:[^"\\]|\\.)*",')
s,_n2=_pat.subn(_tl,s);assert _n2==7,_n2
_o='n:5,dur:75,dir:"Look at the sign and the cards. Answer out loud.",desc:"print concepts (where to start reading, counting words, telling a letter from a word)",html:()=>signFig(),key:["Ask: I want to read the sign. Do I start at the bee or at the crate? (at the bee. Reading starts on the left.)","'
assert s.count(_o)==1
s=s.replace(_o,'n:4,dur:60,dir:"Look at the sign and the cards. Answer out loud.",desc:"print concepts (counting words, telling a letter from a word)",html:()=>signFig(),key:["',1)
