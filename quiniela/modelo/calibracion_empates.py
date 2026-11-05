"""¿Falla el modelo en los empates? Calibración de P(X) fuera de muestra, por competición,
con T=1, con T=1,05 y con T=1,05 aplicado solo al reparto 1/2 (sin tocar la X)."""
import importlib.util, json, math, sys
from datetime import date
M, D = sys.argv[1], sys.argv[2]
spec = importlib.util.spec_from_file_location("em", M + "/euro_model.py"); em = importlib.util.module_from_spec(spec); spec.loader.exec_module(em)
ms = json.load(open(D))["matches"]
def preds(corte, fin):
    tr = [m for m in ms if m["date"] < corte]; te = [m for m in ms if corte <= m["date"] < fin]
    mod = em.EuroPoisson(xi=0.0015, ridge=10, scale=1.05, blend=0.2, hier=True).fit(tr, ref_date=date.fromisoformat(corte))
    out = []
    for m in te:
        if m["home"] not in mod.idx or m["away"] not in mod.idx: continue
        comp = m["competition"].split(":")[0]
        mod.draw_k = 1.0 if comp.startswith("uefa") else 1.08
        (p1, px, p2), _, _ = mod.p1x2(m["home"], m["away"])
        r = 0 if m["hg"] > m["ag"] else (1 if m["hg"] == m["ag"] else 2)
        out.append(([p1, px, p2], r, comp))
    return out
def T_full(p, T): q = [v ** T for v in p]; z = sum(q); return [v / z for v in q]
def T_12(p, T):
    a, b = p[0] ** T, p[2] ** T; s = (p[0] + p[2]) / (a + b); return [a * s, p[1], b * s]
variantes = {"T=1": lambda p: p, "T=1,05": lambda p: T_full(p, 1.05), "T=1,05 sin tocar X": lambda p: T_12(p, 1.05)}
for nom, (c, f) in {"validación mar–jun": ("2026-03-01", "2026-07-01"), "prueba jul–oct": ("2026-07-01", "2026-11-02")}.items():
    out = preds(c, f)
    print(f"\n=== {nom}: {len(out)} partidos ===")
    grupos = {"todo": lambda c: True, "copas UEFA": lambda c: c.startswith("uefa"), "Primera": lambda c: c == "es.1", "Segunda": lambda c: c == "es.2", "otras ligas": lambda c: not c.startswith(("uefa", "es."))}
    for g, sel in grupos.items():
        sub = [o for o in out if sel(o[2])]
        if not sub: continue
        lin = f"  {g:<12} n={len(sub):4d} X real {100*sum(r==1 for _,r,_ in sub)/len(sub):4.1f}%"
        for vn, fn in variantes.items():
            q = [fn(p) for p, _, _ in sub]
            ll = -sum(math.log(qq[r]) for qq, (_, r, _) in zip(q, sub)) / len(sub)
            lin += f" | {vn}: X decl {100*sum(qq[1] for qq in q)/len(sub):4.1f}% LL {ll:.4f}"
        print(lin)
    print("  Calibración de la X (T=1): tramo de P(X) → declarado / real")
    for lo, hi in ((0, .2), (.2, .24), (.24, .28), (.28, .32), (.32, 1)):
        sub = [(p, r) for p, r, _ in out if lo <= p[1] < hi]
        if sub: print(f"    {int(lo*100):2d}–{int(hi*100):3d} %: n={len(sub):4d}  {100*sum(p[1] for p,_ in sub)/len(sub):4.1f}% / {100*sum(r==1 for _,r in sub)/len(sub):4.1f}%")
    # ¿la X fue alguna vez el signo más probable? ¿y cuántos empates salen en partidos «igualados»?
    ig = [(p, r) for p, r, _ in out if abs(p[0] - p[2]) < 0.10]
    print(f"  Partidos igualados (|P1−P2| < 10 puntos): n={len(ig)}, X declarado {100*sum(p[1] for p,_ in ig)/len(ig):.1f}%, real {100*sum(r==1 for _,r in ig)/len(ig):.1f}%")
    print(f"  Partidos donde la X es el signo más probable: {sum(p[1]==max(p) for p,_,_ in out)} de {len(out)}")
