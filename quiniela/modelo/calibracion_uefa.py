"""¿Está bien calibrado el modelo en partidos UEFA (Champions, Europa League, Conference)?
Hilo «técnicas de IA y casas» (22/11/2026): las webs de predicción (PrediBall, Opta) dan a los
grandes favoritos de la J24 bastante más que la mesa (Real Madrid–PSV 82 % frente a 69 %).
Walk-forward mensual (sep. 2024 → nov. 2026), solo fase principal (sin previas), fuera de muestra.
Prueba temperatura T y factor de empate; elige con 2024-25 + 2025-26 y valida con 2026-27.
Uso (desde quiniela/): python3 modelo/calibracion_uefa.py  [--cache datos/calibracion_uefa.json]"""
import importlib.util, json, math, os, sys
from datetime import date
import numpy as np
from scipy.stats import poisson
R = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("em", os.path.join(R, "euro_model.py")); em = importlib.util.module_from_spec(spec); spec.loader.exec_module(em)
CACHE = os.path.join(R, "..", "datos", "calibracion_uefa.json")
COMPS = ("uefa.cl", "uefa.el", "uefa.conf")
G = np.arange(11)

def probs(l, u, draw=1.0, T=1.0):
    M = np.outer(poisson.pmf(G, l), poisson.pmf(G, u)); M[np.diag_indices_from(M)] *= draw; M /= M.sum()
    i, j = np.indices(M.shape); p = np.array([M[i > j].sum(), M[i == j].sum(), M[i < j].sum()])
    q = p ** T; return q / q.sum()

def construir():
    MS = json.load(open(os.path.join(R, "..", "datos", "euro_j23.json")))["matches"]
    meses = []; y, m = 2024, 9
    while (y, m) <= (2026, 12): meses.append(f"{y}-{m:02d}-01"); y, m = (y+1, 1) if m == 12 else (y, m+1)
    filas = []
    for a, b in zip(meses, meses[1:]):
        te = [x for x in MS if a <= x["date"] < b and x["competition"].split(":")[0] in COMPS]
        if not te: continue
        mod = em.EuroPoisson(xi=0.0015, ridge=10, scale=1.05, blend=0.2, hier=True).fit([x for x in MS if x["date"] < a], ref_date=date.fromisoformat(a))
        for x in te:
            if x["home"] in mod.idx and x["away"] in mod.idx:
                l, u = mod.rates(x["home"], x["away"])
                r = 0 if x["hg"] > x["ag"] else (1 if x["hg"] == x["ag"] else 2)
                filas.append({"l": l, "u": u, "r": r, "comp": x["competition"], "date": x["date"]})
        print(a, len(filas), file=sys.stderr, flush=True)
    json.dump(filas, open(CACHE, "w"))
    return filas

def ll(filas, draw, T):
    return float(np.mean([-math.log(probs(f["l"], f["u"], draw, T)[f["r"]]) for f in filas]))

if __name__ == "__main__":
    filas = json.load(open(CACHE)) if os.path.exists(CACHE) and "--rehacer" not in sys.argv else construir()
    ent = [f for f in filas if f["comp"].split(":")[1] in ("2024-25", "2025-26")]
    val = [f for f in filas if f["comp"].split(":")[1] == "2026-27"]
    print(f"Partidos: elegir {len(ent)} · validar {len(val)}")
    res = []
    for d in (0.9, 1.0, 1.08, 1.15):
        for T in (1.0, 1.05, 1.15, 1.25, 1.35, 1.5):
            res.append((ll(ent, d, T), ll(val, d, T), d, T))
    print(f"{'X':>5} {'T':>5} {'elegir':>8} {'validar':>8}")
    for e, v, d, T in sorted(res)[:10]: print(f"{d:5.2f} {T:5.2f} {e:8.4f} {v:8.4f}")
    e0, v0 = ll(ent, 1.0, 1.05), ll(val, 1.0, 1.05)
    print(f"Actual (X 1,0, T 1,05): elegir {e0:.4f} · validar {v0:.4f}")
    mejor = min(res); print(f"Mejor: X {mejor[2]} T {mejor[3]}")
    print("\nCalibración del favorito (actual → mejor), todos los partidos:")
    for lo, hi in ((0.33, 0.45), (0.45, 0.55), (0.55, 0.66), (0.66, 0.75), (0.75, 1.01)):
        sel = []; 
        for f in filas:
            p = probs(f["l"], f["u"], 1.0, 1.05); k = int(np.argmax(p))
            if lo <= p[k] < hi: sel.append((p[k], probs(f["l"], f["u"], mejor[2], mejor[3])[k], f["r"] == k))
        if sel: print(f"  {lo:.2f}-{hi:.2f} n={len(sel):4d} dada {np.mean([s[0] for s in sel]):.3f} → {np.mean([s[1] for s in sel]):.3f} · real {np.mean([s[2] for s in sel]):.3f}")
    xs = [f["r"] == 1 for f in filas]; px = [probs(f["l"], f["u"], 1.0, 1.05)[1] for f in filas]
    print(f"\nX real {np.mean(xs):.3f} · X dada {np.mean(px):.3f} (n={len(filas)})")
