"""¿Conviene afilar más los favoritos claros? (hallazgo de la auditoría de ventaja: el modelo da 75 %
y ganan el 86 % cuando el favorito es muy claro). Walk-forward mensual, Primera y Segunda por separado.
Prueba una temperatura T que sube solo cuando el favorito supera un umbral; elige con 2022-24 y valida
con 2025-26. Uso: python3 modelo/calibracion_favoritos.py (desde quiniela/)."""
import importlib.util, json, math, os, sys
from datetime import date
import numpy as np
from scipy.stats import poisson
R = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("em", os.path.join(R, "euro_model.py")); em = importlib.util.module_from_spec(spec); spec.loader.exec_module(em)
MS = json.load(open(os.path.join(R, "..", "datos", "euro_j21.json")))["matches"]
G = np.arange(11); DRAW = {"es.1": 1.08, "es.2": 1.00}; HOME = {"es.1": 0.07, "es.2": 0.0}

def base_probs(l, u, comp):
    if HOME[comp]: l, u = l * math.exp(HOME[comp]), u * math.exp(-HOME[comp])
    M = np.outer(poisson.pmf(G, l), poisson.pmf(G, u)); M[np.diag_indices_from(M)] *= DRAW[comp]; M /= M.sum()
    i, j = np.indices(M.shape); return np.array([M[i > j].sum(), M[i == j].sum(), M[i < j].sum()])

def afinar(p, T): q = p ** T; return q / q.sum()

def afinar_fav(p, T_base, T_fav, umbral):
    T = T_fav if max(p) >= umbral else T_base
    return afinar(p, T)

def construir():
    filas = []
    y, m = 2022, 1; meses = []
    while (y, m) <= (2026, 12): meses.append(f"{y}-{m:02d}-01"); y, m = (y+1,1) if m==12 else (y,m+1)
    for a, b in zip(meses, meses[1:]):
        te = [x for x in MS if a <= x["date"] < b and x["competition"].split(":")[0] in DRAW]
        if not te: continue
        mod = em.EuroPoisson(xi=0.0015, ridge=10, scale=1.05, blend=0.2, hier=True).fit([x for x in MS if x["date"] < a], ref_date=date.fromisoformat(a))
        for x in te:
            if x["home"] in mod.idx and x["away"] in mod.idx:
                l, u = mod.rates(x["home"], x["away"]); c = x["competition"].split(":")[0]
                r = 0 if x["hg"] > x["ag"] else (1 if x["hg"] == x["ag"] else 2)
                filas.append({"p": base_probs(l, u, c).tolist(), "r": r, "comp": c, "date": x["date"]})
        print(a, len(filas), file=sys.stderr)
    return filas

def ll(filas, fn): return float(np.mean([-math.log(max(fn(np.array(f["p"]))[f["r"]], 1e-12)) for f in filas]))

def main():
    filas = construir()
    for comp in ("es.1", "es.2"):
        val = [f for f in filas if f["comp"] == comp and f["date"] < "2025-07-01"]
        tes = [f for f in filas if f["comp"] == comp and f["date"] >= "2025-07-01"]
        print(f"\n=== {comp}  validación n={len(val)}  prueba n={len(tes)}")
        print(f"  actual (T=1,05):            validación {ll(val, lambda p: afinar(p,1.05)):.4f}  prueba {ll(tes, lambda p: afinar(p,1.05)):.4f}")
        for T in (1.10, 1.15, 1.20, 1.30):
            print(f"  T global {T:.2f}:             validación {ll(val, lambda p,T=T: afinar(p,T)):.4f}  prueba {ll(tes, lambda p,T=T: afinar(p,T)):.4f}")
        best = None
        for Tf in (1.2, 1.4, 1.6, 1.8, 2.0):
            for um in (0.55, 0.60, 0.66):
                v = ll(val, lambda p,Tf=Tf,um=um: afinar_fav(p,1.05,Tf,um))
                if best is None or v < best[0]: best = (v, Tf, um)
        Tf, um = best[1], best[2]
        print(f"  favoritos T={Tf} si fav>={um}:  validación {ll(val, lambda p: afinar_fav(p,1.05,Tf,um)):.4f}  prueba {ll(tes, lambda p: afinar_fav(p,1.05,Tf,um)):.4f}  [elegido en validación]")
        # calibración del tramo alto antes/después en prueba
        hi = [f for f in tes if max(f["p"]) >= um]
        real = 100*np.mean([int(np.argmax(f["p"]))==f["r"] for f in hi])
        da = 100*np.mean([max(afinar(np.array(f["p"]),1.05)) for f in hi])
        df = 100*np.mean([max(afinar_fav(np.array(f["p"]),1.05,Tf,um)) for f in hi])
        print(f"  tramo fav>={um} (prueba, n={len(hi)}): real {real:.1f}% · daba {da:.1f}% · afinado {df:.1f}%")

if __name__ == "__main__":
    main()
