#!/usr/bin/env python3
"""Sencillas con fijos protegidos (regla nueva tras la J23, 22/11/2026).

Problema de la J23: el boleto de 18 € y casi todas las sencillas llevaban los mismos fijos. Rayo (54 %)
y Tenerife–Mallorca (50 %) iban a un solo signo en 32 y 33 de las 36 columnas: un fallo las tumbó todas.

Regla: un partido que el boleto lleva a un solo signo con P < UMBRAL (55 %) es un «fijo débil».
Las sencillas tienen que cubrirlo:
  · el segundo signo más probable en al menos Q1 sencillas (2 si hay 6 o más sencillas, si no 1);
  · el tercero en al menos 1 sencilla si su P ≥ 20 %.
Con --mercado D también cuenta como débil un fijo en el que la mesa supera a las casas en más de D
(la cuota no cambia ninguna probabilidad; solo obliga a cubrir el partido).
Se cumplen las cuotas con las columnas más probables que las satisfacen (premiando las que cubren
varias a la vez) y el resto se rellena con las columnas más probables que no están en el boleto.
El Pleno va al marcador más probable en todas: con columnas distintas, cambiar el Pleno de una columna
solo baja su P(14+Pleno) (ver analisis/revision-j23.md).

Uso: python3 herramientas/proteccion.py jornadas/j24/j24.json 8 [--umbral 0.55] [--mercado 0.08]
     [--resultados "2:2,8:X"]  (escrutinio parcial: cuántas columnas siguen vivas)
"""
import argparse, itertools, json, math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import quiniela_calc as qc
S = "1X2"

def columnas_boleto(signos):
    return ["".join(c) for c in itertools.product(*[signos[str(i)].split() for i in range(1, 15)])]

def p_col(probs, c):
    return math.prod(probs[i][S.index(c[i])] for i in range(14))

def fijos_debiles(d, signos, umbral, mercado=None):
    out = []
    for i, x in enumerate(d["partidos"]):
        s = signos[str(i + 1)].split()
        if len(s) != 1: continue
        p = x["p"]; k = S.index(s[0]); motivo = None
        if p[k] < umbral: motivo = f"P {100*p[k]:.0f} % < {100*umbral:.0f} %"
        elif mercado is not None and x.get("mercado") and p[k] - x["mercado"][k] > mercado:
            motivo = f"mesa {100*p[k]:.0f} % vs casas {100*x['mercado'][k]:.0f} %"
        if motivo:
            alt = sorted([j for j in range(3) if j != k], key=lambda j: -p[j])
            out.append({"i": i, "fijo": S[k], "alt": [S[j] for j in alt], "p": p, "motivo": motivo})
    return out

def proteger(d, signos, n, umbral=0.55, mercado=None, pool=6000):
    probs = [x["p"] for x in d["partidos"]]
    bol = set(columnas_boleto(signos))
    orden = [qc._orden(p) for p in probs]
    cand = ["".join(S[orden[i][r]] for i, r in enumerate(rg)) for _, rg in qc._k_mejores(probs, orden, pool)]
    cand = [c for c in cand if c not in bol]
    deb = fijos_debiles(d, signos, umbral, mercado)
    cuotas = {}
    for f in deb:
        cuotas[(f["i"], f["alt"][0])] = 2 if n >= 6 else 1
        if f["p"][S.index(f["alt"][1])] >= 0.20: cuotas[(f["i"], f["alt"][1])] = 1
    elegidas = []
    while len(elegidas) < n and any(v > 0 for v in cuotas.values()):
        def score(c):
            sat = sum(1 for (i, s), v in cuotas.items() if v > 0 and c[i] == s)
            return (sat > 0, p_col(probs, c) * 4 ** sat)
        mejor = max((c for c in cand if c not in elegidas), key=score)
        if not score(mejor)[0]: break
        elegidas.append(mejor)
        for (i, s) in cuotas:
            if mejor[i] == s: cuotas[(i, s)] -= 1
    for c in cand:
        if len(elegidas) >= n: break
        if c not in elegidas: elegidas.append(c)
    return elegidas, deb, {k: v for k, v in cuotas.items() if v > 0}

def resumen(probs, cols):
    dist = qc.simular_columnas(probs, cols, n=150000)
    return {"p14": sum(p_col(probs, c) for c in cols), "p13": qc.al_menos(dist, 13), "p12": qc.al_menos(dist, 12)}

def vivas(cols, res):
    """Columnas con 0 y 1 fallos en los partidos ya jugados. res = {n: signo}."""
    f = [sum(c[i - 1] != s for i, s in res.items()) for c in cols]
    return f.count(0), f.count(1)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("jornada"); ap.add_argument("n", type=int)
    ap.add_argument("--umbral", type=float, default=0.55); ap.add_argument("--mercado", type=float)
    ap.add_argument("--signos", help="clave del boleto en el JSON (por defecto boleto_provisional)", default="boleto_provisional")
    ap.add_argument("--comparar", help="clave del JSON con las sencillas actuales (lista)", default="columnas_individuales")
    ap.add_argument("--resultados", help='"2:2,8:X"')
    ap.add_argument("--guardar", action="store_true", help="escribe columnas_protegidas en el JSON")
    a = ap.parse_args()
    d = json.load(open(a.jornada, encoding="utf-8"))
    signos = d[a.signos]["signos"]; probs = [x["p"] for x in d["partidos"]]
    nuevas, deb, pend = proteger(d, signos, a.n, a.umbral, a.mercado)
    bol = columnas_boleto(signos)
    print(f"Jornada {d['jornada']} · boleto {len(bol)} columnas + {a.n} sencillas protegidas (umbral {100*a.umbral:.0f} %)\n")
    print("Fijos débiles:")
    for f in deb:
        x = d["partidos"][f["i"]]
        print(f"  {f['i']+1:>2} {x['partido']:28s} fijo {f['fijo']} ({f['motivo']}) → se cubre {f['alt'][0]}" + (f" y {f['alt'][1]}" if f['p'][S.index(f['alt'][1])] >= 0.20 else ""))
    if pend: print("  ⚠ cuotas sin cumplir:", pend)
    print("\nSencillas nuevas:")
    for k, c in enumerate(nuevas, 1):
        print(f"  P{k} {c}  P(14) 1 entre {round(1/p_col(probs, c)):,}".replace(",", "."))
    tot = bol + nuevas
    print("\nCobertura por partido (columnas con cada signo, de", len(tot), "):")
    for i, x in enumerate(d["partidos"]):
        cnt = {s: sum(c[i] == s for c in tot) for s in S}
        print(f"  {i+1:>2} {x['partido']:28s} 1:{cnt['1']:>3}  X:{cnt['X']:>3}  2:{cnt['2']:>3}   mesa {'/'.join(f'{100*v:.0f}' for v in x['p'])}")
    rn = resumen(probs, tot)
    print(f"\nConjunto nuevo: P(14) 1 entre {round(1/rn['p14']):,} · P(≥13) {100*rn['p13']:.2f} % · P(≥12) {100*rn['p12']:.1f} %".replace(",", "."))
    viejas = d.get(a.comparar)
    if isinstance(viejas, dict): viejas = viejas.get("sencillas")
    if viejas:
        tv = bol + list(viejas)
        rv = resumen(probs, tv)
        print(f"Conjunto anterior ({len(tv)} col.): P(14) 1 entre {round(1/rv['p14']):,} · P(≥13) {100*rv['p13']:.2f} % · P(≥12) {100*rv['p12']:.1f} %".replace(",", "."))
    if a.resultados:
        res = {int(k): v for k, v in (t.split(":") for t in a.resultados.split(","))}
        print(f"\nCon los resultados {res}: nuevo {vivas(tot, res)[0]} sin fallo / {vivas(tot, res)[1]} con 1 fallo de {len(tot)}", end="")
        if viejas: print(f" · anterior {vivas(tv, res)[0]} / {vivas(tv, res)[1]} de {len(tv)}")
        else: print()
    if a.guardar:
        d["columnas_protegidas"] = {"regla": f"fijos < {100*a.umbral:.0f} % cubiertos (proteccion.py)", "sencillas": nuevas,
                                    "fijos_debiles": [d["partidos"][f["i"]]["partido"] for f in deb], **{k: round(v, 6) for k, v in rn.items()}}
        json.dump(d, open(a.jornada, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("Guardado en", a.jornada, "→ columnas_protegidas")

if __name__ == "__main__":
    main()
