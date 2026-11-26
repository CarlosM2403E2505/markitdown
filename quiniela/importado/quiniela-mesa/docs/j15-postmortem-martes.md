# J15 — POST-MORTEM DEL MARTES (6 de 15 jugados)

Revisado el miércoles 21/10 a las 07:30.

## Resultados del martes

| Nº | Partido | Resultado | Signo | Boleto 216 | 5 columnas | Prob. declarada del signo jugado |
|---|---|---|---|---|---|---|
| 1 | Oporto – PSV | 0-1 | **2** | 1 ❌ | 1 en las 5 ❌ | 1 al 53.9% (el 2 tenía 25.3%) |
| 2 | Liverpool – Villarreal | 4-3 | 1 | ✅ | ✅ | 60.9% |
| 3 | Man City – AEK | 5-1 | 1 | ✅ | ✅ | 78.8% |
| 4 | Nápoles – Bodø | 4-3 | 1 | ✅ (triple) | ✅ | 50.5% |
| 5 | Stuttgart – Atlético | 1-1 | **X** | 12 ❌ | 2 en las 5 ❌ | doble 12 al 77.1% (X 22.9%) |
| 15 | PSG – Barcelona | 4-2 | Pleno **M-2** | M-1 ❌ | M-1 ❌ | M-2 era el 3º del modelo (10.7%) |

Las 5 columnas tienen 2 fallos cada una: como máximo pueden llegar a 12. El boleto de 216 tampoco puede hacer 14.

## Auditoría de calibración

- Con las 5 columnas, en los partidos del martes se esperaban **2.1 fallos**; hubo **2**. El modelo dijo la verdad sobre cuánto iba a fallar.
- Total de goles PSG–Barça: el modelo esperaba 4.5 (xG 2.50–2.01), hubo 6. Bien en la dirección (partido abierto, PSG goleador), M-2 estaba a 0.5 puntos del M-1 elegido.
- Liverpool–Villarreal 4-3 y Nápoles–Bodø 4-3: partidos de muchos goles, como marcaba el modelo (Más de 2.5 al 69% y 59%).

## Qué falló y por qué

1. **Oporto–PSV.** El ajuste por bajas (PSV sin 6 jugadores) subió el 1 de 49% a 54%. El PSV ganó igual. Sin el ajuste, el 2 tenía un 30%. **El ajuste del Live Trader fue en contra.** No cambió el signo (el 1 seguía primero), pero confirma que esos ajustes son criterio no validado.
2. **Stuttgart–Atlético.** El doble cubría 1 y 2 (77%) y salió X (23%). El optimizador nunca elige la X en un doble cuando el tercer signo pesa más; es lo correcto por probabilidad, pero en 2 jornadas seguidas los empates han roto el boleto.
3. **Pleno.** Tres resultados casi empatados (12.3 / 11.2 / 10.7). Salió el tercero.

## Mejoras medidas (no de opinión)

### A. Factor de empates por competición — IMPLEMENTADO
Medido sobre 4.683 partidos no vistos:

| | Empates que declara el modelo | Empates reales |
|---|---|---|
| Ligas, partidos parejos | 25.9% | 27.5% |
| Ligas, favorito claro | 21.5% | 22.9% |
| Copas UEFA | 22.1% | 18.2% |

- En **ligas nacionales** el Poisson se queda corto de empates en todos los tramos. Multiplicar los empates por **1.08** mejora el log-loss en los dos periodos de prueba. **Se aplica a partir de ahora en jornadas de liga.**
- En **copas** pasa lo contrario: hay menos empates de los que declara. No se toca (factor 1.0). El empate del Stuttgart fue varianza, no sesgo.
- Esto explica en parte la J14 (3 X en liga + Pleno 1-1).

### B. Regla nueva para el Live Trader
- Ningún ajuste por bajas mueve más de un **5%** los goles esperados, salvo baja confirmada del delantero centro titular o del portero.
- Cada ajuste se registra con su resultado para medir si aporta. Si tras 30 ajustes no mejora el log-loss, se eliminan.

### C. La verdad sobre el presupuesto
- 5 columnas = 0.07% de hacer 14 (1 de cada ~1.400 jornadas). Con 2-3 signos sencillos por debajo del 55% es matemáticamente normal fallar 2 cada martes.
- El modelo puede mejorar la calibración y el valor, no eliminar los fallos. Para acercarse al 14 hace falta cobertura (más columnas por jornada, o una peña), no más precisión.

## Pendiente del miércoles y el jueves
Bayern–Arsenal, Como–United, Brujas–Lens, Inter–Shakhtar, Betis–Feyenoord, Real Madrid–Leipzig, Celtic–Celta, Lillestrøm–R. Sociedad, Getafe–Lugano. Las columnas aún pueden puntuar para 10-12 aciertos.
