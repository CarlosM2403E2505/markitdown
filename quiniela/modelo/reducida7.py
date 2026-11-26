#!/usr/bin/env python3
"""Reducida de 7 dobles al 13 (16 apuestas, codigo de Hamming [7,4]).

Elige QUE 7 partidos van dobles y QUE clase (coset) del codigo jugar para
maximizar P(14), y evalua de forma EXACTA la distribucion de aciertos.

Garantia del sistema: si los 7 sencillos se aciertan y los 7 resultados de
los dobles caen dentro de los signos elegidos, al menos una columna hace 13
(y 1 de cada 8 veces, 14).

Uso: python3 reducida7.py probs.json [--objetivo 14|13]
"""
import argparse
import itertools
import json
import math

import numpy as np

S = "1X2"
GEN = [[1, 0, 0, 0, 1, 1, 0], [0, 1, 0, 0, 1, 0, 1],
       [0, 0, 1, 0, 0, 1, 1], [0, 0, 0, 1, 1, 1, 1]]
HAM = sorted({tuple(sum(m[r] * GEN[r][c] for r in range(4)) % 2 for c in range(7))
              for m in itertools.product((0, 1), repeat=4)})


def exact(P, cols):
    N = len(P)
    cols = np.array(cols)
    var = [i for i in range(N) if len(set(cols[:, i])) > 1]
    fix = [i for i in range(N) if i not in var]
    pb = np.array([1.0])
    for i in fix:
        q = P[i][cols[0, i]]
        pb = np.convolve(pb, [1 - q, q])
    dist = np.zeros(N + 1)
    for out in itertools.product(range(3), repeat=len(var)):
        pr = math.prod(P[v][o] for v, o in zip(var, out))
        hits = max(sum(c[v] == o for v, o in zip(var, out)) for c in cols)
        dist[hits:hits + len(pb)] += pr * pb
    return dist


def build(P, objetivo=14):
    N = len(P)
    order = [sorted(range(3), key=lambda k: -p[k]) for p in P]
    best = None
    for D in itertools.combinations(range(N), 7):
        singles = [i for i in range(N) if i not in D]
        ps = math.prod(P[i][order[i][0]] for i in singles)
        pdoub = [(P[d][order[d][0]], P[d][order[d][1]]) for d in D]
        cover = math.prod(a + b for a, b in pdoub)
        for shift in itertools.product((0, 1), repeat=7):
            words = [tuple(a ^ b for a, b in zip(w, shift)) for w in HAM]
            mass = sum(math.prod(pdoub[k][w[k]] for k in range(7)) for w in words)
            score = ps * mass if objetivo == 14 else ps * cover   # 13 garantizado
            if best is None or score > best[0]:
                best = (score, D, words)
        if objetivo == 13:
            pass
    _, D, words = best
    cols = []
    for w in words:
        col = [order[i][0] for i in range(N)]
        for k, d in enumerate(D):
            col[d] = order[d][w[k]]
        cols.append(col)
    return D, cols, order


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("probs")
    ap.add_argument("--objetivo", type=int, default=14)
    args = ap.parse_args()
    rows = [r for r in json.load(open(args.probs, encoding="utf-8"))["rows"] if r["n"] <= 14]
    P = [r["p"] for r in rows]
    D, cols, order = build(P, args.objetivo)
    dist = exact(P, cols)
    print(f"Objetivo: maximizar P({args.objetivo})\n")
    print("Nº  Partido                       Tipo     Signos")
    for i, r in enumerate(rows):
        if i in D:
            sig = "".join(sorted(S[order[i][0]] + S[order[i][1]], key=S.index))
            cov = P[i][order[i][0]] + P[i][order[i][1]]
            print(f"{r['n']:<3} {r['partido']:<29} DOBLE    {sig:<3} ({cov:.1%})")
        else:
            print(f"{r['n']:<3} {r['partido']:<29} sencillo {S[order[i][0]]:<3} ({P[i][order[i][0]]:.1%})")
    print("\nLas 16 columnas (partidos 1-14):")
    for k, c in enumerate(cols, 1):
        print(f"  C{k:<2} " + " ".join(S[x] for x in c))
    for t in (14, 13, 12, 11, 10):
        print(f"P(>={t}) = {dist[t:].sum():.3%}")
    single = [order[i][0] for i in range(len(P))]
    print("\n14 signos individuales: " + " ".join(S[x] for x in single))
    json.dump({"doubles": [rows[i]["n"] for i in D],
               "cols": ["".join(S[x] for x in c) for c in cols],
               "dist": {t: float(dist[t:].sum()) for t in (14, 13, 12, 11, 10)}},
              open(args.probs.replace(".json", "_reducida.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
