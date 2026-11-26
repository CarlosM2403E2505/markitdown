# Liga F: los favoritos claros estaban largos (20/11/2026)

**Pregunta:** ¿el modelo de la Liga F se pasa de confiado con los favoritos? El mercado (52 %) y el público (43 %) daban mucho menos que la mesa (75 %) en Tenerife F – Madrid CFF.

**Método:**
- Walk-forward sobre la temporada 2026-27, en bloques de 8 partidos (por orden del archivo).
- Se reajusta `ligaf_modelo.ajustar()` con todo lo anterior (temporada 2025-26 completa + lo jugado).
- Sin los partidos del Barça. Empates ×0,85. Temperatura T aplicada al 1X2.
- 61 partidos fuera de muestra (solo hay una temporada anterior en `datos/ligaf.json`).

## Calibración con el modelo vigente (T = 1,05)
| Favorito dado | Partidos | Prob. dada | Acierto real |
|---|---|---|---|
| 45-60 % | 16 | 52 % | 44 % |
| 60-70 % | 9 | 63 % | 56 % |
| **≥ 70 %** | **13** | **79 %** | **54 %** |

Casos ≥ 70 % que fallaron:
- Real Madrid – Eibar (X)
- Real Sociedad – Espanyol (X)
- Real Sociedad – Logroño (2)
- Tenerife – Deportivo (X)
- Tenerife – Sevilla (2)
- Real Madrid – Badalona (X)

## Log-loss según la temperatura
| T | Todos (61) | 1.ª mitad (25) | 2.ª mitad (36) |
|---|---|---|---|
| 1,05 (vigente) | 1,0827 | 1,1154 | 1,0599 |
| 0,90 | 1,0645 | 1,0997 | 1,0401 |
| 0,80 | 1,0556 | 1,0915 | 1,0307 |
| **0,70** | **1,0495** | 1,0853 | 1,0247 |
| 0,60 | 1,0465 | 1,0811 | 1,0224 |
| 0,50 | 1,0466 | 1,0789 | 1,0241 |

**Decisión:**
- Aplanar mejora en las dos mitades por separado.
- Se aplica **T = 0,70**, conservador frente al óptimo de 0,5-0,6, por ser una sola temporada y 61 partidos.
- Cambio en `modelo/afinado.py` (`T_POR_COMP["ligaf"]`); test en `test_afinado.py`.
- Se revisará con más jornadas.

## Efecto en la J23
| Partido | Antes | Ahora (T = 0,70) |
|---|---|---|
| Eibar F – Atlético F | 11 / 17 / 72 | 17 / 23 / 60 |
| Granada F – Real Madrid F | 11 / 16 / 73 | 17 / 22 / 61 |
| Real Sociedad F – Sevilla F | 65 / 18 / 17 | 55 / 23 / 23 |
| Tenerife F – Madrid CFF | 75 / 14 / 10 | 63 / 21 / 17 |

**Los signos no cambian.** Con estos precios:
- el mejor boleto de 3 dobles + 1 triple es el mismo que ya teníamos;
- las 9 sencillas actuales dan la misma P(≥13) que las recalculadas (4,27 % frente a 4,23 %), así que se mantienen.

Lo que cambia es la **probabilidad real** del conjunto (33 columnas):
- **P(14): 1 entre 176** (antes se estimaba 1 entre 85);
- **P(≥13): 4,3 %** (antes 7,5 %);
- **P(14 + Pleno 1-1): 1 entre 1.540** (antes 1 entre 760).
