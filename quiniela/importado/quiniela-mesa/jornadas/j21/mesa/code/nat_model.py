"""Modelo Poisson de SELECCIONES (J21). Cero cuotas.

  log(goles A) = c + h*[A juega en casa y neutral=False] + ataque[A] + defensa[B]
  log(goles B) = c + h*[B juega en casa y neutral=False] + ataque[B] + defensa[A]

Peso de cada partido = exp(-xi * dias) * peso_torneo (amistoso = wf, oficial = 1).
Ridge R sobre ataque y defensa (hacia 0). Gradiente analitico, L-BFGS.
Marcadores a 90': los goles de la prorroga (minuto >= 91 en goalscorers.csv) se restan.

Uso como modulo: load(results.csv, goalscorers.csv) -> lista de partidos; NatPoisson(...).fit(ms, ref)
"""
import csv, math
from datetime import date
import numpy as np
from scipy.optimize import minimize

UEFA = set("""Albania|Andorra|Armenia|Austria|Azerbaijan|Belarus|Belgium|Bosnia and Herzegovina|Bulgaria|Croatia|Cyprus|
Czech Republic|Denmark|England|Estonia|Faroe Islands|Finland|France|Georgia|Germany|Gibraltar|Greece|Hungary|Iceland|Israel|
Italy|Kazakhstan|Kosovo|Latvia|Liechtenstein|Lithuania|Luxembourg|Malta|Moldova|Montenegro|Netherlands|North Macedonia|
Northern Ireland|Norway|Poland|Portugal|Republic of Ireland|Romania|Russia|San Marino|Scotland|Serbia|Slovakia|Slovenia|
Spain|Sweden|Switzerland|Turkey|Ukraine|Wales""".replace("\n", "").split("|"))
COMPET_UEFA = {"UEFA Nations League", "UEFA Euro qualification", "FIFA World Cup qualification", "UEFA Euro", "FIFA World Cup"}


def load(results, goals, start="2006-01-01"):
    et = {}
    for g in csv.DictReader(open(goals, encoding="utf-8")):
        if g["date"] < start or g["minute"] in ("NA", ""):
            continue
        if float(g["minute"]) >= 91:
            k = (g["date"], g["home_team"], g["away_team"])
            d = et.setdefault(k, [0, 0])
            d[0 if g["team"] == g["home_team"] else 1] += 1
    ms, nfix = [], 0
    for r in csv.DictReader(open(results, encoding="utf-8")):
        if r["date"] < start or r["home_score"] in ("NA", ""):
            continue
        hg, ag = int(r["home_score"]), int(r["away_score"])
        k = (r["date"], r["home_team"], r["away_team"])
        if k in et:
            hg, ag = hg - et[k][0], ag - et[k][1]; nfix += 1
            assert hg >= 0 and ag >= 0, k
        ms.append({"date": r["date"], "home": r["home_team"], "away": r["away_team"], "hg": hg, "ag": ag,
                   "t": r["tournament"], "neutral": r["neutral"] == "TRUE", "country": r["country"]})
    return ms, nfix


class NatPoisson:
    def __init__(self, xi=0.001, ridge=3.0, wf=0.6):
        self.xi, self.ridge, self.wf = xi, ridge, wf

    def fit(self, ms, ref, x0=None):
        teams = sorted({m["home"] for m in ms} | {m["away"] for m in ms})
        self.idx = {t: i for i, t in enumerate(teams)}; n = len(teams)
        hi = np.array([self.idx[m["home"]] for m in ms]); ai = np.array([self.idx[m["away"]] for m in ms])
        hg = np.array([m["hg"] for m in ms], float); ag = np.array([m["ag"] for m in ms], float)
        hh = np.array([0.0 if m["neutral"] else 1.0 for m in ms])
        days = np.array([(ref - date.fromisoformat(m["date"])).days for m in ms], float)
        w = np.exp(-self.xi * days) * np.array([self.wf if m["t"] == "Friendly" else 1.0 for m in ms])
        R = self.ridge

        def f(q):
            att, dfn, c, h = q[:n], q[n:2 * n], q[-2], q[-1]
            lh = c + h * hh + att[hi] + dfn[ai]; la = c + att[ai] + dfn[hi]
            lam, mu = np.exp(lh), np.exp(la)
            val = -(w * (hg * lh - lam + ag * la - mu)).sum() + R * (att @ att + dfn @ dfn)
            rh, ra = w * (hg - lam), w * (ag - mu)
            g_att = -(np.bincount(hi, rh, n) + np.bincount(ai, ra, n)) + 2 * R * att
            g_dfn = -(np.bincount(ai, rh, n) + np.bincount(hi, ra, n)) + 2 * R * dfn
            return val, np.concatenate([g_att, g_dfn, [-(rh.sum() + ra.sum()), -(rh * hh).sum()]])

        q0 = np.concatenate([np.zeros(2 * n), [math.log(1.3), 0.25]]) if x0 is None else x0
        r = minimize(f, q0, jac=True, method="L-BFGS-B", options={"maxiter": 5000, "ftol": 1e-12, "gtol": 1e-7})
        q = r.x
        self.att, self.dfn, self.c, self.h = q[:n], q[n:2 * n], q[-2], q[-1]
        self.ok = r.success
        self.ngames = np.bincount(hi, minlength=n) + np.bincount(ai, minlength=n)
        return self

    def rates(self, a, b, neutral):
        i, j = self.idx[a], self.idx[b]
        hh = 0.0 if neutral else 1.0
        return (math.exp(self.c + self.h * hh + self.att[i] + self.dfn[j]),
                math.exp(self.c + self.att[j] + self.dfn[i]))

    def strength(self, t):
        i = self.idx[t]; return self.att[i] - self.dfn[i]
