"""Afinado (temperatura T) del 1X2 por competición. Validado el 17/11/2026 en
`analisis/afinado-favoritos.md` (walk-forward 2022-26):
  - Primera: T=1,15 (mejora log-loss fuera de muestra 0,9621 -> 0,9600; los favoritos claros
    estaban cortos: daban 68 %, ganaban 74 %).
  - Segunda y el resto: T=1,05 (afilar NO mejora; en Segunda los favoritos no rinden de más).
Uso: from afinado import afinar_comp; p2 = afinar_comp(p, 'es.1')."""
T_POR_COMP = {"es.1": 1.15}
T_DEFECTO = 1.05


def afinar_comp(p, competicion=None):
    T = T_POR_COMP.get((competicion or "").split(":")[0], T_DEFECTO)
    q = [v ** T for v in p]; z = sum(q)
    return [v / z for v in q]
