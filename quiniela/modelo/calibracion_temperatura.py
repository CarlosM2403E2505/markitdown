"""Backtest: ¿mejora el log-loss elevar las probabilidades del modelo a una potencia T (T>1 = más rotundo)?
Se elige T en un periodo de validación y se confirma en otro posterior, sin cuotas."""
import importlib.util, json, math, sys
from datetime import date
M = sys.argv[1]; D = sys.argv[2]
spec = importlib.util.spec_from_file_location("em", M + "/euro_model.py"); em = importlib.util.module_from_spec(spec); spec.loader.exec_module(em)
ms = json.load(open(D))["matches"]
def preds(corte, fin):
    tr = [m for m in ms if m["date"] < corte]; te = [m for m in ms if corte <= m["date"] < fin]
    mod = em.EuroPoisson(xi=0.0015, ridge=10, scale=1.05, blend=0.2, hier=True).fit(tr, ref_date=date.fromisoformat(corte))
    out = []
    for m in te:
        if m["home"] not in mod.idx or m["away"] not in mod.idx: continue
        dk = 1.0 if m["competition"].startswith("uefa") else 1.08
        mod.draw_k = dk
        (p1, px, p2), _, _ = mod.p1x2(m["home"], m["away"])
        r = 0 if m["hg"] > m["ag"] else (1 if m["hg"] == m["ag"] else 2)
        out.append(((p1, px, p2), r, m["competition"]))
    return out
def ll(out, T, sel=lambda o: True):
    s = n = 0
    for p, r, c in out:
        if not sel((p, r, c)): continue
        q = [v ** T for v in p]; z = sum(q); s -= math.log(q[r] / z); n += 1
    return s / n, n
val = preds("2026-03-01", "2026-07-01"); tes = preds("2026-07-01", "2026-11-02")
Ts = [1.0, 1.05, 1.1, 1.15, 1.2, 1.25, 1.3, 1.4]
print("Validación (mar–jun 2026):", " ".join(f"T={T}:{ll(val,T)[0]:.4f}" for T in Ts), f"n={ll(val,1)[1]}")
best = min(Ts, key=lambda T: ll(val, T)[0]); print("T elegido en validación:", best)
print("Prueba (jul–oct 2026):   ", " ".join(f"T={T}:{ll(tes,T)[0]:.4f}" for T in Ts), f"n={ll(tes,1)[1]}")
fav = lambda o: max(o[0]) >= 0.5; uefa = lambda o: o[2].startswith("uefa"); es1 = lambda o: o[2].startswith("es.1")
for nom, f in (("favoritos ≥50 %", fav), ("copas UEFA", uefa), ("Primera", es1)):
    a, n = ll(tes, 1.0, f); b, _ = ll(tes, best, f); print(f"  {nom:<16} n={n:4d}  T=1: {a:.4f}  T={best}: {b:.4f}")
# calibración del favorito
for T in (1.0, best):
    for lo, hi in ((0.5, 0.6), (0.6, 0.7), (0.7, 0.8), (0.8, 1.0)):
        sel = [(p, r) for p, r, c in tes if lo <= max(p) < hi]
        if not sel: continue
        dec = sum(max([v ** T for v in p]) / sum(v ** T for v in p) for p, r in sel) / len(sel)
        real = sum(p.index(max(p)) == r for p, r in sel) / len(sel)
        print(f"  T={T} favorito {int(lo*100)}–{int(hi*100)} %: n={len(sel):4d} declarado {dec:.3f} real {real:.3f}")
