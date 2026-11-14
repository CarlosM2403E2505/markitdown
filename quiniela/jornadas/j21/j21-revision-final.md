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
