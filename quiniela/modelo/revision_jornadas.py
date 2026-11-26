#!/usr/bin/env python3
"""Revisión de todas las jornadas jugadas (24/11/2026) y prueba de R5b (casas frente a mesa).

Uso (desde quiniela/):
  python3 modelo/revision_jornadas.py                       # J19-J23: aciertos, calibración, fijos, X
  python3 -I modelo/revision_jornadas.py ruta/Matches.csv   # + 1.372 partidos de Primera/Segunda 2024-26 con cuota
Matches.csv: raw.githubusercontent.com/xgabora/Club-Football-Match-Data-2000-2025/main/data/Matches.csv (clase B).
Emparejado sin nombres: fecha + división; solo días en que coinciden el número de partidos y los resultados
(la selección depende del calendario, no del modelo). Dentro de un día, la cuota de los partidos con el mismo
resultado se promedia (eso solo perjudica a las casas: la ventaja medida es prudente).
"""
import json, math, collections, sys
S='1X2'
app={ (r['jornada'],r['n']):r for r in json.load(open('app/datos/partidos.json'))['rows']}
rows=[]
for j in (19,20,21,22,23):
    d=json.load(open(f'jornadas/j{j}/j{j}.json'))
    cols=d.get('columnas_jugadas')
    pub=(d.get('publico') or {}).get('porcentajes')
    for p in d['partidos']:
        r=p.get('resultado')
        if r not in ('1','X','2'): continue
        r = r
        pr=p['p']; m=p.get('mercado')
        a=app.get((j,p['n']))
        if not m and a and a.get('m1') is not None: m=[a['m1'],a['mx'],a['m2']]
        pu=None
        if pub and str(p['n']) in pub: pu=[x/100 for x in pub[str(p['n'])]['lae']]
        cov=None
        if cols: cov=sum(1 for c in cols if c[p['n']-1]==r)/len(cols)
        elif j==19: cov=1.0 if r in p.get('signo_boleto_18eur','') else 0.0
        fijo=None
        if cols: fijo=len(set(c[p['n']-1] for c in cols))==1 and None or None
        signs_cov=set(c[p['n']-1] for c in cols) if cols else (set(p.get('signo_boleto_18eur','')) if j==19 else None)
        rows.append(dict(j=j,n=p['n'],partido=p['partido'],comp=p.get('competicion'),p=pr,m=m,pu=pu,r=r,cov=cov,signs=signs_cov,marc=p.get('marcador')))
def ll(q,r): return -math.log(max(q[S.index(r)],1e-6))
print('N',len(rows))
# per jornada
for j in (19,20,21,22,23):
    R=[x for x in rows if x['j']==j]
    top=sum(1 for x in R if S[x['p'].index(max(x['p']))]==x['r'])
    exp=sum(max(x['p']) for x in R)
    L=sum(ll(x['p'],x['r']) for x in R)/len(R)
    Rm=[x for x in R if x['m']]; Lm=sum(ll(x['m'],x['r']) for x in Rm)/len(Rm) if Rm else None
    Lmm=sum(ll(x['p'],x['r']) for x in Rm)/len(Rm) if Rm else None
    Rp=[x for x in R if x['pu']]; Lp=sum(ll(x['pu'],x['r']) for x in Rp)/len(Rp) if Rp else None
    Lpm=sum(ll(x['p'],x['r']) for x in Rp)/len(Rp) if Rp else None
    xs=sum(1 for x in R if x['r']=='X'); xp=sum(x['p'][1] for x in R)
    print(j,len(R),'fav acierta',top,'esp %.1f'%exp,'LL %.3f'%L,'| mercado n',len(Rm), Lm and 'mesa %.3f casas %.3f'%(Lmm,Lm),'| publico n',len(Rp),Lp and 'mesa %.3f pub %.3f'%(Lpm,Lp),'| X real',xs,'esp %.1f'%xp)
# global
R=rows
print('TOTAL fav',sum(1 for x in R if S[x['p'].index(max(x['p']))]==x['r']),'esp %.1f'%sum(max(x['p']) for x in R),'LL %.3f'%(sum(ll(x['p'],x['r']) for x in R)/len(R)),'X',sum(x['r']=='X' for x in R),'esp %.1f'%sum(x['p'][1] for x in R), '1',sum(x['r']=='1' for x in R),'esp %.1f'%sum(x['p'][0] for x in R),'2',sum(x['r']=='2' for x in R),'esp %.1f'%sum(x['p'][2] for x in R))
# calibration of all sign probabilities
bins=[(0,.2),(.2,.3),(.3,.4),(.4,.5),(.5,.6),(.6,.7),(.7,1.01)]
print('Calibración (todas las probs de signo):')
for lo,hi in bins:
    sel=[(x['p'][i],x['r']==S[i]) for x in R for i in range(3) if lo<=x['p'][i]<hi]
    if sel: print(f'  {lo:.0%}-{hi:.0%}: n={len(sel)} dada {sum(a for a,_ in sel)/len(sel):.1%} real {sum(b for _,b in sel)/len(sel):.1%}')
print('Favorito por tramo:')
for lo,hi in [(0,.45),(.45,.55),(.55,.65),(.65,1.01)]:
    sel=[x for x in R if lo<=max(x['p'])<hi]
    if sel: print(f'  {lo:.0%}-{hi:.0%}: n={len(sel)} dada {sum(max(x["p"]) for x in sel)/len(sel):.1%} gana {sum(S[x["p"].index(max(x["p"]))]==x["r"] for x in sel)/len(sel):.1%} X real {sum(x["r"]=="X" for x in sel)/len(sel):.1%} X dada {sum(x["p"][1] for x in sel)/len(sel):.1%}')
print('Por competición:')
cc=collections.defaultdict(list)
for x in R: cc[x['comp']].append(x)
for c,v in cc.items():
    print(f'  {c}: n={len(v)} fav {sum(S[x["p"].index(max(x["p"]))]==x["r"] for x in v)}/{len(v)} esp {sum(max(x["p"]) for x in v):.1f} X {sum(x["r"]=="X" for x in v)} esp {sum(x["p"][1] for x in v):.1f} LL {sum(ll(x["p"],x["r"]) for x in v)/len(v):.3f}')
# mesa vs casas head to head
Rm=[x for x in R if x['m']]
print('Mesa vs casas n',len(Rm),'LL mesa %.3f casas %.3f'%(sum(ll(x['p'],x['r']) for x in Rm)/len(Rm),sum(ll(x['m'],x['r']) for x in Rm)/len(Rm)))
print(' fav casas acierta',sum(S[x['m'].index(max(x['m']))]==x['r'] for x in Rm),'fav mesa',sum(S[x['p'].index(max(x['p']))]==x['r'] for x in Rm))
# where mesa is above market on fav
up=[x for x in Rm if max(x['p'])-x['m'][x['p'].index(max(x['p']))]>=0.05]
print(' mesa >=5 pts sobre casas en su favorito: n',len(up),'gana',sum(S[x['p'].index(max(x['p']))]==x['r'] for x in up),'mesa media %.2f casas media %.2f'%(sum(max(x['p']) for x in up)/max(1,len(up)), sum(x['m'][x['p'].index(max(x['p']))] for x in up)/max(1,len(up))))
for x in up: print('   ',x['j'],x['partido'],[round(v*100) for v in x['p']],[round(v*100) for v in x['m']],x['r'])
dn=[x for x in Rm if x['m'][1]-x['p'][1]>=0.04]
print(' X casas >= mesa+4: n',len(dn),'X salieron',sum(x['r']=='X' for x in dn))
# fijos fallados
print('Fijos (un solo signo en todas las columnas) y fallos:')
for x in R:
    if x['signs'] is not None and len(x['signs'])==1:
        ok = x['r'] in x['signs']
        if not ok: print('  FALLO',x['j'],x['partido'],x['comp'],'fijo',x['signs'],'mesa',[round(v*100) for v in x['p']],'casas',x['m'] and [round(v*100) for v in x['m']],'res',x['r'],x['marc'])
F=[x for x in R if x['signs'] is not None and len(x['signs'])==1]
print(' fijos',len(F),'acertados',sum(x['r'] in x['signs'] for x in F),'esperados %.1f'%sum(x['p'][S.index(list(x['signs'])[0])] for x in F))
for lo,hi in [(0,.55),(.55,.7),(.7,1.01)]:
    sel=[x for x in F if lo<=x['p'][S.index(list(x['signs'])[0])]<hi]
    print(f'  fijo P {lo:.0%}-{hi:.0%}: n={len(sel)} ac {sum(x["r"] in x["signs"] for x in sel)} esp {sum(x["p"][S.index(list(x["signs"])[0])] for x in sel):.1f}')
# coverage failures (partidos no cubiertos)
print('Partidos que tumban (cobertura del signo real < 25% de columnas):')
for x in R:
    if x['cov'] is not None and x['cov']<0.25: print('  ',x['j'],x['n'],x['partido'],'res',x['r'],'cob %.0f%%'%(100*x['cov']),'mesa',[round(v*100) for v in x['p']])

if len(sys.argv) > 1:
    import csv, statistics as st
    A = json.load(open('datos/auditoria_ventaja.json'))
    O = collections.defaultdict(list)
    for r in csv.DictReader(open(sys.argv[1], encoding='utf-8')):
        if r['Division'] not in ('SP1', 'SP2'): continue
        try: o = [float(r['OddHome']), float(r['OddDraw']), float(r['OddAway'])]
        except ValueError: continue
        q = [1 / x for x in o]; s = sum(q)
        O[(r['MatchDate'], 'es.1' if r['Division'] == 'SP1' else 'es.2')].append(([x / s for x in q], 'HDA'.index(r['FTResult'])))
    G = collections.defaultdict(list)
    for a in A: G[(a['date'], a['comp'])].append(a)
    P = []
    for k, v in G.items():
        o = O.get(k, [])
        if len(v) != len(o) or sorted(a['r'] for a in v) != sorted(x[1] for x in o): continue
        byr = collections.defaultdict(list)
        for q, r in o: byr[r].append(q)
        for a in v: P.append((a, [st.mean(q[i] for q in byr[a['r']]) for i in range(3)]))
    L = lambda p, r: -math.log(p[r])
    print('\nCasas frente a mesa, Primera y Segunda 2024-26 (fuera de muestra): n', len(P))
    for w in (0, .5, .75, .9, 1):
        print(f'  mezcla {w:.2f} casas: log-loss {st.mean(L([(1-w)*a+w*b for a,b in zip(x["p"],m)], x["r"]) for x,m in P):.4f}')
    d = [L(x['p'], x['r']) - L(m, x['r']) for x, m in P]
    print(f'  mesa − casas {st.mean(d):.4f} (error {st.stdev(d)/len(d)**.5:.4f})')
    for lab, sel in (('2024-25', [p for p in P if p[0]['date'] < '2025-07-01']), ('2025-26', [p for p in P if p[0]['date'] >= '2025-07-01'])):
        print(f'  {lab}: n {len(sel)} mesa {st.mean(L(x["p"],x["r"]) for x,m in sel):.4f} casas {st.mean(L(m,x["r"]) for x,m in sel):.4f}')
    S8 = [(x, m) for x, m in P if max(x['p']) >= .45 and max(x['p']) - m[x['p'].index(max(x['p']))] >= .08]
    print(f'  favorito de la mesa ≥ 8 puntos sobre las casas: n {len(S8)}, mesa {st.mean(max(x["p"]) for x,m in S8):.3f}, '
          f'casas {st.mean(m[x["p"].index(max(x["p"]))] for x,m in S8):.3f}, ganó {st.mean(x["p"].index(max(x["p"]))==x["r"] for x,m in S8):.3f}')
