"""Rejilla rapida (prediccion vectorizada; misma validacion de origen movil mensual que nat_eval.py).
Uso: python3 nat_grid3.py 'xi1,xi2' 'R1,R2' 'wf1,wf2' salida.json"""
import importlib.util, json, math, sys, os, itertools
from datetime import date
import numpy as np
from scipy.stats import poisson
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
s = importlib.util.spec_from_file_location("ne", os.path.join(BASE, "code", "nat_eval.py")); ne = importlib.util.module_from_spec(s); s.loader.exec_module(ne)
nm, MS = ne.nm, ne.MS
G = np.arange(11)
def run_fast(cfg, start, end):
    xi, R, wf = cfg; res = []
    for t in ne.months(start, end):
        ts, te = t.isoformat(), ne.nxt(t).isoformat()
        test = [m for m in MS if ts <= m["date"] < te]
        if not test: continue
        train = [m for m in MS if "2006-01-01" <= m["date"] < ts]
        mod = nm.NatPoisson(xi, R, wf).fit(train, t)
        test = [m for m in test if m["home"] in mod.idx and m["away"] in mod.idx]
        lm = np.array([mod.rates(m["home"], m["away"], m["neutral"]) for m in test])
        P = poisson.pmf(G[None, :], lm[:, :1]); Q = poisson.pmf(G[None, :], lm[:, 1:])
        M = P[:, :, None] * Q[:, None, :]; M /= M.sum((1, 2), keepdims=True)
        i, j = np.indices((11, 11))
        p = np.stack([M[:, i > j].sum(1), M[:, i == j].sum(1), M[:, i < j].sum(1)], 1)
        for m, pp in zip(test, p):
            r = 0 if m["hg"] > m["ag"] else 1 if m["hg"] == m["ag"] else 2
            res.append((m["date"], m["home"] in nm.UEFA and m["away"] in nm.UEFA, -math.log(max(pp[r], 1e-12))))
    return res
xis = [float(x) for x in sys.argv[1].split(",")]; Rs = [float(x) for x in sys.argv[2].split(",")]; wfs = [float(x) for x in sys.argv[3].split(",")]
out = {}
for cfg in itertools.product(xis, Rs, wfs):
    rr = run_fast(cfg, (2022, 11), (2026, 10))
    f = lambda sel: float(np.mean([x[2] for x in rr if sel(x)]))
    out[str(cfg)] = {"tune_all": f(lambda x: x[0] < "2024-11-01"), "tune_uefa": f(lambda x: x[0] < "2024-11-01" and x[1]),
                     "test_all": f(lambda x: x[0] >= "2024-11-01"), "test_uefa": f(lambda x: x[0] >= "2024-11-01" and x[1])}
    print(cfg, {k: round(v, 4) for k, v in out[str(cfg)].items()}, flush=True)
json.dump(out, open(sys.argv[4], "w"), indent=1)
