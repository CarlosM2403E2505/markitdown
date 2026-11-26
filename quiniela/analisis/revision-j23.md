# Revisión de la J23 y cambios en la mesa (22/11/2026, madrugada)

Resultados del sábado 21/11 sacados de **Flashscore.es** (abierto desde el navegador integrado del ordenador de Carlos) y el Pleno confirmado con Soccerway.

## 1. Qué pasó el sábado

| N.º | Partido | Resultado | Signo | Mesa 1/X/2 | Casas 1/X/2 | Boleto | ¿Acierto? |
|---|---|---|---|---|---|---|---|
| 1 | Alavés – Deportivo | 3-1 | 1 | 59/23/18 | 43/29/28 | 1 | ✅ |
| 2 | Rayo – Valencia | 0-1 | 2 | 54/26/20 | 49/27/23 | 1 | ❌ |
| 3 | Real Madrid – Celta | 2-1 | 1 | 79/14/8 | 82/12/6 | 1 | ✅ |
| 8 | Tenerife – Mallorca | 0-0 | X | 23/26/50 | 28/29/43 | 2 | ❌ |
| 11 | Eibar F – Atlético F | 1-3 | 2 | 17/23/60 | 10/20/70 | 2 | ✅ |
| 15 | Sevilla – Betis (Pleno) | 1-1 | — | 1-1 era el marcador más probable (11,3 %) | — | 1-1 | ✅ |

- **El Pleno 1-1 se acertó.** Pero el Pleno al 15 solo cobra si la columna tiene los 14, así que con el Rayo fallado ya no vale.
- **Columnas vivas tras el sábado** (36 jugadas): **ninguna sin fallo**. 31 tienen 2 fallos, 4 tienen 3 y solo 1 (C2) tiene 1 fallo. **El 14 ya es imposible y el techo es 13 (solo con C2).**
- El 1 del Rayo iba en 32 de las 36 columnas y el 2 del Tenerife en 33. Con dos fijos débiles fallados el mismo día, todo el boleto se cae.
- **Rayo – Valencia según Flashscore:** xG 0,64 del Rayo frente a 0,73 del Valencia, con un 64 % de posesión y 21 remates a 11, pero ninguna ocasión clara. El gol fue de Copete (41'). No fue mala suerte de un dominador: el Rayo no generó para ganar.
- Quedan los partidos del domingo (4, 5, 6, 7, 9, 10, 12, 13, 14). El escrutinio se hará cuando terminen.

## 2. Por qué falló (con datos, no con excusas)

**a) Error de modelo, medido.** En `modelo/revision_j23.py` y `modelo/x_templados.py` se revisaron **843 partidos de Primera fuera de muestra** (walk-forward mensual, 2024-27):

| Favorito según la mesa | Partidos | La mesa daba | Ganó | X dada | X salió |
|---|---|---|---|---|---|
| 33-45 % | 229 | 41,0 % | 41,0 % | 27,2 % | 23,6 % |
| **45-55 %** | **293** | **49,5 %** | **44,0 %** | **25,8 %** | **35,2 %** |
| 55-65 % | 155 | 59,3 % | 61,3 % | 22,2 % | 19,4 % |
| 65-75 % | 83 | 69,5 % | 68,7 % | 17,7 % | 18,1 % |
| 75 %+ | 83 | 83,1 % | 86,7 % | 10,9 % | 4,8 % |

- **El fallo está en el tramo templado.** Cuando la mesa da al favorito entre 45 y 55 %, gana menos de lo que dice y **la X sale 9 puntos más** (35 % frente a 26 %, unas 3,7 desviaciones). Es exactamente el caso del Rayo (54 %).
- **EURO_F no es el culpable.** Mejora el log-loss en las tres temporadas (0,9930→0,9887, 0,9675→0,9673 y 0,9359→0,9195). Con el europeo jugando en casa como favorito (174 partidos), la mesa daba 69,9 % y ganó el 71,3 %. Se mantiene.
- **La T de 1,15 tampoco.** Con T 1,08 sale lo mismo (0,9696 frente a 0,9694). Se mantiene.
- **Segunda (Tenerife – Mallorca):** el mismo ajuste de la X **no mejora** en Segunda (1,0504→1,0512 en validación). El 0-0 de Tenerife no es un sesgo que se repita: el empate tenía un 26 %. Ahí el fallo es de estructura (punto b).

**b) Error de estructura.** Los cuatro huecos del boleto de 18 € (3 dobles y 1 triple) fueron a los partidos más abiertos (Sporting, Getafe, Racing y Girona). Otros tres partidos por debajo del 55 % se jugaron a un solo signo en casi todas las columnas: Rayo 54 %, Tenerife–Mallorca 50 % y Real Sociedad F 55 %. Las sencillas repetían los mismos fijos. Así, un solo fallo en cualquiera de ellos tumbaba las 36 columnas.

## 3. Cambios aplicados (desde la J24)

| Cambio | Qué hace | Prueba | Dónde |
|---|---|---|---|
| **X templada en Primera** | Si el favorito está entre 45 y 60 %, la X se multiplica por 1,20 (después de T) | Se eligió con 2024-25 y mejora las tres temporadas: 0,9887→0,9831, 0,9673→0,9626 y 0,9195→0,9193. En la J23, el Rayo baja de 54 a 52 % y su X sube de 26 a 29 % | `modelo/afinado.py` (`X_TEMPLADA`), tests en `modelo/test_afinado.py` |
| **Fijos protegidos** | Un partido a un solo signo con P < 55 % obliga a poner su segundo signo en al menos 2 sencillas, y el tercero en 1 si pasa del 20 % | En la J23 (12 sencillas): P(≥13) 4,07 % → 4,36 %, P(14) 1/188 → 1/171. Columnas con 1 solo fallo tras el sábado: 1 → 5 | `herramientas/proteccion.py` |
| **Aviso de las casas (opcional)** | Con `--mercado 0.08`, también se protege un fijo donde la mesa supera a las casas en más de 8 puntos. No cambia ninguna probabilidad, solo obliga a cubrir el partido | Se aplica desde la J24 como opción recomendada (Carlos no eligió; puede quitarse cuando quiera). La regla 3 se mantiene: las cuotas no cambian probabilidades | `proteccion.py --mercado` |
| **Fuentes de resultados y alineaciones** | Flashscore.es se lee desde el navegador integrado de la app de escritorio (resultados, alineaciones y crónicas). Desde el contenedor sigue bloqueado | Probado el 22/11 con LaLiga, Segunda y Liga F | `CLAUDE.md` §6 |

**El Pleno no se reparte entre columnas.** Con columnas distintas, cada una gana más con el marcador más probable (P(14+Pleno) = P(columna) × P(marcador)). Si se pone otro marcador en alguna columna, baja su probabilidad y no se gana nada a cambio. En la J23 el 1-1 era el bueno. Repartir el Pleno solo tiene sentido si se juega dos veces la misma columna, y eso resta P(≥13).

**Lo que no se puede prometer.** Con 27 € y unos 10 partidos a un solo signo, la P(14) de la jornada estaba en 1 entre 188. Perder el 14 es lo normal, aun haciéndolo todo bien. Los cambios suben la P(≥13) y reducen el riesgo de que un solo fallo tumbe todo, pero no lo eliminan. El sábado fallaron dos fijos débiles a la vez: ni con la protección habría quedado viva ninguna columna sin fallo (habría que haber acertado el 2 del Rayo y la X del Tenerife juntos, un 5 %).

## Informe del Auditor

- 843 partidos de Primera y 1.029 de Segunda, todos fuera de muestra. El ajuste se eligió solo con 2024-25 y se validó con 2025-26 y 2026-27. ✅
- Los resultados del sábado vienen de Flashscore (clase A: marcador final) y el Pleno se confirmó con Soccerway. ✅
- `proteccion.py` se comprobó sobre la J23: las cuotas se cumplen y no repite columnas del boleto. ✅
- Datos en `datos/revision_j23.json` y `datos/x_templados.json`. ✅

## 4. Fallo por fallo con 10 de 14 terminados (22/11, 18:55)

| Partido | Resultado | Mesa daba a lo que salió | Casas | ¿En el boleto? | Diagnóstico |
|---|---|---|---|---|---|
| Rayo – Valencia | 0-1 (2) | 20 % | 24 % | ❌ (1 fijo) | El Rayo llegaba con 5 puntos de 15. Esa señal ya es regla (R3, mala forma) |
| Tenerife – Mallorca | 0-0 (X) | 26 % | 29 % | ❌ (2 fijo) | Varianza: la mesa y las casas coincidían. La X de Segunda está calibrada |
| Racing – Real Sociedad | 3-2 (1) | 28 % | 30 % | ✅ (doble 1 2) | Bien cubierto |
| Sporting – Las Palmas | 0-2 (2) | 33 % | 28 % | ✅ (triple) | Bien cubierto |
| Alavés – Deportivo | 3-1 (1) | 59 % | 43 % | ✅ | La mesa se apartó 16 puntos de las casas y acertó |
| Real Madrid, Barcelona, Eibar F, Granada F, Real Sociedad F | 1 · 1 · 2 · 2 · 1 | 55-84 % | 64-82 % | ✅ | Favoritos cumplidos |
| Tenerife F – Madrid CFF | 0-3 en el minuto 85 | 17 % | 22 % | (1 fijo) | Aviso del viernes: la mesa daba 63 % y las casas 52 %. Desde el 22/11 ese desajuste obliga a cubrir el partido (R3, aviso de las casas) |

- Con estos 9 partidos, las casas acertaron algo más que la mesa: log-loss 0,806 frente a 0,819. Con tan pocos partidos es una diferencia pequeña.
- Fallos del boleto: 2 de 10, los dos con fijos por debajo del 55 %. **Con las reglas de hoy (R3 y R7), ninguno de esos dos fijos iría en todas las columnas.**
- No sale ninguna regla nueva comprobada: los dos avisos que se vieron (mala forma y desajuste con las casas) ya están codificados.
- Pendientes: Osasuna – Málaga, Getafe – Atlético, Girona – Eibar y el final de Tenerife F – Madrid CFF.

## 5. Cierre de la J23 (lunes 23/11, 07:30)

Resultado final: **1211112X212212** + Pleno 1-1 (Flashscore). Faltaban Osasuna 1-0 Málaga (1, fijo ✅), Getafe 0-3 Atlético (2, doble X2 ✅), Girona 2-1 Eibar (1, doble 1X ✅) y Tenerife F 0-3 Madrid CFF (2, fijo ❌).

- Boleto de 18 € (24 columnas): **máximo 11 aciertos** (1 columna con 11, 5 con 10, 9 con 9). Fallan en todas el 2 del Rayo, la X del Tenerife y el 2 del Tenerife F.
- Sencillas: C7 con **11**, C2 con **10**; el resto 8-9. Premios según el escrutinio oficial.
- Log-loss de los 13 partidos con cuota: mesa 0,851, casas 0,812. Las casas ganan esta jornada.
- Histórico de cuotas (15 partidos): las X salieron un 13 % frente al 23 % esperado y ninguna opción por debajo del 20 % salió (10 casos). Muestra pequeña: no cambia reglas.
- Conclusión de la mesa: los 3 fallos eran fijos por debajo del 55 % o con desajuste mesa-casas. Con R3 (mala forma y aviso de las casas) y la protección de fijos, ninguno iría hoy en todas las columnas. No sale regla nueva.
- Bank: ninguna apuesta de la J23 se marcó como «Apostada», el bank sigue en 500 €. La propuesta D01 (Alavés 1 a 2,30, 10 €) habría ganado 13 €.
