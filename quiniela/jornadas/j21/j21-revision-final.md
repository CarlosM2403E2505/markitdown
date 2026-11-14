# J21 · Revisión a fondo de la mesa y boleto único (sábado 14/11/2026)

Pedido por el usuario: rehacer la revisión con cada profesional cumpliendo su tarea, **un solo boleto de hasta 20 €** y la máxima probabilidad de **13 o más**. Manda la mesa, no el público (anexo H).

## Cada profesional, con su tarea

| Profesional | Qué ha hecho | Resultado |
|---|---|---|
| **Director** | Lista y orden oficial (quiniela15 = la nuestra), cierre a las 14:00, un boleto ≤ 20 € | ✅ |
| **Data Analyst** | Últimos partidos de los 26 equipos | Selecciones: los 4 del jueves están dentro. Clubes: datos hasta el 9/11 más Tenerife 2-2 Andorra. Copa del Rey entre semana: el Pamplona–Eibar se aplazó el 3/11 y su nueva fecha no está confirmada. No hay ningún otro partido de equipos de la J21 entre el 10 y el 13/11 confirmado |
| **Live Trader** | Bajas de hoy | Ver la tabla de abajo. Sin cambios en Segunda ni en la Liga F (no se encontraron bajas). España: Lamine Yamal y Oyarzabal se perdieron el partido de Praga y se espera que lleguen el domingo, sin confirmación oficial (**clase C: no mueve**) |
| **Calendario y fatiga** | Copa entre semana | Ninguno de los equipos de la J21 jugó Copa en la semana, salvo, quizá, el Eibar (sin comprobar). Solo aviso |
| **Táctico y Contexto** | Contexto sin números | Oviedo (Raúl González) y Ceuta (Lobera) estrenan entrenador: regresión a la media, sin ajuste. El Tenerife juega su primer partido en casa tras la muerte de Jesús de Miguel. España (15 puntos) e Inglaterra (12) se juegan el primer puesto. Bélgica (9), Italia (10) y Francia (10) se juegan el grupo |
| **Odds Compiler** | Precio final | Modelo de clubes y Liga F más el de selecciones, con los ajustes A/B de abajo |
| **Integridad** | Movimientos raros | Ninguna noticia. Nivel 1 |
| **Market Analyst** | Control | El público carga a los favoritos (Almería 84 %, Tenerife 78 %). Solo informativo |
| **Risk Analyst** | Riesgo | Muy alto: partidos 2, 5 y 9. Alto: 1, 6, 7, 11 y 14. Datos flojos: Sabadell (13 partidos); Tenerife, Andorra, Ceuta, Eldense y Real Sociedad B (unos 55) |
| **Red Team** | Contra cada signo fijo | Ver la sección de los 15 |
| **Pleno Specialist** | Pleno | 1-0 (12,2 %). Conservador: 1-0. Varianza: M-1 (8,3 %) |
| **Portfolio** | Boleto único | `herramientas/boleto_unico.py`: 16 formatos comparados (ver abajo) |
| **Auditor** | Revisión | Coste 18 € ≤ 20 €. P(14), P(≥13) y P(≥12) recalculadas con `evaluar_columnas`. Nombres de los equipos en cada fila |

## Bajas que mueven el precio (clase B, jornadaperfecta, 12 y 14/11)

| Nº | Partido | Ajuste |
|---|---|---|
| 1 | Valladolid – Castellón | Valladolid sin Latasa ni Alejo (×0,96); Castellón sin Orozco (×0,98) |
| 2 | Real Sociedad B – Sporting | Sporting sin Juan Otero ni Antonio Casas (×0,95) |
| 3 | Almería – Andorra | Andorra sin el portero Owono ni Lautaro de León (Almería ×1,05; Andorra ×0,99) |
| 6 | Tenerife – Ceuta | Tenerife sin el portero Dani Martín (Ceuta ×1,05) |
| 7 | Granada – Las Palmas | Las Palmas sin Sandro Ramírez (×0,97) |
| 15 | España – Inglaterra | España sin Rodri ni Olmo (×0,97); Inglaterra sin Guéhi (×1,02 a los goles de España) |

## Deliberación del boleto (objetivo: P(≥13), pedido por el usuario)

Salida completa en `j21-boleto-unico.txt`. Los mejores:

| Candidato | Coste | P(14) | **P(≥13)** | P(≥12) | Comentario |
|---|---|---|---|---|---|
| 26 columnas sencillas | 19,50 € | 1 entre 1.136 | **0,93 %** | 4,7 % | No cabe en un boleto: el máximo son 8 apuestas sencillas por boleto. Serían 4 boletos y el usuario pidió uno |
| **Directa: 3 dobles + 1 triple** | **18 €** | **1 entre 1.273** | **0,85 %** | 4,3 % | **ELEGIDO**: un solo boleto y el mejor P(≥13) de los que caben en uno |
| Reducida 3 oficial | 18 € | 1 entre 2.113 | 0,81 % | 4,9 % | Más premios de 10 a 12, pero menos 13 y 14 |
| Directa: 1 doble + 2 triples | 13,50 € | 1 entre 1.616 | 0,71 % | 3,8 % | |
| Directa: 4 dobles | 12 € | 1 entre 1.777 | 0,63 % | 3,3 % | |
| Reducida 2 (7 dobles) | 12 € | 1 entre 3.143 | 0,57 % | 3,7 % | |

**Honestidad:** ningún boleto de 20 € asegura un 13. La «garantía al 13» de las reducidas solo vale si aciertas todos los partidos fijos y cada resultado cae dentro de lo marcado. Con este boleto, la probabilidad de hacer 13 o más es del 0,85 % (1 entre 118).

## El boleto (directa, 24 apuestas, 18 €)

| Nº | Partido | Signo |
|---|---|---|
| 1 | Valladolid – Castellón | 2 |
| 2 | Real Sociedad B – Sporting | **1 2** |
| 3 | Almería – Andorra | 1 |
| 4 | Mallorca – Córdoba | 1 |
| 5 | Oviedo – Girona | **1 2** |
| 6 | Tenerife – Ceuta | 1 |
| 7 | Granada – Las Palmas | **1 2** |
| 8 | Eibar – Cádiz | 1 |
| 9 | Eldense – Sabadell | **1 X 2** |
| 10 | Bélgica – Italia | 1 |
| 11 | Alavés F – Eibar F | 1 |
| 12 | Real Sociedad F – Athletic F | 1 |
| 13 | Sevilla F – Atlético F | 2 |
| 14 | Valencia F – Granada F | 2 |
| 15 | Pleno: España – Inglaterra | **1-0** |

P(14) 1 entre 1.273 · P(≥13) 0,85 % · P(≥12) 4,3 % · P(≥10) 31,0 % · P(14 y Pleno) ≈ 1 entre 10.430.

---

# v2.1 · Deliberación sobre el 14 y los empates (sábado 14/11)

## Techo honesto de P(14)

P(14) de un boleto = suma de las probabilidades de sus columnas. Con nuestras probabilidades:

| Columnas (coste) | Mejor P(14) posible |
|---|---|
| 24 (18 €) | 1 entre 1.218 |
| 26 (19,50 €, el máximo con 20 €) | **1 entre 1.136** |
| 31 (23,25 €) | 1 entre 1.000 |
| 71 (53,25 €) | 1 entre 500 |

Con 20 € no se puede bajar de 1 entre 1.136. Para mejorar de verdad hace falta una de dos cosas:
- **probabilidades más afiladas**, es decir, mejores datos (ver los expertos nuevos);
- **más columnas**, que es decisión del usuario.

## Empates: lo que se ha medido

- **P(X) por partido:**

  | Partido | P(X) |
  |---|---|
  | Alavés F – Eibar F | **32,4 %** |
  | Eldense – Sabadell | **28,4 %** |
  | Oviedo – Girona | 27,6 % |
  | Real Sociedad B – Sporting | 25,5 % |
  | Granada – Las Palmas | 25,3 % |
  | Eibar – Cádiz | 25,1 % |

- **En la jornada:** se esperan 3,4 empates; la probabilidad de que no haya ninguno es del 2 %.
- **Lo que cuesta cubrir la X:** en ningún partido la X es el resultado más probable. Por eso cada X cubierta cuesta P(14). Se compararon 18.810 diseños de un boleto (formatos 3 dobles + 1 triple, 1 doble + 2 triples, 4 dobles y 2 dobles + 1 triple, con dobles 12, 1X o X2):

  | Diseño | X cubierta en | P(14) | P(≥13) | P(todas las X cubiertas) |
  |---|---|---|---|---|
  | Máximo P(14) | 1 partido | 1 entre 1.273 | 0,85 % | 2,9 % |
  | **X en los 2 partidos con más empate** | **2** | **1 entre 1.339 (95 % del máximo)** | **0,82 %** | 4,2 % |
  | X en los 3 con más empate | 3 | 1 entre 1.501 (85 %) | 0,75 % | — |
  | X en 4 partidos | 4 | 1 entre 1.744 (73 %) | 0,66 % | 7,8 % |

## Decisión de la mesa: regla del empate (nueva)

- **Regla:** se cubre la X en los partidos con más probabilidad de empate, mientras la P(14) del boleto se mantenga **≥ 90 % de la máxima** de ese formato.
- **Esta jornada:** X en **Eldense – Sabadell** (triple) y en **Alavés F – Eibar F** (1X). La tercera (Oviedo – Girona) bajaría al 85 %: no entra.

## Boleto final v2.1 (directa, 24 apuestas, 18 €)

| Nº | Partido | Marca |
|---|---|---|
| 1 | Valladolid – Castellón | 2 |
| 2 | Real Sociedad B – Sporting | **1 2** |
| 3 | Almería – Andorra | 1 |
| 4 | Mallorca – Córdoba | 1 |
| 5 | Oviedo – Girona | **1 2** |
| 6 | Tenerife – Ceuta | 1 |
| 7 | Granada – Las Palmas | 1 |
| 8 | Eibar – Cádiz | 1 |
| 9 | Eldense – Sabadell | **1 X 2** |
| 10 | Bélgica – Italia | 1 |
| 11 | Alavés F – Eibar F | **1 X** |
| 12 | Real Sociedad F – Athletic F | 1 |
| 13 | Sevilla F – Atlético F | 2 |
| 14 | Valencia F – Granada F | 2 |
| 15 | Pleno: España – Inglaterra | **1-0** |

## Informe del Auditor

| Comprobación | Resultado |
|---|---|
| Apuestas y coste | 24 apuestas distintas, **18,00 €** ≤ 20 € ✅ |
| P(14) por dos métodos (producto por partido y suma de las 24 columnas) | 1 entre 1.339 en los dos ✅ |
| Distribución exacta (`evaluar_columnas`) | P(≥13) 0,825 %, P(≥12) 4,25 %, P(≥11) 13,6 %, P(≥10) 30,9 % ✅ |
| P(14 y Pleno 1-0) | 1 entre 10.978 ✅ |
| Nombres de los equipos en cada fila | ✅ |
| Bajas aplicadas: solo A/B, con fuente y tope del 5 % | ✅ (6 partidos, ver arriba) |
| Fuentes de los 4 resultados del jueves | Chequia–España con 2 fuentes; los otros 3 con 1 (futboltotal, clase B) ⚠️ Anotado |
| El público no ha intervenido (anexo H) | ✅ |
| Pendiente | Lamine Yamal y Oyarzabal (clase C, sin efecto) y el Pamplona–Eibar de Copa (sin confirmar) ⚠️ |

---

# v2.2 FINAL y CERRADA · Un boleto de 18 € frente a dos de 12 € + 6 €

**Cambio pedido por el usuario:** los empates **no son una regla fija**. La mesa decide en cada partido si cubre la X.

| Opción (18 € en total) | P(14) | P(≥13) | P(≥12) | P(≥10) | X cubiertas (decidido por la mesa) |
|---|---|---|---|---|---|
| A. Un boleto: directa de 3 dobles + 1 triple | 1 entre 1.274 | 0,855 % | 4,35 % | 31,1 % | Eldense – Sabadell |
| **B. Dos boletos: 12 € (4 dobles) + 6 € (8 sencillas nuevas)** | **1 entre 1.224** | **0,875 %** | **4,44 %** | **31,4 %** | **Oviedo – Girona (2 columnas) y Eldense – Sabadell (3)** |

- **Decisión: B.** Al mismo precio, es mejor en todo.
- **Por qué:** las 8 sencillas del segundo boleto van justo a las combinaciones que el primero no cubre. Entre ellas están las X donde la mesa ve probabilidad.

**Informe del Auditor:**
- 24 apuestas distintas, 0 repetidas entre los dos boletos y 18,00 € en total.
- P(14) = suma de las 24 columnas = 1 entre 1.224.
- P(≥13) por simulación con 600.000 jornadas = 0,875 %.
- Pleno 1-0 en los dos boletos.
- Nombres de los equipos en cada fila. ✅
