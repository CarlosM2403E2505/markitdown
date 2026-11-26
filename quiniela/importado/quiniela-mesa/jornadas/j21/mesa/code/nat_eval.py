"""Validacion fuera de muestra (origen movil mensual) del modelo de selecciones.
Cada mes M: se ajusta con los partidos anteriores al dia 1 de M y se predicen los partidos de M (nunca vistos).
Ajuste de hiperparametros en 2022-11..2024-10; evaluacion final en 2024-11..2026-10.
Uso: python3 nat_eval.py grid|long  (rutas fijas dentro de mesa_j21)"""
import importlib.util, json, math, sys, itertools, pickle, os
from datetime import date
import numpy as np
from scipy.stats import poisson

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("nm", os.path.join(BASE, "code", "nat_model.py"))
nm = importlib.util.module_from_spec(spec); spec.loader.exec_module(nm)
D = os.path.join(BASE, "dl_git", "international_results")
MS, NFIX = nm.load(os.path.join(D, "results.csv"), os.path.join(D, "goalscorers.csv"), "2004-01-01")
G = np.arange(11)


def months(a, b):
    y, m = a
    while (y, m) <= b:
        yield date(y, m, 1)
        y, m = (y + 1, 1) if m == 12 else (y, m + 1)


def nxt(d):
    return date(d.year + 1, 1, 1) if d.month == 12 else date(d.year, d.month + 1, 1)


def run(cfg, start, end, train_from="2006-01-01"):
    xi, R, wf = cfg
    out = []; x0 = None
    for t in months(start, end):
        ts, te = t.isoformat(), nxt(t).isoformat()
        test = [m for m in MS if ts <= m["date"] < te]
        if not test:
            continue
        train = [m for m in MS if train_from <= m["date"] < ts]
        mod = nm.NatPoisson(xi, R, wf).fit(train, t)
        ur = sorted([u for u in nm.UEFA if u in mod.idx and mod.ngames[mod.idx[u]] >= 10], key=lambda u: -mod.strength(u))
        rank = {u: k + 1 for k, u in enumerate(ur)}
        for m in test:
            if m["home"] not in mod.idx or m["away"] not in mod.idx:
                continue
            lam, mu = mod.rates(m["home"], m["away"], m["neutral"])
            M = np.outer(poisson.pmf(G, lam), poisson.pmf(G, mu)); M /= M.sum()
            i, j = np.indices(M.shape)
            p = (M[i > j].sum(), M[i == j].sum(), M[i < j].sum())
            cats = np.zeros((4, 4))
            np.add.at(cats, (np.minimum(i, 3), np.minimum(j, 3)), M)
            res = 0 if m["hg"] > m["ag"] else 1 if m["hg"] == m["ag"] else 2
            out.append({"date": m["date"], "home": m["home"], "away": m["away"], "t": m["t"], "neutral": m["neutral"],
                        "p": p, "cats": cats, "res": res, "cat": (min(m["hg"], 3), min(m["ag"], 3)),
                        "uefa2": m["home"] in nm.UEFA and m["away"] in nm.UEFA,
                        "ng": (int(mod.ngames[mod.idx[m["home"]]]), int(mod.ngames[mod.idx[m["away"]]])),
                        "s": (mod.strength(m["home"]), mod.strength(m["away"])), "lam": lam, "mu": mu,
                        "rk": (rank.get(m["home"], 99), rank.get(m["away"], 99)), "month": t.month})
    return out


def ll(rows, k=1.0):
    s = 0.0
    for r in rows:
        p1, px, p2 = r["p"]; z = p1 + k * px + p2
        s -= math.log(max((p1, k * px, p2)[r["res"]] / z, 1e-12))
    return s / max(len(rows), 1)


if __name__ == "__main__":
    mode = sys.argv[1]
    if mode in ("grid", "grid2"):
        grid = list(itertools.product([0.0005, 0.00075, 0.001, 0.0015, 0.002, 0.003], [1.0, 2.0, 4.0, 8.0], [0.4, 0.6, 0.8, 1.0])) if mode == "grid" else \
            list(itertools.product([0.0002, 0.0003, 0.0005], [0.25, 0.5, 1.0], [0.8, 1.0]))
        res = {}
        for cfg in grid:
            rows = run(cfg, (2022, 11), (2026, 10))
            tune = [r for r in rows if r["date"] < "2024-11-01"]; test = [r for r in rows if r["date"] >= "2024-11-01"]
            u_t = [r for r in tune if r["uefa2"]]; u_s = [r for r in test if r["uefa2"]]
            res[str(cfg)] = {"tune_all": ll(tune), "tune_uefa": ll(u_t), "test_all": ll(test), "test_uefa": ll(u_s),
                             "n": [len(tune), len(u_t), len(test), len(u_s)]}
            print(cfg, {k: (round(v, 4) if isinstance(v, float) else v) for k, v in res[str(cfg)].items()}, flush=True)
        json.dump(res, open(os.path.join(BASE, "calc", f"nat_{mode}.json"), "w"), indent=1)
    elif mode == "long":
        cfg = tuple(json.loads(sys.argv[2]))
        rows = run(cfg, (2012, 1), (2026, 10))
        pickle.dump({"cfg": cfg, "rows": rows, "nfix": NFIX}, open(os.path.join(BASE, "calc", "nat_long.pkl"), "wb"))
        print(len(rows), "predicciones fuera de muestra 2012-01..2026-10")
