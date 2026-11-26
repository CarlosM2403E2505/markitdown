"""Validacion final + factor de empates + precios P10/P15 -> nat_j21.json (formato de j16.finish, como j21_run.py).
Uso: python3 nat_build.py   (lee calc/nat_long.pkl, escribe nat_j21.json y calc/nat_validacion.json)"""
import importlib.util, json, math, os, pickle, collections
from datetime import date
import numpy as np
from scipy.stats import poisson
from scipy.optimize import minimize_scalar

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def imp(name, path):
    s = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
nm = imp("nm", os.path.join(BASE, "code", "nat_model.py"))
j16 = imp("j16", "/home/claude/j16_run.py")
D = os.path.join(BASE, "dl_git", "international_results")
MS, NFIX = nm.load(os.path.join(D, "results.csv"), os.path.join(D, "goalscorers.csv"), "2006-01-01")
L = pickle.load(open(os.path.join(BASE, "calc", "nat_long.pkl"), "rb"))
CFG, ROWS = L["cfg"], L["rows"]
CUT = "2024-11-01"
V = {"cfg": {"xi": CFG[0], "ridge": CFG[1], "peso_amistoso": CFG[2]}, "corregidos_a_90": NFIX}


def pk(r, k):
    p1, px, p2 = r["p"]; z = p1 + k * px + p2
    return p1 / z, k * px / z, p2 / z


def ll(rows, k=1.0):
    return -sum(math.log(max(pk(r, k)[r["res"]], 1e-12)) for r in rows) / max(len(rows), 1)


def khat(rows):
    f = lambda k: ll(rows, k) * len(rows)
    o = minimize_scalar(f, bounds=(0.4, 2.5), method="bounded"); k0 = o.x; f0 = o.fun
    grid = np.linspace(0.4, 2.5, 841); ok = [k for k in grid if 2 * (f(k) - f0) <= 3.84]
    return k0, (min(ok), max(ok))


# ---------- tasa base (frecuencias 1X2 de los partidos anteriores al corte, por campo/neutral)
def base_from(ms):
    c = {True: collections.Counter(), False: collections.Counter()}
    for m in ms:
        c[m["neutral"]][0 if m["hg"] > m["ag"] else 1 if m["hg"] == m["ag"] else 2] += 1
    return {k: [v[i] / sum(v.values()) for i in range(3)] for k, v in c.items()}
BASE_P = base_from([m for m in MS if "2012-01-01" <= m["date"] < CUT])
def ll_base(rows):
    return -sum(math.log(BASE_P[r["neutral"]][r["res"]]) for r in rows) / max(len(rows), 1)

comp = lambda r: r["t"] in nm.COMPET_UEFA and r["uefa2"]
test = [r for r in ROWS if r["date"] >= CUT]; pre = [r for r in ROWS if r["date"] < CUT]
subs = {"todos": lambda r: True, "UEFA_vs_UEFA": lambda r: r["uefa2"], "UEFA_oficial": comp,
        "UEFA_oficial_no_neutral": lambda r: comp(r) and not r["neutral"],
        "UEFA_oficial_top16_ambos": lambda r: comp(r) and max(r["rk"]) <= 16,
        "UEFA_oficial_igualado(|P1-P2|<0,15)": lambda r: comp(r) and abs(r["p"][0] - r["p"][2]) < 0.15}
V["validacion_test_2024-11_a_2026-10"] = {}
for name, f in subs.items():
    t = [r for r in test if f(r)]
    if not t: continue
    V["validacion_test_2024-11_a_2026-10"][name] = {"n": len(t), "LL_modelo": round(ll(t), 4), "LL_tasa_base": round(ll_base(t), 4),
        "mejora_%": round(100 * (1 - ll(t) / ll_base(t)), 1), "X_real_%": round(100 * sum(r["res"] == 1 for r in t) / len(t), 1),
        "X_prevista_%": round(100 * np.mean([r["p"][1] for r in t]), 1),
        "1_real_%": round(100 * sum(r["res"] == 0 for r in t) / len(t), 1), "1_previsto_%": round(100 * np.mean([r["p"][0] for r in t]), 1)}
    print("validacion", name, V["validacion_test_2024-11_a_2026-10"][name])

# ---------- factor de empates: estimado en 2012-01..2024-10 (fuera de muestra del ajuste de fuerzas), comprobado en 2024-11..2026-10
dsubs = {"todos": subs["todos"], "UEFA_oficial": comp, "UEFA_oficial_igualado(|P1-P2|<0,15)": subs["UEFA_oficial_igualado(|P1-P2|<0,15)"],
         "UEFA_oficial_top16_ambos": subs["UEFA_oficial_top16_ambos"],
         "UEFA_oficial_top16_ambos_sin_neutral": lambda r: comp(r) and max(r["rk"]) <= 16 and not r["neutral"],
         "UEFA_oficial_top24_ambos": lambda r: comp(r) and max(r["rk"]) <= 24,
         "UEFA_NationsLeague_fase_liga(sep-nov)": lambda r: r["uefa2"] and r["t"] == "UEFA Nations League" and r["month"] in (9, 10, 11)}
V["factor_empates"] = {}
for name, f in dsubs.items():
    a = [r for r in pre if f(r)]; b = [r for r in test if f(r)]; al = a + b
    k_a, ci_a = khat(a); k_all, ci_all = khat(al)
    V["factor_empates"][name] = {
        "n_2012_2024": len(a), "X_real_%": round(100 * sum(r["res"] == 1 for r in a) / len(a), 1), "X_prevista_k1_%": round(100 * np.mean([r["p"][1] for r in a]), 1),
        "k_2012_2024": round(k_a, 3), "IC95_k": [round(ci_a[0], 2), round(ci_a[1], 2)],
        "n_test": len(b), "X_real_test_%": round(100 * sum(r["res"] == 1 for r in b) / max(len(b), 1), 1),
        "X_prevista_test_k1_%": round(100 * np.mean([r["p"][1] for r in b]), 1) if b else None,
        "LL_test_k1": round(ll(b), 4) if b else None, "LL_test_k_estimado": round(ll(b, k_a), 4) if b else None,
        "k_todo_2012_2026": round(k_all, 3), "IC95_todo": [round(ci_all[0], 2), round(ci_all[1], 2)], "n_todo": len(al)}
    print(name, V["factor_empates"][name])

# ---------- Pleno: categorias 0/1/2/M. Modelo puro frente a mezcla 0,8/0,2 con la empirica (como j16.finish con emp)
EMP = {(i, j): 0.0 for i in range(4) for j in range(4)}
emp_src = [m for m in MS if "2012-01-01" <= m["date"] < CUT and m["home"] in nm.UEFA and m["away"] in nm.UEFA and m["t"] in nm.COMPET_UEFA]
for m in emp_src:
    EMP[(min(m["hg"], 3), min(m["ag"], 3))] += 1 / len(emp_src)

def cats_ll(rows, k, blend):
    s = 0
    for r in rows:
        _, cats, _ = j16.finish(r["lam"], r["mu"], None, k)   # matriz 11x11 con la diagonal x k, agrupada en 0/1/2/M
        p = (1 - blend) * cats[r["cat"]] + blend * EMP[r["cat"]]
        s -= math.log(max(p, 1e-12))
    return s / len(rows)

def k_for_match():
    return V["factor_empates"]["UEFA_oficial_top16_ambos"]

tc = [r for r in test if comp(r)]
emp_ll = -sum(math.log(EMP[r["cat"]]) for r in tc) / len(tc)
V["pleno_test_UEFA_oficial"] = {"n": len(tc), "LL_modelo": round(cats_ll(tc, 1.0, 0.0), 4), "LL_mezcla_0.2": round(cats_ll(tc, 1.0, 0.2), 4),
                                "LL_solo_empirica": round(emp_ll, 4)}
print("pleno", V["pleno_test_UEFA_oficial"])
json.dump(V, open(os.path.join(BASE, "calc", "nat_validacion.json"), "w"), ensure_ascii=False, indent=1)
