# J20 — PRONÓSTICO (Primera, Segunda y Liga F, sábado 7 y domingo 8 de noviembre de 2026)

## v0 · Arranque de la mesa (miércoles 4/11, 19:00 de Canarias)

### Decisiones del usuario (4/11)
| Qué | Decisión |
|---|---|
| Presupuesto | **18 € (12 + 6), 24 apuestas**, como en la J19. Presupuesto fijo, nunca para recuperar |
| Sellado | **Sábado 7/11 por la mañana.** Regla R1: el sábado solo cambian noticias de clase A y siempre antes de las 11:00 de Canarias. La mesa entrega el boleto final el viernes por la tarde |
| Administración | **Horario continuo** (punto de la lista de control resuelto) |

### Los 15 partidos (horas peninsulares; Canarias = −1)
| Nº | Partido | Competición | Día |
|---|---|---|---|
| 1 | Málaga – Racing | Primera | sáb 14:00 |
| 2 | Osasuna – Athletic | Primera | sáb 18:30 |
| 3 | Valencia – Real Madrid | Primera | sáb 21:00 |
| 4 | Elche – Betis | Primera | dom 14:00 |
| 5 | Real Sociedad – Rayo | Primera | dom 16:15 |
| 6 | Celta – Levante | Primera | dom 18:30 |
| 7 | Villarreal – Getafe | Primera | dom 18:30 |
| 8 | Cádiz – Oviedo | Segunda | sáb 16:15 |
| 9 | Girona – Almería | Segunda | dom 16:15 |
| 10 | Sporting – Valladolid | Segunda | dom 18:30 |
| 11 | Athletic F – Real Madrid F | Liga F | sáb 16:00 |
| 12 | Logroño F – Sevilla F | Liga F | dom 12:00 |
| 13 | Eibar F – Real Sociedad F | Liga F | sáb 17:15 |
| 14 | Tenerife F – Alavés F | Liga F | dom 13:00 |
| 15 | **Pleno: Atlético – Barcelona** | Primera | dom 21:00 |

Fuente: [Quinielafutbol.info](https://www.quinielafutbol.info/proximas-jornadas-de-la-quiniela.html). Bote de 2,2 M€ al Pleno, según esa web; pendiente de fuente oficial (Trader).

### Mediciones nuevas que cambian el método (4/11)
| Medición | Resultado | Decisión |
|---|---|---|
| Empates en Primera, partidos igualados (diferencia P1−P2 < 0,15) | X real 31,2% frente al 27,0% previsto (189 partidos fuera de muestra). Validación temporal: el factor elegido con datos hasta 07/2026 (1,18) mejora el log-loss en 07–11/2026 (X real 30,3% frente al 25,2%) | **Factor de empates 1,20 en los partidos igualados de Primera.** El resto, 1,08 |
| Empates en Segunda | X real 24,2% frente al 24,9% previsto; en los igualados, 24,1% frente al 26,0% | Sin cambio (1,08) |
| ¿El veto "viene de perder en Europa" vale para la liga? | En la liga, los favoritos que perdieron en Europa en los 5 días anteriores ganaron 4,5 puntos más de lo esperado (346 partidos); los que ganaron o empataron en Europa, +7,3 (546) | **El veto no se aplica a los partidos de liga.** Además, el modelo infravalora en la liga a los equipos que juegan en Europa |
| Dobles candidatos | Regla del 4/11 (registro de errores, §5) | **12, 1X y X2**; los elige la regla de valor |

### Precio v0 (modelo con datos hasta el 1/11; sin noticias ni ajustes; NO es para jugar)
| Nº | Partido | 1 · X · 2 | Goles esperados |
|---|---|---|---|
| 1 | Málaga – Racing | 47,4 · 23,4 · 29,3 | 1,94 – 1,49 |
| 2 | Osasuna – Athletic | 38,9 · **30,2** · 30,9 | 1,37 – 1,19 |
| 3 | Valencia – Real Madrid | 21,9 · 23,4 · 54,7 | 1,14 – 1,93 |
| 4 | Elche – Betis | 39,0 · **28,6** · 32,4 | 1,49 – 1,34 |
| 5 | Real Sociedad – Rayo | 50,0 · 25,0 · 25,0 | 1,75 – 1,17 |
| 6 | Celta – Levante | 53,3 · 24,4 · 22,3 | 1,81 – 1,09 |
| 7 | Villarreal – Getafe | 58,7 · 24,1 · 17,2 | 1,81 – 0,86 |
| 8 | Cádiz – Oviedo | 28,3 · **29,0** · 42,7 | 1,04 – 1,34 |
| 9 | Girona – Almería | 51,2 · 24,0 · 24,8 | 1,87 – 1,24 |
| 10 | Sporting – Valladolid | 51,5 · 25,4 · 23,2 | 1,71 – 1,06 |
| 11 | Athletic F – Real Madrid F | 21,2 · 18,1 · 60,6 | 1,17 – 2,10 |
| 12 | Logroño F – Sevilla F | 34,8 · **28,1** · 37,1 | 0,95 – 0,99 |
| 13 | Eibar F – Real Sociedad F | 36,6 · 27,5 · 35,9 | 1,01 – 0,99 |
| 14 | Tenerife F – Alavés F | 61,3 · 23,5 · 15,2 | 1,46 – 0,58 |
| 15 | Atlético – Barcelona | 37,4 · 24,5 · 38,0 | 1,89 – 1,90 |

- **Empates esperados entre los 14: 3,55.**
- Pleno, primera foto: 1-1 (9,7%), 2-2 (7,8%), M-1 (7,7%), M-M (7,7%).
- Liga F: solo J1–J8 (56 partidos sin el Barça); falta la J9.

### Mesa en marcha (fase 1)
| Agente | Encargo |
|---|---|
| Científico de datos | Dataset hasta el 4/11, Liga F J9–J10 y nombres |
| Investigador | Forma, último partido, semana europea, sanciones, lesiones con fecha, cambios grandes, historial, señales de empate y por qué Loterías eligió cada partido |
| Compilador y Trader | Cuotas (control), % del público, X con valor, Pleno, sueltas, cierre oficial, bote y calendario de noticias |

Ejecutor: /home/claude/j20_run.py. Precio v0: scratchpad/mesa_j20/j20_v0.json.

---

## v1 · Primera pasada completa (miércoles 4/11, noche)

**Quién trabajó:**
- Científico de datos: dataset con 23.649 partidos, hasta el 4/11; Liga F J9 completa; Tenerife F 2-0 Athletic F confirmado.
- Investigador: los 15 partidos.
- Compilador y Trader: cuotas, público, cierre y bote.
- Director: mediciones nuevas y boletos.

### Medición nueva: los equipos que juegan en Europa, infravalorados en la liga
- **El dato:** en partidos de liga entre un equipo que juega en Europa (UEFA en los últimos 120 días) y otro que no, el europeo gana 7–8,5 puntos más de lo esperado (3.434 partidos, fuera de muestra).
- **La corrección:** el factor óptimo es ×1,12 a los goles del europeo y ÷1,12 a los del rival. Lo validé por tiempo: elegido con datos hasta 07/2026, mejora el log-loss en 07–11/2026, que pasa de 0,8645 a 0,8414.
- **En la J20 se aplica a:** Real Madrid (P3), Betis (P4), Real Sociedad (P5) y Celta (P6). No se aplica en P7 ni en P15, porque los dos equipos juegan en Europa.
- **Cansancio:** el cansancio por jugar en Europa entre semana **no se aplica**. Los europeos rinden igual de bien después de jugar en Europa: +4,5 puntos si perdieron y +7,3 si ganaron o empataron.

### Cierre y bote (Trader)
| Concepto | Peninsular | Canarias |
|---|---|---|
| Primer partido | sáb 14:00 | 13:00 |
| Cierre en la administración (estimado; el aviso de LAE aún no está publicado) | ≈14:00 | ≈13:00 |
| **Eduardo Losilla, particulares** | **13:00** | **12:00** |
| **Límite de la mesa** | — | **10:30–11:00** |

- **El rechazo de la J18 (a las 12:01 de Canarias) coincide con el cierre de Losilla para particulares, que es una hora antes del primer partido.** Lección: la hora que manda es la del canal por el que se sella.
- **Bote de 2,2 M€:** lo dan Quiniela15 y Losilla. No hay todavía fuente oficial.

### Precio v1
Modelo con el factor europeo y la regla de empates, más las bajas con fecha. Ajustes aplicados:
- P2: Athletic sin Guruzeta ni Sannadi, sus dos 9 (2: −2); Osasuna sin Oroz (1: −1).
- P4: Betis sin Cucho (2: −2).
- P6: Celta sin Borja Iglesias (1: −3).
- P15: Barça sin Rodri (2: −2).

| Nº | Partido | Mesa 1 · X · 2 | Mercado (control) | Público | Diferencia ≥7 | Revisión escrita |
|---|---|---|---|---|---|---|
| 1 | Málaga – Racing | 47,4 · 23,4 · 29,3 | 39,9 · 26,3 · 33,9 | 41 · 30 · 29 | 7,5 en el 1 | Parcial: recién ascendidos y el Málaga sin ganar en 11 jornadas. La fuerza del modelo sale de Segunda. Mismo signo |
| 2 | Osasuna – Athletic | 38,5 · 31,6 · 29,9 | 27,4 · 27,8 · 44,8 | 16 · 40 · 44 | **14,9 en el 2** | **Causa encontrada:** el modelo reacciona despacio a la forma de esta temporada (Osasuna 15.º con −11 de diferencia de goles; Athletic 7.º con +4) y los dos estrenan entrenador. **P2 debe cubrir el 2** |
| 3 | Valencia – Real Madrid | 16,7 · 21,2 · 62,0 | 11,4 · 16,1 · 72,5 | 6 · 5 · 89 | 10,5 en el 2 | Parcial: queda sesgo europeo; el RM no ha empatado en Liga. Mismo signo |
| 4 | Elche – Betis | 32,6 · 29,7 · 37,7 | 29,3 · 25,5 · 45,2 | 12 · 29 · 59 | 7,5 en el 2 | Parcial: el Elche, 0-1-4 en casa. Mismo signo |
| 5 | Real Sociedad – Rayo | 57,7 · 23,0 · 19,3 | 56,3 · 22,8 · 20,9 | 80 · 15 · 5 | — | — |
| 6 | Celta – Levante | 57,8 · 23,8 · 18,4 | 53,0 · 25,2 · 21,8 | 66 · 24 · 10 | — | — |
| 7 | Villarreal – Getafe | 57,5 · 24,4 · 18,1 | 65,8 · 20,9 · 13,3 | 81 · 12 · 8 | 8,3 en el 1 | Parcial: el Getafe, 0-0-5 fuera y sin marcar. Mismo signo |
| 8 | Cádiz – Oviedo | 29,1 · 28,8 · 42,1 | 34,2 · 30,5 · 35,2 | 23 · 30 · 46 | — | El partido más igualado |
| 9 | Girona – Almería | 50,8 · 24,1 · 25,1 | 45,8 · 26,2 · 27,9 | 44 · 28 · 28 | — | — |
| 10 | Sporting – Valladolid | 51,9 · 25,0 · 23,1 | 40,3 · 29,3 · 30,3 | 64 · 28 · 8 | 11,5 en el 1 | **No encontrada.** Mismo signo; se vigila |
| 11–14 | Liga F | (ver tabla del modelo) | Una sola fuente, que parece un modelo | — | No es un control fiable | La regla de la Liga F (más de 25 puntos de diferencia con el público) no salta |
| 15 | Atlético – Barcelona | 37,4 · 25,5 · 37,1 | 26,5 · 21,4 · 52,1 | — | 15 en el 2 | Solo cuenta para el Pleno |

### Diseños de 24 apuestas (con P2 cubriendo el 2)
| Opción | Signos (juntos) | P(14): mesa · mercado | Peor de los 3 precios | Valor (frente al robusto) | X cubiertas |
|---|---|---|---|---|---|
| **Robusto** | 1 · 12 · 2 · 12 · 1 · 1 · 1 · **1X2** · 1 · 1 · 2 · 12 · 2 · 1 | 1/1.169 · 1/2.023 | **81%** (el mejor posible) | 1,00× | 1 (P8) |
| **Valor con control** | 1 · 12 · 2 · 12 · 1 · 1 · 1 · **1X2** · 1 · 1 · 2 · 1 · 12 · 1 | 1/1.259 · 1/2.203 | 74% | **2,18× · 1,75×** | 1 (P8) |
| Solo el modelo (regla escrita) | 1 · 12 · 2 · 12 · 1 · 1 · 1 · 2 · 1 · 1 · 2 · 12 · 1X2 · 1 | 1/1.105 · 1/2.814 | 58% | 1,17× · 1,23× | 1 (P13) |

- **Por qué no hay más X:** las X con valor (P5, P7, P14) están en partidos con un favorito claro. Cubrirlas cuesta casi un 30% de P(14).
- **Empates esperados entre los 14: 3,48.** El triple va a la X más probable de la jornada, la del P8 (29–30%).
- **La regla de valor escrita (90% de la mejor P(14) solo con la mesa) choca con el mercado esta jornada.** Los diseños que cumple tienen solo el 58% de la P(14) del mercado. Se pregunta al usuario qué criterio quiere.

### Pleno (Atlético – Barça)
| Marcador | Mesa | Mercado | Público | Valor (mesa · mercado) |
|---|---|---|---|---|
| **1-1** | **9,9%** | **11,1%** | 11,8% | 0,84 · 0,94 |
| 1-M | 7,6% | 9,2% | 11,8% | 0,64 · 0,78 |
| 1-2 | 7,5% | 10,0% | 20,2% | 0,37 · 0,50 (el que más juega el público) |
| 1-0 | 5,3% | 6,7% | 3,3% | **1,60 · 2,03** |

**Principal: 1-1**, el más probable para la mesa y para el mercado.

### Sueltas candidatas (v1)
| # | Apuesta | Prob. | Cuota mínima |
|---|---|---|---|
| 1 | Real Madrid marca (P3) | 88,0% | 1,14 |
| 2 | Celta marca (P6) | 86,6% | 1,16 |
| 3 | Real Sociedad marca (P5) | 85,8% | 1,17 |
| 4 | Málaga – Racing: más de 1,5 goles | 85,6% | 1,17 |
| 5 | Girona marca (P9) | 84,3% | 1,19 |

Real Madrid F marca (89,4%) y Tenerife F – Alavés F 1X (86,3%) quedan fuera: son de la Liga F, donde tenemos pocos datos.

Archivos: scratchpad/j20/ (v1.py, busca*.py, xdis.py, j20_v1.json) y mesa_j20/ (informes de los agentes).

---

## v2 · Revisión final (viernes 6/11, de 17:23 a 18:15 de Canarias)

### Noticias del viernes (bajas con fecha y fuente de 72 h o menos)
| Nº | Noticia | Fuente | Ajuste |
|---|---|---|---|
| 3 | **Vinícius, sancionado**: cumple el 4.º y último partido. Rodrygo y Asencio, bajas ya conocidas. Vuelven Tchouaméni y Güler | [OKDiario, convocatoria del RM (6/11)](https://okdiario.com/diariomadridista/real-madrid/convocatoria-del-real-madrid-contra-valencia-tchouameni-guler-vuelven-vinicius-cumple-ultimo-castigo-675660) | 2: −1 (ya faltó en las 3 últimas) |
| 2 | Athletic: Paredes, baja (lesión muscular). Galarreta vuelve. De Djaló y Nico Serrano solo estará uno | [Jornada Perfecta, Terzić](https://www.jornadaperfecta.com/blog/terzic-previa-osasuna-athletic-j12-26-27/) | Sin cambio (se compensan) |
| 1 | Málaga: Ochoa y Lobete, bajas ya conocidas. Racing: Mantilla y Andrés Martín | [FútbolFantasy, previa](https://www.futbolfantasy.com/laliga/noticias/154184-posibles-alineaciones-y-previa-fantasy-del-malaga-racing) | Sin cambio |
| 15 | Barça: Rodri (de 4 a 5 semanas), Olmo, Espart y Bardghji, bajas. Koundé, duda (= 0). Lamine Yamal, disponible | [ElDesmarque (4/11)](https://www.eldesmarque.com/futbol/liga-1a-division/20261104/bajas-barcelona-metropolitano-atletico-madrid_18_020615372.html) | Ya aplicado (2: −2) |

Al dataset se añadieron los partidos europeos del 4–5/11:
- AEK 2-3 Real Madrid
- Dortmund 2-1 Betis
- Real Sociedad 1-1 Lyon
- Celta 1-2 Union SG
- Getafe 0-1 Brighton

**Hora oficial de cierre:** el aviso de LAE de la J20 no aparece en el buscador. Se mantiene la estimación del Trader:

| Canal | Cierre (hora de Canarias) |
|---|---|
| Administración | ≈13:00 (el primer partido) |
| Losilla, particulares | 12:00 |
| **Límite de la mesa** | **11:00** |

### Cómo se eligió el boleto (185.328 diseños de 24 apuestas)
1. **P2 debe cubrir el 2.** La diferencia con el mercado es de 14,8 puntos y la causa está en el modelo, que no recoge la forma de esta temporada.
2. **Regla de valor:** al menos el 90% de la mejor P(14) con el precio de la mesa, entre los diseños que cumplen el punto 1 (quedan 10).
3. **Control de robustez:** al menos el 75% de la mejor P(14) con el mercado (queda 1).
4. **Resultado: triple en P2 y dobles en P4, P8 y P12.** También es el diseño de mejor P(14) con la mezcla.

| Diseño | P(14) mesa · mercado · mezcla | P(≥13) mesa · mercado | P(≥12) mesa · mercado | ¿Pasa las reglas? |
|---|---|---|---|---|
| **Triple P2 + dobles P4, P8, P12 (elegido)** | **1/1.146 · 1/2.103 · 1/1.487** | **0,93% · 0,57%** | **4,65% · 3,16%** | **Sí** |
| Robusto de la v1 (triple P8 + dobles P2, P4, P12) | 1/1.193 · 1/2.023 · 1/1.487 | — | — | Sí la 1 y la 3; en la 2 queda en el 88% del máximo |
| Valor de la v1 (doble en P13 en vez de P12) | 1/1.285 · 1/2.203 | — | — | No pasa ni la 2 (82%) ni la 3 (74%) |
| Solo el modelo (sin el control del mercado) | 1/1.105 · 1/2.814 | — | — | No pasa la 3 (58%) |

**Cambios de valor en el boleto 2:** se probaron P13 = 1, P10 = 2 y X en P5, P7, P14, P1 y P11. Todos cuestan del 5% al 23% de P(14), y ninguno mejora a la vez el 12 y el 13. No entra ninguno.

### Disensos del Investigador (R6), con su coste frente al boleto final
| Nº | Investigador | Coste en P(14): mesa (mercado) | ¿Entra? |
|---|---|---|---|
| 2 | X2 | −14% (+5%) | No: el triple ya cubre la X y el 2 |
| 4 | X2 | −4% (−5%) | No: pierde con la mesa y con el mercado, y el 1 del Elche tiene valor (público 12%) |
| 6 | 1X | −29% (−9%) | No |
| 7 | 1X | −28% (−19%) | No |
| 1, 5, 8, 9, 10, 13 | 1X / X2 | Costes parecidos (P(14) baja del 90%) | No |
| Pleno | 1-2 | 7,5% frente al 9,9% del 1-1 | No |

### Nota sobre el factor de empates (reserva del Auditor)
- En la J20 se aplicó la regla de Primera: factor 1,20 en los partidos igualados, con cualquier número de goles esperados. Se midió solo en Primera (189 partidos: X real 31,2% frente al 27,0%).
- El registro de errores hablaba de la banda de 2,6–3,0 goles esperados. Esa banda es la regla general para todas las ligas, la que se validó en el tiempo.
- Por eso el factor entró en P2 (2,57 goles esperados) y en P15 (3,75), que quedan fuera de esa banda. El impacto es bajo: P2 va triple, y el 1-1 del Pleno también es el marcador más probable para el mercado.
- **Se revisa en el post-mortem de la J20**, con los partidos igualados de Primera separados por goles esperados.

### Boleto final (Auditor: FIRMADO CON RESERVA; las dos reservas quedan resueltas arriba)
| Boleto | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | Pleno |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Boleto 1 · 16 apuestas · 12 € | 1 | 12 | 2 | 12 | 1 | 1 | 1 | 12 | 1 | 1 | 2 | 12 | 2 | 1 | 1-1 |
| Boleto 2 · 8 apuestas · 6 € | 1 | **X** | 2 | 12 | 1 | 1 | 1 | 12 | 1 | 1 | 2 | 12 | 2 | 1 | 1-1 |
| Juntos | 1 | **1X2** | 2 | 12 | 1 | 1 | 1 | 12 | 1 | 1 | 2 | 12 | 2 | 1 | 1-1 |

- **X cubiertas:** 1, la de P2, que es la X más probable de la mesa (31,6%). X esperadas en la jornada: 3,49.
- **14 signos individuales:** 1 · 1 · 2 · 2 · 1 · 1 · 1 · 2 · 1 · 1 · 2 · 1 · 2 · 1 · Pleno 1-1.
- **Pleno: 1-1**, el más probable para la mesa (9,9%) y para el mercado (11,1%). Le siguen 2-2 (7,7%) y 2-1 (7,6%).

**Sueltas:**

| # | Apuesta | Prob. | Cuota mínima |
|---|---|---|---|
| 1 | Real Madrid marca | 87,6% | 1,15 |
| 2 | Real Sociedad marca | 85,7% | 1,17 |
| 3 | Málaga – Racing: más de 1,5 goles | 85,6% | 1,17 |
| 4 | Celta marca | 85,3% | 1,18 |
| 5 | Girona marca | 84,3% | 1,19 |

Archivos: scratchpad/j20/ (v2.py, precios_v2.json, j20_v2.json, final_sel.py, final_b.py).

---

## v3 · Cambio del sábado 7/11 a las 11:10 de Canarias: más empates (lo pidió el usuario)

**Lo que dijo el usuario (11:07):** «Qué está pasando con los empates, siguen sin poner, y las probabilidades de empate, y hay mucho».

**Explicación que se le dio:**
- En la J20 lo más probable son 3 o 4 empates (46%); que no haya ninguno, solo un 1,8%.
- Pero en ningún partido la X es el signo más probable: la máxima es la de P2, con un 31,6%.
- Por eso la X solo entra con dobles y triples.

**Opciones que se le dieron (24 apuestas):**

| Opción | X cubiertas | P(14): mesa · mercado | Valor |
|---|---|---|---|
| v2 (la del viernes) | 1 (P2) | 1/1.146 · 1/2.103 | 1,00× |
| **Con 2 X: P8 en X2 en vez de 12** | **2 (P2, P8)** | **1/1.151 (−0,4%) · 1/2.221 (−5%)** | 0,85× · 0,78× |
| Con 3 X: además, P4 en X2 | 3 | 1/1.202 (−5%) · 1/2.341 (−10%) | 0,42× · 0,40× |

**Decisión:** el usuario respondió «No he sellado» y la mesa le recomendó la opción de 2 X.
- Respeta la regla de valor: conserva el 91% de la mejor P(14) de la mesa.
- Queda algo por debajo del control de robustez: 73% de la mejor P(14) del mercado, frente al 75% mínimo.
- Se acepta como excepción del Director, por la preferencia expresa del usuario por cubrir empates. Cuesta un 0,4% de P(14) con la mesa.

### Boleto definitivo (v3)
| Boleto | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | Pleno |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Boleto 1 · 16 apuestas · 12 € | 1 | 12 | 2 | 12 | 1 | 1 | 1 | **X2** | 1 | 1 | 2 | 12 | 2 | 1 | 1-1 |
| Boleto 2 · 8 apuestas · 6 € | 1 | X | 2 | 12 | 1 | 1 | 1 | **X2** | 1 | 1 | 2 | 12 | 2 | 1 | 1-1 |

**Lección para el método:** el usuario prefiere cubrir más empates aunque se pierda valor. La regla de valor manda dentro de lo que él aguanta, así que desde la J21 cada boleto llevará **al menos 2 X cubiertas** cuando el coste en P(14) de la mesa sea menor del 5%. Hay que comprobarlo con él antes de dejarlo como regla. **Respuesta del usuario (10/11): no es obligatorio; lo decide la mesa.**
