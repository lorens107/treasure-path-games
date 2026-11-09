import json,re,collections
rows=json.load(open('a5a.json'))+json.load(open('a5b.json'))
RS=re.compile(r'^(RF\.(K|1|2)\.(1|3|4)|R[LI]\.(K|1|2)\.10)$')
def rstd(r):return any(RS.match(s) for s in r['std'])
def kindread(r):return r['kind'] in('read','fable','words')
SR=re.compile(r'student reads|reads (it|the passage|the text|the words|the story|each word)|read (it|the passage|the words|each word)[^.]{0,30}(out loud|aloud)|on their own|reads? (them|these) out loud',re.I)
TR=re.compile(r'Read aloud to the student|Read the text marked|read the text on the screen aloud|not expected to read|Say each prompt|Read each (prompt|question)',re.I)
cnt=collections.Counter();ex=collections.defaultdict(list)
def f(k,r):
    cnt[k]+=1
    key=(r['g'],r['title'],','.join(r['std']))
    if key not in [e[:3] for e in ex[k]] and len(ex[k])<40: ex[k].append(key+(r['dir'][:80],r['panel'][:160]))
for r in rows:
    rd=rstd(r) or kindread(r); p=r['panel']; d=r['dir']
    if not r['hasPanel']: f('no panel',r); continue
    # A non-reading part tells student to read
    if not rd and re.search(r'\bread\b',d,re.I) and not re.search(r'listen|teacher reads|your teacher will read|read (the )?(number|numeral)s?\b',d,re.I): f('A nonreading dir says read',r)
    if not rd and SR.search(p): f('B nonreading panel says student reads',r)
    if rd and re.search(r'Read aloud to the student|read the text on the screen aloud',p): f('C reading part but teacher reads text',r)
    if rd and not SR.search(p) and r['kind'] in('read','fable'): f('D fluency part panel lacks student-reads',r)
    vis=len(r['text'].split())
    if not rd and vis>=6 and not TR.search(p) and not r['hasRead']: f('E nonreading with text but no teacher-reads line',r)
    if rd and re.search(r'^\s*Listen',d): f('F reading but dir says Listen',r)
    if not rd and re.search(r'^\s*Read (the|this|each|these|a|an)\b',d): f('G nonreading dir starts with Read',r)
for k,v in sorted(cnt.items()):
    print('\n##',k,v)
    for e in ex[k][:14]:print('  ',e)
