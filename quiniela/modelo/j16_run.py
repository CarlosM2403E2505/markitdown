#!/usr/bin/env python3
"""J16: Primera + Segunda con el modelo multi-liga (factor empates de liga 1.08)
y Liga F con un modelo de tasas agregadas (tabla 2026/27 + 2025/26 como prior).

Uso: python3 j16_run.py euro.json salida.json
"""
import importlib.util
import json
import math
import os
import sys
from datetime import date

import numpy as np
from scipy.stats import poisson

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("em", os.path.join(HERE, "euro_model.py"))
em = importlib.util.module_from_spec(spec)
spec.loader.exec_module(em)

DRAW_K = 1.08          # medido fuera de muestra en ligas nacionales (21/10)
# Ventaja de campo propia de PRIMERA: el modelo usa una comun europea (0.196) y
# en Primera la real es mayor (log goles casa/fuera 0.32). Backtest en 437
# partidos de Primera no vistos: +0.06/0.09 por lado baja el log-loss en los
# dos periodos (0.9725 -> 0.9632). En Segunda no mejora: no se aplica.
PRIMERA_HOME = 0.07
PRIMERA = {1, 2, 3, 4, 5, 6, 7, 15}
G = np.arange(11)


LIGAF_DRAW_K = 0.85   # calibrado: empates reales Liga F 2025/26 = 20.8% (50 de 240)


def finish(lam, mu, emp=None, draw_k=DRAW_K):
    M = np.outer(poisson.pmf(G, lam), poisson.pmf(G, mu))
    M[np.diag_indices_from(M)] *= draw_k
    M /= M.sum()
    i, j = np.indices(M.shape)
    p = [float(M[i > j].sum()), float(M[i == j].sum()), float(M[i < j].sum())]
    cats = {(x, y): 0.0 for x in range(4) for y in range(4)}
    for x in G:
        for y in G:
            cats[(min(x, 3), min(y, 3))] += M[x, y]
    if emp:
        cats = {k: 0.8 * v + 0.2 * emp[k] for k, v in cats.items()}
    mk = {"Mas 2.5": float(M[i + j >= 3].sum()),
          "Ambos marcan": float(M[(i >= 1) & (j >= 1)].sum())}
    return p, cats, mk


# ---------------- Liga F: tasas agregadas con prior ----------------
# 2026/27 tras 7 jornadas (futboleras.io): GF, GC, partidos.
# Se QUITAN los partidos contra el Barcelona (J1-J6 conocidos): el Barça es un
# caso aparte (29-4) y un 7-0 en 7 partidos deforma la defensa de cualquiera.
LF_CUR = {"Barcelona": (29, 4, 7), "Real Madrid": (16, 7, 6), "Athletic": (12, 8, 7),
          "Madrid CFF": (11, 13, 7), "Atletico": (12, 7, 6), "Tenerife": (10, 6, 6),
          "Eibar": (6, 7, 7), "Granada": (8, 11, 7), "Espanyol": (10, 9, 7),
          "Deportivo": (8, 8, 7), "Badalona": (9, 12, 7), "Real Sociedad": (9, 12, 7),
          "Sevilla": (8, 7, 6), "Alaves": (4, 4, 6), "Logrono": (7, 8, 6),
          "Valencia": (4, 14, 7)}
# 2025/26 final, 30 partidos (Wikipedia). Alavés y Valencia no estaban: prior de recien ascendido
LF_PREV = {"Barcelona": (130, 9), "Real Madrid": (65, 18), "Real Sociedad": (61, 27),
           "Tenerife": (49, 22), "Atletico": (63, 39), "Granada": (36, 42),
           "Athletic": (35, 44), "Sevilla": (33, 46), "Madrid CFF": (41, 59),
           "Badalona": (28, 46), "Espanyol": (28, 44), "Deportivo": (34, 54),
           "Eibar": (18, 47), "Logrono": (29, 54)}
PROMOTED = (0.75 * 1.44 * 30, 1.35 * 1.44 * 30)   # ataque flojo, defensa floja
N_CUR, N_PRIOR, N_SHRINK = 7, 8, 3
HOME = 1.10


def ligaf_rates():
    cur_avg = (sum(g for t, (g, _, n) in LF_CUR.items() if t != "Barcelona")
               / sum(n for t, (_, _, n) in LF_CUR.items() if t != "Barcelona"))
    prev_avg = sum(g for g, _ in LF_PREV.values()) / (len(LF_PREV) * 30)
    att, dfn = {}, {}
    for t, (gf, ga, nc) in LF_CUR.items():
        pgf, pga = LF_PREV.get(t, PROMOTED)
        a = (nc * (gf / nc / cur_avg) + N_PRIOR * (pgf / 30 / prev_avg)) / (nc + N_PRIOR)
        d = (nc * (ga / nc / cur_avg) + N_PRIOR * (pga / 30 / prev_avg)) / (nc + N_PRIOR)
        n = nc + N_PRIOR
        att[t] = (n * a + N_SHRINK) / (n + N_SHRINK)
        dfn[t] = (n * d + N_SHRINK) / (n + N_SHRINK)
    return att, dfn, cur_avg


def ligaf_match(h, a):
    att, dfn, avg = ligaf_rates()
    lam = avg * att[h] * dfn[a] * HOME
    mu = avg * att[a] * dfn[h] / HOME
    return lam, mu


FIX = [(1, "Rayo Vallecano – Elche", "rayo vallecano", "elche", "M"),
       (2, "Valencia – Villarreal", "valencia", "villarreal", "M"),
       (3, "Atlético – Deportivo", "atletico", "deportivo coruna", "M"),
       (4, "Athletic – Getafe", "athletic bilbao", "getafe", "M"),
       (5, "Celta – Betis", "celta", "betis", "M"),
       (6, "Real Sociedad – Levante", "real sociedad", "levante", "M"),
       (7, "Sevilla – Osasuna", "sevilla", "osasuna", "M"),
       (8, "Leganés – Mallorca", "leganes", "mallorca", "M"),
       (9, "Almería – Oviedo", "almeria", "real oviedo", "M"),
       (10, "Sabadell – Tenerife", "sabadell", "tenerife", "M"),
       (11, "Logroño F – Badalona F", "Logrono", "Badalona", "F"),
       (12, "Deportivo F – Alavés F", "Deportivo", "Alaves", "F"),
       (13, "Eibar F – Madrid CFF", "Eibar", "Madrid CFF", "F"),
       (14, "Real Madrid F – Tenerife F", "Real Madrid", "Tenerife", "F"),
       (15, "Barcelona – Real Madrid", "barcelona", "real madrid", "M")]


def main():
    ds, outp = sys.argv[1], sys.argv[2]
    adj = json.loads(sys.argv[3]) if len(sys.argv) > 3 else {}
    matches = json.load(open(ds, encoding="utf-8"))["matches"]
    m = em.EuroPoisson(xi=0.0015, ridge=10, scale=1.05, blend=0.2, hier=True).fit(
        matches, ref_date=date(2026, 10, 21))
    print(f"Modelo: {len(matches)} partidos, ventaja campo {m.home_adv:.3f}, conv {m.converged}")
    rows = []
    for n, lab, h, a, kind in FIX:
        if kind == "M":
            lam, mu = m.rates(h, a)
            if n in PRIMERA:
                lam, mu = lam * math.exp(PRIMERA_HOME), mu * math.exp(-PRIMERA_HOME)
            emp = m.emp
            ng = (int(m.ngames[m.idx[h]]), int(m.ngames[m.idx[a]]))
        else:
            lam, mu = ligaf_match(h, a)
            emp = None
            ng = ("tabla", "tabla")
        f = adj.get(str(n), [1.0, 1.0])
        lam, mu = lam * f[0], mu * f[1]
        p, cats, mk = finish(lam, mu, emp, DRAW_K if kind == "M" else LIGAF_DRAW_K)
        lab2 = lambda v: "M" if v == 3 else str(v)
        rows.append({"n": n, "partido": lab, "p": p, "xg": [lam, mu], "adj": f,
                     "cats": {f"{lab2(x)}-{lab2(y)}": v for (x, y), v in cats.items()},
                     "mk": mk, "ng": ng})
        flag = "  [ajuste live]" if f != [1.0, 1.0] else ""
        print(f"P{n:<2} {lab:<28} 1 {p[0]:5.1%}  X {p[1]:5.1%}  2 {p[2]:5.1%}  "
              f"xG {lam:.2f}-{mu:.2f}  n={ng}{flag}")
    pl = rows[-1]["cats"]
    acc = 0
    print("\nPLENO Barcelona – Real Madrid:")
    for k, v in sorted(pl.items(), key=lambda kv: -kv[1])[:8]:
        acc += v
        print(f"   {k:<4} {v:5.1%}  acumulado {acc:5.1%}")
    json.dump({"rows": rows}, open(outp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
