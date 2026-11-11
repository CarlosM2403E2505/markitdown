"""Validación fuera de muestra de los modelos de selecciones (J21, rescate de «quiniela-mesa»).

Prueba: partidos oficiales entre selecciones UEFA (torneos de COMPET_UEFA), del 1/11/2024 al 6/10/2026,
resultado a 90'. Validación (para elegir el factor de empates): lo mismo de 2022-01 a 2024-10.
- Elo: partido a partido (no ve el futuro). Método v1.2: total 2,4 goles.
- NatPoisson: se reajusta cada mes con los partidos anteriores (desde 2006).
Uso: python3 modelo/validacion_selecciones.py
"""
import importlib.util, json, math, os, sys
from datetime import date
import numpy as np
R = os.path.dirname(os.path.abspath(__file__))
s = importlib.util.spec_from_file_location("sm", os.path.join(R, "selecciones_modelo.py")); sm = importlib.util.module_from_spec(s); s.loader.exec_module(sm)
ms = sm.cargar()
antes, _ = sm.elo_historico(ms)
objetivo = [i for i, m in enumerate(ms) if m["date"] >= "2022-01-01" and m["home"] in sm.UEFA and m["away"] in sm.UEFA and m["t"] in sm.COMPET_UEFA]
meses = sorted({ms[i]["date"][:7] for i in objetivo})
CACHE = os.path.join(R, "..", "datos", "selecciones", "validacion_filas.json")
filas = json.load(open(CACHE)) if os.path.exists(CACHE) and "--rehacer" not in sys.argv else []
for mes in ([] if filas else meses):
    corte = mes + "-01"
    tr = [m for m in ms if "2006-01-01" <= m["date"] < corte]
    mod = sm.NatPoisson().fit(tr, date.fromisoformat(corte))
    for i in objetivo:
        m = ms[i]
        if m["date"][:7] != mes or m["home"] not in mod.idx or m["away"] not in mod.idx:
            continue
        lam, mu = mod.rates(m["home"], m["away"], m["neutral"])
        a, b = antes[i]; dr = a - b + (0 if m["neutral"] else 100)
        r = 0 if m["hg90"] > m["ag90"] else (1 if m["hg90"] == m["ag90"] else 2)
        filas.append({"date": m["date"], "home": m["home"], "away": m["away"], "r": r, "lam": lam, "mu": mu, "dr": dr})
    print(mes, len(filas), file=sys.stderr)
json.dump(filas, open(CACHE, "w"))

def ll(sub, f):
    return -np.mean([math.log(f(x)[x["r"]]) for x in sub])
val = [x for x in filas if x["date"] < "2024-11-01"]; tes = [x for x in filas if x["date"] >= "2024-11-01"]
ks = [0.9, 1.0, 1.1, 1.17, 1.25]
res = {}
for nombre, f in (("Elo + Poisson 2,4 (método v1.2)", lambda k: (lambda x: sm.uno_x_dos_elo(x["dr"], 2.4, k))),
                  ("Poisson de selecciones (quiniela-mesa)", lambda k: (lambda x: sm.uno_x_dos(sm.matriz(x["lam"], x["mu"], k))))):
    kv = min(ks, key=lambda k: ll(val, f(k)))
    res[nombre] = {"k_elegido_en_validacion": kv, "LL_validacion": round(ll(val, f(kv)), 4),
                   "LL_prueba_k1": round(ll(tes, f(1.0)), 4), "LL_prueba_k_elegido": round(ll(tes, f(kv)), 4),
                   "X_prevista_prueba_%": round(100 * np.mean([f(1.0)(x)[1] for x in tes]), 1)}
base = np.bincount([x["r"] for x in val], minlength=3) / len(val)
res["Tasa base (frecuencias de validación)"] = {"LL_prueba": round(-np.mean([math.log(base[x["r"]]) for x in tes]), 4)}
res["_n"] = {"validacion": len(val), "prueba": len(tes), "X_real_prueba_%": round(100 * np.mean([x["r"] == 1 for x in tes]), 1)}
# partidos entre grandes (los dos con Elo ≥ 1850 antes del partido): como Bélgica–Italia y España–Inglaterra
gr = [x for x in tes if x["dr"] is not None]
print(json.dumps(res, ensure_ascii=False, indent=1))
json.dump(res, open(os.path.join(R, "..", "datos", "selecciones", "validacion_resumen.json"), "w"), ensure_ascii=False, indent=1)
