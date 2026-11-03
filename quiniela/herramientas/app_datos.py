#!/usr/bin/env python3
"""Genera las tablas de la app «Control Quiniela» a partir de los archivos del proyecto.

Lee jornadas/jNN/jNN.json (y la foto de cuotas bet365_*.json si existe),
app/historial.json y app/bajas.json, y escribe en app/datos/:
jornadas.json, partidos.json, sueltas.json y bajas.json.

Uso: python3 herramientas/app_datos.py   (desde la carpeta quiniela)
"""
import glob
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import quiniela_calc as qc  # noqa: E402

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _leer(ruta):
    with open(ruta, encoding="utf-8") as f:
        return json.load(f)


def _mercado(carpeta):
    fotos = sorted(glob.glob(os.path.join(carpeta, "bet365_*.json")))
    if not fotos:
        return {}
    cuotas = _leer(fotos[-1]).get("cuotas", {})
    salida = {}
    for n, c in cuotas.items():
        inv = [1 / x for x in c]
        salida[int(n)] = [v / sum(inv) for v in inv]
    return salida


def jornada_desde_json(ruta):
    d = _leer(ruta)
    n_j = d["jornada"]
    partidos = d["partidos"]
    probs = [p["p"] for p in partidos]
    mercado = _mercado(os.path.dirname(ruta))
    forzados = qc._forzados(partidos)
    _, elegido = qc.comparar_sistemas(probs, forzados, d.get("presupuesto", 12), (d.get("publico") or {}).get("columna"))
    cols, dist = elegido["columnas"], elegido["dist"]
    # Signos que aparecen en las columnas del boleto, partido a partido ("1", "12", "1X2"...).
    signos_boleto = {i: "".join(s for s in qc.SIGNOS if any(c[i] == s for c in cols)) for i in range(len(probs))}

    filas = []
    for i, p in enumerate(partidos):
        m = mercado.get(p.get("n", i + 1))
        resultado = p.get("resultado")
        signo_boleto = signos_boleto[i]
        filas.append({
            "jornada": n_j, "n": p.get("n", i + 1), "partido": p["partido"],
            "competicion": p.get("competicion"), "dia": p.get("dia"),
            "p1": round(p["p"][0], 4), "px": round(p["p"][1], 4), "p2": round(p["p"][2], 4),
            "signo_modelo": qc.SIGNOS[qc._orden(p["p"])[0]], "signo_boleto": signo_boleto,
            "riesgo": p.get("riesgo") or qc._riesgo(p["p"]), "veto": bool(p.get("veto_unico")),
            "m1": round(m[0], 4) if m else None, "mx": round(m[1], 4) if m else None,
            "m2": round(m[2], 4) if m else None,
            "resultado": resultado,
            "acierto_boleto": (resultado in signo_boleto) if resultado else None,
        })

    pleno = d.get("pleno")
    pleno_jugado = pleno_resultado = None
    if pleno:
        pleno_jugado = pleno.get("pleno_jugado")
        pleno_resultado = pleno.get("resultado_pleno")
        m = mercado.get(pleno.get("n", 15))
        filas.append({
            "jornada": n_j, "n": 15, "partido": pleno["partido"] + " (Pleno)",
            "competicion": pleno.get("competicion"), "dia": pleno.get("dia"),
            "p1": round(pleno["p"][0], 4), "px": round(pleno["p"][1], 4), "p2": round(pleno["p"][2], 4),
            "signo_modelo": qc.SIGNOS[qc._orden(pleno["p"])[0]], "signo_boleto": pleno_jugado,
            "riesgo": "—", "veto": False,
            "m1": round(m[0], 4) if m else None, "mx": round(m[1], 4) if m else None,
            "m2": round(m[2], 4) if m else None,
            "resultado": pleno_resultado,
            "acierto_boleto": (pleno_resultado == pleno_jugado) if pleno_resultado else None,
        })

    sueltas = []
    for k, s in enumerate(d.get("sueltas", []), 1):
        sueltas.append({"jornada": n_j, "n": k, "apuesta": s["apuesta"], "partido": s.get("partido"),
                        "p": s["p"], "resultado": s.get("resultado")})
    acertadas = [s for s in sueltas if s["resultado"] is not None]

    jugados = [f for f in filas if f["n"] <= 14 and f["resultado"]]
    resumen = {
        "jornada": n_j, "fechas": d.get("fechas"), "tipo": d.get("tipo"),
        "estado": "Cerrada" if len(jugados) == 14 else d.get("estado", "Pronóstico"),
        "boleto": ("16 columnas más probables, sin la del público" if "público" in elegido["nombre"]
                   else elegido["nombre"].split(" · ", 1)[1].capitalize()), "coste": d.get("presupuesto", 12),
        "p14": round(qc.al_menos(dist, 14), 6), "p13": round(qc.al_menos(dist, 13), 5),
        "p10": round(qc.al_menos(dist, 10), 4),
        "mejor_columna": d.get("mejor_columna"),
        "sueltas_aciertos": sum(bool(s["resultado"]) for s in acertadas) if acertadas else None,
        "sueltas_total": len(sueltas) if acertadas else None,
        "sueltas_p_todas": round(_producto(s["p"] for s in sueltas), 4) if sueltas else None,
        "pleno_jugado": pleno_jugado, "pleno_resultado": pleno_resultado,
        "log_loss_modelo": round(qc.puntuar(partidos)["log_loss"], 4) if len(jugados) == 14 else None,
        "log_loss_mercado": d.get("log_loss_mercado"),
    }
    return resumen, filas, sueltas


def _producto(valores):
    total = 1.0
    for v in valores:
        total *= v
    return total


def main():
    historial = _leer(os.path.join(RAIZ, "app", "historial.json"))["jornadas"]
    jornadas, partidos, sueltas = list(historial), [], []
    for ruta in sorted(glob.glob(os.path.join(RAIZ, "jornadas", "j*", "j[0-9]*.json"))):
        if not os.path.basename(ruta)[1:-5].isdigit():
            continue
        r, f, s = jornada_desde_json(ruta)
        jornadas = [j for j in jornadas if j["jornada"] != r["jornada"]] + [r]
        partidos += f
        sueltas += s
    jornadas.sort(key=lambda j: j["jornada"])
    bajas = _leer(os.path.join(RAIZ, "app", "bajas.json"))["bajas"]

    salida = os.path.join(RAIZ, "app", "datos")
    os.makedirs(salida, exist_ok=True)
    for nombre, filas in (("jornadas", jornadas), ("partidos", partidos), ("sueltas", sueltas), ("bajas", bajas)):
        with open(os.path.join(salida, f"{nombre}.json"), "w", encoding="utf-8") as f:
            json.dump({"rows": filas}, f, ensure_ascii=False, indent=1)
        print(f"{nombre}: {len(filas)} filas")


if __name__ == "__main__":
    main()
