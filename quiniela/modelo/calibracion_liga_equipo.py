"""Backtest: liga de cada equipo por «más partidos en 365 días» (actual) o por «liga de su último partido de liga» (corrección)."""
import importlib.util, json, math, sys
from datetime import date
M, D = sys.argv[1], sys.argv[2]
spec = importlib.util.spec_from_file_location("em", M + "/euro_model.py"); em = importlib.util.module_from_spec(spec); spec.loader.exec_module(em)
ms = json.load(open(D))["matches"]
original = em.team_leagues
def ultima_liga(matches):
    ult = {}
    for m in matches:
        comp = m["competition"].split(":")[0]
        if comp.startswith("uefa"): continue
        for t in (m["home"], m["away"]):
            if m["date"] >= ult.get(t, ("", ""))[0]: ult[t] = (m["date"], comp)
    return {t: c for t, (_, c) in ult.items()}
cortes = [date(2025, 8, 1), date(2025, 9, 1), date(2025, 10, 1), date(2025, 11, 1), date(2026, 8, 1), date(2026, 9, 1), date(2026, 10, 1), date(2026, 11, 1), date(2026, 11, 10)]
res = {"actual": [], "corregida": []}
for nombre, fn in (("actual", original), ("corregida", ultima_liga)):
    em.team_leagues = fn
    for c, f in zip(cortes, cortes[1:]):
        if c.month == 11 and c.year == 2025: continue  # solo inicios de temporada: ago–oct 2025 y ago–nov 2026
        tr = [m for m in ms if date.fromisoformat(m["date"]) < c]
        te = [m for m in ms if c <= date.fromisoformat(m["date"]) < f and not m["competition"].startswith("uefa")]
        mod = em.EuroPoisson(xi=0.0015, ridge=10, scale=1.05, blend=0.2, hier=True).fit(tr, ref_date=c)
        for m in te:
            if m["home"] not in mod.idx or m["away"] not in mod.idx: continue
            comp = m["competition"].split(":")[0]
            mod.draw_k = 1.0 if comp == "es.2" else 1.08
            (p1, px, p2), _, _ = mod.p1x2(m["home"], m["away"])
            r = 0 if m["hg"] > m["ag"] else (1 if m["hg"] == m["ag"] else 2)
            res[nombre].append((comp, m["home"], m["away"], -math.log([p1, px, p2][r])))
em.team_leagues = original
cambiados = set()
for cut in (date(2025, 8, 1), date(2026, 8, 1), date(2026, 11, 10)):
    tr = [m for m in ms if date.fromisoformat(m["date"]) < cut]
    a, b = original(tr), ultima_liga(tr)
    cambiados |= {t for t in b if a.get(t) != b[t]}
ES_CAMB = {"girona","real oviedo","mallorca","racing santander","deportivo coruna","malaga","real valladolid","las palmas","leganes","levante","elche","espanyol barcelona","cordoba","almeria","granada","eibar","tenerife","burgos","cadiz","huesca","albacete","castellon","andorra","ad ceuta","real sociedad b","sabadell","celta fortuna","sporting gijon","eldense","racing ferrol","mirandes","zaragoza"}
grupos = [("Primera", lambda r: r[0] == "es.1"), ("Segunda", lambda r: r[0] == "es.2"),
          ("España, con equipo que cambió de liga", lambda r: r[0] in ("es.1","es.2") and (r[1] in cambiados or r[2] in cambiados)),
          ("España, sin cambios de liga", lambda r: r[0] in ("es.1","es.2") and not (r[1] in cambiados or r[2] in cambiados)),
          ("Resto de ligas", lambda r: r[0] not in ("es.1","es.2"))]
for g, sel in grupos:
    a = [r[3] for r in res["actual"] if sel(r)]; b = [r[3] for r in res["corregida"] if sel(r)]
    if a: print(f"{g:<40} n={len(a):5d}  actual {sum(a)/len(a):.4f}  corregida {sum(b)/len(b):.4f}  ({1000*(sum(b)/len(b)-sum(a)/len(a)):+.1f})")
print(sorted(t for t in cambiados if t in ES_CAMB or t in ("girona","real oviedo","mallorca","racing santander","deportivo coruna","malaga")))
