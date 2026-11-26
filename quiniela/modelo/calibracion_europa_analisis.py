import json, math, sys, statistics as st
f = json.load(open(sys.argv[1]))
def resumen(sel, nombre):
    if len(sel) < 15: print(f"  {nombre:<44} n={len(sel):4d} (muestra demasiado pequeña)"); return None
    dp = [x["pts"] - x["pts_esp"] for x in sel]
    rf = [x["gf"] / x["xf"] for x in sel if x["xf"] > 0]
    sf = sum(x["gf"] for x in sel) / sum(x["xf"] for x in sel); sc = sum(x["gc"] for x in sel) / sum(x["xc"] for x in sel)
    m = st.mean(dp); se = st.pstdev(dp) / math.sqrt(len(dp))
    print(f"  {nombre:<44} n={len(sel):4d}  puntos real−esperado {m:+.3f} (±{1.96*se:.3f})  goles a favor ×{sf:.3f}  goles en contra ×{sc:.3f}")
    return m, se, sf, sc
for liga, filtro in (("TODAS LAS LIGAS", lambda x: True), ("PRIMERA (es.1)", lambda x: x["liga"] == "es.1")):
    print(f"\n=== {liga} ===")
    base = [x for x in f if filtro(x)]
    ctrl = [x for x in base if x["dias"] is None]
    r0 = resumen(ctrl, "Sin Europa en los 7 días previos (control)")
    grupos = {
        "Tras Europa (cualquier día, 2–6 días antes)": lambda x: x["dias"] is not None and 2 <= x["dias"] <= 6,
        "Tras Champions (martes/miércoles)": lambda x: x["comp"] == "uefa.cl" and x["dia_sem"] in (1, 2),
        "Tras Europa el martes/miércoles (todas)": lambda x: x["dia_sem"] in (1, 2),
        "Tras Europa el jueves": lambda x: x["dia_sem"] == 3,
        "  jueves → 2 días (sábado)": lambda x: x["dia_sem"] == 3 and x["dias"] == 2,
        "  jueves → 3 días (domingo)": lambda x: x["dia_sem"] == 3 and x["dias"] == 3,
        "  jueves → 4 días (lunes)": lambda x: x["dia_sem"] == 3 and x["dias"] == 4,
        "Tras Europa, jugando en casa": lambda x: x["dias"] is not None and x["lado"] == "local",
        "Tras Europa, jugando fuera": lambda x: x["dias"] is not None and x["lado"] == "visitante",
        "Tras Europa, siendo favorito (≥50 %)": lambda x: x["dias"] is not None and x["fav"],
    }
    for n, g in grupos.items():
        r = resumen([x for x in base if g(x)], n)
        if r and r0:
            d = r[0] - r0[0]; se = math.sqrt(r[1] ** 2 + r0[1] ** 2)
            print(f"      → frente al control: {d:+.3f} puntos/partido (±{1.96*se:.3f}); ataque {100*(r[2]/r0[2]-1):+.1f} %; goles en contra {100*(r[3]/r0[3]-1):+.1f} %")
