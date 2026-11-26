# ÍNDICE COMPLETO — QUINIELA NIVEL SUPREMO

Versión 3.1 · domingo 1/11/2026 · añade el post-mortem de la J18 (`j18-resultados.md`). Reúne **todo lo guardado**: los documentos del proyecto, lo grabado en la memoria del proyecto, las instrucciones permanentes, cada jornada con su boleto y resultado, las reglas, los errores, el modelo, las fuentes, las herramientas y lo pendiente.

**Cómo usarlo:** para trabajar una jornada → apartado 2 (instrucciones) + `prompt-maestro-quiniela.md`. Para consultar algo concreto → busca el apartado.

---

## 1. Objetivo del proyecto

- Pronosticar los 14 partidos + Pleno al 15 de la Quiniela y **acertar el Pleno al 15** (todo estudio se orienta a eso).
- Pensar como **dueño de una casa de apuestas** ("la casa nunca pierde"), con los perfiles profesionales que contratan: odds compiler/trader, Risk Analyst, Live Trader, Data Analyst/Quant, Market Analyst, Pleno Specialist, Portfolio Manager, Calibration Auditor y Red Team (más estadístico, físico y "cuántico" pedidos el 14/10).

## 2. Instrucciones permanentes que me has hecho grabar

| Instrucción | Desde | Estado |
|---|---|---|
| Responder siempre en español | — | Vigente |
| Análisis profundos, no superficiales | — | Vigente |
| Cada jornada nueva: tener presentes los fallos anteriores y mejorar a partir de ellos | — | Vigente |
| Dar siempre los 15 pronósticos (14 + Pleno) | — | Vigente |
| Formato: lista principal 3 triples + 3 dobles, y aparte los 14 signos individuales | J13–J15 | **Sustituido** por la reducida de 7 dobles (abajo); los 14 signos individuales siguen |
| Boleto como **reducida de 7 dobles al 13** (16 apuestas, 12 €) | J16 | Vigente |
| **5 apuestas sueltas** con la mayor probabilidad posible, siempre | 23/10 | Vigente |
| Analizar con lupa **por qué Loterías mete esos partidos y no otros**, y qué se aprende de jornadas anteriores | 21/10 | Vigente |
| Las cuotas y pronósticos ajenos se analizan pero **no entran** en el cálculo; solo datos fiables y reales | 17/10 | Vigente |
| Usar las "mentes" de casa de apuestas (odds compiler, Risk Analyst, Live Trader, Quant…) | 17/10 | Vigente |
| "Escoge lo mejor para los dos" (libertad de enfoque) | 17/10 | Vigente |
| **Jornada 17 (Copa del Rey) descartada**; si la vuelves a pedir, decirte que no | 24/10 | Vigente |
| J18: tener en cuenta los resultados de Copa y cómo afectan a sus equipos | 24/10 | Vigente |
| Presupuesto limitado (no llega a 216 columnas) | J14 | Vigente |

## 3. Mapa de documentos

### Uso
| Documento | Contenido |
|---|---|
| `claude/como-hablarme.md` | Órdenes cortas y hábitos para gastar menos (una conversación nueva por jornada) |
| `claude/agentes-mesa.md` | **La mesa de agentes**: organigrama (Investigador, Matemático, Físico, Compilador, Trader, Risk Manager, Científico de datos, Director, Auditor), flujo, reglas de decisión y calendario |
| Panel «Mesa Quiniela J18» (artefacto) | Consejo por partido, boletos A/B, Pleno, sueltas y columnas, en una página |

### Memoria
| Documento | Contenido |
|---|---|
| `claude/registro-errores.md` | **Registro vivo de errores**: patrones repetidos, todos los errores por jornada con su regla, **lista de control que firma el Auditor antes de sellar** y seguimientos abiertos. Se lee antes de cada jornada |
| `claude/memoria-de-trabajo.md` | Copia íntegra de todo lo que me hiciste grabar: instrucciones, registro J13–J17, cambio de metodología, mesa de trading, calibración, correcciones |

### Método
| Documento | Contenido |
|---|---|
| `claude/prompt-maestro-quiniela.md` | Prompt maestro v3: 10 fases, formato de salida, calendario de trabajo, registro de errores, honestidad |
| `claude/protocolo-mesa-trading.md` | Las 9 mentes con veto; primer motor Dixon-Coles; correcciones de rho y cobertura del Pleno |
| `claude/metodologia-sin-cuotas.md` | Cambio a "cero cuotas"; resultados del sábado J14; calibración; reglas nuevas |

### Investigación
| Documento | Contenido |
|---|---|
| `claude/patrones-seleccion-lae.md` | Cómo elige Loterías (día, cuotas por competición, Pleno), signos 2026/27, dificultad y botes, resultado final J15 |
| `claude/historico-quiniela-1972-2026.md` | 2.709 jornadas oficiales: tendencias, patrones que no existen, X por jornada, tabla de 498 Plenos |
| `claude/factores-extra-probados.md` | H2H, entrenadores y árbitros medidos fuera de muestra |
| `claude/seleccion-partidos-y-sistemas.md` | Primeras conclusiones de selección y comparación exacta de sistemas (5 col, 4 dobles, 7 dobles, 3T+3D) |

### Jornadas
| Documento | Contenido |
|---|---|
| `claude/j13-postmortem.md` | Post-mortem de la J13 |
| `claude/j14-pronostico.md` · `claude/j14-revision-final.md` · `claude/j14-boleto-5-columnas.md` · `claude/j14-resultados.md` | J14 completa |
| `claude/resultados-pronosticos-17-18-oct.md` | 5 apuestas sueltas del 17/10 |
| `claude/j15-pronostico.md` · `claude/j15-postmortem-martes.md` | J15 completa |
| `claude/j16-pronostico.md` · `claude/j16-resultados.md` | J16 completa (con revisión Red Team y análisis final) |
| `claude/j17-preliminar.md` | J17 preliminar (descartada) |
| `claude/j18-pronostico.md` · `claude/j18-resultados.md` | J18: v1 (26/10), v1.1 (protocolo v5), v1.2 (xG), v1.3 y v1.4 (mesa de agentes), **v2 revisión final del 30/10 (auditada): boleto A-R/P12, opción de 18 €, sellar antes de las 12:00 de Canarias**; decisión final A-R original a 18 €. **Resultados y post-mortem** (mejor columna 9/13, falta P14) |
| `claude/j19-pronostico.md` | J19 europea (Champions, Europa League y Conference, 3–5/11). v0: decisiones del usuario. v1: primera pasada (precio final, prueba del veto, 18 € con la regla). v2: revisión final del martes (el triple pasa de P8 a P1 por la regla de valor). **v3, boleto definitivo (13:30 del 3/11, elegido por el usuario, auditado y FIRMADO): boleto 1 (16) 12·12·12·2·2·2·1·12·2·2·2·1·1·2 y boleto 2 (8) X·12·12·2·2·2·1·12·2·2·2·2·2·2; Pleno 1-1; P(14) 1/1.878 con la mesa y 1/666 con el mercado** |
| `claude/j19-resultados.md` | Resultados y post-mortem de la J19: mejor columna 10 (sin premio). Sueltas 5/5. Las 2 X (Bodø 0-0 y Real Sociedad 1-1) quedaron sin cubrir y estaban en los 1X del Investigador. Primer registro del descanso y 3 lecciones para la J20 |
| `claude/j20-pronostico.md` | J20 (7–8/11: 7 Primera + 3 Segunda + 4 Liga F; Pleno Atlético–Barça; bote de 2,2 M€). v0: decisiones del usuario (18 €, sellado el sábado por la mañana, administración en horario continuo), mediciones nuevas (empates en igualados de Primera ×1,20; el veto europeo no vale en la liga) y precio v0 |
| `claude/j20-resultados.md` | Resultados y post-mortem de la J20: jornada de sorpresas. Mejor columna 8 (boleto 2), sin premio. 4 X y solo 1 cubierta (P2, gracias a la v3). P14 aplazado y decidido por sorteo. **El 10 cobró 3,41 €** (corrige el "10 nunca cobra"). Log-loss: mesa 1,085, mercado 0,976. Sueltas 3/5 |

## 4. Cronología de jornadas

### J13 · 14/10 · Champions + Europa League
- **Resultado:** principal 7/11 en lo jugado, individual 6/11, Pleno fallado (1-2 jugado vs M-M real). Tasa de sorpresa 45%. Españoles 4/4.
- **Fallos críticos:** Inter–Brujas (fijo; el favorito venía de perder en J1), Viking–Bayern 3-3 ("trampa nórdica"), Feyenoord–Como (fijo con datos no verificados), Bodø–Dortmund (nórdico sin cubrir el 1).
- **Oficial:** 0 acertantes de 14 y 0 de Pleno; 11 de 13 aciertos (6.795 €).
- **6 correcciones que salieron:** campo nórdico nunca fijo; dato no verificado nunca fijo; rebajar al favorito que perdió en J1; máx. 4 fijos en europeas; Pleno priorizando 3+ goles; empate infravalorado en Champions.

### J14 · 17–19/10 · 7 Primera + 3 Segunda + 4 Liga F · Pleno Getafe–Rayo
- **Boleto final 3T+3D (216 col):** triples Valencia–Athletic, Las Palmas–Castellón, Atlético F–Madrid CFF; dobles Celta–Alavés (1X), Burgos–Sabadell (1X), Eibar F–Deportivo F (1X). Individual 2-1-2-X-1-2-1-1-1-1-1-1-1-2. Pleno 0-1.
- **Por presupuesto se pasó a 5 columnas** (reducción a mano, 5 Plenos distintos — después se demostró que eso no aumenta la probabilidad del Pleno).
- **Datos clave:** el ajuste por las bajas del Athletic acertó la X; mayor infravaloración del público, el 2 del Madrid CFF (ratio 4,62); puntos débiles Eibar–Mallorca al 45% y Real Madrid F al 54%.
- **Resultado:** 2 X 2 X 1 2 1 X 2 1 1 1 2 1 · Pleno 1-1. Mejor de las 5 columnas: 11 (no se llegó a sellar). Fijos 6/8 (se esperaban 4,6). Oficial: 50 acertantes de 14 (11.162 €), 18 de Pleno (80.778 €).
- **Hallazgo:** 5 de 8 partidos del sábado acabaron en marcadores bajos (0-0, 0-1, 1-0, 1-1).

### 5 apuestas sueltas · 17–18/10
Madrid–Sevilla 1X, Getafe–Rayo menos de 3,5, Madrid–Sevilla más de 1,5, Celta marca, Real Sociedad marca → **5 de 5**.

### J15 · 20–22/10 · Champions + Europa + Conference · Pleno PSG–Barcelona
- **Primer modelo multi-liga** (22.611 partidos). Jugado: **5 columnas**, Pleno M-1 en las 5.
- **Resultado:** 2 1 1 1 X 1 X 1 1 1 1 2 2 2 · Pleno M-2. **Mejor columna: 9.** Oficial: 4 acertantes de 14 (45.666 €), 0 de Pleno.
- **Errores:** ajuste por bajas que fue en contra (Oporto–PSV); afirmé que M-M era lo que menos jugaba el público y era falso; sencillo con discrepancia de mercado sin resolver (Getafe–Lugano 2-5).

### J16 · 24–26/10 · 7 Primera + 3 Segunda + 4 Liga F · Pleno Barça–Madrid
- **Primera reducida de 7 dobles.** Boleto Red Team: 1 · 12 · 1 · 1X · 1 · 1 · 1 · X2 · 12 · 1 · 12 · 12 · 12 · 1 · Pleno M-1. Sueltas: Barça marca, Atlético marca, Athletic–Getafe <3,5, Real Sociedad marca, Leganés–Mallorca <3,5.
- **Resultado:** 2 2 1 1 X 1 (Sevilla lunes) X X X 1 1 X 1 · Pleno 1-2. **Mejor columna 8/13** (9 si gana el Sevilla). **Sueltas 4/5.**
- **Errores:** no apliqué el ajuste por la baja del portero del Rayo (perdió 0-3); jornada de empates (5–6 X, todos los de Segunda); el cambio Red Team del Sabadell costó un acierto; el cansancio europeo del Getafe se aplicó al ataque pero no a la defensa.

### J17 · 27–29/10 · Copa del Rey — **DESCARTADA** por decisión del usuario.

### J18 · 31/10–2/11 · 7 Primera + 3 Segunda + 4 Liga F · Pleno Athletic–Real Sociedad
Partidos: Levante–Atlético, Rayo–Celta, Betis–Málaga, Barça–Alavés, Getafe–Sevilla, Racing–Madrid, Elche–Valencia, Eibar–Almería, Eldense–Granada, Burgos–Castellón, Alavés F–Real Sociedad F, Madrid CFF–Deportivo F, Sevilla F–Real Madrid F, Tenerife F–Athletic F. Copa entre semana (la del miércoles se suspendió).
- **Jugado (mesa de agentes):** A-R original a 18 € → boleto 1 (16): 2·1·1·1·1X·2·1·1·12·12·12·2·2·1; boleto 2 (8): igual con P11 en 2 y P12 en 1. Pleno 1-1. **El sábado a las 12:01 la app no aceptó el boleto (cierre 12:00 de Canarias).**
- **Resultado (13 de 14):** 2 1 1 1 1 2 2 X 2 X X 1 2 · P14 el lunes · Pleno 2-1. **Mejor columna 9/13** (dos, en el boleto 2); con victoria del Tenerife F, 10 (**no cobra**: 10 aciertos paga menos de 1,50 € y va al bote). **Sueltas 4/5.**
- **Lectura:** el modelo, calibrado (favoritos 7/13, se esperaban 6,6; log-loss 0,863 frente a 1,099 al azar). Primera 6/7; Segunda y Liga F 1/6, con 3 X. El público acertó P12 y ganó en log-loss (0,786 frente a 0,897).

## 5. Reglas acumuladas (con su origen)

| Regla | Origen |
|---|---|
| Nada por debajo del 65% se llama "fijo" | J14 (Villarreal 60%, Eibar 45%) |
| Campo nórdico o dato no verificado nunca fijo | J13 |
| **Favorito que viene de perder en Europa: nunca sencillo** (veto mantenido por el usuario) **y −4,5 puntos en el precio** (medido con 88 partidos UEFA) | J13; medido y decidido el 2/11 |
| Cuotas solo como control; el % del público se usa invertido (valor = modelo/público) | 17/10 |
| Ajustes por bajas con tope del 5% | J15 (Oporto–PSV) |
| Excepción obligatoria: baja del delantero centro titular o del **portero** | J16 (Rayo) |
| Cansancio europeo: también a la defensa | J16 (Getafe) |
| Mismo Pleno en todas las columnas | Corrección J14 |
| No cambiar signos por muestras pequeñas (H2H, árbitro, racha) | J15–J16, medido |
| Empates: ×1.08 en ligas, ×1.0 en copas, ×0.85 en Liga F | Medido 21–23/10 |
| Ventaja de campo extra en Primera +0.07 | Medido 21/10 |
| En Liga F, quitar los partidos contra el Barça | 21/10 |
| Selecciones: el empate pesa mucho (36%) | Histórico 2026/27 |
| Comparar siempre reducida vs 4 dobles completos | 21/10 |
| Red Team: entre boletos casi igual de probables, el de más valor | J16 |
| Coherencia: suma de X de la jornada ≈ 3,5 | Histórico |
| **Sellar el viernes, o el sábado antes de las 11:00 de Canarias**; el sábado solo se cambia algo por una noticia de clase A | J18 (boleto rechazado a las 12:01) |
| Liga F: si el modelo contradice al público en más de 25 puntos sin una razón, se cubre | J18 (P12) |
| **Los boletos se eligen por P(14), P(≥13), P(≥12) y valor. P(≥10) no cuenta: 10 aciertos no cobra** (premio < 1,50 €; 11 paga 2–4 €; 12 paga 13–23 €; 13 paga 165–390 €) | Escrutinios J12, J14, J15 y J17 (comprobado el 1/11) |
| **Bajas con fecha**: solo sanción o lesión con regreso posterior al partido (fuente de ≤72 h); "vuelve a entrenar/duda" = 0 | J18 (Sadiq) |
| Diferencia con el mercado ≥7 puntos en un signo → revisión escrita firmada por el Auditor (el mercado sigue siendo control) | J18 (P7 Valencia) |
| La revisión de diferencias de 7 puntos o más se hace en **los 14 partidos**, no solo en los candidatos a doble | J19 (P4 y P5) |
| **Orden de las reglas del boleto: 1) vetos; 2) regla de valor (90% de la mejor P(14) con el precio final, entre los diseños habituales); 3) disensos del Investigador (R6), solo si se sigue cumpliendo la 2** | J19 (Auditor) |
| Cuota mínima de una suelta = 1/prob., **redondeada hacia arriba** | J19 |
| Antes de fijar la ventana de sellado, preguntar el horario de la administración del usuario (respuesta del 4/11: **horario continuo**) | J19 |
| **Primera: factor de empates 1,20 en los partidos igualados** (diferencia P1−P2 < 0,15); el resto de ligas, 1,08 | Medido el 4/11 (189 partidos, validación temporal) |
| El veto "viene de perder en Europa" **no se aplica a los partidos de liga** (allí esos favoritos rinden +4,5 puntos) | Medido el 4/11 (346 partidos) |
| **Empates:** dobles candidatos 12, 1X y X2 (no solo los dos signos más probables); tabla de X con valor en cada jornada. La X nunca es el signo más probable del modelo, pero sale el 25% de las veces en las ligas | J19 (estudio del 4/11) |
| ~~Protocolo del descanso~~ **Paralizado por el usuario el 7/11.** No se analizan los descansos ni se programan avisos durante los partidos. Los datos de los últimos partidos se miran **solo al hacer los pronósticos** | Pedido el 4/11; paralizado el 7/11 |
| Comprobar **aplazamientos y suspensiones** de los 15 partidos el día del sellado; un partido aplazado se precia con el % de LAE (lo decide un sorteo ponderado) | J20 (P14 aplazado sin que la mesa lo viera) |
| Partidos posteriores al cierre (domingo y lunes): bajas que pueden cambiar tras el cierre, tope del 2%; ante dobles casi iguales, el doble va al partido posterior al cierre | J18 (pregunta del usuario, 1/11) |
| X en Segunda igualada: **no se cambia** (el histórico de las posiciones 8–10 da un 28%, lo mismo que el modelo); se revisa a los 30 partidos | J16 → contestado en J18 |

## 6. Errores míos reconocidos (para no repetirlos)

1. Dije que la corrección rho de Dixon-Coles arreglaba los 0-0 y 1-1: medido, no aporta (0.9908 vs 0.9909).
2. Cobertura del Pleno inflada en J14 (dije 66,1% con 5 Plenos; real 55,8%) y además diversificar el Pleno entre columnas distintas no suma probabilidad.
3. M-M "lo que menos juega el público" (J15): falso.
4. Hora mal situada en una respuesta del 17/10.
5. Ajuste por bajas en contra (Oporto–PSV, J15).
6. No aplicar la regla del portero (Rayo, J16).
7. Primera versión multi-liga inflaba equipos de ligas flojas (Lillestrøm favorito ante la Real): corregido con niveles de liga.
8. Liga F con empates inflados; Primera con ventaja de campo corta: corregidos.
9. Hora de cierre mal situada (13:00 de Canarias en lugar de 12:00), corregida el viernes; aun así, el boleto de la J18 se intentó sellar a las 12:01.

## 7. El modelo: versiones y parámetros

| Versión | Fecha | Datos | Parámetros / validación |
|---|---|---|---|
| Dixon-Coles español | 17/10 | 1.413 partidos (openfootball, 59 nombres → 46 equipos) | xi 0.0015, ridge 0.05, scale 1.10, blend 0.20, ventaja campo 0.306. Log-loss 0.991 vs 1.049 de la base. Pleno: declara 13,8%, acierta 15,8% |
| Multi-liga jerárquico | 20/10 | 22.611 partidos, 30+ ligas + copas UEFA | ridge 10, scale 1.05, blend 0.20. Copas: log-loss 0.960 vs 0.988 plano y 1.038 base. Favoritos 60–70% → 66%; 70–80% → 82% |
| + correcciones | 21–23/10 | 22.732 partidos (+ Segunda 2026/27 completa, Primera J1–J9) | Empates por competición; Primera +0.07; Liga F por tablas (sin backtest) |

Cobertura real del Pleno con los N más probables: 1 → 15,8% · 2 → 29,9% · 3 → 41,0% · 4 → 48,2% · 5 → 55,8% · 6 → 61,2% · 8 → 74,1% (liga). En copas, ~47% con 5.

## 8. Investigación con cifras clave

- **Selección de Loterías:** jueves 0/4, viernes 1/7, sábado 22/22, domingo 21/24, lunes 9/10. Pleno: 8/14 con Madrid/Barça/Atlético/España, 4/14 el partido del lunes.
- **Dinero:** recaudación 0,7–1,5 M€ sin bote; 3,78 M€ con bote de 4 M€. Jornada de favoritos: 270 acertantes y 590 € el 14. Correlación "signos que no son 1" vs acertantes: −0,61.
- **Histórico 1972–2026:** el 1 bajó del 59,5% al 44,4%; el 2 subió del 13,3% al 30,3%. Sin patrones por posición ni repetición. Media 3,55 X y 4,24 doses por jornada. Plenos: 1-1 12,2%, 1-0 11,0%, 2-1 8,2%… empates 24,9%.
- **Liga F elegida por Loterías:** 69% de 1, 6% de X (2026/27).
- **H2H:** mejora 0,0002 (nula). **Cambio de entrenador:** +0,03 pts/partido (nulo). **Árbitros:** ±11 puntos de error por árbitro (no medible).
- **Copa del Rey (90'):** modesto vs Primera 7/17/77; modesto vs Segunda 17/23/60.
- **Sistemas (12 €):** 4 dobles completos dan más P(14); la reducida de 7 dobles da más premios de 10–12. La "garantía al 13" es condicional.
- **Profesiones de las casas de apuestas:** investigadas el 17/10 e integradas como las 9 mentes.

## 9. Datos y fuentes

| Funciona | Para qué |
|---|---|
| openfootball (git): espana, football.json, europe, champions-league | Históricos de ligas y copas |
| FutbolTotal (páginas de ronda) | Resultados de Primera y Segunda |
| Loterías: resultados, escrutinios y notas de prensa (vía búsqueda) | Combinaciones, premios, recaudación |
| HistoricoQuiniela.xls (aportado por ti) | 2.709 jornadas 1972–2026 |
| Libertad Digital (vía búsqueda) | Composición de jornadas antiguas |
| Quiniela15 | % del público (LAE) y del mercado (APU) |
| UEFA, SportsMole, prensa de clubes | Bajas y alineaciones |
| Futboleras, Wikipedia | Liga F |
| Quinielafutbol.info | Partidos de cada jornada y calendario |

**Bloqueadas:** football-data, AS, worldfootball, API de ClubElo, descarga directa de Loterías, Libertad Digital por enlace directo.

## 10. Herramientas (scripts del entorno de trabajo)

`parse_openfootball.py`, `normalize_teams.py`, `dixon_coles.py`, `backtest.py`, `pleno_tuning.py`, `mercados.py` (modelo español) · `build_euro.py`, `euro_model.py` (modelo multi-liga) · `j15_run.py`, `j16_run.py` (jornadas) · `reducida7.py`, `reducida7_valor.py`, `compare_systems.py` (boletos) · `h2h_test.py`, `coach_test.py`, `copa_base.py`, `parse_hist.py` (investigación). Viven en el entorno de trabajo de Claude, no en el proyecto.

## 11. Tareas programadas

- **Viernes 30/10, 08:00:** revisión final de la J18 (ejecutada).
- La revisión de la J17 se canceló.

## 12. Pendiente

1. Cerrar la J18 con Tenerife F–Athletic F (lunes 2/11 por la noche).
2. Llevar cada jornada el log-loss del modelo frente al del público (J18: 0,897 frente a 0,786).
3. X en Segunda elegida por Loterías: van 6 X en 9 partidos (J14, J16, J18); revisar a los 30.
4. **J19 cerrada: 10 aciertos, sin premio** (ver `j19-resultados.md`). **J20 cerrada: 8 aciertos, sin premio** (ver `j20-resultados.md`). Pendiente: que el usuario confirme si selló la J19 y la J20, para el libro de banca.
5. Backtest del modelo de Liga F con resultados partido a partido.
6. Base de datos de árbitros para mercados de tarjetas (no para el 1X2).

## 13. Lo que NO está en este proyecto (aún)

- **Tu prompt maestro original** (el extenso, anterior a la J13) y el **análisis de la J13 que aportaste**: se trabajaron en otro chat. Desde esta sesión no puedo leer otros chats; si los pegas aquí, los incorporo al índice.
- **El skill `quiniela-predictor`**: está instalado en tu cuenta (Poisson + cuotas Shin + reparto de dobles y triples). Es anterior al cambio a "cero cuotas".
