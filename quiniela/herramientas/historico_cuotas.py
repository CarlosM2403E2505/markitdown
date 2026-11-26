"""Histórico de cuotas de bet365 (Carlos, 22/11/2026).

Cada lectura de cuotas (apertura, lunes 11:00, definitiva, cierre) se guarda con su momento, y tras la jornada se
marca si cada selección salió. Con jornadas suficientes se mide: deriva apertura→cierre, sesgo favorito-sorpresa,
la X y la calibración de la cuota frente al resultado. Solo un dato medido y positivo (fuera de muestra) entra en
las reglas de la mesa, sobre todo para el Pleno al 15. Las cuotas son dato: nunca cambian un signo por sí solas.

Uso (desde quiniela/):
  python3 herramientas/historico_cuotas.py añadir jornadas/j23/j23.json jornadas/j23/cuotas_bet365_20261121.json definitiva
  python3 herramientas/historico_cuotas.py resultados jornadas/j23/j23.json
  python3 herramientas/historico_cuotas.py analisis
"""
import csv
import json
import os
import sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import apuestas_valor as av  # noqa: E402

RAIZ = av.RAIZ
RUTA = os.path.join(RAIZ, "datos", "cuotas_bet365", "historico.json")
MOMENTOS = ("apertura", "lunes", "definitiva", "cierre")
CAMPOS = ["jornada", "n", "partido", "mercado", "seleccion", "cuota", "p_implicita", "momento", "leido", "fuente",
          "dudosa", "resultado", "salio"]


def _leer():
    return av._leer(RUTA, {"rows": []})


def _guardar(h):
    os.makedirs(os.path.dirname(RUTA), exist_ok=True)
    h["rows"].sort(key=lambda r: (r["jornada"], r["n"], r["mercado"], r["seleccion"], MOMENTOS.index(r["momento"])))
    av._guardar(RUTA, h)
    with open(RUTA[:-5] + ".csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, CAMPOS, extrasaction="ignore")
        w.writeheader()
        w.writerows(h["rows"])


def _implicitas(cuotas):
    """Probabilidad sin margen por mercado (normaliza las selecciones leídas de cada mercado completo)."""
    por_m = defaultdict(dict)
    for k, c in cuotas.items():
        m, s = k.split("|", 1)
        por_m[m][s] = c
    out = {}
    for m, sels in por_m.items():
        tot = sum(1 / c for c in sels.values())
        completo = (m == "1X2" and len(sels) == 3) or (m != "1X2" and len(sels) == 2)
        for s, c in sels.items():
            out[f"{m}|{s}"] = round((1 / c) / tot, 4) if completo else None
    return out


def añadir(ruta_j, ruta_cuotas, momento):
    assert momento in MOMENTOS, f"momento: {MOMENTOS}"
    j = av._leer(ruta_j, None)["jornada"]
    c = av._leer(ruta_cuotas, None)
    h = _leer()
    clave = {(r["jornada"], r["n"], r["mercado"], r["seleccion"], r["momento"]): r for r in h["rows"]}
    for p in c["partidos"]:
        for dudosa, cuotas in ((False, p.get("cuotas", {})), (True, p.get("dudosas", {}))):
            imp = _implicitas(cuotas) if not dudosa else {}
            for k, cuota in cuotas.items():
                m, s = k.split("|", 1)
                clave[(j, p["n"], m, s, momento)] = {
                    "jornada": j, "n": p["n"], "partido": p.get("partido"), "mercado": m, "seleccion": s,
                    "cuota": cuota, "p_implicita": imp.get(k), "momento": momento, "leido": c.get("leido_el"),
                    "fuente": c.get("fuente", "bet365.es"), "dudosa": dudosa, "resultado": None, "salio": None}
    h["rows"] = list(clave.values())
    _guardar(h)
    return len(h["rows"])


def resultados(ruta_j):
    d = av._leer(ruta_j, None)
    marc = {p["n"]: (p.get("marcador"), p.get("descanso")) for p in d["partidos"]}
    if d.get("pleno"):
        marc[15] = (d["pleno"].get("marcador"), d["pleno"].get("descanso"))
    par = lambda t: tuple(int(x) for x in t.split("-"))  # noqa: E731
    h = _leer()
    for r in h["rows"]:
        ft, ht = marc.get(r["n"], (None, None))
        if r["jornada"] != d["jornada"] or not ft:
            continue
        if r["mercado"].startswith(("Descanso", "Goles 1.ª", "Goles 2.ª", "Mitad")) and not ht:
            continue
        g = av.gana(r["mercado"], r["seleccion"], par(ft), par(ht) if ht else (0, 0))
        r["resultado"], r["salio"] = ft, g
    _guardar(h)


def analisis():
    """Calibración por tramos de probabilidad implícita (1X2, sin dudosas, último momento leído de cada selección)."""
    ult = {}
    for r in _leer()["rows"]:
        if r["dudosa"] or r["salio"] is None or r["p_implicita"] is None:
            continue
        k = (r["jornada"], r["n"], r["mercado"], r["seleccion"])
        if k not in ult or MOMENTOS.index(r["momento"]) > MOMENTOS.index(ult[k]["momento"]):
            ult[k] = r
    tramos = defaultdict(lambda: [0, 0.0, 0])
    x = [0, 0.0, 0]
    for r in ult.values():
        if r["mercado"] != "1X2":
            continue
        t = min(int(r["p_implicita"] * 5), 4)
        tramos[t][0] += 1
        tramos[t][1] += r["p_implicita"]
        tramos[t][2] += bool(r["salio"])
        if r["seleccion"] == "X":
            x[0] += 1
            x[1] += r["p_implicita"]
            x[2] += bool(r["salio"])
    filas = [{"tramo": f"{t * 20}-{t * 20 + 20} %", "n": v[0], "esperado": round(v[1] / v[0], 3),
              "real": round(v[2] / v[0], 3)} for t, v in sorted(tramos.items())]
    if x[0]:
        filas.append({"tramo": "Solo X", "n": x[0], "esperado": round(x[1] / x[0], 3), "real": round(x[2] / x[0], 3)})
    return filas


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "analisis"
    if cmd == "añadir":
        print(añadir(sys.argv[2], sys.argv[3], sys.argv[4]), "cuotas en el histórico")
    elif cmd == "resultados":
        resultados(sys.argv[2])
    else:
        for f in analisis():
            print(f)
        print("Muestra pequeña: nada entra en las reglas hasta que la diferencia aguante fuera de muestra.")
