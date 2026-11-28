#!/usr/bin/env python3
"""Seguro de favoritos (regla 26/11/2026, analisis/seguro-favoritos.md).

Si hay >= 4 favoritos de la mesa entre el 55 % y el 75 %, se toman los 4 más probables y se
sustituyen las 4 sencillas menos probables del boleto por 4 columnas «2 con X y 2 con el favorito»:
cada una lleva el 2.º signo de la mesa (la X, o el otro si es más probable) en 2 de los 4 favoritos
y el favorito en los otros 2. Se prueban las 15 formas de elegir 4 de los 6 pares y se queda la de
mayor P(>=13); solo se aplica si no baja la P(>=13) del boleto. El resto de signos de cada columna
nueva = los de la sencilla que sustituye, para no romper la diversidad R3 (se comprueba) (con la P del boleto: casas si hay mercado, R5b).

Uso: python3 herramientas/seguro_favoritos.py jornadas/jNN/jNN.json [--guardar]
Lee y reescribe boleto_mesa (columnas y, si existe, el reparto en boletos de 8)."""
import argparse, itertools, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import quiniela_calc as qc
import reglas_mesa as rm
from reglas_mesa import probabilidades

S = "1X2"


def p_col(probs, c):
    v = 1.0
    for p, s in zip(probs, c):
        v *= p[S.index(s)]
    return v


def seguro(d, n_sim=200000):
    mesa = [x["p"] for x in d["partidos"]]
    rm.TOPES_JORNADA = rm.topes_partidos(d["partidos"])
    probs = probabilidades(d["partidos"], True)
    todas = list(d["boleto_mesa"]["columnas"])
    import re
    m = re.match(r".+? \+ (\d+) sencillas", d["boleto_mesa"]["formato"])
    fijas = todas[:len(todas) - int(m.group(1))] if m else []   # reducida/directa oficial: no se toca
    cols = todas[len(fijas):]
    favs = [(max(p), i) for i, p in enumerate(mesa) if 0.55 <= max(p) <= 0.75]
    if len(favs) < 4:
        return None, f"solo {len(favs)} favoritos entre 55 y 75 % (hacen falta 4)"
    favs = [i for _, i in sorted(favs, reverse=True)[:4]]
    base = [S[max(range(3), key=lambda t: p[t])] for p in probs]
    segundo = {}
    for i in favs:
        o = sorted(range(3), key=lambda t: -mesa[i][t])
        segundo[i] = S[o[1]]
    for i in favs:
        base[i] = S[max(range(3), key=lambda t: mesa[i][t])]
    pares = list(itertools.combinations(favs, 2))
    quitar = sorted(cols, key=lambda c: p_col(probs, c))[:4]
    resto = [c for c in cols if c not in quitar]
    d0 = qc.simular_columnas(probs, fijas + cols, n=n_sim)
    ref = {"p13": qc.al_menos(d0, 13), "p12": qc.al_menos(d0, 12), "p10": qc.al_menos(d0, 10)}
    mejor = None
    for elegidos in itertools.combinations(pares, 4):
        nuevas = []
        for par, q in zip(elegidos, quitar):   # la columna quitada conserva sus otros 10 signos (diversidad R3)
            c = list(q)
            for i in favs:
                c[i] = segundo[i] if i in par else base[i]
            nuevas.append("".join(c))
        if len(set(nuevas) | set(resto) | set(fijas)) < len(cols) + len(set(fijas)) or rm.diversidad(probs, fijas + resto + nuevas):
            continue
        dist = qc.simular_columnas(probs, fijas + resto + nuevas, n=n_sim)
        r = {"p13": qc.al_menos(dist, 13), "p12": qc.al_menos(dist, 12), "p10": qc.al_menos(dist, 10)}
        if mejor is None or (r["p13"], r["p12"]) > (mejor[1]["p13"], mejor[1]["p12"]):
            mejor = (nuevas, r, elegidos)
    if mejor is None:
        return None, "ninguna forma cumple R3 (el boleto ya cubre a esos favoritos más que el seguro) o ya estaban en el boleto"
    nuevas, r, elegidos = mejor
    info = {"favoritos": [{"n": i + 1, "partido": d["partidos"][i]["partido"], "p_mesa": round(max(mesa[i]), 3),
                           "segundo": segundo[i]} for i in favs],
            "quitadas": quitar, "nuevas": nuevas, "antes": {k: round(v, 4) for k, v in ref.items()},
            "despues": {k: round(v, 4) for k, v in r.items()}, "aplica": r["p13"] >= ref["p13"] - 0.0005}
    return info, None


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("jornada"); ap.add_argument("--guardar", action="store_true")
    a = ap.parse_args()
    d = json.load(open(a.jornada, encoding="utf-8"))
    info, motivo = seguro(d)
    if info is None:
        print("Seguro de favoritos: no aplica —", motivo); return
    for f in info["favoritos"]:
        print(f"  favorito {f['n']:>2} {f['partido']:28s} {100 * f['p_mesa']:.0f} %  2.º signo {f['segundo']}")
    print("  quitadas:", info["quitadas"]); print("  nuevas:  ", info["nuevas"])
    print("  P(≥13) / P(≥12) / P(≥10): antes", info["antes"], "después", info["despues"])
    print("  → APLICA" if info["aplica"] else "  → no aplica (baja la P(≥13))")
    if a.guardar and info["aplica"]:
        bm = d["boleto_mesa"]
        swap = dict(zip(info["quitadas"], info["nuevas"]))
        bm["columnas"] = [swap.get(c, c) for c in bm["columnas"]]
        if bm.get("boletos"):
            bm["boletos"] = [[swap.get(c, c) for c in b] for b in bm["boletos"]]
        bm["seguro_favoritos"] = info
        bm["p13_simulada"] = info["despues"]["p13"]
        json.dump(d, open(a.jornada, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("Guardado en", a.jornada)


if __name__ == "__main__":
    main()
