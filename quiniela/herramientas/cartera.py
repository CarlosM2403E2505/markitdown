#!/usr/bin/env python3
"""Cartera de varios boletos complementarios (sin columnas repetidas) para una jornada.

Compara, con el mismo número total de columnas:
  · C  : las N columnas más probables (máxima P(14));
  · F  : el mejor sistema completo de dobles y triples con N columnas;
y elige con el criterio fijo de la mesa (P(14) ≥ 90 % de la máxima → mayor P(≥12)).
Después reparte las columnas en boletos, del más probable al menos probable.

Uso: python3 herramientas/cartera.py jornadas/j21/j21.json 16,16,16,16,8,8,8,8
"""
import itertools, json, math, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import quiniela_calc as qc
S = "1X2"

def mejor_completo(probs, n_cols):
    """Mejor sistema de d dobles y t triples con 2^d·3^t = n_cols (máxima P(14))."""
    formas = [(d, t) for t in range(0, 6) for d in range(0, 15) if 2 ** d * 3 ** t == n_cols and d + t <= 14]
    orden = [sorted(range(3), key=lambda s: -p[s]) for p in probs]
    mejor = None
    for d, t in formas:
        for tri in itertools.combinations(range(14), t):
            resto = [i for i in range(14) if i not in tri]
            # dobles: los que más ganan al pasar de sencillo a doble
            gan = sorted(resto, key=lambda i: -(probs[i][orden[i][1]] / probs[i][orden[i][0]]))
            dob = gan[:d]
            p14 = 1.0
            for i in range(14):
                if i in tri: continue
                p14 *= probs[i][orden[i][0]] + (probs[i][orden[i][1]] if i in dob else 0)
            if not mejor or p14 > mejor[0]:
                mejor = (p14, tri, tuple(dob))
    p14, tri, dob = mejor
    opciones = [S if i in tri else (S[orden[i][0]] + S[orden[i][1]] if i in dob else S[orden[i][0]]) for i in range(14)]
    cols = ["".join(c) for c in itertools.product(*opciones)]
    cols.sort(key=lambda c: -math.prod(probs[i][S.index(c[i])] for i in range(14)))
    return cols, tri, dob

def resumen(probs, cols):
    dist = qc.simular_columnas(probs, cols, n=200000)
    return {"p14": sum(math.prod(probs[i][S.index(c[i])] for i in range(14)) for c in cols),
            "p13": qc.al_menos(dist, 13), "p12": qc.al_menos(dist, 12), "p11": qc.al_menos(dist, 11), "p10": qc.al_menos(dist, 10)}

def main(ruta, tamanos):
    d = json.load(open(ruta, encoding="utf-8"))
    probs = [x["p"] for x in d["partidos"]]; N = sum(tamanos)
    c = qc.columnas_mas_probables(probs, N)
    f, tri, dob = mejor_completo(probs, N)
    sis = {"C · las %d más probables" % N: c, "F · completo (%d dobles, %d triples)" % (len(dob), len(tri)): f}
    res = {k: resumen(probs, v) for k, v in sis.items()}
    mx = max(r["p14"] for r in res.values())
    elegido = max((k for k in res if res[k]["p14"] >= 0.9 * mx), key=lambda k: res[k]["p12"])
    pnox = math.prod(1 - p[1] for p in probs)
    print(f"Jornada {d['jornada']} · {len(tamanos)} boletos · {N} columnas · {0.75 * N:.2f} €")
    print(f"P(que no haya ningún empate en los 14) = {100 * pnox:.1f} % · empates esperados = {sum(p[1] for p in probs):.2f}\n")
    print(f"{'Sistema':42s} {'P(14)':>16s} {'P(≥13)':>8s} {'P(≥12)':>8s} {'P(≥11)':>8s} {'P(≥10)':>8s}  X cubiertas")
    for k, r in res.items():
        nx = sum(len({col[i] for col in sis[k]} & {"X"}) for i in range(14))
        print(f"{k:42s} {'1 entre %s' % format(round(1 / r['p14']), ',').replace(',', '.'):>16s} {100*r['p13']:7.2f}% {100*r['p12']:7.1f}% {100*r['p11']:7.1f}% {100*r['p10']:7.1f}%  {nx} partidos{'  ← ELEGIDO' if k == elegido else ''}")
    if tri or dob:
        print(f"  F: triples en {[d['partidos'][i]['partido'] for i in tri]}, dobles en {[d['partidos'][i]['partido'] for i in dob]}")
    cols = sis[elegido]; i0 = 0; salida = []
    print()
    for b, t in enumerate(tamanos, 1):
        bloque = cols[i0:i0 + t]; i0 += t
        r = resumen(probs, bloque)
        salida.append({"boleto": b, "euros": 0.75 * t, "columnas": bloque, **r})
        print(f"Boleto {b} ({0.75 * t:.0f} €, {t} columnas): P(14) 1 entre {format(round(1 / r['p14']), ',').replace(',', '.')} · P(≥13) {100*r['p13']:.2f} % · P(≥12) {100*r['p12']:.1f} %")
        for k in range(0, t, 4):
            print("    " + "  ".join(bloque[k:k + 4]))
    return salida, res[elegido], elegido

if __name__ == "__main__":
    salida, total, elegido = main(sys.argv[1], [int(x) for x in sys.argv[2].split(",")])
    json.dump({"elegido": elegido, "total": total, "boletos": salida},
              open(os.path.join(os.path.dirname(sys.argv[1]), "cartera.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
