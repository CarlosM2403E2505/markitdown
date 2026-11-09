#!/usr/bin/env python3
"""J21 (14-15/11/2026, parón de selecciones, prompt v8): Primera/Segunda con el modelo multi-liga (Segunda: empates x1,00; T=1,05 en el 1X2); Liga F con Poisson ridge partido a partido
(J1-J8 2026/27, sin partidos del Barça) y prior de la temporada 2025/26.
Uso: python3 j21_run.py ../datos/euro_j21.json salida.json '{"n":[f_lam,f_mu]}'"""
import importlib.util, json, math, os, sys
from datetime import date
import numpy as np
from scipy.stats import poisson
from scipy.optimize import minimize

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("em", os.path.join(HERE, "euro_model.py"))
em = importlib.util.module_from_spec(spec); spec.loader.exec_module(em)
spec2 = importlib.util.spec_from_file_location("j16", os.path.join(HERE, "j16_run.py"))
j16 = importlib.util.module_from_spec(spec2); spec2.loader.exec_module(j16)

DRAW_K, LIGAF_DRAW_K, PRIMERA_HOME = 1.08, 0.85, 0.07
SEGUNDA_DRAW_K = 1.00   # backtest del 5/11/2026 (prompt v8)
T = 1.05                # calibración del 1X2 (prompt v8)
SEGUNDA = set(range(1, 10))
HOME_LF = 2 * math.log(1.10)   # fijo: 56 partidos no bastan para estimarlo (salía 1.00)
PRIMERA = set()

LF = """1|Deportivo|Sevilla|0|1
1|Real Sociedad|Logrono|0|2
1|Eibar|Espanyol|1|0
1|Madrid CFF|Granada|3|1
1|Athletic|Badalona|3|1
1|Alaves|Valencia|2|0
1|Barcelona|Tenerife|5|0
1|Real Madrid|Atletico|3|2
2|Valencia|Madrid CFF|1|3
2|Espanyol|Badalona|0|1
2|Sevilla|Barcelona|0|4
2|Atletico|Alaves|1|0
2|Tenerife|Deportivo|0|0
2|Logrono|Athletic|0|1
2|Real Madrid|Eibar|0|0
2|Granada|Real Sociedad|3|2
3|Deportivo|Real Madrid|0|2
3|Athletic|Espanyol|2|2
3|Madrid CFF|Sevilla|1|0
3|Barcelona|Atletico|4|2
3|Real Sociedad|Tenerife|1|1
3|Alaves|Granada|1|0
3|Logrono|Valencia|2|1
3|Eibar|Badalona|1|4
4|Alaves|Barcelona|0|6
4|Badalona|Real Sociedad|0|0
4|Espanyol|Madrid CFF|5|1
4|Atletico|Logrono|1|0
4|Real Madrid|Valencia|3|1
4|Granada|Deportivo|0|3
4|Tenerife|Sevilla|1|3
4|Eibar|Athletic|1|0
5|Badalona|Granada|0|1
5|Real Sociedad|Real Madrid|3|5
5|Logrono|Barcelona|0|2
5|Madrid CFF|Alaves|1|0
5|Athletic|Atletico|3|2
5|Valencia|Tenerife|1|2
5|Sevilla|Eibar|0|1
5|Deportivo|Espanyol|1|1
6|Espanyol|Alaves|1|0
6|Sevilla|Badalona|3|3
6|Deportivo|Atletico|1|2
6|Madrid CFF|Athletic|2|2
6|Granada|Eibar|0|0
6|Tenerife|Logrono|2|1
6|Barcelona|Real Madrid|7|0
6|Valencia|Real Sociedad|0|1
7|Badalona|Tenerife|0|4
7|Logrono|Granada|2|3
7|Athletic|Valencia|1|0
7|Real Madrid|Espanyol|3|1
7|Real Sociedad|Barcelona|2|1
7|Alaves|Sevilla|1|1
7|Eibar|Deportivo|2|3
7|Atletico|Madrid CFF|4|0
8|Atletico|Valencia|4|0
8|Real Sociedad|Espanyol|1|1
8|Real Madrid|Tenerife|3|2
8|Logrono|Badalona|1|0
8|Athletic|Sevilla|0|0
8|Deportivo|Alaves|2|1
8|Eibar|Madrid CFF|2|2
8|Barcelona|Granada|3|0
9|Alaves|Real Sociedad|1|1
9|Madrid CFF|Deportivo|2|1
9|Sevilla|Real Madrid|1|3
9|Tenerife|Athletic|2|0
9|Badalona|Barcelona|0|4
9|Granada|Atletico|1|1
9|Valencia|Eibar|2|1
9|Espanyol|Logrono|2|1
10|Eibar|Real Sociedad|1|2
10|Athletic|Real Madrid|1|1"""
LF_M = [l.split("|") for l in LF.splitlines()]
LF_M = [(h, a, int(x), int(y)) for _, h, a, x, y in LF_M if "Barcelona" not in (h, a)]

def ligaf_fit(prior_w=6.0):
    teams = sorted({t for m in LF_M for t in m[:2]})
    ix = {t: i for i, t in enumerate(teams)}; n = len(teams)
    prev_avg = sum(g for g, _ in j16.LF_PREV.values()) / (len(j16.LF_PREV) * 30)
    pa, pd = np.zeros(n), np.zeros(n)
    for t in teams:
        gf, ga = j16.LF_PREV.get(t, j16.PROMOTED)
        pa[ix[t]] = math.log(gf / 30 / prev_avg); pd[ix[t]] = math.log(ga / 30 / prev_avg)
    H = np.array([ix[m[0]] for m in LF_M]); A = np.array([ix[m[1]] for m in LF_M])
    hg = np.array([m[2] for m in LF_M]); ag = np.array([m[3] for m in LF_M])
    lam_ridge = prior_w * 0.25   # peso del prior (aprox. partidos equivalentes)
    def nll(p):
        mu0, home = p[0], HOME_LF; att, dfn = p[2:2 + n], p[2 + n:]
        lh = np.exp(mu0 + home + att[H] + dfn[A]); la = np.exp(mu0 + att[A] + dfn[H])
        ll = (hg * np.log(lh) - lh).sum() + (ag * np.log(la) - la).sum()
        pen = lam_ridge * (((att - pa) ** 2).sum() + ((dfn - pd) ** 2).sum())
        return -ll + pen
    x0 = np.concatenate([[0.2, 0.1], pa, pd])
    r = minimize(nll, x0, method="L-BFGS-B")
    p = r.x
    return dict(mu0=p[0], home=HOME_LF, att=dict(zip(teams, p[2:2 + n])), dfn=dict(zip(teams, p[2 + n:])), ok=r.success)

FIX = [(1, "Valladolid – Castellón", "real valladolid", "castellon", "M"),
       (2, "Real Sociedad B – Sporting", "real sociedad b", "sporting gijon", "M"),
       (3, "Almería – Andorra", "almeria", "andorra", "M"),
       (4, "Mallorca – Córdoba", "mallorca", "cordoba", "M"),
       (5, "Oviedo – Girona", "real oviedo", "girona", "M"),
       (6, "Tenerife – Ceuta", "tenerife", "ad ceuta", "M"),
       (7, "Granada – Las Palmas", "granada", "las palmas", "M"),
       (8, "Eibar – Cádiz", "eibar", "cadiz", "M"),
       (9, "Eldense – Sabadell", "eldense", "sabadell", "M"),
       (10, "Alavés F – Eibar F", "Alaves", "Eibar", "F"),
       (11, "Real Sociedad F – Athletic F", "Real Sociedad", "Athletic", "F"),
       (12, "Sevilla F – Atlético F", "Sevilla", "Atletico", "F"),
       (13, "Valencia F – Granada F", "Valencia", "Granada", "F")]
# 14 Bélgica – Italia y 15 España – Inglaterra: selecciones, sin datos en el modelo (ver j21_selecciones.py)

def afinar(p, t=T):
    q = [v ** t for v in p]; z = sum(q)
    return [v / z for v in q]

def main():
    ds, outp = sys.argv[1], sys.argv[2]
    adj = json.loads(sys.argv[3]) if len(sys.argv) > 3 else {}
    matches = json.load(open(ds, encoding="utf-8"))["matches"]
    m = em.EuroPoisson(xi=0.0015, ridge=10, scale=1.05, blend=0.2, hier=True).fit(matches, ref_date=date(2026, 11, 14))
    lf = ligaf_fit()
    print(f"Modelo: {len(matches)} partidos, campo {m.home_adv:.3f}, conv {m.converged} | Liga F: {len(LF_M)} partidos, conv {lf['ok']}, campo {math.exp(lf['home']):.2f}")
    rows = []
    for n, lab, h, a, kind in FIX:
        if kind == "M":
            lam, mu = m.rates(h, a)
            if n in PRIMERA:
                lam, mu = lam * math.exp(PRIMERA_HOME), mu * math.exp(-PRIMERA_HOME)
            emp = m.emp; ng = (int(m.ngames[m.idx[h]]), int(m.ngames[m.idx[a]]))
        else:
            lam = math.exp(lf["mu0"] + lf["home"] + lf["att"][h] + lf["dfn"][a])
            mu = math.exp(lf["mu0"] + lf["att"][a] + lf["dfn"][h])
            emp = None; ng = ("LF", "LF")
        f = adj.get(str(n), [1.0, 1.0]); lam, mu = lam * f[0], mu * f[1]
        dk = LIGAF_DRAW_K if kind == "F" else (SEGUNDA_DRAW_K if n in SEGUNDA else DRAW_K)
        p, cats, mk = j16.finish(lam, mu, emp, dk)
        p_modelo = list(p); p = afinar(p)
        l2 = lambda v: "M" if v == 3 else str(v)
        # mercados para sueltas
        G = np.arange(11); M = np.outer(poisson.pmf(G, lam), poisson.pmf(G, mu))
        M[np.diag_indices_from(M)] *= dk; M /= M.sum()
        i, j = np.indices(M.shape)
        mk.update({"Menos 3.5": float(M[i + j <= 3].sum()), "Mas 1.5": float(M[i + j >= 2].sum()),
                   "Local marca": float(M[i >= 1].sum()), "Visit marca": float(M[j >= 1].sum())})
        rows.append({"n": n, "partido": lab, "p": p, "p_sin_T": p_modelo, "factor_empates": dk, "xg": [lam, mu], "adj": f,
                     "cats": {f"{l2(x)}-{l2(y)}": v for (x, y), v in cats.items()}, "mk": mk, "ng": ng})
        print(f"P{n:<2} {lab:<28} 1 {p[0]:5.1%} X {p[1]:5.1%} 2 {p[2]:5.1%}  xG {lam:.2f}-{mu:.2f} n={ng}{'  [aj]' if f!=[1.0,1.0] else ''}")
    print("Suma P(X) 1-13:", round(sum(r['p'][1] for r in rows), 2))
    json.dump({"rows": rows}, open(outp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

if __name__ == "__main__":
    main()
