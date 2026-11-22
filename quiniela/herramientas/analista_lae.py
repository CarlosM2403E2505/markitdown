#!/usr/bin/env python3
"""Analista LAE y Analista de Premios (22/11/2026). Estudio en analisis/lae-a-fondo.md.

Se basa en las normas oficiales de SELAE (Normas de La Quiniela y Elige 8, oct. 2019) y en el
histórico oficial 2002-2018 (749 jornadas con acertantes). NO cambia ninguna probabilidad de la mesa
(R5), salvo el caso que fija la propia norma: partido que LAE va a sortear (norma 39.ª B: 100 bolas
proporcionales al % de pronósticos del público).

Subcomandos
  valor   <jornada.json> [--publico pub.json]   valor por signo (mesa / público) y premio esperado de cada columna
  sorteo  <jornada.json> N [--p 1.0]            probabilidad final de un partido que puede ir a sorteo
  premio  <recaudacion> <prod_publico>          acertantes de 14 y premio esperados

El % del público se lee de jornada['publico']['porcentajes'][N]['lae'] = [p1, pX, p2] (en %), o de --publico
con el mismo formato. Fuente habitual: % LAE en quiniela15.com o eduardolosilla.es.
"""
import argparse, json, math, sys

S = "1X2"
PRECIO = 0.75
FONDO_14 = 0.16          # norma 7.ª: 16 % de la recaudación íntegra a la 1.ª categoría
FONDO_13 = 0.075
CORRELACION = 2.5        # el público no es independiente (J21: 4 acertantes reales frente a 1,5 con independencia)
VALOR_ALTO = 1.25        # mesa / público ≥ 1,25 → signo infravalorado por el público
VALOR_BAJO = 0.80        # ≤ 0,80 → signo sobrejugado por el público
P_MIN_VALOR = 0.20       # solo se señala valor en signos con P mesa ≥ 20 %


def publico(d, ruta=None):
    if ruta:
        pub = json.load(open(ruta))
        pub = pub.get("porcentajes", pub)
    else:
        pub = (d.get("publico") or {}).get("porcentajes")
    if not pub:
        sys.exit("Falta el % del público (jornada['publico']['porcentajes'] o --publico)")
    return {int(k): [x / 100 for x in v["lae"]] for k, v in pub.items()}


def mezcla_sorteo(p_mesa, p_pub, p_sorteo):
    """Norma 39.ª B: si no hay resultado válido, el signo sale de 100 bolas proporcionales al público."""
    return [(1 - p_sorteo) * a + p_sorteo * b for a, b in zip(p_mesa, p_pub)]


def acertantes_14(recaudacion, prod_pub, correlacion=CORRELACION):
    return recaudacion / PRECIO * prod_pub * correlacion


def premio_14(recaudacion, prod_pub, correlacion=CORRELACION):
    """Premio esperado por apuesta si se acierta esa columna (se reparte con los demás acertantes)."""
    n = acertantes_14(recaudacion, prod_pub, correlacion)
    return FONDO_14 * recaudacion / (1 + n)


def columnas(d):
    b = d.get("boleto_mesa") or d.get("boleto_provisional") or {}
    cols = b.get("columnas")
    if cols:
        return cols
    sig = b.get("signos")
    if not sig:
        return []
    out = [""]
    for i in range(1, 15):
        out = [c + s for c in out for s in sig[str(i)].split()]
    return out


def valor(d, pub, recaudacion):
    print("Partido | mesa 1-X-2 | público 1-X-2 | mesa/público | aviso")
    for p in d["partidos"][:14]:
        n, pm, pp = p["n"], p["p"], pub[p["n"]]
        r = [a / b if b else float("inf") for a, b in zip(pm, pp)]
        aviso = [f"{S[i]} con valor" for i in range(3) if r[i] >= VALOR_ALTO and pm[i] >= P_MIN_VALOR]
        fav = max(range(3), key=lambda i: pp[i])
        if r[fav] <= VALOR_BAJO:
            aviso.append(f"{S[fav]} sobrejugado")
        print(f"{n:>2} {p['partido'][:28]:<28} | {'-'.join(f'{x:.0%}' for x in pm)} | "
              f"{'-'.join(f'{x:.0%}' for x in pp)} | {' '.join(f'{x:.2f}' for x in r)} | {', '.join(aviso)}")
    cols = columnas(d)
    if not cols:
        return
    print(f"\nColumna | P(14) mesa | acertantes 14 esperados | premio 14 si acierta | índice de valor")
    filas = []
    for c in cols:
        pm = math.prod(d["partidos"][i]["p"][S.index(s)] for i, s in enumerate(c))
        pp = math.prod(pub[i + 1][S.index(s)] for i, s in enumerate(c))
        filas.append((c, pm, acertantes_14(recaudacion, pp), premio_14(recaudacion, pp), pm / pp))
    for c, pm, n, pr, iv in sorted(filas, key=lambda f: -f[1] * f[3]):
        print(f"{c} | {pm:.2e} | {n:,.1f} | {pr:,.0f} € | {iv:.2f}")


def main(argv=None):
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    v = sub.add_parser("valor"); v.add_argument("jornada"); v.add_argument("--publico"); v.add_argument("--recaudacion", type=float, default=1.5e6)
    s = sub.add_parser("sorteo"); s.add_argument("jornada"); s.add_argument("n", type=int); s.add_argument("--p", type=float, default=1.0); s.add_argument("--publico")
    pr = sub.add_parser("premio"); pr.add_argument("recaudacion", type=float); pr.add_argument("prod_publico", type=float)
    a = ap.parse_args(argv)
    if a.cmd == "premio":
        print(f"acertantes 14 ≈ {acertantes_14(a.recaudacion, a.prod_publico):.1f} · premio ≈ {premio_14(a.recaudacion, a.prod_publico):,.0f} €")
        return
    d = json.load(open(a.jornada))
    pub = publico(d, a.publico)
    if a.cmd == "valor":
        valor(d, pub, a.recaudacion)
    else:
        p = next(x for x in d["partidos"] if x["n"] == a.n)
        print(" ".join(f"{S[i]} {x:.1%}" for i, x in enumerate(mezcla_sorteo(p["p"], pub[a.n], a.p))))


if __name__ == "__main__":
    main()
