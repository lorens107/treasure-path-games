import json,re,collections
rows=json.load(open('a4a.json'))+json.load(open('a4b.json'))
READ_STD=re.compile(r'^(RF\.(K|1|2)\.(1|3|4)|R[LI]\.(K|1|2)\.10)$')
def is_reading(r): return any(READ_STD.match(s) for s in r['std'])
TEACHERWORDS=re.compile(r'teacher|listen|i read|read to you|read aloud to',re.I)
def student_reads(r):
    sig=[]
    if r['kind'] in('read','fable'):sig.append('passage')
    if r['kind']=='words' or r['words']:sig.append('words')
    d=r['dir']
    if re.search(r'\b(read|reads|reading|sound out)\b',d,re.I) and not re.search(r'teacher (will )?reads?|your teacher read|listen',d,re.I):
        if re.search(r'count and read|then read the numbers|read the numbers',d,re.I) and any(s.startswith(('1.NBT','2.NBT','K.CC')) for s in r['std']): sig.append('numerals')
        else: sig.append('dir')
    if re.search(r'point to each word',d,re.I):sig.append('dir')
    t=' '.join(r['teach'])
    if re.search(r'student reads',t,re.I):sig.append('panel')
    for q in r['qs']:
        if re.search(r'\bread (this|the|each|these|that|it)\b|what does (it|this|the sign|the word) say',q,re.I):sig.append('qs');break
    return sig
viol=[];info=collections.Counter();by=collections.defaultdict(list)
for r in rows:
    s=student_reads(r)
    r['sig']=s;r['reading']=is_reading(r)
    if s and not r['reading'] and s!=['numerals']:
        viol.append(r)
print('parts',len(rows),'student-read signals',sum(1 for r in rows if r['sig']),'violations',len(viol))
seen=set()
for r in viol:
    k=(r['g'],r['title'],','.join(r['std']),r['dir'][:70],','.join(r['sig']))
    if k in seen:continue
    seen.add(k);print(r['g'],'|',r['title'],'|',','.join(r['std']),'|',','.join(r['sig']),'|',r['dir'][:90],'|',r['kind'])
json.dump(rows,open('an4.json','w'))
