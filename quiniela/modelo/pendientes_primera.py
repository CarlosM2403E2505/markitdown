"""Pruebas pendientes en Primera (J23): (a) empates x1,20 en partidos igualados; (b) EURO_F (equipo con
partido UEFA en los últimos 120 días). Walk-forward mensual 2022-26; elegir con 2022-24, validar con
2025-26. Solo se aplica lo que mejore fuera de muestra. Uso: python3 modelo/pendientes_primera.py"""
import importlib.util, json, math, os, sys
from bisect import bisect_left
from collections import defaultdict
from datetime import date, timedelta
import numpy as np
from scipy.stats import poisson
R = os.path.dirname(os.path.abspath(__file__))
s = importlib.util.spec_from_file_location("em", os.path.join(R, "euro_model.py")); em = importlib.util.module_from_spec(s); s.loader.exec_module(em)
MS = json.load(open(os.path.join(R, "..", "datos", "euro_j23.json")))["matches"]
G = np.arange(11)
uefa = defaultdict(list)
for m in MS:
    if m["competition"].startswith("uefa."):
        uefa[m["home"]].append(m["date"]); uefa[m["away"]].append(m["date"])
for k in uefa: uefa[k].sort()
def europa(t, d):
    xs = uefa.get(t, []); lo = (date.fromisoformat(d) - timedelta(days=120)).isoformat()
    i = bisect_left(xs, lo); return i < len(xs) and xs[i] < d

def probs(l, u, k_draw=1.08, k_ig=1.0, T=1.15):
    l, u = l * math.exp(0.07), u * math.exp(-0.07)
    M = np.outer(poisson.pmf(G, l), poisson.pmf(G, u)); M[np.diag_indices_from(M)] *= k_draw; M /= M.sum()
    i, j = np.indices(M.shape); p = np.array([M[i > j].sum(), M[i == j].sum(), M[i < j].sum()])
    if k_ig != 1.0 and abs(p[0] - p[2]) < 0.15:
        p[1] *= k_ig; p /= p.sum()
    p = p ** T; return p / p.sum()

filas = []
y, m = 2022, 1; meses = []
while (y, m) <= (2026, 12): meses.append(f"{y}-{m:02d}-01"); y, m = (y+1, 1) if m == 12 else (y, m+1)
for a, b in zip(meses, meses[1:]):
    te = [x for x in MS if a <= x["date"] < b and x["competition"].startswith("es.1")]
    if not te: continue
    mod = em.EuroPoisson(xi=0.0015, ridge=10, scale=1.05, blend=0.2, hier=True).fit([x for x in MS if x["date"] < a], ref_date=date.fromisoformat(a))
    for x in te:
        if x["home"] in mod.idx and x["away"] in mod.idx:
            l, u = mod.rates(x["home"], x["away"])
            r = 0 if x["hg"] > x["ag"] else (1 if x["hg"] == x["ag"] else 2)
            filas.append((l, u, r, x["date"], europa(x["home"], x["date"]), europa(x["away"], x["date"])))
    print(a, len(filas), file=sys.stderr)

def ll(sub, fn): return float(np.mean([-math.log(max(fn(f)[f[2]], 1e-12)) for f in sub]))
val = [f for f in filas if f[3] < "2025-07-01"]; tes = [f for f in filas if f[3] >= "2025-07-01"]
print(f"Primera: validación n={len(val)} · prueba n={len(tes)}")
base = lambda f: probs(f[0], f[1])
print(f"  actual:                     validación {ll(val, base):.4f} · prueba {ll(tes, base):.4f}")
for k in (1.10, 1.20):
    fn = lambda f, k=k: probs(f[0], f[1], k_ig=k)
    print(f"  (a) empates x{k:.2f} igualados: validación {ll(val, fn):.4f} · prueba {ll(tes, fn):.4f}")
for fct in (1.04, 1.08, 1.12):
    def fn(f, fct=fct):
        l, u = f[0], f[1]
        if f[4] and not f[5]: l *= fct
        if f[5] and not f[4]: u *= fct
        return probs(l, u)
    print(f"  (b) EURO_F {fct:.2f}:            validación {ll(val, fn):.4f} · prueba {ll(tes, fn):.4f}")
print(f"  partidos con un solo equipo europeo: {sum(1 for f in filas if f[4] != f[5])} de {len(filas)}")
