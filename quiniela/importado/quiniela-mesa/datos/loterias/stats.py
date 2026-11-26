import math, statistics as st
S={'J1':'11X1X1XX121X1X','J2':'2X212XX22X1X11','J3':'11211212X21111','J4':'11221XXX21221X',
'J5':'12211112XX1112','J6':'X2211122121121','J7':'12212111122222','J8':'XX21X122111112',
'J9':'12XX121112122X','J10':'2121X22XX1X1X2','J11':'211X21XXX112X1','J12':'X21X11XX111121',
'J13':'11122X12112X2X','J14':'2X2X121X211121','J15':'2111X1X1111222'}
W={'J1':1,'J2':1,'J3':10,'J4':2,'J5':270,'J6':6,'J7':1,'J8':22,'J9':0,'J10':0,'J11':1,'J12':32,'J13':0,'J14':50}
R={'J1':1.71,'J2':2.45,'J3':2.59,'J4':3.03,'J5':1.00,'J6':2.43,'J7':1.32,'J8':3.78,'J9':1.45,'J10':0.73,'J11':1.46,'J12':3.50,'J13':1.00,'J14':3.49}
T={'J1':'liga','J2':'liga','J3':'liga+F','J4':'liga+F','J5':'europa','J6':'liga+F','J7':'liga-midweek','J8':'liga','J9':'2a+F','J10':'selecc','J11':'2a+F+sel','J12':'liga','J13':'europa','J14':'liga+F','J15':'europa'}
for j,s in S.items(): assert len(s)==14,(j,len(s))
tot={'1':0,'X':0,'2':0}
for s in S.values():
    for c in s: tot[c]+=1
n=sum(tot.values()); print('Signos totales',n,{k:f"{v} ({v/n:.0%})" for k,v in tot.items()})
print('\nJornada tipo        1  X  2  acert14  recaud  14 por millón€')
rows=[]
for j,s in S.items():
    c={k:s.count(k) for k in '1X2'}
    w=W.get(j); r=R.get(j)
    pm = (w/r if w is not None else None)
    rows.append((j,c,w,r,pm))
    print(f"{j:<4} {T[j]:<13} {c['1']:>2} {c['X']:>2} {c['2']:>2}  {'' if w is None else w:>7}  {'' if r is None else r:>6}  {'' if pm is None else round(pm,1)}")
# correlation of log(14 per M€ +0.5) with #non-1 signs
xs=[];ys=[];zs=[]
for j,c,w,r,pm in rows:
    if pm is None: continue
    xs.append(c['X']+c['2']); zs.append(c['X']); ys.append(math.log(pm+0.5))
def corr(a,b):
    ma,mb=st.mean(a),st.mean(b); return sum((x-ma)*(y-mb) for x,y in zip(a,b))/math.sqrt(sum((x-ma)**2 for x in a)*sum((y-mb)**2 for y in b))
print('\ncorr(log 14/M€, nº de signos no-1) =',round(corr(xs,ys),2))
print('corr(log 14/M€, nº de X) =',round(corr(zs,ys),2))
# position analysis for domestic liga+F jornadas: positions 1-7 Primera, 8-10 Segunda, 11-14 LigaF
grp={'Primera(1-7)':range(0,7),'Segunda(8-10)':range(7,10),'LigaF(11-14)':range(10,14)}
for g,rg in grp.items():
    c={'1':0,'X':0,'2':0}
    for j in ['J3','J4','J6','J14']:
        for i in rg: c[S[j][i]]+=1
    m=sum(c.values()); print(g,{k:f"{v/m:.0%}" for k,v in c.items()},'n=',m)
by={}
for j,s in S.items():
    t='europa' if T[j]=='europa' else 'selecc' if 'sel' in T[j] else 'domestica'
    d=by.setdefault(t,{'1':0,'X':0,'2':0})
    for c in s: d[c]+=1
for t,d in by.items():
    m=sum(d.values()); print(t,{k:f"{v/m:.0%}" for k,v in d.items()},'n=',m)
