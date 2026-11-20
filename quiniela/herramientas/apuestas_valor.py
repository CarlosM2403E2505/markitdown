#!/usr/bin/env python3
"""Apuestas sueltas de valor (bet365) y gestión del bank.

Reglas (Carlos 20/11/2026, mejoradas por la mesa): ver quiniela/analisis/reglas-bank.md.

Subcomandos (desde la carpeta quiniela):
  proponer  jornadas/j23/j23.json [cuotas.json] [--mercado=mercado.json] -> app/apuestas.json
  liquidar  jornadas/j23/j23.json                 -> usa "marcador" de cada partido del JSON
  bank                                            -> imprime saldo, ROI, yield, drawdown

Sin archivo de cuotas sale una LISTA DE VIGILANCIA: cada fila trae la cuota mínima
a la que bet365 tiene que pagar para que haya valor. Con cuotas (leídas de bet365)
se calcula el valor real, se mezcla la probabilidad de la mesa con la del mercado
y se fija el stake.

Formato de cuotas.json:
{"leido_el": "2026-11-21 09:30", "fuente": "bet365.es",
 "partidos": [{"n": 1, "mercados": {"1X2": [2.2, 3.3, 3.4], "DC": [1.3, 1.67, 1.33],
   "Goles 1.5": [1.3, 3.5], "Goles 2.5": [1.9, 1.9], "Goles 3.5": [3.2, 1.33],
   "Ambos marcan": [1.8, 1.95], "Hándicap -1.5": [2.4, 1.55], "Empate no apuesta": [1.6, 2.3]}}]}
(cada lista en el orden de SELECCIONES[mercado]).
"""
import json
import math
import os
import sys
from datetime import datetime

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUTA_APUESTAS = os.path.join(RAIZ, "app", "apuestas.json")
RUTA_BANK = os.path.join(RAIZ, "app", "bank.json")

# ---- Reglas del bank (fijas; cambiarlas solo si Carlos lo pide) ----
BANK_INICIAL = 500.0
CUOTA_MIN = 1.80          # Carlos
VALOR_MIN = 0.05          # +5 % de valor esperado con la probabilidad mezclada
PESO_MESA = 0.40          # el mercado pesa 60 %: en J18-J19 su log-loss fue 0,73-0,79 frente a 0,86-0,90 de la mesa
KELLY = 0.25              # cuarto de Kelly
TOPE_APUESTA = 0.02       # máx. 2 % del bank por apuesta
TOPE_JORNADA = 0.10       # máx. 10 % del bank expuesto por jornada
STAKE_MIN = 2.0           # por debajo no compensa
MARGEN_TIPICO = 1.05      # margen habitual de bet365 en 1X2 (solo para estimar en la lista de vigilancia)
PARADA = 0.75             # si el bank baja del 75 % del inicial, se para y se revisa
DRAW = {"Primera": 1.08, "Segunda": 1.00, "Liga F": 0.85}

SELECCIONES = {
    "1X2": ["1", "X", "2"],
    "DC": ["1X", "X2", "12"],
    "Empate no apuesta": ["Local", "Visitante"],
    "Goles 1.5": ["Más de 1,5", "Menos de 1,5"],
    "Goles 2.5": ["Más de 2,5", "Menos de 2,5"],
    "Goles 3.5": ["Más de 3,5", "Menos de 3,5"],
    "Ambos marcan": ["Sí", "No"],
    "Hándicap -1.5": ["Local -1,5", "Visitante +1,5"],
    "Hándicap +1.5": ["Local +1,5", "Visitante -1,5"],
}


def _pois(k, lam):
    return math.exp(-lam) * lam ** k / math.factorial(k)


def matriz(lam, mu, k_x, n=11):
    M = [[_pois(i, lam) * _pois(j, mu) * (k_x if i == j else 1.0) for j in range(n)] for i in range(n)]
    s = sum(map(sum, M))
    return [[v / s for v in fila] for fila in M]


def probabilidades(p1x2, lam, mu, comp):
    """Probabilidad de la mesa para cada selección. 1X2 y derivados salen del precio final
    de la mesa (con temperatura); los de goles, de la matriz de Poisson del partido."""
    M = matriz(lam, mu, DRAW.get(comp, 1.0))
    n = len(M)

    def suma(cond):
        return sum(M[i][j] for i in range(n) for j in range(n) if cond(i, j))
    p1, px, p2 = p1x2
    sin_x = p1 + p2
    return {
        "1X2": [p1, px, p2],
        "DC": [p1 + px, px + p2, p1 + p2],
        # Empate no apuesta: se devuelve el dinero si hay X → probabilidad condicionada y la X como nula.
        "Empate no apuesta": [p1 / sin_x, p2 / sin_x],
        "Goles 1.5": [suma(lambda i, j: i + j >= 2), suma(lambda i, j: i + j <= 1)],
        "Goles 2.5": [suma(lambda i, j: i + j >= 3), suma(lambda i, j: i + j <= 2)],
        "Goles 3.5": [suma(lambda i, j: i + j >= 4), suma(lambda i, j: i + j <= 3)],
        "Ambos marcan": [suma(lambda i, j: i >= 1 and j >= 1), suma(lambda i, j: i == 0 or j == 0)],
        "Hándicap -1.5": [suma(lambda i, j: i - j >= 2), suma(lambda i, j: i - j <= 1)],
        "Hándicap +1.5": [suma(lambda i, j: j - i <= 1), suma(lambda i, j: j - i >= 2)],
    }, px


def gana(mercado, k, g1, g2):
    """True gana, False pierde, None nula (se devuelve el stake)."""
    d, t = g1 - g2, g1 + g2
    if mercado == "1X2":
        return ["1", "X", "2"][k] == ("1" if d > 0 else "X" if d == 0 else "2")
    if mercado == "DC":
        return [d >= 0, d <= 0, d != 0][k]
    if mercado == "Empate no apuesta":
        return None if d == 0 else [d > 0, d < 0][k]
    if mercado.startswith("Goles"):
        linea = float(mercado.split()[1])
        return [t > linea, t < linea][k]
    if mercado == "Ambos marcan":
        return [g1 >= 1 and g2 >= 1, g1 == 0 or g2 == 0][k]
    if mercado == "Hándicap -1.5":
        return [d >= 2, d <= 1][k]
    if mercado == "Hándicap +1.5":
        return [d >= -1, d <= -2][k]
    raise ValueError(mercado)


def _sin_margen(cuotas):
    inv = [1 / c for c in cuotas]
    return [v / sum(inv) for v in inv]


def _partidos(d):
    out = []
    for p in d["partidos"]:
        out.append((p["n"], p["partido"], p.get("competicion"), p["p"], p["xg"][0], p["xg"][1], p))
    pl = d.get("pleno")
    if pl:
        out.append((15, pl["partido"], pl.get("competicion", "Primera"), pl["p"],
                    pl["lambda_local"], pl["lambda_visitante"], pl))
    return out


def _leer(ruta, defecto):
    if not os.path.exists(ruta):
        return defecto
    with open(ruta, encoding="utf-8") as f:
        return json.load(f)


def _guardar(ruta, obj):
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)


def saldo_actual():
    bank = _leer(RUTA_BANK, {"inicial": BANK_INICIAL, "movimientos": []})
    return bank["inicial"] + sum(m["importe"] for m in bank["movimientos"])


def _stake(p, cuota, bank):
    b = cuota - 1
    f = max(0.0, (p * b - (1 - p)) / b) * KELLY
    return min(f, TOPE_APUESTA) * bank


def proponer(ruta_j, ruta_cuotas=None, ruta_mercado=None):
    d = _leer(ruta_j, None)
    vigilancia = (_leer(ruta_mercado, {}) if ruta_mercado else {}).get("partidos", {})
    j = d["jornada"]
    cuotas = {}
    fuente = None
    if ruta_cuotas:
        c = _leer(ruta_cuotas, None)
        fuente = f'{c.get("fuente", "bet365.es")} {c.get("leido_el", "")}'.strip()
        cuotas = {x["n"]: x["mercados"] for x in c["partidos"]}
    bank = saldo_actual()
    candidatas = []
    for n, partido, comp, p1x2, lam, mu, _ in _partidos(d):
        probs, _px = probabilidades(p1x2, lam, mu, comp)
        mejor = None
        for mercado, ps in probs.items():
            ofrecidas = (cuotas.get(n) or {}).get(mercado)
            for k, p_mesa in enumerate(ps):
                sel = SELECCIONES[mercado][k]
                if ofrecidas:
                    cuota = ofrecidas[k]
                    if cuota is None or cuota < CUOTA_MIN:
                        continue
                    p_mkt = _sin_margen([x for x in ofrecidas if x])[k] if all(ofrecidas) else 1 / cuota
                    p = PESO_MESA * p_mesa + (1 - PESO_MESA) * p_mkt
                    valor = p * cuota - 1
                    if valor < VALOR_MIN:
                        continue
                    fila = {"cuota": cuota, "p_mercado": round(p_mkt, 4), "p_final": round(p, 4),
                            "valor": round(valor, 4), "estado": "Propuesta"}
                else:
                    # Lista de vigilancia: solo partidos con mercado 1X2 conocido (OddsPortal sin margen).
                    pm = vigilancia.get(str(n))
                    if not pm or mercado not in ("1X2", "DC", "Empate no apuesta"):
                        continue
                    p_mkt = {"1X2": pm, "DC": [pm[0] + pm[1], pm[1] + pm[2], pm[0] + pm[2]],
                             "Empate no apuesta": [pm[0] / (pm[0] + pm[2]), pm[2] / (pm[0] + pm[2])]}[mercado][k]
                    p = PESO_MESA * p_mesa + (1 - PESO_MESA) * p_mkt
                    minima = max(CUOTA_MIN, (1 + VALOR_MIN) / p)
                    estimada = round(1 / (p_mkt * MARGEN_TIPICO), 2)
                    valor = p * estimada - 1
                    if estimada < CUOTA_MIN or valor < VALOR_MIN:
                        continue
                    fila = {"cuota": None, "cuota_minima": round(minima, 2), "cuota_estimada": estimada,
                            "p_mercado": round(p_mkt, 4), "p_final": round(p, 4), "valor": round(valor, 4),
                            "estado": "Vigilar"}
                fila.update({"jornada": j, "n": n, "partido": partido, "competicion": comp,
                             "mercado": mercado, "seleccion": sel, "p_mesa": round(p_mesa, 4),
                             "cuota_justa": round(1 / p_mesa, 2)})
                clave = fila["valor"]
                if mejor is None or clave > mejor[0]:
                    mejor = (clave, fila)
        if mejor:
            candidatas.append(mejor[1])  # una apuesta por partido: no se apilan selecciones correlacionadas

    if cuotas:
        for f in candidatas:
            f["stake_bruto"] = _stake(f["p_final"], f["cuota"], bank)
        total = sum(f["stake_bruto"] for f in candidatas)
        escala = min(1.0, TOPE_JORNADA * bank / total) if total else 1.0
        for f in candidatas:
            s = math.floor(f.pop("stake_bruto") * escala * 2) / 2
            f["stake"] = s if s >= STAKE_MIN else 0.0
            f["ganancia_posible"] = round(f["stake"] * (f["cuota"] - 1), 2)
        candidatas = [f for f in candidatas if f["stake"] > 0]
        candidatas.sort(key=lambda f: -f["valor"])
    else:
        for f in candidatas:
            # stake orientativo si bet365 paga la cuota estimada (se recalcula con la cuota real)
            f["stake"] = max(STAKE_MIN, math.floor(_stake(f["p_final"], f["cuota_estimada"], bank) * 2) / 2)
            f["ganancia_posible"] = None
        candidatas.sort(key=lambda f: -f["valor"])
    for k, f in enumerate(candidatas, 1):
        f["id"] = f"J{j}-{k:02d}"
        f["fuente_cuota"] = fuente
        f["resultado"] = None
        f["ganancia"] = None

    todas = _leer(RUTA_APUESTAS, {"rows": []})
    todas["rows"] = [r for r in todas["rows"] if r["jornada"] != j or r["estado"] in ("Ganada", "Perdida", "Nula")]
    todas["rows"] += candidatas
    todas["reglas"] = reglas()
    _guardar(RUTA_APUESTAS, todas)
    return candidatas, bank


def liquidar(ruta_j):
    d = _leer(ruta_j, None)
    j = d["jornada"]
    marc = {p["n"]: p.get("marcador") for p in d["partidos"]}
    if d.get("pleno"):
        marc[15] = d["pleno"].get("marcador")
    todas = _leer(RUTA_APUESTAS, {"rows": []})
    bank = _leer(RUTA_BANK, {"inicial": BANK_INICIAL, "movimientos": []})
    hechos = {m["id"] for m in bank["movimientos"]}
    for r in todas["rows"]:
        if r["jornada"] != j or r["estado"] not in ("Apostada",) or not marc.get(r["n"]):
            continue
        g1, g2 = (int(x) for x in marc[r["n"]].split("-"))
        k = SELECCIONES[r["mercado"]].index(r["seleccion"])
        g = gana(r["mercado"], k, g1, g2)
        cuota = r.get("cuota_tomada") or r["cuota"]
        r["resultado"] = marc[r["n"]]
        r["estado"] = "Nula" if g is None else "Ganada" if g else "Perdida"
        r["ganancia"] = 0.0 if g is None else round(r["stake"] * (cuota - 1), 2) if g else -r["stake"]
        if r["id"] not in hechos:
            bank["movimientos"].append({"id": r["id"], "fecha": datetime.now().strftime("%Y-%m-%d"),
                                        "jornada": j, "concepto": f'{r["partido"]} · {r["seleccion"]} @ {cuota}',
                                        "stake": r["stake"], "importe": r["ganancia"]})
    _guardar(RUTA_APUESTAS, todas)
    _guardar(RUTA_BANK, bank)


def resumen_bank():
    bank = _leer(RUTA_BANK, {"inicial": BANK_INICIAL, "movimientos": []})
    saldo, pico, dd, apostado = bank["inicial"], bank["inicial"], 0.0, 0.0
    for m in bank["movimientos"]:
        saldo += m["importe"]
        apostado += m.get("stake", 0)
        pico = max(pico, saldo)
        dd = max(dd, (pico - saldo) / pico)
    ben = saldo - bank["inicial"]
    return {"inicial": bank["inicial"], "saldo": round(saldo, 2), "beneficio": round(ben, 2),
            "roi": round(ben / bank["inicial"], 4), "yield": round(ben / apostado, 4) if apostado else None,
            "apostado": round(apostado, 2), "drawdown_max": round(dd, 4),
            "parada": saldo < PARADA * bank["inicial"]}


def reglas():
    return {"bank_inicial": BANK_INICIAL, "cuota_min": CUOTA_MIN, "valor_min": VALOR_MIN, "peso_mesa": PESO_MESA,
            "kelly": KELLY, "tope_apuesta": TOPE_APUESTA, "tope_jornada": TOPE_JORNADA,
            "stake_min": STAKE_MIN, "parada": PARADA}


if __name__ == "__main__":
    os.chdir(RAIZ)
    cmd = sys.argv[1] if len(sys.argv) > 1 else "bank"
    if cmd == "proponer":
        args = sys.argv[2:]
        mercado = next((a.split("=", 1)[1] for a in args if a.startswith("--mercado=")), None)
        args = [a for a in args if not a.startswith("--")]
        filas, bank = proponer(args[0], args[1] if len(args) > 1 else None, mercado)
        print(f"Bank {bank:.2f} € · {len(filas)} filas")
        for f in filas:
            print(f'{f["id"]} {f["partido"]:28s} {f["mercado"]:18s} {f["seleccion"]:14s} mesa {100*f["p_mesa"]:5.1f} % '
                  f'justa {f["cuota_justa"]:5.2f} ' + (f'cuota {f["cuota"]:.2f} valor {100*f["valor"]:+.1f} % stake {f["stake"]:.2f}'
                  if f["cuota"] else f'mínima {f["cuota_minima"]:.2f} estimada {f["cuota_estimada"]:.2f} valor≈{100*f["valor"]:+.1f} % stake≈{f["stake"]:.2f}'))
    elif cmd == "liquidar":
        liquidar(sys.argv[2])
        print(resumen_bank())
    else:
        print(resumen_bank())
