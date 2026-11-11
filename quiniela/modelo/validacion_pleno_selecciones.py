"""Pleno con selecciones: ¿mezclar el Poisson con la distribución histórica de marcadores mejora? (J21)
16 categorías del Pleno (0,1,2,M × 0,1,2,M). Distribución empírica: partidos oficiales UEFA 2012-2024-10 (90').
Peso elegido con la validación (2022-01 a 2024-10) y comprobado en la prueba (2024-11 a 2026-10)."""
import importlib.util, json, math, os
import numpy as np
R = os.path.dirname(os.path.abspath(__file__))
s = importlib.util.spec_from_file_location("sm", os.path.join(R, "selecciones_modelo.py")); sm = importlib.util.module_from_spec(s); s.loader.exec_module(sm)
ms = sm.cargar("2012-01-01"); idx = {(m["date"], m["home"], m["away"]): m for m in ms}
filas = json.load(open(os.path.join(R, "..", "datos", "selecciones", "validacion_filas.json")))
cat = lambda g: min(g, 3)
emp = np.zeros((4, 4)); src = [m for m in ms if m["date"] < "2024-11-01" and m["home"] in sm.UEFA and m["away"] in sm.UEFA and m["t"] in sm.COMPET_UEFA]
for m in src: emp[cat(m["hg90"]), cat(m["ag90"])] += 1
emp /= emp.sum()
def cats(lam, mu):
    M = sm.matriz(lam, mu); C = np.zeros((4, 4))
    for i in range(11):
        for j in range(11): C[cat(i), cat(j)] += M[i, j]
    return C
def ll(sub, w):
    out = []
    for x in sub:
        m = idx[(x["date"], x["home"], x["away"])]; C = (1 - w) * cats(x["lam"], x["mu"]) + w * emp
        out.append(-math.log(C[cat(m["hg90"]), cat(m["ag90"])]))
    return np.mean(out)
val = [x for x in filas if x["date"] < "2024-11-01"]; tes = [x for x in filas if x["date"] >= "2024-11-01"]
res = {f"{w:.1f}": (round(ll(val, w), 4), round(ll(tes, w), 4)) for w in (0.0, 0.1, 0.2, 0.3)}
best = min(res, key=lambda k: res[k][0])
print("peso: (log-loss validación, log-loss prueba)", res, "→ elegido en validación:", best)
json.dump({"pesos": res, "elegido": best, "n_val": len(val), "n_test": len(tes)}, open(os.path.join(R, "..", "datos", "selecciones", "validacion_pleno.json"), "w"), indent=1)
