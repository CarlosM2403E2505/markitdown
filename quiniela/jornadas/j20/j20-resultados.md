# Jornada 20 · resultados (provisional, sin premios) · 8/11/2026

> Combinación: elperiodicodeceuta.es (de SELAE) y lotoluck.com, 8/11/2026. Premios: `pendiente` (escrutinio oficial). Boleto evaluado: v1.1 (16 sencillas, el último registrado; el sábado no hubo revisión final).

## Combinación ganadora: `2X221X1222XX21` · Pleno 1-2 · 4 empates

| # | Partido | Resultado | Signo | P(signo que salió) | En el boleto |
|---|---|---|---|---|---|
| 1 | Málaga – Racing | 1-2 | 2 | 29,0 % | ❌ |
| 2 | Osasuna – Athletic | 1-1 | X | 27,8 % | ✅ (2 columnas) |
| 3 | Valencia – Real Madrid | 0-3 | 2 | 55,5 % | ✅ |
| 4 | Elche – Betis | 0-2 | 2 | 33,8 % | ✅ |
| 5 | Real Sociedad – Rayo | 1-0 | 1 | 50,9 % | ✅ |
| 6 | Celta – Levante | 0-0 | X | 24,0 % | ❌ |
| 7 | Villarreal – Getafe | 2-0 | 1 | 58,6 % | ✅ |
| 8 | Cádiz – Oviedo | 1-2 | 2 | 43,6 % | ✅ |
| 9 | Girona – Almería | — | 2 | 25,1 % | ❌ |
| 10 | Sporting – Valladolid | — | 2 | 23,1 % | ❌ |
| 11 | Athletic F – Real Madrid F | — | X | 16,4 % | ❌ |
| 12 | Logroño F – Sevilla F | — | X | 26,4 % | ✅ |
| 13 | Eibar F – Real Sociedad F | — | 2 | 40,2 % | ✅ |
| 14 | Tenerife F – Alavés F | — | 1 | 64,6 % | ✅ |
| 15 | Pleno: Atlético – Barcelona | 1-2 | | 7,6 % (4.º) | ❌ (1-1) |

Marcadores de los partidos 9 a 14: `pendiente`.

## Balance provisional

- **Mejor columna: 7 aciertos → sin premio.** Reparto: 7 columnas con 7, 6 con 6 y 3 con 5. Con 4 dobles (A) también habría hecho 7; con la reducida (B), 8. Tampoco cobra.
- **Log-loss 1,072** (repartir 1/3 a cada signo da 1,099). Fallos del signo principal: 8, esperados 6,95.
- **Corrección del 9/11 (post-mortem): no era un error que convenga arreglar.** Se probó con datos fuera de muestra (`modelo/calibracion_liga_equipo.py`): asignar a cada equipo la liga de esta temporada mejora en el resto de Europa, pero **empeora en España**. En los 126 partidos españoles con un equipo ascendido o descendido, el log-loss sube de 1,006 a 1,016. Los recién descendidos sí son fuertes en Segunda y los recién ascendidos tardan en adaptarse. El modelo se queda como está; la derrota del Girona fue varianza.
- **Lo que se escribió el 8/11 (retirado):** el modelo asigna a cada equipo la liga en la que más jugó en los últimos 365 días. Así, Girona, Oviedo y Mallorca (descendidos) cuentan como de Primera y salen sobrevalorados en Segunda, y Racing, Deportivo y Málaga (ascendidos) cuentan como de Segunda y salen infravalorados en Primera. En esta jornada afectó al Girona–Almería (el Girona era favorito al 53 % frente al líder), al Cádiz–Oviedo y al Málaga–Racing. Se corrige en el post-mortem, con backtest.
