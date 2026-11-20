#!/usr/bin/env python3
"""J23 (21-22/11/2026). Clubes: modelo multi-liga (Primera: empates x1,08, campo +0,07, T=1,15,
EURO_F 1,12 validado el 18/11; Segunda: empates x1,00, T=1,05). Liga F: ligaf_modelo (empates x0,85).
Pleno Sevilla–Betis: 80 % Poisson + 20 % empírica. Bajas A/B como ajustes (jornadaperfecta 18/11).
Uso: python3 modelo/j23_run.py   (desde quiniela/) -> jornadas/j23/j23.json"""
import importlib.util, json, math, os
from bisect import bisect_left
from collections import defaultdict
from datetime import date, timedelta
import numpy as np
from scipy.stats import poisson
H = os.path.dirname(os.path.abspath(__file__))
def imp(n, f):
    s = importlib.util.spec_from_file_location(n, os.path.join(H, f)); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
em = imp("em", "euro_model.py"); j16 = imp("j16", "j16_run.py"); lfm = imp("lfm", "ligaf_modelo.py"); af = imp("af", "afinado.py")
REF = date(2026, 11, 21)
EURO_F = 1.12
DRAW = {"es.1": 1.08, "es.2": 1.00, "F": 0.85}
FIX = [(1, "Alavés – Deportivo", "deportivo alaves", "deportivo coruna", "es.1"),
       (2, "Rayo – Valencia", "rayo vallecano", "valencia", "es.1"),
       (3, "Real Madrid – Celta", "real madrid", "celta", "es.1"),
       (4, "Barcelona – Villarreal", "barcelona", "villarreal", "es.1"),
       (5, "Racing – Real Sociedad", "racing santander", "real sociedad", "es.1"),
       (6, "Osasuna – Málaga", "osasuna", "malaga", "es.1"),
       (7, "Getafe – Atlético", "getafe", "atletico", "es.1"),
       (8, "Tenerife – Mallorca", "tenerife", "mallorca", "es.2"),
       (9, "Sporting – Las Palmas", "sporting gijon", "las palmas", "es.2"),
       (10, "Girona – Eibar", "girona", "eibar", "es.2"),
       (11, "Eibar F – Atlético F", "Eibar", "Atletico", "F"),
       (12, "Granada F – Real Madrid F", "Granada", "Real Madrid", "F"),
       (13, "Real Sociedad F – Sevilla F", "Real Sociedad", "Sevilla", "F"),
       (14, "Tenerife F – Madrid CFF", "Tenerife", "Madrid CFF", "F")]
PLENO = (15, "Sevilla – Betis", "sevilla", "betis", "es.1")
# Bajas A/B (jornadaperfecta 18/11; prensa del 18/11): [factor goles local, factor goles visitante]
AJ = {2: ([1.03, 0.97], "Valencia sin Gayà (roja), Jesús Vázquez, Danjuma, Otorbi y Diego López"),
      3: ([1.03, 0.93], "Celta sin Borja Iglesias (delantero titular) ni El-Abdellaoui; Starfelt y Álvaro Núñez (defensas) fuera"),
      4: ([1.00, 0.95], "Villarreal sin Gerard Moreno, Akhomach y Foyth"),
      5: ([0.95, 1.00], "Racing sin Andrés Martín (delantero clave)"),
      6: ([1.02, 0.99], "Málaga sin Lobete y Aznou (sancionado); viernes 20/11 tarde: Juan Cruz puede jugar (Funes en rueda de prensa, B)"),
      7: ([0.98, 0.96], "Getafe sin Gudelj (sancionado), Uche y Juanmi; Atlético sin Lookman (rodilla, con Nigeria) ni Pubill (con España)"),
      9: ([0.96, 0.96], "Sporting sin Otero (sanción J14-15), Casas, Gelabert, Konrad y Corredera (sancionado); Las Palmas sin Opoku (roja), Sandro Ramírez ni Ale García (20/11, B)"),
      10: ([0.98, 1.00], "Girona sin Bryan Gil, Jastin García y Álex Moreno (sancionado)"),
      15: ([1.00, 0.98], "Convocatoria oficial del Betis (20/11, A): Ceballos (MC titular) y Morante fuera (−3 %); vuelven Cucho y Bernal (+1 %). Neto 0,98. Riquelme convocado")}

ms = json.load(open(os.path.join(H, "..", "datos", "euro_j23.json")))["matches"]
uefa = defaultdict(list)
for m in ms:
    if m["competition"].startswith("uefa."):
        uefa[m["home"]].append(m["date"]); uefa[m["away"]].append(m["date"])
for k in uefa: uefa[k].sort()
def europa(t):
    xs = uefa.get(t, []); lo = (REF - timedelta(days=120)).isoformat()
    i = bisect_left(xs, lo); return i < len(xs) and xs[i] < REF.isoformat()

mod = em.EuroPoisson(xi=0.0015, ridge=10, scale=1.05, blend=0.2, hier=True).fit(ms, ref_date=REF)
lf = lfm.ajustar()
G = np.arange(11)

def precio(n, lab, h, a, comp):
    notas = []
    if comp == "F":
        lam = math.exp(lf["mu0"] + lf["home"] + lf["att"][h] + lf["dfn"][a]); mu = math.exp(lf["mu0"] + lf["att"][a] + lf["dfn"][h]); emp = None
    else:
        lam, mu = mod.rates(h, a); emp = mod.emp
        if comp == "es.1":
            lam, mu = lam * math.exp(0.07), mu * math.exp(-0.07)
            eh, ea = europa(h), europa(a)
            if eh and not ea: lam *= EURO_F; notas.append(f"EURO_F local ({h})")
            if ea and not eh: mu *= EURO_F; notas.append(f"EURO_F visitante ({a})")
    f, txt = AJ.get(n, ([1.0, 1.0], ""))
    lam, mu = lam * f[0], mu * f[1]
    p, cats, mk = j16.finish(lam, mu, emp, DRAW[comp])
    p = af.afinar_comp(p, {"es.1": "es.1", "F": "ligaf"}.get(comp, "otro"))
    M = np.outer(poisson.pmf(G, lam), poisson.pmf(G, mu)); M[np.diag_indices_from(M)] *= DRAW[comp]; M /= M.sum()
    i, j = np.indices(M.shape)
    mk.update({"Menos 3.5": float(M[i + j <= 3].sum()), "Local marca": float(M[i >= 1].sum()), "Visit marca": float(M[j >= 1].sum())})
    return {"n": n, "partido": lab, "competicion": {"es.1": "Primera", "es.2": "Segunda", "F": "Liga F"}[comp],
            "p": [round(v, 4) for v in p], "xg": [round(lam, 3), round(mu, 3)], "ajuste": f, "bajas": txt, "notas": notas,
            "mk": {k: round(v, 4) for k, v in mk.items()}}, cats, lam, mu

rows = []
for fx in FIX:
    r, _, _, _ = precio(*fx); rows.append(r)
    print(f"{r['n']:2d} {r['partido']:30s} 1 {100*r['p'][0]:4.1f} X {100*r['p'][1]:4.1f} 2 {100*r['p'][2]:4.1f}  xG {r['xg'][0]:.2f}-{r['xg'][1]:.2f} {' '.join(r['notas'])}")
pr, cats, lam, mu = precio(*PLENO)
l2 = lambda v: "M" if v == 3 else str(v)
emp = {f"{l2(x)}-{l2(y)}": round(v, 5) for (x, y), v in mod.emp.items()}
pleno = {"n": 15, "partido": PLENO[1], "competicion": "Primera", "p": pr["p"], "lambda_local": round(lam, 3), "lambda_visitante": round(mu, 3),
         "factor_x": 1.08, "empirica": emp, "mezcla": 0.2, "bajas": pr["bajas"], "notas": pr["notas"],
         "cats": {f"{l2(x)}-{l2(y)}": round(v, 4) for (x, y), v in cats.items()}}
top = sorted(pleno["cats"].items(), key=lambda kv: -kv[1])[:6]
print(f"15 Pleno {PLENO[1]:24s} 1 {100*pr['p'][0]:4.1f} X {100*pr['p'][1]:4.1f} 2 {100*pr['p'][2]:4.1f}  xG {lam:.2f}-{mu:.2f} {' '.join(pr['notas'])}")
print("   marcadores:", ", ".join(f"{k} {100*v:.1f}%" for k, v in top))
print("   Suma P(X):", round(sum(r["p"][1] for r in rows), 2))
out = {"jornada": 23, "fechas": "21-22/11/2026", "tipo": "Liga (7 Primera + 3 Segunda + 4 Liga F); Pleno derbi Sevilla–Betis",
       "cierre": "sábado 21/11 14:00", "estado": "Primera revisión (miércoles 18/11)", "presupuesto": 20,
       "lista": "quiniela15.com, 18/11/2026", "partidos": rows, "pleno": pleno}
os.makedirs(os.path.join(H, "..", "jornadas", "j23"), exist_ok=True)
json.dump(out, open(os.path.join(H, "..", "jornadas", "j23", "j23.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
