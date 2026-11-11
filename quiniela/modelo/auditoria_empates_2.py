"""Auditoría de empates, parte 2 (J21).
A) Primera y Segunda: recalibración de P(X) según lo igualado del partido.
   logit(X') = a + b·logit(X), con a y b elegidos en 2024-25 y probados en 2025-26 y 2026-27.
B) Liga F: factor de empate (hoy 0,85) con validación que avanza en el tiempo."""
import json, math, os
import numpy as np
from scipy.stats import poisson
from scipy.optimize import minimize
import importlib.util
R = os.path.dirname(os.path.abspath(__file__)); G = np.arange(11)
def base(l, u, k):
    M = np.outer(poisson.pmf(G, l), poisson.pmf(G, u)); M[np.diag_indices_from(M)] *= k; M /= M.sum()
    i, j = np.indices(M.shape); return np.array([M[i > j].sum(), M[i == j].sum(), M[i < j].sum()])
def afinar(p, T=1.05):
    p = p ** T; return p / p.sum()
def recal(p, a, b):
    x = p[1]; lx = math.log(x / (1 - x)); xn = 1 / (1 + math.exp(-(a + b * lx)))
    r = (1 - xn) / (p[0] + p[2]); return np.array([p[0] * r, xn, p[2] * r])
filas = json.load(open(os.path.join(R, "..", "datos", "auditoria_empates_lambdas.json")))
K = {"es.1": 1.08, "es.2": 1.00}
P = [(afinar(base(l, u, K[c])), r, c, d) for l, u, r, c, d in filas]
val = [x for x in P if x[3] < "2025-07-01"]; tes = [x for x in P if x[3] >= "2025-07-01"]
def ll(sub, a=0.0, b=1.0): return -np.mean([math.log(recal(p, a, b)[r]) for p, r, c, d in sub])
f = lambda v: ll(val, v[0], v[1]); opt = minimize(f, [0.0, 1.0], method="Nelder-Mead").x
print("A) Primera y Segunda")
print(f"  a={opt[0]:.3f} b={opt[1]:.3f} (b>1: más X en partidos igualados y menos en los desiguales)")
print(f"  validación: actual {ll(val):.4f} → recalibrado {f(opt):.4f}")
print(f"  prueba:     actual {ll(tes):.4f} → recalibrado {ll(tes, *opt):.4f}  (n={len(tes)})")
for comp in ("es.1", "es.2"):
    s = [x for x in tes if x[2] == comp]; print(f"  {comp} prueba: {ll(s):.4f} → {ll(s, *opt):.4f}")
# calibración del recalibrado en prueba
ps = np.array([recal(p, *opt)[1] for p, r, c, d in tes]); rs = np.array([r == 1 for p, r, c, d in tes])
p0 = np.array([p[1] for p, r, c, d in tes])
for lo, hi in ((0, .2), (.2, .24), (.24, .27), (.27, .30), (.30, 1)):
    m0 = (p0 >= lo) & (p0 < hi)
    if m0.sum(): print(f"  tramo actual {lo:.2f}-{hi:.2f}: n={m0.sum():4d} · actual {100*p0[m0].mean():5.1f} % · recalibrado {100*ps[m0].mean():5.1f} % · real {100*rs[m0].mean():5.1f} %")
print(f"  Partidos de prueba con X como signo más probable tras recalibrar: {sum(np.argmax(recal(p,*opt))==1 for p,r,c,d in tes)} de {len(tes)}")
json.dump({"a": opt[0], "b": opt[1]}, open(os.path.join(R, "..", "datos", "recalibracion_x.json"), "w"))

print("\nB) Liga F (factor de empate)")
spec = importlib.util.spec_from_file_location("lfm", os.path.join(R, "ligaf_modelo.py")); lfm = importlib.util.module_from_spec(spec); spec.loader.exec_module(lfm)
todos = json.load(open(os.path.join(R, "..", "datos", "ligaf.json")))["partidos"]
act = [p for p in todos if p["temporada"] == "2026-27"]; ant = [p for p in todos if p["temporada"] == "2025-26"]
import tempfile
res = {k: [] for k in (0.85, 0.9, 1.0, 1.1, 1.2)}; xs = []
for corte in range(16, len(act), 8):
    tmp = os.path.join(tempfile.mkdtemp(), "lf.json"); json.dump({"partidos": ant + act[:corte]}, open(tmp, "w"))
    lf = lfm.ajustar(ruta=tmp)
    for p in act[corte:corte + 8]:
        h, a = p["local"], p["visitante"]
        if "Barcelona" in (h, a) or h not in lf["att"] or a not in lf["att"]: continue
        l = math.exp(lf["mu0"] + lf["home"] + lf["att"][h] + lf["dfn"][a]); u = math.exp(lf["mu0"] + lf["att"][a] + lf["dfn"][h])
        r = 0 if p["goles_local"] > p["goles_visitante"] else (1 if p["goles_local"] == p["goles_visitante"] else 2); xs.append(r == 1)
        for k in res: res[k].append((afinar(base(l, u, k)), r))
print(f"  {len(xs)} partidos fuera de muestra (sin el Barça) · X real {100*np.mean(xs):.1f} %")
for k, v in res.items():
    print(f"  factor {k:.2f}: log-loss {-np.mean([math.log(p[r]) for p, r in v]):.4f} · X dada {100*np.mean([p[1] for p, r in v]):.1f} %")
sin = [p for p in ant if "Barcelona" not in (p["local"], p["visitante"])]
print(f"  Empates en 2025-26 sin el Barça: {100*np.mean([p['goles_local']==p['goles_visitante'] for p in sin]):.1f} % de {len(sin)}")
