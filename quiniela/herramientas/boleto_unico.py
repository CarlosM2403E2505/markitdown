#!/usr/bin/env python3
"""Un solo boleto con un presupuesto máximo: compara todos los formatos y elige con el objetivo dado.

Candidatos (0,75 € por apuesta):
  - directas de d dobles y t triples (2^d·3^t apuestas);
  - reducidas oficiales 1 (4 triples, 9), 2 (7 dobles, 16) y 3 (3 dobles + 3 triples, 24);
  - las k columnas sencillas más probables (k = 8, 16 y el máximo que permita el presupuesto).
En cada formato, los partidos con dobles y triples son los que más P(14) dan (boletos_oficiales.candidatos).
Objetivo «p13» (pedido por el usuario el 14/11/2026): mayor P(≥13); desempate por P(14), P(≥12) y menor coste.
Objetivo «fijo»: el criterio de la fase 8 (P(14) ≥ 90 % de la máxima → mayor P(≥12)).

Uso: python3 herramientas/boleto_unico.py jornadas/j21/j21.json 20 [p13|fijo]
"""
import json, math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import quiniela_calc as qc
import boletos_oficiales as bo

S = "1X2"


def candidatos(probs, presupuesto):
    bo.CODIGOS = {"R1": bo.ternario42(), "R2": bo.hamming74(), "R3": bo.codigo_cubridor(3, 3)}
    max_ap = int(presupuesto / bo.PRECIO + 1e-9)
    formatos = [(f"Directa: {d} doble(s) + {t} triple(s)", d, t, None) for d in range(0, 6) for t in range(0, 4)
                if 2 <= 2 ** d * 3 ** t <= max_ap]
    formatos += [(n, d, t, c) for n, d, t, c in bo.FORMATOS if c and len(bo.CODIGOS[c]) <= max_ap]
    out = []
    for nombre, d, t, cod in formatos:
        _, dob, tri, cols = bo.candidatos(probs, d, t, cod, set())
        out.append({"nombre": nombre, "dobles": dob, "triples": list(tri), "columnas": cols})
    for k in sorted({8, 16, max_ap}):
        if k <= max_ap:
            out.append({"nombre": f"{k} columnas sencillas más probables", "dobles": {}, "triples": [],
                        "columnas": qc.columnas_mas_probables(probs, k)})
    for c in out:
        cols = c["columnas"]
        nvar = sum(len({x[i] for x in cols}) > 1 for i in range(14))
        dist = qc.evaluar_columnas(probs, cols) if nvar <= 10 else qc.simular_columnas(probs, cols, n=300000)
        c.update(coste=bo.PRECIO * len(cols), p14=sum(bo.pcol(probs, x) for x in set(cols)),
                 p13=qc.al_menos(dist, 13), p12=qc.al_menos(dist, 12), p10=qc.al_menos(dist, 10))
    return out


def elegir(cands, objetivo="p13"):
    if objetivo == "fijo":
        mx = max(c["p14"] for c in cands)
        return max((c for c in cands if c["p14"] >= 0.9 * mx), key=lambda c: (c["p12"], -c["coste"]))
    return max(cands, key=lambda c: (round(c["p13"], 5), c["p14"], c["p12"], -c["coste"]))


def main(ruta, presupuesto, objetivo):
    d = json.load(open(ruta, encoding="utf-8")); probs = [x["p"] for x in d["partidos"]]
    cands = candidatos(probs, presupuesto)
    el = elegir(cands, objetivo); fijo = elegir(cands, "fijo")
    print(f"Jornada {d['jornada']} · un boleto de hasta {presupuesto:.2f} € · objetivo {objetivo}\n")
    print(f"{'Candidato':52s} {'€':>6s} {'P(14)':>14s} {'P(≥13)':>8s} {'P(≥12)':>8s} {'P(≥10)':>8s}")
    for c in sorted(cands, key=lambda c: -c["p13"]):
        marca = ("  ← ELEGIDO" if c is el else "") + ("  (criterio fijo)" if c is fijo and c is not el else "")
        print(f"{c['nombre']:52s} {c['coste']:6.2f} {'1 entre ' + format(round(1 / c['p14']), ',').replace(',', '.'):>14s} "
              f"{100 * c['p13']:7.2f}% {100 * c['p12']:7.1f}% {100 * c['p10']:7.1f}%{marca}")
    print(f"\nElegido: {el['nombre']} · {len(el['columnas'])} apuestas · {el['coste']:.2f} €")
    for i, x in enumerate(d["partidos"]):
        if el["dobles"] or el["triples"]:
            s = "1X2" if i in el["triples"] else ("".join(sorted(el["dobles"][i], key=S.index)) if i in el["dobles"] else S[max(range(3), key=lambda t: x["p"][t])])
        else:
            s = "".join(sorted({c[i] for c in el["columnas"]}, key=S.index))
        print(f"  {i + 1:2d}. {x['partido']:30s} {s}")
    json.dump({"objetivo": objetivo, "elegido": el, "criterio_fijo": fijo["nombre"],
               "candidatos": [{k: v for k, v in c.items() if k != "columnas"} for c in cands]},
              open(os.path.join(os.path.dirname(ruta), "boleto_unico.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
    return el


if __name__ == "__main__":
    main(sys.argv[1], float(sys.argv[2]), sys.argv[3] if len(sys.argv) > 3 else "p13")
