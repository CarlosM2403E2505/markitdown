#!/usr/bin/env python3
"""Exporta los datos de la mesa a CSV (UTF-8, comas, fechas AAAA-MM-DD) en exportacion/datos_para_mesa.zip.

No rellena nada: un dato que no está en los archivos de origen queda vacío.
Uso: python3 herramientas/exportar.py   (desde la carpeta quiniela)
"""
import csv
import json
import os
import sys
import zipfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import quiniela_calc as qc  # noqa: E402

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SALIDA = os.path.join(RAIZ, "exportacion", "datos_para_mesa")
J19 = os.path.join(RAIZ, "jornadas", "j19")
OBTENIDO = "2026-11-02"  # día en que llegaron los archivos de la mesa a esta sesión
MESA = "Mesa de claude.ai, paquete quiniela_mesa_j19.zip"
CALC = "Calculado en Claude Code con herramientas/quiniela_calc.py sobre el precio de la mesa"


def leer(ruta):
    with open(ruta, encoding="utf-8") as f:
        return json.load(f)


def escribir(nombre, campos, filas):
    os.makedirs(SALIDA, exist_ok=True)
    with open(os.path.join(SALIDA, nombre), "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=campos)
        w.writeheader()
        for fila in filas:
            w.writerow({k: ("" if fila.get(k) is None else fila.get(k)) for k in campos})
    return len(filas)


def fecha_y_hora(dia):
    """'mar 3, 21:00 (hora peninsular)' -> ('2026-11-03', '21:00'). Solo J19 (noviembre de 2026)."""
    if not dia:
        return None, None
    numero = int(dia.split(",")[0].split()[1])
    hora = dia.split(",")[1].strip().split()[0]
    return f"2026-11-{numero:02d}", hora


def partidos():
    filas = []
    with open(os.path.join(RAIZ, "datos", "euro_j19.csv"), encoding="utf-8") as f:
        for r in csv.DictReader(f):
            origen = ("openfootball (football.json, europe, champions-league)" if r["fecha"] <= "2026-09-20"
                      else "uefa.com, futboltotal.futbol, ESPN o thestatsapi (la mesa no indica cuál por partido)")
            filas.append({"fecha": r["fecha"], "competicion": r["competicion"], "local": r["local"],
                          "visitante": r["visitante"], "goles_local": r["goles_local"],
                          "goles_visitante": r["goles_visitante"], "xg_local": None, "xg_visitante": None,
                          "fuente": f"{MESA}, datos/euro_j19.csv; origen: {origen}", "fecha_obtencion": OBTENIDO})
    return escribir("partidos.csv", ["fecha", "competicion", "local", "visitante", "goles_local", "goles_visitante",
                                     "xg_local", "xg_visitante", "fuente", "fecha_obtencion"], filas)


def bajas():
    tipos = {"Lesión": "lesion", "Sanción": "sancion", "Duda": "duda", "Vuelve a entrenar": "vuelve_a_entrenar"}
    filas = []
    for b in leer(os.path.join(RAIZ, "app", "bajas.json"))["bajas"]:
        filas.append({"equipo": b["equipo"], "jugador": b["jugador"],
                      "posicion": None if b["posicion"] == "Sin comprobar" else b["posicion"].lower(),
                      "tipo": tipos.get(b["tipo"]), "fecha_regreso": None, "fecha_fuente": b["fecha"],
                      "fuente": b["fuente"], "clase": b["clase"], "estado": b["estado"].lower(),
                      "partido": b["partido"], "fecha_obtencion": b.get("consultado", OBTENIDO)})
    return escribir("bajas.csv", ["equipo", "jugador", "posicion", "tipo", "fecha_regreso", "fecha_fuente", "fuente",
                                  "clase", "estado", "partido", "fecha_obtencion"], filas)


def cuotas():
    foto = leer(os.path.join(J19, "bet365_lunes_2nov_1300.json"))
    nombres = {p["n"]: p["partido"] for p in leer(os.path.join(J19, "j19.json"))["partidos"]}
    nombres[15] = leer(os.path.join(J19, "j19.json"))["pleno"]["partido"]
    filas = []
    for clave, casa, fecha_hora, fuente in (
            ("cuotas", "bet365", "2026-11-02T14:00+01:00",
             foto["fuente"]),
            ("oddsportal_dom0015", "OddsPortal", None,
             "OddsPortal; el archivo de la mesa solo dice «dom0015», sin fecha completa")):
        for n, c in foto[clave].items():
            filas.append({"fecha_hora": fecha_hora, "partido": nombres[int(n)], "casa": casa, "cuota_1": c[0],
                          "cuota_X": c[1], "cuota_2": c[2], "fuente": f"{fuente}; archivo jornadas/j19/bet365_lunes_2nov_1300.json",
                          "jornada": 19, "n_boleto": int(n), "fecha_obtencion": OBTENIDO})
    extra = os.path.join(J19, "cuotas_comparadores_3nov.json")
    if os.path.exists(extra):
        c3 = leer(extra)
        for x in c3["partidos"]:
            filas.append({"fecha_hora": None, "partido": x["partido"], "casa": "Comparador (varias casas)",
                          "cuota_1": x["cuota_1"], "cuota_X": x["cuota_X"], "cuota_2": x["cuota_2"],
                          "fuente": f"{' y '.join(c3['fuentes'])}; {x['casas']}", "jornada": 19, "n_boleto": x["n"],
                          "fecha_obtencion": c3["consultado"]})
    return escribir("cuotas.csv", ["fecha_hora", "partido", "casa", "cuota_1", "cuota_X", "cuota_2", "fuente",
                                   "jornada", "n_boleto", "fecha_obtencion"], filas)


def pronosticos():
    d = leer(os.path.join(J19, "j19.json"))
    filas = []
    for p in d["partidos"] + [dict(d["pleno"], partido=d["pleno"]["partido"] + " (Pleno)")]:
        fecha, hora = fecha_y_hora(p.get("dia"))
        local, visitante = p["partido"].replace(" (Pleno)", "").split(" – ")
        sin = p.get("xg_modelo_sin_ajustes") or [None, None]
        filas.append({"jornada": 19, "n_boleto": p["n"], "fecha": fecha, "hora_peninsular": hora,
                      "competicion": p.get("competicion"), "local": local, "visitante": visitante,
                      "p1": p["p"][0], "px": p["p"][1], "p2": p["p"][2],
                      "goles_esperados_local": p["lambda_local"], "goles_esperados_visitante": p["lambda_visitante"],
                      "goles_esperados_local_sin_ajustes": sin[0], "goles_esperados_visitante_sin_ajustes": sin[1],
                      "lambdas_ajustadas": "si" if p.get("lambdas_ajustadas") else "no",
                      "veto_signo_unico": "si" if p.get("veto_unico") else "no", "motivo_veto": p.get("motivo_veto"),
                      "riesgo": p.get("riesgo") or (qc._riesgo(p["p"]) if p["n"] <= 14 else None),
                      "fuente": f"{MESA}, datos/j19_lambdas_1x2.json (riesgo: jornadas/j19/j19-pronostico.md)",
                      "fecha_obtencion": OBTENIDO})
    return escribir("pronosticos_j19.csv", list(filas[0].keys()), filas)


def boleto():
    d = leer(os.path.join(J19, "j19.json"))
    probs = [p["p"] for p in d["partidos"]]
    sistemas, elegido = qc.comparar_sistemas(probs, qc._forzados(d["partidos"]), d.get("presupuesto", 12))
    resumen, columnas = [], []
    for s in sistemas:
        resumen.append({"jornada": 19, "sistema": s["nombre"], "elegido": "si" if s is elegido else "no",
                        "apuestas": len(s["columnas"]), "coste_eur": len(s["columnas"]) * qc.PRECIO_APUESTA,
                        "p14": round(s["p14"], 8), "p13_o_mas": round(s["p13"], 6), "p12_o_mas": round(s["p12"], 6),
                        "p10_o_mas": round(s["p10"], 6), "fuente": CALC, "fecha_obtencion": OBTENIDO})
    for n, c in enumerate(elegido["columnas"], 1):
        columnas.append({"jornada": 19, "sistema": elegido["nombre"], "columna": n, "signos_1_a_14": c,
                         "pleno": d["pleno"].get("pleno_jugado"), "fuente": CALC, "fecha_obtencion": OBTENIDO})
    a = escribir("sistemas_j19.csv", list(resumen[0].keys()), resumen)
    b = escribir("boleto_j19.csv", list(columnas[0].keys()), columnas)
    return a, b


def pleno():
    p = leer(os.path.join(J19, "j19.json"))["pleno"]
    m = qc.matriz_marcadores(p["lambda_local"], p["lambda_visitante"], p.get("factor_x", 1.0))
    cats = qc.mezclar(qc.categorias_pleno(m), p["empirica"], p["mezcla"])
    filas = [{"jornada": 19, "partido": p["partido"], "resultado_pleno": r, "probabilidad": round(v, 6),
              "fuente": CALC + " (80 % Poisson + 20 % distribución de datos/euro_j19.csv)", "fecha_obtencion": OBTENIDO}
             for r, v in sorted(cats.items(), key=lambda x: -x[1])]
    return escribir("pleno_j19.csv", list(filas[0].keys()), filas)


def sueltas():
    filas = [{"jornada": 19, "apuesta": s["apuesta"], "partido": s["partido"], "probabilidad": s["p"], "resultado": None,
              "fuente": CALC + " (matriz de marcadores de cada partido)", "fecha_obtencion": OBTENIDO}
             for s in leer(os.path.join(J19, "j19.json"))["sueltas"]]
    return escribir("sueltas_j19.csv", list(filas[0].keys()), filas)


def historial():
    fuentes = {15: "Prompt maestro v5 del usuario, registro de errores (J15: «Mejor columna: 9»)",
               16: "Prompt maestro v5 del usuario, registro de errores (J16: «Mejor columna: 8 de 13. Sueltas: 4/5»), fase 9 e instrucciones permanentes («reducida de 7 dobles al 13 [...] desde la J16»)",
               17: "Instrucciones permanentes del usuario (J17 no se pronostica)",
               18: f"{MESA}, README.md («log-loss 0,786 frente a 0,897»; j18_run.py: «Jornada doméstica»)"}
    filas = []
    for j in leer(os.path.join(RAIZ, "app", "historial.json"))["jornadas"]:
        filas.append({"jornada": j["jornada"], "fechas": j["fechas"], "tipo": None if j["tipo"] == "—" else j["tipo"],
                      "estado": j["estado"], "boleto": j["boleto"], "coste_eur": j["coste"],
                      "mejor_columna": j["mejor_columna"], "sueltas_acertadas": j["sueltas_aciertos"],
                      "sueltas_jugadas": j["sueltas_total"], "log_loss_modelo": j["log_loss_modelo"],
                      "log_loss_mercado": j["log_loss_mercado"], "fuente": fuentes.get(j["jornada"]),
                      "fecha_obtencion": OBTENIDO})
    return escribir("historial_jornadas.csv", list(filas[0].keys()), filas)


def main():
    cuentas = {"partidos.csv": partidos(), "bajas.csv": bajas(), "cuotas.csv": cuotas(),
               "pronosticos_j19.csv": pronosticos()}
    cuentas["sistemas_j19.csv"], cuentas["boleto_j19.csv"] = boleto()
    cuentas["pleno_j19.csv"] = pleno()
    cuentas["sueltas_j19.csv"] = sueltas()
    cuentas["historial_jornadas.csv"] = historial()
    with open(os.path.join(RAIZ, "exportacion", "LEEME.txt"), encoding="utf-8") as f:
        leeme = f.read()
    with open(os.path.join(SALIDA, "LEEME.txt"), "w", encoding="utf-8") as f:
        f.write(leeme)
    zip_ruta = os.path.join(RAIZ, "exportacion", "datos_para_mesa.zip")
    with zipfile.ZipFile(zip_ruta, "w", zipfile.ZIP_DEFLATED) as z:
        for nombre in sorted(os.listdir(SALIDA)):
            z.write(os.path.join(SALIDA, nombre), nombre)
    for k, v in cuentas.items():
        print(f"{k}: {v} filas")
    print(zip_ruta)


if __name__ == "__main__":
    main()
