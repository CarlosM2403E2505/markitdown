"""¿Qué regla de fatiga predice mejor (log-loss) los partidos de liga tras Europa? Fuera de muestra."""
import json, math, sys
import numpy as np
from scipy.stats import poisson
f = [x for x in json.load(open(sys.argv[1])) if x["dias"] is not None and 2 <= x["dias"] <= 6]
G = np.arange(11)
def p_res(own, opp):
    M = np.outer(poisson.pmf(G, own), poisson.pmf(G, opp)); M[np.diag_indices_from(M)] *= 1.08; M /= M.sum()
    i, j = np.indices(M.shape); p = [M[i > j].sum(), M[i == j].sum(), M[i < j].sum()]; q = [v ** 1.05 for v in p]; z = sum(q); return [v / z for v in q]
reglas = {
    "Ninguna": lambda x: (1, 1),
    "Actual (jueves −4 % / +2,5 %; mar–mié nada)": lambda x: (0.96, 1.025) if x["dia_sem"] == 3 else (1, 1),
    "Actual + mar–mié −3 % ataque": lambda x: (0.96, 1.025) if x["dia_sem"] == 3 else (0.97, 1.0),
    "Jueves −4 % / +4 %; mar–mié −3 %": lambda x: (0.96, 1.04) if x["dia_sem"] == 3 else (0.97, 1.0),
    "Jueves doble (−8 % / +5 %)": lambda x: (0.92, 1.05) if x["dia_sem"] == 3 else (1, 1),
}
for liga, sel in (("todas las ligas", lambda x: True), ("Primera", lambda x: x["liga"] == "es.1")):
    sub = [x for x in f if sel(x)]
    print(f"\n{liga}: {len(sub)} partidos tras Europa")
    base = None
    for n, r in reglas.items():
        ll = 0
        for x in sub:
            a, d = r(x); pw, pd, pl = p_res(x["xf"] * a, x["xc"] * d)
            res = pw if x["pts"] == 3 else (pd if x["pts"] == 1 else pl); ll -= math.log(res)
        ll /= len(sub); base = base or ll
        print(f"  {n:<44} log-loss {ll:.5f}  ({1000*(ll-base):+.2f} milésimas frente a ninguna)")
