import os, json, math, importlib.util
os.environ["LF_EXTRA"] = "../ligaf_j9_j10.txt"
spec = importlib.util.spec_from_file_location("j21", "/home/claude/j21_run.py"); j21 = importlib.util.module_from_spec(spec); spec.loader.exec_module(j21)
import numpy as np
def adj(p, k):
    s = p[0] + p[2] + k * p[1]; return [p[0] / s, k * p[1] / s, p[2] / s]
def wilson(x, n, z=1.96):
    p = x / n; d = 1 + z * z / n; c = (p + z * z / (2 * n)) / d; h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return c - h, c + h
prev_avg = sum(g for g, _ in j21.j16.LF_PREV.values()) / (len(j21.j16.LF_PREV) * 30)
def prior(t):
    gf, ga = j21.j16.LF_PREV.get(t, j21.j16.PROMOTED); return math.log(gf / 30 / prev_avg), math.log(ga / 30 / prev_avg)
lines = [l.split("|") for l in j21.LF.splitlines() if l.count("|") == 4]
ALL = [(int(j), h, a, int(x), int(y)) for j, h, a, x, y in lines]
# quitar duplicados exactos (el LF base + extra podrían repetir)
seen = set(); A2 = []
for r in ALL:
    if r[:3] in seen: continue
    seen.add(r[:3]); A2.append(r)
ALL = A2
print("Liga F partidos 2026/27 cargados:", len(ALL), "| jornadas", sorted({r[0] for r in ALL}))
rows = []
for j in range(2, 11):
    j21.LF_M = [(h, a, x, y) for jj, h, a, x, y in ALL if jj < j and "Barcelona" not in (h, a)]
    lf = j21.ligaf_fit()
    for jj, h, a, x, y in ALL:
        if jj != j or "Barcelona" in (h, a): continue
        ah, dh = (lf["att"][h], lf["dfn"][h]) if h in lf["att"] else prior(h)
        aa, da = (lf["att"][a], lf["dfn"][a]) if a in lf["att"] else prior(a)
        lam = math.exp(lf["mu0"] + lf["home"] + ah + da); mu = math.exp(lf["mu0"] + aa + dh)
        p, _, _ = j21.j16.finish(lam, mu, None, 1.0)
        rows.append({"j": j, "h": h, "a": a, "res": 0 if x > y else 1 if x == y else 2, "p": p, "lm": [lam, mu]})
n = len(rows); xr = sum(r["res"] == 1 for r in rows)
def LL(k): return np.mean([-math.log(adj(r["p"], k)[r["res"]]) for r in rows])
ks = np.arange(0.5, 1.51, 0.01); bk = ks[int(np.argmin([LL(k) for k in ks]))]
pr0 = np.mean([r["p"][1] for r in rows]); pr85 = np.mean([adj(r["p"], 0.85)[1] for r in rows])
lo, hi = wilson(xr, n)
bal = lambda p: abs(p[0] - p[2])
ig = [r for r in rows if bal(adj(r["p"], .85)) < .15]
xi = sum(r["res"] == 1 for r in ig)
out = dict(n=n, x=xr, real=xr / n, ci=[lo, hi], pred_raw=pr0, pred_085=pr85, k=float(bk), ll1=LL(1.0), ll085=LL(0.85),
           ig_n=len(ig), ig_x=xi, ig_pred085=float(np.mean([adj(r["p"], .85)[1] for r in ig])) if ig else None, ig_ci=wilson(xi, len(ig)) if ig else None)
print(json.dumps(out, indent=1))
# bootstrap del k
rng = np.random.default_rng(3); B = []
arr = np.array([[r["p"][0], r["p"][1], r["p"][2], r["res"]] for r in rows])
for _ in range(500):
    s = arr[rng.integers(0, n, n)]
    vals = []
    for k in ks:
        den = s[:, 0] + s[:, 2] + k * s[:, 1]; pr = np.where(s[:, 3] == 0, s[:, 0], np.where(s[:, 3] == 1, k * s[:, 1], s[:, 2])) / den
        vals.append(-np.log(pr).mean())
    B.append(ks[int(np.argmin(vals))])
out["kci90"] = list(np.percentile(B, [5, 95]))
print("k IC90:", out["kci90"])
json.dump(out, open("draws_ligaf.json", "w"), indent=1)
json.dump(rows, open("ligaf_oos.json", "w"))
