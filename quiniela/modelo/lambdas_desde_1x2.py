#!/usr/bin/env python3
"""Calcula las lambdas (goles esperados local y visitante) que reproducen un 1X2 dado
con el método de la mesa: Poisson independiente, factor de empates en la diagonal,
renormalizado, G = 0..10.

Uso: python3 lambdas_desde_1x2.py ../datos/j19_precio_final.json [factor_empates]
"""
import json, sys
import numpy as np
from scipy.stats import poisson
from scipy.optimize import least_squares

G = np.arange(11)

def p1x2(l, m, k=1.0):
    M = np.outer(poisson.pmf(G, l), poisson.pmf(G, m))
    M[np.diag_indices_from(M)] *= k
    M /= M.sum()
    i, j = np.indices(M.shape)
    return np.array([M[i > j].sum(), M[i == j].sum(), M[i < j].sum()])

def lambdas(p_obj, k=1.0, inicio=(1.4, 1.2)):
    p_obj = np.asarray(p_obj, dtype=float)
    r = least_squares(lambda x: (p1x2(x[0], x[1], k) - p_obj)[[0, 2]], inicio,
                      bounds=([0.05, 0.05], [6, 6]))
    return r.x

if __name__ == "__main__":
    k = float(sys.argv[2]) if len(sys.argv) > 2 else 1.0
    for r in json.load(open(sys.argv[1], encoding="utf-8"))["rows"]:
        l, m = lambdas(r["p"], k, r.get("xg", (1.4, 1.2)))
        print(f"P{r['n']:<2} {r['partido']:<30} λ {l:.3f} – {m:.3f}   1X2 " +
              " · ".join(f"{x:.4f}" for x in p1x2(l, m, k)))
