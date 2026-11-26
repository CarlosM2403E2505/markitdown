"""¿Cuándo falla un favorito claro? (22/11/2026, caso Rayo 0-1 Valencia, J23). Primera y Segunda, jul. 2024 - nov. 2026,
probabilidades de la mesa fuera de muestra (las de x_templados.py, con la X templada). Favorito = máx(p) entre 45 y 70 %
(cuota ~1,45-2,20). Para cada situación se compara lo que la mesa daba con lo que pasó. Una situación solo se vuelve
regla si falla de más en 2024-25 (selección) Y en 2025-27 (validación), y se mide el log-loss.
Uso: TMPDIR=<carpeta con x_templados_filas.pkl> python3 modelo/favoritos_fallan.py → datos/favoritos_fallan.json"""
import json, math, os, sys, contextlib, io
from bisect import bisect_left
from collections import defaultdict
from datetime import date
import numpy as np
R = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(R, "x_templados.py"), encoding="utf-8").read().split("P = [(f, base(f))")[0]
ns = {"__file__": os.path.join(R, "x_templados.py")}
with contextlib.redirect_stderr(io.StringIO()): exec(src, ns)
filas, base, con_x, MS, temporada = ns["filas"], ns["base"], ns["con_x"], ns["MS"], ns["temporada"]
uefa = defaultdict(list); liga = defaultdict(list)
for m in MS:
    d = m["date"]
    if m["competition"].startswith("uefa."):
        uefa[m["home"]].append(d); uefa[m["away"]].append(d)
    elif m["competition"][:4] in ("es.1", "es.2"):
        r = 3 if m["hg"] > m["ag"] else (1 if m["hg"] == m["ag"] else 0)
        liga[m["home"]].append((d, r)); liga[m["away"]].append((d, 3 - r if r != 1 else 1))
for k in uefa: uefa[k].sort()
for k in liga: liga[k].sort()
def dias(a, b): return (date.fromisoformat(b) - date.fromisoformat(a)).days
def uefa_antes(t, d):  # días desde su último partido UEFA (None si > 10)
    xs = uefa.get(t, []); i = bisect_left(xs, d) - 1
    return dias(xs[i], d) if i >= 0 and dias(xs[i], d) <= 10 else None
def uefa_despues(t, d):
    xs = uefa.get(t, []); i = bisect_left(xs, d)
    while i < len(xs) and xs[i] <= d: i += 1
    return dias(d, xs[i]) if i < len(xs) and dias(d, xs[i]) <= 5 else None
def forma(t, d, n=5):
    xs = [r for dd, r in liga.get(t, []) if dd < d][-n:]
    return sum(xs) / (3 * len(xs)) if len(xs) == n else None
# encontrar equipos por fila: filas = (comp, l, u, r, date, eh, ea) no lleva nombres → se recuperan de MS
idx = {}
for m in MS:
    if m["competition"][:4] in ("es.1", "es.2"): idx.setdefault((m["date"], m["competition"][:4]), []).append(m)
F = []
for f in filas:
    if f[4] < "2024-07-01": continue
    p = base(f)
    if f[0] == "es.1": p = con_x(p, 0.45, 0.60, 1.20)
    fav = int(np.argmax(p)); pf = float(p[fav])
    if not (0.45 <= pf < 0.70) or fav == 1: continue
    # emparejar partido por fecha, competición y resultado (las λ no identifican; se toma el que coincide en resultado y orden)
    F.append({"f": f, "p": [float(v) for v in p], "fav": fav, "pf": pf})
# emparejar en orden: filas y MS del mismo día/competición siguen el mismo orden de inserción
pos = defaultdict(int)
for x in F: pass
cand = defaultdict(list)
for f in filas:
    cand[(f[4], f[0])].append(f)
mapa = {}
for k, fs in cand.items():
    ms = [m for m in idx.get(k, [])]
    ms = [m for m in ms if True]
    if len(ms) >= len(fs):
        # filas se crearon filtrando equipos sin índice; se emparejan por resultado en orden
        j = 0
        for f in fs:
            while j < len(ms):
                m = ms[j]; j += 1
                r = 0 if m["hg"] > m["ag"] else (1 if m["hg"] == m["ag"] else 2)
                if r == f[3]: mapa[id(f)] = m; break
rasgos = {
    "favorito local": lambda x, m, h, a: x["fav"] == 0,
    "favorito visitante": lambda x, m, h, a: x["fav"] == 2,
    "favorito jugó UEFA hace ≤ 4 días": lambda x, m, h, a: (uefa_antes(h if x["fav"] == 0 else a, m["date"]) or 99) <= 4,
    "favorito juega UEFA en ≤ 4 días": lambda x, m, h, a: (uefa_despues(h if x["fav"] == 0 else a, m["date"]) or 99) <= 4,
    "favorito europeo y rival no (EURO_F)": lambda x, m, h, a: (x["f"][5] and not x["f"][6]) if x["fav"] == 0 else (x["f"][6] and not x["f"][5]),
    "favorito en mala forma (≤ 5 puntos de 15)": lambda x, m, h, a: (forma(h if x["fav"] == 0 else a, m["date"]) or 1) <= 5 / 15,
    "rival en buena forma (≥ 10 puntos de 15)": lambda x, m, h, a: (forma(a if x["fav"] == 0 else h, m["date"]) or 0) >= 10 / 15,
    "favorito templado (45-55 %)": lambda x, m, h, a: x["pf"] < 0.55,
    "Primera": lambda x, m, h, a: x["f"][0] == "es.1",
    "Segunda": lambda x, m, h, a: x["f"][0] == "es.2",
}
out = {"n": 0, "rasgos": {}}
tabla = defaultdict(lambda: {"sel": [], "val": []})
for x in F:
    m = mapa.get(id(x["f"]))
    if not m: continue
    out["n"] += 1
    gana = x["f"][3] == x["fav"]
    parte = "sel" if temporada(x["f"][4]) == "2024-25" else "val"
    for nom, fn in rasgos.items():
        try: ok = fn(x, m, m["home"], m["away"])
        except Exception: ok = False
        if ok: tabla[nom][parte].append((x["pf"], gana, x["p"][1], x["f"][3] == 1))
for nom in rasgos:
    r = {}
    for parte in ("sel", "val"):
        v = tabla[nom][parte]
        if v:
            dab = np.mean([a for a, *_ in v]); gan = np.mean([b for _, b, *_ in v]); se = math.sqrt(dab * (1 - dab) / len(v))
            r[parte] = {"n": len(v), "daba": round(float(dab), 3), "gano": round(float(gan), 3), "z": round(float((gan - dab) / se), 2),
                        "daba_X": round(float(np.mean([c for *_, c, _ in v])), 3), "salio_X": round(float(np.mean([d for *_, d in v])), 3)}
    out["rasgos"][nom] = r
json.dump(out, open(os.path.join(R, "..", "datos", "favoritos_fallan.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("partidos con favorito 45-70 %:", out["n"])
for nom, r in out["rasgos"].items():
    print(f"{nom:42s}", "  ".join(f"{k}: n={v['n']} daba {100*v['daba']:.0f} ganó {100*v['gano']:.0f} (z {v['z']:+.1f}) X {100*v['daba_X']:.0f}→{100*v['salio_X']:.0f}" for k, v in r.items()))
