# QUINIELA NIVEL SUPREMO — LA MESA DE TRADING

**Protocolo de análisis orientado a acertar el Pleno al 15**
17 octubre 2026 · Sustituye a la metodología basada en cuotas

---

## Por qué apuntar al Pleno es la decisión correcta

Hay una razón técnica, no de gusto:

> **Un modelo de marcadores exactos produce el 1X2 gratis. Un modelo de 1X2 nunca produce el Pleno.**

El 1X2 es solo la matriz de marcadores agrupada en tres bloques (local gana, empate, visitante gana). Si el modelo acierta la distribución de marcadores, el 1X2 sale por descarte. Al revés es imposible: de una probabilidad "61% al 1" no se puede sacar si será 1-0 o 3-2.

Nuestro modelo anterior partía de cuotas 1X2. Por construcción **nunca podía predecir bien el Pleno.** Tu instrucción arregla eso de raíz.

---

## LA MESA: ocho mentes, cada una con un trabajo y un veto

Cada jornada pasa por las ocho. Ninguna puede saltarse.

### 1. Odds Compiler — *construye el precio honesto*
Produce la probabilidad base de los 14 partidos y la matriz de marcadores del Pleno **antes de que ningún dato de mercado o de público entre en la sala**. Su única fuente son goles reales marcados y encajados.
**Herramienta:** `dixon_coles.py` sobre `dataset_clean.json`.
**Entrega:** probabilidades 1X2 + xG de cada equipo + distribución 0/1/2/M del Pleno.

### 2. Data Analyst / Quant — *demuestra que el número es bueno*
No acepta un modelo porque parezca razonable. Lo valida fuera de muestra: entrena con partidos antiguos, predice los nuevos, y mide log-loss, Brier y acierto del Pleno contra una base tonta.
**Veto:** si el modelo no bate a la base tonta en datos no vistos, no se usa.
**Herramientas:** `backtest.py`, `pleno_tuning.py`.

### 3. Risk Analyst — *busca por dónde vamos a perder*
Su trabajo no es acertar, es impedir el desastre. Revisa:
- ¿Hay signos por debajo del 65% llamados "fijos"? → veto
- ¿Cuántos signos únicos hay? Más de 6 → veto
- ¿Algún dato viene de fuente no verificada? → mínimo doble
- ¿Está el modelo entrenado con menos de 1.000 partidos? → no es fiable
- ¿Hay nombres de equipo duplicados en el dataset? → aborta
**Veto:** absoluto. Es la mente que habría matado el "fijo al 45%" del Eibar.

### 4. Live Trader — *la información de las últimas horas*
Lo único que el modelo no puede saber: alineaciones, bajas confirmadas, sanciones, rotaciones por competición europea, viajes largos, clima. Ajusta en las horas previas al cierre.
**Precedente:** en la J14 el Athletic perdió a Nico Williams, Sancet, Canales, Guruzeta e Iñaki Williams. Nos salimos del mercado y pusimos la X. **Salió 0-0.** Esta mente es la que más valor ha aportado hasta ahora.
**Regla:** una baja de la unidad ofensiva titular pesa más que cualquier cuota.

### 5. Market Analyst (contrainteligencia) — *lee al enemigo, no le obedece*
Mira cuotas y porcentajes del público **después** de que el precio propio esté cerrado, y solo para responder a una pregunta: *¿dónde discrepamos y por qué?*
- Discrepancia a nuestro favor con razón identificada → ahí está el valor
- Discrepancia sin razón identificable → probablemente nos falta información, revisar
**Regla:** el % del público se usa **invertido**. Sirve para saber dónde NO ir.

### 6. Pleno Specialist — *la mente dedicada al 15*
Dueño exclusivo de la categoría 0/1/2/M. Aplica la escala de goles y la mezcla empírica calibradas, y decide cuántos Plenos cubrir según la tabla de cobertura real (abajo).
**Regla:** nunca anunciar una cobertura del Pleno sin respaldarla con la tabla medida.

### 7. Portfolio Manager — *convierte probabilidades en boleto*
Reparte triples, dobles y columnas dentro del presupuesto, maximizando lo que de verdad se puede ganar. Sabe que 5 columnas no se forman con dobles y triples (5 es primo) y que hay que construir la reducción a mano.
**Herramienta:** el optimizador de columnas con evaluación exacta.

### 8. Calibration Auditor — *nos mantiene honestos*
Después de cada jornada compara probabilidad declarada con resultado real. No pregunta "¿acertamos?" sino "¿**fallamos las veces que dijimos que fallaríamos**?".
**Precedente J14:** los 8 fijos predecían 3.41 fallos; de los 6 jugados se esperaban 2.56 y hubo 2. El modelo estaba bien calibrado. El error fue de lenguaje, no de número.

### 9. Red Team — *la mente de la casa*
Una pregunta, siempre la misma: *"Si yo fuera el Risk Analyst de la casa y quisiera que este señor perdiera, ¿qué columna querría que rellenase?"* Si la respuesta es nuestro boleto, hay que rehacerlo.

---

## Lo que se ha construido y medido hoy

### El canal de datos

| Paso | Herramienta | Resultado |
|---|---|---|
| Descarga | `git clone openfootball/espana` | GitHub está en la lista blanca del proxy; football-data.co.uk da 403 |
| Parseo | `parse_openfootball.py` | 3 formatos distintos en el repo, resueltos |
| Normalización | `normalize_teams.py` | 59 nombres → **46 equipos canónicos** |
| Ajuste | `dixon_coles.py` | 1.413 partidos, convergencia OK |

**Dos bugs cazados que habrían corrompido todo:**

1. **Fechas desordenadas.** El repo omite el año salvo cuando cambia, y algunos ficheros traen bloques de partidos aplazados fuera de orden. Mi heurística de "si el mes retrocede, suma un año" estampaba 2026 a partidos de octubre de 2025. Arreglado leyendo la ventana de temporada del encabezado del propio fichero.

2. **Equipos duplicados.** "Barcelona" y "FC Barcelona" eran dos equipos para el modelo. Y la trampa gorda: **"Real Sociedad" vs "Real Sociedad B"** (el filial juega en Segunda) y **"Racing Santander" vs "Racing Ferrol"** son clubes distintos que una normalización automática habría fusionado. Tabla explícita, con validación que aborta ante cualquier nombre desconocido.

### La puerta de validación

Anoche el problema era que con 90 partidos el modelo estimaba la ventaja de campo en **−0.03** (signo cambiado). Con 1.413 partidos:

**ventaja de campo = 0.306** ✅ · convergencia OK · 0 problemas de integridad

### Los parámetros calibrados

Medidos entrenando con 1.135 partidos y evaluando sobre **278 que el modelo no había visto**:

| Parámetro | Valor | Por qué |
|---|---|---|
| `xi` (decaimiento temporal) | **0.0015** | Vida media ~15 meses. Decaimientos más agresivos empeoran: el pasado pesa más de lo que suponía |
| `scale` (goles esperados) | **1.10** | El modelo sale **corto de goles un 10%**. Corregirlo subió el acierto del Pleno del 12.6% al 15.5% |
| `blend` (mezcla empírica) | **0.20** | El modelo es demasiado confiado en marcadores exactos. Mezclar bajó el log-loss de 2.626 a 2.589 |
| `ridge` | 0.05 | Encogimiento hacia la media, evita sobreajustar a recién ascendidos |

---

## Dos correcciones a lo que te dije anoche

### 1. La corrección rho de Dixon-Coles NO sirve

Te dije que era el arreglo para los 0-0 y 1-1 que nos mataron. **Me equivoqué.** Medido sobre 278 partidos no vistos:

| Modelo | log-loss 1X2 | Pleno #1 |
|---|---|---|
| Base tonta (media de la liga) | 1.0493 | 10.8% |
| Poisson simple (rho = 0) | 0.9909 | 12.6% |
| Dixon-Coles (rho libre) | **0.9908** | 12.6% |

Idénticas. Y rho se ajusta a **+0.01**, no al −0.13 de la literatura. El motor lo mantiene como opción, pero no es la mejora que parecía. Lo que sí mejoró el Pleno fue la escala de goles y la mezcla empírica.

### 2. La cobertura del Pleno que te di estaba inflada

Para la J14 te dije que 5 Plenos cubrían el 66.1%. Ese número salía de las propias probabilidades del modelo, que son optimistas. **Medido sobre datos reales no vistos:**

| Plenos jugados | Cobertura REAL | Lo que yo dije |
|---|---|---|
| 1 | **15.8%** | 15.7% ✓ |
| 2 | **29.9%** | 31.4% |
| 3 | **41.0%** | — |
| 4 | **48.2%** | 58.2% ❌ |
| 5 | **55.8%** | 66.1% ❌ |
| 6 | **61.2%** | — |
| 8 | **74.1%** | — |

Esta tabla es ahora la referencia. Nada de anunciar coberturas sin respaldarlas aquí.

**Lo bueno:** la calibración del modelo es honesta. Declara un 13.8% al mejor Pleno y acierta el 15.8%. Va ligeramente **infra**confiado, que es el lado correcto del error.

---

## El modelo contradice al mercado en el Pleno de la J14

Getafe–Rayo (lunes 19, 21:00). Sin mirar una sola cuota:

| | Modelo propio (1.413 partidos) | Lo que dije anoche (anclado en cuotas) |
|---|---|---|
| 1X2 | **35.7 / 33.8 / 30.5** → Getafe favorito | 33 / 31 / 36 → Rayo favorito |
| xG | Getafe **0.93** – Rayo **0.84** | Getafe 0.85 – Rayo 1.00 |
| Pleno #1 | **0-0 (15.4%)** | 0-1 (15.7%) |
| Pleno #2 | **1-0 (15.1%)** | 0-0 (15.7%) |

**Por qué discrepan:** yo me anclé en las cuotas (2.80 al Rayo frente a 3.05 al Getafe) y en los 0.5 goles por partido del Getafe esta temporada. El modelo, con dos temporadas, ve que la **defensa del Getafe es −0.457, la cuarta mejor de los 46 equipos**, y eso pesa más que su ataque flojo (−0.299). Además tiene la ventaja de campo bien estimada.

El Live Trader añade lo que el modelo no sabe: Getafe sin Uche, con Ünal en duda y viniendo de jugar el jueves en Rumanía. Eso empuja hacia menos goles del Getafe.

**Síntesis de la mesa: 0-0 como principal**, que es a la vez el top del modelo y lo coherente con las bajas. Después 1-0 y 1-1.

El modelo también firma, para los partidos del domingo que aún no se han jugado: **Celta–Alavés 49.7/25.4/24.9**, **Málaga–R.Sociedad 22.5/25.2/52.3**, **R.Madrid–Sevilla 77.1/14.1/8.8**. Son predicciones comprobables mañana.

---

## Lo que falta

| Hueco | Impacto | Cómo se cierra |
|---|---|---|
| **Liga F** no está en openfootball ni en football-data | Fueron 4 de 14 partidos en la J14 | Hay que encontrar fuente de resultados históricos de Liga F |
| **Segunda 2026/27** no está en el repo | P8–P10 de cada jornada | Vía football-data con paginación, o esperar al repo |
| Segunda 2025/26 solo al 28% | Menos muestra en Segunda | Igual que arriba |
| Primera 2026/27 llega al 20/09 | Faltan jornadas 8 y 9 | Añadir a mano los resultados verificados |

Mientras esos huecos existan, los partidos de Liga F y Segunda siguen siendo "dato no verificado" y por la regla del Risk Analyst **nunca pueden ser signo único**.
