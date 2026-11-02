# Quiniela · índice

Entrada a todo el proyecto. Se actualiza al cerrar cada jornada.

## Cómo se trabaja
- **Prompt:** `prompt-maestro-v6.md` (pegarlo y escribir debajo `Jornada N · fase · presupuesto X €`).
- **Modelo oficial:** `modelo/euro_model.py` (necesita `numpy` y `scipy`; instrucciones en `modelo/README-mesa.md`).
- **Datos:** `datos/euro_j19.csv`, 23.631 partidos hasta el 1/11/2026.
- **Cuentas:** `herramientas/quiniela_calc.py` (instrucciones en `herramientas/README.md`).

## Jornadas
| Jornada | Fechas | Tipo | Estado | Boleto | Mejor columna | Sueltas | Pleno | Log-loss |
|---|---|---|---|---|---|---|---|---|
| J13–J16 | — | — | Registro en la sesión de claude.ai | — | J15: 9 · J16: 8 | J16: 4/5 | — | — |
| J17 | 27–29/10 | Copa del Rey | **No se pronostica** | — | — | — | — | — |
| J18 | — | Doméstica | Registro en la sesión de claude.ai | 18 € | — | — | — | Modelo 0,897 · mercado 0,786 |
| **J19** | 3–5/11 | Europea | **v1 primera pasada** (`jornadas/j19/`) | B · 12 € | pendiente | pendiente | 1-1 | pendiente |

## Pendiente
- J19: revisión final antes del cierre (martes 3/11).
- Traer a `jornadas/` los JSON de J13–J18 con sus resultados para calcular la calibración acumulada.
- Hipótesis para medir: ¿el modelo infravalora a los favoritos claros frente al mercado? (J18 y J19).
