#!/usr/bin/env python3
"""Boletos que se rellenan fácil: múltiples directas y reducidas oficiales de Loterías (SELAE).

Formatos (0,75 € por apuesta; fuente: loteriasyapuestas.es, «Quinielas reducidas»):
  Reducida 1: 4 triples → 9 apuestas (6,75 €), garantía 13 si aciertas los fijos.
  Reducida 2: 7 dobles → 16 apuestas (12 €), garantía 13.
  Reducida 3: 3 dobles + 3 triples → 24 apuestas (18 €), garantía 13.
  Directa: d dobles y t triples → 2^d·3^t apuestas (todas las combinaciones).

Para cada formato elige qué partidos llevan dobles o triples. Elige los boletos uno a uno: cada
nuevo boleto es el que más probabilidad de 14 añade a los ya elegidos, sin contar las columnas
repetidas. Las columnas de las reducidas siguen un código con la misma garantía que el oficial;
la tabla exacta de Loterías puede repartir los signos de otra forma, así que su P(14) es aproximada.

Uso: python3 herramientas/boletos_oficiales.py jornadas/j21/j21.json 20 4
"""
import itertools, json, math, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import quiniela_calc as qc
S = "1X2"; PRECIO = 0.75


def codigo_cubridor(dobles, triples):
    """Conjunto mínimo de palabras (radio 1) en {0,1}^dobles × {0,1,2}^triples, por programación entera."""
    from scipy.optimize import milp, LinearConstraint, Bounds
    esp = list(itertools.product(*([range(2)] * dobles + [range(3)] * triples)))
    ix = {w: i for i, w in enumerate(esp)}
    A = np.zeros((len(esp), len(esp)))
    for v in esp:
        A[ix[v], ix[v]] = 1
        for k in range(len(v)):
            for s in range(2 if k < dobles else 3):
                if s != v[k]:
                    A[ix[v], ix[v[:k] + (s,) + v[k + 1:]]] = 1
    r = milp(np.ones(len(esp)), constraints=LinearConstraint(A, 1, np.inf), integrality=np.ones(len(esp)), bounds=Bounds(0, 1))
    return [esp[i] for i in range(len(esp)) if r.x[i] > 0.5]


def hamming74():
    return [w for w in itertools.product(range(2), repeat=7)
            if (w[0] ^ w[1] ^ w[3] ^ w[4]) == 0 and (w[0] ^ w[2] ^ w[3] ^ w[5]) == 0 and (w[1] ^ w[2] ^ w[3] ^ w[6]) == 0]


def ternario42():
    return [(a, b, (a + b) % 3, (a + 2 * b) % 3) for a in range(3) for b in range(3)]


FORMATOS = [  # nombre, dobles, triples, código (None = directa)
    ("Reducida 3 oficial (3 dobles + 3 triples)", 3, 3, "R3"),
    ("Directa (3 dobles + 1 triple)", 3, 1, None),
    ("Reducida 2 oficial (7 dobles)", 7, 0, "R2"),
    ("Directa (1 doble + 2 triples)", 1, 2, None),
    ("Directa (4 dobles)", 4, 0, None),
    ("Directa (2 dobles + 2 triples)", 2, 2, None),
    ("Reducida 1 oficial (4 triples)", 0, 4, "R1"),
    ("Directa (5 dobles)", 5, 0, None),
    ("Directa (3 triples)", 0, 3, None),
]


def columnas(probs, dob, tri, codigo):
    """dob: {partido: dos signos}, tri: lista de partidos con triple."""
    base = [S[max(range(3), key=lambda s: p[s])] for p in probs]
    dl = sorted(dob); tl = sorted(tri)
    if codigo is None:
        palabras = itertools.product(*([range(2)] * len(dl) + [range(3)] * len(tl)))
    else:
        palabras = CODIGOS[codigo]
    out = []
    for w in palabras:
        c = list(base)
        for k, i in enumerate(dl):
            c[i] = "".join(sorted(dob[i], key=S.index))[w[k]]  # orden 1-X-2 del boleto
        for k, i in enumerate(tl):
            c[i] = S[w[len(dl) + k]]
        out.append("".join(c))
    return out


def pcol(probs, c):
    return math.prod(probs[i][S.index(c[i])] for i in range(14))


def candidatos(probs, nd, nt, codigo, ya):
    """Mejor asignación de partidos para un formato: la que más P(14) nueva añade."""
    orden = [sorted(range(3), key=lambda s: -p[s]) for p in probs]
    mejor = None
    for tri in itertools.combinations(range(14), nt):
        resto = [i for i in range(14) if i not in tri]
        for dob in itertools.combinations(resto, nd):
            # para los dobles se prueban las dos parejas más probables del partido
            for parejas in itertools.product(*[[(orden[i][0], orden[i][1]), (orden[i][0], orden[i][2])] for i in dob]) if nd <= 4 else [[(orden[i][0], orden[i][1]) for i in dob]]:
                d = {i: S[a] + S[b] for i, (a, b) in zip(dob, parejas)}
                cols = columnas(probs, d, tri, codigo)
                nuevo = sum(pcol(probs, c) for c in set(cols) - ya)
                if not mejor or nuevo > mejor[0]:
                    mejor = (nuevo, d, tri, cols)
    return mejor


def main(ruta, presupuesto, n_boletos):
    global CODIGOS
    CODIGOS = {"R1": ternario42(), "R2": hamming74(), "R3": codigo_cubridor(3, 3)}
    assert len(CODIGOS["R1"]) == 9 and len(CODIGOS["R2"]) == 16 and len(CODIGOS["R3"]) == 24, {k: len(v) for k, v in CODIGOS.items()}
    d = json.load(open(ruta, encoding="utf-8")); probs = [x["p"] for x in d["partidos"]]
    formatos = [f for f in FORMATOS if PRECIO * (len(CODIGOS[f[3]]) if f[3] else 2 ** f[1] * 3 ** f[2]) <= presupuesto]
    ya, elegidos = set(), []
    for _ in range(n_boletos):
        opciones = []
        for nombre, nd, nt, cod in formatos:
            if any(e["formato"] == nombre for e in elegidos):
                continue  # boletos de formatos distintos
            nuevo, dob, tri, cols = candidatos(probs, nd, nt, cod, ya)
            coste = PRECIO * len(cols)
            opciones.append((nuevo, nombre, dob, tri, cols, coste))
        # criterio: más P(14) nueva por euro, para no premiar gastar más
        nuevo, nombre, dob, tri, cols, coste = max(opciones, key=lambda o: o[0] / o[5])
        elegidos.append({"formato": nombre, "dobles": dob, "triples": list(tri), "columnas": cols, "coste": coste, "p14_nueva": nuevo})
        ya |= set(cols)
    for e in elegidos:
        dist = qc.evaluar_columnas(probs, e["columnas"])
        e.update(p14=qc.al_menos(dist, 14), p13=qc.al_menos(dist, 13), p12=qc.al_menos(dist, 12), p10=qc.al_menos(dist, 10))
    todas = sorted(ya)
    dist = qc.simular_columnas(probs, todas, n=300000)
    total = {"coste": sum(e["coste"] for e in elegidos), "columnas": len(todas), "p14": sum(pcol(probs, c) for c in todas),
             "p13": qc.al_menos(dist, 13), "p12": qc.al_menos(dist, 12), "p10": qc.al_menos(dist, 10)}
    return d, elegidos, total


if __name__ == "__main__":
    d, el, tot = main(sys.argv[1], float(sys.argv[2]), int(sys.argv[3]))
    for k, e in enumerate(el, 1):
        print(f"\nBoleto {k}: {e['formato']} · {len(e['columnas'])} apuestas · {e['coste']:.2f} €")
        print(f"  P(14) 1 entre {round(1/e['p14'])} · P(≥13) {100*e['p13']:.2f} % · P(≥12) {100*e['p12']:.1f} % · P(≥10) {100*e['p10']:.1f} %")
        for i, x in enumerate(d["partidos"]):
            s = "1X2" if i in e["triples"] else e["dobles"].get(i) or S[max(range(3), key=lambda t: x["p"][t])]
            s = "".join(sorted(s, key=S.index))
            print(f"  {i+1:2d}. {x['partido']:30s} {s:4s} {'TRIPLE' if len(s)==3 else ('DOBLE' if len(s)==2 else '')}")
    print(f"\nLos {len(el)} juntos: {tot['coste']:.2f} € · {tot['columnas']} columnas distintas · P(14) 1 entre {round(1/tot['p14'])} · P(≥13) {100*tot['p13']:.2f} % · P(≥12) {100*tot['p12']:.1f} % · P(≥10) {100*tot['p10']:.1f} %")
    json.dump({"boletos": [{k: v for k, v in e.items()} for e in el], "total": tot},
              open(os.path.join(os.path.dirname(sys.argv[1]), "boletos_oficiales.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
