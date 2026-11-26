#!/usr/bin/env python3
"""H2 (autopsia J24): ¿infla la mesa los goles del local fuerte? Calibración fuera de muestra de P(local >= 3)
y del marcador más probable, en Primera y Segunda. Se ajusta el modelo con los datos anteriores a cada corte
y se predicen los partidos de liga de los 120 días siguientes. Uso: python3 modelo/h2_goles_local.py"""
import importlib.util, json, math, os
from datetime import date, timedelta
import numpy as np
from scipy.stats import poisson
H = os.path.dirname(os.path.abspath(__file__)); Q = os.path.dirname(H)
s = importlib.util.spec_from_file_location("em", os.path.join(H, "euro_model.py")); em = importlib.util.module_from_spec(s); s.loader.exec_module(em)
ms = json.load(open(os.path.join(Q, "datos", "euro_j24.json")))["matches"]
CORTES = [date(2025, 1, 1), date(2025, 8, 10), date(2025, 12, 1), date(2026, 8, 10)]
rows = []
for c in CORTES:
    tr = [m for m in ms if m["date"] < c.isoformat()]
    mod = em.EuroPoisson(xi=0.0015, ridge=10, scale=1.05, blend=0.2, hier=True).fit(tr, ref_date=c)
    fin = (c + timedelta(days=120)).isoformat()
    for m in ms:
        comp = m["competition"].split(":")[0]
        if comp not in ("es.1", "es.2") or not (c.isoformat() <= m["date"] < fin): continue
        try: lam, mu = mod.rates(m["home"], m["away"])
        except Exception: continue
        if comp == "es.1": lam, mu = lam * math.exp(0.07), mu * math.exp(-0.07)
        G = np.arange(11); M = np.outer(poisson.pmf(G, lam), poisson.pmf(G, mu)); M /= M.sum()
        i, j = np.indices(M.shape)
        rows.append({"corte": c.isoformat(), "comp": comp, "p1": float(M[i > j].sum()), "p3": float(M[i >= 3].sum()), "real3": m["hg"] >= 3, "lam": lam, "hg": m["hg"]})
out = {"n": len(rows), "tramos": []}
for lo, hi in [(0, .45), (.45, .6), (.6, .75), (.75, 1.01)]:
    x = [r for r in rows if lo <= r["p1"] < hi]
    if x:
        t = {"p_local_gana": f"{int(100*lo)}-{int(100*min(hi,1))} %", "n": len(x), "P3_mesa": round(np.mean([r["p3"] for r in x]), 3),
             "P3_real": round(np.mean([r["real3"] for r in x]), 3), "goles_mesa": round(np.mean([r["lam"] for r in x]), 2), "goles_real": round(np.mean([r["hg"] for r in x]), 2)}
        out["tramos"].append(t); print(t)
json.dump(out, open(os.path.join(Q, "datos", "h2_goles_local.json"), "w"), ensure_ascii=False, indent=1)

# Prueba fuera de muestra: factor k sobre los goles del local, ajustado en los dos primeros cortes y probado en los dos últimos
from scipy.stats import poisson as P
def ll(x, k): return float(np.mean([P.logpmf(r["hg"], r["lam"] * k) for r in x]))
for nombre, filtro in [("todos", lambda r: True), ("local < 45 %", lambda r: r["p1"] < .45), ("local >= 75 %", lambda r: r["p1"] >= .75)]:
    a = [r for r in rows if r["corte"] < "2025-12" and filtro(r)]; b = [r for r in rows if r["corte"] >= "2025-12" and filtro(r)]
    ks = np.arange(0.80, 1.11, 0.01); k = float(ks[np.argmax([ll(a, k) for k in ks])])
    res = {"grupo": nombre, "n_ajuste": len(a), "n_prueba": len(b), "k": round(k, 2), "ll_prueba_sin": round(ll(b, 1.0), 5), "ll_prueba_con": round(ll(b, k), 5)}
    res["mejora"] = res["ll_prueba_con"] > res["ll_prueba_sin"]; out.setdefault("prueba", []).append(res); print(res)
json.dump(out, open(os.path.join(Q, "datos", "h2_goles_local.json"), "w"), ensure_ascii=False, indent=1)
