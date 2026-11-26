#!/usr/bin/env python3
"""J19 (Champions + Europa League, 3-5/11/2026): modelo multi-liga, empates x1.0 (copas UEFA).
Uso: python3 j19_run.py datos.json fixtures.json salida.json '{"n":[f_lam,f_mu]}' [ref_date]"""
import importlib.util, json, math, os, sys
from datetime import date
import numpy as np
from scipy.stats import poisson
HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("em", os.path.join(HERE, "euro_model.py"))
em = importlib.util.module_from_spec(spec); spec.loader.exec_module(em)
spec2 = importlib.util.spec_from_file_location("j16", os.path.join(HERE, "j16_run.py"))
j16 = importlib.util.module_from_spec(spec2); spec2.loader.exec_module(j16)
DRAW_K = 1.0  # copas UEFA: sin corrección de empates (medido 21-23/10)

def main():
    ds, fxp, outp = sys.argv[1:4]
    adj = json.loads(sys.argv[4]) if len(sys.argv) > 4 else {}
    ref = date.fromisoformat(sys.argv[5]) if len(sys.argv) > 5 else date(2026, 11, 2)
    matches = json.load(open(ds, encoding="utf-8"))["matches"]
    fx = json.load(open(fxp, encoding="utf-8"))["fixtures"]
    m = em.EuroPoisson(xi=0.0015, ridge=10, scale=1.05, blend=0.2, hier=True).fit(matches, ref_date=ref)
    print(f"Modelo: {len(matches)} partidos, campo {m.home_adv:.3f}, conv {m.converged}")
    rows = []
    for x in fx:
        n, lab, h, a = x["n"], x["label"], x["home"], x["away"]
        lam, mu = m.rates(h, a)
        f = adj.get(str(n), [1.0, 1.0]); lam, mu = lam * f[0], mu * f[1]
        p, cats, mk = j16.finish(lam, mu, m.emp, DRAW_K)
        l2 = lambda v: "M" if v == 3 else str(v)
        G = np.arange(11); M = np.outer(poisson.pmf(G, lam), poisson.pmf(G, mu)); M /= M.sum()
        i, j = np.indices(M.shape)
        mk.update({"Menos 3.5": float(M[i + j <= 3].sum()), "Mas 1.5": float(M[i + j >= 2].sum()),
                   "Local marca": float(M[i >= 1].sum()), "Visit marca": float(M[j >= 1].sum())})
        ng = (int(m.ngames[m.idx[h]]), int(m.ngames[m.idx[a]]))
        rows.append({"n": n, "partido": lab, "dia": x.get("dia"), "comp": x.get("comp"), "p": p, "xg": [lam, mu], "adj": f,
                     "cats": {f"{l2(a_)}-{l2(b_)}": v for (a_, b_), v in cats.items()}, "mk": mk, "ng": ng})
        print(f"P{n:<2} {lab:<28} 1 {p[0]:5.1%} X {p[1]:5.1%} 2 {p[2]:5.1%}  xG {lam:.2f}-{mu:.2f} n={ng}{'  [aj]' if f!=[1.0,1.0] else ''}")
    print("Suma P(X) 1-14:", round(sum(r['p'][1] for r in rows[:14]), 2))
    pl = rows[-1]["cats"]; acc = 0
    print("\nPLENO:", rows[-1]["partido"])
    for k, v in sorted(pl.items(), key=lambda kv: -kv[1])[:8]:
        acc += v; print(f"   {k:<4} {v:5.1%}  acum {acc:5.1%}")
    json.dump({"rows": rows}, open(outp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

if __name__ == "__main__":
    main()
