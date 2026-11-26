"""Revisión tras la J23 (22/11/2026): ¿sobreestima la mesa a los favoritos de Primera?
Walk-forward mensual de Primera 2022-26 (mismo esquema que pendientes_primera.py).
Mide, fuera de muestra: (1) log-loss por temporada con y sin EURO_F 1,12 y con T 1,00/1,08/1,15;
(2) calibración del favorito y de la X con el modelo vigente (T 1,15 + EURO_F 1,12).
Uso: python3 modelo/revision_j23.py  → datos/revision_j23.json"""
import importlib.util, json, math, os, sys
from collections import defaultdict
from datetime import date
import numpy as np
R = os.path.dirname(os.path.abspath(__file__))
s = importlib.util.spec_from_file_location("pp0", os.path.join(R, "pendientes_primera.py"))
# reutiliza probs() y europa() sin relanzar su bucle: se copia lo mínimo
src = open(os.path.join(R, "pendientes_primera.py"), encoding="utf-8").read().split("filas = []")[0]
ns = {"__file__": os.path.join(R, "pendientes_primera.py")}; exec(src, ns)
em, MS, probs, europa = ns["em"], ns["MS"], ns["probs"], ns["europa"]
filas = []
y, m = 2022, 1; meses = []
while (y, m) <= (2026, 12): meses.append(f"{y}-{m:02d}-01"); y, m = (y+1, 1) if m == 12 else (y, m+1)
for a, b in zip(meses, meses[1:]):
    te = [x for x in MS if a <= x["date"] < b and x["competition"].startswith("es.1")]
    if not te: continue
    mod = em.EuroPoisson(xi=0.0015, ridge=10, scale=1.05, blend=0.2, hier=True).fit([x for x in MS if x["date"] < a], ref_date=date.fromisoformat(a))
    for x in te:
        if x["home"] in mod.idx and x["away"] in mod.idx:
            l, u = mod.rates(x["home"], x["away"])
            r = 0 if x["hg"] > x["ag"] else (1 if x["hg"] == x["ag"] else 2)
            filas.append((l, u, r, x["date"], europa(x["home"], x["date"]), europa(x["away"], x["date"])))
    print(a, len(filas), file=sys.stderr)

def pr(f, ef=1.12, T=1.15):
    l, u = f[0], f[1]
    if f[4] and not f[5]: l *= ef
    if f[5] and not f[4]: u *= ef
    return probs(l, u, T=T)
def temporada(d): y, m = int(d[:4]), int(d[5:7]); return f"{y}-{(y+1)%100:02d}" if m >= 7 else f"{y-1}-{y%100:02d}"
ll = lambda sub, fn: float(np.mean([-math.log(max(fn(f)[f[2]], 1e-12)) for f in sub]))
out = {"n": len(filas), "temporadas": {}, "calibracion_favorito": [], "calibracion_x": [], "euro_f_solo": {}}
por = defaultdict(list)
for f in filas: por[temporada(f[3])].append(f)
variantes = {"vigente (T1,15+EURO_F1,12)": lambda f: pr(f), "sin EURO_F": lambda f: pr(f, ef=1.0),
             "T 1,08": lambda f: pr(f, T=1.08), "T 1,00": lambda f: pr(f, T=1.0), "T1,00 sin EURO_F": lambda f: pr(f, ef=1.0, T=1.0)}
for t, sub in sorted(por.items()) + [("total", filas)]:
    out["temporadas"][t] = {"n": len(sub), **{k: round(ll(sub, fn), 4) for k, fn in variantes.items()}}
# solo partidos con un equipo europeo
uno = [f for f in filas if f[4] != f[5]]
out["euro_f_solo"] = {"n": len(uno), **{k: round(ll(uno, fn), 4) for k, fn in variantes.items()}}
# el europeo es el local favorito (caso Rayo)
loc = [f for f in filas if f[4] and not f[5] and pr(f)[0] >= 0.45]
out["europeo_local_favorito"] = {"n": len(loc), "daba_1": round(float(np.mean([pr(f)[0] for f in loc])), 3),
    "salio_1": round(float(np.mean([f[2] == 0 for f in loc])), 3), "daba_X": round(float(np.mean([pr(f)[1] for f in loc])), 3),
    "salio_X": round(float(np.mean([f[2] == 1 for f in loc])), 3), "sin_EURO_F_daba_1": round(float(np.mean([pr(f, ef=1.0)[0] for f in loc])), 3)}
for lo, hi in [(0.33, 0.45), (0.45, 0.55), (0.55, 0.65), (0.65, 0.75), (0.75, 1.0)]:
    sub = [(pr(f), f) for f in filas if lo <= max(pr(f)) < hi]
    if sub:
        out["calibracion_favorito"].append({"tramo": f"{int(lo*100)}-{int(hi*100)} %", "n": len(sub),
            "daba": round(float(np.mean([max(p) for p, _ in sub])), 3), "gano": round(float(np.mean([int(np.argmax(p)) == f[2] for p, f in sub])), 3),
            "daba_X": round(float(np.mean([p[1] for p, _ in sub])), 3), "salio_X": round(float(np.mean([f[2] == 1 for _, f in sub])), 3)})
json.dump(out, open(os.path.join(R, "..", "datos", "revision_j23.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps(out, ensure_ascii=False, indent=1))
