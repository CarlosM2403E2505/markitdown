# Reglas codificadas de la mesa (22/11/2026)

Carlos, 22/11 a las 2:23: «tiene que ser la mesa quien decida», el máximo son 18 € y no se pueden seguir poniendo todas las columnas a 1. Desde la J24, **el boleto sale solo de `herramientas/reglas_mesa.py`**. Las reglas están escritas en el propio script y se comprueban con `herramientas/test_reglas_mesa.py`.

## Reglas

| Regla | Qué dice |
|---|---|
| R1 Presupuesto | Como máximo **18 € por jornada**, todo incluido (24 apuestas de 0,75 €) |
| R2 Objetivo | De los formatos que cumplen R3, gana el de mayor P(≥13). Si empatan, decide la P(14) y después la P(≥12) |
| R3 Diversidad | Parte máxima de columnas que puede llevar el signo favorito: menos del 45 % → 60 %; entre 45 y 55 % → 75 %; entre 55 y 65 % → 90 %; desde el 65 %, sin tope. Si la mesa da al favorito más de 8 puntos por encima de las casas, se aplica el tope del tramo de abajo |
| R4 Pleno | El marcador más probable de la mesa en todas las apuestas |
| R5 Probabilidades | Solo las de la mesa (modelo y noticias de clase A o B). Ni las cuotas ni el % del público cambian ninguna probabilidad |
| R6 Formatos | Se comparan siempre todos: directas, reducidas oficiales, directa o reducida con sencillas, y 24 sencillas optimizadas. Las sencillas optimizadas se buscan para la máxima P(≥13) dentro de los topes de R3 |

## ¿Sirven los formatos de 12 y 18 €? Prueba con resultados reales

`modelo/backtest_formatos.py`: **133 bloques de 14 partidos reales seguidos** de Primera y Segunda (septiembre de 2024 a noviembre de 2026). Las probabilidades son las de la mesa, siempre fuera de muestra. Cada formato se construye con esas probabilidades y se cuenta cuántos aciertos hace su mejor columna con los resultados reales.

| Formato | Media de aciertos | Bloques con ≥10 | ≥11 | ≥12 | ≥13 |
|---|---|---|---|---|---|
| 18 €, directa 3 dobles + 1 triple (el formato de Carlos) | 8,56 | 40 | 17 | 3 | 1 |
| 12 €, directa 4 dobles | 8,31 | 31 | 13 | 3 | 1 |
| 12 €, reducida 7 dobles | 8,74 | 40 | 17 | 4 | 1 |
| 18 €, las 24 sencillas más probables | 8,59 | 39 | 19 | 5 | 1 |
| 18 €, 24 sencillas optimizadas sin tope | 9,16 | 57 | 22 | **9** | 1 |
| **18 €, 24 sencillas optimizadas con R3 (lo nuevo)** | **9,27** | **57** | **22** | 8 | 1 |

**Veredicto de la mesa:**
- **El formato de 12 € (directa de 4 dobles) no sirve**: es el peor en todo.
- **El de 18 € (3 dobles + 1 triple) se queda corto.** Con el mismo dinero, las 24 sencillas optimizadas sacan más aciertos: 57 bloques con 10 o más frente a 40, y 8 con 12 o más frente a 3.
- **Desde la J24 se juegan 24 sencillas optimizadas con R3, por 18 €.** Caben en 3 boletos de 8.
- El tope de diversidad (R3) no cuesta nada con los resultados reales: da la mejor media de aciertos (9,27) y los mismos ≥10, ≥11 y ≥13. Según la mesa le resta algo de P(≥13): en la J24, 3,38 % frente al 3,85 % de las 24 más probables. Pero con resultados reales no se nota.
- Con 14 partidos de liga cualquiera, el 13 sale muy pocas veces (1 de cada 133 bloques). Las jornadas de quiniela llevan más favoritos claros y la P(≥13) que se espera sube al 3-4 %. **La Quiniela devuelve unos 0,55 € por cada euro jugado: ningún formato garantiza ganar dinero.** Lo que sí se puede hacer es elegir el formato que más aciertos da por euro, y ese es este.

## J24 con las reglas

24 sencillas optimizadas, 18 €, P(14) 1 entre 299, P(≥13) 3,38 %, P(≥12) 14,3 %. Pleno M-1 en todas. Ningún favorito por debajo del 65 % va en todas las columnas. Por ejemplo, Crystal Palace – Real Sociedad (53 %) lleva el 1 en 18 de las 24, y Sporting – Manchester United (44 %) en 13. Las columnas están en `jornadas/j24/j24.json`, en `boleto_mesa`.

## Informe del Auditor

- 133 bloques, todos fuera de muestra (walk-forward mensual). Cada formato se construye solo con las probabilidades de antes del partido. ✅
- `reglas_mesa.py` es determinista (semillas fijas) y los tests comprueban R1, R3, que no haya columnas repetidas y el caso del Rayo. ✅
- Datos en `datos/backtest_formatos.json`. ✅
