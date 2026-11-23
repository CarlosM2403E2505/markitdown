"""Puntúa un estudio externo (p. ej. el de estilos de Carlos) frente a la mesa y el mercado.

Uso:  python3 herramientas/puntuar_externo.py jornadas/j25/j25.json jornadas/j25/estudio_estilos.json

Mide, solo en los partidos con resultado y con las tres fuentes, el Brier (menor = mejor)
y el log-loss. Regla de la mesa (23/11/2026): el estudio externo pesa 0 hasta que gane al
mercado en Brier en 3 jornadas medidas; entonces entra con un 10 % de peso en la mezcla.
"""
import json
import math
import sys

SIG = {"1": 0, "X": 1, "2": 2}


def norm(v):
    if v is None:
        return None
    v = [float(x) for x in v]
    s = sum(v)
    return [x / s for x in v] if s > 0 else None


def brier(p, k):
    return sum((p[i] - (1.0 if i == k else 0.0)) ** 2 for i in range(3))


def logloss(p, k):
    return -math.log(max(p[k], 1e-9))


def puntuar(jornada, externo):
    ext = {e["n"]: norm(e.get("estudio_1x2")) for e in externo["partidos"]}
    filas = []
    for p in jornada["partidos"]:
        k = SIG.get(str(p.get("resultado", "")).strip().upper())
        e, m, me = ext.get(p["n"]), norm(p.get("mercado")), norm(p.get("p"))
        if k is None or not (e and m and me):
            continue
        filas.append((p["n"], k, me, m, e))
    out = {"partidos": len(filas)}
    for nombre, i in (("mesa", 2), ("mercado", 3), ("estudio", 4)):
        out[nombre] = {
            "brier": round(sum(brier(f[i], f[1]) for f in filas) / len(filas), 4) if filas else None,
            "logloss": round(sum(logloss(f[i], f[1]) for f in filas) / len(filas), 4) if filas else None,
        }
    if filas:
        out["estudio_gana_al_mercado"] = out["estudio"]["brier"] < out["mercado"]["brier"]
    return out


if __name__ == "__main__":
    j = json.load(open(sys.argv[1], encoding="utf-8"))
    x = json.load(open(sys.argv[2], encoding="utf-8"))
    print(json.dumps(puntuar(j, x), ensure_ascii=False, indent=1))
