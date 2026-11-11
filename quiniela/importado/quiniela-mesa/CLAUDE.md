# CLAUDE.md — Mesa de la Quiniela (proyecto migrado desde claude.ai "F Almacén")

Exportado el 11/11/2026, con todo lo recogido en el chat de trabajo de la J18 a la J21 y en los documentos del proyecto.
Este archivo es la memoria de trabajo de Claude Code. Léelo entero antes de cada jornada.

---

## 1. Qué es esto
- Pronósticos de la **Quiniela española**: 14 partidos 1X2 + **Pleno al 15**. El objetivo final de todo es acertar el Pleno al 15.
- Funciona como **una casa de apuestas que trabaja para el usuario**: precio honesto, gestión del riesgo y aprovechar los sesgos del público.
- Lo hace una **"mesa" de agentes especialistas** que trabajan por separado y dictaminan cada partido. El Director (la sesión principal) decide con reglas escritas y un Auditor independiente revisa antes de entregar.
- El método completo está en `docs/prompt-maestro-quiniela.md` (v5), y el organigrama y las reglas de decisión en `docs/agentes-mesa.md`. Los agentes están definidos en `.claude/agents/` y el flujo en la skill `.claude/skills/mesa-quiniela/`.

## 2. Instrucciones permanentes del usuario (obligatorias)
1. **Siempre en español.** Análisis **profundos**, nunca superficiales. **Siempre en tablas.**
2. **Siempre los 15 pronósticos** (14 + Pleno). Aparte: **los 14 signos individuales, el Pleno y 5 apuestas sueltas** con la mayor probabilidad posible.
3. **No hay formato fijo de boleto.** La mesa recomienda como profesional el sistema que considere mejor (3 triples + 3 dobles, reducida de 7 dobles, 4 dobles completos u otro), lo dice claramente y avisa si necesita investigar en webs.
   - Presupuesto de las últimas jornadas: **18 € (12 + 6)**. El presupuesto lo fija el usuario.
4. **Cuotas y pronósticos ajenos: se analizan, pero NUNCA entran en el modelo.** Son solo control. Lo reconfirmó el 10/11/2026.
5. **Aprender de los errores:** tener presentes los fallos anteriores (`docs/registro-errores.md`), guardarlos y preguntarle lo necesario.
6. En cada jornada, analizar **por qué Loterías mete esos partidos y no otros** (`docs/patrones-seleccion-lae.md`).
7. **La J17 de 2026 (Copa del Rey, 27–29/10) no se pronostica nunca.** Si la pide, decir que no.
8. **No analizar los partidos en el descanso.** Lo paralizó el 7/11/2026. Los datos de los últimos partidos se miran solo al hacer los pronósticos.
9. **Empates:** le preocupa que se escapen y quiere más X cubiertas. Pero el 10/11 decidió que **el mínimo de 2 X no es obligatorio**: lo decide la mesa con los números.
10. Pensar con la mente de quien hace ganar a la casa, pero usándola para hacerle ganar a él.
11. Un **favorito que viene de perder en Europa nunca va de sencillo** (veto mantenido por el usuario el 2/11).

## 3. Límites que no se cruzan
- **Nunca sellar, apostar ni cargar dinero por el usuario.** Solo se le recomienda; él sella en su administración, que tiene horario continuo.
- **Risk Manager:**
  - Presupuesto fijo; **nunca subir para recuperar**.
  - Nada de combinadas ni de apuestas en vivo para recuperar.
  - Kelly fraccionado solo con valor esperado positivo **demostrado**: unos 50 partidos en la prueba de confianza, que todavía no hay.
- **Webs bloqueadas por motivos legales: Marca, Sport, Mundo Deportivo y L'Équipe.** No se intentan por otras vías.
- **No inventar nada:** horas, porcentajes, bajas o posiciones siempre con fuente. Si algo no aparece: "no encontrado".
- **Noticias A/B/C/D:** A oficial, B medio fiable con dato concreto, C rumor, D especulación. **Solo A y B mueven números.**

## 4. El modelo (precio oficial)
- **EuroPoisson jerárquico** (`modelo/euro_model.py`) sobre unos 23.700 partidos (`datos/clubes/euro_j21.json`): fuerza = nivel de liga + desviación del equipo, decaimiento temporal y ridge.
- **Parámetros:** xi = 0,0015 (vida media unos 15 meses), ridge = 10/0,05, escala = 1,05, mezcla del Pleno = 0,20 (80% Poisson + 20% distribución empírica), hier = True.
- **Factor de empates** (multiplica la diagonal): ligas ×1,08, copas UEFA ×1,00, Liga F ×0,85.
  - **Medición nueva del 10/11 (Matemático, J21):**
    - En Segunda, el ×1,08 está algo pasado (k medido 0,93); lo honesto sería 1,00.
    - En la Liga F, el ×0,85 se queda corto (k 1,12, n = 62).
    - Ninguno de los dos cambios es significativo todavía. **Pendiente de decidir.** Detalle en `jornadas/j21/mesa/matematico_fisico.md`, §2.
- **Primera:**
  - +0,07 de campo por lado.
  - Capa de xG de statz.ai: ataque ×(xG/goles)^0,30 y defensa ×(xGA/encajados)^0,15, con tope de ±5%.
  - **DRAW_K_IGUALADO = 1,20** cuando |P1−P2| < 0,15. Medido el 4/11: 189 partidos, X real 31,2% frente al 27,0% previsto. **No vale en Segunda** (medido el 10/11).
- **EURO_F = 1,12** en liga: equipo con partido UEFA en los últimos 120 días frente a uno sin él. Validado: 3.434 partidos, log-loss de 0,8645 a 0,8414.
- **Lo que NO se aplica** (medido): el veto "viene de perder en Europa" como número en liga (sí sigue como veto de sencillo); el cansancio europeo en liga; enfrentamientos directos; cambio de entrenador; árbitro; la rho de Dixon-Coles.
- **Liga F:**
  - Poisson ridge partido a partido sobre la temporada actual, sin los partidos del Barça.
  - Prior de la 2025/26 y campo fijo ×1,10.
  - La cadena de la J1 a la J8 está dentro de `modelo/j20_run.py` / `j21_run.py`; la J9 y la J10 están en `datos/liga-f/ligaf_j9_j10.txt`.
- **Selecciones (nuevo, J21):**
  - Poisson de selecciones del Científico (`datos/selecciones/nat_j21.json`), hecho con `datos/selecciones/international_results/results.csv` (martj42, GitHub).
  - Elo alternativo del Matemático en `jornadas/j21/mesa/mf/`.
- **Ajustes de última hora:**
  - ±5% a los goles esperados.
  - Hasta 10% solo por la baja del portero o del delantero centro titular.
  - Cansancio por Copa o Europa del jueves: Europa −4% en ataque y +2–3% en goles encajados; Copa −2% / +1,5%.
  - Una baja solo cuenta con sanción o lesión y una fuente de las últimas 72 h. "Vuelve a entrenar", "en duda" o "recuperado" = 0.
- **Riesgo:** nada por debajo del 65% es "fijo" (lleva ⚠️). Equipo con menos de 30 partidos en los datos = **dato flojo** → nunca signo único.
- **Mercado:** si la mesa se separa **7 puntos o más** del mercado, revisión escrita. Si la causa está en el modelo, el boleto cubre el signo del mercado (regla de la J20).
  - Ojo: **el mercado ha predicho mejor que la mesa tres jornadas seguidas** (J20: log-loss 0,976 del mercado frente a 1,085 de la mesa). Aun así, el usuario mantiene que las cuotas son solo control.
- **Empates en el boleto:** en todo partido igualado (|P1−P2| < 0,15), el doble se elige entre **12, 1X y X2**, con una decisión escrita y su coste en P(14).
  - Lección clave: la X **nunca** es el signo más probable del modelo (0 de 6.055) y se escapa como tercer signo.
  - J14–J20: 18 X reales, 3 cubiertas.
- **Aplazamientos:** comprobar el día del sellado que se juegan los 15 (error de la J20, P14). Un partido aplazado lo decide un **sorteo de LAE ponderado** con los porcentajes del público; su precio es el % de LAE.
- **Premios:** el dinero está en 13 y 14. **10 aciertos solo cobra en jornadas con muchas sorpresas** (J20: 3,41 €; antes no llegó a 1,50 € y no cobró).

## 5. Cómo se ejecuta
Requisitos: Python 3.10 o superior, `numpy`, `scipy` y `pandas` (para algunos estudios).

```bash
cd modelo
# J21: clubes + Liga F + selecciones (unos 1–3 minutos de ajuste)
LF_EXTRA=../datos/liga-f/ligaf_j9_j10.txt NAT_JSON=../datos/selecciones/nat_j21.json \
  python3 j21_run.py ../datos/clubes/euro_j21.json ../jornadas/j21/j21_v1.json
```

- **Para una jornada nueva:** copia `j21_run.py` a `jNN_run.py` y cambia `FIX` (los 15 partidos con los nombres exactos del dataset; tipo "M" para clubes, "F" para Liga F y "N" para selecciones), `PRIMERA` (los números de los partidos de Primera) y las fechas de referencia.
- **Ajustes por partido:** tercer argumento, en JSON: `'{"n": [factor_lambda_local, factor_lambda_visitante]}'`.
- **Boletos:**
  - `modelo/reducida7.py`: reducida de 7 dobles, Hamming [7,4], distribución exacta de aciertos.
  - `modelo/compare_systems.py` y `modelo/j19_director.py`: 4 dobles, vetos y boletos dobles.
  - `jornadas/j20/director/final_sel.py`: selección con valor y robustez.
- **Actualizar datos:** `modelo/build_euro.py` + `modelo/parse_openfootball.py` sobre `datos/fuentes-openfootball/`. Después, añadir a mano (con dos fuentes) los partidos recientes que openfootball no trae. Ejemplos de esto en `jornadas/j2x/mesa/code/build_j2x.py`.
- ⚠️ Algunos scripts de `jornadas/` y 4 de `modelo/` (coach_test, copa_base, h2h_test y reducida7_valor) tienen **rutas absolutas del entorno antiguo** (`/tmp/claude-0/...` o `/home/claude/...`). Hay que cambiarlas por rutas relativas antes de usarlos.

## 6. Mapa de carpetas
| Carpeta | Qué hay |
|---|---|
| `docs/` | Los 30 documentos del proyecto de claude.ai. **Empieza por `00-indice.md`.** Clave: `prompt-maestro-quiniela.md`, `agentes-mesa.md`, `registro-errores.md`, `prueba-confianza.md`, `jNN-pronostico.md` / `jNN-resultados.md`, `historico-quiniela-1972-2026.md`, `patrones-seleccion-lae.md` y `como-hablarme.md` |
| `memoria/` | Lo que la memoria de claude.ai guardaba sobre el método y las preferencias de la Quiniela |
| `modelo/` | Código oficial: modelo, scripts de cada jornada (j15–j21), boletos y estudios |
| `datos/clubes/` | `euro_j21.json`: dataset oficial (23.672 partidos, hasta el 9/11/2026). `euro_j20b.json`: la versión anterior. También están los resultados de Segunda de la J1 a la J13 recopilados por el Investigador |
| `datos/liga-f/` | La Liga F de la J9 y la J10 (y de la J1 a la J10 según el Investigador) |
| `datos/selecciones/` | `international_results` (results.csv de martj42) + `nat_j21.json` (precios de P10 y P15 de la J21) |
| `datos/historico-quiniela/` | La Quiniela de 1972 a 2026: 2.709 jornadas (`hist.json`) y el original `h.xls` |
| `datos/loterias/` | Jornadas, premios y Primera incluida (estudio de por qué LAE elige los partidos) |
| `datos/fuentes-openfootball/` | Fuentes en bruto: football.json, europe, champions-league y espana |
| `datos/estudios/` | El estudio de empates (predicciones fuera de muestra), el registro del descanso (paralizado), el código del histórico y el xG |
| `jornadas/` | El trabajo de la mesa por jornada: informes de cada agente, precios en JSON, código, auditorías. De la J14 a la J16 solo hay archivos sueltos; de la J18 a la J21, completo |
| `panel/` | Datos y HTML del panel de la mesa (artifact de claude.ai) |
| `.claude/agents/` | Definición de los agentes de la mesa para Claude Code |
| `.claude/skills/` | `mesa-quiniela` (el flujo de la mesa) y `quiniela-predictor` (skill anterior) |

## 7. Fuentes
- **Funcionan:**
  - futboltotal.futbol (resultados y rondas, también de la Liga F).
  - laliga.com: las fichas en-GB y las tablas oficiales. Ojo: las fichas con prefijo es-DE, es-NL… dan la hora en UTC; `/partido/` sin prefijo la da en hora peninsular.
  - en.ligaf.es (a veces va con retraso).
  - statz.ai (xG de Primera y de los equipos de Segunda).
  - quiniela15.com (porcentajes de LAE, APU y sus usuarios).
  - Eduardo Losilla (escrutinio).
  - lasfutbolistas.com, Infobae/EFE, ESPN, FotMob (a veces desfasado), Sky Sports, uefa.com.
  - Gainblers (cuotas 1X2 de Segunda por casa; las de selecciones solo en Gainblers México).
  - OddsPortal.
  - GitHub: openfootball y martj42/international_results.
  - bet365.es, solo desde el navegador del usuario y con su aprobación.
- **Bloqueadas o inútiles:**
  - Por motivos legales: Marca, Sport, MD y L'Équipe.
  - Transfermarkt, Understat, Football-Data, AS, worldfootball, la API de ClubElo, COPE y 365scores.
  - Las descargas directas de Loterías.
  - Sofascore y Flashscore sin datos (solo noticias).

## 8. Libro de banca y prueba de confianza
| Jornada | Coste | Sellado | Mejor columna | Premio |
|---|---|---|---|---|
| J19 | 18 € | Sí | 10 | 0 € |
| J20 | 18 € | Sí | 8 (el boleto 1 hizo 7) | 0 € |
| **Total** | **36 €** | | | **0 €** |

- De la J13 a la J18 hay más historia en `docs/` (J14: 11 aciertos sin sellar; J18: el boleto se rechazó a las 12:01).
- **Prueba de confianza** (`docs/prueba-confianza.md`): 9 partidos, log-loss de la mesa 0,906 frente a 0,867 del mercado. Hace falta llegar a unos 50 partidos.
- **Sueltas:** J18 4/5, J19 5/5, J20 3/5.

## 9. ESTADO ACTUAL: J21 (sábado 14 y domingo 15 de noviembre de 2026), A MEDIAS
**Composición:** parón de selecciones: 9 de Segunda, Bélgica–Italia (Nations League), 4 de Liga F y **Pleno España–Inglaterra**.

**Cierre:** sábado a las 14:00 peninsulares (13:00 de Canarias); los particulares de Losilla cierran una hora antes. **Límite de la mesa: sábado a las 11:00 de Canarias.** El boleto oficial de LAE está por confirmar.

**Precio v1** (Científico, datos hasta el 9/11; `jornadas/j21/mesa/j21_v1.json`):

| Nº | Partido | 1 | X | 2 | Notas de la mesa |
|---|---|---|---|---|---|
| 1 | Valladolid – Castellón | 27,6 | 25,1 | 47,3 | La mesa ve el 2 unos 7 puntos por encima del mercado. Castellón sin Maty (sancionado, −3%) |
| 2 | Real Sociedad B – Sporting | 36,2 | 27,0 | 36,9 | Igualado y **frágil**. Sporting sin Juan Otero (expulsado, −4%) |
| 3 | Almería – Andorra | 55,9 | 21,7 | 22,4 | Owono, portero del Andorra: sanción pendiente (+4% al Almería si sale antes del sábado) |
| 4 | Mallorca – Córdoba | 61,9 | 22,0 | 16,1 | La mesa infla el 1 unos 7 puntos frente al mercado y frente al Dixon-Coles español → revisar |
| 5 | Oviedo – Girona | 35,6 | 29,4 | 35,0 | Igualado y **frágil** |
| 6 | Tenerife – Ceuta | 48,8 | 26,3 | 24,9 | Primer partido tras la muerte de Jesús de Miguel. Al Tenerife le falta la 2025/26 en los datos |
| 7 | Granada – Las Palmas | 40,5 | 27,0 | 32,4 | **El mercado da al 1 un 54% frente al 41% de la mesa** → por la regla de la J20, va **1X**. Las Palmas sin Herzog (Sub-21) |
| 8 | Eibar – Cádiz | 51,9 | 27,0 | 21,1 | El Eibar jugó la Copa el martes 10/11 (−2%) |
| 9 | Eldense – Sabadell | 34,5 | 30,2 | 35,3 | **Dato flojo** (Sabadell, 13 partidos) y **frágil**: nunca signo único |
| 10 | Bélgica – Italia | 48,9 | 27,1 | 24,0 | En Bruselas. Se juegan el 2.º puesto; faltan los resultados del jueves 12/11. El Elo alternativo da 50,7·27,6·21,7 |
| 11 | Alavés F – Eibar F | 42,3 | 32,8 | 24,9 | Dato flojo; el aplazado Tenerife F–Alavés F sigue sin fecha |
| 12 | Real Sociedad F – Athletic F | 38,7 | 23,9 | 37,5 | Igualado; las dos llevan 4 empates de 10 |
| 13 | Sevilla F – Atlético F | 21,4 | 20,1 | 58,5 | |
| 14 | Valencia F – Granada F | 35,7 | 25,0 | 39,3 | **Precio inestable**: cambió 9 puntos con una sola jornada |
| 15 | **Pleno España – Inglaterra** | 51,0 | 27,5 | 21,5 | En el Metropolitano. Pleno del modelo: **1-1** (13,1%) y después 1-0 (11,4%). Mercado: 58,6·21,6·19,8 |

**Informes ya entregados** (`jornadas/j21/mesa/`):
- `brief.md` (expediente común).
- `investigador.md`.
- `compilador_trader.md`.
- `cientifico.md`.
- `matematico_fisico.md`: recomienda el diseño D3 (cubrir más X con poco coste de P(14)). Frágiles: P2, P5 y P9.

**Pendiente:**
1. **Risk Manager:** se cortó por el límite de uso. Su código a medias está en `jornadas/j21/mesa/calc/risk/`.
2. **Revisión del jueves y el viernes:**
   - Sanciones del Comité: Owono, y el ciclo de amarillas del Eldense (7) y el Oviedo (6).
   - Resultados de selecciones del jueves 12/11 (Italia–Francia, etc.).
   - Resultado del Pamplona–Eibar de Copa.
   - Porcentajes oficiales de LAE.
   - Cuotas frente a la base del martes: un movimiento de 3 puntos o más sin noticia es una alerta.
   - Seis equipos con la J13 aplazada y sin fecha: Castellón, Eibar, Granada, Tenerife, Andorra y Mallorca.
3. **Director:** precio final con los ajustes A/B, la decisión de cada igualado (12/1X/X2), el boleto de 18 € (comparación exacta), los 14 signos, los 3 Plenos y las 5 sueltas.
4. **Auditor independiente** antes de entregar. Después, guardar `docs/j21-pronostico.md` y actualizar `docs/00-indice.md`.
5. Decidir con el usuario si se cambian los factores de empate de Segunda (1,08 → 1,00) y de la Liga F (0,85 → 1,00).
6. Tras la jornada: `docs/j21-resultados.md` (resultados, log-loss mesa/mercado/público, X cubiertas, sueltas y banca).

## 10. Cómo trabajar una jornada (resumen del flujo)
1. **Expediente común** (`brief.md`): reglas, los 15 partidos con su precio, datos flojos, fuentes y formato de entrega.
2. **Especialistas en paralelo, sin verse:**
   - Investigador.
   - Matemático/Quant.
   - Físico.
   - Compilador de cuotas.
   - Trader.
   - Risk Manager.
   - Científico de datos.
   Cada uno entrega una tabla de 15 filas con su **Dictamen**.
3. **Director:**
   - Precio base = el modelo oficial. Un modelo alternativo entra solo si gana fuera de muestra, con un peso máximo del 50%.
   - Solo los hechos A y B mueven el precio.
   - Dobles con optimización exacta.
   - El valor solo desempata, siempre por encima del 90% de la P(14) máxima.
   - Nunca se cambia un signo con más de 10 puntos de ventaja.
   - Si 3 o más agentes contradicen al modelo en un partido, ese partido va a dobles.
4. **Auditor independiente** (con veto): recalcula y comprueba las fuentes.
5. **Entrega en tablas:** el boleto o los boletos con P(14), P(≥13) y P(≥12); los 14 signos; Pleno principal, conservador y de varianza; 5 sueltas con su cuota mínima; alertas.
6. **Revisión final** el viernes o el sábado temprano, y **post-mortem** el lunes.
7. Una vez por jornada, sin sermón: ningún sistema garantiza el 14 ni el Pleno.
