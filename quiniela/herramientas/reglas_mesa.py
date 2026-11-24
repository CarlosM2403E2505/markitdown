#!/usr/bin/env python3
"""Reglas codificadas de la mesa (22/11/2026). Desde la J24, el boleto sale SOLO de estas reglas.

Carlos (22/11): «tiene que ser la mesa quien decida», tope de 18 € por jornada y que todas las columnas
dejen de llevar los mismos fijos. Explicación y prueba histórica: analisis/reglas-mesa.md.

R1 PRESUPUESTO   Como máximo 18 € por jornada, todo incluido (24 apuestas de 0,75 €).
R2 OBJETIVO      De los formatos que cumplen R3, se elige el de mayor P(≥13). Desempate: P(14), después P(≥12).
R3 DIVERSIDAD    En cada partido, el signo favorito puede ir como mucho en esta parte de las columnas:
                   P(favorito) < 45 %       → 60 %
                   45 % ≤ P < 55 %          → 75 %
                   55 % ≤ P < 65 %          → 90 %
                   P ≥ 65 %                 → sin tope
                 Así ningún fijo con poco margen está en todas las columnas. Si la mesa da al favorito más de
                 8 puntos por encima de las casas, se aplica el tope del tramo de abajo (las cuotas no cambian
                 ninguna probabilidad: solo obligan a cubrir más ese partido). Lo mismo si el favorito llega en
                 mala forma: 5 puntos o menos en sus 5 últimos partidos de liga (campo `forma_favorito` del
                 partido, 0-15). Prueba: modelo/favoritos_fallan.py (es precaución de cobertura, no cambia la P).
                 R3b (23/11, estudio de sorpresas): si hay mercado, el tramo se busca también con la probabilidad
                 de las casas para el signo favorito de la mesa y se aplica el tope más estricto. Las casas están
                 bien calibradas (7.912 favoritos 45-70 % de Primera y Segunda 2005-26: daban 46,4 % de sorpresa
                 y salió 44,3 %), así que no es pesimismo. Prueba: modelo/sorpresas.py, analisis/sorpresas.md.
R4 PLENO         El marcador más probable de la mesa en todas las apuestas.
R5 PROBABILIDAD  Solo las de la mesa (modelo + noticias A/B). Las cuotas y el % del público no cambian nada.
R6 FORMATOS      Se prueban siempre todos: directas, reducidas oficiales, directa + sencillas protegidas y
                 24 sencillas optimizadas (búsqueda de máxima P(≥13) con el tope de R3).
R7 CUÁNTO JUGAR  18 € es un tope, no un objetivo. Cada euro pierde de media 0,45 €, así que se juega por bloques
                 de 8 columnas (6, 12 o 18 €) y solo se añade un bloque si su P(≥13) por euro es al menos la
                 mitad de la del primer bloque (EFICIENCIA_MIN). Si no, se para ahí.

Uso: python3 herramientas/reglas_mesa.py jornadas/j24/j24.json [--guardar]
"""
import argparse, itertools, json, math, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import quiniela_calc as qc
import boletos_oficiales as bo

S = "1X2"
PRECIO = 0.75
PRESUPUESTO_MAX = 18.0
TOPES = [(0.45, 0.60), (0.55, 0.75), (0.65, 0.90), (1.01, 1.00)]  # (P favorito por debajo de, tope)
N_MUESTRAS = 20000
N_CANDIDATAS = 1000
N_EXTRA = 2000      # columnas sacadas de las muestras de optimización
N_OPT = 6000        # muestras para optimizar (las de evaluar son otras: N_MUESTRAS)


AVISO_MERCADO = 0.08
TOPES_JORNADA = None  # topes por partido de la jornada en curso (los fija topes_partidos)


MALA_FORMA = 5  # puntos de 15 o menos en los 5 últimos de liga


def tope(pfav, ventaja=0.0, forma=None):
    ts = [t for _, t in TOPES]
    for k, (lim, t) in enumerate(TOPES):
        if pfav < lim:
            duro = ventaja > AVISO_MERCADO or (forma is not None and forma <= MALA_FORMA and pfav < 0.70)
            return ts[max(k - 1, 0)] if duro else t
    return 1.0


def topes_partidos(partidos):
    """Tope de R3 por partido, con el aviso de las casas (si hay mercado) y la mala forma del favorito."""
    out = []
    for x in partidos:
        p = x["p"]; f = int(np.argmax(p)); m = x.get("mercado")
        t = tope(max(p), (p[f] - m[f]) if m else 0.0, x.get("forma_favorito"))
        if m:  # R3b (23/11): el tramo se mira también con la P de las casas para ese signo; manda el más estricto
            t = min(t, tope(m[f], 0.0, x.get("forma_favorito")))
        if x.get("tope_mesa"):  # 24/11 (orden de Carlos: asegurar fijos): tope fijado por la mesa para ese partido
            t = min(t, float(x["tope_mesa"]))
        out.append(t)
    return out


def tope_i(i, p):
    return TOPES_JORNADA[i] if TOPES_JORNADA else tope(max(p))


def pcol(probs, c):
    return math.prod(probs[i][S.index(c[i])] for i in range(14))


def diversidad(probs, cols):
    """Lista de incumplimientos de R3: (partido, parte de columnas con el favorito, tope)."""
    out = []
    for i, p in enumerate(probs):
        f = S[int(np.argmax(p))]
        share = sum(c[i] == f for c in cols) / len(cols)
        t = tope_i(i, p)
        if share > t + 1e-9:
            out.append((i + 1, round(share, 3), t))
    return out


def muestras(probs, n=N_MUESTRAS, semilla=24):
    rng = np.random.default_rng(semilla)
    P = np.array(probs)
    u = rng.random((n, 14))
    return (u >= P[:, 0]).astype(np.int8) + (u >= P[:, 0] + P[:, 1]).astype(np.int8)


def a_idx(cols):
    return np.array([[S.index(s) for s in c] for c in cols], dtype=np.int8)


def evaluar(probs, cols, Y):
    """P(14) exacta y P(≥13), P(≥12), P(≥10) por muestreo (las mismas muestras para todos los formatos)."""
    C = a_idx(cols)
    best = np.zeros(len(Y), dtype=np.int8)
    for k in range(0, len(C), 64):
        hits = (Y[:, None, :] == C[None, k:k + 64, :]).sum(axis=2)
        best = np.maximum(best, hits.max(axis=1))
    return {"p14": sum(pcol(probs, c) for c in set(cols)), "p13": float((best >= 13).mean()),
            "p12": float((best >= 12).mean()), "p10": float((best >= 10).mean())}


def optimizadas(probs, n, Y, ya=()):
    """n sencillas que maximizan P(≥13) (cobertura a distancia ≤ 1 de las muestras), respetando R3."""
    orden = [qc._orden(p) for p in probs]
    cand = ["".join(S[orden[i][r]] for i, r in enumerate(rg)) for _, rg in qc._k_mejores(probs, orden, N_CANDIDATAS)]
    # también columnas sacadas de las muestras: dan variedad cuando los topes obligan a salir del favorito
    vistos = set(cand)
    extra = sorted({"".join(S[v] for v in row) for row in Y} - vistos, key=lambda c: -pcol(probs, c))[:N_EXTRA]
    cand += extra
    cand = [c for c in cand if c not in set(ya)]
    C0 = a_idx(cand)
    hecho = np.zeros(len(Y), dtype=bool)
    if ya:
        A = a_idx(list(ya))
        hecho = ((Y[:, None, :] == A[None, :, :]).sum(axis=2) >= 13).any(axis=1)
    total = len(ya) + n
    fav = [int(np.argmax(p)) for p in probs]
    seg = [qc._orden(p)[1] for p in probs]
    lim = [math.floor(tope_i(i, p) * total + 1e-9) for i, p in enumerate(probs)]
    cuenta = [sum(S.index(c[i]) == fav[i] for c in ya) for i in range(14)]
    P = np.array(probs)
    elegidas, puestas = [], set(ya)
    for _ in range(n):
        # R3: en los partidos que ya llegaron a su tope, el favorito de la candidata se cambia por el 2.º signo
        C = C0.copy()
        for i in range(14):
            if cuenta[i] + 1 > lim[i]:
                C[C[:, i] == fav[i], i] = seg[i]
        gan = np.zeros(len(C))
        for k in range(0, len(C), 200):
            gan[k:k + 200] = (((Y[:, None, :] == C[None, k:k + 200, :]).sum(axis=2) >= 13) & ~hecho[:, None]).sum(axis=0)
        pc = np.prod(P[np.arange(14), C], axis=1)
        gan = gan + pc / pc.max() * 0.5
        txt = ["".join(S[v] for v in row) for row in C]
        for j, t in enumerate(txt):
            if t in puestas: gan[j] = -1
        j = int(np.argmax(gan))
        if gan[j] < 0:
            break
        elegidas.append(txt[j]); puestas.add(txt[j])
        hecho |= (Y == C[j]).sum(axis=1) >= 13
        for i in range(14):
            cuenta[i] += int(C[j, i] == fav[i])
    return elegidas


def formatos(probs, Y, presupuesto=PRESUPUESTO_MAX):
    """Todos los formatos de R6 que caben en el presupuesto. Se optimiza con muestras distintas de las de evaluar."""
    Y = muestras(probs, N_OPT, semilla=7)
    max_ap = int(presupuesto / PRECIO + 1e-9)
    bo.CODIGOS = getattr(bo, "CODIGOS", None) or {"R1": bo.ternario42(), "R2": bo.hamming74(), "R3": bo.codigo_cubridor(3, 3)}
    out = {}
    for nombre, d, t, cod in [("Directa 3 dobles + 1 triple", 3, 1, None), ("Directa 4 dobles", 4, 0, None),
                              ("Directa 1 doble + 2 triples", 1, 2, None), ("Reducida 3 (3 dobles + 3 triples)", 3, 3, "R3"),
                              ("Reducida 2 (7 dobles)", 7, 0, "R2"), ("Reducida 1 (4 triples)", 0, 4, "R1")]:
        _, dob, tri, cols = bo.candidatos(probs, d, t, cod, set())
        if len(cols) > max_ap:
            continue
        out[f"{nombre} · {len(cols)} ap."] = cols
        resto = max_ap - len(cols)
        if resto >= 4:
            extra = optimizadas(probs, resto, Y, ya=cols)
            out[f"{nombre} + {len(extra)} sencillas optimizadas"] = cols + extra
    out[f"{max_ap} sencillas optimizadas"] = optimizadas(probs, max_ap, Y)
    out[f"{max_ap} sencillas más probables"] = qc.columnas_mas_probables(probs, max_ap)
    return out


EFICIENCIA_MIN = 0.5


def presupuesto_r7(probs):
    """R7: 6, 12 o 18 € según lo que rinde cada bloque de 8 sencillas optimizadas."""
    Y = muestras(probs, N_OPT, semilla=7); Ye = muestras(probs)
    p13 = {n: evaluar(probs, optimizadas(probs, n, Y), Ye)["p13"] for n in (8, 16, 24)}
    base = p13[8] / 8
    n = 8
    for m in (16, 24):
        if (p13[m] - p13[m - 8]) / 8 >= EFICIENCIA_MIN * base:
            n = m
        else:
            break
    return PRECIO * n, p13


def decidir(probs, presupuesto=PRESUPUESTO_MAX):
    Y = muestras(probs)
    tabla = []
    for nombre, cols in formatos(probs, Y, presupuesto).items():
        r = evaluar(probs, cols, Y)
        inc = diversidad(probs, cols)
        tabla.append({"formato": nombre, "apuestas": len(cols), "coste": PRECIO * len(cols), **r,
                      "cumple_R3": not inc, "incumple": inc, "columnas": cols})
    validos = [t for t in tabla if t["cumple_R3"] and t["coste"] <= presupuesto + 1e-9]
    if not validos:  # no debería pasar: las sencillas optimizadas se construyen dentro de los topes
        raise SystemExit("Ningún formato cumple R3: revisar " + ", ".join(f"{t['formato']} {t['incumple']}" for t in tabla))
    el = max(validos, key=lambda t: (round(t["p13"], 3), t["p14"], t["p12"]))
    return el, tabla


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("jornada"); ap.add_argument("--guardar", action="store_true")
    ap.add_argument("--presupuesto", type=float, help="por defecto lo fija R7")
    a = ap.parse_args()
    d = json.load(open(a.jornada, encoding="utf-8"))
    probs = [x["p"] for x in d["partidos"]]
    global TOPES_JORNADA
    TOPES_JORNADA = topes_partidos(d["partidos"])
    if a.presupuesto is None:
        a.presupuesto, p13 = presupuesto_r7(probs)
        print("R7: P(≥13) con 8/16/24 sencillas = " + " / ".join(f"{100 * v:.2f} %" for v in p13.values()) + f" → se juegan {a.presupuesto:.0f} €")
    assert a.presupuesto <= PRESUPUESTO_MAX, "R1: el tope es 18 €"
    el, tabla = decidir(probs, a.presupuesto)
    print(f"Jornada {d['jornada']} · reglas de la mesa (R1-R7) · tope {a.presupuesto:.0f} €\n")
    print(f"{'Formato':52s} {'€':>6s} {'P(14)':>13s} {'P(≥13)':>7s} {'P(≥12)':>7s}  R3")
    for t in sorted(tabla, key=lambda t: -t["p13"]):
        print(f"{t['formato']:52s} {t['coste']:6.2f} {'1/' + format(round(1 / t['p14']), ',').replace(',', '.'):>13s} "
              f"{100 * t['p13']:6.2f}% {100 * t['p12']:6.1f}%  {'✓' if t['cumple_R3'] else '✗ ' + str(len(t['incumple'])) + ' partidos'}"
              + ("  ← ELEGIDO" if t is el else ""))
    print(f"\nElegido: {el['formato']} · {el['apuestas']} apuestas · {el['coste']:.2f} €")
    cols = el["columnas"]
    print("\nCobertura por partido (columnas con cada signo):")
    for i, x in enumerate(d["partidos"]):
        cnt = {s: sum(c[i] == s for c in cols) for s in S}
        print(f"  {i + 1:>2} {x['partido']:32s} 1:{cnt['1']:>3} X:{cnt['X']:>3} 2:{cnt['2']:>3}   mesa {'/'.join(f'{100 * v:.0f}' for v in x['p'])}  tope fav {100 * TOPES_JORNADA[i]:.0f} %")
    pl = d.get("pleno", {})
    marc = pl.get("cats") or pl.get("empirica") or {}
    pleno = max(marc, key=marc.get) if marc else pl.get("marcador")
    print(f"\nPleno (R4): {pleno} en todas las apuestas")
    if a.guardar:
        d["boleto_mesa"] = {"reglas": "herramientas/reglas_mesa.py (R1-R7, 22/11/2026)", "formato": el["formato"],
                            "apuestas": el["apuestas"], "coste": el["coste"], "columnas": cols, "pleno": pleno,
                            "p14": round(el["p14"], 6), "p13": round(el["p13"], 4), "p12": round(el["p12"], 4),
                            "comparativa": [{k: (round(v, 6) if isinstance(v, float) else v) for k, v in t.items() if k != "columnas"} for t in tabla]}
        json.dump(d, open(a.jornada, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("Guardado en", a.jornada, "→ boleto_mesa")


if __name__ == "__main__":
    main()
