"""Estudio de probabilidad de sorpresas (23/11/2026, petición de Carlos tras Rayo y Tenerife en la J23).

¿Qué favoritos pierden o empatan MÁS de lo que dice la cuota? Para cada factor medible se compara
la sorpresa real (el favorito no gana) con la que daba el mercado sin margen (1 - p_fav).
Un factor solo cuenta si va en el mismo sentido en las dos mitades (2005-15 y 2016-26) de España
y también en las otras cuatro grandes ligas (control independiente).

Datos: football-data.co.uk vía github.com/xgabora/Club-Football-Match-Data-2000-2025 (clase B).
Uso: python3 -I modelo/sorpresas.py ruta/Matches.csv > datos/sorpresas.json
"""
import csv
import json
import math
import sys
from collections import defaultdict

ESP = ("SP1", "SP2")
OTRAS = ("E0", "I1", "D1", "F1")


def leer(ruta):
    ultimo = {}  # (div, equipo) -> fecha del partido anterior
    filas = []
    for r in csv.DictReader(open(ruta, encoding="utf-8")):
        if r["Division"] not in ESP + OTRAS or r["MatchDate"] < "2005-07-01":
            continue
        try:
            o = [float(r["OddHome"]), float(r["OddDraw"]), float(r["OddAway"])]
            g = int(float(r["FTHome"])), int(float(r["FTAway"]))
        except ValueError:
            continue
        if min(o) <= 1:
            continue
        filas.append((r, o, g))
    filas.sort(key=lambda x: x[0]["MatchDate"])
    from datetime import date
    for r, o, g in filas:
        f = date.fromisoformat(r["MatchDate"])
        dias = []
        for eq in (r["HomeTeam"], r["AwayTeam"]):
            k = (r["Division"], eq)
            dias.append((f - ultimo[k]).days if k in ultimo else None)
            ultimo[k] = f
        inv = [1 / x for x in o]
        s = sum(inv)
        p = [x / s for x in inv]
        fav = 0 if p[0] >= p[2] else 2
        pf = p[fav]
        if not 0.45 <= pf < 0.70:
            continue
        res = 0 if g[0] > g[1] else 1 if g[0] == g[1] else 2

        def num(c):
            try:
                return float(r[c])
            except ValueError:
                return None
        loc = fav == 0
        ff = num("Form5Home" if loc else "Form5Away")
        fr = num("Form5Away" if loc else "Form5Home")
        ef, er = (num("HomeElo"), num("AwayElo")) if loc else (num("AwayElo"), num("HomeElo"))
        # probabilidad Elo del favorito (sin X): ventaja de campo 65 puntos
        pe = None
        if ef and er:
            d = (ef - er) + (65 if loc else -65)
            pe = 1 / (1 + 10 ** (-d / 400))
        o25 = num("Over25")
        u25 = num("Under25")
        p_over = (1 / o25) / (1 / o25 + 1 / u25) if o25 and u25 and o25 > 1 and u25 > 1 else None
        mes = int(r["MatchDate"][5:7])
        yield {
            "div": r["Division"], "esp": r["Division"] in ESP, "mitad": 0 if r["MatchDate"] < "2015-07-01" else 1,
            "pf": pf, "px": p[1], "sorpresa": res != fav, "x": res == 1,
            "rasgos": {
                "favorito local": loc,
                "favorito visitante": not loc,
                "Segunda División": r["Division"] == "SP2",
                "favorito 45-55 %": pf < 0.55,
                "favorito 55-70 %": pf >= 0.55,
                "favorito en mala forma (≤5 de 15)": ff is not None and ff <= 5,
                "favorito en gran forma (≥12 de 15)": ff is not None and ff >= 12,
                "rival en buena forma (≥10 de 15)": fr is not None and fr >= 10,
                "rival en mala forma (≤3 de 15)": fr is not None and fr <= 3,
                "Elo ve al favorito ≥8 pt por debajo de la cuota": pe is not None and pf / (1 - p[1]) - pe >= 0.08,
                "Elo ve al favorito ≥8 pt por encima de la cuota": pe is not None and pe - pf / (1 - p[1]) >= 0.08,
                "pocos goles esperados (P over 2,5 < 45 %)": p_over is not None and p_over < 0.45,
                "muchos goles esperados (P over 2,5 > 55 %)": p_over is not None and p_over > 0.55,
                "favorito con ≤3 días de descanso": dias[0 if loc else 1] is not None and dias[0 if loc else 1] <= 3,
                "rival con ≥3 días más de descanso": None not in dias and (dias[1 if loc else 0] - dias[0 if loc else 1]) >= 3
                and dias[0 if loc else 1] <= 10,
                "agosto-septiembre": mes in (8, 9),
                "abril-mayo (final de liga)": mes in (4, 5, 6),
                "mercado da X ≥ 29 %": p[1] >= 0.29,
                "favorito 45-55 % y pocos goles esperados": pf < 0.55 and p_over is not None and p_over < 0.45,
                "favorito 45-55 %, pocos goles y mala forma": pf < 0.55 and p_over is not None and p_over < 0.45
                and ff is not None and ff <= 5,
            },
        }


def resumen(ps):
    n = len(ps)
    if n == 0:
        return None
    dada = sum(1 - p["pf"] for p in ps) / n
    real = sum(p["sorpresa"] for p in ps) / n
    var = sum((1 - p["pf"]) * p["pf"] for p in ps) / n
    z = (real - dada) / math.sqrt(var / n)
    return {"n": n, "sorpresa_dada": round(dada, 3), "sorpresa_real": round(real, 3),
            "dif": round(real - dada, 3), "z": round(z, 2),
            "x_dada": round(sum(p["px"] for p in ps) / n, 3), "x_real": round(sum(p["x"] for p in ps) / n, 3)}


def main(ruta):
    todos = list(leer(ruta))
    nombres = list(todos[0]["rasgos"])
    out = {"n_esp": sum(p["esp"] for p in todos), "n_otras": sum(not p["esp"] for p in todos),
           "base": {}, "rasgos": {}}
    grupos = {"esp_2005_15": lambda p: p["esp"] and p["mitad"] == 0, "esp_2016_26": lambda p: p["esp"] and p["mitad"] == 1,
              "otras_ligas": lambda p: not p["esp"]}
    for g, f in grupos.items():
        out["base"][g] = resumen([p for p in todos if f(p)])
    for nm in nombres:
        fila = {g: resumen([p for p in todos if f(p) and p["rasgos"][nm]]) for g, f in grupos.items()}
        for g in grupos:
            if fila[g]:  # diferencia frente a la base del grupo (el mercado ya acierta de media)
                fila[g]["dif_rel"] = round(fila[g]["dif"] - out["base"][g]["dif"], 3)
        difs = [fila[g]["dif_rel"] for g in grupos if fila[g]]
        fila["estable"] = len(difs) == 3 and (all(d > 0.005 for d in difs) or all(d < -0.005 for d in difs))
        out["rasgos"][nm] = fila
    # combinaciones de los rasgos estables que suben la sorpresa (España, todas las temporadas)
    suben = [nm for nm in nombres if out["rasgos"][nm]["estable"] and out["rasgos"][nm]["esp_2016_26"]["dif_rel"] > 0
             and "," not in nm and " y " not in nm]
    out["suben_sorpresa"] = suben
    puntos = defaultdict(list)
    for p in todos:
        if p["esp"]:
            puntos[min(sum(p["rasgos"][nm] for nm in suben), 3)].append(p)
    out["por_n_alertas_esp"] = {str(k): resumen(v) for k, v in sorted(puntos.items())}
    puntos = defaultdict(list)
    for p in todos:
        if not p["esp"]:
            puntos[min(sum(p["rasgos"][nm] for nm in suben), 3)].append(p)
    out["por_n_alertas_otras"] = {str(k): resumen(v) for k, v in sorted(puntos.items())}
    json.dump(out, sys.stdout, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main(sys.argv[1])
