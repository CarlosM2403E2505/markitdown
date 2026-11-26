"""Efecto de jugar en Europa entre semana sobre el partido de liga siguiente.
Predicciones fuera de muestra (modelo reajustado cada mes con datos anteriores).
Se compara, para clubes con competición europea esa temporada, el residuo (real − esperado)
tras Europa frente al residuo de sus partidos de liga sin Europa en los 7 días previos."""
import importlib.util, json, math, sys, statistics as st
from datetime import date, timedelta
M, D, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
spec = importlib.util.spec_from_file_location("em", M + "/euro_model.py"); em = importlib.util.module_from_spec(spec); spec.loader.exec_module(em)
ms = json.load(open(D))["matches"]
UE = ("uefa.cl:", "uefa.el:", "uefa.conf:")
eur = {}  # equipo -> lista (fecha, competición)
for m in ms:
    if m["competition"].startswith(UE):
        for t in (m["home"], m["away"]): eur.setdefault(t, []).append((date.fromisoformat(m["date"]), m["competition"].split(":")[0]))
def temporada(d): return d.year if d.month >= 7 else d.year - 1
club_eur = {(t, temporada(f)) for t, l in eur.items() for f, _ in l}
cortes = []
d = date(2024, 9, 1)
while d < date(2026, 11, 6):
    cortes.append(d); d = date(d.year + (d.month == 12), d.month % 12 + 1, 1)
filas = []
for i, c in enumerate(cortes):
    fin = cortes[i + 1] if i + 1 < len(cortes) else date(2026, 11, 6)
    tr = [m for m in ms if date.fromisoformat(m["date"]) < c]
    te = [m for m in ms if c <= date.fromisoformat(m["date"]) < fin and not m["competition"].startswith("uefa")]
    mod = em.EuroPoisson(xi=0.0015, ridge=10, scale=1.05, blend=0.2, hier=True).fit(tr, ref_date=c)
    mod.draw_k = 1.08
    for m in te:
        if m["home"] not in mod.idx or m["away"] not in mod.idx: continue
        f = date.fromisoformat(m["date"])
        (p1, px, p2), lam, mu = mod.p1x2(m["home"], m["away"])
        for lado, t, xf, xc, gf, gc, pw, pl in (("local", m["home"], lam, mu, m["hg"], m["ag"], p1, p2), ("visitante", m["away"], mu, lam, m["ag"], m["hg"], p2, p1)):
            if (t, temporada(f)) not in club_eur: continue
            prev = [(g, comp) for g, comp in eur.get(t, []) if timedelta(0) < f - g <= timedelta(7)]
            dias, comp, dia_sem = None, None, None
            if prev:
                g, comp = max(prev); dias = (f - g).days; dia_sem = g.weekday()  # 0 lunes … 3 jueves
            pts = 3 if gf > gc else (1 if gf == gc else 0)
            filas.append({"liga": m["competition"].split(":")[0], "fecha": m["date"], "equipo": t, "lado": lado, "dias": dias, "comp": comp, "dia_sem": dia_sem,
                          "pts": pts, "pts_esp": 3 * pw + px, "gf": gf, "xf": xf, "gc": gc, "xc": xc, "fav": pw >= 0.5})
    print(c, len(filas), flush=True)
json.dump(filas, open(OUT, "w"))
