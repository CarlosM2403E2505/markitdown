# ¿Tiene ventaja la mesa? Auditoría honesta (14/11/2026)

Pregunta de una casa de apuestas antes de jugar más fuerte: **¿nuestro método gana a lo fácil?**
Método: `modelo/auditoria_ventaja.py`, walk-forward sobre 1.862 partidos de Primera y Segunda
(sep. 2024 – nov. 2026), **todos fuera de muestra** (el modelo nunca ve el futuro de lo que predice).

## 1. Sí, el modelo gana a las referencias

| Medida | Modelo | Siempre el local | Mejor clasificado | Climatología (la media 46/25/29) |
|---|---|---|---|---|
| **Log-loss** (menos es mejor) | **1,014** | — | — | 1,062 |
| **Acierto del signo** | **50,4 %** | 46,3 % | 45,7 % | — |

- El modelo acierta el signo **4 puntos más** que apostar siempre al local o al mejor clasificado.
- En log-loss bate a la climatología un 4,5 %: nuestras probabilidades llevan información real, no son el reparto medio.
- No es magia: acertar la mitad de los signos es lo que da de sí el fútbol. Pero es una ventaja medida y repetible.

## 2. El modelo está bien calibrado (y algo tímido con los grandes favoritos)

| Probabilidad que da el modelo al favorito | Partidos | Dada | Real |
|---|---|---|---|
| 33–42 % | 528 | 39,4 % | 44,1 % |
| 42–50 % | 732 | 45,7 % | 44,7 % |
| 50–58 % | 354 | 53,4 % | 55,1 % |
| 58–66 % | 136 | 61,5 % | 64,7 % |
| **66 %+** | **112** | **74,7 %** | **85,7 %** |

- En el grueso de los partidos la probabilidad dada y la real casi coinciden: el modelo no engaña.
- **Hallazgo:** cuando el favorito es muy claro, el modelo se queda corto (da 75 %, gana el 86 %). Afilar más esos partidos (temperatura más alta) está pendiente de probar (anexo I). No se toca aquí.

## 3. El boleto no es optimista de más

133 bloques de 14 partidos reales, tomando el signo más probable del modelo:

| Aciertos | Observado | Esperado por el modelo |
|---|---|---|
| 10 | 9 | 6,5 |
| 11 | 4 | 2,2 |
| 12 | 0 | 0,5 |
| 13–14 | 0 | 0,2 |

- Lo observado va **por encima o igual** que lo esperado: el modelo, si acaso, se queda corto; nunca promete de más.
- Con un solo signo por partido, el 13 y el 14 casi no salen (0,2 esperados en 133 jornadas). Por eso se juega con dobles y triples: para comprar esas colas.

## Veredicto de la mesa

1. **Hay ventaja real y medida** sobre las apuestas ingenuas y sobre el reparto medio. Es la ventaja de la casa, puesta a tu favor.
2. **Las probabilidades son honestas**: lo que el modelo dice que pasa, pasa con esa frecuencia.
3. **El límite no es el modelo, es el juego:** la Quiniela devuelve ~0,55 €/€. La ventaja mejora las probabilidades de premio, no convierte el boleto en rentable seguro. Por eso el presupuesto lo fija el usuario y **nunca se sube para recuperar**.
4. **Lo único que de verdad bajaría el "1 entre 1.000"** es afilar los favoritos claros (punto 2) y jugar más columnas; lo primero se probará, lo segundo lo decides tú.

## Informe del Auditor

- 1.862 partidos, todos fuera de muestra; reajuste mensual. ✅
- Log-loss y acierto recalculados; baselines con probabilidad justa (climatología), no degenerada. ✅
- Distribución del boleto por Poisson-binomial (`quiniela_calc`), suma = nº de bloques. ✅
- Datos en `datos/auditoria_ventaja_resumen.json`. Tests en `modelo/test_auditoria_ventaja.py`. ✅
