"""Cuotas históricas frente a resultados: Primera (SP1) y Segunda (SP2), 2005-2026.

Fuente: football-data.co.uk vía github.com/xgabora/Club-Football-Match-Data-2000-2025 (OddHome/Draw/Away, cuota
de mercado, clase B). Mide calibración por tramos, la X, el sesgo favorito-sorpresa y la distribución del Pleno.
Cada efecto se mide en dos mitades (2005-2015 y 2016-2026): solo cuenta si va en el mismo sentido en las dos.
Uso: python3 -I herramientas/backtest_cuotas.py ruta/Matches.csv > datos/backtest_cuotas.json
"""
import csv
import json
import sys
from collections import defaultdict


def leer(ruta):
    for r in csv.DictReader(open(ruta, encoding="utf-8")):
        if r["Division"] not in ("SP1", "SP2") or r["MatchDate"] < "2005-07-01":
            continue
        try:
            o = [float(r["OddHome"]), float(r["OddDraw"]), float(r["OddAway"])]
            g = int(float(r["FTHome"])), int(float(r["FTAway"]))
        except ValueError:
            continue
        if min(o) <= 1:
            continue
        inv = [1 / x for x in o]
        s = sum(inv)
        yield {"div": r["Division"], "fecha": r["MatchDate"], "p": [x / s for x in inv], "margen": s - 1,
               "res": 0 if g[0] > g[1] else 1 if g[0] == g[1] else 2, "g": g}


def pleno(g):
    f = lambda x: "M" if x >= 3 else str(x)  # noqa: E731
    return f(g[0]) + "-" + f(g[1])


def main(ruta):
    ps = list(leer(ruta))
    mitad = lambda p: "A 2005-15" if p["fecha"] < "2016-07-01" else "B 2016-26"  # noqa: E731
    calib = defaultdict(lambda: [0, 0.0, 0])   # (div, sel, tramo, mitad)
    xfav = defaultdict(lambda: [0, 0.0, 0])    # (div, tramo favorito, mitad)
    plen = defaultdict(lambda: defaultdict(int))
    for p in ps:
        for k, sel in enumerate("1X2"):
            t = min(int(p["p"][k] * 10), 9)
            for m in (mitad(p), "Todo"):
                c = calib[(p["div"], sel, t, m)]
                c[0] += 1; c[1] += p["p"][k]; c[2] += p["res"] == k  # noqa: E702
        fav = max(p["p"][0], p["p"][2])
        tf = "<45" if fav < .45 else "45-55" if fav < .55 else "55-65" if fav < .65 else "65+"
        for m in (mitad(p), "Todo"):
            c = xfav[(p["div"], tf, m)]
            c[0] += 1; c[1] += p["p"][1]; c[2] += p["res"] == 1  # noqa: E702
        plen[(p["div"], tf)][pleno(p["g"])] += 1
    fila = lambda c: {"n": c[0], "esperado": round(c[1] / c[0], 4), "real": round(c[2] / c[0], 4),  # noqa: E731
                      "dif": round((c[2] - c[1]) / c[0], 4)}
    out = {"fuente": "football-data.co.uk vía xgabora (cuota de mercado OddHome/Draw/Away), clase B",
           "partidos": len(ps), "margen_medio": round(sum(p["margen"] for p in ps) / len(ps), 4),
           "calibracion": [{"div": d, "sel": s, "tramo": f"{t * 10}-{t * 10 + 10} %", "mitad": m, **fila(c)}
                           for (d, s, t, m), c in sorted(calib.items()) if c[0] >= 30],
           "x_por_favorito": [{"div": d, "favorito": t, "mitad": m, **fila(c)} for (d, t, m), c in sorted(xfav.items())],
           "pleno": [{"div": d, "favorito": t, "n": sum(v.values()),
                      "top": [[k, round(n / sum(v.values()), 4)] for k, n in sorted(v.items(), key=lambda x: -x[1])[:4]]}
                     for (d, t), v in sorted(plen.items())]}
    json.dump(out, sys.stdout, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main(sys.argv[1])
