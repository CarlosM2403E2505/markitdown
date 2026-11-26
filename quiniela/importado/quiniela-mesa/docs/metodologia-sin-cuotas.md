# QUINIELA NIVEL SUPREMO — CAMBIO DE METODOLOGÍA

**17 octubre 2026** · Por qué dejamos de usar las cuotas como entrada y qué las sustituye

---

## 1. El marcador de hoy

| Nº | Partido | Resultado | Signo real | Nuestro signo | |
|---|---|---|---|---|---|
| 1 | Espanyol – Atlético | 0-1 | 2 | 2 fijo | ✅ |
| 2 | Villarreal – Elche | **0-0** | **X** | 1 fijo (60%) | ❌ |
| 3 | Betis – Barcelona | 2-5 | 2 | 2 fijo | ✅ |
| 4 | Valencia – Athletic | **0-0** | **X** | triple / **X** individual | ✅ |
| 8 | Eibar – Mallorca | **1-1** | **X** | 1 fijo (45%) | ❌ |
| 9 | Las Palmas – Castellón | 0-3 | 2 | triple | ✅ |
| 11 | Athletic F – Valencia F | 1-0 | 1 | 1 fijo | ✅ |
| 12 | R. Madrid F – Espanyol F | 3-1 | 1 | 1 fijo | ✅ |

**6 de 8.** Quedan P5, P6, P7, P10, P13, P14 el domingo y el Pleno el lunes.

En el boleto de 5 columnas, **C2 va 6/8** y es la única que acertó P4 y P9 a la vez.

---

## 2. El dato que lo explica todo

**5 de los 8 partidos de hoy acabaron en 0-0, 0-1, 1-0 o 1-1.**

| Partido | Marcador |
|---|---|
| Espanyol – Atlético | **0-1** |
| Villarreal – Elche | **0-0** |
| Valencia – Athletic | **0-0** |
| Eibar – Mallorca | **1-1** |
| Athletic F – Valencia F | **1-0** |

Esas cuatro casillas exactas —0-0, 0-1, 1-0, 1-1— son precisamente las que el modelo de Poisson simple **infraestima de forma sistemática**, y las que el modelo Dixon-Coles corrige con un parámetro dedicado (ρ). Nuestro modelo actual usa Poisson simple mezclado con cuotas. Por construcción, estaba ciego a lo que pasó hoy.

---

## 3. Pero el modelo NO falló. El error fue llamar "fijo" a lo que no lo era

Esta es la parte incómoda. Los números de nuestros propios 8 fijos eran:

| Fijo | Probabilidad |
|---|---|
| P1 Espanyol – Atlético | 49% |
| P2 Villarreal – Elche | 60% |
| P3 Betis – Barcelona | 63% |
| P6 Málaga – R. Sociedad | 47% |
| P7 R. Madrid – Sevilla | 68% |
| P8 Eibar – Mallorca | 45% |
| P11 Athletic F – Valencia F | 73% |
| P12 R. Madrid F – Espanyol F | 54% |

- **P(los 8 correctos) = 1.05%**
- **Fallos esperados entre los 8 = 3.41**
- De los 6 ya jugados: fallos esperados 2.56, **fallos reales 2**

**El modelo estuvo bien calibrado. Acertó incluso un poco por encima de lo previsto.** El problema es de lenguaje y de diseño: llamamos "fijo" a un signo del 45%, que falla más veces de las que acierta, y a uno del 60%, que falla 2 de cada 5 veces.

### La aritmética que mata la Quiniela

| Estructura | P(todos correctos) |
|---|---|
| 4 fijos al 70% | 24.0% |
| 6 fijos al 70% | 11.8% |
| 8 fijos al 70% | 5.8% |
| **8 fijos al 60%** | **1.7%** |
| 8 fijos al 55% | 0.8% |
| 10 fijos al 75% | 5.6% |

Villarreal al 60% no fue una sorpresa. Fue el 40% haciendo su trabajo. Bayern al 87% y el Inter al 73% en la J13 tampoco fueron sorpresas: eran el 13% y el 27%.

---

## 4. Quién fija las cuotas: los perfiles de una casa de apuestas

Tenías razón en que hay profesionales detrás. Esto es lo que hacen:

### Los que tocan las cuotas

**Odds compiler / Trader de cuotas.** Es quien fija los precios. Según la descripción del puesto, sus funciones son: fijar las cuotas, **supervisar las cuentas de los clientes y la rentabilidad del negocio**, vigilar la posición financiera de la casa y ajustar las cuotas si hace falta, y ser consultado antes de aceptar apuestas muy grandes para evitar pasivos excesivos. Perfil matemático; su remuneración depende de sus habilidades numéricas.

**Sports Trader.** Ajusta las cuotas según tendencias del mercado, **actividad de los apostantes** y modelos estadísticos, y reacciona a los movimientos de la competencia. Muchos vienen de finanzas o análisis cuantitativo.

**Live Trader.** Ajusta cuotas en tiempo real durante el partido. Decisiones en segundos.

### Los que protegen el dinero

**Risk Analyst.** Monitoriza la actividad de apuestas, **detecta patrones inusuales y apostantes profesionales**, y ajusta la exposición. SQL/Python, perfil de finanzas, ciberseguridad o compliance. Este es literalmente el puesto cuyo trabajo es que tú no ganes de forma sostenida: si detecta que ganas, te limitan la cuenta.

**Data Analyst / Quant.** Modelado estadístico, comportamiento de clientes, métricas. Camino hacia machine learning y modelado predictivo.

**Software developers.** Construyen los algoritmos de cuotas y el procesamiento en tiempo real.

### La frase clave

De la descripción del oficio de odds compiler:

> *"Si una selección recibe mucho volumen de dinero, puede reducir su cuota."*

Ahí está todo. **La cuota se mueve por el DINERO, no por información nueva sobre los equipos.**

---

## 5. Por qué una cuota no es una probabilidad

Una cuota es un **precio**, no un pronóstico. Se fija para tres objetivos a la vez, y solo uno de ellos es acertar:

1. **Equilibrar el libro.** La casa quiere dinero repartido en los tres signos para cobrar el margen sin riesgo, pase lo que pase.
2. **Extraer margen (overround).** La suma de las probabilidades implícitas da 105-108%, no 100%. Ese 5-8% es la comisión.
3. **Reaccionar al flujo de dinero.** Si el público carga un signo, la cuota baja aunque no haya cambiado nada en el campo.

Consecuencia directa: cuando el Villarreal recibe en casa a un recién ascendido, el público carga el 1. La cuota baja a 1.52. Nosotros la convertimos en "61% de probabilidad". Pero parte de esa cortedad **no era información, era dinero del público**.

### Y para la Quiniela es peor todavía

La Quiniela es **parimutuel**: el bote se reparte entre los acertantes. Seguir la cuota es seguir a la multitud, y la multitud es exactamente con quien vas a tener que repartir el premio. En la J14 el público jugaba el 94% al Real Madrid y el 95% al Real Madrid Femenino. Acertar eso no te hace ganar dinero: te mete en la cola de reparto.

---

## 6. Lo que SÍ hacemos y lo que NO — con honestidad

Tu instrucción es correcta en el fondo, pero **ejecutarla hoy tal cual nos haría perder, no ganar.** Y tengo la prueba numérica.

He construido el motor Dixon-Coles que estima fuerza de ataque y defensa directamente de los goles reales, sin tocar una sola cuota. Lo he validado sobre ligas sintéticas donde conozco la verdad. Esto es lo que recupera según el tamaño de la muestra:

| Partidos en la muestra | Correlación ataque | Correlación defensa | Ventaja de campo (real 0.26) |
|---|---|---|---|
| **90** (≈ lo que llevamos esta temporada) | **0.55** | 0.75 | **−0.03** ❌ |
| 220 | 0.72 | 0.79 | 0.23 |
| 1.100 | 0.97 | 0.94 | 0.26 ✅ |
| 4.400 | 0.99 | 0.98 | 0.25 ✅ |

Con las 9 jornadas que lleva LaLiga, un modelo puro de goles **estima la ventaja de campo con el signo cambiado** y solo correlaciona 0.55 con la fuerza real de ataque. Sería peor que las cuotas, no mejor.

**La solución no es tirar las cuotas. Es alimentar el modelo con suficientes datos para que se sostenga solo:**

- Temporada 2025/26 completa + 2026/27 en curso = ~1.100 partidos → correlación 0.97
- Ponderación temporal (ξ) para que lo reciente pese más
- Encogimiento (ridge) para no sobreajustar a los recién ascendidos

En ese régimen el modelo **sí** es una fuente independiente y las cuotas pasan a ser lo que deben ser: un control de sanidad, no la entrada.

---

## 7. El motor nuevo

`dixon_coles.py` — ya construido y validado. Características:

- **No acepta cuotas como entrada.** Solo goles reales, equipos y fechas.
- Estima ataque y defensa por equipo, ventaja de campo y ρ por máxima verosimilitud.
- **Corrección ρ de marcadores bajos** (0-0, 0-1, 1-0, 1-1): justo lo que falló hoy.
- Ponderación temporal exponencial.
- Encogimiento hacia la media de la liga, imprescindible con pocas jornadas.
- Salida: probabilidades 1X2, xG de cada equipo y distribución completa del Pleno en categorías 0/1/2/M.
- Autotest incluido que valida la consistencia del estimador.

---

## 8. Reglas nuevas, que sustituyen a las de la J13

| # | Regla | Origen |
|---|---|---|
| **1** | **Ningún signo por debajo del 65% se llama "fijo".** Entre 50-65% es "signo único por presupuesto", que es otra cosa. | Villarreal 60%, Eibar 45% |
| **2** | **Máximo 6 signos únicos por boleto.** Con 8 al 55% de media, P(todos) = 0.8%. | Aritmética del punto 3 |
| **3** | **Las cuotas no entran en el modelo.** Se registran aparte y solo se usan para detectar dónde discrepamos y por qué. | Punto 5 |
| **4** | **El % del público se usa invertido**: para decidir dónde NO ir, no dónde ir. | Parimutuel |
| **5** | **Los marcadores bajos se modelan con ρ, nunca con Poisson simple.** | 5 de 8 partidos hoy |
| **6** | **Una baja confirmada de la unidad ofensiva titular pesa más que cualquier cuota.** | P4: predijimos X, salió 0-0 |
| **7** | **El modelo se ajusta sobre 2 temporadas, no sobre la actual.** Con 90 partidos la ventaja de campo sale con el signo cambiado. | Punto 6 |

---

## 9. Lo que hay que hacer para la J15

1. Recolectar los resultados completos de LaLiga, Hypermotion y Liga F de la temporada 2025/26 y de la 2026/27 hasta hoy. Es la tarea pesada y es la que desbloquea todo.
2. Ajustar el motor y verificar que la ventaja de campo sale en torno a 0.25-0.30 (si sale negativa, faltan datos).
3. Generar las probabilidades sin mirar cuotas.
4. Solo entonces comparar con el mercado y con el % público, y anotar las discrepancias con su motivo.
5. Construir el boleto con máximo 6 signos únicos.
