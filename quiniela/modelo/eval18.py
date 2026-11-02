import json, math, itertools, importlib.util, os
spec = importlib.util.spec_from_file_location("r7", os.path.join(os.path.dirname(os.path.abspath(__file__)),"reducida7.py"))
r7 = importlib.util.module_from_spec(spec); spec.loader.exec_module(r7)
S="1X2"; import os; SP=os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","datos")
F=[r['p'] for r in json.load(open(os.path.join(SP,'j19_precio_final.json')))['rows'] if r['n']<=14]
MK=[[77,13,10],[52,24,24],[41,24,35],[19.5,20.6,59.9],[11,14,75],[19,21,60],[55.5,22.4,22.1],[43,26,31],[32,24,44],[18,20,62],[10,15,75],[48.8,24.8,26.5],[46,25,28],[18,25,57]]
MK=[[x/sum(r) for x in r] for r in MK]; BL=[[(a+b)/2 for a,b in zip(f,m)] for f,m in zip(F,MK)]
order=[sorted(range(3),key=lambda k:-p[k]) for p in F]
def spec_cols(dobles, triples):
    opts=[]
    for i in range(14):
        n=i+1
        if n in triples: opts.append([0,1,2])
        elif n in dobles: opts.append(order[i][:2])
        else: opts.append([order[i][0]])
    return [list(c) for c in itertools.product(*opts)], opts
def p14(opts,Pt): return math.prod(sum(Pt[i][k] for k in o) for i,o in enumerate(opts))
designs={
 '12€ robusta: D 2,3,9,13':([2,3,9,13],[]),
 '18€ T8 + D 1,2,3':([1,2,3],[8]),
 '18€ T2 + D 1,3,8':([1,3,8],[2]),
 '18€ T3 + D 1,2,8':([1,2,8],[3]),
 '18€ T1 + D 2,3,8':([2,3,8],[1]),
}
# best unconstrained 1T+3D for reference
best=None
for T in range(1,15):
    for D in itertools.combinations([n for n in range(1,15) if n!=T],3):
        _,o=spec_cols(list(D),[T]); v=p14(o,F)
        if best is None or v>best[0]: best=(v,list(D),[T])
designs[f'18€ libre (sin regla): T{best[2][0]} + D {",".join(map(str,best[1]))}']=(best[1],best[2])
for name,(D,T) in designs.items():
    cols,o=spec_cols(D,T)
    d=r7.exact(F,cols)
    sig=["".join(S[k] for k in sorted(x)) for x in o]
    print(f"{name:<34} col {len(cols)}  P14 1/{1/p14(o,F):,.0f}  mercado 1/{1/p14(o,MK):,.0f}  mezcla 1/{1/p14(o,BL):,.0f}  P13 {d[13:].sum():.2%}  P12 {d[12:].sum():.2%} | {' '.join(sig)}")
