# Jornada 19 · resultados y post-mortem · 5/11/2026

> Escrutinio oficial: loteriasyapuestas.es (captura del usuario, `escrutinio-oficial.jpg`). Pronóstico evaluado: `j19-pronostico.md`, sin retocar.

## 1. Resultados

| # | Partido | Resultado | Signo | Nuestro signo principal | P(signo que salió) |
|---|---|---|---|---|---|
| 1 | Barcelona – Aston Villa | 3-0 | 1 | 1 ✅ | 52,6 % |
| 2 | Bodø/Glimt – Lille | 0-0 | X | 1 ❌ | 26,1 % |
| 3 | Man. United – Roma | 3-2 | 1 | 1 ✅ | 42,6 % |
| 4 | Villarreal – PSG | 0-6 | 2 | 2 ✅ | 51,9 % |
| 5 | AEK – Real Madrid | 2-3 | 2 | 2 ✅ | 66,0 % |
| 6 | Fenerbahçe – Liverpool | 3-2 | 1 | 2 ❌ | 18,6 % |
| 7 | B. Dortmund – Betis | 2-1 | 1 | 1 ✅ | 51,4 % |
| 8 | Oporto – Nápoles | 4-1 | 1 | 1 ✅ | 43,2 % |
| 9 | Lens – Como | 1-9 | 2 | 2 ✅ | 38,8 % |
| 10 | Leipzig – Man. City | 2-3 | 2 | 2 ✅ | 57,4 % |
| 11 | Slavia Praga – Arsenal | 1-2 | 2 | 2 ✅ | 68,8 % |
| 12 | Real Sociedad – Lyon | 1-1 | X | 1 ❌ | 23,4 % |
| 13 | Celta – Union SG | 1-2 | 2 | 1 ❌ | 36,5 % |
| 14 | Getafe – Brighton | 0-1 | 2 | 2 ✅ | 56,0 % |
| 15 | **Pleno: Atlético – Bayern** | **0-2** | | 1-1 ❌ | 4,8 % (puesto 13 de 16) |

Columna ganadora: `1X122111222X22` · 2 empates (el modelo esperaba 3,23).

## 2. Premios oficiales

| Categoría | Acertantes | Premio por apuesta |
|---|---|---|
| Pleno al 15 | 2 | 42.255,09 € |
| 14 | 18 | 10.016,02 € |
| 13 | 534 | 158,26 € |
| 12 | 7.285 | 11,60 € |
| 11 | 45.070 | 1,88 € |
| 10 | 152.115 | **0,00 €** |

Recaudación: 1.126.802,25 € · 1.502.403 apuestas · premios: 619.741,24 € (el 55 %) · sin bote.

## 3. Qué cobró cada boleto

| Boleto | Coste | Mejor columna | Premios | Cobrado | Neto |
|---|---|---|---|---|---|
| v3 (16 sencillas, el definitivo de esta mesa) | 12 € | 11 | 4 × 11 aciertos | **7,52 €** | −4,48 € |
| Múltiple de 4 dobles (v3.2) | 12 € | 11 | 4 × 11 | 7,52 € | −4,48 € |
| Múltiples de 4 + 3 dobles (v3.2, 18 €) | 18 € | 11 | 4 × 11 | 7,52 € | −10,48 € |
| v1.1 (con vetos) | 12 € | 11 | 4 × 11 | 7,52 € | −4,48 € |
| Reducida B (v1) | 12 € | 10 | — | 0 € | −12 € |
| Boleto de 18 € de la otra sesión | 18 € | 10 | — | 0 € | −18 € |
| Columna del público | — | 10 | — | — | — |

**Sueltas: 5 de 5** (marcaron el Liverpool, el Real Madrid, el City, el Arsenal y el Barça). Historial: 5/5 · 4/5 · 5/5.

## 4. Calificación de las probabilidades

- **Log-loss de los 14: 0,858** (repartir 1/3 a cada signo da 1,099; J18: 0,897). Brier: 0,491.
- **Fallos del signo principal: 4, cuando se esperaban 6,94.**
- **Modelo frente a mercado** (11 partidos con cuota de bet365): **modelo 0,816 · mercado 0,729.** El mercado gana por segunda jornada seguida (J18: 0,897 frente a 0,786).
- **El patrón:** de los 9 partidos que ganó el favorito del mercado, en 8 el mercado le daba más probabilidad que el modelo (la excepción, el United: 42,6 % frente a 42,0 %) (Barça 75,6 % frente a 52,6 %; Real Madrid 75,9 % frente a 66,0 %; Arsenal 75,9 % frente a 68,8 %…). El modelo solo «ganó» al mercado en los resultados raros (la X del Bodø, el 1 del Fenerbahçe).

## 5. Clasificación de cada fallo

| Fallo | Tipo | Por qué |
|---|---|---|
| X del Bodø (26 %) | Varianza | El partido más igualado de la jornada |
| 1 del Fenerbahçe (19 %) | Varianza | El mercado le daba lo mismo (18 %) |
| X de la Real Sociedad (23 %) | Varianza | Sin cuota completa; el mercado veía al 1 más claro |
| 2 del Union (37 %) | Varianza | Prácticamente a cara o cruz con el 1 |
| Pleno 0-2 (4,8 %) | Varianza | Ganó el favorito por poco en el 1X2 (42 %), pero sin encajar |
| **Favoritos infravalorados** | **Modelo** | Dos jornadas seguidas y backtest (punto 6): error sistemático, no varianza |
| **Dos boletos distintos al cierre** | **Proceso** | La otra sesión propuso un boleto de 18 € con los vetos ya retirados. Cobró 0 €, frente a 7,52 € del nuestro. Hubo prisa y confusión en los últimos 30 minutos |
| **Siete versiones del boleto en dos días** | **Proceso** | v1 → v1.1 → v2 → v2.1 → v3 → v3.1 → v3.2. Cada cambio estaba justificado, pero el último llegó a media hora del cierre |

## 6. Comprobación con datos: el modelo es tímido con los favoritos

Backtest sin cuotas (`modelo/calibracion_temperatura.py`): el modelo se ajusta con los datos hasta una fecha y se evalúa en partidos posteriores que no ha visto.

| Favorito del modelo (jul–oct 2026) | Partidos | El modelo decía | Ganó |
|---|---|---|---|
| 50–60 % | 259 | 53,8 % | 59,1 % |
| 60–70 % | 138 | 64,4 % | 69,6 % |
| 70–80 % | 54 | 74,5 % | 81,5 % |
| 80–100 % | 20 | 85,5 % | 85,0 % |

**Corrección:** elevar el 1X2 a la potencia **T = 1,05** y renormalizar. T se eligió en marzo–junio de 2026 (1.113 partidos) y se comprobó en julio–octubre (1.155 partidos): mejora el log-loss en general (0,9790 → 0,9776), en los favoritos (0,8639 → 0,8614), en las copas UEFA (0,9010 → 0,8998) y en Primera (0,9388 → 0,9352). En julio–octubre el óptimo sería mayor (T ≈ 1,2), pero elegirlo con los mismos datos de prueba sería trampa: se revisa en la J29.

## 7. Lo que se aprende (y lo que no)

1. **El modelo se corrige con T = 1,05** (fase 2 del prompt v8). Es la única corrección del modelo: tiene evidencia fuera de muestra.
2. **Cada columna cobra por separado.** El boleto cobró cuatro premios de 11, pero el criterio de elección solo miraba la mejor columna. Desde ahora la calculadora da también el **valor esperado en euros** con una tabla de premios, contando todas las columnas.
3. **El premio de 10 aciertos fue 0 € y el de 11, 1,88 €.** P(≥10) y P(≥11) no sirven para decidir. Con los premios de la J19, la reducida B valía 7,6 € esperados por 12 €, frente a 13 € de las 16 columnas más probables. Es la primera jornada con premios: se apuntan en el registro de premios y el criterio pasa a valor esperado cuando haya 10.
4. **Una sola mesa y un solo boleto.** El boleto se congela al terminar la revisión final, **al menos 3 horas antes del cierre**. Después solo cambia con una noticia A o B (una baja, por ejemplo), nunca por una propuesta de otra sesión.
5. **No se cambia nada por varianza.** Los cuatro fallos tenían entre el 19 % y el 37 %. El Pleno 0-2 tenía un 4,8 %, pero el 1-1 tampoco era probable (9,3 %); el Pleno siempre se acierta poco.
6. **La regla del −4,5 se mantiene.** Esta jornada, de los cinco favoritos que venían de perder en Europa, ganaron tres (Barça, United, Oporto), empató uno (Bodø) y perdió otro (Lens). Cinco partidos no bastan para cambiar una regla medida con 88.
