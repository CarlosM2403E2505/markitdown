"""Prueba con resultados reales de los formatos de boleto (22/11/2026, petición de Carlos: «¿sirven mis
apuestas de 12 y 18 €?»). Bloques de 14 partidos reales seguidos de Primera y Segunda (jul. 2024 - nov. 2026),
con las probabilidades de la mesa fuera de muestra (walk-forward mensual, las de modelo/x_templados.py,
incluida la X templada en Primera). Cada formato se construye con esas probabilidades y se cuenta la mejor
columna contra los resultados reales.
Uso: TMPDIR=<carpeta con x_templados_filas.pkl> python3 modelo/backtest_formatos.py → datos/backtest_formatos.json"""
import json, os, sys, contextlib, io
import numpy as np
R = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(R, "..", "herramientas"))
src = open(os.path.join(R, "x_templados.py"), encoding="utf-8").read().split("P = [(f, base(f))")[0]
ns = {"__file__": os.path.join(R, "x_templados.py")}
with contextlib.redirect_stderr(io.StringIO()): exec(src, ns)
filas, base, con_x = ns["filas"], ns["base"], ns["con_x"]
import reglas_mesa as rm, boletos_oficiales as bo, quiniela_calc as qc
rm.N_OPT, rm.N_EXTRA, rm.N_CANDIDATAS, rm.N_MUESTRAS = 3000, 800, 600, 6000
bo.CODIGOS = {"R1": bo.ternario42(), "R2": bo.hamming74(), "R3": bo.codigo_cubridor(3, 3)}
filas = sorted([f for f in filas if f[4] >= "2024-07-01"], key=lambda f: f[4])
def prob(f):
    p = base(f)
    if f[0] == "es.1": p = con_x(p, 0.45, 0.60, 1.20)
    return [float(v) for v in p]
bloques = [filas[k:k + 14] for k in range(0, len(filas) - 13, 14)]
def sin_r3(probs, n, Y):
    viejo = rm.TOPES; rm.TOPES = [(1.01, 1.0)]
    try: return rm.optimizadas(probs, n, Y)
    finally: rm.TOPES = viejo
FORM = {
    "18 € directa 3 dobles + 1 triple (formato de Carlos)": lambda p, Y: bo.candidatos(p, 3, 1, None, set())[3],
    "12 € directa 4 dobles": lambda p, Y: bo.candidatos(p, 4, 0, None, set())[3],
    "12 € reducida 7 dobles": lambda p, Y: bo.candidatos(p, 7, 0, "R2", set())[3],
    "18 € 24 sencillas más probables": lambda p, Y: qc.columnas_mas_probables(p, 24),
    "18 € 24 sencillas optimizadas SIN tope R3": lambda p, Y: sin_r3(p, 24, Y),
    "18 € 24 sencillas optimizadas CON tope R3 (reglas_mesa)": lambda p, Y: rm.optimizadas(p, 24, Y),
}
res = {k: [] for k in FORM}; esp = {k: [] for k in FORM}
for b, bl in enumerate(bloques):
    probs = [prob(f) for f in bl]; real = np.array([f[3] for f in bl])
    Y = rm.muestras(probs, rm.N_OPT, semilla=7); Ye = rm.muestras(probs, rm.N_MUESTRAS)
    for k, fn in FORM.items():
        cols = fn(probs, Y)
        C = rm.a_idx(cols)
        res[k].append(int((C == real).sum(axis=1).max()))
        esp[k].append(rm.evaluar(probs, cols, Ye)["p13"])
    print(b + 1, len(bloques), {k[:12]: res[k][-1] for k in FORM}, file=sys.stderr, flush=True)
out = {"bloques": len(bloques), "desde": filas[0][4], "hasta": filas[-1][4], "formatos": {}}
for k in FORM:
    r = np.array(res[k])
    out["formatos"][k] = {"media_aciertos": round(float(r.mean()), 2), **{f">={t}": int((r >= t).sum()) for t in (10, 11, 12, 13, 14)},
                          "p13_esperada_por_la_mesa": round(float(np.mean(esp[k])), 4)}
json.dump(out, open(os.path.join(R, "..", "datos", "backtest_formatos.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps(out, ensure_ascii=False, indent=1))
