"""Auditoría de empates (J21): ¿el modelo da a la X la probabilidad que tiene en la realidad?

Validación avanzando en el tiempo: se reajusta el modelo cada mes con los partidos anteriores
y se predice el mes siguiente (Primera y Segunda, desde agosto de 2024). Mide:
  1. Calibración de P(X): por tramos, probabilidad media dada frente a frecuencia real.
  2. Alternativas para la X: factor de empate, Dixon-Coles (rho) y ambos; log-loss fuera de muestra.
Uso: python3 modelo/auditoria_empates.py   (desde la carpeta quiniela)
"""
import importlib.util, json, math, os, sys
from datetime import date
import numpy as np
from scipy.stats import poisson
R = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("em", os.path.join(R, "euro_model.py")); em = importlib.util.module_from_spec(spec); spec.loader.exec_module(em)
ms = json.load(open(os.path.join(R, "..", "datos", "euro_j21.json")))["matches"]
G = np.arange(11)
meses = []
y, m = 2024, 8
while (y, m) <= (2026, 11):
    meses.append(f"{y}-{m:02d}-01"); y, m = (y + 1, 1) if m == 12 else (y, m + 1)
filas = []
for a, b in zip(meses, meses[1:]):
    te = [x for x in ms if a <= x["date"] < b and x["competition"].split(":")[0] in ("es.1", "es.2")]
    if not te: continue
    mod = em.EuroPoisson(xi=0.0015, ridge=10, scale=1.05, blend=0.2, hier=True).fit([x for x in ms if x["date"] < a], ref_date=date.fromisoformat(a))
    for x in te:
        if x["home"] in mod.idx and x["away"] in mod.idx:
            l, u = mod.rates(x["home"], x["away"]); c = x["competition"].split(":")[0]
            if c == "es.1": l, u = l * math.exp(0.07), u * math.exp(-0.07)
            filas.append((l, u, 0 if x["hg"] > x["ag"] else (1 if x["hg"] == x["ag"] else 2), c, x["date"]))
    print(a, len(filas), file=sys.stderr)
json.dump(filas, open(os.path.join(R, "..", "datos", "auditoria_empates_lambdas.json"), "w"))

def probs(l, u, k=1.0, rho=0.0, T=1.05):
    M = np.outer(poisson.pmf(G, l), poisson.pmf(G, u))
    if rho:
        M[0, 0] *= 1 - l * u * rho; M[0, 1] *= 1 + l * rho; M[1, 0] *= 1 + u * rho; M[1, 1] *= 1 - rho
    M[np.diag_indices_from(M)] *= k; M /= M.sum()
    i, j = np.indices(M.shape); p = np.array([M[i > j].sum(), M[i == j].sum(), M[i < j].sum()])
    p = p ** T; return p / p.sum()
KACT = {"es.1": 1.08, "es.2": 1.00}
def evaluar(sub, k=None, rho=0.0):
    s = 0; px = []
    for l, u, r, c, _ in sub:
        p = probs(l, u, KACT[c] if k is None else k, rho); s -= math.log(p[r]); px.append(p[1])
    return s / len(sub), 100 * np.mean(px)
for comp in ("es.1", "es.2", "todas"):
    sub = [f for f in filas if comp == "todas" or f[3] == comp]
    real = 100 * np.mean([f[2] == 1 for f in sub])
    print(f"\n=== {comp}: {len(sub)} partidos fuera de muestra · X real {real:.1f} %")
    ll0, x0 = evaluar(sub)
    print(f"Modelo actual: log-loss {ll0:.4f} · X dada {x0:.1f} %")
    # calibración por tramos
    ps = np.array([probs(l, u, KACT[c])[1] for l, u, r, c, _ in sub]); rs = np.array([f[2] == 1 for f in sub])
    for lo, hi in ((0, .2), (.2, .24), (.24, .27), (.27, .30), (.30, .34), (.34, 1)):
        msk = (ps >= lo) & (ps < hi)
        if msk.sum(): print(f"  P(X) {lo:.2f}-{hi:.2f}: n={msk.sum():4d} · dada {100*ps[msk].mean():5.1f} % · real {100*rs[msk].mean():5.1f} %")
    # partidos donde X fue el signo más probable
    print(f"  Partidos con X como signo más probable: {sum(1 for l,u,r,c,_ in sub if np.argmax(probs(l,u,KACT[c]))==1)}")
# alternativas: elegir con 2024-25, probar con 2025-26 y 2026-27
val = [f for f in filas if f[4] < "2025-07-01"]; tes = [f for f in filas if f[4] >= "2025-07-01"]
print("\n=== Alternativas (elegida con 2024-25, probada con 2025-26 y 2026-27)")
res = []
for rho in (0.0, -0.05, -0.1, -0.15):
    for kk in (None, 1.0, 1.05, 1.10, 1.15):
        a = evaluar(val, kk, rho); b = evaluar(tes, kk, rho); res.append((a[0], rho, kk, b))
        print(f"  rho {rho:5.2f} · factor {'actual' if kk is None else kk}: validación {a[0]:.4f} · prueba {b[0]:.4f} (X dada {b[1]:.1f} %)")
best = min(res); print(f"Mejor en validación: rho {best[1]}, factor {best[2] or 'actual'} → prueba {best[3][0]:.4f}")
