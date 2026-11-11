# Quiniela · índice

Entrada a todo el proyecto. Se actualiza al cerrar cada jornada.

## Cómo se trabaja
- **Prompt:** `prompt-maestro-v8.md` (pegarlo y escribir debajo `Jornada N · fase · presupuesto X €`).
- **Modelo oficial:** `modelo/euro_model.py` (necesita `numpy` y `scipy`; instrucciones en `modelo/README-mesa.md`).
- **Datos:** `datos/euro_j19.csv`, 23.631 partidos hasta el 1/11/2026.
- **Datos del navegador (Claude in Chrome):** procedimiento seguro y texto para pegar en `navegador/encargo-claude-in-chrome.md`; carga con `herramientas/importar_navegador.py`.
- **Cuentas:** `herramientas/quiniela_calc.py` (instrucciones en `herramientas/README.md`).
- **App «Control Quiniela»:** https://claude.ai/artifact/L7JpUFruxB2b3HLWoNRG6c. Sus datos salen de `python3 herramientas/app_datos.py` (escribe `app/datos/`); las bajas se mantienen a mano en `app/bajas.json` y las jornadas antiguas en `app/historial.json`. La página está en `app/index.html`.

## Jornadas
| Jornada | Fechas | Tipo | Estado | Boleto | Mejor columna | Sueltas | Pleno | Log-loss |
|---|---|---|---|---|---|---|---|---|
| J13–J16 | — | — | Registro en la sesión de claude.ai | — | J15: 9 · J16: 8 | J16: 4/5 | — | — |
| J17 | 27–29/10 | Copa del Rey | **No se pronostica** | — | — | — | — | — |
| J18 | — | Doméstica | Registro en la sesión de claude.ai | 18 € | — | — | — | Modelo 0,897 · mercado 0,786 |
| **J19** | 3–5/11 | Europea | **Cerrada** (`jornadas/j19/j19-resultados.md`) | 16 columnas · 12 € | 11 (4 × 1,88 € = 7,52 €) | 5/5 | 1-1 (salió 0-2) | Modelo 0,858 · mercado 0,729 (11 partidos) |
| **J20** | 7–8/11 | Doméstica | **Jugada** | 16 columnas · 12 € | 7 | pendiente | 1-1 (salió 1-2) | Modelo 1,072 |
| **J21** | 14–15/11 | Parón | **v1.1** (orden corregido) | 16 columnas (2 con X) · 12 € | pendiente | pendiente | 1-0 | pendiente |

## Pendiente
- J20: jugada (`jornadas/j20/j20-resultados.md`); faltan los premios.
- J21: v1 hecha (`jornadas/j21/j21-pronostico.md`). Revisión final y congelación el sábado 14 antes de las 11:00.
- Traer a `jornadas/` los JSON de J13–J18 con sus resultados para calcular la calibración acumulada.
- **Confirmado en la J19:** el modelo infravaloraba a los favoritos (backtest fuera de muestra). Corregido con T = 1,05; revisar en la J29.
