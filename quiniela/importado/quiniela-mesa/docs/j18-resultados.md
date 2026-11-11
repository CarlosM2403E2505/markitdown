# J18 — RESULTADOS Y POST-MORTEM (domingo 1/11, falta Tenerife F–Athletic F del lunes 2/11)

> **Boleto de la mesa:** A-R original a 18 €. Boleto 1: 16 apuestas, con P11 en 12 y P12 en 2. Boleto 2: 8 apuestas, con P11 en 2 y P12 en 1. Pleno 1-1.
> **Aviso:** el sábado a las 12:01 el usuario avisó de que la app no aceptaba el boleto (el cierre es a las 12:00 de Canarias). Si no se llegó a sellar, esto evalúa el pronóstico pero no hay premio que cobrar.

| Nº | Partido | Resultado | Signo | Boleto 1 (16) | Boleto 2 (8) | Prob. del modelo para el signo real |
|---|---|---|---|---|---|---|
| 1 | Levante – Atlético | 0-2 | 2 | 2 ✅ | 2 ✅ | 45,4% |
| 2 | Rayo – Celta | 3-0 | 1 | 1 ✅ | 1 ✅ | 44,2% |
| 3 | Betis – Málaga | 2-1 | 1 | 1 ✅ | 1 ✅ | 70,1% |
| 4 | Barcelona – Alavés | 6-1 | 1 | 1 ✅ | 1 ✅ | 82,1% |
| 5 | Getafe – Sevilla | 3-1 | 1 | 1X ✅ | 1X ✅ | 42,6% |
| 6 | Racing – Real Madrid | 0-3 | 2 | 2 ✅ | 2 ✅ | 67,1% |
| 7 | Elche – Valencia | 0-1 | 2 | 1 ❌ | 1 ❌ | 23,6% |
| 8 | Eibar – Almería | 1-1 | X | 1 ❌ | 1 ❌ | 26,4% |
| 9 | Eldense – Granada | 0-2 | 2 | 12 ✅ | 12 ✅ | 36,2% |
| 10 | Burgos – Castellón | 1-1 | X | 12 ❌ | 12 ❌ | 29,3% |
| 11 | Alavés F – Real Sociedad F | 1-1 | X | 12 ❌ | 2 ❌ | 28,0% |
| 12 | Madrid CFF – Deportivo F | 2-1 | 1 | 2 ❌ | 1 ✅ | 34,8% |
| 13 | Sevilla F – Real Madrid F | 1-3 | 2 | 2 ✅ | 2 ✅ | 63,7% |
| 14 | Tenerife F – Athletic F | lunes 2/11 | — | 1 | 1 | (56,1% al 1) |
| P15 | Athletic – Real Sociedad | 2-1 | Pleno 2-1 | 1-1 ❌ | 1-1 ❌ | 9,0% (3.er marcador del modelo) |

**Signos con 13 partidos jugados:** 2 1 1 1 1 2 2 X 2 X X 1 2 · (P14 el lunes) · Pleno 2-1.

## Escrutinio de columnas (13 jugados)

| Boleto | Columnas | Mejor columna hoy | Si gana el Tenerife F |
|---|---|---|---|
| Boleto 1 (A-R original, 12 €) | 16 | 8 | 9: sin premio |
| **Boleto 2 (las 8 extra, 6 €)** | 8 | **9** (2 columnas) | 10: **no cobra** (ver corrección del 1/11) |
| A-R/P12 (el de 12 € que recomendó el Director el viernes) | 16 | 9 | 10 |
| B, reducida de 7 dobles (referencia) | 16 | 9 | 10 |

Las dos columnas con 9 aciertos: `2 1 1 1 1 2 1 1 2 1 2 1 2 1` y `2 1 1 1 1 2 1 1 2 2 2 1 2 1`.

## 5 sueltas: 4 de 5 ✅ (se esperaban 4,4)

| # | Apuesta | Prob. | Resultado |
|---|---|---|---|
| 1 | Barcelona marca | 95,4% | ✅ (6-1) |
| 2 | Real Madrid marca | 92,7% | ✅ (0-3) |
| 3 | Betis marca | 89,5% | ✅ (2-1) |
| 4 | Getafe – Sevilla: menos de 3,5 goles | 82,1% | ❌ (3-1; el cuarto gol llegó en el 90+3, con el Sevilla ya con 10) |
| 5 | Atlético marca | 80,8% | ✅ (0-2) |

## Cómo se comportó el modelo

| Medida (13 partidos) | Modelo | Referencia |
|---|---|---|
| Log-loss | **0,863** | 1,099 si se reparte al azar (1/3 cada signo) |
| Brier | **0,499** | 0,667 al azar |
| Aciertos del favorito | 7 de 13 | 6,6 esperados → bien calibrado |
| Primera: aciertos del favorito | **6 de 7** | 4,0 esperados |
| Segunda + Liga F: aciertos del favorito | **1 de 6** | 2,6 esperados |
| Log-loss en P1–P12 | 0,897 | **Público (LAE): 0,786** |

Esta jornada el % del público fue mejor que el modelo, sobre todo por P12 (puso un 67% al 1) y porque en Primera ganaron todos los favoritos claros, a los que el público da más confianza.

## Qué pasó

1. **Tres empates, todos en Segunda y Liga F** (P8, P10 y P11), con un 26–29% cada uno. El boleto solo llevaba X en el Getafe, que acabó en 1. Una jornada con 3 X es lo normal (la media histórica es 3,55). El sistema A-R maximiza P(14) a costa de necesitar una jornada con pocos empates.
2. **P12, Madrid CFF – Deportivo F (2-1): el público acertó** (67% al 1; el modelo daba 34,8%). La decisión del Director del viernes de cubrir P12 era la correcta. En la opción de 18 € solo el boleto 2 llevaba el 1, y ahí están las dos mejores columnas.
3. **P7, Elche – Valencia (0-1):** el 2 tenía un 23,6%. El público también jugaba el 1. Es varianza, no un error.
4. **Pleno 2-1:** era el tercer marcador más probable del modelo (9,0%), por detrás del 1-1 (12,2%) y el 1-0 (9,6%). No hay nada que corregir.
5. **Proceso:** el boleto se intentó sellar a las 12:01, con el cierre a las 12:00 de Canarias. Es el fallo más caro de la jornada: si gana el Tenerife F, el boleto 2 tendría 10 aciertos y cobraría premio.

## La X en la Segunda que elige Loterías (pendiente desde la J16)

| Jornada | Partidos de Segunda | X |
|---|---|---|
| J14 | Eibar–Mallorca 1-1 · Las Palmas–Castellón 0-3 · Burgos–Sabadell 1-0 | 1 |
| J16 | Leganés–Mallorca 1-1 · Almería–Oviedo 2-2 · Sabadell–Tenerife 1-1 | 3 |
| J18 | Eibar–Almería 1-1 · Eldense–Granada 0-2 · Burgos–Castellón 1-1 | 2 |
| **Total** | 9 partidos | **6 (67%)** |

**Qué dice el histórico.** Las posiciones 8–10 de la Quiniela (Segunda) traen un **28% de X** (2019–2026). La Segunda entera tuvo un 28,1% en 2024-25, un 24,9% en 2025-26 y lleva un 21,5% en 2026-27 (121 partidos). El modelo daba a la X de esos partidos entre el 26% y el 29%, que es justo esa tasa.

**Conclusión del Científico de datos.** Con un 28% de X, que salgan 6 o más en 9 partidos pasa el 1,8% de las veces. Es mala suerte, no un sesgo del modelo: siete años de histórico pesan más que 9 partidos.

**Qué se decide.**
- **No se cambia el modelo.**
- En los partidos de Segunda igualados (1 y 2 a menos de 5 puntos), el doble 12 sigue siendo el que más cubre: un 71% frente al 65% del 1X en Burgos–Castellón.
- Con la regla "1X si están igualados", en esta jornada se habría ganado P10 y perdido P9, así que el saldo es cero.
- La pregunta pendiente de la J16 queda contestada.
- Se revisa solo si la racha sigue: a los 30 partidos de Segunda elegidos por Loterías.

## Reglas y tareas que salen de aquí

| Qué | Tipo |
|---|---|
| **Sellar el viernes, o el sábado antes de las 11:00 de Canarias.** El sábado, solo se ajusta el boleto si hay una noticia de clase A, y con una hora de margen como mínimo | Regla de proceso (obligatoria) |
| Liga F: si el modelo contradice al público en más de 25 puntos sin una razón identificada, ese partido se cubre | Se confirma (1 caso a favor) |
| Llevar cada jornada el log-loss del modelo frente al del público. J18: público 0,786, modelo 0,897 | Seguimiento nuevo del Científico de datos |
| X en Segunda: no se cambia nada; se revisa a los 30 partidos (van 9, con 6 X) | Seguimiento |
| No se toca ningún parámetro por una sola jornada | Norma de siempre |

## Fuentes
FutbolTotal (Barça–Alavés, Athletic–Real Sociedad y la jornada de Primera; Madrid CFF 2-1 Deportivo), Fox Sports (Getafe 3-1 Sevilla), Periódico de Ibiza (jornada 12 de Segunda), Infobae/EFE (Alavés 1-1 Real Sociedad F), El Sevillista y OKDiario (Sevilla 1-3 Real Madrid F).


---

## Análisis pedido por el usuario (domingo 1/11, 23:22): el Valencia, los dobles 12 y por qué no llegamos a 10

> El usuario pidió que no se cambie nada, solo analizar, y que la mesa aprenda para la J19.

### P7 Elche 0-1 Valencia: no se dio por perdido, se infravaloró
| Fuente | 1 | X | 2 |
|---|---|---|---|
| Modelo (precio final) | 49,9 | 26,5 | **23,6** |
| Mercado (control) | 40 | 28 | **32** |
| Público (LAE) | 40 | 33 | 27 |

- **Sadiq contado como baja.** Volvía de lesión, entró en el 61' y marcó el 0-1 en el 67'. En el modelo oficial, ese error movía el 2 solo medio punto (de 24,1 a 24,6).
- **El mercado le daba 8 puntos más al Valencia.** La regla v5 obliga a revisar los datos ante una discrepancia sin causa. No se revisó: el Trader puso "mantener".
- **Señales que el modelo no pesa:**
  - xG del Valencia: 10,3 frente a 7 goles; la capa xG tiene un tope del 5%.
  - El Elche no había ganado en casa esta temporada.
  - El Valencia acababa de cambiar de entrenador (Aguirre); la regla del proyecto dice que el cambio de entrenador no ajusta.
- **Aunque se hubiera doblado P7, se habría fallado:** con nuestros números el doble era 1X, porque la X (26,5) iba por delante del 2 (23,6). Además, con 4 dobles, P7 nunca iba a llevar uno: el doble multiplica P(14) por 1,53 en P7 y por 1,97–1,99 en P9, P10 y P11.

### Los dobles 12 y el segundo boleto clonado
| Nº | 1 · X · 2 | Cubre 12 | Cubre 1X | Cubre X2 | Investigador | Salió |
|---|---|---|---|---|---|---|
| 8 | 40,3 · 26,4 · 33,3 | 73,6 | 66,7 | 59,7 | 12 | X |
| 9 | 36,8 · 27,1 · 36,2 | 73,0 | 63,9 | 63,3 | 12 (2 si va sencillo) | 2 |
| 10 | 35,6 · 29,3 · 35,1 | 70,7 | 64,9 | 64,4 | X2 el 27/10 (la retiró el 30/10) | X |
| 11 | 35,5 · 28,0 · 36,5 | 72,0 | 63,5 | 64,5 | **X2** | X |

- En los cuatro, la X era el signo menos probable. Optimizando P(14), el doble siempre es 12 y **la X no entra nunca**.
- Consecuencia: en el 73% de las jornadas al menos uno de estos cuatro acaba en X, y entonces **fallan las 24 columnas a la vez**. Que acaben en X tres de los cuatro pasa un 6,7% de las veces.
- El segundo boleto se diseñó solo para cubrir el 1 de P12 y copió todo lo demás. ~~Es el error de diseño de la jornada.~~ **Corregido el 1/11 a las 23:55:** solo es un error si se mira P(≥10), y 10 aciertos no cobra (ver más abajo).

Cálculo exacto con los precios de antes del partido, manteniendo el boleto 1:

| Segundo boleto (8 apuestas) | Signos | P(≥10) | P(≥11) | P(14) | Aciertos reales (13 jugados) |
|---|---|---|---|---|---|
| Jugado | P11 2 · P12 1 | 33,9% | 15,5% | 1 entre 1.050 | 9 |
| Con lo que propuso el Investigador | P9 2 · P10 X2 · P11 X2 · P12 1 | 35,6% | 16,2% | 1 entre 1.115 | 11 |
| Optimizado para 10 o más | 12 1 1 1 12 2 1 2 X X X 12 2 1 | **38,2%** | 16,9% | 1 entre 1.280 | 10 |

Diversificar daba más P(≥10) y P(≥11) **antes** del partido (+1,7 a +4,3 puntos), a cambio de un 6–18% de P(14). **Pero 10 aciertos no cobra y 11 cobra 2–4 €.** En las categorías que pagan (12 o más), las tres opciones quedan iguales (5,0–5,1%), y en 13 y 14 el boleto jugado era el mejor (P(≥13): 1,01% frente a 1,00% y 0,92%).

### ¿Por qué no llegamos a 10?
| Jornada | Sistema | Coste | P(≥10) calculada antes | Mejor columna | Incidencia |
|---|---|---|---|---|---|
| J14 | 5 columnas | 3,75 € | 20,3% | **11** | **No se selló** |
| J15 | 5 columnas | 3,75 € | 29,5% | 9 | — |
| J16 | Reducida de 7 dobles | 12 € | 22,7% | 9 | — |
| J18 | A-R + 8 | 18 € | 33,9% | 9 (10 si gana el Tenerife F) | **Boleto rechazado a las 12:01** |

- Se esperaba llegar a 10 en **1,1 jornadas** de estas cuatro, y se llegó en 1, la J14, que no se selló.
- No llegar a 10 en la J15, la J16 y la J18 tenía un 36% de probabilidad.
- **El modelo rinde como dijo que rendiría. Lo que falla es:**
  - el diseño, que optimiza solo el 14;
  - el proceso: dos de cuatro boletos sin validar;
  - las reglas que existen pero no se aplican.

### Errores de la mesa
| Error | Jornadas | Responsable |
|---|---|---|
| Boleto sin sellar o fuera de plazo; hora de cierre mal dada | J14, J18 | Claude (Director) |
| ~~Segundo boleto clonado del primero~~ No era un error en dinero: solo pierde en 10 y 11, que no pagan o pagan muy poco | J18 | Corregido por el Director |
| Reglas escritas que no se aplican: portero del Rayo, discrepancia con el mercado en P7 | J16, J18 | Director y Auditor |
| Bajas caducadas o falsas: Sadiq, Antony | J18 | Investigador y Auditor |
| Decidir el sistema solo por P(14) (regla R), sin poner P(≥10) en la balanza | J16, J18 | Risk Manager y Director |
| Descartar el disenso del Investigador sin registrarlo ni medirlo | J18 | Director |

### Reglas para la J19 (propuestas)
| Regla | Qué evita | Responsable |
|---|---|---|
| **Boleto cerrado el viernes.** El sábado solo cambia por una noticia de clase A y se sella antes de las 11:00 de Canarias. La hora oficial de cierre se da siempre en hora de Canarias | J14 y J18 | Director |
| **Bajas con fecha.** Una baja solo mueve números si es una sanción o una lesión con regreso posterior al partido, según una fuente de las últimas 72 h. Si el jugador "vuelve a entrenar", está "recuperado" o "en duda", el ajuste es 0 | Sadiq | Investigador y Auditor |
| **Diferencia con el mercado de 7 puntos o más en cualquier signo:** revisión escrita y firmada por el Auditor antes de cerrar. El mercado sigue siendo solo control | P7 | Compilador y Auditor |
| **Los boletos se eligen por P(14), P(≥13), P(≥12) y valor; P(≥10) no cuenta, porque 10 aciertos no cobra.** Si hay un segundo boleto, el disenso documentado del Investigador entra cuando cueste menos del 10% de P(14) | Optimizar una categoría sin premio | Matemático y Risk Manager |
| **Cada propuesta muestra P(14), P(≥10) y P(≥12),** y se decide según el objetivo que fije el usuario | Decidir solo por el 14 | Director |
| **Registro del Investigador:** sus disensos se apuntan y se miden. J18: P11 X2 ✓; P10 X2 (retirada) habría acertado; P14 1X pendiente | Perder información buena | Científico de datos |

~~La mesa recomienda el mixto con 18 € para buscar 10 o más.~~ **Corregido:** 10 no cobra. Ver la recomendación de la J19 más abajo.


---

## Corrección y análisis (domingo 1/11, 23:55)

### Corrección: 10 aciertos no cobra
Datos de los escrutinios oficiales de Loterías:

| Categoría | J12 (11/10) | J14 (18/10) | J15 (21/10) | J17, Copa (28/10) |
|---|---|---|---|---|
| 14 | 17.501 € | 11.162 € | 45.666 € | 302 € |
| 13 | 254 € | 165 € | 389 € | 4,65 € |
| 12 | 23,25 € | 12,76 € | 22,02 € | 1,38 € |
| 11 | 3,91 € | 2,22 € | 3,05 € | no cobra |
| **10** | **no cobra** | **no cobra** | **no cobra** | **no cobra** |

- **10 aciertos no ha cobrado en ninguna de estas jornadas:** su premio queda por debajo de 1,50 € y el dinero va al bote de la categoría especial.
- **El dinero está en 13 y 14.** El 12 paga lo justo y el 11 casi nada.
- **Lo que queda corregido:**
  - Decir que el boleto 2 cobraría con 10 aciertos fue un error.
  - Recomendar diversificar para buscar 10 o más también fue un error.
  - El "segundo boleto clonado" no costó dinero: en 12 o más los tres diseños quedan igual, y en 13 y 14 el jugado era el mejor.
- J18: había un bote de 2,7 M€ para la categoría especial (14 + Pleno con un único acertante).

### ¿Sábado bien y domingo mal? (pregunta del usuario)
Partido a partido: ¿ganó el favorito del modelo? Se compara con lo esperado (la suma de las probabilidades del favorito).

| Jornada | Sábado: aciertos | Esperado | Domingo y lunes: aciertos | Esperado |
|---|---|---|---|---|
| J14 | 4 de 8 | 4,2 | **5 de 6** | 2,8 |
| J16 (solo los partidos con día confirmado) | 2 de 3 | 1,5 | 4 de 6 | 2,8 |
| J18 | 4 de 6 | 3,3 | 3 de 7 | 3,3 |
| **Total** | **10 de 17 (59%)** | 9,0 | **12 de 19 (63%)** | 8,9 |

- **En la J18 fue así en el boleto:** el sábado se acertaron 5 de 6 (boleto 2) y el domingo 4 de 7.
- **En favoritos, el domingo de la J18 salió justo lo esperado** (3 de 7, con 3,3 esperados). El que salió mejor de lo esperado fue el sábado.
- **En la J14 pasó al revés** (domingo 5 de 6).
- **Con tres jornadas, no hay ninguna prueba de que el domingo falle más.**
- **Lo que sí es real es el mecanismo de información:**
  - Las convocatorias de los partidos del domingo y del lunes salen después del cierre. El caso Sadiq es justo eso: el Valencia publicó su lista el sábado.
  - En los partidos del sábado, las convocatorias salen el viernes y se pueden usar.

**Reglas nuevas:**
1. **Partidos posteriores al cierre (domingo y lunes):**
   - No se aplica ningún ajuste por bajas de más del 2% si la noticia puede cambiar después del cierre: lesión sin fecha de regreso, "duda", "vuelve a entrenar".
   - Ante dos dobles casi iguales (menos del 2% de diferencia en P(14)), el doble va al partido posterior al cierre.
2. **Partidos del sábado:** el viernes por la tarde se revisan sus convocatorias.
3. **El Científico de datos lleva la cuenta por día.** Se revisa a los 50 partidos.

### Recomendación de la mesa para la J19
**Veredicto: sí, jugarla, con cuatro condiciones.**

| Agente | Dictamen |
|---|---|
| Risk Manager | La Quiniela devuelve de media unos 55 céntimos por euro; ningún sistema lo cambia. Se juega como gasto fijo de ocio: **12 € por jornada**. 18 € solo si se fija como presupuesto estable, nunca para recuperar. Hasta ahora la mesa no ha demostrado que gane dinero |
| Matemático | Con 12 €, **4 dobles completos (tipo A)** frente a la reducida de 7 dobles: más 14 (1 entre 1.470 frente a 1 entre 2.210 en la J18) y más 13. La reducida solo gana en 12, 11 y 10, que pagan poco o nada |
| Compilador | **Filtro de valor:** si el 14 más probable coincide con lo que juega todo el mundo, paga poco (en una jornada de favoritos, 590 € el 14). Entre boletos con al menos el 90% de la P(14) máxima, el de más valor |
| Investigador | La composición de la J19 aún no está publicada (domingo noche). Loterías suele publicarla el lunes o el martes. Entre semana hay Europa: el jueves habrá que mirar el cansancio |
| Trader / Director | **Calendario:** primera pasada en cuanto se publique; revisión el viernes por la tarde; **sellado el viernes**. El sábado, solo noticias de clase A y antes de las 11:00 de Canarias |
| Auditor | Antes de sellar, la lista de control de `registro-errores.md`, firmada punto por punto |

Pendiente de confirmar con el usuario: presupuesto, sistema y cuándo y cómo sella.

## Cierre del P14 (lunes 2/11, 23:35)
**Tenerife F – Athletic F: 2-0, sin confirmar** (titular de Radio Marca Tenerife; falta una segunda fuente). Signo 1, que estaba en todas las columnas.
- **Mejor columna final de la J18: 10 de 14** (dos columnas, en el boleto 2). **10 aciertos no cobra.** Boleto 1: 9 de 14.
- Signos finales: 2 1 1 1 1 2 2 X 2 X X 1 2 1 · Pleno 2-1.
- Recordatorio: el boleto no llegó a validarse (rechazado a las 12:01).
