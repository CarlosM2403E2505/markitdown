# PRUEBA DE CONFIANZA — pronósticos registrados ANTES de cada partido

> **Para qué:** el usuario quiere comprobar si se puede fiar de la mesa. Cada pronóstico se apunta aquí con la hora y antes de que empiece el partido, con la probabilidad de la mesa y la del mercado (bet365, solo control). Después se anota el resultado.
>
> **Cómo se mide:** acertar un día no prueba nada. Lo que se mide, con muchos partidos, es:
> 1. **Calibración:** de los signos que damos al 60%, ¿sale más o menos el 60%?
> 2. **Mesa frente a mercado:** el log-loss de las dos; quien tenga menos, predice mejor.
> 3. **Sueltas:** aciertos reales frente a los esperados.
>
> Hasta tener unos 50 partidos, **no se pone dinero por "valor" del modelo contra el mercado** (regla del Risk Manager).

## Lunes 2/11/2026 · registrado a las 13:10 de Canarias (antes del primer partido)

Modelo oficial con los datos hasta el 1/11. Primera con su ventaja de campo propia; empates ×1,08 en ligas. Mercado: bet365 a las 13:00–13:08 de Canarias, sin margen.

| Hora (Canarias) | Partido | Mesa 1 · X · 2 | bet365 1 · X · 2 (justo) | Signo de la mesa | Prob. | Diferencia con el mercado |
|---|---|---|---|---|---|---|
| 15:15 | Oviedo – Las Palmas (Segunda) | 47,1 · 28,1 · 24,9 | 57,1 · 24,1 · 18,8 (1,65 · 3,90 · 5,00) | **1** | 47% | 10 puntos (el mercado ve más al Oviedo) |
| 17:30 | Valladolid – Leganés (Segunda) | 37,4 · 29,3 · 33,2 | 44,9 · 29,0 · 26,2 (2,10 · 3,25 · 3,60) | **1X** | 67% | 7,5 puntos |
| 19:00 | Tenerife F – Athletic F (Liga F, P14 de la J18) | 56,1 · 21,5 · 22,3 | — | **1** | 56% | Público LAE 30 · 29 · 41 |
| 20:00 | Mallorca – Cádiz (Segunda) | 63,0 · 23,0 · 14,0 | 62,2 · 22,2 · 15,6 (1,50 · 4,20 · 6,00) | **1** | 63% | Coinciden |
| 20:00 | Deportivo – Osasuna (Primera) | 37,9 · 27,7 · 34,4 | 45,2 · 29,2 · 25,6 (2,10 · 3,25 · 3,70) | **1X** | 66% | 9 puntos (causa no encontrada: el Deportivo es recién ascendido) |

**Sueltas del día** (las de más probabilidad; cuota mínima = 1/prob.):

| # | Suelta | Prob. de la mesa | Cuota mínima |
|---|---|---|---|
| 1 | Mallorca – Cádiz: 1X | 86% | 1,16 |
| 2 | Mallorca marca | 84% | 1,19 |
| 3 | Valladolid – Leganés: menos de 3,5 goles | 78% | 1,28 |
| 4 | Oviedo – Las Palmas: menos de 3,5 goles | 77% | 1,30 |
| 5 | Oviedo marca | 76% | 1,32 |

**Aviso de la mesa:**
- En 3 de los 4 partidos de liga, nuestro modelo ve **menos** a los equipos de casa que el mercado.
- Si eso fuera "valor", habría que apostar a Las Palmas, Leganés y Osasuna. **No se hace:** el mercado suele saber más, y la J18 ya mostró que el público y el mercado nos ganaron en log-loss. Esta prueba sirve justamente para medir quién tiene razón.

**Resultados (actualizado el lunes 2/11 a las 23:35):**

| Partido | Resultado | Signo | Mesa | Prob. de la mesa al signo real | Log-loss mesa | Log-loss mercado |
|---|---|---|---|---|---|---|
| Oviedo – Las Palmas | 2-3 | 2 | 1 ❌ | 24.9% | 1.390 | 1.671 |
| Valladolid – Leganés | 4-3 | 1 | 1X ✅ | 37.4% | 0.983 | 0.801 |
| Mallorca – Cádiz | 2-1 | 1 | 1 ✅ | 63.0% | 0.462 | 0.475 |
| Deportivo – Osasuna | 2-1 | 1 | 1X ✅ | 37.9% | 0.970 | 0.794 |
| Tenerife F – Athletic F | **2-0 (sin confirmar)** | 1 | 1 ✅ (si se confirma) | 56,1% | 0,578 | — |
| **Media (4 partidos confirmados)** | | | **3 de 4** | | **0.952** | **0.935** |

- El 2-0 del Tenerife F sale de un titular de Radio Marca Tenerife que no se ha podido abrir. Queda pendiente de una segunda fuente.
- **Hoy, el mercado predijo algo mejor que la mesa** (log-loss 0,935 frente a 0,952). Un día no prueba nada.

**Sueltas: 3 de 5** (se esperaban 4,0)

| Suelta | Resultado |
|---|---|
| Mallorca – Cádiz: 1X | ✅ |
| Mallorca marca | ✅ |
| Valladolid – Leganés: menos de 3,5 goles | ❌ (4-3, 7 goles) |
| Oviedo – Las Palmas: menos de 3,5 goles | ❌ (2-3, 5 goles) |
| Oviedo marca | ✅ |

**Aviso que confirma lo del Compilador:** las dos sueltas falladas son de "menos de 3,5 goles". El modelo espera menos goles que el mercado (ya se vio en la Champions). Seguimiento abierto: **sesgo de pocos goles**. Hasta medirlo con más partidos, no se proponen sueltas de "menos de X goles" cuando el modelo y el mercado se separan 5 puntos o más.

## Martes 3/11/2026 · registrado a las 08:40 de Canarias (antes del primer partido)

Son los partidos del martes de la J19, con el precio v2 de la mesa (bajas del martes incluidas). Mercado: SportRadar a las 07:32 de Canarias.

| Hora (Canarias) | Partido | Mesa 1 · X · 2 | Mercado 1 · X · 2 | Signo de la mesa | Prob. | Diferencia con el mercado |
|---|---|---|---|---|---|---|
| 20:00 | Barcelona – Aston Villa | 51,6 · 22,0 · 26,4 | 75,3 · 13,1 · 11,6 | **1** | 52% | 24 puntos (revisada; causa no encontrada) |
| 20:00 | Bodø/Glimt – Lille | 37,3 · 26,1 · 36,6 | 55,4 · 22,5 · 22,1 | **1** | 37% | 18 puntos (Noruega incompleta en los datos) |
| 20:00 | Man. United – Roma | 45,6 · 24,5 · 29,9 | 43,8 · 23,9 · 32,3 | **1** | 46% | Coinciden |
| 20:00 | Villarreal – PSG | 26,0 · 23,9 · 50,1 | 21,9 · 20,9 · 57,2 | **2** | 50% | 7 puntos (revisada) |
| 20:00 | Atlético – Bayern | 36,1 · 21,9 · 42,1 | 35,5 · 24,1 · 40,4 | **2** | 42% | Coinciden |

Aquí la prueba es clara: en P1 y P2 la mesa y el mercado se separan mucho. Si el Barça y el Bodø ganan, el mercado tenía razón; el log-loss lo dirá.

**Resultados (actualizado el miércoles 4/11):**

| Partido | Resultado | Signo | Signo de la mesa | Prob. de la mesa al signo real | Log-loss mesa | Log-loss mercado |
|---|---|---|---|---|---|---|
| Barcelona – Aston Villa | 3-0 | 1 | 1 ✅ | 51,6% | 0,662 | 0,284 |
| Bodø/Glimt – Lille | 0-0 | X | 1 ❌ | 26,1% | 1,343 | 1,492 |
| Man. United – Roma | 3-2 | 1 | 1 ✅ | 45,6% | 0,785 | 0,826 |
| Villarreal – PSG | 0-6 | 2 | 2 ✅ | 50,1% | 0,691 | 0,559 |
| Atlético – Bayern | 0-2 | 2 | 2 ✅ | 42,1% | 0,865 | 0,906 |
| **Media** | | | **4 de 5** | | **0,869** | **0,813** |

- El mercado vuelve a ganar en log-loss. La diferencia viene casi toda del Barça: le dábamos un 52%, el mercado un 75%, y ganó 3-0.
- El 0-0 del Bodø: la mesa le daba más a la X (26%) que el mercado (22,5%).

### Acumulado
| Desde | Partidos | Aciertos del signo de la mesa | Log-loss mesa | Log-loss mercado | Sueltas (reales / esperadas) |
|---|---|---|---|---|---|
| 2/11/2026 | 4 (+1 sin confirmar) | 3 de 4 | 0,952 | 0,935 | 3 / 4,0 |
| 3/11/2026 | 5 | 4 de 5 | 0,869 | 0,813 | (sueltas de la J19, pendientes) |
| **Total** | **9** | **7 de 9** | **0,906** | **0,867** | |

