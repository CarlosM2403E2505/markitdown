#!/usr/bin/env python3
"""J24 (Champions MD5 + Europa League, 24-26/11/2026): modelo multi-liga, empates x1,0 (UEFA), T=1,05 (resto).
Validación 21/11 (walk-forward UEFA, 347 partidos 2025-26 y 2026-27): el modelo NO sobrevalora a los favoritos
en Europa (favoritos 45-55 %: daba 50 %, ganaron 58 %); aplanar (T<1) empeora el log-loss en las dos mitades.
Uso: python3 modelo/j24_run.py [datos.json] [ajustes_json]
Escribe jornadas/j24/j24.json (partidos, pleno, sueltas, boleto de 18 € y 8 sencillas complementarias)."""
import importlib.util, json, os, sys
from datetime import date
import numpy as np
from scipy.stats import poisson

H = os.path.dirname(os.path.abspath(__file__)); Q = os.path.dirname(H)
def imp(n, f):
    s = importlib.util.spec_from_file_location(n, f); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
em = imp("em", os.path.join(H, "euro_model.py")); j16 = imp("j16", os.path.join(H, "j16_run.py"))
af = imp("af", os.path.join(H, "afinado.py"))
sys.path.insert(0, os.path.join(Q, "herramientas"))
bu = imp("bu", os.path.join(Q, "herramientas", "boleto_unico.py")); qc = bu.qc

DS = sys.argv[1] if len(sys.argv) > 1 else os.path.join(Q, "datos", "euro_j23.json")
AJ = json.loads(sys.argv[2]) if len(sys.argv) > 2 else {}   # {"n": [f_local, f_visitante, "motivo (clase, fuente)"]}
REF = date(2026, 11, 24)
OUT = os.path.join(Q, "jornadas", "j24", "j24.json")
fx = json.load(open(os.path.join(Q, "jornadas", "j24", "j24_fx.json"), encoding="utf-8"))["fixtures"]
ms = json.load(open(DS, encoding="utf-8"))["matches"]
m = em.EuroPoisson(xi=0.0015, ridge=10, scale=1.05, blend=0.2, hier=True).fit(ms, ref_date=REF)
print(f"Modelo: {len(ms)} partidos (hasta {max(x['date'] for x in ms)}), campo {m.home_adv:.3f}")

rows = []
for x in fx:
    lam, mu = m.rates(x["home"], x["away"])
    a = AJ.get(str(x["n"]))
    if a: lam, mu = lam * a[0], mu * a[1]
    p, cats, mk = j16.finish(lam, mu, m.emp, 1.0)
    p = af.afinar_comp(p, "uefa")
    G = np.arange(11); M = np.outer(poisson.pmf(G, lam), poisson.pmf(G, mu)); M /= M.sum(); i, j = np.indices(M.shape)
    mk.update({"Local marca": float(M[i >= 1].sum()), "Visit marca": float(M[j >= 1].sum()), "Menos 3.5": float(M[i + j <= 3].sum())})
    l2 = lambda v: "M" if v == 3 else str(v)
    r = {"n": x["n"], "partido": x["label"], "competicion": x["comp"], "dia": x["dia"], "p": [round(v, 4) for v in p],
         "xg": [round(lam, 3), round(mu, 3)], "mk": {k: round(v, 4) for k, v in mk.items()},
         "n_partidos_datos": [int(m.ngames[m.idx[x["home"]]]), int(m.ngames[m.idx[x["away"]]])]}
    if a: r["ajuste"] = a
    if x["n"] == 15:
        r["cats"] = {f"{l2(u)}-{l2(v)}": round(w, 5) for (u, v), w in cats.items()}
    rows.append(r)

partidos, pleno = rows[:14], rows[14]
pl = sorted(pleno["cats"].items(), key=lambda kv: -kv[1])
pleno.update({"factor_x": 1.0, "lambda_local": pleno["xg"][0], "lambda_visitante": pleno["xg"][1], "marcador_mesa": pl[0][0]})

# Sueltas: las 5 «marca el favorito» más probables (una por partido)
su = []
for r in partidos + [pleno]:
    eq = r["partido"].split(" – ")
    su += [(r["mk"]["Local marca"], r["partido"], f"Marca el {eq[0]}"), (r["mk"]["Visit marca"], r["partido"], f"Marca el {eq[1]}")]
vistos, sueltas = set(), []
for pv, par, ap in sorted(su, reverse=True):
    if par not in vistos and len(sueltas) < 5:
        vistos.add(par); sueltas.append({"partido": par, "apuesta": ap, "p": round(pv, 3)})

d = {"jornada": 24, "fechas": "24–26/11/2026", "tipo": "Europea (Champions J5 + Europa League)",
     "estado": "Provisional (lista no oficial: quinielafutbol.info, 21/11, clase C)",
     "primer_partido": "mar 24/11 21:00", "definitivo": "mar 24/11 18:45",
     "presupuesto": 18, "partidos": partidos, "pleno": pleno, "sueltas": sueltas,
     "datos_modelo": {"fichero": os.path.basename(DS), "hasta": max(x["date"] for x in ms),
                      "huecos": "Ligas extranjeras hasta ~1/11 (Eredivisie y Chequia hasta 20/09); sin liga eslovaca, azerí ni ucraniana 2026/27"}}
probs = [r["p"] for r in partidos]
cands = [c for c in bu.candidatos(probs, 18) if not (c["nombre"].endswith("sencillas más probables") and len(c["columnas"]) > 8)]
el = bu.elegir(cands, "p13")   # tiene que caber en un boleto (§1.5): fuera las >8 sencillas
S = "1X2"
signos = {}
for k, r in enumerate(partidos):
    if k in el["triples"]: signos[str(k + 1)] = "1 X 2"
    elif k in el["dobles"]: signos[str(k + 1)] = " ".join(sorted(el["dobles"][k], key=S.index))
    else: signos[str(k + 1)] = S[max(range(3), key=lambda t: r["p"][t])]
d["boleto_provisional"] = {"tipo": el["nombre"], "apuestas": len(el["columnas"]), "coste": el["coste"], "signos": signos,
                           "pleno": pleno["marcador_mesa"], "p14": round(el["p14"], 6), "p13": round(el["p13"], 4)}
dentro = set(el["columnas"])
pr = imp("pr", os.path.join(Q, "herramientas", "proteccion.py"))
comp, deb, pend = pr.proteger(d, signos, 8)   # regla de fijos protegidos (22/11)
d["columnas_individuales"] = comp; d["columnas_protegidas"] = comp
d["fijos_debiles"] = [{"n": f["i"] + 1, "fijo": f["fijo"], "cubre": f["alt"], "motivo": f["motivo"]} for f in deb]
todas = sorted(dentro | set(comp))
dist = qc.simular_columnas(probs, todas, n=400000)
d["conjunto"] = {"columnas": len(todas), "coste": 0.75 * len(todas), "p14": round(qc.al_menos(dist, 14), 6),
                 "p13": round(qc.al_menos(dist, 13), 4), "p12": round(qc.al_menos(dist, 12), 4), "p10": round(qc.al_menos(dist, 10), 4)}
d["empates"] = {"x_esperadas": round(sum(p[1] for p in probs), 2),
                "p_ninguna_x": round(float(np.prod([1 - p[1] for p in probs])), 4),
                "x_cubiertas_boleto": sum("X" in s for s in signos.values())}
json.dump(d, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

for r in partidos + [pleno]:
    p = r["p"]; s = signos.get(str(r["n"]), "Pleno")
    print(f"P{r['n']:<2} {r['partido']:32s} {100*p[0]:5.1f} {100*p[1]:5.1f} {100*p[2]:5.1f}  xG {r['xg'][0]:.2f}-{r['xg'][1]:.2f}  {s}")
print("Boleto:", el["nombre"], el["coste"], "€  P14 1/%d  P13 %.2f%%" % (round(1 / el["p14"]), 100 * el["p13"]))
print("Sencillas:", comp)
print("Conjunto:", d["conjunto"], "Empates:", d["empates"])
print("Pleno:", pl[:6])
print("Sueltas:", sueltas)
