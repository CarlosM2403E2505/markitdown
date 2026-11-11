"""Precios P10 y P15 con el modelo de selecciones -> nat_j21.json (mismo formato que las filas de j21_run.py).
Uso: python3 nat_price.py XI RIDGE WF DRAW_K BLEND(0|1) SALIDA.json"""
import importlib.util, json, math, os, sys, collections
from datetime import date
import numpy as np
from scipy.stats import poisson

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def imp(name, path):
    s = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
nm = imp("nm", os.path.join(BASE, "code", "nat_model.py"))
j16 = imp("j16", "/home/claude/j16_run.py")
xi, R, wf, dk, blend, outp = float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]), int(sys.argv[5]), sys.argv[6]
D = os.path.join(BASE, "dl_git", "international_results")
MS, NFIX = nm.load(os.path.join(D, "results.csv"), os.path.join(D, "goalscorers.csv"), "2006-01-01")
REF = date(2026, 11, 15)
# NAT_EXTRA: partidos posteriores al 6/10 que aun no esten en results.csv (p. ej. la jornada del jueves 12/11),
# una linea por partido: fecha,local,visitante,goles_local,goles_visitante,torneo,neutral(TRUE/FALSE)  (marcador a 90')
EXTRA = os.environ.get("NAT_EXTRA")
if EXTRA:
    known = {(m["date"], m["home"], m["away"]) for m in MS}
    for l in open(EXTRA, encoding="utf-8"):
        if l.startswith("#") or l.count(",") != 6: continue
        d, h, a, x, y, t, ne = [z.strip() for z in l.split(",")]
        if (d, h, a) in known: continue
        MS.append({"date": d, "home": h, "away": a, "hg": int(x), "ag": int(y), "t": t, "neutral": ne == "TRUE", "country": ""})
        print("NAT_EXTRA anadido:", d, h, x, "-", y, a)
mod = nm.NatPoisson(xi, R, wf).fit(MS, REF)
EMP = None
if blend:
    src = [m for m in MS if m["date"] >= "2012-01-01" and m["home"] in nm.UEFA and m["away"] in nm.UEFA and m["t"] in nm.COMPET_UEFA]
    EMP = {(i, j): 0.0 for i in range(4) for j in range(4)}
    for m in src: EMP[(min(m["hg"], 3), min(m["ag"], 3))] += 1 / len(src)
l2 = lambda v: "M" if v == 3 else str(v)
G = np.arange(11)
ur = sorted([u for u in nm.UEFA if u in mod.idx and mod.ngames[mod.idx[u]] >= 10], key=lambda u: -mod.strength(u))
out = {"_meta": {"modelo": "Poisson de selecciones (ataque/defensa por seleccion, ridge, decaimiento temporal, campo solo si neutral=False)",
                 "xi": xi, "ridge": R, "peso_amistoso": wf, "draw_k": dk, "mezcla_empirica_pleno": bool(blend),
                 "datos": "martj42/international_results results.csv (commit b0948cb, 31/10/2026), partidos 2006-01-01..2026-10-06, marcador a 90'",
                 "partidos": len(MS), "campo": round(math.exp(mod.h), 3), "convergencia": bool(mod.ok),
                 "top12_UEFA": [(u, round(mod.strength(u), 2)) for u in ur[:12]]}}
for n, h, a in ((10, "Belgium", "Italy"), (15, "Spain", "England")):
    lam, mu = mod.rates(h, a, neutral=False)
    p, cats, mk = j16.finish(lam, mu, EMP, dk)
    M = np.outer(poisson.pmf(G, lam), poisson.pmf(G, mu)); M[np.diag_indices_from(M)] *= dk; M /= M.sum()
    i, j = np.indices(M.shape)
    mk.update({"Menos 3.5": float(M[i + j <= 3].sum()), "Mas 1.5": float(M[i + j >= 2].sum()),
               "Local marca": float(M[i >= 1].sum()), "Visit marca": float(M[j >= 1].sum())})
    ng = [int(mod.ngames[mod.idx[h]]), int(mod.ngames[mod.idx[a]])]
    out[str(n)] = {"p": p, "xg": [lam, mu], "adj": [1.0, 1.0], "draw_k": dk,
                   "cats": {f"{l2(x)}-{l2(y)}": v for (x, y), v in cats.items()}, "mk": mk, "ng": ng}
    top = sorted(out[str(n)]["cats"].items(), key=lambda kv: -kv[1])[:6]
    print(f"P{n} {h}-{a}: lam {lam:.3f} mu {mu:.3f} | 1 {p[0]:.3f} X {p[1]:.3f} 2 {p[2]:.3f} | ng {ng} | rango UEFA {ur.index(h)+1},{ur.index(a)+1}")
    print("    pleno:", ", ".join(f"{k} {v:.1%}" for k, v in top), "|", {k: round(v, 3) for k, v in mk.items()})
json.dump(out, open(outp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
