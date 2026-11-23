#!/usr/bin/env python3
"""Después de j24_run.py: añade a jornadas/j24/j24.json lo que el modelo no pone.
- forma_favorito (0-15): puntos del favorito en sus 5 últimos de liga nacional (datos/euro_j24.json).
- mercado (1X2 sin margen) desde la foto de cuotas más reciente jornadas/j24/cuotas_*.json (solo aviso, R5).
- publico: % LAE más reciente (jornadas/j24/publico_*.json), solo informativo (R5).
- pleno.mercado_1x2, pleno.mercado_cats y pleno.mercado_pleno (marcador del Pleno según las casas).
Luego: python3 herramientas/reglas_mesa.py jornadas/j24/j24.json --guardar
"""
import glob, json, os
Q = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(Q, "jornadas", "j24", "j24.json")
d = json.load(open(P, encoding="utf-8"))
ms = json.load(open(os.path.join(Q, "datos", "euro_j24.json"), encoding="utf-8"))["matches"]
fx = {x["n"]: x for x in json.load(open(os.path.join(Q, "jornadas", "j24", "j24_fx.json"), encoding="utf-8"))["fixtures"]}
for r in d["partidos"]:
    x, p = fx[r["n"]], r["p"]
    t = x["home"] if p[0] >= p[2] else x["away"]
    L = sorted([m for m in ms if t in (m["home"], m["away"]) and not m["competition"].startswith("uefa")], key=lambda m: m["date"])[-5:]
    pts = 0
    for m in L:
        g, o = (m["hg"], m["ag"]) if m["home"] == t else (m["ag"], m["hg"])
        pts += 3 if g > o else 1 if g == o else 0
    r["forma_favorito"] = pts
fotos = sorted(glob.glob(os.path.join(Q, "jornadas", "j24", "cuotas_*.json")))
if fotos:
    c = json.load(open(fotos[-1], encoding="utf-8"))
    sinmargen = lambda q: [round((1 / v) / sum(1 / w for w in q), 4) for v in q]
    for r in d["partidos"]:
        q = c["cuotas"].get(str(r["n"]))
        if q: r["mercado"] = sinmargen(q); r["mercado_fuente"] = c["fuente"]
    pl = d["pleno"]
    if c["cuotas"].get("15"): pl["mercado_1x2"] = sinmargen(c["cuotas"]["15"])
    if c.get("marcador_15"):
        inv = {k: 1 / v for k, v in c["marcador_15"].items()}; s = sum(inv.values())
        cat = lambda g: "M" if g >= 3 else str(g)
        agg = {}
        for k, v in inv.items():
            a, b = map(int, k.split(":")); key = f"{cat(a)}-{cat(b)}"; agg[key] = agg.get(key, 0) + v / s
        pl["mercado_cats"] = {k: round(v, 4) for k, v in sorted(agg.items(), key=lambda kv: -kv[1])}
        top = max(pl["cats"], key=pl["cats"].get)
        pl["mercado_pleno"] = pl["mercado_cats"].get(top)
pubs = sorted(glob.glob(os.path.join(Q, "jornadas", "j24", "publico_*.json")))
if pubs: d["publico"] = json.load(open(pubs[-1], encoding="utf-8"))
json.dump(d, open(P, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("forma:", {r["n"]: r["forma_favorito"] for r in d["partidos"]}, "| mercado:", sum(1 for r in d["partidos"] if r.get("mercado")), "partidos")
