#!/usr/bin/env python3
"""Modelo Poisson multi-liga con gradiente analitico (escala a +20.000 partidos).

  log(goles local)     = c + ventaja + ataque[local] + defensa[visitante]
  log(goles visitante) = c +           ataque[visit] + defensa[local]

Ponderacion temporal exp(-xi * dias) y encogimiento ridge hacia la media.
Los partidos europeos enlazan las ligas: asi un 1.0 de ataque en Noruega y
un 1.0 en Inglaterra quedan en la MISMA escala.

Sin rho de Dixon-Coles: en el backtest espanol no aporto nada.
Cero cuotas de casas de apuestas.

Uso:
    python3 euro_model.py euro.json --backtest 2026-02-01
    python3 euro_model.py euro.json --fixtures j15_fx.json
"""
import argparse
import json
import math
from datetime import date

import numpy as np
from scipy.optimize import minimize
from scipy.stats import poisson

MAXG = 10
EPS = 1e-12


def team_leagues(matches):
    """Liga de cada equipo = la competicion domestica con mas partidos suyos
    en sus ultimos 365 dias con datos. Las copas UEFA no cuentan."""
    last = {}
    for m in matches:
        for t in (m["home"], m["away"]):
            last[t] = max(last.get(t, ""), m["date"])
    cnt = {}
    for m in matches:
        comp = m["competition"].split(":")[0]
        if comp.startswith("uefa"):
            continue
        for t in (m["home"], m["away"]):
            if (date.fromisoformat(last[t]) - date.fromisoformat(m["date"])).days > 365:
                continue
            cnt.setdefault(t, {}).setdefault(comp, 0)
            cnt[t][comp] += 1
    return {t: max(c, key=c.get) for t, c in cnt.items()}


class EuroPoisson:
    """hier=True: fuerza = nivel de la LIGA + desviacion del equipo.

    El encogimiento lleva a cada equipo hacia la media de SU liga, no hacia
    la media global. Asi un equipo que arrasa en una liga floja (Noruega 2a)
    no se cuela como si fuera de elite: su liga entera queda por debajo.
    """

    def __init__(self, xi=0.0015, ridge=1.0, scale=1.0, blend=0.0,
                 hier=True, ridge_league=0.05):
        self.xi, self.ridge, self.scale, self.blend = xi, ridge, scale, blend
        self.hier, self.ridge_league = hier, ridge_league
        # Factor de empates medido fuera de muestra (21/10/2026):
        #   ligas nacionales: 1.08 mejora el log-loss (el Poisson se queda
        #   corto de empates ~1.5-2 puntos); copas UEFA: 1.0 (en copas hay
        #   MENOS empates de los que declara el modelo).
        self.draw_k = 1.0

    def fit(self, matches, ref_date=None):
        teams = sorted({m["home"] for m in matches} | {m["away"] for m in matches})
        self.idx = {t: i for i, t in enumerate(teams)}
        n = len(teams)
        hi = np.array([self.idx[m["home"]] for m in matches])
        ai = np.array([self.idx[m["away"]] for m in matches])
        hg = np.array([m["hg"] for m in matches], float)
        ag = np.array([m["ag"] for m in matches], float)
        ref = ref_date or max(date.fromisoformat(m["date"]) for m in matches)
        days = np.array([(ref - date.fromisoformat(m["date"])).days
                         for m in matches], float)
        w = np.exp(-self.xi * days)
        R, RL = self.ridge, self.ridge_league
        tl = team_leagues(matches) if self.hier else {}
        leagues = sorted(set(tl.values())) or ["-"]
        self.leagues = leagues
        L = len(leagues)
        lix = {l: k for k, l in enumerate(leagues)}
        # equipos sin liga domestica (solo copas): sin efecto de liga
        lg = np.array([lix.get(tl.get(t), -1) for t in teams])
        has = lg >= 0
        lgc = np.where(has, lg, 0)
        self.team_league = {t: tl.get(t) for t in teams}

        def f(q):
            d_att, d_dfn = q[:n], q[n:2 * n]
            A, D = q[2 * n:2 * n + L], q[2 * n + L:2 * n + 2 * L]
            c, h = q[-2], q[-1]
            att = d_att + np.where(has, A[lgc], 0.0)
            dfn = d_dfn + np.where(has, D[lgc], 0.0)
            ll_h = c + h + att[hi] + dfn[ai]
            ll_a = c + att[ai] + dfn[hi]
            lam, mu = np.exp(ll_h), np.exp(ll_a)
            val = -(w * (hg * ll_h - lam + ag * ll_a - mu)).sum()
            val += R * (d_att @ d_att + d_dfn @ d_dfn) + RL * (A @ A + D @ D)
            rh = w * (hg - lam)          # d ll / d log lam
            ra = w * (ag - mu)
            g_att = -(np.bincount(hi, rh, n) + np.bincount(ai, ra, n))
            g_dfn = -(np.bincount(ai, rh, n) + np.bincount(hi, ra, n))
            g_A = np.bincount(lgc[has], g_att[has], L) + 2 * RL * A
            g_D = np.bincount(lgc[has], g_dfn[has], L) + 2 * RL * D
            g_c = -(rh.sum() + ra.sum())
            g_h = -rh.sum()
            return val, np.concatenate([g_att + 2 * R * d_att,
                                        g_dfn + 2 * R * d_dfn,
                                        g_A, g_D, [g_c, g_h]])

        q0 = np.concatenate([np.zeros(2 * n + 2 * L), [math.log(1.3), 0.2]])
        res = minimize(f, q0, jac=True, method="L-BFGS-B",
                       options={"maxiter": 8000, "ftol": 1e-13, "gtol": 1e-7})
        q = res.x
        A, D = q[2 * n:2 * n + L], q[2 * n + L:2 * n + 2 * L]
        self.att = q[:n] + np.where(has, A[lgc], 0.0)
        self.dfn = q[n:2 * n] + np.where(has, D[lgc], 0.0)
        self.league_att = dict(zip(leagues, A))
        self.league_dfn = dict(zip(leagues, D))
        self.c, self.home_adv = q[-2], q[-1]
        self.converged = res.success
        self.ngames = np.bincount(hi, minlength=n) + np.bincount(ai, minlength=n)
        self.emp = {(i, j): 0.0 for i in range(4) for j in range(4)}
        for m in matches:
            self.emp[(min(m["hg"], 3), min(m["ag"], 3))] += 1 / len(matches)
        return self

    def rates(self, home, away):
        i, j = self.idx[home], self.idx[away]
        lam = math.exp(self.c + self.home_adv + self.att[i] + self.dfn[j])
        mu = math.exp(self.c + self.att[j] + self.dfn[i])
        return lam * self.scale, mu * self.scale

    def matrix(self, home, away):
        lam, mu = self.rates(home, away)
        g = np.arange(MAXG + 1)
        M = np.outer(poisson.pmf(g, lam), poisson.pmf(g, mu))
        if self.draw_k != 1.0:
            M = M.copy()
            M[np.diag_indices_from(M)] *= self.draw_k
        return M / M.sum(), lam, mu

    def cats(self, home, away):
        M, _, _ = self.matrix(home, away)
        out = {(i, j): 0.0 for i in range(4) for j in range(4)}
        for x in range(MAXG + 1):
            for y in range(MAXG + 1):
                out[(min(x, 3), min(y, 3))] += M[x, y]
        if self.blend:
            out = {k: (1 - self.blend) * v + self.blend * self.emp[k]
                   for k, v in out.items()}
        return out

    def p1x2(self, home, away):
        M, lam, mu = self.matrix(home, away)
        i, j = np.indices(M.shape)
        return (float(M[i > j].sum()), float(M[i == j].sum()),
                float(M[i < j].sum())), lam, mu


def evaluate(model, test, base_split, base_cats):
    rows = {"modelo": [0, 0, 0, 0], "base": [0, 0, 0, 0]}
    n = 0
    for r in test:
        if r["home"] not in model.idx or r["away"] not in model.idx:
            continue
        res = 0 if r["hg"] > r["ag"] else (1 if r["hg"] == r["ag"] else 2)
        cat = (min(r["hg"], 3), min(r["ag"], 3))
        (p1, px, p2), _, _ = model.p1x2(r["home"], r["away"])
        cm = model.cats(r["home"], r["away"])
        for name, p, c in (("modelo", (p1, px, p2), cm),
                           ("base", base_split, base_cats)):
            rows[name][0] += -math.log(max(p[res], EPS))
            rows[name][1] += -math.log(max(c[cat], EPS))
            rows[name][2] += max(c, key=c.get) == cat
            rows[name][3] += cat in sorted(c, key=c.get, reverse=True)[:5]
        n += 1
    return n, {k: [v / max(n, 1) for v in vals] for k, vals in rows.items()}


def backtest(matches, cutoff, xi, ridge):
    train = [m for m in matches if m["date"] < cutoff]
    test = [m for m in matches if m["date"] >= cutoff]
    nt = len(train)
    split = (sum(m["hg"] > m["ag"] for m in train) / nt,
             sum(m["hg"] == m["ag"] for m in train) / nt,
             sum(m["hg"] < m["ag"] for m in train) / nt)
    bc = {(i, j): 0.0 for i in range(4) for j in range(4)}
    for m in train:
        bc[(min(m["hg"], 3), min(m["ag"], 3))] += 1 / nt
    print(f"Entreno {nt} | prueba {len(test)} (desde {cutoff}, nunca vistos)\n")
    print(f"{'config':<34}{'n':>6}{'LL 1X2':>9}{'LL pleno':>10}"
          f"{'pleno#1':>9}{'pleno top5':>11}")
    best = None
    for hier, rdg in [(False, 1.0)] + [(True, r) for r in ridge]:
        m = EuroPoisson(xi=xi, ridge=rdg, hier=hier).fit(train)
        for scale in (1.05,):
            for blend in (0.2,):
                m.scale, m.blend = scale, blend
                for subset, data in (("todo", test),
                                     ("COPAS", [r for r in test if
                                                r["competition"].startswith("uefa")])):
                    n, rs = evaluate(m, data, split, bc)
                    a = rs["modelo"]
                    lab = f"{'JERARQ' if hier else 'plano '} ridge={rdg} [{subset}]"
                    print(f"{lab:<34}{n:>6}{a[0]:>9.4f}{a[1]:>10.4f}"
                          f"{a[2]:>9.1%}{a[3]:>11.1%}")
                    if subset == "todo" and (best is None or a[1] < best[0]):
                        best = (a[1], f"hier={hier} ridge={rdg}", scale, blend)
    for subset, data in (("todo", test), ("COPAS", [r for r in test if
                                                   r["competition"].startswith("uefa")])):
        n, rs = evaluate(m, data, split, bc)
        b = rs["base"]
        lab = f"BASE (media de la liga) [{subset}]"
        print(f"{lab:<34}{n:>6}{b[0]:>9.4f}{b[1]:>10.4f}{b[2]:>9.1%}{b[3]:>11.1%}")
    print(f"\nMejor (LL pleno, todo): {best[1]} escala={best[2]} mezcla={best[3]}")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("dataset")
    ap.add_argument("--backtest", default=None)
    ap.add_argument("--fixtures", default=None)
    ap.add_argument("--xi", type=float, default=0.0015)
    ap.add_argument("--ridge", type=float, default=1.0)
    ap.add_argument("--scale", type=float, default=1.0)
    ap.add_argument("--blend", type=float, default=0.2)
    ap.add_argument("--out", default=None)
    ap.add_argument("--flat", action="store_true", help="sin niveles de liga")
    args = ap.parse_args()
    with open(args.dataset, encoding="utf-8") as f:
        matches = json.load(f)["matches"]

    if args.backtest:
        backtest(matches, args.backtest, args.xi, (1.0, 3.0, 10.0))
        return

    m = EuroPoisson(args.xi, args.ridge, args.scale, args.blend,
                    hier=not args.flat).fit(
        matches, ref_date=date(2026, 10, 20))
    print(f"Ajustado: {len(matches)} partidos, {len(m.idx)} equipos, "
          f"ventaja campo={m.home_adv:.3f}, convergencia={m.converged}\n")
    with open(args.fixtures, encoding="utf-8") as f:
        fx = json.load(f)["fixtures"]
    out = []
    for x in fx:
        h, a = x["home"], x["away"]
        (p1, px, p2), lam, mu = m.p1x2(h, a)
        c = m.cats(h, a)
        top = sorted(c.items(), key=lambda kv: -kv[1])[:6]
        lab = lambda v: "M" if v == 3 else str(v)
        M, _, _ = m.matrix(h, a)
        i, j = np.indices(M.shape)
        mk = {"Mas 1.5": float(M[i + j >= 2].sum()),
              "Mas 2.5": float(M[i + j >= 3].sum()),
              "Menos 3.5": float(M[i + j <= 3].sum()),
              "Ambos marcan": float(M[(i >= 1) & (j >= 1)].sum()),
              "Local marca": float(M[i >= 1].sum()),
              "Visit marca": float(M[j >= 1].sum())}
        rec = {"n": x["n"], "home": h, "away": a, "p": [p1, px, p2],
               "xg": [lam, mu], "top": [(f"{lab(k[0])}-{lab(k[1])}", v) for k, v in top],
               "mk": mk, "ngames": [int(m.ngames[m.idx[h]]), int(m.ngames[m.idx[a]])]}
        out.append(rec)
        print(f"P{x['n']:<2} {h:>12} - {a:<12} 1 {p1:5.1%}  X {px:5.1%}  "
              f"2 {p2:5.1%}   xG {lam:.2f}-{mu:.2f}   n={rec['ngames']}")
        print("      plenos: " + "  ".join(f"{s} {v:.1%}" for s, v in rec["top"]))
        print("      " + "  ".join(f"{k} {v:.0%}" for k, v in mk.items()))
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            json.dump(out, f, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
