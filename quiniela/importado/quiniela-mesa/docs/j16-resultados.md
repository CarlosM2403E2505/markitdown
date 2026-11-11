# J16 — RESULTADOS Y POST-MORTEM (lunes 26/10, falta Sevilla–Osasuna)

| Nº | Partido | Resultado | Signo | Boleto (Red Team) |
|---|---|---|---|---|
| 1 | Rayo – Elche | 0-3 | 2 | 1 ❌ |
| 2 | Valencia – Villarreal | 1-2 | 2 | 12 ✅ |
| 3 | Atlético – Deportivo | 1-0 | 1 | 1 ✅ |
| 4 | Athletic – Getafe | 4-0 | 1 | 1X ✅ |
| 5 | Celta – Betis | 0-0 | X | 1 ❌ |
| 6 | Real Sociedad – Levante | 2-1 | 1 | 1 ✅ |
| 7 | Sevilla – Osasuna | lunes 21:00 | — | 1 |
| 8 | Leganés – Mallorca | 1-1 | X | X2 ✅ |
| 9 | Almería – Oviedo | 2-2 | X | 12 ❌ |
| 10 | Sabadell – Tenerife | 1-1 | X | 1 ❌ |
| 11 | Logroño F – Badalona F | 1-0 | 1 | 12 ✅ |
| 12 | Deportivo F – Alavés F | 2-1 | 1 | 12 ✅ |
| 13 | Eibar F – Madrid CFF | 2-2 | X | 12 ❌ |
| 14 | Real Madrid F – Tenerife F | 3-2 | 1 | 1 ✅ |
| P15 | Barcelona – Real Madrid | 1-2 | Pleno 1-2 | M-1 ❌ |

**Mejor columna: 8 de 13** (C4); con victoria del Sevilla, 9. Sin premio (hace falta 10). La variante "óptima P(14)" también se queda en 8 (C2 y C4).

## 5 sueltas: 4 de 5 ✅
Barça marca ✅ (1-2) · Atlético marca ✅ · Athletic–Getafe menos de 3,5 ❌ (4-0) · Real Sociedad marca ✅ · Leganés–Mallorca menos de 3,5 ✅.

## Qué pasó
1. **Jornada de empates: 5 X en 13 (6 si empata el Sevilla).** La media histórica es 3,55; el modelo esperaba 3,65. Una jornada con 6+ X sale el 14% de las veces. Los tres partidos de Segunda acabaron en empate. Es varianza (≈1 desviación típica), pero rompió el boleto: la reducida solo cubría la X en Athletic (1X) y Leganés (X2).
2. **Error de proceso en el Rayo:** nuestra propia regla permite superar el tope del 5% cuando falta el portero titular, y Batalla no jugaba. No lo apliqué. El Rayo perdió 0-3.
3. **Red Team:** pasar Sabadell de 1X a 1 costó un acierto (salió X). Celta (1 sencillo) habría fallado igual con el doble 12. Las dos variantes empatan en 8.
4. **Pleno:** el Madrid ganó en el Camp Nou (1-2). El modelo daba 20,8% al 2 y 5,7% al 1-2.
5. **Suelta fallida:** el Getafe venía de encajar 5 contra el Lugano el jueves; le quitamos ataque por cansancio pero no defensa. El Athletic le metió 4.

## Reglas que salen de aquí
- **Baja del portero titular: aplicar el ajuste (hasta −10% a la defensa propia).** Ya estaba en el prompt; ahora es obligatorio revisarlo partido a partido.
- **Cansancio europeo: también a la defensa** del equipo que jugó el jueves, no solo al ataque (pendiente de medir con datos).
- **Segunda igualada**: con dos equipos de Segunda parejos, la X debe entrar en el doble antes que el signo menos probable de otro partido (a validar con el histórico de Segunda).

## Cierre (27/10)
**Sevilla 2-0 Osasuna** (FutbolTotal). El signo 1 estaba en el boleto → **mejor columna final: 9 de 14**. Sin premio (hacen falta 10). Signos finales: 2 2 1 1 X 1 1 X X X 1 1 X 1 · Pleno 1-2.
