"""Modelo de la Liga F (desde la J21): Poisson con ridge, partido a partido, con la temporada
anterior completa (peso 1) y la actual, sin los partidos del Barça, campo fijo 1,10.
Backtest del 11/11/2026 (jornadas 4 a 10 de 2026/27, 48 partidos, fuera de muestra):
log-loss 0,976 frente a 1,061 del método anterior (actual + totales de la temporada pasada)."""
import json, math, os
import numpy as np
from scipy.optimize import minimize

HOME = 2 * math.log(1.10)
RUTA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "datos", "ligaf.json")


def partidos(ruta=RUTA):
    with open(ruta, encoding="utf-8") as f:
        return [(p["temporada"], p["local"], p["visitante"], p["goles_local"], p["goles_visitante"])
                for p in json.load(f)["partidos"]]


def ajustar(peso_anterior=1.0, ridge=1.5, ruta=RUTA, temporada_actual="2026-27"):
    ms = [(h, a, x, y, 1.0 if t == temporada_actual else peso_anterior)
          for t, h, a, x, y in partidos(ruta) if "Barcelona" not in (h, a)]
    teams = sorted({t for m in ms for t in m[:2]}); ix = {t: i for i, t in enumerate(teams)}; n = len(teams)
    H = np.array([ix[m[0]] for m in ms]); A = np.array([ix[m[1]] for m in ms])
    hg = np.array([m[2] for m in ms]); ag = np.array([m[3] for m in ms]); w = np.array([m[4] for m in ms])

    def nll(p):
        mu0, att, dfn = p[0], p[1:1 + n], p[1 + n:]
        lh = np.exp(mu0 + HOME + att[H] + dfn[A]); la = np.exp(mu0 + att[A] + dfn[H])
        return -(w * (hg * np.log(lh) - lh + ag * np.log(la) - la)).sum() + ridge * ((att ** 2).sum() + (dfn ** 2).sum())

    r = minimize(nll, np.zeros(1 + 2 * n), method="L-BFGS-B")
    p = r.x
    return dict(mu0=p[0], home=HOME, att=dict(zip(teams, p[1:1 + n])), dfn=dict(zip(teams, p[1 + n:])), ok=r.success,
                n=len(ms))
