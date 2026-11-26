"""Modelos de selecciones (desde la J21, rescatado de «quiniela-mesa» y validado aquí).

Datos: datos/selecciones/results.csv y goalscorers.csv (martj42/international_results, CC0),
hasta el 6/10/2026. Marcador a 90': se restan los goles de la prórroga (minuto ≥ 91).

- NatPoisson: Poisson con ataque y defensa por selección, ridge y decaimiento temporal; campo
  solo si el partido no es en campo neutral. Código original del proyecto «quiniela-mesa»
  (jornadas/j21/mesa/code/nat_model.py), sin cambios de fondo.
- elo_historico: Elo calculado partido a partido con la fórmula de eloratings.net (K por
  torneo, multiplicador por diferencia de goles, +100 de campo).
- uno_x_dos_elo: el método usado hasta la v1.6 de la J21 (Elo + 100 de campo → puntuación
  esperada → Poisson de 2,4 goles en total).
"""
import csv, math, os
from datetime import date
import numpy as np
from scipy.optimize import minimize, brentq
from scipy.stats import poisson

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIR = os.path.join(RAIZ, "datos", "selecciones")
UEFA = set("""Albania|Andorra|Armenia|Austria|Azerbaijan|Belarus|Belgium|Bosnia and Herzegovina|Bulgaria|Croatia|Cyprus|
Czech Republic|Denmark|England|Estonia|Faroe Islands|Finland|France|Georgia|Germany|Gibraltar|Greece|Hungary|Iceland|Israel|
Italy|Kazakhstan|Kosovo|Latvia|Liechtenstein|Lithuania|Luxembourg|Malta|Moldova|Montenegro|Netherlands|North Macedonia|
Northern Ireland|Norway|Poland|Portugal|Republic of Ireland|Romania|Russia|San Marino|Scotland|Serbia|Slovakia|Slovenia|
Spain|Sweden|Switzerland|Turkey|Ukraine|Wales""".replace("\n", "").split("|"))
COMPET_UEFA = {"UEFA Nations League", "UEFA Euro qualification", "FIFA World Cup qualification", "UEFA Euro", "FIFA World Cup"}
NOMBRES = {"España": "Spain", "Inglaterra": "England", "Bélgica": "Belgium", "Italia": "Italy", "Francia": "France",
           "Chequia": "Czech Republic", "Croacia": "Croatia"}
G = np.arange(11)


def cargar(desde="1872-01-01"):
    """Partidos con marcador final (hg, ag) y a 90' (hg90, ag90)."""
    pr = {}
    for g in csv.DictReader(open(os.path.join(DIR, "goalscorers.csv"), encoding="utf-8")):
        if g["minute"] in ("NA", "") or float(g["minute"]) < 91:
            continue
        d = pr.setdefault((g["date"], g["home_team"], g["away_team"]), [0, 0])
        d[0 if g["team"] == g["home_team"] else 1] += 1
    ms = []
    for r in csv.DictReader(open(os.path.join(DIR, "results.csv"), encoding="utf-8")):
        if r["date"] < desde or r["home_score"] in ("NA", ""):
            continue
        hg, ag = int(r["home_score"]), int(r["away_score"])
        e = pr.get((r["date"], r["home_team"], r["away_team"]), [0, 0])
        ms.append({"date": r["date"], "home": r["home_team"], "away": r["away_team"], "hg": hg, "ag": ag,
                   "hg90": max(0, hg - e[0]), "ag90": max(0, ag - e[1]), "t": r["tournament"], "neutral": r["neutral"] == "TRUE"})
    return ms


class NatPoisson:
    def __init__(self, xi=0.00075, ridge=0.1, wf=1.0):
        self.xi, self.ridge, self.wf = xi, ridge, wf

    def fit(self, ms, ref):
        teams = sorted({m["home"] for m in ms} | {m["away"] for m in ms})
        self.idx = {t: i for i, t in enumerate(teams)}; n = len(teams)
        hi = np.array([self.idx[m["home"]] for m in ms]); ai = np.array([self.idx[m["away"]] for m in ms])
        hg = np.array([m["hg90"] for m in ms], float); ag = np.array([m["ag90"] for m in ms], float)
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

        q0 = np.concatenate([np.zeros(2 * n), [math.log(1.3), 0.25]])
        r = minimize(f, q0, jac=True, method="L-BFGS-B", options={"maxiter": 5000, "ftol": 1e-12, "gtol": 1e-7})
        q = r.x; self.att, self.dfn, self.c, self.h, self.ok = q[:n], q[n:2 * n], q[-2], q[-1], r.success
        return self

    def rates(self, a, b, neutral=False):
        i, j = self.idx[a], self.idx[b]
        return (math.exp(self.c + (0 if neutral else self.h) + self.att[i] + self.dfn[j]), math.exp(self.c + self.att[j] + self.dfn[i]))


def matriz(lam, mu, k=1.0):
    M = np.outer(poisson.pmf(G, lam), poisson.pmf(G, mu)); M[np.diag_indices_from(M)] *= k; return M / M.sum()


def uno_x_dos(M):
    i, j = np.indices(M.shape); return [float(M[i > j].sum()), float(M[i == j].sum()), float(M[i < j].sum())]


def _k_torneo(t):
    if t == "FIFA World Cup":
        return 60
    if t in ("UEFA Euro", "Copa América", "African Cup of Nations", "AFC Asian Cup", "Gold Cup", "Confederations Cup"):
        return 50
    if "qualification" in t or "Nations League" in t:
        return 40
    return 20 if t == "Friendly" else 30


def elo_historico(ms):
    """Devuelve (elo_antes, elo_final): elo_antes[i] = (Elo local, Elo visitante) antes del partido i."""
    elo, antes = {}, []
    for m in ms:
        a, b = elo.get(m["home"], 1500.0), elo.get(m["away"], 1500.0)
        antes.append((a, b))
        dr = a - b + (0 if m["neutral"] else 100)
        we = 1 / (10 ** (-dr / 400) + 1)
        n = abs(m["hg"] - m["ag"]); gmul = 1 if n <= 1 else (1.5 if n == 2 else (11 + n) / 8)
        w = 1.0 if m["hg"] > m["ag"] else (0.5 if m["hg"] == m["ag"] else 0.0)
        d = _k_torneo(m["t"]) * gmul * (w - we)
        elo[m["home"]] = a + d; elo[m["away"]] = b - d
    return antes, elo


def uno_x_dos_elo(dr, total=2.4, k=1.0):
    """Método de la v1.2: puntuación esperada del Elo (dr ya incluye el campo) → Poisson con total fijo."""
    we = 1 / (10 ** (-dr / 400) + 1)
    def err(s):
        p = uno_x_dos(matriz(total * s, total * (1 - s), k)); return p[0] + 0.5 * p[1] - we
    lo, hi = 0.001, 0.999
    if err(lo) > 0: s = lo
    elif err(hi) < 0: s = hi
    else: s = brentq(err, lo, hi)
    return uno_x_dos(matriz(total * s, total * (1 - s), k))
