"""Afinado (temperatura T) del 1X2 por competición. Validado el 17/11/2026 en
`analisis/afinado-favoritos.md` (walk-forward 2022-26):
  - Primera: T=1,15 (mejora log-loss fuera de muestra 0,9621 -> 0,9600; los favoritos claros
    estaban cortos: daban 68 %, ganaban 74 %).
  - Segunda y el resto: T=1,05 (afilar NO mejora; en Segunda los favoritos no rinden de más).
  - Liga F: T=0,70 (20/11/2026, `analisis/ligaf-favoritos.md`): los favoritos claros estaban largos
    (daban 79 %, ganaban 54 %); aplanar mejora el log-loss en las dos mitades de la temporada.
  - X templada en Primera (22/11/2026, tras la J23, `analisis/revision-j23.md`, `modelo/x_templados.py`):
    con el favorito entre 45 y 60 % la mesa daba X 25 % y salía 31-35 %. X x1,20 en ese tramo
    (después de T) mejora el log-loss en las tres temporadas (0,9887->0,9831; 0,9673->0,9626;
    0,9195->0,9193). En Segunda no mejora (no se aplica).
  - X con favorito claro en Primera (22/11/2026, `analisis/cuotas-historicas.md`, `herramientas/backtest_cuotas.py`):
    con el favorito >= 65 % las casas dan X 16,4 % y sale 13,5 % (6.096 partidos 2005-2026, igual en
    las dos mitades) y la mesa daba 15,6 % con 7,4 % real. X x0,82 (factor sacado de las cuotas, no
    ajustado a la mesa) mejora el log-loss de la mesa en las dos mitades (0,98645->0,98601;
    0,95679->0,95526). En Segunda no mejora (no se aplica).
Uso: from afinado import afinar_comp; p2 = afinar_comp(p, 'es.1')."""
T_POR_COMP = {"es.1": 1.15, "ligaf": 0.70}
T_DEFECTO = 1.05
X_TEMPLADA = {"es.1": (0.45, 0.60, 1.20)}  # (desde, hasta, factor de la X)
X_CLARO = {"es.1": (0.65, 0.82)}  # (favorito desde, factor de la X)


def afinar_comp(p, competicion=None):
    T = T_POR_COMP.get((competicion or "").split(":")[0], T_DEFECTO)
    q = [v ** T for v in p]; z = sum(q)
    p = [v / z for v in q]
    xt = X_TEMPLADA.get((competicion or "").split(":")[0])
    if xt and xt[0] <= max(p) < xt[1]:
        p[1] *= xt[2]; z = sum(p); p = [v / z for v in p]
    xc = X_CLARO.get((competicion or "").split(":")[0])
    if xc and max(p[0], p[2]) >= xc[0]:
        p[1] *= xc[1]; z = sum(p); p = [v / z for v in p]
    return p
