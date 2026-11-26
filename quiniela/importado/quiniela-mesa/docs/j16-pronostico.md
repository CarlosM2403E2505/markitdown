# QUINIELA J16 — PRONÓSTICO (reducida 7 dobles al 13) · revisado 23/10

24–26 octubre 2026 · Preparado el miércoles 21/10 · **Cierre: sábado 24 a las 14:00 peninsular (13:00 Canarias)**

Sistema acordado a partir de esta jornada: **reducida de 7 dobles al 13, 16 apuestas (12 €)**.

---

## 1. Por qué Loterías ha elegido estos partidos

| Bloque | Partidos | Lectura |
|---|---|---|
| Primera (7 + Pleno) | 8 de los 10 de la jornada 10 | Fuera quedan los de Espanyol, Alavés, Málaga y Racing, los de menos tirón (y probablemente el del viernes, que no cabe porque la validación cierra el sábado). Entra un partido del **lunes** (Sevilla–Osasuna) |
| Segunda (3) | Leganés–Mallorca, Almería–Oviedo, Sabadell–Tenerife | Equipos con nombre de Primera reciente (Mallorca, Oviedo, Leganés, Almería, líder) |
| Liga F (4) | Logroño–Badalona, Dépor–Alavés, Eibar–Madrid CFF, Real Madrid–Tenerife | **El Barça femenino tampoco está, como en la J14 (2 de 2)**: Loterías evita el partido casi seguro (el Barça va 29-4 en goles) |
| Pleno | Barcelona–Real Madrid | El partido estrella, último del domingo |

**Lo más importante: es la jornada más abierta que hemos analizado.** Solo un partido pasa del 65% (Atlético). En la J15 había 3 y en la J14, 2. Jornada de pocas quinielas de 14 y posible bote.

## 2. Lo aprendido que se aplica (medido, no opinado)

1. **Empates en liga ×1.08** (lección J14 y J15): el modelo se quedaba corto de empates en ligas nacionales.
2. **NUEVO: ventaja de campo propia de Primera.** El modelo europeo usaba una ventaja de campo común; en Primera es mayor (los locales marcan 1.60 frente a 1.16). Corrigiéndolo, el log-loss sobre 437 partidos de Primera no vistos baja de 0.9725 a 0.9632. En Segunda no mejora y no se aplica. Explica por qué el modelo daba menos a los locales que el mercado.
3. **Ajustes por bajas con tope del 5%** (lección Oporto–PSV).
4. **Liga F sin el efecto Barça:** se descuentan los partidos contra el Barcelona (7-0 al Real Madrid, 5-0 al Tenerife…) para no deformar las defensas.
5. **Datos completados:** Primera 2026/27 hasta la jornada 9 (88 partidos), **Segunda 2026/27 completa (110 partidos, 10 jornadas)**, Liga F con la tabla de 7 jornadas + temporada 2025/26 como base.

## 3. Probabilidades (modelo propio, sin cuotas) y control de mercado

| Nº | Partido | 1 | X | 2 | Mercado (APU) | Público Q15 |
|---|---|---|---|---|---|---|
| 1 | Rayo – Elche | 48.6 | 26.8 | 24.6 | 53/25/21 | 65/19/15 |
| 2 | Valencia – Villarreal | 36.1 | 25.9 | 38.0 | 29/27/44 | 20/32/47 |
| 3 | Atlético – Deportivo | **67.9** | 19.0 | 13.1 | 74/17/10 | 83/10/7 |
| 4 | Athletic – Getafe | 48.2 | 31.0 | 20.8 | 57/25/18 | 71/20/10 |
| 5 | Celta – Betis | 43.1 | 25.9 | 31.0 | 35/28/37 | 11/28/61 |
| 6 | Real Sociedad – Levante | 50.3 | 23.6 | 26.1 | 55/24/21 | 78/13/9 |
| 7 | Sevilla – Osasuna | 47.4 | 25.9 | 26.7 | 49/28/23 | 68/20/12 |
| 8 | Leganés – Mallorca | 25.4 | 30.0 | 44.7 | 30/30/39 | 16/25/59 |
| 9 | Almería – Oviedo | 45.4 | 26.8 | 27.9 | 55/25/20 | 74/16/10 |
| 10 | Sabadell – Tenerife | 45.8 | 29.5 | 24.6 | 49/30/21 | 63/22/15 |
| 11 | Logroño F – Badalona F | 40.2 | 29.5 | 30.2 | — | 41/35/24 |
| 12 | Deportivo F – Alavés F | 41.7 | 32.0 | 26.2 | — | 64/26/10 |
| 13 | Eibar F – Madrid CFF | 34.2 | 30.5 | 35.3 | — | 20/38/42 |
| 14 | Real Madrid F – Tenerife F | 50.2 | 27.6 | 22.2 | — | 83/8/9 |
| 15 | Barcelona – Real Madrid | 60.2 | 19.0 | 20.8 | | |

Ajustes del Live Trader (tope 5%): Celta, Real Sociedad y Getafe jugaron el jueves en Europa (−4% a su ataque, +2% al rival). Clásico: Vinícius sancionado (Madrid −3%), Olmo lesionado (Barça −2%); Koundé duda.

Discrepancias con el mercado:
- **Celta–Betis**: el modelo ve al Celta (43%), el mercado al Betis (37%) y el público se vuelca al Betis (61%). Va de doble 12.
- **Almería–Oviedo**: modelo 45% al 1, mercado 55%. El Almería es líder de Segunda; el modelo pesa su temporada pasada. Va de sencillo: riesgo.
- **Real Madrid F**: el público lo juega al 83%; el modelo lo deja en 50% (Tenerife fue 4º la temporada pasada). El modelo de Liga F no tiene backtest: dato menos fiable.

---

## 4. BOLETO — reducida 7 dobles al 13 (16 apuestas) · REVISADO 23/10

Cambio respecto a la versión del 21/10: la Liga F tenía los empates inflados (el modelo daba 25–32% y en la Liga F real 2025/26 hubo un 20.8%; en los 16 partidos de Liga F que ha metido Loterías esta temporada solo hubo 1 empate). Calibrado a 20.8% → **Athletic–Getafe pasa a doble 1X** y **Deportivo F–Alavés F pasa a sencillo 1**.

| Nº | Partido | Tipo | Signo |
|---|---|---|---|
| 1 | Rayo – Elche | sencillo | **1** |
| 2 | Valencia – Villarreal | doble | **12** |
| 3 | Atlético – Deportivo | sencillo | **1** |
| 4 | Athletic – Getafe | doble | **1X** |
| 5 | Celta – Betis | doble | **12** |
| 6 | Real Sociedad – Levante | sencillo | **1** |
| 7 | Sevilla – Osasuna | sencillo | **1** |
| 8 | Leganés – Mallorca | doble | **X2** |
| 9 | Almería – Oviedo | sencillo | **1** |
| 10 | Sabadell – Tenerife | doble | **1X** |
| 11 | Logroño F – Badalona F | doble | **12** |
| 12 | Deportivo F – Alavés F | sencillo | **1** |
| 13 | Eibar F – Madrid CFF | doble | **12** |
| 14 | Real Madrid F – Tenerife F | sencillo | **1** |
| 15 | **Barcelona – Real Madrid** | Pleno | **M-1** |

### Las 16 columnas

| | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | P15 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| C1 | 1 | 2 | 1 | 1 | 1 | 1 | 1 | 2 | 1 | 1 | 1 | 1 | 2 | 1 | M-1 |
| C2 | 1 | 2 | 1 | 1 | 1 | 1 | 1 | X | 1 | X | 2 | 1 | 1 | 1 | M-1 |
| C3 | 1 | 2 | 1 | 1 | 2 | 1 | 1 | 2 | 1 | 1 | 2 | 1 | 1 | 1 | M-1 |
| C4 | 1 | 2 | 1 | 1 | 2 | 1 | 1 | X | 1 | X | 1 | 1 | 2 | 1 | M-1 |
| C5 | 1 | 2 | 1 | X | 1 | 1 | 1 | 2 | 1 | X | 1 | 1 | 1 | 1 | M-1 |
| C6 | 1 | 2 | 1 | X | 1 | 1 | 1 | X | 1 | 1 | 2 | 1 | 2 | 1 | M-1 |
| C7 | 1 | 2 | 1 | X | 2 | 1 | 1 | 2 | 1 | X | 2 | 1 | 2 | 1 | M-1 |
| C8 | 1 | 2 | 1 | X | 2 | 1 | 1 | X | 1 | 1 | 1 | 1 | 1 | 1 | M-1 |
| C9 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 2 | 1 | X | 2 | 1 | 2 | 1 | M-1 |
| C10 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | X | 1 | 1 | 1 | 1 | 1 | 1 | M-1 |
| C11 | 1 | 1 | 1 | 1 | 2 | 1 | 1 | 2 | 1 | X | 1 | 1 | 1 | 1 | M-1 |
| C12 | 1 | 1 | 1 | 1 | 2 | 1 | 1 | X | 1 | 1 | 2 | 1 | 2 | 1 | M-1 |
| C13 | 1 | 1 | 1 | X | 1 | 1 | 1 | 2 | 1 | 1 | 2 | 1 | 1 | 1 | M-1 |
| C14 | 1 | 1 | 1 | X | 1 | 1 | 1 | X | 1 | X | 1 | 1 | 2 | 1 | M-1 |
| C15 | 1 | 1 | 1 | X | 2 | 1 | 1 | 2 | 1 | 1 | 1 | 1 | 2 | 1 | M-1 |
| C16 | 1 | 1 | 1 | X | 2 | 1 | 1 | X | 1 | X | 2 | 1 | 1 | 1 | M-1 |

**Probabilidades exactas:** ≥14 0.015% · ≥13 0.29% · ≥12 2.1% · ≥11 8.6% · ≥10 23.4%

## 5. LOS 14 SIGNOS INDIVIDUALES

1 · 2 · 1 · 1 · 1 · 1 · 1 · 2 · 1 · 1 · 1 · 1 · 2 · 1 · **Pleno M-1**

## 6. PLENO AL 15 — Barcelona – Real Madrid: **M-1**

| Pleno | Prob. |
|---|---|
| **M-1** | **14.1%** |
| M-2 | 10.6% |
| M-0 | 9.7% |
| M-M | 8.4% |
| 2-1 | 8.2% |
| 1-1 | 7.6% |

xG 2.63–1.54: Barça en casa con su ataque (21 goles en 5 primeras jornadas, 3-0 al Getafe, 5-2 al Betis) contra un Madrid sin Vinícius. La comunidad de Quiniela15 también va al M-1 (23%), así que no es un pleno de valor: es el de más probabilidad, con 3.5 puntos de ventaja. Revisar los % de Loterías el viernes.

## 7. Risk Analyst

- **Solo un sencillo pasa del 65% (Atlético).** Los otros 6 sencillos están entre 45% y 50%: se esperan ~3.4 fallos entre los sencillos. Hacer 14 es lotería (1 entre ~8.000).
- **Liga F** (4 partidos, 3 de ellos dobles): modelo por tablas, sin backtest.
- **Sabadell** solo tiene 10 partidos en los datos.
- **Pendiente antes del cierre:** bajas definitivas, porcentajes de Loterías (LAE) y la confirmación de Koundé.


---

## 8. REVISIÓN CON EL PROMPT MAESTRO (23/10 noche) — BOLETO RECOMENDADO

Porcentajes oficiales del público (LAE) ya publicados. El público va muy cargado a favoritos que el modelo ve mucho más flojos:

| Partido | Público | Modelo | Lectura |
|---|---|---|---|
| Real Madrid F – Tenerife F | 87% al 1 | 53% | El 2 vale ×4.7 |
| Real Sociedad – Levante | 79% al 1 | 50% | El 2 vale ×3.3 |
| Almería – Oviedo | 72% al 1 | 45% | El 2 vale ×2.8 |
| Athletic – Getafe | 69% al 1 | 48% | La X vale ×1.4 |
| Celta – Betis | 21% al 1 | 43% | **El 1 vale ×2.05** |

**Red Team:** el boleto que maximiza P(14) se parece demasiado al del público. Variante elegida: entre todos los boletos con al menos el 90% de la P(14) máxima, el de más valor (premio esperado relativo).

| | Óptimo P(14) | **Red Team (recomendado)** |
|---|---|---|
| P(14) | 0.0146% | 0.0135% (−8%) |
| P(≥12) | 2.09% | 1.98% |
| P(≥10) | 23.4% | 22.7% |
| Índice de valor (premio esperado relativo) | 2.10 | **17.84 (×8.5)** |

Cambios: **Celta–Betis pasa a sencillo 1** (el público lo juega al 21%, el modelo 43%); **Almería–Oviedo pasa a doble 12** y **Deportivo F–Alavés F a doble 12**; **Sabadell–Tenerife pasa a sencillo 1**.

| Nº | Partido | Signo |
|---|---|---|
| 1 | Rayo – Elche | 1 |
| 2 | Valencia – Villarreal | **12** |
| 3 | Atlético – Deportivo | 1 |
| 4 | Athletic – Getafe | **1X** |
| 5 | Celta – Betis | 1 ⚠️ |
| 6 | Real Sociedad – Levante | 1 ⚠️ |
| 7 | Sevilla – Osasuna | 1 ⚠️ |
| 8 | Leganés – Mallorca | **X2** |
| 9 | Almería – Oviedo | **12** |
| 10 | Sabadell – Tenerife | 1 ⚠️ |
| 11 | Logroño F – Badalona F | **12** |
| 12 | Deportivo F – Alavés F | **12** |
| 13 | Eibar F – Madrid CFF | **12** |
| 14 | Real Madrid F – Tenerife F | 1 ⚠️ |
| 15 | Barcelona – Real Madrid | **M-1** |

| | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | P15 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| C1 | 1 | 2 | 1 | 1 | 1 | 1 | 1 | 2 | 1 | 1 | 2 | 1 | 2 | 1 | M-1 |
| C2 | 1 | 2 | 1 | 1 | 1 | 1 | 1 | 2 | 2 | 1 | 1 | 2 | 1 | 1 | M-1 |
| C3 | 1 | 2 | 1 | 1 | 1 | 1 | 1 | X | 1 | 1 | 2 | 2 | 1 | 1 | M-1 |
| C4 | 1 | 2 | 1 | 1 | 1 | 1 | 1 | X | 2 | 1 | 1 | 1 | 2 | 1 | M-1 |
| C5 | 1 | 2 | 1 | X | 1 | 1 | 1 | 2 | 1 | 1 | 1 | 1 | 1 | 1 | M-1 |
| C6 | 1 | 2 | 1 | X | 1 | 1 | 1 | 2 | 2 | 1 | 2 | 2 | 2 | 1 | M-1 |
| C7 | 1 | 2 | 1 | X | 1 | 1 | 1 | X | 1 | 1 | 1 | 2 | 2 | 1 | M-1 |
| C8 | 1 | 2 | 1 | X | 1 | 1 | 1 | X | 2 | 1 | 2 | 1 | 1 | 1 | M-1 |
| C9 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 2 | 1 | 1 | 1 | 2 | 2 | 1 | M-1 |
| C10 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 2 | 2 | 1 | 2 | 1 | 1 | 1 | M-1 |
| C11 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | X | 1 | 1 | 1 | 1 | 1 | 1 | M-1 |
| C12 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | X | 2 | 1 | 2 | 2 | 2 | 1 | M-1 |
| C13 | 1 | 1 | 1 | X | 1 | 1 | 1 | 2 | 1 | 1 | 2 | 2 | 1 | 1 | M-1 |
| C14 | 1 | 1 | 1 | X | 1 | 1 | 1 | 2 | 2 | 1 | 1 | 1 | 2 | 1 | M-1 |
| C15 | 1 | 1 | 1 | X | 1 | 1 | 1 | X | 1 | 1 | 2 | 1 | 2 | 1 | M-1 |
| C16 | 1 | 1 | 1 | X | 1 | 1 | 1 | X | 2 | 1 | 1 | 2 | 1 | 1 | M-1 |

Pleno: M-1 (14.1%) se mantiene por probabilidad. El público lo juega ~18% (sobrejugado). Alternativa de valor: **M-0** (9.7% modelo, ~3.6% público, valor ×2.7).

Sistema: 4 dobles completos daría P(14) 0.026% (×1.7) pero menos en 10–12; se mantiene la reducida por decisión del usuario.

J15 final oficial: 4 acertantes de 14 (45.666 €), 0 de Pleno. Nuestra mejor columna: 9.

---

## 9. ANÁLISIS FINAL (sábado 24/10, antes del cierre): árbitros, entrenadores y enfrentamientos

Veredicto: **sin cambios en el boleto recomendado (sección 8).**

- **Clásico:** árbitro Martínez Munuera, VAR Iglesias Villanueva. En sus 4 Clásicos: 3 victorias del Madrid y 1 del Barça. Muestra de 4 partidos: no se ajusta nada.
- **Celta–Betis:** el Celta ganó 5 de los últimos 8 contra el Betis; el Betis perdió sus últimas 3 visitas a Balaídos; Pellegrini perdió sus últimas 3 visitas allí (incluida la única contra Giráldez, 3-2). Aspas: 9 goles en 18 partidos contra el Betis. Refuerza el **1 del Celta**. Ojo: el Celta perdió sus 2 últimos partidos en casa y el Betis marca en sus últimas 10 salidas.
- **Real Sociedad–Levante:** el Levante no gana en Anoeta desde octubre de 2019; la Real suma 12 de los últimos 15 puntos. Bajas de la Real: Aramburu, Yangel Herrera, Odriozola, Beitia. Refuerza el 1.
- **Rayo–Elche:** el Rayo ganó el último (1-0, abril 2026); el Elche es 18º y sin Marc Aguado. **El Rayo pierde a su portero Batalla** y a Luiz Felipe: riesgo para el 1 (49%).
- **Sevilla–Osasuna:** cara a cara cerrado: 1 victoria del Sevilla, 2 de Osasuna y 3 empates en los últimos 6, todos con 2 goles o menos. Riesgo de X para el 1 del Sevilla (47%). No se cambia: seis partidos son poca muestra (lección Oporto–PSV).
