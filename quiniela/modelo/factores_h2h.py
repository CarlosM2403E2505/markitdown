#!/usr/bin/env python3
"""¿Aportan algo los enfrentamientos previos y el «mismo partido la temporada pasada» sobre las cuotas? (25/11/2026)

Carlos (25/11): «datos, datos y más datos: enfrentamientos previos, qué pasó la temporada pasada…».
Datos: football-data.co.uk vía el espejo de GitHub (xgabora, clase B), Primera y Segunda con cuota 1X2.
Método: logit multinomial con log(P casas sin margen) como base. Se ajusta en 2005-2015 y se mide en 2016-2026
(fuera de muestra). Un factor cuenta solo si baja el log-loss fuera de muestra frente a «casas + recalibración».

Factores (todos con datos anteriores a la fecha del partido):
  h2h_dif   (victorias local − victorias visitante)/n en los últimos ≤ 6 duelos (cualquier campo, 6 años)
  h2h_x     proporción de empates en esos duelos
  ult_sig   resultado del mismo partido (mismo campo) la temporada pasada: +1 local, 0 X, −1 visitante
Uso: python3 -I modelo/factores_h2h.py Matches.csv [--j25 jornadas/j25/j25.json] > datos/factores_h2h.json
"""
import csv, json, math, sys
from collections import defaultdict
import numpy as np
from scipy.optimize import minimize

NOMBRES = {"Betis": "Betis", "Rayo": "Vallecano", "Málaga": "Malaga", "Athletic": "Ath Bilbao", "Elche": "Elche",
           "Atlético": "Ath Madrid", "Real Madrid": "Real Madrid", "Alavés": "Alaves", "Valencia": "Valencia",
           "Osasuna": "Osasuna", "Deportivo": "La Coruna", "Barcelona": "Barcelona", "Celta": "Celta",
           "Villarreal": "Villarreal", "Real Sociedad": "Sociedad", "Sevilla": "Sevilla", "Las Palmas": "Las Palmas",
           "Andorra": "Andorra", "Albacete": "Albacete", "Tenerife": "Tenerife", "Eibar": "Eibar", "Burgos": "Burgos",
           "Granada": "Granada", "Ceuta": "Ceuta", "Mallorca": "Mallorca", "Castellón": "Castellon",
           "Almería": "Almeria", "Sporting": "Sp Gijon", "Espanyol": "Espanol", "Getafe": "Getafe"}


def temporada(f):
    return int(f[:4]) - (1 if f[5:7] < "07" else 0)


def leer(ruta):
    out = []
    for r in csv.DictReader(open(ruta, encoding="utf-8")):
        if r["Division"] not in ("SP1", "SP2") or not r["FTResult"]:
            continue
        try:
            o = [float(r["OddHome"]), float(r["OddDraw"]), float(r["OddAway"])]
            p = [1 / x for x in o]; s = sum(p); p = [x / s for x in p]
        except (ValueError, ZeroDivisionError):
            p = None
        out.append({"f": r["MatchDate"], "l": r["HomeTeam"], "v": r["AwayTeam"], "r": "HDA".index(r["FTResult"]),
                    "gl": r["FTHome"], "gv": r["FTAway"], "p": p, "div": r["Division"]})
    return sorted(out, key=lambda x: x["f"])


def factores(hist, l, v, fecha):
    """hist: lista de partidos anteriores a la fecha entre l y v (cualquier campo)."""
    t = temporada(fecha)
    duelos = [h for h in hist if h["f"] < fecha and temporada(h["f"]) >= t - 6][-6:]
    n = len(duelos)
    wl = sum((h["l"] == l and h["r"] == 0) or (h["v"] == l and h["r"] == 2) for h in duelos)
    wv = sum((h["l"] == v and h["r"] == 0) or (h["v"] == v and h["r"] == 2) for h in duelos)
    x = sum(h["r"] == 1 for h in duelos)
    ult = [h for h in hist if h["l"] == l and h["v"] == v and temporada(h["f"]) == t - 1]
    return {"n": n, "h2h_dif": (wl - wv) / n if n else 0.0, "h2h_x": x / n if n else 0.0,
            "ult_sig": (1 - ult[-1]["r"]) if ult else 0.0, "hay_ult": 1.0 if ult else 0.0, "duelos": duelos, "ult": ult[-1] if ult else None}


def construir(partidos):
    por_par = defaultdict(list); filas = []
    for m in partidos:
        k = frozenset((m["l"], m["v"]))
        if m["p"]:
            f = factores(por_par[k], m["l"], m["v"], m["f"])
            filas.append((m, f))
        por_par[k].append(m)
    return filas, por_par


def ll(theta, X, LP, y, k):
    W = theta[:2 + 2 * k].reshape(2, 1 + k)  # logits de 1 y 2 frente a X
    z = np.zeros((len(y), 3)); z[:, 0] = LP[:, 0] - LP[:, 1] + X @ W[0]; z[:, 2] = LP[:, 2] - LP[:, 1] + X @ W[1]
    z -= z.max(axis=1, keepdims=True); lp = z - np.log(np.exp(z).sum(axis=1, keepdims=True))
    return -lp[np.arange(len(y)), y].mean()


def medir(filas, cols):
    def mat(sel):
        X = np.array([[1.0] + [f[c] for c in cols] for _, f in sel]); LP = np.log(np.array([m["p"] for m, _ in sel]))
        y = np.array([m["r"] for m, _ in sel]); return X, LP, y
    tr = [(m, f) for m, f in filas if temporada(m["f"]) <= 2015 and f["n"] >= 1]
    te = [(m, f) for m, f in filas if temporada(m["f"]) >= 2016 and f["n"] >= 1]
    Xtr, Ltr, ytr = mat(tr); Xte, Lte, yte = mat(te)
    k = len(cols)
    base = minimize(ll, np.zeros(2), args=(Xtr[:, :1], Ltr, ytr, 0)).x
    mod = minimize(ll, np.zeros(2 + 2 * k), args=(Xtr, Ltr, ytr, k)).x
    casas = ll(np.zeros(2), Xte[:, :1], Lte, yte, 0)
    b = ll(base, Xte[:, :1], Lte, yte, 0); m_ = ll(mod, Xte, Lte, yte, k)
    # mitades del test para ver si se repite
    mitad = [temporada(m["f"]) <= 2020 for m, _ in te]
    idx = [np.array(mitad), ~np.array(mitad)]
    mit = [round(float(ll(base, Xte[i][:, :1], Lte[i], yte[i], 0) - ll(mod, Xte[i], Lte[i], yte[i], k)), 5) for i in idx]
    return {"factores": cols, "n_ajuste": len(tr), "n_prueba": len(te), "ll_casas": round(float(casas), 5),
            "ll_casas_recal": round(float(b), 5), "ll_con_factor": round(float(m_), 5),
            "mejora": round(float(b - m_), 5), "mejora_2016_20_y_2021_26": mit, "coef": [round(float(x), 4) for x in mod]}


def main():
    partidos = leer(sys.argv[1])
    filas, por_par = construir(partidos)
    res = {"fuente": "football-data.co.uk (espejo xgabora, clase B), SP1+SP2", "hasta": partidos[-1]["f"],
           "pruebas": [medir(filas, c) for c in (["h2h_dif"], ["h2h_x"], ["ult_sig", "hay_ult"], ["h2h_dif", "h2h_x", "ult_sig", "hay_ult"])]}
    if "--j25" in sys.argv:
        d = json.load(open(sys.argv[sys.argv.index("--j25") + 1], encoding="utf-8"))
        res["j25"] = []
        for x in d["partidos"] + [dict(d["pleno"], n=15)]:
            l, v = [NOMBRES[t.strip()] for t in x["partido"].split("–")]
            f = factores(por_par[frozenset((l, v))], l, v, "2026-11-28")
            res["j25"].append({"n": x["n"], "partido": x["partido"], "duelos_6": f["n"],
                               "h2h": " · ".join(f'{h["f"][5:7]}/{h["f"][2:4]} ' + (f'{int(float(h["gl"]))}-{int(float(h["gv"]))}' if h["l"] == l else f'{int(float(h["gv"]))}-{int(float(h["gl"]))} fuera') for h in f["duelos"]),
                               "balance": f"{sum((h['l'] == l and h['r'] == 0) or (h['v'] == l and h['r'] == 2) for h in f['duelos'])}-"
                                          f"{sum(h['r'] == 1 for h in f['duelos'])}-"
                                          f"{sum((h['l'] == v and h['r'] == 0) or (h['v'] == v and h['r'] == 2) for h in f['duelos'])}",
                               "temporada_pasada": (f'{int(float(f["ult"]["gl"]))}-{int(float(f["ult"]["gv"]))}' if f["ult"] else "no se jugó")})
    json.dump(res, sys.stdout, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
