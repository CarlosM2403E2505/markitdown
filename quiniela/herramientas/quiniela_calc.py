#!/usr/bin/env python3
"""Calculadora de la Quiniela.

Hace las cuentas que el prompt maestro exige ejecutar, no estimar:

- marcador: matriz de Poisson con factor de empates -> 1X2, marcadores y Pleno al 15.
- boleto:   comprobaciones de coherencia, boleto A (4 dobles completos) y
            boleto B (reducida de 7 dobles al 13, código de Hamming [7,4]),
            con la distribución exacta de aciertos, el Pleno y las sueltas.
- postmortem: log-loss, Brier, fallos esperados frente a reales y calibración.

Solo usa la biblioteca estándar. Ejemplo de entrada: ejemplo-jornada.json.
"""
import argparse
import itertools
import json
import math
import sys

SIGNOS = "1X2"
PRECIO_APUESTA = 0.75
CATEGORIAS_PLENO = ["0", "1", "2", "M"]

# Distribución previa de 498 Plenos (prompt maestro, fase 7). Solo los 10 más frecuentes.
PREVIA_PLENO = {
    "1-1": 0.122, "1-0": 0.110, "2-1": 0.082, "M-1": 0.076, "M-0": 0.074,
    "0-1": 0.074, "2-0": 0.068, "1-2": 0.066, "0-0": 0.064, "M-2": 0.060,
}


# ---------------------------------------------------------------- marcadores

def _poisson(k, lam):
    return math.exp(-lam) * lam ** k / math.factorial(k)


def matriz_marcadores(lam_local, lam_visitante, factor_x=1.0, max_goles=10):
    """Matriz P(goles local = i, goles visitante = j), con la diagonal multiplicada
    por factor_x y renormalizada."""
    m = [[_poisson(i, lam_local) * _poisson(j, lam_visitante)
          for j in range(max_goles + 1)] for i in range(max_goles + 1)]
    for i in range(max_goles + 1):
        m[i][i] *= factor_x
    total = sum(map(sum, m))
    return [[v / total for v in fila] for fila in m]


def uno_x_dos(m):
    p1 = sum(m[i][j] for i in range(len(m)) for j in range(len(m)) if i > j)
    px = sum(m[i][i] for i in range(len(m)))
    return [p1, px, 1 - p1 - px]


def _categoria(goles):
    return CATEGORIAS_PLENO[min(goles, 3)]


def categorias_pleno(m):
    """Probabilidad de cada resultado del Pleno (0, 1, 2, M por equipo)."""
    p = {f"{a}-{b}": 0.0 for a in CATEGORIAS_PLENO for b in CATEGORIAS_PLENO}
    for i, fila in enumerate(m):
        for j, v in enumerate(fila):
            p[f"{_categoria(i)}-{_categoria(j)}"] += v
    return p


def _signo_pleno(resultado):
    a, b = (3 if g == "M" else int(g) for g in resultado.split("-"))
    if a == b:
        # M-M no implica empate exacto, pero se trata como X, igual que el boleto.
        return "X"
    return "1" if a > b else "2"


def tres_plenos(p_cat, signo):
    """Principal, conservador y de varianza, según las reglas de la fase 7.

    signo: el signo 1X2 más probable del partido del Pleno."""
    principal = max(p_cat, key=p_cat.get)
    compatibles = [r for r in PREVIA_PLENO if _signo_pleno(r) == signo]
    conservador = max(compatibles, key=PREVIA_PLENO.get) if compatibles else principal

    def goles(r):
        return sum(3 if g == "M" else int(g) for g in r.split("-"))

    candidatos = [r for r, v in p_cat.items() if v >= 0.06]
    varianza = max(candidatos, key=lambda r: (goles(r), p_cat[r])) if candidatos else principal
    return {"principal": principal, "conservador": conservador, "varianza": varianza}


# -------------------------------------------------------- evaluación exacta

def _poisson_binomial(probs):
    dist = [1.0]
    for p in probs:
        nueva = [0.0] * (len(dist) + 1)
        for k, v in enumerate(dist):
            nueva[k] += v * (1 - p)
            nueva[k + 1] += v * p
        dist = nueva
    return dist


def evaluar_columnas(probs, columnas, max_variables=10):
    """Distribución exacta del mejor número de aciertos entre las columnas.

    probs: 14 listas [p1, pX, p2]. columnas: cadenas de 14 caracteres sobre "1X2".
    Devuelve una lista donde el índice k es P(la mejor columna acierta exactamente k).
    """
    n = len(probs)
    variables = [i for i in range(n) if len({c[i] for c in columnas}) > 1]
    if len(variables) > max_variables:
        raise ValueError(f"{len(variables)} posiciones variables: demasiadas para enumerar")
    fijas = [i for i in range(n) if i not in variables]
    dist_fijas = _poisson_binomial(
        [probs[i][SIGNOS.index(columnas[0][i])] for i in fijas])

    dist_var = [0.0] * (len(variables) + 1)
    for resultado in itertools.product(range(3), repeat=len(variables)):
        p = 1.0
        for i, r in zip(variables, resultado):
            p *= probs[i][r]
        if p == 0:
            continue
        mejor = max(sum(SIGNOS[r] == c[i] for i, r in zip(variables, resultado))
                    for c in columnas)
        dist_var[mejor] += p

    total = [0.0] * (n + 1)
    for a, pa in enumerate(dist_fijas):
        for b, pb in enumerate(dist_var):
            total[a + b] += pa * pb
    return total


def al_menos(dist, k):
    return sum(dist[k:])


# ------------------------------------------------------------------ boletos

def _orden(p):
    return sorted(range(3), key=lambda s: -p[s])


def _hamming_7_4():
    """Las 16 palabras del código de Hamming [7,4] (radio de cobertura 1)."""
    palabras = []
    for v in itertools.product((0, 1), repeat=7):
        sindrome = 0
        for posicion, bit in enumerate(v, start=1):
            if bit:
                sindrome ^= posicion
        if sindrome == 0:
            palabras.append(v)
    return palabras


HAMMING = _hamming_7_4()
assert len(HAMMING) == 16


def _clases_laterales():
    """Un representante de cada una de las 8 clases laterales del código: las 8 maneras
    de reducir 7 dobles a 16 columnas manteniendo la garantía al 13."""
    vistas, clases = set(), []
    for v in itertools.product((0, 1), repeat=7):
        clave = frozenset(tuple(a ^ b for a, b in zip(v, h)) for h in HAMMING)
        if clave not in vistas:
            vistas.add(clave)
            clases.append(v)
    return clases


CLASES = _clases_laterales()
assert len(CLASES) == 8


def columnas_reducida(probs, dobles, clase):
    base = [SIGNOS[_orden(p)[0]] for p in probs]
    columnas = []
    for palabra in HAMMING:
        col = list(base)
        for d, bit in zip(dobles, palabra):
            col[d] = SIGNOS[_orden(probs[d])[bit ^ clase[dobles.index(d)]]]
        columnas.append("".join(col))
    return columnas


def columnas_completas(probs, dobles):
    base = [SIGNOS[_orden(p)[0]] for p in probs]
    columnas = []
    for bits in itertools.product((0, 1), repeat=len(dobles)):
        col = list(base)
        for d, bit in zip(dobles, bits):
            col[d] = SIGNOS[_orden(probs[d])[bit]]
        columnas.append("".join(col))
    return columnas


def _p14_reducida(probs, dobles, clase, p_sencillos):
    total = 0.0
    for palabra in HAMMING:
        p = 1.0
        for k, d in enumerate(dobles):
            p *= probs[d][_orden(probs[d])[palabra[k] ^ clase[k]]]
        total += p
    return p_sencillos * total


def _forzados(partidos):
    return [i for i, x in enumerate(partidos) if x.get("veto_unico")]


def _sencillos(probs, dobles):
    p = 1.0
    for i, pr in enumerate(probs):
        if i not in dobles:
            p *= max(pr)
    return p


def mejor_boleto_a(probs, forzados, n_dobles=4):
    if len(forzados) > n_dobles:
        raise ValueError(f"{len(forzados)} partidos con veto, pero el boleto A solo tiene {n_dobles} dobles")
    libres = [i for i in range(len(probs)) if i not in forzados]
    mejor = None
    for extra in itertools.combinations(libres, n_dobles - len(forzados)):
        dobles = sorted(forzados + list(extra))
        p14 = _sencillos(probs, dobles)
        for d in dobles:
            o = _orden(probs[d])
            p14 *= probs[d][o[0]] + probs[d][o[1]]
        if mejor is None or p14 > mejor[0]:
            mejor = (p14, dobles)
    return mejor[1], columnas_completas(probs, mejor[1])


def mejor_boleto_b(probs, forzados, objetivo="p14", n_dobles=7, finalistas=40):
    if len(forzados) > n_dobles:
        raise ValueError(f"{len(forzados)} partidos con veto, pero la reducida solo tiene {n_dobles} dobles")
    libres = [i for i in range(len(probs)) if i not in forzados]
    candidatos = []
    for extra in itertools.combinations(libres, n_dobles - len(forzados)):
        dobles = sorted(forzados + list(extra))
        ps = _sencillos(probs, dobles)
        for clase in CLASES:
            candidatos.append((_p14_reducida(probs, dobles, clase, ps), dobles, clase))
    candidatos.sort(key=lambda c: -c[0])
    if objetivo == "p14":
        _, dobles, clase = candidatos[0]
        return dobles, columnas_reducida(probs, dobles, clase), len(candidatos)

    k = {"p13": 13, "p12": 12}[objetivo]
    mejor = None
    for _, dobles, clase in candidatos[:finalistas]:
        cols = columnas_reducida(probs, dobles, clase)
        valor = al_menos(evaluar_columnas(probs, cols), k)
        if mejor is None or valor > mejor[0]:
            mejor = (valor, dobles, cols)
    return mejor[1], mejor[2], len(candidatos)


# ------------------------------------------------------------- comprobaciones

def comprobar(datos):
    avisos, errores = [], []
    partidos = datos["partidos"]
    if len(partidos) != 14:
        errores.append(f"Hay {len(partidos)} partidos; tienen que ser 14 (más el Pleno).")
    nombres = [p["partido"] for p in partidos]
    if len(set(nombres)) != len(nombres):
        errores.append("Hay partidos repetidos.")
    for p in partidos:
        s = sum(p["p"])
        if abs(s - 1) > 0.005:
            errores.append(f"{p['partido']}: las probabilidades suman {s:.3f}, no 1.")
        if any(v < 0 for v in p["p"]):
            errores.append(f"{p['partido']}: probabilidad negativa.")
    suma_x = sum(p["p"][1] for p in partidos)
    if not 2.5 <= suma_x <= 4.5:
        avisos.append(f"La suma de P(X) es {suma_x:.2f}; lo normal es rondar 3,5. Revisar el factor de empates.")
    return errores, avisos, suma_x


def _riesgo(p):
    o = sorted(p, reverse=True)
    if o[0] < 0.40:
        return "Muy alto"
    if o[0] < 0.50 or o[0] - o[1] < 0.10:
        return "Alto"
    if o[0] < 0.65:
        return "Moderado"
    return "Bajo"


# ---------------------------------------------------------------- informes

def _pct(x):
    return f"{100 * x:5.1f}%"


def _prob(x):
    """Porcentaje legible también cuando es muy pequeño."""
    if x >= 0.01:
        return _pct(x)
    return f"{100 * x:.3f}% (1 entre {1 / x:,.0f})".replace(",", ".") if x > 0 else "0%"


def _signo_mas_probable(p):
    return SIGNOS[_orden(p)[0]]


def _informe_distribucion(nombre, cols, dist, coste):
    lineas = [f"\n## {nombre}: {len(cols)} apuestas, {coste:.2f} €"]
    for k in (14, 13, 12, 11, 10):
        lineas.append(f"  P(≥{k}) = {_prob(al_menos(dist, k))}")
    esperados = sum(k * v for k, v in enumerate(dist))
    lineas.append(f"  Aciertos esperados de la mejor columna: {esperados:.2f}")
    return lineas


def cmd_marcador(args):
    m = matriz_marcadores(args.local, args.visitante, args.factor_x)
    p = uno_x_dos(m)
    print(f"1X2: 1 {_pct(p[0])} · X {_pct(p[1])} · 2 {_pct(p[2])}")
    marcadores = sorted(((m[i][j], f"{i}-{j}") for i in range(len(m)) for j in range(len(m))), reverse=True)
    print("Marcadores más probables: " + ", ".join(f"{r} {_pct(v)}" for v, r in marcadores[:6]))
    p_cat = categorias_pleno(m)
    print("Pleno: " + ", ".join(f"{r} {_pct(v)}" for r, v in sorted(p_cat.items(), key=lambda x: -x[1])[:6]))
    print("Tres Plenos: " + json.dumps(tres_plenos(p_cat, _signo_mas_probable(p)), ensure_ascii=False))


def cmd_boleto(args):
    with open(args.entrada, encoding="utf-8") as f:
        datos = json.load(f)
    errores, avisos, suma_x = comprobar(datos)
    if errores:
        print("ERRORES (se para aquí):")
        for e in errores:
            print("  - " + e)
        return 1

    partidos = datos["partidos"]
    probs = [p["p"] for p in partidos]
    presupuesto = datos.get("presupuesto", 12)
    forzados = _forzados(partidos)
    salida = [f"# Jornada {datos.get('jornada', '?')} · presupuesto {presupuesto} €",
              f"Suma de P(X): {suma_x:.2f}"]
    salida += ["AVISO: " + a for a in avisos]

    salida.append("\n## Los 14 signos")
    fallos = 0.0
    for i, p in enumerate(partidos, 1):
        signo = SIGNOS[_orden(p["p"])[0]]
        fallos += 1 - max(p["p"])
        marca = "" if max(p["p"]) >= 0.65 else " ⚠️"
        veto = " (veto: nunca signo único)" if p.get("veto_unico") else ""
        salida.append(f"{i:2d}. {p['partido']:<32} 1 {_pct(p['p'][0])} X {_pct(p['p'][1])} 2 {_pct(p['p'][2])}"
                      f"  → {signo}{marca}  riesgo {_riesgo(p['p'])}{veto}")
    salida.append(f"Fallos esperados con los 14 signos individuales: {fallos:.2f}")

    dobles_a, cols_a = mejor_boleto_a(probs, forzados)
    dist_a = evaluar_columnas(probs, cols_a)
    dobles_b, cols_b, n_cand = mejor_boleto_b(probs, forzados, args.objetivo)
    dist_b = evaluar_columnas(probs, cols_b)

    for nombre, cols, dist, dobles in (("Boleto A · 4 dobles completos", cols_a, dist_a, dobles_a),
                                       ("Boleto B · reducida de 7 dobles al 13", cols_b, dist_b, dobles_b)):
        coste = len(cols) * PRECIO_APUESTA
        if coste > presupuesto:
            print(f"ERROR: {nombre} cuesta {coste:.2f} €, más que el presupuesto ({presupuesto} €).")
            return 1
        if len(set(cols)) != len(cols):
            print(f"ERROR: {nombre} tiene columnas duplicadas.")
            return 1
        salida += _informe_distribucion(nombre, cols, dist, coste)
        salida.append("  Dobles: " + ", ".join(
            f"{partidos[d]['partido']} ({''.join(SIGNOS[s] for s in sorted(_orden(probs[d])[:2]))})"
            for d in dobles))
        salida.append("  Columnas:")
        salida += [f"    {n:2d}. {c}" for n, c in enumerate(cols, 1)]
    salida.append(f"\n(Reducida: {n_cand} combinaciones evaluadas; objetivo {args.objetivo}.)")

    pleno = datos.get("pleno")
    if pleno:
        m = matriz_marcadores(pleno["lambda_local"], pleno["lambda_visitante"], pleno.get("factor_x", 1.0))
        p_cat = categorias_pleno(m)
        p_1x2 = uno_x_dos(m)
        tres = tres_plenos(p_cat, _signo_mas_probable(p_1x2))
        salida.append(f"\n## Pleno al 15 · {pleno['partido']}")
        salida.append(f"  1X2 del partido: 1 {_pct(p_1x2[0])} · X {_pct(p_1x2[1])} · 2 {_pct(p_1x2[2])}")
        for tipo, r in tres.items():
            salida.append(f"  {tipo:<12} {r}  {_pct(p_cat[r])}")
        p_principal = p_cat[tres["principal"]]
        salida.append("  Se juega solo el principal, el mismo en todas las columnas.")
        salida.append(f"  P(14 y Pleno) con el boleto B: {_prob(al_menos(dist_b, 14) * p_principal)}")

    sueltas = datos.get("sueltas")
    if sueltas:
        salida.append("\n## Apuestas sueltas")
        p_todas = 1.0
        for s in sueltas:
            p_todas *= s["p"]
            marca = "" if s["p"] >= 0.80 else "  ⚠️ por debajo del 80%"
            salida.append(f"  {s['apuesta']:<40} {_pct(s['p'])}{marca}")
        salida.append(f"  Aciertos esperados: {sum(s['p'] for s in sueltas):.2f} de {len(sueltas)}"
                      f" · P(todas) = {_pct(p_todas)}")
        if len({s.get('partido') for s in sueltas}) < len(sueltas):
            salida.append("  AVISO: hay sueltas del mismo partido (están correlacionadas).")

    print("\n".join(salida))
    return 0


def puntuar(partidos):
    """Log-loss, Brier y fallos de una lista de partidos con 'p' y 'resultado' (1, X o 2)."""
    jugados = [p for p in partidos if p.get("resultado") in SIGNOS]
    if not jugados:
        raise ValueError("Ningún partido tiene 'resultado' (1, X o 2).")
    log_loss = brier = fallos_esperados = fallos_reales = 0.0
    for p in jugados:
        r = SIGNOS.index(p["resultado"])
        log_loss -= math.log(max(p["p"][r], 1e-12))
        brier += sum((p["p"][s] - (s == r)) ** 2 for s in range(3))
        fallos_esperados += 1 - max(p["p"])
        fallos_reales += _orden(p["p"])[0] != r
    n = len(jugados)
    return {"partidos": n, "log_loss": log_loss / n, "brier": brier / n,
            "fallos_esperados": fallos_esperados, "fallos_reales": fallos_reales}


def cmd_postmortem(args):
    partidos = []
    for ruta in args.entradas:
        with open(ruta, encoding="utf-8") as f:
            partidos += json.load(f)["partidos"]
    r = puntuar(partidos)
    print(f"Partidos puntuados: {r['partidos']}")
    print(f"Log-loss: {r['log_loss']:.4f}  (referencia: repartir 1/3 a cada signo da {math.log(3):.4f})")
    print(f"Brier:    {r['brier']:.4f}  (referencia: 1/3 a cada signo da 0.6667)")
    print(f"Fallos del signo principal: {r['fallos_reales']:.0f} reales frente a {r['fallos_esperados']:.2f} esperados")

    # Calibración por tramos del signo principal: solo tiene sentido con varias jornadas.
    tramos = {}
    for p in partidos:
        if p.get("resultado") not in SIGNOS:
            continue
        principal = max(p["p"])
        tramo = min(int(principal * 10), 9) / 10
        t = tramos.setdefault(tramo, [0, 0.0, 0])
        t[0] += 1
        t[1] += principal
        t[2] += _orden(p["p"])[0] == SIGNOS.index(p["resultado"])
    print("\nCalibración del signo principal (tramo: partidos, declarado, real):")
    for tramo in sorted(tramos):
        n, declarado, aciertos = tramos[tramo]
        aviso = "  (muestra pequeña)" if n < 30 else ""
        print(f"  {int(tramo * 100)}–{int(tramo * 100) + 10}%: {n:3d}, {_pct(declarado / n)}, {_pct(aciertos / n)}{aviso}")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="orden", required=True)

    m = sub.add_parser("marcador", help="1X2, marcadores y Pleno a partir de los goles esperados")
    m.add_argument("--local", type=float, required=True, help="goles esperados del local")
    m.add_argument("--visitante", type=float, required=True, help="goles esperados del visitante")
    m.add_argument("--factor-x", type=float, default=1.0, help="factor de empates (ligas 1.08, Liga F 0.85)")
    m.set_defaults(funcion=cmd_marcador)

    b = sub.add_parser("boleto", help="comprobaciones, boletos A y B, Pleno y sueltas")
    b.add_argument("entrada", help="JSON de la jornada (ver ejemplo-jornada.json)")
    b.add_argument("--objetivo", choices=["p14", "p13", "p12"], default="p14",
                   help="qué maximiza la reducida (por defecto, P(14))")
    b.set_defaults(funcion=cmd_boleto)

    p = sub.add_parser("postmortem", help="log-loss, Brier y calibración de una o varias jornadas")
    p.add_argument("entradas", nargs="+", help="JSON de jornada con 'resultado' (1, X o 2) en cada partido")
    p.set_defaults(funcion=cmd_postmortem)

    args = parser.parse_args(argv)
    return args.funcion(args) or 0


if __name__ == "__main__":
    sys.exit(main())
