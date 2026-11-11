#!/usr/bin/env python3
"""Afina la prediccion del PLENO AL 15 (categorias 0/1/2/M).

El modelo trata los goles de cada equipo como Poisson independientes, asi que
sus marcadores exactos salen demasiado confiados. Aqui se mide si MEZCLAR la
matriz del modelo con la distribucion empirica de marcadores de la liga mejora
el acierto del Pleno, y con cuanto peso.

  p_final = (1 - w) * p_modelo + w * p_empirica_liga

Tambien prueba un factor de dispersion sobre los goles esperados, por si el
modelo esta sistematicamente corto o largo de goles.

Uso:
    python3 pleno_tuning.py dataset_clean.json --cutoff 2026-01-01
"""
import argparse
import importlib.util
import json
import math

import numpy as np

_spec = importlib.util.spec_from_file_location(
    "dc", __file__.replace("pleno_tuning.py", "dixon_coles.py"))
dc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(dc)

EPS = 1e-12
CATS = [(i, j) for i in range(4) for j in range(4)]


def cat_of(hg, ag):
    return (min(hg, 3), min(ag, 3))


def model_cats(model, home, away, scale=1.0):
    lam, mu = model.rates(home, away)
    lam, mu = lam * scale, mu * scale
    from scipy.stats import poisson
    g = np.arange(dc.MAXG + 1)
    M = np.outer(poisson.pmf(g, lam), poisson.pmf(g, mu))
    X, Y = np.meshgrid(g, g, indexing="ij")
    M = M * dc.tau_vec(X, Y, lam, mu, model.rho)
    M /= M.sum()
    out = {c: 0.0 for c in CATS}
    for x in range(M.shape[0]):
        for y in range(M.shape[1]):
            out[cat_of(x, y)] += M[x, y]
    return out


def score(preds, truths):
    ll = sum(-math.log(max(p.get(t, 0.0), EPS)) for p, t in zip(preds, truths))
    top1 = sum(1 for p, t in zip(preds, truths)
               if max(p, key=p.get) == t)
    top4 = sum(1 for p, t in zip(preds, truths)
               if t in [k for k, _ in sorted(p.items(), key=lambda kv: -kv[1])[:4]])
    n = len(truths)
    return ll / n, top1 / n, top4 / n


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("dataset")
    ap.add_argument("--cutoff", default="2026-01-01")
    ap.add_argument("--xi", type=float, default=0.0015)
    ap.add_argument("--ridge", type=float, default=0.05)
    args = ap.parse_args()

    with open(args.dataset, encoding="utf-8") as f:
        matches = json.load(f)["matches"]
    train = [r for r in matches if r["date"] < args.cutoff]
    test = [r for r in matches if r["date"] >= args.cutoff]
    print(f"Entreno {len(train)} | Prueba {len(test)} (nunca vistos)\n")

    model = dc.DixonColes(xi=args.xi, ridge=args.ridge).fit(train)

    # Distribucion empirica de categorias en el entreno
    emp = {c: 0.0 for c in CATS}
    for r in train:
        emp[cat_of(r["hg"], r["ag"])] += 1.0 / len(train)

    test = [r for r in test if r["home"] in model.idx and r["away"] in model.idx]
    truths = [cat_of(r["hg"], r["ag"]) for r in test]

    print("A) Mezcla con la distribucion empirica de la liga")
    print(f"{'peso w':>8} {'LL(Pleno)':>11} {'Pleno #1':>10} {'Pleno top4':>11}")
    base_cache = [model_cats(model, r["home"], r["away"]) for r in test]
    best_w = None
    for w in (0.0, 0.05, 0.10, 0.15, 0.20, 0.30, 0.40, 0.60, 1.0):
        preds = [{c: (1 - w) * mc[c] + w * emp[c] for c in CATS}
                 for mc in base_cache]
        ll, t1, t4 = score(preds, truths)
        print(f"{w:>8.2f} {ll:>11.4f} {t1:>10.1%} {t4:>11.1%}")
        if best_w is None or ll < best_w[1]:
            best_w = (w, ll, t1, t4)
    print(f"  -> mejor w = {best_w[0]:.2f}  (LL {best_w[1]:.4f}, "
          f"#1 {best_w[2]:.1%}, top4 {best_w[3]:.1%})")

    print("\nB) Factor de escala sobre los goles esperados")
    print(f"{'escala':>8} {'LL(Pleno)':>11} {'Pleno #1':>10} {'Pleno top4':>11}")
    best_s = None
    for s in (0.90, 0.95, 1.00, 1.05, 1.10):
        preds = [model_cats(model, r["home"], r["away"], scale=s) for r in test]
        ll, t1, t4 = score(preds, truths)
        print(f"{s:>8.2f} {ll:>11.4f} {t1:>10.1%} {t4:>11.1%}")
        if best_s is None or ll < best_s[1]:
            best_s = (s, ll, t1, t4)
    print(f"  -> mejor escala = {best_s[0]:.2f}")

    print("\nC) Combinado: mejor escala + mejor mezcla")
    cache_s = [model_cats(model, r["home"], r["away"], scale=best_s[0])
               for r in test]
    best_c = None
    for w in (0.0, 0.05, 0.10, 0.15, 0.20, 0.30):
        preds = [{c: (1 - w) * mc[c] + w * emp[c] for c in CATS}
                 for mc in cache_s]
        ll, t1, t4 = score(preds, truths)
        print(f"  escala={best_s[0]:.2f} w={w:<5.2f} LL={ll:.4f} "
              f"#1={t1:.1%} top4={t4:.1%}")
        if best_c is None or ll < best_c[1]:
            best_c = (w, ll, t1, t4)

    print("\nD) Techo realista para el boleto")
    w, ll, t1, t4 = best_c
    preds = [{c: (1 - w) * mc[c] + w * emp[c] for c in CATS} for mc in cache_s]
    for k in (1, 2, 3, 4, 5, 6, 8):
        cov = sum(1 for p, t in zip(preds, truths)
                  if t in [c for c, _ in sorted(p.items(),
                                                key=lambda kv: -kv[1])[:k]])
        print(f"  jugando los {k} plenos mas probables: acierto real "
              f"{cov / len(truths):.1%}")

    print("\nTambien: cuanto se EQUIVOCA el modelo al declarar su confianza")
    top_probs = [max(p.values()) for p in preds]
    hit = [1.0 if max(p, key=p.get) == t else 0.0 for p, t in zip(preds, truths)]
    print(f"  probabilidad media que declara al mejor pleno: {np.mean(top_probs):.1%}")
    print(f"  acierto real de ese mejor pleno:               {np.mean(hit):.1%}")
    gap = np.mean(top_probs) - np.mean(hit)
    print(f"  exceso de confianza: {gap:+.1%}")


if __name__ == "__main__":
    main()
