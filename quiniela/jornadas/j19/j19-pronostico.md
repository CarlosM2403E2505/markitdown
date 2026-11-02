# Jornada 19 · v1 primera pasada · presupuesto 12 €

> Registro: **v1** · 2/11/2026. Precio: mesa de claude.ai (modelo oficial `euro_model.py` + ajustes de bajas y del favorito que viene de perder). Auditoría, boletos, Pleno y sueltas: `herramientas/quiniela_calc.py` (salida completa en `j19-calculadora.txt`). **No sobrescribir: la revisión final va como v2 debajo.**

## A. Resumen ejecutivo

- **Estado:** primera pasada. Revisión final pendiente (martes 3/11, antes del cierre): alineaciones, portero del Bayern, Olise y cuotas de los partidos 12–14.
- **Auditoría del precio:** volví a ejecutar el modelo con los 23.631 partidos y reproduce exactamente los goles esperados «sin ajustes» de la mesa. Las lambdas finales reproducen el 1X2 final con un error máximo de 0,1 puntos.
- **Lo más claro:** Arsenal (68,8 %) y Real Madrid (66,0 %) fuera. El mercado los ve aún más claros (75,9 %).
- **Lo más incierto:** Bodø–Lille, Lens–Como, Real Sociedad–Lyon y Celta–Union. Las cuatro van con el favorito por debajo del 40 %.
- **Alarma de mercado:** Barcelona–Aston Villa. Para el modelo, el Barça gana el 52,6 %; para el mercado, el 75,6 %. La diferencia es de 23 puntos y no tiene razón identificada (ver E). El partido va a doble por el veto, así que el boleto cubre el 1 en cualquier caso.
- **Boleto por defecto (B):** P(14) = 1 entre 2.564 · P(≥13) = 0,69 % · P(≥10) = 34,8 %.
- **Pleno:** 1-1 (9,3 %).

## B. Por qué estos partidos

Es una **semana europea** y Loterías ha aplicado la regla «miércoles europeo: españoles y grandes»: 11 partidos de Champions, 2 de Europa League y 1 de Conference. Hay 7 equipos españoles en el 1–14 (Barça, Villarreal, Real Madrid, Betis, Real Sociedad, Celta y Getafe) más el Atlético en el Pleno. El resto son los grandes: PSG, Liverpool, City, Arsenal, United, Nápoles, Dortmund y Bayern. El Pleno es **Atlético–Bayern**, el partido de más tirón del martes, coherente con la regla de 8 de 14 Plenos con Madrid, Barça, Atlético o España.

**Jornada abierta:** 6 partidos tienen el favorito por debajo del 45 % y la suma de P(X) es 3,23. Habrá pocos acertantes de 14 y el premio será alto si sale.

*Pendiente:* comprobar si algún equipo español con partido europeo esta semana ha quedado fuera, y la competición exacta de Getafe–Brighton (el JSON dice Conference y el archivo de partidos, «Europa/Conference»). No cambia el precio, porque el factor de empates es 1,0 en las dos.

## C. Los 14 + Pleno

| # | Partido | P(1) | P(X) | P(2) | Signo | Riesgo | Motivo principal |
|---|---|---|---|---|---|---|---|
| 1 | Barcelona – Aston Villa | 52,6 | 21,6 | 25,8 | **12** (veto) | Muy alto | Viene de perder en París; el mercado discrepa 23 puntos sin razón identificada |
| 2 | Bodø/Glimt – Lille | 37,3 | 26,1 | 36,6 | **12** (veto) | Muy alto | Campo nórdico; datos de Noruega incompletos |
| 3 | Man. United – Roma | 42,6 | 25,9 | 31,6 | **12** (veto) | Alto | Viene de perder 4-1 en Como; el mercado coincide (42,0) |
| 4 | Villarreal – PSG | 26,9 | 21,1 | 51,9 | 2 ⚠️ | Moderado | PSG superior; el mercado da 60,1 |
| 5 | AEK Atenas – Real Madrid | 15,4 | 18,6 | 66,0 | 2 | Moderado* | Datos de Grecia incompletos (* subido de Bajo) |
| 6 | Fenerbahçe – Liverpool | 18,6 | 18,7 | 62,7 | 2 ⚠️ | Moderado | Datos de Turquía incompletos; el mercado coincide (61,3) |
| 7 | B. Dortmund – Betis | 51,4 | 22,5 | 26,1 | 1 ⚠️ | Moderado | Dortmund en casa; el mercado da 56,0 |
| 8 | Oporto – Nápoles | 43,2 | 28,2 | 28,7 | **12** (veto) | Alto | Viene de perder 0-1 con el PSV |
| 9 | Lens – Como | 34,3 | 26,9 | 38,8 | **12** | Muy alto | Sin favorito; el mercado da al Como un 43,1 |
| 10 | Leipzig – Man. City | 22,4 | 20,2 | 57,4 | 2 ⚠️ | Moderado | City superior; el mercado da 60,1 |
| 11 | Slavia Praga – Arsenal | 12,2 | 19,0 | 68,8 | 2 | Moderado* | Chequia sin datos desde el 20/09 (* subido de Bajo) |
| 12 | Real Sociedad – Lyon | 39,8 | 23,4 | 36,8 | **12** | Muy alto | Sin favorito; sin cuota todavía |
| 13 | Celta – Union SG | 37,2 | 26,2 | 36,5 | **12** | Muy alto | Sin favorito; faltan datos de Bélgica 2025-26 |
| 14 | Getafe – Brighton | 19,1 | 24,9 | 56,0 | 2 ⚠️ | Moderado | Brighton superior; sin cuota todavía |
| 15 | **Pleno: Atlético – Bayern** | 36,1 | 21,9 | 42,1 | **1-1** | — | Bayern sin Saibari, Gnabry, Musiala ni Díaz |

Suma de P(X) = 3,23 (normal: ~3,5; las copas UEFA tienen menos empates). Fallos esperados con los 14 signos sencillos: 6,94.

\* **Criterio aplicado:** AEK, Fenerbahçe, Slavia y Union tienen más de 30 partidos, así que no son «dato flojo» según la fase 1. Sin embargo, les faltan temporadas enteras. En lugar de vetarlos, lo que llevaría a 8 vetos con solo 7 dobles, he **subido su riesgo un nivel**. El mercado confirma la dirección en los cuatro.

## D. Copa/Europa y bajas

Los ajustes son los de la mesa de claude.ai: bajas de clase A/B y el −4,5 al favorito que viene de perder. **No los he reverificado aquí.**

| # | Ajuste | Goles esperados sin ajuste → final |
|---|---|---|
| 1 | Barça viene de perder 4-2 en París (−4,5) + bajas | 2,42–1,49 → 2,01–1,36 |
| 2 | Bodø viene de perder 4-3 en Nápoles (−4,5) + bajas | 1,57–1,44 → 1,33–1,32 |
| 3 | United viene de perder 4-1 en Como (−4,5) + bajas | 1,70–1,29 → 1,45–1,21 |
| 4 | Bajas | 1,49–2,16 → 1,46–2,08 |
| 8 | Oporto viene de perder 0-1 con el PSV (−4,5) + bajas | 1,48–1,11 → 1,28–0,99 |
| 9 | Bajas | 1,45–1,39 → 1,21–1,31 |
| 15 | Bayern sin Saibari, Gnabry, Musiala ni Díaz (×0,925); Atlético sin Hjulmand (×0,985) | Pendiente: portero del Bayern y Olise |

**Aviso de proceso:** en el partido 9, el local pasa de 1,45 a 1,21 (un −17 %) por bajas, muy por encima del tope de ±5 % de la fase 3. Solo estaría justificado si la baja es del portero o del delantero centro, y aun así el tope es del 10 %. **Hay que confirmarlo en la revisión final.** Lo mismo ocurre con el local del partido 2 (−15 %) y el del 3 (−15 %), aunque ahí se suma el −4,5 del veto.

## E. Mercado y discrepancias

Cuotas de bet365 del lunes 2/11 a las 14:00, normalizadas. Solo sirven de control.

| # | Modelo (signo principal) | bet365 | Diferencia | Razón |
|---|---|---|---|---|
| 1 | 52,6 (1) | 75,6 | **−23,0** | **Sin identificar.** Los datos del Barça están bien (40-16 en goles en sus 10 últimos). Sin ajustes el modelo ya da 58,1, así que la diferencia no viene de los ajustes. Hipótesis para el post-mortem: el modelo infravalora a los grandes de LaLiga frente a la Premier |
| 2 | 37,3 (1) | 52,6 | **−15,4** | **Identificada:** Noruega a medias (80 de ~200 partidos) y una sola ventaja de campo para todos (el Bodø ganó 4 de sus 5 últimos en casa, con césped artificial) |
| 5 | 66,0 (2) | 75,9 | −9,9 | Datos de Grecia incompletos |
| 4 | 51,9 (2) | 60,1 | −8,2 | — |
| 11 | 68,8 (2) | 75,9 | −7,1 | Chequia sin datos desde el 20/09 |
| 3, 6, 7, 8, 9, 10, 15 | — | — | Menos de 6 puntos | — |
| 12, 13, 14 | — | Sin cuota | `pendiente` | — |

El modelo es sistemáticamente **menos rotundo que el mercado con los favoritos**: en los 11 partidos con cuota, el favorito del mercado tiene más probabilidad en 9. Lo mismo pasó en la J18, donde el mercado (log-loss 0,786) superó al modelo (0,897). **Es la señal más importante de esta jornada para el post-mortem.**

% del público (Quiniela15): `pendiente`.

**Integridad:** solo hay una foto de cuotas, así que no se pueden ver movimientos. *«No se ha encontrado evidencia pública verificable suficiente para afirmar una irregularidad»*.

## F. Contrario (partidos de riesgo Alto y Muy alto)

**P1 Barcelona – Aston Villa.** Los 3 factores que más mueven el precio: el ataque del Barça (40 goles en 10 partidos), una defensa que encaja (16 goles, 4 en París) y el nivel del Villa en Premier (ganó al City el 24/10). Mejor argumento para el **1**: todo el mercado y el Camp Nou. Para la **X**: el Villa empata con frecuencia (3 de sus 10 últimos). Para el **2**: el Barça encaja en casi todos los partidos y el Villa marcó en 9 de 10. → **12** por el veto. El 1 queda cubierto.

**P2 Bodø – Lille.** Factores: el campo (4 de 5 ganados en casa), los datos de Noruega incompletos y el Lille, que marca poco (12 goles en 10 partidos). **1**: el mercado lo da favorito (52,6). **X**: el Lille empató 2 de sus 5 últimos. **2**: el Bodø encajó 18 goles en sus 10 últimos. → **12**. Si la revisión final no aporta nada nuevo, el mercado sugiere que el 1X podría ser mejor doble que el 12. Solo se cambiaría con evidencia A/B, porque la diferencia entre la X y el 2 en el modelo es de 10 puntos.

**P3 Man. United – Roma.** Factores: el mal momento del United (10 goles a favor y 17 en contra en sus 10 últimos, con el 4-1 de Como), Old Trafford y el ataque de la Roma (26 goles en 10 partidos). **1**: el modelo y el mercado coinciden en un 42 %. **X**: 25,9 %. **2**: el United encaja casi dos goles por partido y la Roma marca más de dos. → **12**.

**P8 Oporto – Nápoles.** Factores: el Oporto viene de perder con el PSV pero lleva 21 goles a favor y 10 en contra en sus 10 últimos; el Dragão; y un Nápoles irregular (17 a favor y 15 en contra). **1**: el mercado da 48,5. **X**: es el partido con más empate de la jornada (28,2). **2**: casi igual que la X (28,7). → **12**, porque el 2 supera a la X por 0,5 puntos. Con esa diferencia, el 1X sería igual de defendible.

**P9 Lens – Como.** Factores: la forma del Como (ganó 4-1 al United), el Lens en casa y la reducción del −17 % en el local, pendiente de confirmar. **1**: el campo. **X**: 26,9. **2**: el mercado lo da al 43,1. → **12**.

**P12 Real Sociedad – Lyon.** Factores: la igualdad, dos ataques parecidos (1,63 y 1,56 goles esperados) y que aún no hay cuota. **1**: el campo. **X**: 23,4. **2**: el Lyon marca fuera. → **12**.

**P13 Celta – Union SG.** Factores: los datos incompletos del Union, la igualdad y Balaídos. **1**: 37,2. **X**: 26,2. **2**: 36,5. → **12**. Es el doble menos fiable por datos.

## G. Boleto B · reducida de 7 dobles al 13 (16 apuestas, 12 €)

Dobles: 1, 2, 3, 8 (vetos) + 9, 12, 13 (todos como 12). Sencillos: 4·2, 5·2, 6·2, 7·1, 10·2, 11·2, 14·2.

```
 1. 11122211222112     9. 21122211222222
 2. 11122212122222    10. 21122212122112
 3. 11222211122212    11. 21222211122122
 4. 11222212222122    12. 21222212222212
 5. 12122211122122    13. 22122211122212
 6. 12122212222212    14. 22122212222122
 7. 12222211222222    15. 22222211222112
 8. 12222212122112    16. 22222212122222
```
Pleno en las 16 columnas: **1-1**.

| | Boleto B (reducida, 12 €) | Boleto A (4 dobles, 12 €) | 18 € de la otra sesión (1 triple + 3 dobles) |
|---|---|---|---|
| P(14) | 1 entre 2.564 | **1 entre 2.300** | 1 entre 1.652 |
| P(≥13) | **0,69 %** | 0,53 % | 0,71 % |
| P(≥12) | **4,3 %** | 2,9 % | 3,8 % |
| P(≥11) | **15,1 %** | 10,2 % | 12,7 % |
| P(≥10) | **34,8 %** | 24,9 % | 29,6 % |

- El **A** (dobles en 1, 2, 3 y 8, los cuatro vetos) da algo más de P(14). El **B** da muchos más premios de 10 a 12.
- Maximizar P(13) en vez de P(14) da la misma reducida.
- El boleto de 18 € cuesta un 50 % más y su P(14) es un 39 % mejor que el A. **El presupuesto lo fijas tú.** Aquí va el de 12 €, que es el que marcan las instrucciones.

## H. Los 14 signos individuales + Pleno

`1 1 1 2 2 2 1 1 2 2 2 1 1 2` (fallos esperados: 6,94).

| Pleno | Resultado | Probabilidad |
|---|---|---|
| **Principal (se juega)** | **1-1** | 9,3 % |
| Conservador (el más frecuente compatible con el 2) | 0-1 | 5,6 % |
| De varianza | M-M | 6,2 % |

Mezcla de 80 % Poisson y 20 % de la distribución empírica (23.631 partidos). El 1-1 saca más de 1 punto al 1-2 (8,0 %). P(14 y Pleno) con el B: 1 entre 27.521.

## I. 5 apuestas sueltas

| Apuesta | Probabilidad | Mercado |
|---|---|---|
| Liverpool marca (en Fenerbahçe) | 90,8 % | Datos de Turquía incompletos |
| Real Madrid marca (en Atenas) | 89,9 % | El mercado lo ve más claro |
| Man. City marca (en Leipzig) | 88,9 % | — |
| Arsenal marca (en Praga) | 88,1 % | El mercado lo ve más claro |
| Barcelona marca (contra el Villa) | 86,6 % | El mercado lo ve mucho más claro |

Son 5 partidos distintos. Aciertos esperados: 4,44 de 5. P(las 5) = 55,4 %. No hay ninguna de Primera porque esta semana no hay liga.

## J. Lo aprendido aplicado

1. **Veto del favorito que viene de perder en Europa** (decisión del usuario): 4 partidos (1, 2, 3 y 8) van a doble.
2. **Veto de campo nórdico** (*provisional, n = 3*): el Bodø, coincidente con el anterior.
3. **Datos incompletos sin veto:** se sube un nivel de riesgo en lugar de vetar, para no superar los 7 dobles.
4. **J18, el mercado superó al modelo:** esta jornada el patrón se repite (el modelo es menos rotundo con los favoritos). Se registra para medirlo con más jornadas, sin tocar todavía el precio.

## K. Auditoría final y riesgos

- [x] Los 15 partidos coinciden con la captura del boleto oficial (`boleto-oficial.png`). El partido 10 sale como «Leipzig – Manche…»: es el City, porque el United juega el partido 3.
- [x] La salida de la calculadora no tiene errores; cada partido suma el 100 %; suma de X: 3,23.
- [x] El modelo, reejecutado, reproduce el precio sin ajustes de la mesa.
- [ ] **Ajustes por bajas por encima del tope de ±5 %** en los partidos 2, 3 y 9: confirmar las clases A/B y el tamaño en la revisión final.
- [ ] Bajas: la clasificación A–D está en la sesión de claude.ai, no aquí.
- [x] Coste: 12 €, sin columnas duplicadas, los 4 vetos dentro de los dobles y el mismo Pleno en todas.
- **Lo que puede cambiar antes del cierre:** el portero del Bayern y Olise (Pleno), las cuotas de los partidos 12–14 y la confirmación de las bajas de los partidos 2, 3 y 9.

**Honestidad:** con 16 apuestas, los 14 aciertos salen 1 vez entre 2.564 en esta jornada, y con el Pleno, 1 entre 27.521. La Quiniela devuelve el 55 % de lo apostado. El sistema busca precio y valor; no elimina la varianza.

## L. Registro

| Versión | Fecha | Qué |
|---|---|---|
| v1 | 2/11/2026 | Primera pasada (este documento) |
| v2 | — | Revisión final: `pendiente` |
| Resultado | — | `pendiente` |
| Evaluación | — | `pendiente` (`quiniela_calc.py postmortem jornadas/j19/j19.json`) |

## M. Fuentes

- Boleto oficial: captura de juegos.loteriasyapuestas.es aportada por el usuario el 2/11/2026 (`boleto-oficial.png`).
- Precio: mesa de claude.ai, 2/11/2026 (`j19_lambdas_1x2.json`, `j19_precio_final.json`, `j19_modelo_v1_sin_ajustes.json`).
- Datos: `datos/euro_j19.csv`, 23.631 partidos (openfootball hasta el 20/09/2026; después uefa.com, futboltotal.futbol, ESPN y thestatsapi, según el README de la mesa).
- Cuotas: bet365.es en el navegador integrado del usuario, 2/11/2026 a las 14:00 CET (`bet365_lunes_2nov_1300.json`).

---

# v1.1 · cambio de sistema · 2/11/2026

> El usuario pide que la mesa elija el sistema cada jornada. **No cambia ningún precio ni ningún signo de la v1**; cambia solo cómo se reparten las 16 apuestas. Salida completa: `j19-calculadora-v1.1.txt`.

## Por qué cambia

Con 16 apuestas, la probabilidad de hacer 14 es la suma de las probabilidades de las 16 columnas, porque como mucho una acierta las 14. El conjunto de 16 columnas con más P(14) es, por tanto, el de **las 16 columnas más probables**, que ningún sistema de dobles puede superar. La calculadora las busca entre todas las combinaciones posibles y respeta los 4 vetos: los partidos 1, 2, 3 y 8 aparecen con dos signos.

| Sistema (12 €) | P(14) | P(≥13) | P(≥12) | P(≥10) |
|---|---|---|---|---|
| A · 4 dobles completos | 1 entre 2.300 | 0,53 % | 2,9 % | 24,9 % |
| B · reducida de 7 dobles (v1) | 1 entre 2.564 | 0,69 % | **4,3 %** | **34,8 %** |
| **C · las 16 columnas más probables (elegido)** | **1 entre 1.434** | **0,77 %** | 4,0 % | 29,4 % |

**Criterio** (prompt v6, fase 8): de los sistemas con P(14) de al menos el 90 % de la máxima, el de mayor P(≥12). Aquí solo C cumple el primer filtro: A se queda en el 62 % de la máxima y B en el 56 %. C mejora la P(14) de la reducida en un 79 % y también su P(≥13). A cambio, cede 5 puntos en P(≥10), que es el premio más pequeño.

## Boleto v1.1 · 16 apuestas sencillas · 12 €

Se juega en «Sencilla o múltiple», en 2 bloques de 8 columnas. **Pleno 1-1 en todas.**

```
 1. 11122211222112     9. 11122211122112
 2. 12122211222112    10. 12122211122112
 3. 11122211222122    11. 11122211122122
 4. 12122211222122    12. 12122211122122
 5. 11122211222212    13. 11122211122212
 6. 12122211222212    14. 11222211222112
 7. 11122211222222    15. 11122212222112
 8. 12122211222222    16. 21122211222112
```

Las columnas se concentran donde el modelo no tiene favorito: el 2 (Bodø–Lille) y el 13 (Celta–Union) cambian de signo en 6 de las 16 columnas, y el 9 (Lens–Como) y el 12 (Real Sociedad–Lyon) en 5. Los partidos 1, 3 y 8 cambian en una sola columna, lo justo para cumplir el veto. Los otros 7 partidos llevan el mismo signo en las 16.

P(14 y Pleno) = 1/1.434 × 9,3 % = **1 entre 15.400**, frente a 1 entre 27.521 con la reducida.

**Riesgo propio del sistema:** al concentrarse en lo que el modelo ve más probable, C depende más del modelo que una reducida. Si el modelo se equivoca de forma sistemática (la J18 y la alarma del Barça apuntan a que es menos rotundo que el mercado con los favoritos), C lo nota más. Se medirá en el post-mortem comparando el resultado de C con el que habrían tenido A y B.

| Versión | Fecha | Qué |
|---|---|---|
| v1.1 | 2/11/2026 | Sistema C (16 columnas más probables) en lugar de la reducida. Precio y signos sin cambios |

### Nota sobre los empates (v1.1)

Ninguna de las 16 columnas lleva una X. Tampoco las llevaban el boleto A ni la reducida B. Que la jornada termine **sin ningún empate** tiene una probabilidad del **2,5 %** según el modelo: lo normal son 2 a 4 empates (media de 3,23).

Aun así, meter X empeora el boleto en todas las categorías:

| Sistema | P(14) | P(≥13) | P(≥12) | P(≥10) |
|---|---|---|---|---|
| C · sin X (elegido) | 1 entre 1.434 | 0,77 % | 4,0 % | 29,4 % |
| C + 2 columnas con X | 1 entre 1.462 | 0,7 % | 3,8 % | 28,6 % |
| C + 4 columnas con X | 1 entre 1.501 | 0,7 % | 3,7 % | 28,0 % |
| C + 8 columnas con X | 1 entre 1.608 | 0,7 % | 3,6 % | 28,0 % |

El motivo: sabemos que habrá unos 3 empates, pero no en qué partidos. Poner una X en un partido concreto es apostar a algo que pasa como mucho el 28 % de las veces, en lugar del 37–43 % del signo que va en el boleto. Además, en las copas europeas el modelo declara más empates de los que salen (22 % frente a 18 %), así que no hay motivo para pensar que los está infravalorando.

Las variantes con X quedan en la comparación de todas las jornadas: entrarán solas cuando la X sea competitiva, como en ligas con muchos empates o en partidos de selecciones.
