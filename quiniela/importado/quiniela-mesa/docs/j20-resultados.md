# J20 — RESULTADOS Y POST-MORTEM (7–8 de noviembre de 2026)

## 1. Resultados frente al boleto definitivo (v3, con 2 X)
| Nº | Partido | Resultado | Signo | Mesa (P del signo real) | Mercado | Público | Boleto 1 | Boleto 2 |
|---|---|---|---|---|---|---|---|---|
| 1 | Málaga – Racing | 1-2 | 2 | 29,3% | 33,9% | 28,6% | 1 ❌ | 1 ❌ |
| 2 | Osasuna – Athletic | 1-1 | **X** | 31,6% | 27,8% | 40,2% | 12 ❌ | **X ✅** |
| 3 | Valencia – Real Madrid | 0-3 | 2 | 61,1% | 72,5% | 89,4% | 2 ✅ | 2 ✅ |
| 4 | Elche – Betis | 0-2 | 2 | 37,7% | 45,2% | 59,0% | 12 ✅ | 12 ✅ |
| 5 | Real Sociedad – Rayo | 1-0 | 1 | 57,7% | 56,3% | 79,6% | 1 ✅ | 1 ✅ |
| 6 | Celta – Levante | 0-0 | **X** | 23,9% | 25,2% | 24,0% | 1 ❌ | 1 ❌ |
| 7 | Villarreal – Getafe | 2-0 | 1 | 57,5% | 65,8% | 81,0% | 1 ✅ | 1 ✅ |
| 8 | Cádiz – Oviedo | 1-2 | 2 | 42,1% | 35,2% | 46,5% | X2 ✅ | X2 ✅ |
| 9 | Girona – Almería | 0-1 | 2 | 25,1% | 27,9% | 27,5% | 1 ❌ | 1 ❌ |
| 10 | Sporting – Valladolid | 1-2 | 2 | 23,1% | 30,3% | 8,0% | 1 ❌ | 1 ❌ |
| 11 | Athletic F – Real Madrid F | 1-1 (0-1 en el 85', 1-1 en el 92') | **X** | 17,1% | 27,0% | 22,0% | 2 ❌ | 2 ❌ |
| 12 | Logroño F – Sevilla F | 2-2 | **X** | 26,7% | 27,0% | 26,1% | 12 ❌ | 12 ❌ |
| 13 | Eibar F – Real Sociedad F | 1-2 (autogol en el 95') | 2 | 39,8% | 49,0% | 52,8% | 2 ✅ | 2 ✅ |
| 14 | Tenerife F – Alavés F | **Aplazado** (luto por Jesús de Miguel). Signo por sorteo ponderado de LAE: la prensa da **1**; falta el acta oficial | (1) | 63,3% | — | LAE 77% | 1 | 1 |
| 15 | Pleno: Atlético – Barcelona | **1-2** | — | — | — | — | 1-1 ❌ | 1-1 ❌ |

Combinación: 2 X 2 2 1 X 1 2 2 2 X X 2 (1) · Pleno 1-2.

**Mejor columna: boleto 1, 7 aciertos; boleto 2, 8 aciertos** (contando el 1 del P14). **Sin premio.**

Fuentes:
- P1–P7 y Pleno: SportRadar.
- Combinación, P9, P10 y premios: [El Periódico de Ceuta](https://www.elperiodicodeceuta.es/resultado-la-quiniela-jornada-20-2026-27/) y [Quiniela15](https://www.quiniela15.com/resultados-quiniela).
- P8: [Infobae/EFE](https://www.infobae.com/espana/agencias/2026/11/07/1-2-el-oviedo-impone-su-superioridad-en-cadiz/).
- P11: [Real Madrid](https://www.realmadrid.com/es-ES/noticias/futbol/primer-equipo-femenino/cronicas/cronica-athletic-club-real-madrid-07-11-2026).
- P12: [Infobae/EFE](https://www.infobae.com/espana/agencias/2026/11/08/2-2-dos-errores-de-las-porteras-llevan-al-reparto-de-puntos-entre-logrono-y-sevilla/).
- P13: [Las Futbolistas](https://lasfutbolistas.com/cronica-sd-eibar-1-2-real-sociedad-autogol-95-derbi-guipuzcoano/).

## 2. Escrutinio (jornada de sorpresas)
| Categoría | Acertantes | Premio |
|---|---|---|
| Pleno al 15 | 1 | 1.647.986,55 € |
| 14 | 6 | 90.099,00 € |
| 13 | 185 | 1.369,75 € |
| 12 | 2.301 | 110,13 € |
| 11 | 17.496 | 14,48 € |
| **10** | 89.116 | **3,41 €** |

**Corrección importante:** esta jornada **10 aciertos sí cobró (3,41 €)**. La regla de la J18 ("10 no cobra") salía de 4 jornadas con pocas sorpresas, en las que el premio del 10 quedó por debajo de 1,50 € y pasó al bote. Lo correcto: **el 10 cobra solo en jornadas con muchas sorpresas**, que es justo cuando nuestros boletos aciertan menos. Por eso P(≥10) sigue sin decidir el boleto, pero ya no se puede decir que "10 nunca cobra".

## 3. Cómo predijo cada uno (13 partidos jugados)
| Fuente | Log-loss | Favorito acertado |
|---|---|---|
| Mesa | **1,085** | 6 de 13 |
| Mercado | **0,976** | 6 de 13 |
| Público (LAE) | 0,980 | 6 de 13 |

- **Es la jornada con más sorpresas de la temporada:** el favorito de todos (mesa, mercado y público) solo acertó 6 de 13. Perdieron Málaga, Girona y Sporting en casa, y el Celta empató.
- **El mercado vuelve a predecir mejor que la mesa.** La mesa era menos optimista que el mercado con los favoritos que sí ganaron: P3, P4, P7 y P13.
- La mesa solo superó al mercado en P2 (la X) y P8 (el 2).

## 4. Empates
| Medida | J20 |
|---|---|
| X esperadas por la mesa (13 partidos) | 3,26 |
| X reales | **4** (P2, P6, P11 y P12) |
| X cubiertas | **1**: la del P2, solo en el boleto 2 (cambio de la v3, pedido por el usuario) |

- **P12 (37 · 27 · 36):** otra vez una X que era el tercer signo de un partido igualado. Se dobló 12, y es exactamente el fallo del estudio del 4/11.
- **P6 (57 · 24 · 19):** el 1 era fijo y por debajo del 65%. El X del mercado también estaba en el 25%.
- **P11:** la mesa daba la X como lo menos probable (17%), frente al 27% del mercado. El empate llegó en el 92'.
- **Acumulado J14–J20:** 18 X reales, 3 cubiertas (17%).
- **La v3 sí sirvió:** sin la X del P2, el boleto 2 habría hecho 7.

## 5. Sueltas: 3 de 5 (se esperaban 4,3)
| Suelta | Resultado |
|---|---|
| Real Madrid marca | ✅ (0-3) |
| Real Sociedad marca | ✅ (1-0) |
| Málaga – Racing: más de 1,5 goles | ✅ (1-2) |
| Celta marca | ❌ (0-0) |
| Girona marca | ❌ (0-1) |

## 6. Lecciones para la J21
| # | Lección | Qué cambia |
|---|---|---|
| 1 | Las X siguen escapándose como tercer signo en los partidos igualados (P12) | **Decisión del usuario (10/11): el mínimo de 2 X NO es obligatorio; lo decide la mesa con los números.** En todo partido igualado (P1−P2 < 0,15), el doble se elige entre 12, 1X y X2 con una decisión escrita y su coste |
| 2 | El mercado predice mejor: 3 jornadas seguidas (J18, J19 y J20) | **Decisión del usuario (10/11): se mantiene la regla actual.** Las cuotas son solo control; con 7 puntos o más de diferencia, revisión escrita y cobertura del signo del mercado si la causa está en el modelo |
| 3 | Aplazamiento no visto (P14) | Ya está en la lista de control: los aplazamientos se comprueban el día del sellado |
| 4 | "10 no cobra" era una generalización | Corregido en el registro de errores (R4) |
| 5 | Descansos | Análisis paralizado por el usuario el 7/11. Lo registrado se queda como dato |

## 7. Libro de banca
| Jornada | Coste | ¿Sellado? | Mejor columna | Premio |
|---|---|---|---|---|
| J19 | 18 € | Sí (confirmado el 10/11) | 10 | 0 € |
| J20 | 18 € | **Sí** (confirmado el 10/11) | 8 | 0 € |
| **Total J19–J20** | **36 €** | | | **0 €** |
