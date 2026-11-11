"""J21 v1.7: precio del partido 10 (Bélgica–Italia) y del Pleno (España–Inglaterra) con el Poisson de selecciones.
Validado en modelo/validacion_selecciones.py (log-loss en prueba 0,795 frente a 0,810 del Elo; empates ×1,00)
y modelo/validacion_pleno_selecciones.py (sin mezcla empírica). Bajas de clase B como en la v1.3:
España sin Rodri ni Olmo (ataque ×0,97) e Inglaterra sin Guéhi (goles de España ×1,02).
Escribe los precios en jornadas/j21/j21.json."""
import importlib.util, json, os
from datetime import date
import numpy as np
R = os.path.dirname(os.path.abspath(__file__))
s = importlib.util.spec_from_file_location("sm", os.path.join(R, "selecciones_modelo.py")); sm = importlib.util.module_from_spec(s); s.loader.exec_module(sm)
ms = sm.cargar("2006-01-01")
mod = sm.NatPoisson().fit(ms, date(2026, 11, 14))
ruta = os.path.join(R, "..", "jornadas", "j21", "j21.json"); d = json.load(open(ruta, encoding="utf-8"))
def precio(h, a, fl=1.0, fv=1.0):
    lam, mu = mod.rates(sm.NOMBRES[h], sm.NOMBRES[a], neutral=False); lam, mu = lam * fl, mu * fv
    return lam, mu, sm.uno_x_dos(sm.matriz(lam, mu))
fuente = "Poisson de selecciones (modelo/selecciones_modelo.py, datos martj42 hasta el 6/10/2026; validado: log-loss 0,795 frente a 0,810 del Elo)"
for x in d["partidos"]:
    if x["partido"] == "Bélgica – Italia":
        lam, mu, p = precio("Bélgica", "Italia")
        x.update(p=[round(v, 4) for v in p], xg=[round(lam, 3), round(mu, 3)], precio=fuente)
        print("10 Bélgica – Italia", [round(100 * v, 1) for v in p], round(lam, 2), round(mu, 2))
lam, mu, p = precio("España", "Inglaterra", fl=0.97 * 1.02)
d["pleno"].update(p=[round(v, 4) for v in p], lambda_local=round(lam, 3), lambda_visitante=round(mu, 3), mezcla=0.0, factor_x=1.0,
                  precio=fuente + "; Pleno sin mezcla empírica (validado)",
                  ajuste="España sin Rodri ni Olmo (×0,97) e Inglaterra sin Guéhi (×1,02 a los goles de España), clase B.")
print("15 España – Inglaterra", [round(100 * v, 1) for v in p], round(lam, 2), round(mu, 2))
d["estado"] = "Pronóstico v1.7 (selecciones con el modelo validado)"
json.dump(d, open(ruta, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
