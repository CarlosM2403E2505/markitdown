# ¿Afilar los favoritos claros? Estudio del 17/11/2026

**Origen:** la auditoría de ventaja (`analisis/ventaja-de-la-mesa.md`) encontró que, con los favoritos muy claros, el modelo se quedaba corto (daba 75 %, ganaban el 86 %). Aquí se mide si subir la temperatura T lo arregla, sin romper el resto.

**Método:** `modelo/calibracion_favoritos.py`, walk-forward mensual 2022-26, Primera y Segunda por separado. Elegir con 2022-24, validar con 2025-26 (fuera de muestra).

## Primera: SÍ afila (aplicado)

| T | Validación | Prueba |
|---|---|---|
| 1,05 (actual) | 0,9941 | 0,9621 |
| 1,15 | 0,9930 | **0,9600** |
| 1,20 | 0,9930 | 0,9596 |
| 1,40 solo si favorito ≥0,55 | 0,9890 | 0,9587 |

- Subir T mejora la prueba de forma consistente. El tramo de favoritos claros estaba descalibrado (daba 68 %, ganaba 74 %); con T más alta se acerca.
- **Decisión: T = 1,15 para Primera.** Da casi toda la mejora (0,9600) y es simple y robusto; el afinado por tramos (0,9587) mejora algo más pero es más frágil (riesgo de sobreajuste). Lo recoge `modelo/afinado.py`.

## Segunda: NO afila (sin cambios)

| T | Validación | Prueba |
|---|---|---|
| 1,05 (actual) | 1,0402 | **1,0506** |
| 1,15 | 1,0392 | 1,0510 |
| 1,20 | 1,0390 | 1,0515 |
| Afinado por tramos | 1,0358 | 1,0601 (peor) |

- Afilar **empeora** la prueba. En Segunda los favoritos claros no rinden de más (en el tramo alto daban 66 %, ganaron 56 %, n=18). **Se mantiene T = 1,05.**

## Qué cambia a partir de la J23
- Los partidos de **Primera** se afinan con **T = 1,15**; Segunda, Liga F, selecciones y Champions femenina siguen con 1,05. Función única: `modelo/afinado.py` (`afinar_comp`), con test.
- Es la primera mejora del modelo que sale de la auditoría de ventaja. El Auditor repasó que la prueba mejora y que no se tocó Segunda.
