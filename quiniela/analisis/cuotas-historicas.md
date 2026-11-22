# Cuotas históricas frente a resultados (22/11/2026)

Petición de Carlos: buscar las cuotas de partidos pasados y su resultado para ajustar la mesa.

- **Datos:** football-data.co.uk (vía github.com/xgabora/Club-Football-Match-Data-2000-2025), cuota de mercado 1X2 y marcador, Primera y Segunda 2005-2026: 16.862 partidos (clase B). Margen medio 6,6 %. Script: `herramientas/backtest_cuotas.py` → `datos/backtest_cuotas.json`. Desde el contenedor, football-data.co.uk está bloqueado; el espejo de GitHub, no.
- **Método:** probabilidad sin margen; cada efecto se mide en dos mitades (2005-15 y 2016-26) y solo cuenta si va igual en las dos. Después se prueba en la mesa con sus probabilidades fuera de muestra (`datos/auditoria_ventaja.json`, 2024-26), con el factor sacado de las cuotas, sin reajustarlo.

| Hallazgo | Casas | Real | Mitades | En la mesa | Decisión |
|---|---|---|---|---|---|
| Primera, favorito ≥ 65 %: la X sale menos | 16,4 % | 13,5 % | −3,0 / −2,9 | daba 15,6 %, salía 7,4 %; X ×0,82 mejora log-loss 0,98645→0,98601 y 0,95679→0,95526 | **Aplicado** en `modelo/afinado.py` (X_CLARO) |
| Primera, favoritos 60-90 %: ganan más de lo que dice la cuota | 65-84 % | 69-89 % | sí | ya cubierto por T = 1,15 | Sin cambio |
| Segunda, partidos igualados (favorito < 45 %): X algo más | 30,7 % | 32,1 % | +1,1 / +1,7 | X ×1,06 mejora una mitad y empeora la otra | Rechazado |
| Segunda, favorito 55-65 %: X menos | 25,4 % | 23,3 % | −2,7 / −1,6 | la mesa va al revés (22 % vs 28 %) | Rechazado |
| Primera, partidos igualados: X | 29,2 % | 30,0 % | −0,4 / +2,0 | — | No estable |

- **Pleno al 15** (frecuencia real del marcador por tramo de favorito, Primera): favorito < 45 % → 1-1 (14,7 %), 1-0, 0-1/0-0; 45-55 % → 1-1 (13,3 %), 1-0; 55-65 % → 2-1 (11,0 %), 1-1, 1-0; ≥ 65 % → M-0 (16,8 %), M-1 (13,0 %). Es dato de control: el Pleno sigue siendo el marcador más probable de la mesa (§1.12); la X ×0,82 ya lo empuja hacia M-0 / M-1 en los favoritos claros.
- **Pendiente:** cruzar partido a partido con las 133 jornadas del backtest (los nombres de equipos de la auditoría no están guardados) y repetir con las cuotas de bet365 del histórico propio cuando haya jornadas.
