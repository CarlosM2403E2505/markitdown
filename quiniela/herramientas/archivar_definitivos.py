"""Archiva los pronósticos definitivos de una jornada terminada en app/definitivos.json.

La app «Control Quiniela» los muestra en la sección «Pronósticos definitivos anteriores»,
una entrada por jornada que se despliega al hacer clic.

Uso (desde quiniela/):
    python3 herramientas/archivar_definitivos.py jornadas/j23/j23.json
    python3 herramientas/app_datos.py   # copia el archivo a app/datos/definitivos.json

Cada fila es un partido (1-14) o el Pleno (15) de una jornada, con las probabilidades de las
casas y de la mesa, los signos del boleto, las sencillas (C1..Cn) y el resultado si ya está.
Si la jornada ya estaba archivada, se reemplaza. Si el JSON trae `jugado_real` (boletos sellados
de verdad), se archivan esas columnas y ese Pleno, que son los que se contrastan con los resultados.
"""
import json
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARCHIVO = os.path.join(RAIZ, "app", "definitivos.json")


def filas_jornada(d):
    import boleto_mesa_compat as bmc
    bm = bmc.desde_boleto_mesa(d)
    if bm:
        boleto, cols = bm[0], list(bm[1])
    else:
        boleto = d["boleto_provisional"]
        cols = list(d.get("columnas_individuales") or [])
        if d.get("columna_novena"):
            cols.append(d["columna_novena"])
    j = d["jornada"]
    real = d.get("jugado_real")
    etiquetas = [f"C{i + 1}" for i in range(len(cols))]
    titulo_s = None
    if real:
        # Boletos sellados de verdad (fotos de Carlos): las sencillas y el coste son los jugados.
        cols, etiquetas = list(real["sencillas"]), list(real.get("etiquetas") or [f"C{i + 1}" for i in range(len(real["sencillas"]))])
        boleto = {**boleto, **{k: v for k, v in real["boleto"].items() if k in ("tipo", "signos", "pleno", "apuestas", "coste")}}
        titulo_s = f'Sencillas jugadas (sellado real) · {len(cols)} apuestas · {len(cols) * 0.75:.2f} €'.replace(".", ",")
    comun = {"jornada": j, "fechas": d.get("fechas"),
             "boleto": f'{boleto["tipo"]} · {boleto["apuestas"]} apuestas · {boleto["coste"]:.0f} €' + (" · sellado real" if real else ""),
             "coste_total": (real or {}).get("coste") or d.get("coste_total_previsto") or d.get("coste_jugado"), "n_sencillas": len(cols),
             "etiquetas": " ".join(etiquetas), "titulo_sencillas": titulo_s, "nota": (real or {}).get("diferencias")}
    filas = []
    for p in d["partidos"]:
        n = p["n"]
        m = p.get("mercado")
        filas.append({**comun, "id": f"j{j}-{n:02d}", "n": n, "partido": p["partido"],
                      "casas": " · ".join(str(round(v * 100)) for v in m) if m else "sin dato",
                      "mesa": " · ".join(str(round(v * 100)) for v in p["p"]),
                      "signos_boleto": boleto["signos"][str(n)].replace(" ", ""),
                      "sencillas": " ".join(c[n - 1] for c in cols),
                      "resultado": p.get("resultado")})
    pl = d["pleno"]
    marc = pl.get("cats") or pl.get("empirica") or {}
    pm = marc.get(boleto["pleno"])
    filas.append({**comun, "id": f"j{j}-15", "n": 15, "partido": pl["partido"] + " (Pleno)",
                  "casas": f'{round(pl["mercado_pleno"] * 100)} %' if pl.get("mercado_pleno") else "sin dato",
                  "mesa": f"{round(pm * 100)} %" if pm is not None else "—",
                  "signos_boleto": boleto["pleno"],
                  "sencillas": " ".join(boleto["pleno"] for _ in cols),
                  "resultado": pl.get("resultado_pleno")})
    return filas


def main():
    d = json.load(open(sys.argv[1], encoding="utf-8"))
    filas = json.load(open(ARCHIVO, encoding="utf-8"))["rows"] if os.path.exists(ARCHIVO) else []
    filas = [f for f in filas if f["jornada"] != d["jornada"]] + filas_jornada(d)
    filas.sort(key=lambda f: (-f["jornada"], f["n"]))
    json.dump({"rows": filas}, open(ARCHIVO, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"J{d['jornada']} archivada: {len(filas)} filas en total")


if __name__ == "__main__":
    main()
