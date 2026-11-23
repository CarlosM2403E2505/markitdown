"""Histórico oficial LAE de jornadas europeas (Champions/Europa/Conference) frente a las de fin de semana.
Uso: python3 herramientas/historico_europeo.py   (lee datos/lae_historico.json, 612 jornadas 2018-2026)."""
import json,statistics as st,collections as C,datetime as DT
d=json.load(open('datos/lae_historico.json'))['jornadas']
U="""2018-02-21 2018-02-14 2018-11-28 2018-11-07 2018-10-24 2018-10-03 2018-09-19 2019-03-13 2019-03-06 2019-02-20 2019-02-13 2019-12-11 2019-11-27 2019-11-06 2019-10-23 2019-10-02 2019-09-18 2020-02-26 2020-02-19 2020-12-09 2020-12-02 2020-11-25 2020-11-04 2020-10-28 2020-10-21 2021-02-24 2021-02-17 2021-12-08 2021-11-24 2021-11-03 2021-10-20 2021-09-29 2021-09-15 2022-03-16 2022-03-09 2022-02-23 2022-02-16 2022-11-02 2022-10-26 2022-10-12 2022-10-05 2022-09-14 2022-09-07 2023-03-15 2023-03-08 2023-02-22 2023-02-15 2023-12-13 2023-11-29 2023-11-08 2023-10-25 2023-10-04 2023-09-20 2024-04-17 2024-04-10 2024-03-13 2024-03-06 2024-02-21 2024-02-14 2024-12-11 2024-11-27 2024-11-06 2024-10-23 2024-10-02 2024-09-18 2025-04-16 2025-04-09 2025-03-12 2025-03-05 2025-02-19 2025-02-12 2025-01-29 2025-01-22 2025-12-18 2025-12-10 2025-11-26 2025-11-05 2025-10-22 2025-10-01 2025-09-17 2026-04-15 2026-04-08 2026-03-18 2026-03-11 2026-02-18 2026-01-28 2026-01-21 2026-11-04 2026-10-21 2026-10-14 2026-09-09""".split()
def wd(f):return DT.date.fromisoformat(f).weekday()
uefa=[r for r in d if r['f'] in U]
# baseline: weekend jornadas (sorteo sab/dom/lun) with >=13 partidos
base=[r for r in d if r['f'] not in U and all(wd(p[4])>=4 or wd(p[4])==0 for p in r['p'][:14] if p[4])]
print('n uefa',len(uefa),'base',len(base),'missing',set(U)-{r['f'] for r in uefa})
def esc(r,k):
  for c in r['e']:
    if c[0]==k: return int(c[1] or 0),float(str(c[2]).replace('.','').replace(',','.') or 0)
  return None,None
def stats(rs,name):
  S=C.Counter();nn=[];w14=[];p14=[];bote=0;pl0=0;rec=[];p13=[]
  for r in rs:
    sg=[p[2] for p in r['p'][:14]];S.update(sg);nn.append(sum(s!='1' for s in sg))
    g,pr=esc(r,2)
    if g is None: continue
    w14.append(g);rec.append(int(r['rec'] or 0)/100)
    if g==0: bote+=1
    else: p14.append(pr)
    g1,_=esc(r,1)
    if g and g1==0: pl0+=1
    g3,pr3=esc(r,3)
    if pr3: p13.append(pr3)
  T=sum(S.values())
  print(f"{name}: {len(rs)} jornadas | 1 {S['1']/T:.1%} X {S['X']/T:.1%} 2 {S['2']/T:.1%} | no-1 por jornada mediana {st.median(nn)} | recaud. mediana {st.median(rec)/1e6:.2f} M€ | acertantes 14 mediana {st.median(w14)} | premio 14 mediana {st.median(p14):,.0f} € | bote 14 {bote}/{len(w14)} | Pleno desierto con 14 {pl0}/{len(w14)-bote} | 13 mediana {st.median(p13):,.0f} €")
stats(uefa,'UEFA');stats(base,'Fin de semana')
import re,unicodedata
def norm(n):
  n=re.sub(r'\s*\((m|f)\)','',n).lower();n=unicodedata.normalize('NFD',n);return ''.join(c for c in n if unicodedata.category(c)!='Mn')
EL=['real madrid','barcelona','bayern','man.city','manchester city','manch. city','manch city','liverpool','psg','arsenal','inter de milan']
ES=['real madrid','barcelona','at. madrid','sevilla','valencia','villarreal','real sociedad','betis','athletic club','girona','getafe','espanyol','granada','celta','osasuna','rayo vallecano']
el=lambda n:any(e==norm(n) or norm(n).startswith(e) for e in EL)
es=lambda n:any(norm(n)==e for e in ES)
def tab(rs,label,pred):
  c=C.Counter()
  for r in rs:
    for p in r['p'][:14]:
      k=pred(p)
      if k: c[(k,p[2])]+=1
  for k in sorted({a for a,_ in c}):
    n=sum(c[(k,s)] for s in '1X2');print(f"  {label} {k}: n={n} 1 {c[(k,'1')]/n:.0%} X {c[(k,'X')]/n:.0%} 2 {c[(k,'2')]/n:.0%}")
def kel(p):
  a,b=el(p[0]),el(p[1])
  return 'elite casa vs no élite' if a and not b else 'no élite vs elite fuera' if b and not a else 'élite vs élite' if a and b else 'sin élite'
def kes(p):
  a,b=es(p[0]),es(p[1])
  if a and b: return None
  return 'español en casa' if a else 'español fuera' if b else None
print('UEFA por partido:');tab(uefa,'',kel);tab(uefa,'',kes)
for nm,rs in [('2018-24 grupos',[r for r in uefa if r['f']<'2024-07']),('2024-26 fase liga',[r for r in uefa if r['f']>'2024-07'])]:
  S=C.Counter(p[2] for r in rs for p in r['p'][:14]);T=sum(S.values());print(nm,len(rs),{k:f'{v/T:.0%}' for k,v in S.items()})
# pleno
P=C.Counter();PS=C.Counter()
for r in uefa:
  p=r['p'][14] if len(r['p'])>14 else None
  if not p or '-' not in p[3]: continue
  a,b=[int(x) for x in p[3].split('-')];f=lambda g:'M' if g>=3 else str(g);P[f(a)+'-'+f(b)]+=1;PS[p[2]]+=1
print('Pleno UEFA',sum(P.values()),P.most_common(8),PS)
# bote by no-1
B=C.defaultdict(list)
for r in uefa:
  g,_=esc(r,2)
  if g is None: continue
  k=sum(p[2]!='1' for p in r['p'][:14]);B[min(max(k,4),10)].append(g==0)
print('bote por nº no-1:',{k:f'{sum(v)}/{len(v)}' for k,v in sorted(B.items())})
G=C.Counter();n=0
for r in uefa:
  p=r['p'][14]
  if norm(p[0]) in ('at. madrid','atletico de madrid','atletico madrid') or el(p[0]):
    a,b=[int(x) for x in p[3].split('-')];n+=1;G[('M' if a>=3 else str(a))+'-'+('M' if b>=3 else str(b))]+=1
print('Pleno con grande en casa',n,G.most_common(6))
print('Pleno locales:',C.Counter(r['p'][14][0] for r in uefa).most_common(8))
g=[r['p'][14] for r in uefa if norm(r['p'][14][0]) in ('at. madrid',) or el(r['p'][14][0])]
print('grande casa M local',sum(int(p[3].split('-')[0])>=3 for p in g),len(g),'signo',C.Counter(p[2] for p in g))
for nm,rs in [('<2024-07',[r for r in uefa if r['f']<'2024-07']),('>2024-07',[r for r in uefa if r['f']>'2024-07'])]: tab(rs,nm,kel)
xs=[sum(p[2]=='X' for p in r['p'][:14]) for r in uefa];print('X por jornada',st.mean(xs),C.Counter(xs))
