#!/usr/bin/env python3
"""Director J19: boletos A (4 dobles completos) y B (reducida 7 dobles) con partidos vetados
(que no pueden ir de sencillo). Métricas exactas P(14), P(>=13), P(>=12).
Uso: python3 j19_director.py precios.json '[1,2,8]'   (lista de vetos, números de partido)"""
import itertools, json, math, sys, importlib.util, os
HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("r7", os.path.join(HERE, "reducida7.py"))
r7 = importlib.util.module_from_spec(spec); spec.loader.exec_module(r7)
S = "1X2"
rows = [r for r in json.load(open(sys.argv[1]))["rows"] if r["n"] <= 14]
veto = set(json.loads(sys.argv[2])) if len(sys.argv) > 2 else set()
P = [r["p"] for r in rows]; N = len(P)
order = [sorted(range(3), key=lambda k: -p[k]) for p in P]
def colsA(D):
    base = [order[i][0] for i in range(N)]
    out = []
    for bits in itertools.product((0, 1), repeat=len(D)):
        c = base[:]
        for b, d in zip(bits, D): c[d] = order[d][b]
        out.append(c)
    return out
def p14A(D):
    return math.prod((P[i][order[i][0]] + P[i][order[i][1]]) if i in D else P[i][order[i][0]] for i in range(N))
vidx = {i for i in range(N) if rows[i]["n"] in veto}
res = []
for D in itertools.combinations(range(N), 4):
    broken = len(vidx - set(D))
    res.append((broken, -p14A(D), D))
res.sort()
best_free = max(res, key=lambda x: -x[1])
def show(D, cols, tag):
    d = r7.exact(P, cols)
    s = []
    for i in range(N):
        if i in D:
            sig = "".join(sorted(S[order[i][0]] + S[order[i][1]], key=S.index))
        else: sig = S[order[i][0]]
        s.append(sig)
    return {"tag": tag, "dobles": [rows[i]["n"] for i in D], "signos": s,
            "vetos_rotos": sorted(rows[i]["n"] for i in vidx - set(D)),
            "p14": float(d[14:].sum()), "p13": float(d[13:].sum()), "p12": float(d[12:].sum()),
            "cols": ["".join(S[x] for x in c) for c in cols]}
out = []
_, _, D = best_free; out.append(show(set(D), colsA(D), "A libre (máx. P14)"))
minb = res[0][0]
for k, (b, negp, D) in enumerate([x for x in res if x[0] == minb][:3]):
    out.append(show(set(D), colsA(D), f"A con vetos (rompe {b}) #{k+1}"))
# B reducida con vetos dentro de los 7 dobles
best = None
for D in itertools.combinations(range(N), 7):
    if not vidx <= set(D): continue
    singles = [i for i in range(N) if i not in D]
    ps = math.prod(P[i][order[i][0]] for i in singles)
    pd = [(P[d][order[d][0]], P[d][order[d][1]]) for d in D]
    for shift in itertools.product((0, 1), repeat=7):
        words = [tuple(a ^ b for a, b in zip(w, shift)) for w in r7.HAM]
        mass = sum(math.prod(pd[k][w[k]] for k in range(7)) for w in words)
        if best is None or ps * mass > best[0]: best = (ps * mass, D, words)
if best:
    _, D, words = best; cols = []
    for w in words:
        c = [order[i][0] for i in range(N)]
        for k, d in enumerate(D): c[d] = order[d][w[k]]
        cols.append(c)
    out.append(show(set(D), cols, "B reducida 7 dobles (vetos dentro)"))
for o in out:
    print(f"{o['tag']:<34} dobles {o['dobles']}  vetos rotos {o['vetos_rotos']}  P14 1/{1/o['p14']:,.0f}  P13 {o['p13']:.2%}  P12 {o['p12']:.2%}")
    print("   ", " ".join(o["signos"]))
json.dump(out, open(sys.argv[1].replace(".json", "_director.json"), "w"), ensure_ascii=False, indent=1)
