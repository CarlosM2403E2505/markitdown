#!/usr/bin/env python3
"""J25 (28-30/11/2026, Liga: 8 Primera + 6 Segunda; Pleno Espanyol–Getafe). Patrón de j23_run.py.
Primera: empates x1,08, campo +0,07, T=1,15, X templada y X con favorito claro (afinado.py), EURO_F 1,12.
Segunda: empates x1,00, T=1,05. Pleno: 80 % Poisson + 20 % empírica.
Datos: datos/euro_j24.json (Primera hasta 22/11; Segunda hasta 15/11) + resultados de Segunda de la J23 (j23.json).
Conserva de jornadas/j25/j25.json los campos 'datos' y la P del estudio de estilos (como p_estudio, peso 0).
Uso: python3 modelo/j25_run.py   (desde quiniela/)  -> después: herramientas/reglas_mesa.py jornadas/j25/j25.json --guardar"""
import importlib.util, json, math, os
from bisect import bisect_left
from collections import defaultdict
from datetime import date, timedelta
import numpy as np
from scipy.stats import poisson
H = os.path.dirname(os.path.abspath(__file__)); Q = os.path.dirname(H)
def imp(n, f):
    s = importlib.util.spec_from_file_location(n, os.path.join(H, f)); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
em = imp("em", "euro_model.py"); j16 = imp("j16", "j16_run.py"); af = imp("af", "afinado.py")
REF = date(2026, 11, 27)
EURO_F = 1.12
DRAW = {"es.1": 1.08, "es.2": 1.00}
HORA = {1: "sáb 28/11 14:00", 2: "sáb 28/11 16:15", 3: "sáb 28/11 18:30", 4: "sáb 28/11 21:00", 5: "dom 29/11 14:00",
        6: "dom 29/11 16:15", 7: "dom 29/11 18:30", 8: "dom 29/11 21:00", 9: "sáb 28/11 14:00", 10: "sáb 28/11 16:15",
        11: "sáb 28/11 18:30", 12: "dom 29/11 14:00", 13: "dom 29/11 16:15", 14: "dom 29/11 21:00", 15: "lun 30/11 21:00"}
FIX = [(1, "Betis – Rayo", "betis", "rayo vallecano", "es.1"),
       (2, "Málaga – Athletic", "malaga", "athletic bilbao", "es.1"),
       (3, "Elche – Atlético", "elche", "atletico", "es.1"),
       (4, "Real Madrid – Alavés", "real madrid", "deportivo alaves", "es.1"),
       (5, "Valencia – Osasuna", "valencia", "osasuna", "es.1"),
       (6, "Deportivo – Barcelona", "deportivo coruna", "barcelona", "es.1"),
       (7, "Celta – Villarreal", "celta", "villarreal", "es.1"),
       (8, "Real Sociedad – Sevilla", "real sociedad", "sevilla", "es.1"),
       (9, "Las Palmas – Andorra", "las palmas", "andorra", "es.2"),
       (10, "Albacete – Tenerife", "albacete", "tenerife", "es.2"),
       (11, "Eibar – Burgos", "eibar", "burgos", "es.2"),
       (12, "Granada – Ceuta", "granada", "ad ceuta", "es.2"),
       (13, "Mallorca – Castellón", "mallorca", "castellon", "es.2"),
       (14, "Almería – Sporting", "almeria", "sporting gijon", "es.2")]
PLENO = (15, "Espanyol – Getafe", "espanyol barcelona", "getafe", "es.1")
# Bajas A/B: [factor goles local, factor goles visitante]. Primer repaso (26/11): se rellena con lo comprobado.
AJ = json.load(open(os.path.join(Q, "jornadas", "j25", "bajas_2611.json"), encoding="utf-8")) if os.path.exists(
    os.path.join(Q, "jornadas", "j25", "bajas_2611.json")) else {}
AJ = {int(k): (v["f"], v["txt"]) for k, v in AJ.items() if isinstance(v, dict) and v.get("clase") in ("A", "B")}

ms = json.load(open(os.path.join(Q, "datos", "euro_j24.json")))["matches"]
extra = [("tenerife", "mallorca", 0, 0), ("sporting gijon", "las palmas", 0, 2), ("girona", "eibar", 2, 1)]
ms += [{"home": h, "away": a, "date": "2026-11-22", "hg": x, "ag": y, "competition": "es.2:2026-27", "fuente": "j23.json"} for h, a, x, y in extra]
uefa = defaultdict(list)
for m in ms:
    if m["competition"].startswith("uefa."):
        uefa[m["home"]].append(m["date"]); uefa[m["away"]].append(m["date"])
for k in uefa: uefa[k].sort()
def europa(t):
    xs = uefa.get(t, []); lo = (REF - timedelta(days=120)).isoformat()
    i = bisect_left(xs, lo); return i < len(xs) and xs[i] < REF.isoformat()
def forma(t, comp):
    xs = sorted((m for m in ms if m["competition"] == comp + ":2026-27" and t in (m["home"], m["away"])), key=lambda m: m["date"])[-5:]
    pts = 0
    for m in xs:
        g, c = (m["hg"], m["ag"]) if m["home"] == t else (m["ag"], m["hg"])
        pts += 3 if g > c else 1 if g == c else 0
    return pts if len(xs) == 5 else None

mod = em.EuroPoisson(xi=0.0015, ridge=10, scale=1.05, blend=0.2, hier=True).fit(ms, ref_date=REF)
G = np.arange(11)

def precio(n, lab, h, a, comp):
    notas = []
    lam, mu = mod.rates(h, a); emp = mod.emp
    if comp == "es.1":
        lam, mu = lam * math.exp(0.07), mu * math.exp(-0.07)
        eh, ea = europa(h), europa(a)
        if eh and not ea: lam *= EURO_F; notas.append(f"EURO_F local ({h})")
        if ea and not eh: mu *= EURO_F; notas.append(f"EURO_F visitante ({a})")
    f, txt = AJ.get(n, ([1.0, 1.0], ""))
    lam, mu = lam * f[0], mu * f[1]
    p, cats, mk = j16.finish(lam, mu, emp, DRAW[comp])
    p = af.afinar_comp(p, comp)
    M = np.outer(poisson.pmf(G, lam), poisson.pmf(G, mu)); M[np.diag_indices_from(M)] *= DRAW[comp]; M /= M.sum()
    i, j = np.indices(M.shape)
    mk.update({"Menos 3.5": float(M[i + j <= 3].sum()), "Local marca": float(M[i >= 1].sum()), "Visit marca": float(M[j >= 1].sum())})
    fav = h if p[0] >= p[2] else a
    return {"n": n, "partido": lab, "competicion": {"es.1": "Primera", "es.2": "Segunda"}[comp], "hora": HORA[n],
            "p": [round(v, 4) for v in p], "xg": [round(lam, 3), round(mu, 3)], "ajuste": f, "bajas": txt, "notas": notas,
            "forma_favorito": forma(fav, comp), "mk": {k: round(v, 4) for k, v in mk.items()}}, cats, lam, mu

OUTF = os.path.join(Q, "jornadas", "j25", "j25.json")
prev = json.load(open(OUTF, encoding="utf-8"))
pv = {x["n"]: x for x in prev["partidos"]}
rows = []
for fx in FIX:
    r, _, _, _ = precio(*fx)
    o = pv.get(r["n"], {})
    if o.get("datos"): r["datos"] = o["datos"]
    if o.get("p_estudio") or o.get("fuente_p", "").startswith("estudio"): r["p_estudio"] = o.get("p_estudio", o.get("p"))
    for k in ("mercado", "mercado_fuente", "publico"):
        if k in o: r[k] = o[k]
    rows.append(r)
    print(f"{r['n']:2d} {r['partido']:26s} 1 {100*r['p'][0]:4.1f} X {100*r['p'][1]:4.1f} 2 {100*r['p'][2]:4.1f}  xG {r['xg'][0]:.2f}-{r['xg'][1]:.2f} forma {r['forma_favorito']} {' '.join(r['notas'])}")
pr, cats, lam, mu = precio(*PLENO)
l2 = lambda v: "M" if v == 3 else str(v)
pleno = {"n": 15, "partido": PLENO[1], "competicion": "Primera", "hora": HORA[15], "p": pr["p"], "lambda_local": round(lam, 3),
         "lambda_visitante": round(mu, 3), "factor_x": 1.08, "mezcla": 0.2, "bajas": pr["bajas"], "notas": pr["notas"],
         "cats": {f"{l2(x)}-{l2(y)}": round(v, 4) for (x, y), v in cats.items()}, "mk": pr["mk"]}
top = sorted(pleno["cats"].items(), key=lambda kv: -kv[1])
pleno["marcador_mesa"] = top[0][0]
if prev.get("pleno", {}).get("datos"): pleno["datos"] = prev["pleno"]["datos"]
pleno["estudio"] = {"marcador": prev.get("pleno", {}).get("marcador_mesa"), "p": prev.get("pleno", {}).get("p")}
print(f"15 Pleno {PLENO[1]:20s} 1 {100*pr['p'][0]:4.1f} X {100*pr['p'][1]:4.1f} 2 {100*pr['p'][2]:4.1f}  xG {lam:.2f}-{mu:.2f} {' '.join(pr['notas'])}")
print("   marcadores:", ", ".join(f"{k} {100*v:.1f}%" for k, v in top[:6]))
su = []
for r in rows + [pleno]:
    eq = r["partido"].split(" – ")
    su += [(r["mk"]["Local marca"], r["partido"], f"Marca el {eq[0]}"), (r["mk"]["Visit marca"], r["partido"], f"Marca el {eq[1]}")]
vistos, sueltas = set(), []
for p_, par, ap in sorted(su, reverse=True):
    if par not in vistos and len(sueltas) < 5:
        vistos.add(par); sueltas.append({"partido": par, "apuesta": ap, "p": round(p_, 3)})
probs = [r["p"] for r in rows]
out = {k: v for k, v in prev.items() if k in ("pendientes", "medicion_factores", "publico")}
out.update({"jornada": 25, "fechas": "28-30/11/2026", "tipo": "Liga (8 Primera + 6 Segunda); Pleno Espanyol–Getafe",
            "cierre": "sábado 28/11 13:00 particulares (eduardolosilla; quiniela15 dice 14:00)", "primer_partido": "sáb 28/11 14:00",
            "definitivo": "sáb 28/11 11:45", "bote": "1.100.000 € (quiniela15 y eduardolosilla, 26/11)",
            "estado": "Primer repaso (jueves 26/11)", "presupuesto": 18,
            "lista": "quiniela15.com y eduardolosilla.es, 26/11/2026; horarios laliga.com (A)",
            "datos_modelo": {"fichero": "euro_j24.json + 3 de Segunda (j23.json)", "huecos": "Segunda J15 (21-23/11) sin 8 de sus 11 partidos"},
            "partidos": rows, "pleno": pleno, "sueltas": sueltas,
            "empates": {"x_esperadas": round(sum(p[1] for p in probs), 2), "p_ninguna_x": round(float(np.prod([1 - p[1] for p in probs])), 4)}})
json.dump(out, open(OUTF, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("Suma X", out["empates"], "Sueltas", sueltas)
