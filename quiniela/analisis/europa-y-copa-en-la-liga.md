# Cómo afectan la Champions, la Europa League y la Copa a la liga · 6/11/2026

> Pregunta del usuario: «Analiza los resultados de las anteriores fechas con partidos de Champions y Copa entre medias; cómo afectó a la liga y a la Segunda». Scripts: `modelo/calibracion_europa_liga.py`, `calibracion_europa_analisis.py` y `calibracion_reglas_fatiga.py`. Datos: `datos/euro_j20.json`.

## Método

- El modelo se reajusta cada mes (de septiembre de 2024 a noviembre de 2026) solo con los datos anteriores a ese mes: **todas las predicciones son fuera de muestra**.
- Se toman los partidos de liga de los clubes que jugaban competición europea esa temporada (4.822 partidos de 39 ligas):
  - **Tras Europa:** el club jugó en Champions, Europa League o Conference entre 2 y 6 días antes (1.371 partidos).
  - **Control:** el mismo tipo de club sin Europa en los 7 días previos (3.451 partidos).
- Se compara lo real con lo esperado (puntos y goles) en los dos grupos. La diferencia entre grupos es el efecto de Europa, sin confundirlo con que estos clubes son favoritos.

## Resultados

| Grupo | Partidos | Puntos frente a lo esperado (respecto al control) | Ataque | Goles encajados |
|---|---|---|---|---|
| Tras Europa, cualquier día | 1.371 | −0,07 (±0,08) | −3,8 % | +1,4 % |
| Tras Champions (martes o miércoles) | 749 | −0,04 (±0,10) | −3,8 % | 0,0 % |
| Tras Europa el jueves | 652 | −0,09 (±0,10) | −2,1 % | +4,3 % |
| Jueves → domingo | 517 | −0,11 (±0,11) | −3,9 % | +3,6 % |
| Jueves → lunes | 83 | +0,04 (±0,26) | +2,7 % | +2,3 % |
| Tras Europa, fuera de casa | 706 | −0,09 (±0,10) | −5,3 % | −0,4 % |
| Tras Europa, en casa | 742 | −0,03 (±0,10) | −0,6 % | +4,1 % |
| **Primera, tras Europa** | 164 | +0,10 (±0,23) | −1,5 % | −8,8 % |

Entre paréntesis, el margen del 95 %. Ninguna diferencia es estadísticamente clara: el efecto existe en la dirección esperada, pero es pequeño (menos de una décima de punto por partido). En Primera no se ve.

## ¿Mejora el precio ajustar por cansancio?

| Regla (con la calibración T = 1,05 aplicada) | Log-loss, todas las ligas | Log-loss, Primera |
|---|---|---|
| **Sin ajuste** | **0,9568** | **0,9239** |
| La que se usaba (jueves −4 % ataque / +2,5 % encajados) | 0,9592 | 0,9275 |
| La anterior + martes/miércoles −3 % | 0,9609 | 0,9302 |
| Jueves −4 % / +4 % y martes/miércoles −3 % | 0,9615 | 0,9311 |
| Jueves doble (−8 % / +5 %) | 0,9628 | 0,9318 |

**No ajustar es lo mejor en todos los casos.** El modelo ya infravalora a estos clubes, que suelen ser favoritos (en el control sacan 0,21 puntos más de lo esperado), y restarles goles los infravalora todavía más. **Decisión:** el ajuste de cansancio se retira del prompt (v8, fase 3). Queda como aviso.

## Copa del Rey (primera ronda de 2026/27, 27–29 de octubre)

No hay partidos de Copa en los datos; se buscaron los del martes y el jueves (los del miércoles no aparecieron).

| Equipo | Copa | Liga el fin de semana | Puntos (esperados) |
|---|---|---|---|
| Villarreal | mar: 5-0 en Manacor | vie: 0-1 con el Espanyol | 0 (1,90) |
| Espanyol | mar: eliminado en la prórroga | vie: 1-0 en Villarreal | 3 (0,87) |
| Rayo | mar: 3-2 en la prórroga | sáb: 3-0 al Celta | 3 (1,40) |
| Málaga | mar: 3-0 | sáb: 1-2 en el Betis | 0 (0,62) |
| Sevilla | jue: 3-0 | dom: 1-3 en Getafe | 0 (1,28) |
| Athletic | jue: 6-1 | dom: 2-1 a la Real | 3 (1,58) |
| Deportivo | jue: 3-0 | lun: 2-1 a Osasuna | 3 (1,29) |
| Osasuna | jue: 6-0 | lun: 1-2 en Riazor | 0 (1,43) |
| Girona (Segunda) | mar: 2-0 | sáb: 0-1 en el Sanse | 0 (1,84) |
| Oviedo (Segunda) | jue: eliminado en los penaltis | lun: 2-3 con Las Palmas | 0 (1,69) |
| Las Palmas (Segunda) | mar: 3-1 en la prórroga | lun: 3-2 en Oviedo | 3 (1,03) |
| Cádiz (Segunda) | jue: 3-1 | lun: 1-2 en Mallorca | 0 (0,65) |

**Total: −0,05 puntos por partido frente a lo esperado.** Con 12 casos no hay efecto medible, y hay de todo: el Villarreal perdió en casa tres días después; el Rayo y Las Palmas, que jugaron prórroga, ganaron.

## Segunda División

Los equipos de Segunda no juegan en Europa, así que su única competición entre semana es la Copa. Con los 4 casos de esta temporada no se puede medir nada. Para saberlo haría falta el histórico de la Copa de 2024/25 y 2025/26, que no está en los datos: queda pendiente para el ingeniero de datos (sección 1 del prompt).

## Consecuencias

1. **Prompt v8, fase 3:** sin ajuste por Europa ni por Copa. Se vuelve a medir en la J29.
2. **J20 v1.1:** la Real Sociedad, el Celta y el Getafe recuperan unos 2 puntos cada uno. El boleto no cambia y P(14) mejora de 1 entre 1.584 a 1 entre 1.489.
3. **Lo que sí sirve como aviso:** las prórrogas y las rotaciones anunciadas, que ningún número recoge todavía.
