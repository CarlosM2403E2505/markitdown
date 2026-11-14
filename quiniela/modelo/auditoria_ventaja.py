"""Auditoría de la ventaja del método (edge audit, estilo casa de apuestas).

Walk-forward sobre datos/euro_j21.json: cada mes de Primera y Segunda desde 2022 se reajusta el
modelo con lo anterior y se predice el mes siguiente (nunca ve el futuro). Mide, fuera de muestra:
  1. Log-loss y acierto del signo del modelo frente a dos baselines: "siempre 1" y "mejor clasificado".
  2. Calibración: probabilidad del favorito dada frente a la real, por tramos.
  3. Distribución de aciertos de un boleto: tomando el signo más probable del modelo en bloques de 14
     partidos, cuántas veces se aciertan 10/11/12/13/14, frente a lo que el modelo predice.
El modelo se aplica como en producción: T=1,05; empates Primera ×1,08 con campo ±0,07; Segunda ×1,00.
Uso: python3 modelo/auditoria_ventaja.py   (desde la carpeta quiniela)
"""
import importlib.util, json, math, os, sys
from collections import defaultdict
from datetime import date
import numpy as np
from scipy.stats import poisson

R = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("em", os.path.join(R, "euro_model.py"))
em = importlib.util.module_from_spec(spec); spec.loader.exec_module(em)
sys.path.insert(0, os.path.join(R, "..", "herramientas"))
import quiniela_calc as qc
MS = json.load(open(os.path.join(R, "..", "datos", "euro_j21.json")))["matches"]
G = np.arange(11)
DRAW = {"es.1": 1.08, "es.2": 1.00}
HOME = {"es.1": 0.07, "es.2": 0.0}


def probs(l, u, comp, T=1.05):
    if HOME[comp]:
        l, u = l * math.exp(HOME[comp]), u * math.exp(-HOME[comp])
    M = np.outer(poisson.pmf(G, l), poisson.pmf(G, u)); M[np.diag_indices_from(M)] *= DRAW[comp]; M /= M.sum()
    i, j = np.indices(M.shape); p = np.array([M[i > j].sum(), M[i == j].sum(), M[i < j].sum()])
    p = p ** T; return p / p.sum()


def meses(desde, hasta):
    out = []; y, m = desde
    while (y, m) <= hasta:
        out.append(f"{y}-{m:02d}-01"); y, m = (y + 1, 1) if m == 12 else (y, m + 1)
    return out


def tabla_hasta(comp_season, antes):
    """Puntos por equipo dentro de una temporada, con los partidos anteriores a la fecha."""
    pts = defaultdict(int)
    for x in antes:
        if x["competition"] != comp_season:
            continue
        if x["hg"] > x["ag"]:
            pts[x["home"]] += 3
        elif x["hg"] == x["ag"]:
            pts[x["home"]] += 1; pts[x["away"]] += 1
        else:
            pts[x["away"]] += 3
    return pts


def construir():
    filas = []
    for a, b in zip(meses((2022, 1), (2026, 12)), meses((2022, 2), (2027, 1))):
        te = [x for x in MS if a <= x["date"] < b and x["competition"].split(":")[0] in DRAW]
        if not te:
            continue
        antes = [x for x in MS if x["date"] < a]
        mod = em.EuroPoisson(xi=0.0015, ridge=10, scale=1.05, blend=0.2, hier=True).fit(antes, ref_date=date.fromisoformat(a))
        for x in te:
            if x["home"] not in mod.idx or x["away"] not in mod.idx:
                continue
            comp = x["competition"].split(":")[0]
            l, u = mod.rates(x["home"], x["away"])
            p = probs(l, u, comp)
            r = 0 if x["hg"] > x["ag"] else (1 if x["hg"] == x["ag"] else 2)
            pts = tabla_hasta(x["competition"], antes)
            # "mejor clasificado": 0 si gana el local, 2 el visitante; empate -> favorito local por el campo
            dh, da = pts.get(x["home"], 0), pts.get(x["away"], 0)
            mejor = 0 if dh >= da else 2
            filas.append({"p": [round(v, 5) for v in p], "r": r, "comp": comp, "date": x["date"], "mejor": mejor})
        print(a, len(filas), file=sys.stderr)
    json.dump(filas, open(os.path.join(R, "..", "datos", "auditoria_ventaja.json"), "w"))
    return filas


def logloss(filas, prob_fn):
    return float(np.mean([-math.log(max(prob_fn(f)[f["r"]], 1e-12)) for f in filas]))


def acierto(filas, sign_fn):
    return float(np.mean([sign_fn(f) == f["r"] for f in filas]))


def dist_boleto(filas):
    """Bloques de 14 partidos en orden: aciertos reales del signo más probable vs esperado por el modelo."""
    bloques = [filas[i:i + 14] for i in range(0, len(filas) - 13, 14)]
    obs = np.zeros(15); esp = np.zeros(15)
    for bl in bloques:
        signos = [int(np.argmax(f["p"])) for f in bl]
        aciertos = sum(s == f["r"] for s, f in zip(signos, bl))
        obs[aciertos] += 1
        d = qc._poisson_binomial([f["p"][s] for s, f in zip(signos, bl)])
        esp += np.array(d)
    return len(bloques), obs, esp


def main():
    filas = construir()
    base_uno = lambda f: [1.0, 0.0, 0.0]  # "siempre 1"
    base_mejor = lambda f: [1.0 if f["mejor"] == 0 else 0.0, 0.0, 1.0 if f["mejor"] == 2 else 0.0]
    out = {"n": len(filas), "desde": filas[0]["date"], "hasta": filas[-1]["date"]}
    # Referencia justa de log-loss: la "climatología", es decir la frecuencia media de 1/X/2 en la muestra.
    base = np.bincount([f["r"] for f in filas], minlength=3) / len(filas)
    out["frecuencia_1X2"] = [round(float(v), 3) for v in base]
    out["log_loss"] = {
        "modelo": round(logloss(filas, lambda f: f["p"]), 4),
        "tasa_base (climatología)": round(logloss(filas, lambda f: base), 4),
    }
    out["acierto_signo"] = {
        "modelo": round(acierto(filas, lambda f: int(np.argmax(f["p"]))), 4),
        "siempre_1": round(acierto(filas, lambda f: 0), 4),
        "mejor_clasificado": round(acierto(filas, lambda f: f["mejor"]), 4),
    }
    # calibración del favorito
    cal = []
    pf = np.array([max(f["p"]) for f in filas]); fav = np.array([int(np.argmax(f["p"])) for f in filas])
    ok = np.array([fav[i] == filas[i]["r"] for i in range(len(filas))])
    for lo, hi in ((0.33, 0.42), (0.42, 0.50), (0.50, 0.58), (0.58, 0.66), (0.66, 1.01)):
        msk = (pf >= lo) & (pf < hi)
        if msk.sum():
            cal.append({"tramo": f"{lo:.2f}-{hi:.2f}", "n": int(msk.sum()),
                        "dada": round(100 * pf[msk].mean(), 1), "real": round(100 * ok[msk].mean(), 1)})
    out["calibracion_favorito"] = cal
    nb, obs, esp = dist_boleto(filas)
    out["boleto"] = {"bloques_de_14": nb,
                     "aciertos": [{"k": k, "observado": int(obs[k]), "esperado": round(esp[k], 1)} for k in range(8, 15)]}
    json.dump(out, open(os.path.join(R, "..", "datos", "auditoria_ventaja_resumen.json"), "w"), ensure_ascii=False, indent=1)
    print(json.dumps(out, ensure_ascii=False, indent=1))
    return out


if __name__ == "__main__":
    main()
