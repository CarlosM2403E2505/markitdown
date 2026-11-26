"""Calibracion del campo y de los empates en partidos oficiales UEFA (no neutrales) de nivel similar.
Ajuste conjunto (k empates, d campo): lam*exp(-d), mu*exp(+d), diagonal x k. Estimado en 2012-01..2024-10, comprobado en 2024-11..2026-10."""
import pickle, math, json, os, importlib.util
import numpy as np
from scipy.stats import poisson
from scipy.optimize import minimize
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
s = importlib.util.spec_from_file_location("nm", os.path.join(BASE, "code", "nat_model.py")); nm = importlib.util.module_from_spec(s); s.loader.exec_module(nm)
L = pickle.load(open(os.path.join(BASE, "calc", "nat_long.pkl"), "rb")); R = L["rows"]
G = np.arange(11); I, J = np.indices((11, 11))
def probs(r, k, d):
    M = np.outer(poisson.pmf(G, r["lam"] * math.exp(-d)), poisson.pmf(G, r["mu"] * math.exp(d))); M[np.diag_indices(11)] *= k; M /= M.sum()
    return M[I > J].sum(), M[I == J].sum(), M[I < J].sum()
def nll(rows, k, d): return -sum(math.log(probs(r, k, d)[r["res"]]) for r in rows) / len(rows)
comp = lambda r: r["uefa2"] and r["t"] in nm.COMPET_UEFA and not r["neutral"]
S = {"UEFA_oficial_no_neutral": comp,
     "top16_ambos_no_neutral": lambda r: comp(r) and max(r["rk"]) <= 16,
     "top24_ambos_|ds|<0,3_no_neutral": lambda r: comp(r) and max(r["rk"]) <= 24 and abs(r["s"][0] - r["s"][1]) < 0.3,
     "top24_ambos_|ds|<0,5_no_neutral": lambda r: comp(r) and max(r["rk"]) <= 24 and abs(r["s"][0] - r["s"][1]) < 0.5}
out = {}
for name, f in S.items():
    a = [r for r in R if f(r) and r["date"] < "2024-11-01"]; b = [r for r in R if f(r) and r["date"] >= "2024-11-01"]; al = a + b
    obs = lambda rr: [round(100 * sum(r["res"] == x for r in rr) / len(rr), 1) for x in range(3)]
    pre = lambda rr: [round(100 * float(np.mean([r["p"][x] for r in rr])), 1) for x in range(3)]
    fa = minimize(lambda q: nll(a, q[0], q[1]), [1.0, 0.0], method="Nelder-Mead").x
    fk = minimize(lambda q: nll(a, q[0], 0.0), [1.0], method="Nelder-Mead").x
    fall = minimize(lambda q: nll(al, q[0], q[1]), [1.0, 0.0], method="Nelder-Mead").x
    out[name] = {"n_2012_24": len(a), "n_test": len(b), "real_1X2_2012_24": obs(a), "previsto_1X2_2012_24": pre(a),
                 "real_1X2_test": obs(b) if b else None, "previsto_1X2_test": pre(b) if b else None,
                 "k_d_2012_24": [round(fa[0], 3), round(fa[1], 3)], "k_solo_2012_24": round(fk[0], 3),
                 "LL_test_base_modelo": round(nll(b, 1, 0), 4) if b else None, "LL_test_k_d": round(nll(b, fa[0], fa[1]), 4) if b else None,
                 "LL_test_k_solo": round(nll(b, fk[0], 0), 4) if b else None, "k_d_2012_26": [round(fall[0], 3), round(fall[1], 3)], "n_todo": len(al)}
    print(name, out[name], flush=True)
json.dump(out, open(os.path.join(BASE, "calc", "nat_home_draw.json"), "w"), indent=1)
