"""Factor de empates por liga española, elegido en validación y comprobado en prueba (fuera de muestra)."""
import importlib.util, json, math, sys
from datetime import date
import numpy as np
from scipy.stats import poisson
M, D = sys.argv[1], sys.argv[2]
spec = importlib.util.spec_from_file_location("em", M + "/euro_model.py"); em = importlib.util.module_from_spec(spec); spec.loader.exec_module(em)
ms = json.load(open(D))["matches"]
G = np.arange(11)
def lams(corte, fin, comps):
    tr = [m for m in ms if m["date"] < corte]; te = [m for m in ms if corte <= m["date"] < fin and m["competition"].split(":")[0] in comps]
    mod = em.EuroPoisson(xi=0.0015, ridge=10, scale=1.05, blend=0.2, hier=True).fit(tr, ref_date=date.fromisoformat(corte))
    out = []
    for m in te:
        if m["home"] in mod.idx and m["away"] in mod.idx:
            l, u = mod.rates(m["home"], m["away"])
            out.append((l, u, 0 if m["hg"] > m["ag"] else (1 if m["hg"] == m["ag"] else 2), m["competition"].split(":")[0]))
    return out
def ll(out, k, comp, extra_home=0.0):
    s = n = 0; x = 0
    for l, u, r, c in out:
        if c != comp: continue
        if extra_home: l, u = l * math.exp(extra_home), u * math.exp(-extra_home)
        Mx = np.outer(poisson.pmf(G, l), poisson.pmf(G, u)); Mx[np.diag_indices_from(Mx)] *= k; Mx /= Mx.sum()
        i, j = np.indices(Mx.shape); p = [Mx[i > j].sum(), Mx[i == j].sum(), Mx[i < j].sum()]
        s -= math.log(p[r]); x += p[1]; n += 1
    return s / n, 100 * x / n, n
ks = [0.85, 0.9, 0.95, 1.0, 1.04, 1.08, 1.12]
# dos cortes: validación con temporadas anteriores, prueba con la actual
val = lams("2025-09-01", "2026-07-01", {"es.1", "es.2"}); tes = lams("2026-07-01", "2026-11-02", {"es.1", "es.2"})
for comp in ("es.1", "es.2"):
    real_v = 100 * sum(r == 1 for *_, r, c in val if c == comp) / max(1, sum(c == comp for *_, c in val))
    real_t = 100 * sum(r == 1 for *_, r, c in tes if c == comp) / max(1, sum(c == comp for *_, c in tes))
    print(f"\n{comp}: X real validación {real_v:.1f}% · prueba {real_t:.1f}%")
    best = min(ks, key=lambda k: ll(val, k, comp)[0])
    for k in ks:
        a = ll(val, k, comp); b = ll(tes, k, comp)
        print(f"  factor {k:4.2f}: validación LL {a[0]:.4f} (X decl {a[1]:.1f}%, n={a[2]}) · prueba LL {b[0]:.4f} (X decl {b[1]:.1f}%, n={b[2]}){'  ← elegido en validación' if k == best else ''}")
