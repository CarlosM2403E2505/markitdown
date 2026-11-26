"""Modelo de la UEFA Women's Champions League (J22): Poisson ridge partido a partido.

Temporada actual (2026-27, fase liga) con peso 1 y la anterior (2025-26) con peso menor; ridge alto
porque hay pocos partidos por club; campo fijo. Datos: datos/champions_f.json (de Wikipedia).
CONFIANZA MEDIA: ~4-10 partidos por club. Uso como módulo: ajustar() -> dict(mu0, home, att, dfn).
"""
import json, math, os
import numpy as np
from scipy.optimize import minimize

RUTA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "datos", "champions_f.json")
HOME = 2 * math.log(1.20)  # ventaja de campo típica del fútbol femenino europeo


def ajustar(peso_anterior=0.5, ridge=2.5, ruta=RUTA, temporada_actual="2026-27"):
    todos = json.load(open(ruta, encoding="utf-8"))["partidos"]
    ms = [(p["local"], p["visitante"], p["goles_local"], p["goles_visitante"],
           1.0 if p["temporada"] == temporada_actual else peso_anterior) for p in todos]
    teams = sorted({t for m in ms for t in m[:2]}); ix = {t: i for i, t in enumerate(teams)}; n = len(teams)
    H = np.array([ix[m[0]] for m in ms]); A = np.array([ix[m[1]] for m in ms])
    hg = np.array([m[2] for m in ms], float); ag = np.array([m[3] for m in ms], float); w = np.array([m[4] for m in ms])

    def nll(p):
        mu0, att, dfn = p[0], p[1:1 + n], p[1 + n:]
        lh = np.exp(mu0 + HOME + att[H] + dfn[A]); la = np.exp(mu0 + att[A] + dfn[H])
        return -(w * (hg * np.log(lh) - lh + ag * np.log(la) - la)).sum() + ridge * ((att ** 2).sum() + (dfn ** 2).sum())

    r = minimize(nll, np.zeros(1 + 2 * n), method="L-BFGS-B")
    p = r.x
    return dict(mu0=p[0], home=HOME, att=dict(zip(teams, p[1:1 + n])), dfn=dict(zip(teams, p[1 + n:])),
               ok=r.success, n=len(ms), teams=teams)


def rates(lf, h, a):
    return (math.exp(lf["mu0"] + lf["home"] + lf["att"][h] + lf["dfn"][a]),
            math.exp(lf["mu0"] + lf["att"][a] + lf["dfn"][h]))


if __name__ == "__main__":
    lf = ajustar()
    fuerza = {t: lf["att"][t] - lf["dfn"][t] for t in lf["teams"]}
    print("convergió", lf["ok"], "·", lf["n"], "partidos ·", len(lf["teams"]), "equipos")
    print("fuerza (ataque-defensa), de mejor a peor:")
    for t in sorted(fuerza, key=lambda x: -fuerza[x]):
        print(f"  {t:22s} {fuerza[t]:+.2f}")
