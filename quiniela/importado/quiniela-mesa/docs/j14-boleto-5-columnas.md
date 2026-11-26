# QUINIELA J14 — BOLETO DE 5 COLUMNAS

**Sábado 17 octubre 2026** · Presupuesto reducido · Reducción construida a mano

---

## Por qué no se puede usar el formato de 3 triples + 3 dobles

5 es número primo. La estructura de dobles y triples es multiplicativa: cada doble multiplica por 2 y cada triple por 3. Las combinaciones posibles son 2, 3, 4, 6, 8, 9, 12, 16, 18… **nunca 5.**

- 1 triple = 3 columnas
- 2 dobles = 4 columnas
- 1 triple + 1 doble = 6 columnas

Así que con 5 columnas hay que abandonar el formato habitual y construir una **reducción a mano**: 5 columnas elegidas una por una, optimizadas con búsqueda exhaustiva sobre la distribución exacta de aciertos.

---

## EL BOLETO — 5 columnas

| | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | **Pleno 15** |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **C1** | 2 | 1 | 2 | 2 | 1 | 2 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | **2** | **0-1** |
| **C2** | 2 | 1 | 2 | **X** | 1 | 2 | 1 | 1 | **2** | 1 | 1 | 1 | 1 | 1 | **0-0** |
| **C3** | 2 | 1 | 2 | 2 | 1 | 2 | 1 | 1 | **X** | **X** | 1 | 1 | 1 | 1 | **1-0** |
| **C4** | 2 | 1 | 2 | **1** | **X** | 2 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | **2** | **1-1** |
| **C5** | 2 | 1 | 2 | 2 | 1 | 2 | 1 | 1 | **2** | 1 | 1 | 1 | **X** | **X** | **0-2** |

### Los 8 signos que van iguales en las 5 columnas

Son los partidos con probabilidad más alta y análisis más sólido. Si uno de estos falla, caen las 5 columnas a la vez — es el riesgo asumido a cambio de concentrar la cobertura donde hay duda real.

| Nº | Partido | Signo | Prob. | Público |
|---|---|---|---|---|
| 1 | Espanyol – Atlético | **2** | 49% | 50% |
| 2 | Villarreal – Elche | **1** | 60% | 72% |
| 3 | Betis – Barcelona | **2** | 63% | 59% |
| 6 | Málaga – R. Sociedad | **2** | 47% | 55% |
| 7 | R. Madrid – Sevilla | **1** | 68% | 94% |
| 8 | Eibar – Mallorca | **1** | 45% | 48% |
| 11 | Athletic F – Valencia F | **1** | 73% | 63% |
| 12 | R. Madrid F – Espanyol F | **1** | 54% | 95% |

### Los 6 partidos donde se varía

| Nº | Partido | Reparto en las 5 columnas | Por qué |
|---|---|---|---|
| 4 | Valencia – Athletic | 2 ×3 · X ×1 · 1 ×1 | 33/31/36 — con el Athletic sin ataque es casi un triple natural |
| 5 | Celta – Alavés | 1 ×4 · X ×1 | Celta con 5 empates en 8 partidos |
| 9 | Las Palmas – Castellón | 2 ×2 · 1 ×2 · X ×1 | 36/29/35, el más abierto. Público al 2 (43%) |
| 10 | Burgos – Sabadell | 1 ×4 · X ×1 | 41/30/29, Segunda igualada |
| 13 | Eibar F – Deportivo F | 1 ×4 · X ×1 | Eibar F ultradefensivo (0.67 goles/partido) |
| 14 | Atlético F – Madrid CFF | 2 ×2 · 1 ×2 · X ×1 | **El 2 tiene ratio de valor 4.62** |

---

## Probabilidades del boleto

| Categoría | 5 columnas | 1 sola columna | Mejora |
|---|---|---|---|
| **14 aciertos** | **0.0137%** | 0.0041% | ×3.3 |
| **≥13** | **0.236%** | 0.067% | ×3.5 |
| **≥12** | **1.71%** | 0.52% | ×3.3 |
| **≥11** | **7.20%** | 2.45% | ×2.9 |
| **≥10** | **20.26%** | 8.14% | ×2.5 |

**Dónde está el premio realista:** con 5 columnas, 1 de cada 5 veces entra en la categoría de 10 aciertos y 1 de cada 14 llega a 11. El 14 es lotería pura (1 entre 7.300). El objetivo honesto de este boleto es la categoría de 10-11, no el bote.

---

## Pleno al 15 — cobertura del 66.1%

Esta es la gran ventaja de jugar 5 columnas: **cada columna lleva su propio Pleno**, así que se cubren los 5 resultados más probables en lugar de uno.

| Pleno | Columna | Prob. |
|---|---|---|
| 0-1 | C1 | 15.7% |
| 0-0 | C2 | 15.7% |
| 1-0 | C3 | 13.4% |
| 1-1 | C4 | 13.4% |
| 0-2 | C5 | 7.9% |
| | **Total** | **66.1%** |

Getafe–Rayo, xG ajustado 0.85–1.00. **Getafe ha marcado 4 goles en 8 partidos (0.50/partido)** y pierde a Uche (cruzado) con Ünal en duda. La probabilidad de que Getafe no marque es del **42.7%**: por eso tres de los cinco Plenos empiezan por 0.

El Pleno más probable va asignado a la columna con mayor P(14), que es la que más posibilidades tiene de necesitarlo.

---

## Decisión de diseño: valor parimutuel

El optimizador puro daba P(≥12)=1.79% con un multiplicador de pago de 1.9x. Forzar el **2 de P14 (Atlético F – Madrid CFF) en dos columnas** cambia el balance:

| Variante | P(≥12) | P(≥11) | Multiplicador de pago |
|---|---|---|---|
| Óptimo puro | 1.79% | 7.46% | 1.9x |
| **Elegida (P14=2 ×2)** | **1.71%** | **7.20%** | **3.3x** |
| P14=2 ×3 | 1.67% | 7.01% | 3.9x |

Se pierde un 4% relativo de probabilidad y se gana un 74% de multiplicador. Merece la pena: Madrid CFF es **2º de la Liga F con 13 puntos** y el Atlético F es **6º con 9**, pero el público juega el 73% al Atlético por el nombre. Si entra ese 2, hay muy poca gente compartiendo el premio.

---

## Advertencia

Con 5 columnas no hay forma de acercarse a los 14 aciertos. La probabilidad es del 0.0137% — una entre 7.300. Lo que este boleto sí hace es triplicar la cobertura de las categorías bajas respecto a jugar una sola columna, y cubrir dos tercios del Pleno. Es el mejor uso posible de 5 columnas, no un boleto ganador.
