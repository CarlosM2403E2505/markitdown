#!/usr/bin/env python3
"""Apuestas sueltas de valor (bet365) y gestión del bank.

Reglas: quiniela/analisis/reglas-bank.md (Carlos 20/11/2026).

Subcomandos (desde la carpeta quiniela):
  proponer  jornadas/j23/j23.json [cuotas.json]  -> app/apuestas.json (filas de la jornada)
  liquidar  jornadas/j23/j23.json                -> usa "marcador" y "descanso" ("2-1", "1-0") de cada partido
  encargo   jornadas/j23/j23.json                -> texto para leer en bet365 (Claude in Chrome) las cuotas de las candidatas
  bank                                           -> saldo, ROI, yield, drawdown

La mesa repasa todos los mercados que sabe preciar (lista MERCADOS) en todos los partidos.
Solo apuesta a lo que ELLA espera que pase y nunca contra los signos de su quiniela
(regla de coherencia, Carlos 20/11/2026).

Sin cuotas: lista «Vigilar» con la cuota mínima a la que bet365 tiene que pagar.
Con cuotas (cuotas.json, leído de bet365): valor real, mezcla mesa/mercado y stake.

cuotas.json: {"fuente": "bet365.es", "leido_el": "...", "partidos": [{"n": 1, "cuotas": {
    "Goles 2.5|Más de 2,5": 1.85, "1X2|1": 2.20, ...}}]}
La clave es "mercado|selección" con los nombres de MERCADOS. Si están todas las
selecciones de un mercado, se usa su probabilidad sin margen para la mezcla.
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
PESO_MESA = 0.40          # el mercado pesa 60 % (J18-J19: log-loss 0,73-0,79 frente a 0,86-0,90 de la mesa)
EXIGENCIA_PROV = 1.10     # sin cuota real: la mesa pide un 10 % por encima de su cuota justa
KELLY = 0.25              # cuarto de Kelly
TOPE_APUESTA = 0.02       # máx. 2 % del bank por apuesta
TOPE_JORNADA = 0.10       # máx. 10 % del bank expuesto por jornada
STAKE_MIN = 2.0
PARADA = 0.75             # si el bank baja del 75 % del inicial, se para y se revisa
VIGILAR_POR_PARTIDO = 3   # candidatas por partido en la lista provisional
CUOTA_MAX_PROV = 3.50     # en la provisional, solo sucesos que la mesa ve bastante probables
CUOTA_JUSTA_MIN_PROV = 1.60  # por debajo, bet365 no suele pagar 1,80 aunque la mesa tenga razón
DRAW = {"Primera": 1.08, "Segunda": 1.00, "Liga F": 0.85}
PRIMERA_PARTE = 0.45      # fracción de goles antes del descanso


def _pois(k, lam):
    return math.exp(-lam) * lam ** k / math.factorial(k)


def conjunta(lam, mu, k_x, n=8):
    """Probabilidad de cada (goles local 1.ª, visitante 1.ª, local 2.ª, visitante 2.ª)."""
    a1 = [_pois(i, lam * PRIMERA_PARTE) for i in range(n)]
    b1 = [_pois(i, mu * PRIMERA_PARTE) for i in range(n)]
    a2 = [_pois(i, lam * (1 - PRIMERA_PARTE)) for i in range(n)]
    b2 = [_pois(i, mu * (1 - PRIMERA_PARTE)) for i in range(n)]
    celdas = []
    for h1 in range(n):
        for v1 in range(n):
            for h2 in range(n):
                for v2 in range(n):
                    p = a1[h1] * b1[v1] * a2[h2] * b2[v2]
                    if h1 + h2 == v1 + v2:
                        p *= k_x
                    celdas.append(((h1, v1, h2, v2), p))
    s = sum(p for _, p in celdas)
    return [(c, p / s) for c, p in celdas]


def _sg(a, b):
    return "1" if a > b else "X" if a == b else "2"


def mercados():
    """Lista de (mercado, [(selección, condición)]); condición(h1, v1, h2, v2) -> True/False/None (nula)."""
    ft = lambda f: (lambda h1, v1, h2, v2: f(h1 + h2, v1 + v2))  # noqa: E731
    m = []
    m.append(("1X2", [(s, ft(lambda g, v, s=s: _sg(g, v) == s)) for s in "1X2"]))
    m.append(("Doble oportunidad", [("1X", ft(lambda g, v: g >= v)), ("X2", ft(lambda g, v: g <= v)),
                                    ("12", ft(lambda g, v: g != v))]))
    m.append(("Empate no apuesta", [("Local", ft(lambda g, v: None if g == v else g > v)),
                                    ("Visitante", ft(lambda g, v: None if g == v else v > g))]))
    for L in (0.5, 1.5, 2.5, 3.5, 4.5):
        m.append((f"Goles {L}", [(f"Más de {str(L).replace('.', ',')}", ft(lambda g, v, L=L: g + v > L)),
                                 (f"Menos de {str(L).replace('.', ',')}", ft(lambda g, v, L=L: g + v < L))]))
    m.append(("Ambos marcan", [("Sí", ft(lambda g, v: g > 0 and v > 0)), ("No", ft(lambda g, v: g == 0 or v == 0))]))
    for L in (0.5, 1.5, 2.5):
        Ls = str(L).replace('.', ',')
        m.append((f"Goles local {L}", [(f"Local más de {Ls}", ft(lambda g, v, L=L: g > L)),
                                       (f"Local menos de {Ls}", ft(lambda g, v, L=L: g < L))]))
        m.append((f"Goles visitante {L}", [(f"Visitante más de {Ls}", ft(lambda g, v, L=L: v > L)),
                                           (f"Visitante menos de {Ls}", ft(lambda g, v, L=L: v < L))]))
    for L in (1.5, 2.5):
        Ls = str(L).replace('.', ',')
        m.append((f"Hándicap local -{L}", [(f"Local -{Ls}", ft(lambda g, v, L=L: g - v > L)),
                                           (f"Visitante +{Ls}", ft(lambda g, v, L=L: g - v < L))]))
        m.append((f"Hándicap visitante -{L}", [(f"Visitante -{Ls}", ft(lambda g, v, L=L: v - g > L)),
                                               (f"Local +{Ls}", ft(lambda g, v, L=L: v - g < L))]))
    m.append(("Local gana a cero", [("Local gana a cero: sí", ft(lambda g, v: g > 0 and v == 0)),
                                    ("Local gana a cero: no", ft(lambda g, v: not (g > 0 and v == 0)))]))
    m.append(("Visitante gana a cero", [("Visitante gana a cero: sí", ft(lambda g, v: v > 0 and g == 0)),
                                        ("Visitante gana a cero: no", ft(lambda g, v: not (v > 0 and g == 0)))]))
    m.append(("Resultado y ambos marcan", [(f"{s} y {b}", ft(lambda g, v, s=s, b=b: _sg(g, v) == s and ((g > 0 and v > 0) == (b == "Sí"))))
                                           for s in "1X2" for b in ("Sí", "No")]))
    m.append(("Resultado y goles 2.5", [(f"{s} y {t} de 2,5", ft(lambda g, v, s=s, t=t: _sg(g, v) == s and ((g + v > 2.5) == (t == "más"))))
                                        for s in "1X2" for t in ("más", "menos")]))
    m.append(("Descanso 1X2", [(f"Descanso {s}", lambda h1, v1, h2, v2, s=s: _sg(h1, v1) == s) for s in "1X2"]))
    for L in (0.5, 1.5):
        Ls = str(L).replace('.', ',')
        m.append((f"Goles 1.ª parte {L}", [(f"1.ª parte más de {Ls}", lambda h1, v1, h2, v2, L=L: h1 + v1 > L),
                                           (f"1.ª parte menos de {Ls}", lambda h1, v1, h2, v2, L=L: h1 + v1 < L)]))
    m.append(("Goles 2.ª parte 1.5", [("2.ª parte más de 1,5", lambda h1, v1, h2, v2: h2 + v2 > 1.5),
                                      ("2.ª parte menos de 1,5", lambda h1, v1, h2, v2: h2 + v2 < 1.5)]))
    m.append(("Mitad con más goles", [("1.ª parte", lambda h1, v1, h2, v2: h1 + v1 > h2 + v2),
                                      ("2.ª parte", lambda h1, v1, h2, v2: h2 + v2 > h1 + v1),
                                      ("Igual", lambda h1, v1, h2, v2: h1 + v1 == h2 + v2)]))
    m.append(("Descanso/Final", [(f"{a}/{b}", lambda h1, v1, h2, v2, a=a, b=b: _sg(h1, v1) == a and _sg(h1 + h2, v1 + v2) == b)
                                 for a in "1X2" for b in "1X2"]))
    return m


MERCADOS = mercados()
SELECCIONES = {m: [s for s, _ in sel] for m, sel in MERCADOS}
_COND = {(m, s): c for m, sel in MERCADOS for s, c in sel}
# Mercados que la mesa no tiene modelo para preciar (no se apuestan hasta tener datos):
SIN_MODELO = ["Córners", "Tarjetas", "Goleadores", "Resultado exacto (salvo el Pleno)"]


def probabilidades(p1x2, lam, mu, comp):
    """{mercado: {selección: (p_gana, p_nula)}} y P(signo | gana) para la regla de coherencia."""
    celdas = conjunta(lam, mu, DRAW.get(comp, 1.0))
    p_sig_mat = {s: sum(p for c, p in celdas if _sg(c[0] + c[2], c[1] + c[3]) == s) for s in "1X2"}
    # Reescalado: los signos finales cuadran con el 1X2 de la mesa (con su temperatura).
    w = {s: p1x2["1X2".index(s)] / p_sig_mat[s] for s in "1X2"}
    celdas = [(c, p * w[_sg(c[0] + c[2], c[1] + c[3])]) for c, p in celdas]
    out = {}
    for mercado, sel in MERCADOS:
        out[mercado] = {}
        for s, cond in sel:
            gana = nula = 0.0
            sig = {"1": 0.0, "X": 0.0, "2": 0.0}
            for c, p in celdas:
                r = cond(*c)
                if r is None:
                    nula += p
                elif r:
                    gana += p
                    sig[_sg(c[0] + c[2], c[1] + c[3])] += p
            out[mercado][s] = (gana, nula, {k: v / gana for k, v in sig.items()} if gana else sig)
    return out


def gana(mercado, seleccion, ft, ht):
    """True gana, False pierde, None nula. ft y ht son (local, visitante)."""
    h1, v1 = ht
    return _COND[(mercado, seleccion)](h1, v1, ft[0] - h1, ft[1] - v1)


def _signos_quiniela(d):
    """Signos del boleto principal de la mesa en cada partido (no las sencillas, que buscan sorpresas)."""
    cols = list(d.get("columnas_jugadas") or [])
    sig = {}
    for i, p in enumerate(d["partidos"]):
        n = p.get("n", i + 1)
        sig[n] = {c[i] for c in cols} if cols else {"1X2"[max(range(3), key=lambda k: p["p"][k])]}
    pl = d.get("pleno")
    if pl:
        pj = pl.get("pleno_jugado") or (d.get("boleto_provisional") or {}).get("pleno")  # p. ej. "1-1"
        if pj and "-" in pj:
            a, b = pj.split("-")
            sig[15] = {_sg(int(a.replace("M", "3")), int(b.replace("M", "3")))}
        else:
            sig[15] = {"1X2"[max(range(3), key=lambda k: pl["p"][k])]}
    return sig


def _partidos(d):
    out = []
    for p in d["partidos"]:
        out.append((p["n"], p["partido"], p.get("competicion"), p["p"], p["xg"][0], p["xg"][1]))
    pl = d.get("pleno")
    if pl:
        out.append((15, pl["partido"], pl.get("competicion", "Primera"), pl["p"], pl["lambda_local"], pl["lambda_visitante"]))
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


def _stake(p, nula, cuota, bank):
    """¼ de Kelly con nula (se devuelve el stake): f = (p·b − q) / b sobre las no nulas."""
    b = cuota - 1
    q = 1 - p - nula
    f = max(0.0, (p * b - q) / b) * KELLY
    return min(f, TOPE_APUESTA) * bank


def coherente(mercado, s, pg, pn, sig_dado, todas, signos_q, p1x2_previo):
    """La mesa solo apuesta a lo que espera y nunca contra su quiniela."""
    # 1) Lo que la mesa espera: la selección más probable de su mercado (en los de dos lados, > 50 %).
    if pg < max(v[0] for v in todas.values()) - 1e-9:
        return False
    # 2) Nunca a favor de lo que la quiniela descarta: si la apuesta gana, el signo que el boleto no
    #    lleva no puede ser más probable que de entrada (margen de 2 puntos).
    fuera = [k for k in "1X2" if k not in signos_q]
    if not fuera:
        return True
    return sum(sig_dado[k] for k in fuera) <= sum(p1x2_previo[k] for k in fuera) + 0.02


def proponer(ruta_j, ruta_cuotas=None):
    d = _leer(ruta_j, None)
    j = d["jornada"]
    cuotas, fuente = {}, None
    if ruta_cuotas:
        c = _leer(ruta_cuotas, None)
        fuente = f'{c.get("fuente", "bet365.es")} {c.get("leido_el", "")}'.strip()
        cuotas = {x["n"]: x["cuotas"] for x in c["partidos"]}
    signos = _signos_quiniela(d)
    bank = saldo_actual()
    filas = []
    revisadas = 0
    for n, partido, comp, p1x2, lam, mu in _partidos(d):
        probs = probabilidades(p1x2, lam, mu, comp)
        cand = []
        for mercado, sels in probs.items():
            for s, (pg, pn, sig_dado) in sels.items():
                revisadas += 1
                if not coherente(mercado, s, pg, pn, sig_dado, sels, signos.get(n, set("1X2")), dict(zip("1X2", p1x2))):
                    continue
                base = {"jornada": j, "n": n, "partido": partido, "competicion": comp, "mercado": mercado,
                        "seleccion": s, "p_mesa": round(pg, 4), "p_nula": round(pn, 4),
                        "cuota_justa": round((1 - pn) / pg, 2) if pg else None,
                        "signos_quiniela": "".join(x for x in "1X2" if x in signos.get(n, set()))}
                of = cuotas.get(n) or {}
                if cuotas:
                    cuota = of.get(f"{mercado}|{s}")
                    if not cuota or cuota < CUOTA_MIN:
                        continue
                    todas = [of.get(f"{mercado}|{x}") for x in SELECCIONES[mercado]]
                    if all(todas) and pn == 0:
                        inv = [1 / x for x in todas]
                        p_mkt = (1 / cuota) / sum(inv)
                    else:
                        p_mkt = None  # mercado incompleto: la mesa se exige el margen típico
                    p = PESO_MESA * pg + (1 - PESO_MESA) * p_mkt if p_mkt is not None else pg / EXIGENCIA_PROV
                    valor = p * cuota + pn - 1
                    if valor < VALOR_MIN:
                        continue
                    base.update({"cuota": cuota, "p_mercado": round(p_mkt, 4) if p_mkt is not None else None,
                                 "p_final": round(p, 4), "valor": round(valor, 4), "estado": "Propuesta",
                                 "cuota_minima": None})
                    cand.append((valor, base))
                else:
                    minima = round(max(CUOTA_MIN, EXIGENCIA_PROV * (1 - pn) / pg), 2)
                    if minima > CUOTA_MAX_PROV or (1 - pn) / pg < CUOTA_JUSTA_MIN_PROV:
                        # fuera lo que la mesa ve tan seguro que bet365 no pagará 1,80, y lo muy improbable
                        continue
                    base.update({"cuota": None, "cuota_minima": minima, "p_mercado": None, "p_final": round(pg, 4),
                                 "valor": None, "estado": "Vigilar", "stake": None})
                    cand.append((pg, base))
        cand.sort(key=lambda t: -t[0])
        if cuotas:
            filas += [c for _, c in cand[:1]]  # definitivas: una por partido, la de más valor
        else:
            vistos = set()
            for _, c in cand:
                if c["mercado"] in vistos:
                    continue
                vistos.add(c["mercado"])
                filas.append(c)
                if len(vistos) >= VIGILAR_POR_PARTIDO:
                    break

    if cuotas:
        for f in filas:
            f["stake_bruto"] = _stake(f["p_final"], f["p_nula"], f["cuota"], bank)
        total = sum(f["stake_bruto"] for f in filas)
        escala = min(1.0, TOPE_JORNADA * bank / total) if total else 1.0
        for f in filas:
            st = math.floor(f.pop("stake_bruto") * escala * 2) / 2
            f["stake"] = st if st >= STAKE_MIN else 0.0
            f["ganancia_posible"] = round(f["stake"] * (f["cuota"] - 1), 2)
        filas = [f for f in filas if f["stake"] > 0]
        filas.sort(key=lambda f: -f["valor"])
    else:
        filas.sort(key=lambda f: (f["n"], -f["p_mesa"]))
        for f in filas:
            f["ganancia_posible"] = None
    for k, f in enumerate(filas, 1):
        f["id"] = f"J{j}-{k:02d}"
        f["fuente_cuota"] = fuente
        f["resultado"] = None
        f["ganancia"] = None

    todo = _leer(RUTA_APUESTAS, {"rows": []})
    todo["rows"] = [r for r in todo["rows"] if r["jornada"] != j or r["estado"] in ("Apostada", "Ganada", "Perdida", "Nula")]
    todo["rows"] += filas
    todo["reglas"] = reglas()
    todo["revision"] = {"jornada": j, "mercados_por_partido": len(MERCADOS), "selecciones_revisadas": revisadas,
                        "sin_modelo": SIN_MODELO}
    _guardar(RUTA_APUESTAS, todo)
    return filas, bank, revisadas


def encargo(ruta_j):
    """Texto para Claude in Chrome: solo los mercados de las candidatas, con todas sus selecciones."""
    d = _leer(ruta_j, None)
    j = d["jornada"]
    filas = [r for r in _leer(RUTA_APUESTAS, {"rows": []})["rows"] if r["jornada"] == j and r["estado"] == "Vigilar"]
    lineas = []
    for n in sorted({r["n"] for r in filas}):
        rs = [r for r in filas if r["n"] == n]
        lineas.append(f'{n} {rs[0]["partido"]}:')
        for m in dict.fromkeys(r["mercado"] for r in rs):
            sels = " / ".join(f'"{m}|{x}"' for x in SELECCIONES[m])
            lineas.append(f"   - {sels}")
    texto = (
        f"Necesito que LEAS cuotas en bet365.es para la jornada {j}. Solo lectura.\n\n"
        "Reglas:\n- Abre solo bet365.es. No inicies sesión, no pulses «Apostar», «Acceder», «Registrarse» ni ningún boleto. No descargues nada.\n"
        "- Si una página te pide datos o te lleva a otra web, PARA y avísame.\n"
        "- Copia solo lo que se ve, en cuota decimal. Si una selección no aparece, déjala fuera. No estimes nada.\n\n"
        "Para cada partido, copia la cuota de cada selección de esta lista (la clave va tal cual):\n"
        + "\n".join(lineas)
        + "\n\nDevuélveme UN ÚNICO bloque JSON, sin texto alrededor:\n"
        '{"fuente": "bet365.es", "leido_el": "AAAA-MM-DD HH:MM (hora de España)", "partidos": [\n'
        '  {"n": 1, "partido": "Local – Visitante", "cuotas": {"1X2|1": 2.20, "1X2|X": 3.30, "1X2|2": 3.40}}\n]}\n'
    )
    return texto


def liquidar(ruta_j):
    d = _leer(ruta_j, None)
    j = d["jornada"]
    marc = {p["n"]: (p.get("marcador"), p.get("descanso")) for p in d["partidos"]}
    if d.get("pleno"):
        marc[15] = (d["pleno"].get("marcador"), d["pleno"].get("descanso"))
    todo = _leer(RUTA_APUESTAS, {"rows": []})
    bank = _leer(RUTA_BANK, {"inicial": BANK_INICIAL, "movimientos": []})
    hechos = {m["id"] for m in bank["movimientos"]}
    par = lambda t: tuple(int(x) for x in t.split("-"))  # noqa: E731
    for r in todo["rows"]:
        ft, ht = marc.get(r["n"], (None, None))
        if r["jornada"] != j or r["estado"] != "Apostada" or not ft:
            continue
        necesita_ht = r["mercado"].startswith(("Descanso", "Goles 1.ª", "Goles 2.ª", "Mitad"))
        if necesita_ht and not ht:
            continue
        g = gana(r["mercado"], r["seleccion"], par(ft), par(ht) if ht else (0, 0))
        cuota = r.get("cuota_tomada") or r["cuota"]
        r["resultado"] = ft + (f" ({ht})" if ht else "")
        r["estado"] = "Nula" if g is None else "Ganada" if g else "Perdida"
        r["ganancia"] = 0.0 if g is None else round(r["stake"] * (cuota - 1), 2) if g else -r["stake"]
        if r["id"] not in hechos:
            bank["movimientos"].append({"id": r["id"], "fecha": datetime.now().strftime("%Y-%m-%d"), "jornada": j,
                                        "concepto": f'{r["partido"]} · {r["seleccion"]} @ {cuota}',
                                        "stake": r["stake"], "importe": r["ganancia"]})
    _guardar(RUTA_APUESTAS, todo)
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
            "exigencia_provisional": EXIGENCIA_PROV, "kelly": KELLY, "tope_apuesta": TOPE_APUESTA,
            "tope_jornada": TOPE_JORNADA, "stake_min": STAKE_MIN, "parada": PARADA}


if __name__ == "__main__":
    os.chdir(RAIZ)
    cmd = sys.argv[1] if len(sys.argv) > 1 else "bank"
    if cmd == "proponer":
        filas, bank, rev = proponer(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else None)
        print(f"Bank {bank:.2f} € · {len(MERCADOS)} mercados por partido · {rev} selecciones revisadas · {len(filas)} filas")
        for f in filas:
            extra = (f'cuota {f["cuota"]:.2f} valor {100*f["valor"]:+.1f} % stake {f["stake"]:.2f}' if f["cuota"]
                     else f'mínima {f["cuota_minima"]:.2f}')
            print(f'{f["id"]} {f["partido"]:28s} [{f["signos_quiniela"]:3s}] {f["mercado"]:26s} {f["seleccion"]:24s} '
                  f'mesa {100*f["p_mesa"]:5.1f} % justa {f["cuota_justa"]:5.2f} {extra}')
    elif cmd == "encargo":
        print(encargo(sys.argv[2]))
    elif cmd == "liquidar":
        liquidar(sys.argv[2])
        print(resumen_bank())
    else:
        print(resumen_bank())
