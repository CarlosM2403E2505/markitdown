#!/usr/bin/env python3
"""Tabla de equipos para la app «Control Quiniela»: todos los equipos de Primera, Segunda y
Liga F de esta temporada, y las selecciones de la jornada en curso.

Para cada equipo: clasificación con los partidos que hay en los datos, últimos 5 resultados,
fuerza de ataque y de defensa del modelo (100 = media de su liga), próximo partido en la
quiniela y bajas registradas. Escribe app/datos/equipos.json.

Uso: python3 herramientas/app_equipos.py   (desde la carpeta quiniela; tarda unos segundos)
"""
import csv
import glob
import importlib.util
import json
import math
import os
from datetime import date

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPORADA = {"es.1:2026-27": "Primera", "es.2:2026-27": "Segunda"}
# Nombres del dataset → nombres para la app.
BONITO = {
    "athletic bilbao": "Athletic", "atletico": "Atlético", "barcelona": "Barcelona", "betis": "Betis", "celta": "Celta",
    "deportivo alaves": "Alavés", "deportivo coruna": "Deportivo", "elche": "Elche", "espanyol barcelona": "Espanyol",
    "getafe": "Getafe", "levante": "Levante", "malaga": "Málaga", "osasuna": "Osasuna", "racing santander": "Racing",
    "rayo vallecano": "Rayo Vallecano", "real madrid": "Real Madrid", "real sociedad": "Real Sociedad", "sevilla": "Sevilla",
    "valencia": "Valencia", "villarreal": "Villarreal", "ad ceuta": "Ceuta", "albacete": "Albacete", "almeria": "Almería",
    "andorra": "Andorra", "burgos": "Burgos", "cadiz": "Cádiz", "castellon": "Castellón", "celta fortuna": "Celta Fortuna",
    "cordoba": "Córdoba", "eibar": "Eibar", "eldense": "Eldense", "girona": "Girona", "granada": "Granada",
    "las palmas": "Las Palmas", "leganes": "Leganés", "mallorca": "Mallorca", "real oviedo": "Oviedo",
    "real sociedad b": "Real Sociedad B", "real valladolid": "Valladolid", "sabadell": "Sabadell",
    "sporting gijon": "Sporting", "tenerife": "Tenerife",
}
LIGAF_BONITO = {"Atletico": "Atlético", "Alaves": "Alavés", "Logrono": "Logroño"}


def _ultimo(patron):
    rutas = sorted(glob.glob(os.path.join(RAIZ, patron)))
    return rutas[-1] if rutas else None


def _clasificacion(partidos):
    """partidos: lista de (fecha, local, visitante, gl, gv). Devuelve dict equipo -> estadísticas."""
    t = {}
    for fecha, h, a, gh, ga in sorted(partidos):
        for eq, gf, gc in ((h, gh, ga), (a, ga, gh)):
            s = t.setdefault(eq, {"pj": 0, "g": 0, "e": 0, "p": 0, "gf": 0, "gc": 0, "forma": []})
            s["pj"] += 1; s["gf"] += gf; s["gc"] += gc
            r = "V" if gf > gc else ("E" if gf == gc else "D")
            s[{"V": "g", "E": "e", "D": "p"}[r]] += 1
            s["forma"].append(r)
    for s in t.values():
        s["pts"] = 3 * s["g"] + s["e"]
        s["forma"] = "".join(s["forma"][-5:])
    return t


def _posiciones(tabla):
    orden = sorted(tabla, key=lambda e: (-tabla[e]["pts"], -(tabla[e]["gf"] - tabla[e]["gc"]), -tabla[e]["gf"], e))
    return {e: i + 1 for i, e in enumerate(orden)}


def _fuerzas_modelo(ruta_json, equipos):
    """Ataque y defensa del modelo multi-liga, relativos a la media de los equipos dados (100 = media)."""
    spec = importlib.util.spec_from_file_location("em", os.path.join(RAIZ, "modelo", "euro_model.py"))
    em = importlib.util.module_from_spec(spec); spec.loader.exec_module(em)
    with open(ruta_json, encoding="utf-8") as f:
        ms = json.load(f)["matches"]
    ref = max(date.fromisoformat(m["date"]) for m in ms)
    mod = em.EuroPoisson(xi=0.0015, ridge=10, scale=1.05, blend=0.2, hier=True).fit(ms, ref_date=ref)
    salida = {}
    for liga, lista in equipos.items():
        dentro = [e for e in lista if e in mod.idx]
        if not dentro:
            continue
        ma = sum(mod.att[mod.idx[e]] for e in dentro) / len(dentro)
        md = sum(mod.dfn[mod.idx[e]] for e in dentro) / len(dentro)
        for e in dentro:
            salida[e] = (round(100 * math.exp(mod.att[mod.idx[e]] - ma)), round(100 * math.exp(mod.dfn[mod.idx[e]] - md)))
    return salida


def _fuerzas_ligaf():
    spec = importlib.util.spec_from_file_location("lfm", os.path.join(RAIZ, "modelo", "ligaf_modelo.py"))
    lfm = importlib.util.module_from_spec(spec); spec.loader.exec_module(lfm)
    lf = lfm.ajustar()
    ma = sum(lf["att"].values()) / len(lf["att"]); md = sum(lf["dfn"].values()) / len(lf["dfn"])
    return {e: (round(100 * math.exp(lf["att"][e] - ma)), round(100 * math.exp(lf["dfn"][e] - md))) for e in lf["att"]}


def _proximos():
    """Próximo partido en la quiniela de cada equipo (jornada más alta con JSON)."""
    ruta = _ultimo("jornadas/j*/j[0-9][0-9].json")
    if not ruta:
        return {}, None
    with open(ruta, encoding="utf-8") as f:
        d = json.load(f)
    prox = {}
    for x in d["partidos"] + ([dict(d["pleno"], n=15)] if d.get("pleno") else []):
        partes = x["partido"].replace(" (Pleno)", "").split(" – ")
        for i, nombre in enumerate(partes):
            p = x.get("p") or [None, None, None]
            prox[nombre.replace(" F", "").strip() + (" F" if nombre.endswith(" F") else "")] = {
                "jornada": d["jornada"], "n": x.get("n"), "partido": x["partido"], "condicion": "local" if i == 0 else "visitante",
                "p_ganar": p[0] if i == 0 else p[2]}
    return prox, d["jornada"]


def construir():
    ruta_csv = _ultimo("datos/euro_j*.csv"); ruta_json = ruta_csv.replace(".csv", ".json")
    porliga = {"Primera": [], "Segunda": []}
    with open(ruta_csv, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["competicion"] in TEMPORADA:
                porliga[TEMPORADA[r["competicion"]]].append((r["fecha"], r["local"], r["visitante"], int(r["goles_local"]), int(r["goles_visitante"])))
    with open(os.path.join(RAIZ, "datos", "ligaf.json"), encoding="utf-8") as f:
        lf = [(str(i).zfill(4), p["local"], p["visitante"], p["goles_local"], p["goles_visitante"])
              for i, p in enumerate(json.load(f)["partidos"]) if p["temporada"] == "2026-27"]
    with open(os.path.join(RAIZ, "app", "bajas.json"), encoding="utf-8") as f:
        bajas = json.load(f)["bajas"]
    prox, jornada = _proximos()

    fuerzas = _fuerzas_modelo(ruta_json, {k: sorted({t for p in v for t in p[1:3]}) for k, v in porliga.items()})
    fuerzas_lf = _fuerzas_ligaf()
    filas = []
    for comp, partidos in (("Primera", porliga["Primera"]), ("Segunda", porliga["Segunda"]), ("Liga F", lf)):
        tabla = _clasificacion(partidos); pos = _posiciones(tabla)
        for eq, s in tabla.items():
            nombre = BONITO.get(eq, LIGAF_BONITO.get(eq, eq))
            clave = nombre + " F" if comp == "Liga F" else nombre
            at, de = (fuerzas_lf if comp == "Liga F" else fuerzas).get(eq, (None, None))
            px = prox.get(clave) or {}
            nb = [b for b in bajas if b["equipo"].lower().startswith(nombre.lower()) and comp != "Liga F"]
            filas.append({"id": f"{comp}|{nombre}", "competicion": comp, "equipo": nombre, "posicion": pos[eq],
                          "pj": s["pj"], "g": s["g"], "e": s["e"], "p": s["p"], "gf": s["gf"], "gc": s["gc"],
                          "dg": s["gf"] - s["gc"], "pts": s["pts"], "forma": s["forma"],
                          "ataque": at, "defensa": de,
                          "proximo": px.get("partido"), "proximo_n": px.get("n"), "p_ganar_proximo": px.get("p_ganar"),
                          "bajas": len([b for b in nb if b["estado"] == "Confirmada"]) or None,
                          "dudas": len([b for b in nb if b["estado"] == "Duda"]) or None})
    # Selecciones de la jornada en curso, con su Elo.
    ruta_j = _ultimo("jornadas/j*/j[0-9][0-9].json")
    if ruta_j:
        with open(ruta_j, encoding="utf-8") as f:
            d = json.load(f)
        elo = {"España": 2287, "Inglaterra": 2146, "Bélgica": 1956, "Italia": 1910}  # eloratings.net, 11/11/2026
        for x in d["partidos"] + [dict(d["pleno"], n=15)]:
            if x.get("competicion") != "Selecciones":
                continue
            for i, nombre in enumerate(x["partido"].split(" – ")):
                if nombre in elo:
                    filas.append({"id": f"Selecciones|{nombre}", "competicion": "Selecciones", "equipo": nombre, "posicion": None,
                                  "pj": None, "g": None, "e": None, "p": None, "gf": None, "gc": None, "dg": None, "pts": None,
                                  "forma": None, "ataque": None, "defensa": None, "elo": elo[nombre],
                                  "proximo": x["partido"], "proximo_n": x["n"], "p_ganar_proximo": x["p"][0] if i == 0 else x["p"][2],
                                  "bajas": None, "dudas": None})
    for fila in filas:
        fila.setdefault("elo", None)
    filas.sort(key=lambda r: (["Primera", "Segunda", "Liga F", "Selecciones"].index(r["competicion"]), r["posicion"] or 0, r["equipo"]))
    salida = os.path.join(RAIZ, "app", "datos", "equipos.json")
    with open(salida, "w", encoding="utf-8") as f:
        json.dump({"rows": filas, "datos": os.path.basename(ruta_csv), "jornada": jornada}, f, ensure_ascii=False, indent=1)
    return filas


if __name__ == "__main__":
    filas = construir()
    from collections import Counter
    print(len(filas), "equipos:", dict(Counter(r["competicion"] for r in filas)))
