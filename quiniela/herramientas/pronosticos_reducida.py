#!/usr/bin/env python3
"""Artefacto «Pronósticos por reducida» (Carlos, 25/11/2026).

Opción A: 3 Reducidas 1 oficiales (4 triples, 9 apuestas, 6,75 € cada una), con triples en partidos distintos.
Opción B: Reducida 1 + sencillas optimizadas en boletos de 8 (la de siempre, reglas_mesa.py).
Bloque «Qué falta»: datos pendientes, signos sin cubrir y fijos sin protección (lección de la J24).

Columnas de la Reducida 1 = tabla oficial (boletos_oficiales.ternario42, BOE 9/1/2006 norma 21.ª B):
los triples se asignan por orden creciente de partido. P(14) exacta; P(≥13) exacta por enumeración.
Probabilidad: R5b (casas si el partido trae `mercado`; si no, `p`).

Uso: python3 herramientas/pronosticos_reducida.py jornadas/j25/j25.json [--sencillas 16] [--html salida.html]
"""
import argparse, html, itertools, json, math, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import boletos_oficiales as bo
import reglas_mesa as rm

S = "1X2"; PRECIO = 0.75; R1 = bo.ternario42()


def expandir(base, triples):
    out = []
    for w in R1:
        c = list(base)
        for k, i in enumerate(sorted(triples)):
            c[i] = S[w[k]]
        out.append("".join(c))
    return out


def exacta(probs, cols):
    """Distribución exacta del mejor acierto (0-14) sobre las columnas, enumerando solo los partidos que varían."""
    C = rm.a_idx(cols); P = np.array(probs)
    var = [i for i in range(14) if len(set(C[:, i])) > 1]
    fij = [i for i in range(14) if i not in var]
    # partidos fijos: número de aciertos fijos ~ Poisson-binomial
    pf = np.ones(1)
    for i in fij:
        q = P[i, C[0, i]]; pf = np.concatenate([pf * (1 - q), [0]]) + np.concatenate([[0], pf * q])
    dist = np.zeros(15)
    outs = np.array(list(itertools.product(range(3), repeat=len(var))), dtype=np.int8) if var else np.zeros((1, 0), np.int8)
    for k in range(0, len(outs), 200000):
        O = outs[k:k + 200000]
        pr = np.prod(P[var, :][np.arange(len(var)), O], axis=1) if var else np.ones(len(O))
        best = (O[:, None, :] == C[None, :, var]).sum(axis=2).max(axis=1)
        for v in range(len(var) + 1):
            m = best == v
            if m.any():
                dist[v:v + len(fij) + 1] += pr[m].sum() * pf
    return dist


def al_menos(dist, k):
    return float(dist[k:].sum())


def mejor_tres(probs, obligatorios=(), n=3, n_muestras=120000):
    """n conjuntos de 4 triples (greedy por P(≥13) del conjunto) con muestras; el resto de partidos al favorito.
    obligatorios: partidos (índice 0) que deben ir a triple en alguna reducida (fijos < 65 %: nadie a 1 en todas)."""
    Y = rm.muestras(probs, n_muestras, semilla=25)
    fav = np.array([int(np.argmax(p)) for p in probs])
    H = (Y == fav[None, :])  # acierto del favorito por partido
    code = {w for w in R1}
    combos = list(itertools.combinations(range(14), 4))
    nh = H.sum(axis=1)

    def mejor_r1(T):
        T = list(T)
        fuera = nh - H[:, T].sum(axis=1)
        # palabra del código: (a,b,a+b,2a+b) mod 3 en el orden de los partidos
        a, b, c, d = (Y[:, t] for t in sorted(T))
        en = ((a + b) % 3 == c) & ((2 * a + b) % 3 == d)
        return fuera + 3 + en.astype(int)

    elegidos, best = [], np.zeros(len(Y), int)
    for k in range(n):
        top = None
        hechos = set().union(*elegidos) if elegidos else set()
        for T in combos:
            if any(len(set(T) & set(e)) > 1 for e in elegidos):
                continue  # partidos distintos: como mucho 1 triple compartido con cada reducida
            if len(set(obligatorios) - hechos - set(T)) > 4 * (n - k - 1):
                continue  # que los obligatorios quepan en las reducidas que quedan
            v = np.maximum(best, mejor_r1(T))
            sc = (v >= 13).mean() + 1e-3 * (v >= 12).mean()
            if not top or sc > top[0]:
                top = (sc, T, v)
        elegidos.append(top[1]); best = top[2]
    return elegidos


def acierto(probs, c):
    return 100 * float(np.mean([probs[i][S.index(c[i])] for i in range(14)]))


def resumen(probs, cols, coste):
    d = exacta(probs, cols)
    return {"apuestas": len(cols), "coste": coste, "p14": al_menos(d, 14), "p13": al_menos(d, 13), "p12": al_menos(d, 12),
            "p10": al_menos(d, 10), "distintas": len(set(cols))}


def ordenar_proteccion(probs, base_cols, sencillas, por_boleto=8):
    """Boleto 1 primero con las columnas que más signos nuevos (no favoritos) cubren: la protección va delante."""
    cub = {(i, c[i]) for c in base_cols for i in range(14)}
    resto, out = list(sencillas), []
    while resto:
        j = max(range(len(resto)), key=lambda k: (len({(i, resto[k][i]) for i in range(14)} - cub), rm.pcol(probs, resto[k])))
        c = resto.pop(j); out.append(c); cub |= {(i, c[i]) for i in range(14)}
    return out


def que_falta(d, probs, opciones):
    falta = []
    sin_m = [x["n"] for x in d["partidos"] if not x.get("mercado")]
    if sin_m:
        falta.append(("Dato", f"Cuotas de las casas (R5b) en {len(sin_m)} de 14 partidos: {', '.join(map(str, sin_m))}"))
    for x in d["partidos"]:
        if "sin dato" in x.get("fuente_p", ""):
            falta.append(("Dato", f"P{x['n']} {x['partido']}: sin probabilidad propia (base de Segunda)"))
    for k in d.get("pendientes", []):
        falta.append(("Dato", k))
    for nombre, cols in opciones:
        for i, x in enumerate(d["partidos"]):
            sig = {c[i] for c in cols}
            f = S[int(np.argmax(probs[i]))]
            if sig == {f} and max(probs[i]) < 0.65:
                falta.append(("Fijo sin protección", f"{nombre}: P{i + 1} {x['partido']} a {f} en todas ({100 * max(probs[i]):.0f} %)"))
            elif len(sig) < 3:
                no = [s for s in S if s not in sig]
                pno = sum(probs[i][S.index(s)] for s in no)
                if pno >= 0.25:
                    falta.append(("Signo sin cubrir", f"{nombre}: P{i + 1} {x['partido']} sin {'/'.join(no)} ({100 * pno:.0f} %)"))
    return falta


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("jornada"); ap.add_argument("--sencillas", type=int, default=16)
    ap.add_argument("--html"); ap.add_argument("--json")
    a = ap.parse_args()
    d = json.load(open(a.jornada, encoding="utf-8"))
    probs = rm.probabilidades(d["partidos"])
    rm.TOPES_JORNADA = rm.topes_partidos(d["partidos"])
    base = "".join(S[int(np.argmax(p))] for p in probs)
    debiles = [i for i, p in enumerate(probs) if max(p) < 0.65]
    if len(debiles) > 12:  # no caben: los 12 más flojos
        debiles = sorted(debiles, key=lambda i: max(probs[i]))[:12]
    sets = mejor_tres(probs, debiles)
    A = []
    for T in sets:
        cols = expandir(base, T)
        A.append({"triples": [i + 1 for i in sorted(T)], "columnas": cols, **resumen(probs, cols, 6.75)})
    todasA = [c for r in A for c in r["columnas"]]
    totA = resumen(probs, todasA, 20.25)
    # Opción B: Reducida 1 (la mejor sola) + sencillas optimizadas (R3), protección en el boleto 1
    Y = rm.muestras(probs, rm.N_OPT, semilla=7)
    tB = mejor_tres(probs, n=1)[0]
    r1 = expandir(base, tB)
    sen = rm.optimizadas(probs, a.sencillas, Y, ya=r1)
    sen = ordenar_proteccion(probs, r1, sen)
    totB = resumen(probs, r1 + sen, PRECIO * (9 + len(sen)))
    pleno = (d.get("pleno") or {}).get("marcador_mesa", "?")
    out = {"jornada": d["jornada"], "estado": d.get("estado"), "pleno": pleno, "base": base,
           "A": {"reducidas": A, "total": totA}, "B": {"reducida": r1, "triples": [i + 1 for i in sorted(tB)], "sencillas": sen, "total": totB},
           "falta": que_falta(d, probs, [("Opción A", todasA), ("Opción B", r1 + sen)])}
    if a.json:
        json.dump(out, open(a.json, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    if a.html:
        open(a.html, "w", encoding="utf-8").write(pagina(d, probs, out))
    print(json.dumps({"A": [(r["triples"], round(100 * r["p13"], 2)) for r in A], "totA": totA, "totB": totB, "falta": out["falta"]}, ensure_ascii=False, indent=1))


# ---------------------------------------------------------------- HTML
def pct(x):
    return f"{100 * x:.2f} %".replace(".", ",")


def uno_entre(x):
    return "1 entre " + format(round(1 / x), ",").replace(",", ".") if x > 0 else "—"


def tabla_reducida(d, probs, cols, triples, titulo, pleno, cifras, etiqueta="C"):
    e = html.escape
    h = [f'<section><h2>{e(titulo)}</h2><div class="cifras">{cifras}</div><div class="scroll"><table>']
    h.append('<thead><tr><th class="n">#</th><th class="p">Partido</th><th class="pc">Casas/mesa %</th><th class="def">Boleto</th>'
             + "".join(f'<th class="c">{etiqueta}{k + 1}</th>' for k in range(len(cols))) + "</tr></thead><tbody>")
    for i, x in enumerate(d["partidos"]):
        sig = "".join(s for s in S if any(c[i] == s for c in cols))
        cls = "tri" if len(sig) == 3 else ("dob" if len(sig) == 2 else "")
        pr = "/".join(f"{100 * v:.0f}" for v in probs[i])
        h.append(f'<tr><td class="n">{i + 1}</td><td class="p">{e(x["partido"])}</td><td class="pc">{pr}</td>'
                 f'<td class="def {cls}">{" ".join(sig)}</td>'
                 + "".join(f'<td class="c{" alt" if c[i] != S[int(np.argmax(probs[i]))] else ""}">{c[i]}</td>' for c in cols) + "</tr>")
    pl = (d.get("pleno") or {}).get("partido", "Pleno al 15")
    h.append(f'<tr class="pleno"><td class="n">15</td><td class="p">{e(pl)}</td><td class="pc"></td><td class="def">{e(pleno)}</td>'
             + "".join(f'<td class="c">{e(pleno)}</td>' for _ in cols) + "</tr>")
    ac = [acierto(probs, c) for c in cols]
    h.append(f'<tr class="acierto"><td class="n"></td><td class="p" colspan="2">Acierto esperado por la mesa (0-100 %)</td>'
             f'<td class="def">{np.mean(ac):.0f}</td>' + "".join(f'<td class="c">{v:.0f}</td>' for v in ac) + "</tr>")
    h.append("</tbody></table></div></section>")
    return "".join(h)


def cifras(r):
    return (f'<span><b>{r["apuestas"]}</b> apuestas</span><span><b>{format(r["coste"], ".2f").replace(".", ",")} €</b></span>'
            f'<span>P(14) <b>{uno_entre(r["p14"])}</b></span><span>P(≥13) <b>{pct(r["p13"])}</b></span>'
            f'<span>P(≥12) <b>{pct(r["p12"])}</b></span>')


def tabla_datos(d):
    e = html.escape
    filas = [(x.get("n", 15), x["partido"], x["datos"]) for x in d["partidos"] + [d.get("pleno") or {}] if x.get("datos")]
    if not filas:
        return ""
    h = ['<section><h2>Datos por partido</h2><div class="scroll"><table class="datos"><thead><tr><th class="n">#</th><th class="p">Partido</th>'
         '<th>Duelos (6 años, goles del local de hoy)</th><th>L-X-V</th><th>Temporada pasada</th><th>Entrenador nuevo</th><th>Carga (hasta 22/11) y Europa</th><th>Riesgo de rotación</th></tr></thead><tbody>']
    for n, pa, x in filas:
        h.append(f'<tr><td class="n">{n}</td><td class="p">{e(pa)}</td><td class="h2h">{e(x["h2h_6"])}</td><td>{e(x["balance_LXV"])}</td>'
                 f'<td>{e(x["temporada_pasada"])}</td><td>{e(x["entrenador_nuevo"])}</td>'
                 f'<td class="h2h">{e(x.get("carga", "—"))}</td><td class="h2h">{e(x.get("rotacion", "—"))}</td></tr>')
    h.append("</tbody></table></div></section>")
    m = d.get("medicion_factores")
    if m:
        nom = {"h2h_dif": "Balance de duelos", "h2h_x": "Empates en duelos", "ult_sig": "Temporada pasada", "hay_ult": None}
        h.append('<section><h2>¿Mejora a las cuotas? (Primera y Segunda, fuera de muestra 2016-26)</h2><div class="scroll"><table><thead><tr>'
                 '<th class="p">Dato</th><th>Partidos</th><th>Log-loss casas</th><th>Con el dato</th><th>Mejora</th><th>2016-20 / 2021-26</th><th>Entra</th></tr></thead><tbody>')
        for t in m["pruebas"]:
            nm = " + ".join(nom[c] for c in t["factores"] if nom[c]) if len(t["factores"]) < 4 else "Los tres juntos"
            ok = t["mejora"] > 0 and min(t["mejora_2016_20_y_2021_26"]) > 0
            h.append(f'<tr><td class="p">{e(nm)}</td><td>{t["n_prueba"]}</td><td>{t["ll_casas_recal"]:.4f}</td><td>{t["ll_con_factor"]:.4f}</td>'
                     f'<td class="{"bien" if ok else "mal"}">{t["mejora"]:+.4f}</td><td>{" / ".join(f"{v:+.4f}" for v in t["mejora_2016_20_y_2021_26"])}</td>'
                     f'<td class="{"bien" if ok else "mal"}">{"Sí" if ok else "No"}</td></tr>')
        for nm, res, fu in m.get("otros", []):
            h.append(f'<tr><td class="p">{e(nm)}</td><td colspan="5" class="h2h">{e(res)} · {e(fu)}</td><td class="{"bien" if res.startswith("Sí") else "mal"}">{"Sí" if res.startswith("Sí") else "No"}</td></tr>')
        h.append("</tbody></table></div></section>")
    return "".join(h)


def pagina(d, probs, o):
    e = html.escape
    tope = 18.0
    filas = [("A · 3 Reducidas 1", o["A"]["total"]), ("B · Reducida 1 + sencillas", o["B"]["total"])]
    comp = ['<section><h2>Comparativa</h2><div class="scroll"><table class="comp"><thead><tr><th>Opción</th><th>Apuestas</th>'
            '<th>Coste</th><th>Tope 18 €</th><th>P(14)</th><th>P(≥13)</th><th>P(≥12)</th><th>P(≥10)</th></tr></thead><tbody>']
    for n, r in filas:
        comp.append(f'<tr><td>{e(n)}</td><td>{r["apuestas"]}</td><td>{format(r["coste"], ".2f").replace(".", ",")} €</td>'
                    f'<td class="{"mal" if r["coste"] > tope else "bien"}">{"+" + format(r["coste"] - tope, ".2f").replace(".", ",") + " €" if r["coste"] > tope else "dentro"}</td>'
                    f'<td>{uno_entre(r["p14"])}</td><td>{pct(r["p13"])}</td><td>{pct(r["p12"])}</td><td>{pct(r["p10"])}</td></tr>')
    comp.append("</tbody></table></div></section>")
    falta = ['<section class="falta"><h2>Qué falta</h2><div class="scroll"><table><thead><tr><th>Tipo</th><th>Detalle</th></tr></thead><tbody>']
    for t, txt in o["falta"] or [("—", "Nada pendiente")]:
        falta.append(f'<tr><td class="tipo t-{e(t.split()[0].lower())}">{e(t)}</td><td>{e(txt)}</td></tr>')
    falta.append("</tbody></table></div></section>")
    secs = []
    for k, r in enumerate(o["A"]["reducidas"], 1):
        secs.append(tabla_reducida(d, probs, r["columnas"], r["triples"], f"A{k} · Reducida 1 oficial · triples en {', '.join(map(str, r['triples']))}",
                                   o["pleno"], cifras(r)))
    secs_b = [tabla_reducida(d, probs, o["B"]["reducida"], o["B"]["triples"],
                             f"B · Reducida 1 oficial · triples en {', '.join(map(str, o['B']['triples']))}", o["pleno"], cifras(resumen(probs, o["B"]["reducida"], 6.75)))]
    sen = o["B"]["sencillas"]
    for b in range(0, len(sen), 8):
        blk = sen[b:b + 8]
        secs_b.append(tabla_reducida(d, probs, blk, [], f"B · Boleto {b // 8 + 1} de sencillas (S{b + 1}–S{b + len(blk)})", o["pleno"],
                                     f'<span><b>{len(blk)}</b> apuestas</span><span><b>{format(PRECIO * len(blk), ".2f").replace(".", ",")} €</b></span>', etiqueta="S"))
    estado = "Provisional" if d.get("estado") != "definitivo" else "Definitivo"
    return f"""<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Pronósticos por reducida</title><style>
:root{{--bg:#f7f7f5;--fg:#1d1d1b;--mut:#6b6b66;--card:#fff;--line:#e3e2dc;--acc:#1f6f4a;--tri:#e8f3ec;--dob:#eef3fb;--alt:#b4561c;--mal:#b3261e;--malbg:#fbeceb;--warnbg:#fff6e0}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#151514;--fg:#ecebe6;--mut:#9b9a94;--card:#1e1e1c;--line:#33332f;--acc:#5fc28f;--tri:#1f3328;--dob:#1f2a3a;--alt:#f0a06a;--mal:#ff8a80;--malbg:#3a1f1d;--warnbg:#3a3020}}}}
:root[data-theme="dark"]{{--bg:#151514;--fg:#ecebe6;--mut:#9b9a94;--card:#1e1e1c;--line:#33332f;--acc:#5fc28f;--tri:#1f3328;--dob:#1f2a3a;--alt:#f0a06a;--mal:#ff8a80;--malbg:#3a1f1d;--warnbg:#3a3020}}
body{{margin:0;background:var(--bg);color:var(--fg);font:14px/1.4 system-ui,-apple-system,Segoe UI,sans-serif}}
main{{max-width:1180px;margin:0 auto;padding:16px}}
header h1{{font-size:20px;margin:0 0 4px}} header p{{margin:0;color:var(--mut)}}
h2{{font-size:15px;margin:0 0 8px}}
section{{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px;margin:14px 0}}
.falta{{border-color:var(--mal);background:var(--malbg)}}
.grupo{{font-size:13px;text-transform:uppercase;letter-spacing:.06em;color:var(--mut);margin:24px 0 0}}
.scroll{{overflow-x:auto}} table{{border-collapse:collapse;font-variant-numeric:tabular-nums;width:100%}}
th,td{{border-bottom:1px solid var(--line);padding:4px 6px;text-align:center;white-space:nowrap}}
th{{font-size:12px;color:var(--mut);font-weight:600}}
td.p,th.p{{text-align:left}} td.n{{color:var(--mut)}} td.pc{{color:var(--mut);font-size:12px}}
td.def{{font-weight:700;letter-spacing:.08em}} td.tri{{background:var(--tri)}} td.dob{{background:var(--dob)}}
td.c{{font-family:ui-monospace,Menlo,monospace}} td.alt{{color:var(--alt);font-weight:700}}
tr.pleno td{{border-top:2px solid var(--line)}} tr.acierto td{{color:var(--mut);font-size:12px}}
.cifras{{display:flex;flex-wrap:wrap;gap:6px 16px;margin:0 0 8px;color:var(--mut)}} .cifras b{{color:var(--fg)}}
.comp td:first-child{{text-align:left;font-weight:600}} td.mal{{color:var(--mal);font-weight:700}} td.bien{{color:var(--acc)}}
td.tipo{{text-align:left;font-weight:600}} td.h2h{{white-space:normal;min-width:260px;font-size:12px;text-align:left}} .falta td{{white-space:normal;text-align:left}}
</style></head><body><main>
<header><h1>Pronósticos por reducida · J{d['jornada']}</h1><p>{e(estado)} · {e(d.get('fechas', ''))} · Pleno {e((d.get('pleno') or {}).get('partido', ''))}</p></header>
{''.join(falta)}
{''.join(comp)}
{tabla_datos(d)}
<h3 class="grupo">Opción A · 3 Reducidas 1 oficiales</h3>
{cifras_total(o['A']['total'])}
{''.join(secs)}
<h3 class="grupo">Opción B · Reducida 1 + sencillas en boletos de 8</h3>
{cifras_total(o['B']['total'])}
{''.join(secs_b)}
</main></body></html>"""


def cifras_total(r):
    return f'<section><h2>Conjunto</h2><div class="cifras">{cifras(r)}<span>Columnas distintas <b>{r["distintas"]}</b></span></div></section>'


if __name__ == "__main__":
    main()
