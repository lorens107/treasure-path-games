import json,collections,sys
rows=json.load(open('a7a.json'))+json.load(open('a7b.json'))
gs=sys.argv[1].split(',')
D=collections.OrderedDict()
for r in rows:
    if r['g'] not in gs: continue
    d=' '.join((r['desc'] or ('T:'+r['title'])).split()[:9])
    D.setdefault((r['g'],','.join(r['std'])),collections.OrderedDict())
    D[(r['g'],','.join(r['std']))].setdefault(d,0);D[(r['g'],','.join(r['std']))][d]+=1
for k,v in sorted(D.items(),key=lambda x:(gs.index(x[0][0]),x[0][1])):
    print('##',k[0],k[1]);
    for d,n in v.items():print('   ',n,d)
