"""X en favoritos templados (revisión tras la J23, 22/11/2026).
Hallazgo de revision_j23.py: en Primera, con el favorito de la mesa entre 45 y 55 %, la mesa daba X 25,8 %
y salió 35,2 % (293 partidos fuera de muestra); el favorito daba 49,5 % y ganó 44 %.
Prueba: multiplicar la X por k cuando max(p) está en [lo, hi) y renormalizar. Se elige (lo, hi, k) SOLO con
2024-25 y se valida con 2025-26 y 2026-27. Se hace igual para Segunda (empates x1,00, T=1,05, sin campo extra).
Uso: python3 modelo/x_templados.py  → datos/x_templados.json"""
import json, math, os, pickle, sys
from collections import defaultdict
from datetime import date
import numpy as np
from scipy.stats import poisson
R = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(R, "pendientes_primera.py"), encoding="utf-8").read().split("filas = []")[0]
ns = {"__file__": os.path.join(R, "pendientes_primera.py")}; exec(src, ns)
em, MS, europa = ns["em"], ns["MS"], ns["europa"]
G = np.arange(11)
CACHE = os.path.join(os.environ.get("TMPDIR", "/tmp"), "x_templados_filas.pkl")
if os.path.exists(CACHE):
    filas = pickle.load(open(CACHE, "rb"))
else:
    filas = []
    y, m = 2022, 1; meses = []
    while (y, m) <= (2026, 12): meses.append(f"{y}-{m:02d}-01"); y, m = (y+1, 1) if m == 12 else (y, m+1)
    for a, b in zip(meses, meses[1:]):
        te = [x for x in MS if a <= x["date"] < b and x["competition"][:4] in ("es.1", "es.2")]
        if not te: continue
        mod = em.EuroPoisson(xi=0.0015, ridge=10, scale=1.05, blend=0.2, hier=True).fit([x for x in MS if x["date"] < a], ref_date=date.fromisoformat(a))
        for x in te:
            if x["home"] in mod.idx and x["away"] in mod.idx:
                l, u = mod.rates(x["home"], x["away"])
                r = 0 if x["hg"] > x["ag"] else (1 if x["hg"] == x["ag"] else 2)
                filas.append((x["competition"][:4], l, u, r, x["date"], europa(x["home"], x["date"]), europa(x["away"], x["date"])))
        print(a, len(filas), file=sys.stderr)
    pickle.dump(filas, open(CACHE, "wb"))

def base(f):
    comp, l, u = f[0], f[1], f[2]
    if comp == "es.1":
        l, u, kd, T = l * math.exp(0.07), u * math.exp(-0.07), 1.08, 1.15
        if f[5] and not f[6]: l *= 1.12
        if f[6] and not f[5]: u *= 1.12
    else:
        kd, T = 1.00, 1.05
    M = np.outer(poisson.pmf(G, l), poisson.pmf(G, u)); M[np.diag_indices_from(M)] *= kd; M /= M.sum()
    i, j = np.indices(M.shape); p = np.array([M[i > j].sum(), M[i == j].sum(), M[i < j].sum()]) ** T
    return p / p.sum()
def con_x(p, lo, hi, k):
    if lo <= p.max() < hi: p = p.copy(); p[1] *= k; p /= p.sum()
    return p
def temporada(d): y, m = int(d[:4]), int(d[5:7]); return f"{y}-{(y+1)%100:02d}" if m >= 7 else f"{y-1}-{y%100:02d}"
P = [(f, base(f)) for f in filas]
ll = lambda sub, fn: float(np.mean([-math.log(max(fn(p)[f[3]], 1e-12)) for f, p in sub]))
out = {}
for comp in ("es.1", "es.2"):
    sel = [(f, p) for f, p in P if f[0] == comp and temporada(f[4]) == "2024-25"]
    val = [(f, p) for f, p in P if f[0] == comp and temporada(f[4]) > "2024-25"]
    rej = []
    for lo in (0.40, 0.45):
        for hi in (0.55, 0.60):
            for k in (1.0, 1.1, 1.2, 1.3, 1.4, 1.5):
                rej.append((ll(sel, lambda p: con_x(p, lo, hi, k)), lo, hi, k))
    best = min(rej)
    _, lo, hi, k = best
    cal = defaultdict(list)
    for f, p in val:
        if lo <= p.max() < hi: cal["n"].append(1); cal["daba_X"].append(p[1]); cal["daba_X_nuevo"].append(con_x(p, lo, hi, k)[1]); cal["salio_X"].append(f[3] == 1)
    out[comp] = {"n_seleccion": len(sel), "n_validacion": len(val), "elegido": {"lo": lo, "hi": hi, "k": k},
                 "seleccion": {"vigente": round(ll(sel, lambda p: p), 4), "nuevo": round(best[0], 4)},
                 "validacion": {"vigente": round(ll(val, lambda p: p), 4), "nuevo": round(ll(val, lambda p: con_x(p, lo, hi, k)), 4)},
                 "validacion_por_temporada": {t: {"vigente": round(ll([x for x in val if temporada(x[0][4]) == t], lambda p: p), 4),
                                                   "nuevo": round(ll([x for x in val if temporada(x[0][4]) == t], lambda p: con_x(p, lo, hi, k)), 4)}
                                              for t in sorted({temporada(f[4]) for f, _ in val})},
                 "tramo_validacion": {"n": len(cal["n"]), "daba_X": round(float(np.mean(cal["daba_X"])), 3) if cal["n"] else None,
                                      "nuevo_X": round(float(np.mean(cal["daba_X_nuevo"])), 3) if cal["n"] else None,
                                      "salio_X": round(float(np.mean(cal["salio_X"])), 3) if cal["n"] else None}}
json.dump(out, open(os.path.join(R, "..", "datos", "x_templados.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps(out, ensure_ascii=False, indent=1))
