# Jornada 21 · v1 primera pasada · lunes 9/11/2026 · presupuesto 12 €

> Prompt v8. Clubes: `modelo/j21_run.py` sobre `datos/euro_j21.csv` (23.665 partidos), T = 1,05, empates Segunda 1,00 y Liga F 0,85. **Selecciones: precio de baja calidad** (Elo público, ver D). Cuentas: `j21-calculadora-v1.txt`. **Lista y orden sin verificar con el boleto oficial.**

## A. Resumen

- **Jornada de parón:** 9 de Segunda, 4 de Liga F, Bélgica–Italia y, de Pleno, España–Inglaterra. Cierre: sábado 14 a las 14:00 (según webs de pronósticos). **Congelación: sábado 14 a las 11:00.**
- **Boleto: 16 columnas, 2 de ellas con X** (en el Alavés–Eibar femenino). P(14) = 1 entre 2.703. **Pleno: 1-0.**
- **Jornada muy abierta:** fallos esperados con los 14 signos, 7,33; P(14) más baja que en la J19 y la J20.
- **Lo más claro:** Mallorca–Córdoba (65 %) y Almería–Andorra (57 %).
- **Lo más incierto:** Real Sociedad B–Sporting, Oviedo–Girona, Eldense–Sabadell y Real Sociedad–Athletic femenino, todos cerca del 37/25/37.

## B. Por qué estos partidos

Es el **parón de selecciones**, y Loterías hace lo que dice la fase 0: Segunda, Liga F y selecciones. Esta vez son 9 + 4 + 2 (la regla habitual era 10 + 4 + Pleno de selección). El Pleno es **España–Inglaterra**, en línea con la regla de 8 de 14 Plenos con España, Madrid, Barça o Atlético.

## C. Los 14 + Pleno

| # | Partido | P(1) | P(X) | P(2) | En el boleto | Riesgo |
|---|---|---|---|---|---|---|
| 1 | Valladolid – Castellón | 27,2 | 23,2 | 49,5 | 2 | Alto |
| 2 | Real Sociedad B – Sporting | 36,4 | 24,9 | 38,7 | 1 2 | Muy alto |
| 3 | Almería – Andorra | 57,3 | 20,0 | 22,8 | 1 | Moderado |
| 4 | Mallorca – Córdoba | 65,2 | 19,7 | 15,1 | 1 | Bajo |
| 5 | Oviedo – Girona | 36,1 | 27,4 | 36,5 | 1 2 | Muy alto |
| 6 | Tenerife – Ceuta | 49,5 | 24,8 | 25,7 | 1 | Alto |
| 7 | Granada – Las Palmas | 42,2 | 25,1 | 32,7 | 1 | Alto |
| 8 | Eibar – Cádiz | 53,9 | 25,1 | 21,0 | 1 | Moderado |
| 9 | Eldense – Sabadell | 36,0 | 27,6 | 36,4 | 1 2 | Muy alto (Sabadell: 12 partidos en los datos) |
| 10 | Alavés F – Eibar F | 42,5 | 33,0 | 24,5 | 1 X | Alto |
| 11 | Real Sociedad F – Athletic F | 39,2 | 23,5 | 37,3 | 1 2 | Muy alto |
| 12 | Sevilla F – Atlético F | 22,8 | 20,7 | 56,5 | 2 | Moderado |
| 13 | Valencia F – Granada F | 27,9 | 23,1 | 49,0 | 2 | Alto |
| 14 | Bélgica – Italia | 50,7 | 26,2 | 23,0 | 1 | **Muy alto** (sin rating de ninguna de las dos) |
| 15 | **Pleno: España – Inglaterra** | 69,8 | 20,6 | 9,7 | **1-0** | Muy alto (Elo, baja calidad) |

Suma de P(X): 3,44.

## D. Selecciones: cómo se ha puesto el precio

El modelo no tiene partidos de selecciones. Para no inventar:
- **España–Inglaterra:** Elo de eloratings.net del 8/11/2026 (España 2.287, Inglaterra 2.146), más 100 puntos por jugar en casa. Eso da a España un 80 % de «puntuación esperada». Se pasa a 1X2 con un Poisson de **2,4 goles en total (supuesto)**. Con 2,0 o 2,8 goles, España queda entre el 68 % y el 71 %: el supuesto apenas cambia el resultado.
- **Bélgica–Italia:** no se encontró su Elo; la descarga directa de eloratings.net está bloqueada desde el entorno. Se ha supuesto que son iguales, más el campo: **es un precio casi a ciegas.**
- Es probable que el Elo exagere el favoritismo de España. El mercado se mirará en la revisión final, como control.

## E. Datos y huecos

- Añadidos: la jornada 12 de Primera (8 partidos), 2 de Segunda (Cádiz 1-2 Oviedo, Leganés 1-3 Albacete) y 2 de la jornada 10 de Liga F (Eibar 1-2 Real Sociedad; Athletic 1-1 Real Madrid).
- **Faltan:** el resto de la jornada 13 de Segunda (del Girona–Almería y del Sporting–Valladolid solo se sabe el signo; el Granada–Tenerife se aplazó) y el resto de la jornada 10 de la Liga F. Se completan en la revisión final.
- **Liga de cada equipo (comprobado el 9/11):** los recién descendidos (Oviedo, Girona y Mallorca) siguen contando con su nivel de Primera. Probado con datos, en España predice mejor que tratarlos como de Segunda: se deja así.

## G. Boleto v1 · 16 apuestas sencillas · 12 € · Pleno 1-0 en todas

```
 1. 22112111211221     9. 21112111111221
 2. 22112111111221    10. 21111111211221
 3. 22111111211221    11. 22111111112221
 4. 22111111111221    12. 21111111111221
 5. 22112111212221    13. 21112111212221
 6. 21112111211221    14. 21112111112221
 7. 22112111112221    15. 221121112X1221
 8. 22111111212221    16. 221121111X1221
```

| Sistema (12 €) | P(14) | P(≥13) | P(≥12) |
|---|---|---|---|
| A · 4 dobles = C · 16 más probables | 1 entre 2.665 | 0,5 % | 2,6 % |
| B · reducida de 7 dobles | 1 entre 4.311 | 0,4 % | 2,9 % |
| **C + 2 columnas con X · elegido** | **1 entre 2.703** | **0,5 %** | **2,6 %** |

## H. 14 signos + Pleno

`2 2 1 1 2 1 1 1 2 1 1 2 2 1` · **Pleno: 1-0** (15,5 %; conservador 1-0; de varianza M-1). P(14 y Pleno) = 1 entre 17.413.

## I. 5 apuestas sueltas

| Apuesta | Probabilidad |
|---|---|
| Alavés F – Eibar F: menos de 3,5 goles | 93,8 % |
| Marca el Almería (contra el Andorra) | 88,4 % |
| Marca el Mallorca (contra el Córdoba) | 87,2 % |
| Marca el Castellón (en Valladolid) | 82,2 % |
| Marca el Atlético F (en Sevilla) | 81,9 % |

P(las 5) = 48,7 %. Ninguna de selecciones, por la baja calidad de su precio.

## K. Pendiente para la revisión final (sábado 14, antes de las 11:00)

- [ ] Boleto oficial: lista y orden.
- [ ] Resto de la jornada 13 de Segunda y de la jornada 10 de Liga F.
- [ ] Bajas (sobre todo de selecciones: España e Inglaterra).
- [ ] Cuotas y % del público (capturas de quiniela15.com y bet365).

| Versión | Fecha | Qué |
|---|---|---|
| v1 | 9/11/2026 | Primera pasada |

---

# v1.1 · segunda comprobación · martes 10/11/2026

> A petición del usuario se ha vuelto a comprobar todo. Salida: `j21-calculadora-v1.1.txt`.

## Lo que estaba mal en la v1

1. **El orden de los partidos.** En el boleto, **Bélgica–Italia es el 10** y la Liga F va del 11 al 14 (quinielafutbol.info, quiniela15.com y loterias1fuengirola.com coinciden). La v1 lo ponía en el 14: con aquel orden, las columnas se habrían rellenado mal. **No usar las columnas de la v1.**
2. **Faltaban resultados.** Añadidos 6 de la jornada 13 de Segunda: Girona 0-1 Almería, Sporting 1-2 Valladolid, Las Palmas 2-0 Eldense, Córdoba 3-0 Ceuta, Burgos 2-1 Celta Fortuna y Sabadell 0-0 Real Sociedad B. Y uno de la Liga F: Granada 0-1 Espanyol.

## Lo nuevo que hay que saber

- **Tres partidos de la jornada 13 de Segunda se aplazaron:** Castellón–Eibar, Granada–Tenerife y Andorra–Mallorca. No hay motivo oficial; una web lo atribuye a un fallecimiento, pero la fuente es dudosa. Afecta a seis equipos de esta jornada (partidos 1, 3, 4, 6, 7 y 8): llegan con un partido menos y más descanso. **Sin ajuste**, porque no hay nada medido.
- **El Tenerife F–Alavés F de la J20 se aplazó.** El «1» de la combinación oficial de aquel partido salió del sorteo de Loterías, no del juego.
- **Bélgica–Italia:** sigue sin Elo. Control (no entra en el precio): en el ranking FIFA, Bélgica es 8.ª e Italia 15.ª; un mercado de predicciones da 44/18/31 (≈ 47/19/33 normalizado). El precio propio (51/26/23) le da a Italia 10 puntos menos que ese mercado: **riesgo muy alto**, y se mira en la revisión final.

## Precio v1.1 (cambios de más de 1 punto)

| # | Partido | v1 | v1.1 |
|---|---|---|---|
| 5 | Oviedo – Girona | 36,1 / 27,4 / 36,5 | **36,5 / 27,6 / 35,9** (el 1 pasa a ser el signo principal) |
| 14 | Valencia F – Granada F | 27,9 / 23,1 / 49,0 | **29,4 / 24,4 / 46,2** |

El resto se mueve menos de un punto.

## Boleto v1.1 · 16 apuestas sencillas · 12 € · Pleno 1-0 en todas

```
 1. 22111111211122     9. 22112111211222
 2. 22112111211122    10. 21112111111122
 3. 21111111211122    11. 21111111211222
 4. 22111111111122    12. 22111111111222
 5. 21112111211122    13. 21112111211222
 6. 22112111111122    14. 22112111111222
 7. 22111111211222    15. 22111111X11122
 8. 21111111111122    16. 2211111121X122
```

| # | Partido | En el boleto |
|---|---|---|
| 1 | Valladolid – Castellón | 2 |
| 2 | Real Sociedad B – Sporting | 1 2 |
| 3 | Almería – Andorra | 1 |
| 4 | Mallorca – Córdoba | 1 |
| 5 | Oviedo – Girona | 1 2 |
| 6 | Tenerife – Ceuta | 1 |
| 7 | Granada – Las Palmas | 1 |
| 8 | Eibar – Cádiz | 1 |
| 9 | Eldense – Sabadell | 1 X 2 |
| 10 | **Bélgica – Italia** | 1 |
| 11 | Alavés F – Eibar F | 1 X |
| 12 | Real Sociedad F – Athletic F | 1 2 |
| 13 | Sevilla F – Atlético F | 2 |
| 14 | Valencia F – Granada F | 2 |
| 15 | **Pleno: España – Inglaterra** | **1-0** |

Sistema elegido: C + 2 columnas con X. P(14) = 1 entre 2.935 · P(14 y Pleno) = 1 entre 18.902.

**14 signos:** `2 2 1 1 1 1 1 1 2 1 1 1 2 2`

**Sueltas:** Alavés F–Eibar F menos de 3,5 goles (93,6 %), marcan el Almería (88,4 %), el Mallorca (86,9 %), el Castellón (82,1 %) y el Atlético F (81,8 %). P(las 5) = 48,3 %.

| Versión | Fecha | Qué |
|---|---|---|
| v1.1 | 10/11/2026 | Orden corregido (Bélgica–Italia es el 10), 7 resultados nuevos, aplazamientos anotados |

---

# v1.2 · Liga F con la temporada pasada y Elo real de Bélgica e Italia · miércoles 11/11/2026

> Nuevo entorno con acceso a Wikipedia y eloratings.net (aprobado por el usuario). Salida: `j21-calculadora-v1.2.txt`.

## Qué cambia y con qué evidencia

1. **Liga F (partidos 11 a 14):** el modelo usa ahora los **240 partidos de la temporada 2025/26**, partido a partido (`modelo/ligaf_modelo.py`, datos en `datos/ligaf.json`). Antes solo usaba los totales de goles de cada equipo. **Backtest** (jornadas 4 a 10 de esta temporada, 48 partidos fuera de muestra): log-loss **0,976** frente a **1,061** del método anterior. Los 75 resultados de esta temporada que la mesa tenía a mano coinciden con Wikipedia.
2. **Bélgica–Italia (partido 10):** deja de ser un precio a ciegas. Elo de eloratings.net, descargado hoy: **Bélgica 1.956, Italia 1.910**, más 100 por campo → 57,5 / 24,7 / 17,8. Control (no entra en el precio): un mercado de predicciones daba ≈ 47/19/33.
3. **España–Inglaterra:** Elo confirmado en la descarga (España 2.287, Inglaterra 2.146). Sin cambios.

| # | Partido | v1.1 | **v1.2** |
|---|---|---|---|
| 10 | Bélgica – Italia | 50,7 / 26,2 / 23,0 | **57,5 / 24,7 / 17,8** |
| 11 | Alavés F – Eibar F | 42,6 / 32,8 / 24,6 | **48,6 / 32,4 / 19,0** |
| 12 | Real Sociedad F – Athletic F | 39,1 / 23,4 / 37,5 | **57,7 / 21,1 / 21,2** |
| 13 | Sevilla F – Atlético F | 22,9 / 20,8 / 56,3 | **19,5 / 18,5 / 62,0** |
| 14 | Valencia F – Granada F | 29,4 / 24,4 / 46,2 | **32,9 / 23,4 / 43,7** |

## Boleto v1.2 · 16 apuestas sencillas · 12 € · Pleno 1-0 en todas

```
 1. 22111111211122     9. 22111121211122
 2. 22112111211122    10. 22111111X11122
 3. 21111111211122    11. 22112121211122
 4. 22111111111122    12. 21111121211122
 5. 21112111211122    13. 22111121111122
 6. 22112111111122    14. 22112111X11122
 7. 21111111111122    15. 21111111X11122
 8. 21112111111122    16. 21112121211122
```

| # | Partido | En el boleto |
|---|---|---|
| 1 | Valladolid – Castellón | 2 |
| 2 | Real Sociedad B – Sporting | 1 2 |
| 3 | Almería – Andorra | 1 |
| 4 | Mallorca – Córdoba | 1 |
| 5 | Oviedo – Girona | 1 2 |
| 6 | Tenerife – Ceuta | 1 |
| 7 | Granada – Las Palmas | 1 2 |
| 8 | Eibar – Cádiz | 1 |
| 9 | Eldense – Sabadell | 1 X 2 |
| 10 | Bélgica – Italia | 1 |
| 11 | Alavés F – Eibar F | 1 |
| 12 | Real Sociedad F – Athletic F | 1 |
| 13 | Sevilla F – Atlético F | 2 |
| 14 | Valencia F – Granada F | 2 |
| 15 | **Pleno: España – Inglaterra** | **1-0** |

| | v1.1 | **v1.2** |
|---|---|---|
| P(14) | 1 entre 2.935 | **1 entre 1.577** |
| P(14 y Pleno) | 1 entre 18.902 | **1 entre 10.155** |
| P(≥13) | 0,4 % (1 entre 250) | **0,7 % (1 entre 143)** |
| P(≥12) | 2,4 % | **3,7 %** |

Sistema elegido: C (las 16 columnas más probables). **14 signos:** `2 2 1 1 1 1 1 1 2 1 1 1 2 2`.

**Sueltas:** Alavés F–Eibar F, menos de 3,5 goles (94,1 %); marcan el Almería (88,4 %), el Mallorca (86,9 %), el Atlético F (85,9 %) y el Castellón (82,1 %). P(las 5) = 51,0 %.

**Por qué sube tanto P(14):** el nuevo modelo de la Liga F distingue mejor a los equipos y da favoritos más claros en tres de los cuatro partidos, y el backtest dice que esos favoritos están justificados. No es optimismo: es un modelo que acierta más con datos que no había visto.

| Versión | Fecha | Qué |
|---|---|---|
| v1.2 | 11/11/2026 | Liga F con la temporada pasada (backtest 1,061 → 0,976) y Elo real de Bélgica e Italia |

---

# v1.3 · noticias del miércoles 11/11/2026 · la mesa al completo, con foco en el Pleno

> Búsquedas del día (Live Trader, Calendario, Contexto). Salida: `j21-calculadora-v1.3.txt`. **El boleto no cambia.**

## Pleno: España – Inglaterra (domingo 15, estadio Metropolitano)

| Hecho | Clase | Fuente | Efecto |
|---|---|---|---|
| España sin **Rodri** ni **Dani Olmo** | B | Convocatoria del 6/11 (meridiano.net, sportaragon.com) | Ataque de España ×0,97 |
| Inglaterra sin **Guéhi** (central titular); entra Dan Burn | B | ESPN, englandfootball.com (9/11) | Goles de España ×1,02 |
| Pickford, portero titular de Inglaterra | B | englandfootball.com | — |
| Las dos juegan el **jueves 12**: España en Praga, Inglaterra contra Croacia en Wembley | B | Varias | **Aviso:** si el jueves alguna se clasifica, puede rotar el domingo. Se mira el sábado |
| Inglaterra es segunda del grupo A3 y solo perdió con España | B | englandfootball.com | Contexto, sin efecto en el precio |

**Precio del Pleno:** 69,3 / 20,8 / 9,8. **Resultado más probable: 1-0 (15,7 %).** Le siguen M-0 (14,7 %) y 2-0 (14,1 %). Como el M-0 está a solo 1 punto, **el sábado se juega el que menos juegue el público** (fase 7). P(14 y Pleno) = 1 entre 10.073.

## Bélgica – Italia (partido 10)

- **Courtois** no juega la Nations League (portero titular). Es una baja larga y el Elo ya incluye partidos sin él: **sin ajuste**, para no contarla dos veces.
- Debast y Openda, posibles bajas (clase C: lista de plantilla sin fecha fiable). Sin efecto.
- De Bruyne y Lukaku, convocados; vuelve Doku.
- Italia: no se han encontrado noticias de noviembre. `pendiente`.

## Segunda

- **Granada:** bajas de Pau Casadesús y Baïla Diallo (B, futbolfantasy.com). Posición sin comprobar: aviso, sin ajuste.
- **Las Palmas:** José Arnáiz, duda (B).
- **Castellón** (Ousmane Camara) y **Almería** (João Carvalho): datos de clase C, sin fecha fiable. Solo aviso.

## Liga F

No se han encontrado noticias de la jornada.

## Pendiente para el sábado 14 (congelación a las 11:00)

1. **Resultados del jueves** de España e Inglaterra, y si alguna ya está clasificada (posibles rotaciones).
2. **Boleto oficial, % del público y cuotas** con Claude in Chrome (`navegador/encargo-claude-in-chrome.md`). **Deciden el Pleno** (1-0 frente a M-0) y la columna del público.
3. Bajas de última hora y onces probables de las selecciones.

| Versión | Fecha | Qué |
|---|---|---|
| v1.3 | 11/11/2026 | Noticias del día; ajuste del Pleno por Rodri, Olmo y Guéhi. Boleto y Pleno sin cambios |

---

# v1.4 · 11/11/2026 · auditoría de empates y cartera de 8 boletos (72 €, pedida por el usuario)

## Auditoría de empates (`modelo/auditoria_empates.py` y `auditoria_empates_2.py`)
Validación que avanza en el tiempo: el modelo se reajusta cada mes y predice el mes siguiente.
- **Primera y Segunda, 1.834 partidos fuera de muestra:** empates reales 25,2 %, probabilidad dada por el modelo 25,0 %. En total están bien medidos.
- **Por tramos:** en los partidos igualados el modelo se queda 1–2 puntos corto, y en los desiguales da de más (15,9 % frente a 8,7 % real).
- **Alternativas probadas** (elegidas con 2024-25 y probadas con 2025-26 y 2026-27):
  - Dixon-Coles con rho de −0,05 a −0,15;
  - factores de empate de 1,00 a 1,15;
  - recalibración de P(X) según lo igualado del partido.
  **Ninguna mejora fuera de muestra** (1,0107 actual frente a 1,0110–1,0196). No se aplica ninguna.
- **Liga F, 54 partidos fuera de muestra:** empates reales 22,2 %. Factor 0,85 → 21,5 % dado; 0,90 → 22,5 %; 1,00 → 24,4 %. El 0,85 y el 0,90 empatan en log-loss. Se mantiene.
- **Conclusión:** la X está bien medida. El problema está en el boleto:
  - P(ningún empate en los 14) = 2,0 %, y se esperan 3,4 empates;
  - el boleto de 16 columnas solo cubre la X en un partido.
  Con 96 columnas la X queda cubierta en 6 partidos.

## Cartera de 8 boletos (`herramientas/cartera.py`, salida en `j21-cartera-72.txt`)
- **Sistema:** 4 de 12 € y 4 de 6 €, con 96 columnas distintas (sin repetir), por orden de probabilidad.
- **Comparación:** C (las 96 más probables) frente a F (completo de 5 dobles y 1 triple). Por el criterio fijo gana **C**.
- **Probabilidades:** P(14) 1 entre 350; P(≥13) 2,46 %; P(≥12) 10,0 %.
- **Pleno:** 1-0 en los boletos de 12 € y M-0 en los de 6 €. Entonces P(14 y Pleno) = 1 entre 2.268, frente a 1 entre 2.228 con todo 1-0. Se confirma el sábado con el % del público.

---

# v1.5 · 11/11/2026 · investigación partido a partido y recomendación de la mesa

**Los datos están al día.** Las clasificaciones de los datos de la mesa coinciden con la prensa:
- Segunda: Almería 29 pts, Castellón 27 con un partido menos, Ceuta último con 5.
- Liga F: Barça 27, Valencia F colista con 6, Sevilla F 13.º con 10.

**Hechos nuevos.** Ninguno es de clase A/B sobre un jugador clave, así que **no se mueve ningún precio**:
- **Tenerife:** falleció su jugador **Jesús de Miguel**, y la J13 de Segunda quedó en parte aplazada (Granada–Tenerife y Castellón–Eibar). Contexto emocional, sin efecto medible.
- **Ceuta:** destituido Romero; llega **Sergio Lobera**. Último con 5 puntos y −20 de diferencia de goles. Cambio de entrenador: aviso, no mueve el precio.
- **Oviedo:** destituido Julián Calero tras ganar 1-2 en Cádiz; **Raúl González debuta contra el Girona** (sábado a las 21:00). Aviso.
- **Sporting** (fotmob, clase C): Casas lesionado, Otero sancionado; dudas de Gelabert, Pablo García y Konrad de la Fuente. Si el sábado se confirman (clase A/B), el Live Trader revisa el partido 2.
- **Girona** (jornadaperfecta, sin fecha, clase C): posibles sanciones de David López y Rubén Pulido; Bryan Gil lesionado.
- **Italia:** juega el jueves 12 contra Francia en Milán y el domingo en Bruselas. Zaniolo deja la concentración. Italia es 2.ª del grupo con 7 puntos y Bélgica 3.ª con 6.
- **Integridad:** no hay ninguna noticia de investigación ni de movimientos raros en estos partidos → nivel 1 (sin indicios).

**Recomendación técnica de la mesa:**
- Valor esperado por euro ≈ 0,77 (negativo) con cualquier número de boletos. Jugar más solo sube la probabilidad en proporción.
- **No hay razón técnica para pasar de 12 €.**
- Con 12 €: boleto 1 de la cartera. Si el usuario decide jugar más, se juega en el orden de la cartera, sin repetir columnas.

---

# v1.6 · 11/11/2026 · 4 boletos de formato oficial (máximo 20 € cada uno)

- **Herramienta:** `herramientas/boletos_oficiales.py`. Salida en `j21-boletos-oficiales.txt`.
- **Formatos de Loterías (loteriasyapuestas.es, «Quinielas reducidas»):**
  - Reducida 1: 4 triples, 9 apuestas, 6,75 €.
  - Reducida 2: 7 dobles, 16 apuestas, 12 €.
  - Reducida 3: 3 dobles + 3 triples, 24 apuestas, 18 €.
  - Directas.
- **Criterio:** cada boleto es de un formato distinto y el que más P(14) nueva añade por euro.
- **Elegidos:**
  - Directa de 4 dobles (12 €).
  - Directa de 3 dobles + 1 triple (18 €).
  - Reducida 1 (6,75 €).
  - Reducida 3 (18 €).
- **Los 4 juntos:** 54,75 €; P(14) 1 entre 542; P(≥12) 9,0 %.
- **La Reducida 2 (7 dobles)** no entra: P(14) 1 entre 2.770 por 12 €, frente a 1 entre 1.583 de los 4 dobles directos al mismo precio.

---

# v1.7 · 11/11/2026 · rescate de «quiniela-mesa»: selecciones con el modelo validado

Detalle: `analisis/rescate-quiniela-mesa.md`. Salida: `j21-calculadora-v1.7.txt` y `j21-boletos-oficiales-v1.7.txt`.

| Nº | Partido | v1.6 | **v1.7** | Motivo |
|---|---|---|---|---|
| 10 | Bélgica – Italia | 57,5 / 24,7 / 17,8 | **50,9 / 24,1 / 25,0** | Poisson de selecciones (log-loss en prueba 0,795 frente a 0,810 del Elo) |
| 15 | España – Inglaterra | 69,3 / 20,8 / 9,8 | **52,7 / 24,6 / 22,6** | Ídem, con las bajas de clase B (Rodri, Olmo y Guéhi) |

- **Pleno:** 1-0 11,9 % y 1-1 11,7 % casi empatados. **El sábado se juega el que menos juegue el público.**
- **Datos:** se añaden Tenerife 2-2 Andorra y 3 partidos de Champions. Los precios de los clubes cambian menos de 0,3 puntos.
- **4 boletos de 20 € como máximo:** mismos formatos y mismos dobles y triples que en la v1.6. Los 4 juntos (54,75 €): P(14) 1 entre 609, P(≥12) 8,3 %.
- **Retorno:** se corrige el «0,77 € por euro». La Quiniela devuelve de media unos 0,55 € por euro jugado.

---

# v1.8 · jueves 12/11/2026 · primer repaso completo con el acceso a las webs

**Datos nuevos:**
- quiniela15.com: % LAE del público y orden oficial. **Coincide con el nuestro.**
- jornadaperfecta.com: lesionados y sancionados de la próxima jornada, leídos hoy.

**Bajas aplicadas** (clase B, tope del 5 %; portero titular sancionado hasta un 5 %):

| Nº | Partido | Ajuste |
|---|---|---|
| 1 | Valladolid – Castellón | Valladolid sin Latasa (lesión) ni Iván Alejo (sanción): ataque ×0,96. Castellón sin Orozco (roja): ×0,98 |
| 2 | Real Sociedad B – Sporting | Sporting sin Juan Otero (roja) ni Antonio Casas (grado 3): ataque ×0,95 |
| 3 | Almería – Andorra | Andorra sin su portero Owono (roja) ni Lautaro de León (doble amarilla): Almería ×1,05 y Andorra ×0,99 (Marcos Luna, del Almería, sancionado) |
| 6 | Tenerife – Ceuta | Tenerife sin su portero Dani Martín (doble amarilla): Ceuta ×1,05 |

**Estadístico:**
- Favoritos de Segunda: el modelo da un poco menos de lo real (47,2 % frente a 52,1 % en 2026/27, n = 119, dentro del ruido). Subir la temperatura no mejora la prueba: T = 1,05 sigue siendo la mejor (1,0513).
- **El 78 % del público en el Almería, o el 73 % en el Tenerife, es el sesgo hacia el favorito.**
- En **Primera**, T = 1,15–1,20 mejora la validación y la prueba (0,9630 → 0,9607). **Se aplicará en la próxima jornada con Primera.**

**Pleno:**

| Marcador | Modelo | Público estimado | Valor |
|---|---|---|---|
| **1-0** | 11,9 % | ≈2,8 % | **4,3** |
| 1-1 | 11,7 % | 10,4 % | 1,1 |
| 2-1 (lo que más juega el público) | 9,6 % | 26 % | 0,37 |

- El público estimado sale de multiplicar los % de goles de cada equipo que da LAE.
- **Pleno 1-0 en los 4 boletos.**

**Boletos:** mismos formatos. Los 4 juntos: P(14) 1 entre 598; P(≥12) 8,4 %. Ninguno contiene la columna del público (22111111111121).

**Pendiente:**
- resultados del jueves (selecciones);
- revisión del sábado a las 9:00 (bajas de última hora y % definitivos);
- congelación a las 11:00.
