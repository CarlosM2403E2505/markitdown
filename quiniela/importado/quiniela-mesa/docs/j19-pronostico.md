# J19 — PRONÓSTICO (Champions + Europa League + Conference, martes 3 a jueves 5 de noviembre de 2026)

## v0 · Decisiones y arranque de la mesa (lunes 2/11, 00:15 Canarias)

### Decisiones del usuario (1/11, 23:58)
| Qué | Decisión |
|---|---|
| Presupuesto | **12 € fijos** (16 apuestas), nunca para recuperar |
| Sistema | **4 dobles completos** y 10 sencillos; el mismo Pleno en todas las columnas |
| Sellado | **El martes 3/11.** La mesa entrega el boleto final antes de las 15:00 de Canarias y el usuario sella antes de las 17:00 de Canarias |

### Los 15 partidos (horas peninsulares; Canarias = −1)
| Nº | Partido | Competición | Día | Público Q15 | Mercado APU (control) |
|---|---|---|---|---|---|
| 1 | Barcelona – Aston Villa | Champions | mar 3, 21:00 | 84 · 8 · 8 | 75 · 15 · 9 |
| 2 | Bodø/Glimt – Lille | Champions | mar 3, 21:00 | 76 · 14 · 10 | 50 · 25 · 25 |
| 3 | Man. United – Roma | Champions | mar 3, 21:00 | 43 · 31 · 26 | 40 · 25 · 35 |
| 4 | Villarreal – PSG | Champions | mar 3, 21:00 | 8 · 7 · 86 | 20 · 22 · 58 |
| 5 | AEK Atenas – Real Madrid | Champions | mié 4, 18:45 | 8 · 8 · 84 | 12 · 16 · 72 |
| 6 | Fenerbahçe – Liverpool | Champions | mié 4, 18:45 | 11 · 13 · 75 | 19 · 22 · 59 |
| 7 | B. Dortmund – Betis | Champions | mié 4, 21:00 | 62 · 26 · 12 | 53 · 25 · 22 |
| 8 | Oporto – Nápoles | Champions | mié 4, 21:00 | 56 · 29 · 15 | 42 · 26 · 32 |
| 9 | Lens – Como | Champions | mié 4, 21:00 | 14 · 31 · 55 | 32 · 25 · 43 |
| 10 | Leipzig – Man. City | Champions | mié 4, 21:00 | 9 · 10 · 82 | 19 · 21 · 61 |
| 11 | Slavia Praga – Arsenal | Champions | mié 4, 21:00 | 6 · 8 · 85 | 12 · 17 · 71 |
| 12 | Real Sociedad – Lyon | Europa League | jue 5, 18:45 | 60 · 23 · 17 | 48 · 26 · 26 |
| 13 | Celta – Union SG | Europa League | jue 5, 21:00 | 53 · 24 · 23 | 45 · 26 · 28 |
| 14 | Getafe – Brighton | Europa/Conference | jue 5, 21:00 | 13 · 17 · 70 | 18 · 25 · 56 |
| 15 | **Pleno: Atlético – Bayern** | Champions | mar 3, 21:00 | Q15: 1-2 21%, 2-2 16%, 2-1 12% | — |

Fuentes: [Quiniela15](https://www.quiniela15.com/pronostico-quiniela) y [Quinielafutbol.info](https://www.quinielafutbol.info/proximas-jornadas-de-la-quiniela.html). Según Quinielafutbol.info, la jornada no tiene bote.

### Avisos de arranque
- **El cierre está pendiente de confirmar en Loterías.** Probable: martes a las 21:00 peninsular (20:00 de Canarias). Lo verifica el Trader.
- **10 de los 14 partidos se juegan después del cierre** (miércoles y jueves). Se aplica la regla nueva: un tope del 2% para noticias que puedan cambiar tras el cierre.
- **Datos del modelo viejos**:
  - Ligas extranjeras solo hasta el 20/09 y Noruega 2026 ausente.
  - Lyon y Brighton sin partidos desde el 19/09.
  - Champions y Europa League incompletas.
  - **El precio v0 no es válido para jugar.** El Científico de datos lo está actualizando.
- **Reglas europeas que aplican:**
  - Campo nórdico nunca de sencillo (P2, Bodø).
  - Favorito que viene de perder en Europa, nunca de sencillo.
  - Dato no verificado, nunca de sencillo.
  - Empates ×1,0 en copas UEFA.

### Mesa en marcha (fase 1)
Científico de datos (actualizar datos), Investigador (bajas, fin de semana y Champions), Compilador (mercado, público, valor, Pleno, sueltas y bote) y Trader (cierre oficial, movimientos y calendario de noticias). Fase 2: Matemático, Físico y Risk Manager con los datos nuevos. Después, el Director decide y el Auditor firma la lista de control.


---

## v1 · Primera pasada de la mesa (lunes 2/11, mediodía)

**Quién trabajó:**
- Científico de datos: dataset puesto al día, de 23.112 a 23.631 partidos, hasta el 1/11.
- Investigador: bajas con fecha y verificación del informe externo de Perplexity.
- Compilador: mercado, público, valor, Pleno y sueltas.
- Trader: cierre oficial y movimientos de cuotas.
- Director: precio final, prueba del veto, robustez y boletos.

El Matemático y el Físico no se lanzaron como agentes por el límite de uso. La prueba de robustez la hizo el Director. Esta jornada no hay ensemble: el precio final es el modelo oficial v1 más los ajustes A/B del Investigador y el ajuste medido por derrota europea. El Auditor revisa el boleto final el martes.

**Cierre oficial (aviso de Loterías):** martes 3/11 a las 21:00 peninsular = **20:00 de Canarias**. En Eduardo Losilla, particulares a las 19:00 de Canarias. **Sellar entre las 15:15 y las 16:30 de Canarias; límite duro, las 17:00.**

### Prueba del veto "favorito que viene de perder en Europa" (medida hoy)
Partidos UEFA de 2025-26 y 2026-27. Fuera de muestra: el modelo se ajustó con datos anteriores a cada temporada.

| Grupo | Partidos | Victorias esperadas | Victorias reales | Diferencia |
|---|---|---|---|---|
| Favorito que venía de perder en Europa | 88 | 47,0 | 43 | **−4,5 puntos** (z = −0,88) |
| Favorito que no venía de perder | 147 | 78,5 | 88 | +6,5 puntos (z = +1,61) |

**Conclusión:**
- El efecto existe, pero es moderado y no es significativo con 88 partidos.
- Se pone en el precio como **−4,5 puntos al favorito** (P1, P2, P3, P8 y P9).
- Mantener además el veto absoluto sería contarlo dos veces. **Propuesta: sustituir el veto por este ajuste medido.** Pendiente de aprobación del usuario.
- El veto del campo nórdico (P2) se mantiene.
- De paso: en Europa, el modelo infravalora a los favoritos en general (+2,3 puntos de media).

### Precio final y consejo de la mesa
| Nº | Partido | Día | Final 1·X·2 | Mercado (control) | Investigador | Compilador | Científico | Trader |
|---|---|---|---|---|---|---|---|---|
| 1 | Barcelona – Aston Villa | mar | 52,6 · 21,6 · 25,8 | 77 · 13 · 10 | 1X | 1 | 12 | mantener |
| 2 | Bodø/Glimt – Lille | mar | 37,3 · 26,1 · 36,6 | 52 · 24 · 24 | 1X | 12 | 12 | doble |
| 3 | Man. United – Roma | mar | 42,6 · 25,8 · 31,6 | 41 · 24 · 35 | X2 | 12 | 12 | doble |
| 4 | Villarreal – PSG | mar | 26,9 · 21,1 · 52,0 | 19,5 · 20,6 · 59,9 | X2 | 2 | 2 | — |
| 5 | AEK – Real Madrid | mié | 15,4 · 18,6 · 66,0 | 11 · 14 · 75 | 2 | 2 | 2 | mantener |
| 6 | Fenerbahçe – Liverpool | mié | 18,5 · 18,7 · 62,8 | 19 · 21 · 60 | X2 | 2 | 2 | vigilar |
| 7 | B. Dortmund – Betis | mié | 51,4 · 22,5 · 26,1 | 55,5 · 22,4 · 22,1 | 1X | 1 | 1 | vigilar |
| 8 | Oporto – Nápoles | mié | 43,2 · 28,2 · 28,7 | 43 · 26 · 31 | 1X | 12 | 12 | doble |
| 9 | Lens – Como | mié | 34,3 · 26,9 · 38,8 | 32 · 24 · 44 | X2 | 12 | 12 | doble |
| 10 | Leipzig – Man. City | mié | 22,4 · 20,3 · 57,4 | 18 · 20 · 62 | X2 | 2 | 2 | vigilar |
| 11 | Slavia Praga – Arsenal | mié | 12,2 · 19,0 · 68,8 | 10 · 15 · 75 | 2 | 2 | 2 | — |
| 12 | Real Sociedad – Lyon | jue | 39,8 · 23,4 · 36,8 | 48,8 · 24,8 · 26,5 | 1X | 1 | 12 | — |
| 13 | Celta – Union SG | jue | 37,2 · 26,2 · 36,5 | 46 · 25 · 28 | X2 | 1 | 12 | doble |
| 14 | Getafe – Brighton | jue | 19,1 · 24,9 · 56,1 | 18 · 25 · 57 | X2 | 2 | 2 | vigilar |
| 15 | Pleno: Atlético – Bayern | mar | 36,1 · 21,9 · 42,1 | 34,4 · 23,8 · 41,8 | 1-1 | 1-1 | 1-M | — |

**Ajustes aplicados:**
- P1: −1 al 1 (bajas con fecha de E. García, Espart y Olmo; bajas del Villa).
- P2: +1 al 1 (Ethan Mbappé sancionado).
- P4: −1 al 2 (Kvaratskhelia).
- P8: +2 al 1 (Lobotka).
- P15: Bayern sin Saibari, Gnabry, Musiala ni Díaz; Atlético sin Hjulmand.

**Pendiente de hoy por la tarde:**
- Svilar en la convocatoria de la Roma (si no va: +3 al United).
- Portero del Bayern (si juega Ulreich: −4 más al Bayern).
- Parte de Gerard Moreno (si es baja: −3 al Villarreal).
- Olise.

### Discrepancias de 7 puntos o más con el mercado (revisión escrita del Científico)
| Nº | ¿Causa encontrada? | Revisión |
|---|---|---|
| P1 | No | El modelo ve al Villa casi tan fuerte como el Barça (6-0, 3-1, 2-1 al City); el Barça perdió 4-2 en París y el Clásico |
| P2 | Parcial | Noruega incompleta (80 de 200 partidos); la ventaja de campo es común. Lo cubre el veto nórdico |
| P3 | Sí | Racha del United (3 derrotas en 4); el modelo descuenta despacio |
| P12 | Parcial | El Lyon se valora por la temporada 2025-26; su 0-3 en Hoffenheim pesa poco |
| P13 | Sí | Faltaba la liga belga; el Union sube. Su dato sigue siendo corto |

### Boletos (12 €, 4 dobles completos)
Todos los dobles salen 12. Los signos del boleto son los del precio final. "Peor caso" = la peor de las tres comparaciones con el mejor boleto posible, calculando con el modelo, con el mercado y con una mezcla al 50%.

| Opción | Dobles | Vetos rotos | P(14) con el modelo | P(14) con el mercado | Peor caso | P(≥13) | P(≥12) |
|---|---|---|---|---|---|---|---|
| **Robusta (recomendada)** | **P2, P3, P9, P13** | Barça, Oporto | 1 entre 1.531 | 1 entre 476 | **90%** | 0,73% | 3,77% |
| Reglas | P2, P3, P8, P9 | Barça | 1 entre 1.822 | 1 entre 445 | 76% | 0,63% | 3,39% |
| Máx. modelo | P2, P9, P12, P13 | Barça, United, Oporto | 1 entre 1.385 | 1 entre 572 | 78% | 0,79% | 4,02% |

**Boleto robusto:** 1 · 12 · 12 · 2 · 2 · 2 · 1 · 1 · 12 · 2 · 2 · 1 · 12 · 2 · Pleno **1-1**.
Fallos esperados entre los 10 sencillos: 4,5.
**14 signos individuales:** 1 1 1 2 2 2 1 1 2 2 2 1 1 2 · Pleno 1-1.

### Pleno al 15 (Atlético – Bayern)
| Tipo | Marcador | Prob. |
|---|---|---|
| Principal | **1-1** | 9,3% |
| Conservador | 1-2 | 8,0% |
| De varianza | 1-M | 8,0% |

Público (Quiniela15): 1-2 21%, 2-2 16%, 2-1 12%. El 1-1 no está entre los más jugados: tiene valor.

### 5 sueltas
| # | Apuesta | Prob. | Cuota mínima |
|---|---|---|---|
| 1 | Barcelona marca | 91,1% | 1,10 |
| 2 | Liverpool marca | 90,8% | 1,10 |
| 3 | Real Madrid marca | 89,9% | 1,11 |
| 4 | Man. City marca | 88,8% | 1,13 |
| 5 | PSG marca | 88,5% | 1,13 |

Aciertos esperados: 4,5; P(las 5) ≈ 58%. **Risk Manager:** sin dinero por debajo de la cuota mínima y nunca en combinada. La única con valor según el Compilador es Leipzig–City menos de 3,5 goles (55%, cuota mínima 1,81, Bet365 1,91).

---

### Decisiones del usuario (lunes 2/11, mediodía)
| Qué | Decisión |
|---|---|
| Veto "favorito que viene de perder en Europa" | **Sustituido por el ajuste medido de −4,5 puntos** (ya incluido en el precio). Se mantienen los vetos del campo nórdico y del dato no verificado. Se actualizan el prompt maestro, el registro de errores y el índice |
| Boleto | **Lo que recomiende la mesa → opción robusta: dobles en P2, P3, P9 y P13**, a falta de la revisión del martes |
| Canal de sellado | **Administración física.** El cierre oficial es a las 20:00 de Canarias; ojo con el horario de la administración. La mesa entrega el boleto final el martes a las **10:30 de Canarias**, para poder sellar por la mañana o, si no, a primera hora de la tarde |

### Cambio de decisión del usuario (lunes 2/11, 09:48): 18 € y sin romper la regla
"No rompas la regla, quiero los 18 €, como la jornada anterior (12 € + 6 €)."
- **Se mantiene el veto**: ningún favorito que venga de perder en Europa va de sencillo. El ajuste medido de −4,5 puntos sigue en el precio.
- Con 24 apuestas, la única forma de cubrir los 4 partidos vetados (P1 Barça, P2 Bodø, P3 United, P8 Oporto) en todas las columnas es **1 triple + 3 dobles**: triple en P8 (es el que más suma) y dobles en P1, P2 y P3.

| Boleto | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | Pleno |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Boleto 1 · 16 apuestas · 12 € | 12 | 12 | 12 | 2 | 2 | 2 | 1 | 12 | 2 | 2 | 2 | 1 | 1 | 2 | 1-1 |
| Boleto 2 · 8 apuestas · 6 € | 12 | 12 | 12 | 2 | 2 | 2 | 1 | X | 2 | 2 | 2 | 1 | 1 | 2 | 1-1 |
| Juntos (un solo boleto) | 12 | 12 | 12 | 2 | 2 | 2 | 1 | **1X2** | 2 | 2 | 2 | 1 | 1 | 2 | 1-1 |

| Opción | € | P(14) modelo | P(14) mercado | P(14) mezcla | P(≥13) | P(≥12) |
|---|---|---|---|---|---|---|
| **18 € con la regla (decisión del usuario)** | 18 | 1 entre 1.654 | 1 entre 504 | 1 entre 893 | 0,71% | 3,82% |
| 12 € con la regla (dobles P1, P2, P3, P8) | 12 | 1 entre 2.302 | — | — | 0,53% | 2,95% |
| 12 € robusta (rompe Barça y Oporto) | 12 | 1 entre 1.531 | 1 entre 476 | 1 entre 828 | 0,73% | 3,77% |
| 18 € sin regla (triple P9 + dobles P2, P12, P13) | 18 | 1 entre 1.013 | 1 entre 435 | 1 entre 647 | 1,04% | 5,12% |

Nota del Director: esta jornada la regla es cara. Con ella, los 18 € rinden algo menos que los 12 € de la opción robusta. Es decisión del usuario y se respeta. **Nota del Risk Manager:** 18 € como presupuesto fijo de la jornada, nunca para recuperar.

### Foto de cuotas bet365 (lunes 2/11, 13:00 de Canarias, navegador integrado) · solo control
| Nº | Partido | bet365 1 · X · 2 | Justo (%) | Movimiento frente a OddsPortal del domingo, 00:15 | ¿Hay noticia que lo explique? |
|---|---|---|---|---|---|
| 1 | Barcelona – Aston Villa | 1,25 · 7,50 · 8,00 | 75,6 · 12,6 · 11,8 | −1,4 al 1 | — |
| 2 | Bodø/Glimt – Lille | 1,80 · 4,00 · 4,00 | 52,6 · 23,7 · 23,7 | estable | — |
| 3 | Man. United – Roma | 2,25 · 4,00 · 2,75 | 42,0 · 23,6 · 34,4 | estable | — |
| 4 | Villarreal – PSG | 5,00 · 4,50 · 1,57 | 18,9 · 21,0 · 60,1 | estable | — |
| 5 | AEK – Real Madrid | 9,00 · 7,00 · 1,25 | 10,5 · 13,6 · 75,9 | estable | — |
| 6 | Fenerbahçe – Liverpool | 5,25 · 4,50 · 1,53 | 17,9 · 20,8 · 61,3 | estable | — |
| 7 | B. Dortmund – Betis | 1,70 · 4,33 · 4,33 | 56,0 · 22,0 · 22,0 | estable | — |
| 8 | Oporto – Nápoles | 1,95 · 3,60 · 3,75 | 48,5 · 26,3 · 25,2 | **+5,8 al Oporto** | **Sí:** Lobotka, baja, y el Nápoles perdió 2-0 en Turín (ya estaba en nuestro ajuste) |
| 9 | Lens – Como | 3,00 · 3,75 · 2,20 | 31,6 · 25,3 · 43,1 | estable | — |
| 10 | Leipzig – Man. City | 5,00 · 4,50 · 1,57 | 18,9 · 21,0 · 60,1 | estable | — |
| 11 | Slavia Praga – Arsenal | 10,00 · 6,50 · 1,25 | 9,5 · 14,6 · 75,9 | estable | — |
| 15 | Atlético – Bayern | 2,55 · 4,00 · 2,45 | 37,3 · 23,8 · 38,9 | **+3,7 al Atlético** | **Sí:** las bajas y la portería del Bayern (ya estaban en nuestro ajuste) |

Nota: se comparan casas distintas, así que parte de la diferencia puede ser de la casa y no del mercado. P12–P14 (Europa League y Conference) no salen en la portada; quedan para el martes. Archivo: scratchpad/j19/bet365_snap_lun1300.json.

### Tercera referencia de control: SportRadar (integrado, lunes 2/11)
| Nº | Partido | SportRadar 1 · X · 2 |
|---|---|---|
| 1 | Barcelona – Aston Villa | 77,7 · 12,4 · 9,9 |
| 2 | Bodø/Glimt – Lille | 51,6 · 23,8 · 24,6 |
| 3 | Man. United – Roma | 40,5 · 24,4 · 35,1 |
| 4 | Villarreal – PSG | 19,5 · 19,8 · 60,7 |
| 5 | AEK – Real Madrid | 9,5 · 13,4 · 77,1 |
| 15 | Atlético – Bayern | 36,3 · 24,3 · 39,4 |

Coincide con el mercado. Clasificación de la Champions tras la J3 (SportRadar): PSG, Villa, Liverpool, Madrid y Betis con 9 puntos; Barça 8.º (6); Bayern 14.º (5); Atlético 16.º (4); United 20.º (3); Bodø 28.º (3); Oporto y Lille 34.º y 35.º (0).


---

## v2 · Revisión final (martes 3/11, de 07:30 a 08:45 de Canarias)

**Resultado: el triple pasa de P8 a P1** (regla de valor; ver "Boleto final"). Cambian el precio de P1, P3 y P4 y una suelta: sale "PSG marca" y entra "Arsenal marca". El Auditor revisó la v2. Su primera firma fue **NO FIRMADO** por 6 puntos; los 6 se corrigieron abajo. La segunda fue **FIRMADO CON RESERVA**: el horario de la administración y la regla de valor (ver "Auditoría").

### Noticias comprobadas
Regla: solo cuentan las bajas con fecha y fuente de 72 h o menos. "Duda" = 0.

| Nº | Partido | Noticia | Fuente y fecha | Ajuste |
|---|---|---|---|---|
| 1 | Barcelona – Aston Villa | Koundé, baja (vuelve tras el parón). Christensen "probablemente" fuera: es duda, cuenta 0 | [Sportaragón](https://www.sportaragon.com/futbol-aragon/barca-aston-villa-hora-bajas-flick/20261103081040162262.html), 3/11 08:10 | −1 al 1 (bajas del Barça en total: −3; tope 5) |
| 3 | Man. United – Roma | Svilar (portero), baja confirmada por Gasperini. Koné y Dybala también, pero ya faltaban hace dos semanas y están en los datos | [Get Italian Football News](https://www.getfootballnewsitaly.com/2026/roma-set-for-three-major-absentees-v-manchester-united-confirms-gian-piero-gasperini/), 2/11 | +3 al 1 (regla del portero; tope 10) |
| 4 | Villarreal – PSG | Gerard Moreno, baja | [El Gol Digital](https://www.elgoldigital.com/futbol/champions-league/villarreal-psg-previa-champions-league-horario-bajas-jornada-4), 3/11 07:30 | −3 al 1 |
| 4 | Villarreal – PSG | Dembélé, Marquinhos y Nuno Mendes, fuera de la lista oficial (Kvaratskhelia ya se descontó el lunes) | [beIN Sports](https://www.beinsports.com/fr-fr/football/uefa-ligue-des-champions/articles/ligue-des-champions-avec-quatre-grosses-absences-le-groupe-du-psg-contre-villarreal-2026-11-02), 2/11 | −4 al 2 (bajas del PSG en total: −5; tope 5) |
| 15 | Atlético – Bayern (Pleno) | Neuer y Olise viajan; no está decidido si son titulares: duda, cuenta 0. No se activa el caso Ulreich | [Sky Sport](https://sport.sky.de/fussball/artikel/mini-kader-in-madrid-bayern-verkuendet-aufgebot-gegen-atletico-mit-olise-und-neuer/13607167/34942) y [Sport1](https://www.sport1.de/news/fussball/champions-league/2026/11/gewissheit-bei-manuel-neuer-und-michael-olise-ein-bayern-juwel-dabei), 2/11 | Ninguno |
| 2 | Bodø/Glimt – Lille | El mercado sube 3,8 puntos al Bodø. No he encontrado la noticia | — | Ninguno (va doble) |
| 5–14 | Miércoles y jueves | Se juegan después del cierre (tope del 2%). Porteros de Madrid, Liverpool, City, Arsenal, Dortmund y Nápoles disponibles (Auditor). Sin noticias nuevas en Celta – Union | — | Ninguno |

### Precio que cambia
| Nº | Partido | Lunes 1 · X · 2 | Martes 1 · X · 2 | Mercado del martes (SportRadar) |
|---|---|---|---|---|
| 1 | Barcelona – Aston Villa | 52,6 · 21,6 · 25,8 | **51,6 · 22,0 · 26,4** | 75,3 · 13,1 · 11,6 |
| 3 | Man. United – Roma | 42,6 · 25,8 · 31,6 | **45,6 · 24,5 · 29,9** | 43,8 · 23,9 · 32,3 |
| 4 | Villarreal – PSG | 26,9 · 21,1 · 52,0 | **26,0 · 23,9 · 50,1** | 21,9 · 20,9 · 57,2 |

El Auditor rehízo el cálculo y coincide (diferencia 0). Nota suya: en P3 el Investigador quitaba los 3 puntos solo al 2; el script los reparte entre X y 2. No cambia ningún signo.

### Movimiento de cuotas frente al lunes (SportRadar; solo control)
| Nº | Partido | Lunes | Martes 07:32 | Movimiento | ¿Hay noticia que lo explique? |
|---|---|---|---|---|---|
| 1 | Barcelona – Aston Villa | 77,7 · 12,4 · 9,9 | 75,3 · 13,1 · 11,6 | −2,4 al Barça | Sí: Koundé y Christensen |
| 2 | Bodø/Glimt – Lille | 51,6 · 23,8 · 24,6 | 55,4 · 22,5 · 22,1 | +3,8 al Bodø | No encontrada |
| 3 | Man. United – Roma | 40,5 · 24,4 · 35,1 | 43,8 · 23,9 · 32,3 | +3,3 al United | Sí: Svilar |
| 4 | Villarreal – PSG | 19,5 · 19,8 · 60,7 | 21,9 · 20,9 · 57,2 | −3,5 al PSG | Sí: Dembélé, Marquinhos y Mendes (y Moreno en sentido contrario) |
| 5 | AEK – Real Madrid | 9,5 · 13,4 · 77,1 | 9,6 · 13,3 · 77,1 | Estable | — |
| 15 | Atlético – Bayern | 36,3 · 24,3 · 39,4 | 35,5 · 24,1 · 40,4 | +1,0 al Bayern | Sí: Neuer y Olise viajan |

El navegador no estaba conectado esta mañana: no hay foto nueva de bet365. SportRadar no da P6–P14.

### Diferencias de 7 puntos o más con el mercado (revisión escrita)
| Nº | Diferencia en el signo jugado | Revisión |
|---|---|---|
| P1, P2 | 23,7 y 18,1 puntos en el 1 | Revisadas el lunes. Van dobles (12), así que no deciden el boleto |
| P12, P13 | 9,0 y 9,2 en el 1 | Revisadas el lunes. Sencillo 1, el mismo signo que el mercado |
| **P4** | **7,1** en el 2 (50,1 frente a 57,2); el lunes, 8,7 frente a SportRadar | **Causa parcial.** Mismo signo que el mercado; la diferencia es de tamaño y se ha estrechado: el mercado bajó el 2 en 3,5 puntos con las bajas y nosotros en 1,9. Lo que queda encaja con la infravaloración de los favoritos en Europa que tiene el modelo (+2,3 puntos de media, medida el lunes). El sencillo sigue siendo 2 |
| **P5** | **9,0** en el 2 (66,0 frente a 75 de OddsPortal; unos 11 con SportRadar) | **Causa no encontrada.** Hipótesis: con tan pocos datos del AEK (12 partidos en 365 días), su fuerza es poco fiable; además, la infravaloración general de los favoritos en Europa. Mismo signo que el mercado: sencillo 2 |
| P11 | 6,2 con OddsPortal y 7,1 con bet365 del lunes | Vigilar. Mismo signo (2). Al Slavia también le faltan datos |

La v1 dejó P4 y P5 sin revisión escrita: se anota como R2 en el registro de errores.

### Sencillos por debajo del 65% (aviso ⚠️)
| Nº | Partido | Signo | Prob. de la mesa |
|---|---|---|---|
| 4 | Villarreal – PSG | 2 | ⚠️ 50,1% |
| 6 | Fenerbahçe – Liverpool | 2 | ⚠️ 62,8% |
| 7 | B. Dortmund – Betis | 1 | ⚠️ 51,4% |
| 9 | Lens – Como | 2 | ⚠️ 38,8% |
| 10 | Leipzig – Man. City | 2 | ⚠️ 57,4% |
| 12 | Real Sociedad – Lyon | 1 | ⚠️ 39,8% |
| 13 | Celta – Union SG | 1 | ⚠️ 37,2% |
| 14 | Getafe – Brighton | 2 | ⚠️ 56,1% |

Solo P5 (66,0%) y P11 (68,8%) llegan al 65%. Fallos esperados entre los 10 sencillos: 4,7. Con 18 € y la regla no hay dinero para más dobles.

### Comparación de diseños con el precio del martes (24 apuestas, con la regla)
| Diseño | P(14) mesa · mercado · mezcla | P(≥13) mesa · mercado · mezcla | P(≥12) mesa · mercado · mezcla | Valor frente al público |
|---|---|---|---|---|
| Triple P8 + dobles P1, P2, P3 (el del lunes) | 1/1.695 · 1/517 · 1/916 | 0,69% · 1,83% · 1,15% | 3,77% · 8,11% · 5,62% | base |
| Triple P2 + dobles P1, P3, P8 | 1/1.743 · 1/541 · 1/951 | 0,68% · 1,76% · 1,11% | 3,69% · 7,85% · 5,47% | +6% |
| Triple P3 + dobles P1, P2, P8 | 1/1.781 · 1/532 · 1/952 | 0,66% · 1,79% · 1,11% | 3,63% · 7,95% · 5,46% | 0% |
| **Triple P1 + dobles P2, P3, P8 (boleto final)** | **1/1.839 · 1/607 · 1/1.035** | **0,65% · 1,59% · 1,03%** | **3,54% · 7,21% · 5,13%** | **+25% (+29% con el mercado)** |
| Sin la regla, solo referencia: triple P9 + dobles P2, P12, P13 | 1/1.000 · 1/427 · 1/638 | 1,05% | 5,14% | — |

**Decisión sobre el valor: el triple pasa a P1.** La regla escrita (prompt maestro, fase 10; agentes-mesa §4) dice: entre los boletos con al menos el 90% de la mejor P(14) **con el precio final**, el de más valor. El triple en P1 conserva el 92,1% y da un **25% más de valor con el precio de la mesa y un 29% más con el del mercado**: la X del Barça la juega el 8% del público, la mesa le da un 22% y el mercado un 13%. A cambio, pierde un 8% de P(14) con la mesa, un 15% con el mercado y un 11,5% con la mezcla. En la v2 se había rechazado por robustez (el peor de los tres precios), pero ese criterio no está escrito como regla y el valor gana con los dos precios. **Se aplica la regla.**

**Alcance de la regla (decisión del Director, para seguimiento):** la regla compara los diseños habituales de la mesa, es decir, dónde va el triple y dónde los dobles. Una búsqueda amplia cambiando además sencillos solo en el boleto 2 da diseños con un valor del +180% al +355% dentro del 90% de P(14). Por ejemplo: triple P1 con P12 = 2 y P13 = 2 en el boleto 2. Pero ese valor depende de los porcentajes del público de Quiniela15, que no son oficiales, y de los partidos en los que el modelo más se separa del público. No se usa hasta comprobarlo con los porcentajes oficiales de Loterías. Queda como seguimiento.

### Boleto final (v2)
| Boleto | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | Pleno |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Boleto 1 · 16 apuestas · 12 € | 12 | 12 | 12 | 2 | 2 | 2 | 1 | 12 | 2 | 2 | 2 | 1 | 1 | 2 | 1-1 |
| Boleto 2 · 8 apuestas · 6 € | **X** | 12 | 12 | 2 | 2 | 2 | 1 | 12 | 2 | 2 | 2 | 1 | 1 | 2 | 1-1 |
| Juntos (un solo boleto) | **1X2** | 12 | 12 | 2 | 2 | 2 | 1 | 12 | 2 | 2 | 2 | 1 | 1 | 2 | 1-1 |

| Medida | Mesa | Mercado | Mezcla |
|---|---|---|---|
| P(14) | 1 entre 1.839 | 1 entre 607 | 1 entre 1.035 |
| P(≥13) | 0,65% | 1,59% | 1,03% |
| P(≥12) | 3,54% | 7,21% | 5,13% |
| Valor frente al boleto del lunes | +25% | +29% | — |

Vetos: P1, P2, P3 y P8 nunca llevan al favorito como signo único (P1 lleva 1 y 2 en el boleto 1, y X en el boleto 2; P8 lleva 1 y 2 en los dos). Campo nórdico (P2): doble.

### Disensos del Investigador (regla R6), con su coste frente al boleto final
Orden de las reglas: 1) vetos; 2) regla de valor (90% de la mejor P(14) con el precio final); 3) R6, solo si el boleto que resulta sigue cumpliendo la 2.

| Nº | Boleto → Investigador | Coste en P(14): mesa · mercado · mezcla | Valor (mesa · mercado) | Decisión |
|---|---|---|---|---|
| 1 | 12 → 1X | — | — | **Entra de hecho:** el triple cubre 1 y X |
| 2 | 12 → 1X | −14,3% · +0,5% · −6,7% | −43% · −21% | No entra (más del 10% con la mesa) |
| 3 | 12 → X2 | −27,9% · −26,1% · −27,0% | −12% · −11% | No entra |
| 8 | 12 → 1X | −0,7% · −6,8% · −3,8% | −35% · −41% | No entra por la regla de valor: el 2 del Nápoles lo juega el 15% del público y la mesa le da un 29% |
| 9 | 2 → la X en el boleto 2 | −6,8% · −6,0% · −6,8% | +9% · −1% | No entra: el boleto bajaría al 86% de la mejor P(14) |
| 13 | 1 → la X en el boleto 2 | −6,5% · −6,0% · −6,8% | +23% · +8% | No entra: también bajaría al 86% |
| 12 | 1 → la X en el boleto 2 | −9,1% · −6,4% · −8,0% | +22% · +13% | No entra (84%) |
| 4, 6, 7, 10, 14 | sencillo → la X en el boleto 2 | entre −7,4% y −15,5% | — | No entran (por debajo del 90%) |

Los disensos quedan anotados para medirlos tras la jornada (seguimiento "Disensos del Investigador").

### Sueltas (recalculadas; cuota mínima redondeada hacia arriba)
| # | Apuesta | Prob. | Cuota mínima |
|---|---|---|---|
| 1 | Liverpool marca | 90,8% | 1,11 |
| 2 | Barcelona marca | 90,4% | 1,11 |
| 3 | Real Madrid marca | 89,9% | 1,12 |
| 4 | Man. City marca | 88,8% | 1,13 |
| 5 | **Arsenal marca** (entra) | 88,1% | 1,14 |

"PSG marca" baja del 88,5% al 84,4% con el precio del martes (sobre todo, por la baja de Dembélé) y sale. Cálculo: los goles esperados del lunes se escalan hasta reproducir el 1X2 del martes (sueltas_v2.py); el campo 'marca' de j19_Fp2.json ya está actualizado en P1, P3 y P4. Aciertos esperados: 4,5; P(las 5) ≈ 58%. Nunca en combinada.

### Pleno al 15 (sin cambios)
1-1 principal (9,3%), 1-2 conservador (8,0%), 1-M de varianza (8,0%).

### Sellado
- **Cierre oficial:** martes 3/11 a las 21:00 peninsular = **20:00 de Canarias** ([aviso de Loterías](https://www.loteriasyapuestas.es/es/avisos-de-interes)). Eduardo Losilla, particulares: 19:00 de Canarias.
- **No sabemos el horario de la administración del usuario** (punto ✖ del Auditor). Por eso: **sellar esta mañana.** Si no se puede, por la tarde en cuanto reabra, y siempre antes de las 19:00 de Canarias. Se retira la ventana de 15:15 a 16:30 de la v1: puede caer en el cierre de mediodía.
- Aviso: que la jornada no tiene bote lo dice Quinielafutbol.info, que no es una fuente oficial. Los porcentajes del público son de Quiniela15 (no oficiales).

### Auditoría
| Corrección pedida por el Auditor | Estado |
|---|---|
| 1. Revisión escrita de P4 y P5 (y P11, recomendable) | Hecha (tabla de diferencias) |
| 2. Aplicar R6 o explicar por qué no; decidir sobre el valor del triple en P1 | Hecho: no entran, con su coste y su motivo |
| 3. Horario de la administración | **Pendiente del usuario.** Mientras tanto: sellar por la mañana; límite, las 19:00 de Canarias |
| 4. Cifras de la v2 y ⚠️ en los sencillos por debajo del 65% | Hecho |
| 5. Cuotas mínimas hacia arriba y motivo de quitar "PSG marca" calculado | Hecho |
| 6. Bote y porcentajes del público con su fuente | Hecho (marcados como no oficiales) |

**Segunda pasada del Auditor (08:50): FIRMADO CON RESERVA.**

| Reserva | Cómo queda |
|---|---|
| Frases de P4 y P5 inexactas | Corregidas (P4: el mercado bajó el 2 más que nosotros; P5: hipótesis, causa no encontrada) |
| Rechazar el triple en P1 iba contra la regla de valor escrita, que mide el 90% con el precio final | **Se aplica la regla: el triple pasa a P1.** Se informa al usuario |
| Disensos: decir que P1 1X ganaba valor con el mercado (+8%) | Ya no aplica: con el triple, P1 cubre 1 y X |
| Horario de la administración | Pendiente del usuario. Sellar por la mañana; límite, las 19:00 de Canarias |

Archivos: scratchpad/j19/v2/ (ajustar_v2.py, j19_Fp2.json, eval_v2.py, sueltas_v2.py, r6_opciones.py, r6_triple1.py, busca_valor.py, auditor.md).


---

## v3 · Boleto definitivo (martes 3/11, 13:30 de Canarias): variante de valor en el boleto 2

**Origen:** a las 13:22, el usuario envió una captura de Quiniela15 con su pronóstico (SIS) y lo que más juegan sus usuarios (USU).

| Nº | SIS | USU | Mesa | Nota |
|---|---|---|---|---|
| 1–14 | 1 1 X 2 2 X 1 1 1 2 2 X 2 2 | 1 1 1 2 2 2 1 1 2 2 2 1 1 2 | 1 1 1 2 2 2 1 1 2 2 2 1 1 2 | **Los 14 signos individuales de la mesa son los 14 que más juega el público** |
| Pleno | 1-1 | 1-2 | 1-1 | El público se va al 1-2 (21%) |

- **SIS no es un dato del modelo** (regla: los pronósticos de otras fuentes se analizan, no entran). Su columna sale 1 de cada 238.639 veces con nuestro precio. Sirve para señalar dónde se pasa el público: P9, P12 y P13.
- **En esos partidos, el mercado le da al signo contrario mucho más de lo que se juega:** Lens 32% (público 14%), Lyon 27% (17%), Union 28% (23%). La mesa los ve casi a cara o cruz.
- **La mesa no acompaña a la SIS en la X del P3 (25%) ni en la X del P6 (19%).**

**Decisión del usuario: "Tu recomendación"**, es decir, la variante.

| Boleto | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | Pleno |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Boleto 1 · 16 apuestas · 12 € | 12 | 12 | 12 | 2 | 2 | 2 | 1 | 12 | 2 | 2 | 2 | 1 | 1 | 2 | 1-1 |
| **Boleto 2 · 8 apuestas · 6 €** | **X** | 12 | 12 | 2 | 2 | 2 | 1 | 12 | 2 | 2 | 2 | **2** | **2** | 2 | 1-1 |

| | Boleto firmado de la mañana | **Boleto definitivo** |
|---|---|---|
| P(14), mesa · mercado | 1/1.839 · 1/607 | **1/1.878 · 1/666** |
| P(≥13), mesa · mercado | 0,65% · 1,59% | **0,69% · 1,55%** |
| P(≥12), mesa · mercado | 3,54% · 7,21% | **3,88% · 7,23%** |
| Valor del 14, mesa · mercado | base | **+264% · +69%** |
| Fracción de la mejor P(14) (regla de valor, ≥90%) | 92,1% | **90,2%** |

**Por qué se levanta la cautela de la mañana**, que dejaba este tipo de cambios a la espera de porcentajes oficiales del público:
- Se hizo una prueba de sensibilidad con el Lyon y el Union al 25% del público.
- Con esos porcentajes, la variante sigue dando más valor.
- El sesgo del público lo confirma también el mercado, no solo el modelo.

Coincide con la preferencia del usuario de "aprovechar los sesgos del público a su favor". Cálculo: scratchpad/j19/v2/sis_vs_mesa.py. Revisión del Auditor: lanzada a las 13:30.

**Auditor (13:40): FIRMADO.** Ha comprobado:
- 24 columnas distintas y 18 €.
- Los vetos se cumplen y el Pleno 1-1 va en las 24.
- P(14), P(≥13) y P(≥12) coinciden.
- El boleto conserva el 90,25% de la referencia.
- Valor frente al boleto firmado por la mañana: +263,6% con la mesa y +69,4% con el mercado.

**Sensibilidad.** Con el público al 25% en el 2 de P12 y de P13, la ganancia de valor sigue siendo positiva, pero baja a menos de la mitad:
- +127% con la mesa y +20% con el mercado, si se ponen esas filas directamente al 25%;
- +150% y +28%, si se suman 25 puntos y se renormaliza la fila.

**Avisos.**
- Con el mercado, el boleto conserva el 77,7% de la mejor P(14). La regla se cumple porque se mide con la mesa.
- Casi todo el valor depende de lo poco que el público juega el 2 en P12 y P13: es lo primero que hay que medir en el post-mortem.
