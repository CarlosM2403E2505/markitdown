"""Precios de la J22: selecciones (NatPoisson validado) + Champions femenina (modelo nuevo).
Escribe jornadas/j22/j22.json. Uso: python3 modelo/j22_run.py"""
import importlib.util, json, os
from datetime import date
import numpy as np
R = os.path.dirname(os.path.abspath(__file__))
def imp(n, f):
    s = importlib.util.spec_from_file_location(n, os.path.join(R, f)); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
sm = imp("sm", "selecciones_modelo.py"); cf = imp("cf", "champions_f_modelo.py")
T = 1.05
def afinar(p):
    q = [v ** T for v in p]; z = sum(q); return [v / z for v in q]

nat = sm.NatPoisson().fit(sm.cargar("2006-01-01"), date(2026, 11, 17))
lf = cf.ajustar()

NT = {"España": "Spain", "Bosnia": "Bosnia and Herzegovina", "Rumanía": "Romania", "Ucrania": "Ukraine",
      "Georgia": "Georgia", "Gales": "Wales", "Portugal": "Portugal", "Hungría": "Hungary",
      "Irlanda del Norte": "Northern Ireland", "Polonia": "Poland", "Suecia": "Sweden",
      "Eire": "Republic of Ireland", "Kosovo": "Kosovo", "Dinamarca": "Denmark", "Noruega": "Norway"}
WC = {"Real Madrid F": "Real Madrid", "Inter F": "Inter Milan", "Häcken F": "Häcken",
      "Manchester City F": "Manchester City", "Chelsea F": "Chelsea", "PSG F": "Paris Saint-Germain",
      "Juventus F": "Juventus", "OH Leuven F": "OH Leuven", "Austria Wien F": "Austria Wien",
      "Bayern F": "Bayern", "Arsenal F": "Arsenal", "Lyon F": "Lyon", "Barcelona F": "Barcelona",
      "Servette F": "Servette", "Benfica F": "Roma" if False else "Benfica", "Roma F": "Roma"}

def pnat(h, a):
    lam, mu = nat.rates(NT[h], NT[a], neutral=False); return sm.uno_x_dos(sm.matriz(lam, mu)), lam, mu
def pwc(h, a):
    lam, mu = cf.rates(lf, WC[h], WC[a]); return sm.uno_x_dos(sm.matriz(lam, mu)), lam, mu

FIX = [
    (1, "Bosnia – Rumanía", "nat", "Bosnia", "Rumanía"),
    (2, "Ucrania – Georgia", "nat", "Ucrania", "Georgia"),
    (3, "Gales – Portugal", "nat", "Gales", "Portugal"),
    (4, "Hungría – Irlanda del Norte", "nat", "Hungría", "Irlanda del Norte"),
    (5, "Polonia – Suecia", "nat", "Polonia", "Suecia"),
    (6, "Eire – Kosovo", "nat", "Eire", "Kosovo"),
    (7, "Real Madrid F – Inter F", "wc", "Real Madrid F", "Inter F"),
    (8, "Häcken F – Manchester City F", "wc", "Häcken F", "Manchester City F"),
    (9, "Chelsea F – PSG F", "wc", "Chelsea F", "PSG F"),
    (10, "Juventus F – OH Leuven F", "wc", "Juventus F", "OH Leuven F"),
    (11, "Austria Wien F – Bayern F", "wc", "Austria Wien F", "Bayern F"),
    (12, "Arsenal F – Lyon F", "wc", "Arsenal F", "Lyon F"),
    (13, "Barcelona F – Servette F", "wc", "Barcelona F", "Servette F"),
    (14, "Benfica F – Roma F", "wc", "Benfica F", "Roma F"),
]
partidos = []
for n, lab, tipo, h, a in FIX:
    (p, lam, mu) = pnat(h, a) if tipo == "nat" else pwc(h, a)  # sin T: Poisson validado
    partidos.append({"n": n, "partido": lab, "competicion": "Selecciones" if tipo == "nat" else "Champions F",
                     "p": [round(v, 4) for v in p], "xg": [round(lam, 2), round(mu, 2)],
                     "confianza": "alta" if tipo == "nat" else "media (modelo femenino nuevo)"})
    print(f"{n:2d} {lab:32s} 1 {100*p[0]:4.1f}  X {100*p[1]:4.1f}  2 {100*p[2]:4.1f}  [{partidos[-1]['confianza'][:5]}]")
# Pleno Dinamarca – Noruega
pp, lam, mu = pnat("Dinamarca", "Noruega")
m = sm.matriz(lam, mu); cats = {}
for i in range(11):
    for j in range(11):
        k = f"{min(i,3) if i<3 else 'M'}-{min(j,3) if j<3 else 'M'}".replace('3','M')
        cats[k] = cats.get(k, 0) + m[i, j]
pleno = {"n": 15, "partido": "Dinamarca – Noruega", "competicion": "Selecciones", "p": [round(v, 4) for v in pp],
         "lambda_local": round(lam, 3), "lambda_visitante": round(mu, 3), "mezcla": 0.0,
         "cats": {k: round(v, 4) for k, v in cats.items()},
         "precio": "Poisson de selecciones (validado), sin mezcla empírica"}
print(f"15 Pleno Dinamarca – Noruega        1 {100*pp[0]:4.1f}  X {100*pp[1]:4.1f}  2 {100*pp[2]:4.1f}  xG {lam:.2f}-{mu:.2f}")
top = sorted(cats.items(), key=lambda x: -x[1])[:5]
print("   Pleno marcadores:", ", ".join(f"{k} {100*v:.1f}%" for k, v in top))
out = {"jornada": 22, "fechas": "17-19/11/2026", "tipo": "Selecciones (repesca Mundial) + Champions femenina",
       "cierre": "martes 17/11 20:45", "estado": "Pronóstico v1 (selecciones validadas + modelo femenino nuevo)",
       "presupuesto": 20, "partidos": partidos, "pleno": pleno}
json.dump(out, open(os.path.join(R, "..", "jornadas", "j22", "j22.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
