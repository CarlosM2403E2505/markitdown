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
