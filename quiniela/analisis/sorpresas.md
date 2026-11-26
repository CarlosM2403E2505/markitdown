# Probabilidad de sorpresas (23/11/2026)

Carlos, tras el Rayo y el Tenerife de la J23: estudiar qué favoritos tienen más riesgo de sorpresa.

- **Datos:** football-data.co.uk vía el espejo de GitHub (xgabora, clase B): cuota 1X2, over/under, Elo y forma. 7.912 partidos de Primera y Segunda (2005-26) con el favorito de las casas entre el 45 y el 70 %, y 15.773 de Inglaterra, Italia, Alemania y Francia como control. Script `modelo/sorpresas.py` → `datos/sorpresas.json`.
- **Método:** sorpresa = el favorito no gana. Se compara con la que daban las casas sin margen. Un factor solo cuenta si sube la sorpresa por encima de la media en las dos mitades de España (2005-15 y 2016-26) y en las otras ligas.

## Resultado

| Grupo | Casas daban | Salió | X dada → real |
|---|---|---|---|
| España 2005-15 (n 3.476) | 46,6 % | 44,7 % | 26,7 → 25,1 % |
| España 2016-26 (n 4.436) | 46,3 % | 44,0 % | 26,5 → 26,3 % |
| Otras ligas (n 15.773) | 44,8 % | 43,7 % | 25,3 → 24,9 % |
| Favorito 45-55 % (España) | 50,5 % | 48,6 % | 28,1 → 27,9 % |

Diferencia frente a esa media (puntos de sorpresa), en España 1.ª mitad / 2.ª mitad / otras ligas:

| Factor | Diferencia | ¿Se repite? |
|---|---|---|
| Favorito en mala forma (≤ 5 de 15) | +0,3 / +1,3 / −1,0 | No |
| Rival en buena forma (≥ 10 de 15) | −0,7 / +2,0 / −0,7 | No |
| Favorito con ≤ 3 días de descanso | 0,0 / −2,0 / −2,2 | No (al revés) |
| Favorito visitante | +0,2 / +1,8 / −0,5 | No |
| Segunda División | −0,6 / 0,0 / — | No |
| Pocos goles esperados (over 2,5 < 45 %) | +1,7 / +1,8 / +0,4 | Solo en España, y depende del corte (con 43 % sale −0,6 en la 1.ª mitad) |
| Elo por debajo de la cuota | +0,1 / −0,1 / −1,0 | No |
| Agosto-septiembre / final de liga | −2,9 / +2,2 / +0,7 · −2,8 / −0,4 / −0,4 | No |

**Conclusión:**
- **Ningún factor medible hace que un favorito pierda más de lo que ya dicen las casas.** La cuota ya lleva la forma, el descanso, el Elo y la categoría. Las casas incluso se quedan algo cortas con el favorito (gana unos 2 puntos más).
- Un favorito del 49-55 % (el Rayo daba 49 % en las casas y el Tenerife-Mallorca, 43 %) **no gana una de cada dos veces**. Eso no se arregla con un factor: se arregla cubriendo. Dos fijos así aciertan los dos solo el 27 % de las veces.
- El fallo de la J23 fue de cobertura (el 1 del Rayo iba en 32 de 36 columnas) y de que la mesa daba más que las casas (Alavés 59 frente a 43, Tenerife-Mallorca 50 frente a 43).

## Regla nueva R3b (`herramientas/reglas_mesa.py`)

Si hay cuotas, el tramo de R3 se busca también con la probabilidad de las casas para el signo favorito de la mesa, y se aplica el tope más estricto. Las casas están calibradas (tabla de arriba), así que no es pesimismo, y no cambia ninguna probabilidad (R5): solo obliga a cubrir más.

| Partido | Antes | Con R3b |
|---|---|---|
| J23 Alavés – Deportivo (mesa 59, casas 43) | 75 % de columnas | 60 % |
| J23 Tenerife – Mallorca (mesa 50, casas 43; salió X) | 75 % | 60 % |
| J24 Feyenoord – Oporto (mesa 46, casas 40) | 75 % | 60 % |
| J24 Sporting CP – Man. United (mesa 45, casas 38) | 75 % | 60 % |

El Rayo (mesa 54, casas 49, 5 puntos de 15) ya baja al 60 % con la regla de mala forma. Tests en `herramientas/test_reglas_mesa.py` (7 OK). «Pocos goles» queda en vigilancia, sin regla: no se repite fuera de España.
