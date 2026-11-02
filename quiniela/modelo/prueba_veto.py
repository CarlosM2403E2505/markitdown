import importlib.util, json, math, collections, os
from datetime import date
import numpy as np
from scipy.stats import poisson
spec = importlib.util.spec_from_file_location("em", os.path.join(os.path.dirname(os.path.abspath(__file__)),"euro_model.py"))
em = importlib.util.module_from_spec(spec); spec.loader.exec_module(em)
S=os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","datos")
ms=json.load(open(os.path.join(S,"euro_j19.json")))["matches"]
U=[m for m in ms if m["competition"].split(":")[0] in ("uefa.cl","uefa.el","uefa.conf")]
U.sort(key=lambda m:m["date"])
# Walk-forward light: fit at 3 cutoffs, predict the following window out of sample
cuts=[("2025-07-01","2026-07-01"),("2026-07-01","2026-11-02")]
rows=[]
for c0,c1 in cuts:
    train=[m for m in ms if m["date"]<c0]
    m=em.EuroPoisson(xi=0.0015, ridge=10, scale=1.05, blend=0.2, hier=True).fit(train, ref_date=date.fromisoformat(c0))
    last=collections.defaultdict(lambda:None)  # last UEFA result per team within season
    for x in U:
        if not (c0<=x["date"]<c1): continue
        h,a=x["home"],x["away"]
        try: lam,mu=m.rates(h,a)
        except Exception: continue
        G=np.arange(11); M=np.outer(poisson.pmf(G,lam),poisson.pmf(G,mu)); M/=M.sum(); i,j=np.indices(M.shape)
        p=[M[i>j].sum(),M[i==j].sum(),M[i<j].sum()]
        res=0 if x["hg"]>x["ag"] else 1 if x["hg"]==x["ag"] else 2
        fav=0 if p[0]>=p[2] else 2
        favteam=h if fav==0 else a
        lr=last[favteam]
        rows.append({"pfav":p[fav],"win":int(res==fav),"afterloss":lr=="L","prevknown":lr is not None,"comp":x["competition"]})
        # update last results
        last[h]="W" if res==0 else "D" if res==1 else "L"
        last[a]="W" if res==2 else "D" if res==1 else "L"
pass
for grp,cond in (("tras derrota",lambda r:r["prevknown"] and r["afterloss"]),("tras no derrota",lambda r:r["prevknown"] and not r["afterloss"])):
    g=[r for r in rows if cond(r)]
    n=len(g); exp=sum(r["pfav"] for r in g); act=sum(r["win"] for r in g)
    var=sum(r["pfav"]*(1-r["pfav"]) for r in g)
    print(f"{grp}: n={n} esperado {exp:.1f} real {act} ({act/n:.1%} vs {exp/n:.1%}) z={(act-exp)/math.sqrt(var):.2f}")
    g2=[r for r in g if r["pfav"]>=0.5]
    n=len(g2); exp=sum(r["pfav"] for r in g2); act=sum(r["win"] for r in g2); var=sum(r["pfav"]*(1-r["pfav"]) for r in g2)
    print(f"   favoritos >=50%: n={n} esperado {exp:.1f} real {act} z={(act-exp)/math.sqrt(var):.2f}")
