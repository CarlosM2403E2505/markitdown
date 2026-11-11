# LA MESA DE AGENTES — ARQUITECTURA (v1.1, 27/10/2026)

> Una casa de apuestas no tiene un "pronosticador": tiene departamentos que trabajan por separado y una mesa que decide. Aquí igual. Cada agente es un especialista independiente, con su función, sus herramientas y su formato de entrega. **Todos dictaminan los 15 partidos uno a uno**, y el Director decide con reglas escritas, no a ojo.
> Base de conocimiento de todos: el prompt maestro v5 (`prompt-maestro-quiniela.md`) y la trayectoria J13–J18 de este proyecto. No se inventa nada nuevo: cada agente aplica lo que ya está medido.

---

## 1. El organigrama

| Agente | Equivale en una casa a… | Función | Herramientas | Entrega por partido | Veto |
|---|---|---|---|---|---|
| **Investigador** ("el Perplexity de la casa") | Departamento de *trading intelligence* | Saca de internet hechos fechados: Copa y Europa entre semana, bajas, porteros, alineaciones, contexto. Clasifica A/B/C/D | Búsqueda web, lectura de páginas | Novedades A–D, efecto propuesto, dictamen | No |
| **Matemático / Quant** | *Quant team* | Desafía el precio oficial con modelos alternativos (Elo, Poisson solo con datos españoles, tasas base); valida fuera de muestra (log-loss, Brier) y propone un ensemble | Python, datos del proyecto | Prob. oficial frente a alternativas, discrepancia, dictamen | Sí, si un modelo alternativo gana claramente fuera de muestra |
| **Físico** (incertidumbre) | *Risk modelling* | Mide la incertidumbre, no el favorito: entropía, robustez del signo ante perturbaciones, correlación entre partidos (jornadas "de empates") y Monte Carlo del boleto | Python, histórico 1972–2026 | Entropía, robustez (%), frágil sí/no, dictamen | No (alimenta al Risk Analyst) |
| **Compilador de cuotas** | *Odds compiler* | Convierte probabilidades en cuotas justas y de casa; compara con el mercado y con el % del público; encuentra el valor | Búsqueda web, Python | Cuota justa, mercado sin margen, % público, valor, dictamen | No (solo desempata) |
| **Trader deportivo** | *Trader de la casa* | Vigila cómo se mueve el mercado durante la semana (apertura frente a actual), qué noticia lo explica y qué movimientos no tienen explicación (alerta: el mercado sabe algo). Recomienda cuándo sellar | Búsqueda web, comparadores | Movimiento, ¿explicado?, mantener o revisar | No |
| **Risk Manager** | *Head of risk* | Mapa de exposición (qué partido hunde más el boleto), escenarios de estrés, decisión entre A y B según el objetivo, gestión de banca (presupuesto fijo, nunca subir para recuperar, Kelly solo con EV positivo) y correlaciones peligrosas | Python, reglas del v5 | Contribución al riesgo, alerta, cobertura mínima | **Sí** |
| **Científico de datos** | *Data engineering* | Dueño de la calidad de los datos: completa huecos (por ejemplo, la Segunda 2025/26), audita nombres, duplicados y huecos de fechas, y mide cuánto mejora el modelo con los datos arreglados | Git, búsqueda web, Python | Calidad por equipo, impacto en log-loss, nuevas probabilidades | Sí, si los datos de un partido no son fiables |
| **Risk Analyst** (reglas) | *Risk manager* | Clasifica el riesgo (bajo/moderado/alto/muy alto con criterios fijos); nada <65% es fijo; fallos esperados | Reglas del v5 | Riesgo y cobertura mínima | **Sí** |
| **Red Team** | *Trader contrario* | "¿Qué columna querría la casa que jugase?" Mejor argumento contra cada signo | Reglas del v5 + informe del compilador | Argumento contrario, cambio sí/no | **Sí** (con la regla de los 10 puntos) |
| **Pleno Specialist** | *Correct score trader* | Pleno principal, conservador y de varianza; P(Pleno) real | Matriz de marcadores | 3 marcadores con % | No |
| **Portfolio Manager** | *Head of trading* | Boleto óptimo exacto dentro del presupuesto (A y B), sueltas | `reducida7.py`, `compare_systems.py` | Boleto, P(14), P(≥10) | No |
| **Director** | *Director de la mesa* | Orquesta, resuelve contradicciones con las reglas de la sección 3 y firma | Todo | Decisión final por partido | **Sí** |
| **Auditor** (independiente, sin ver el proceso) | *Compliance / auditoría* | Revisa cuentas, fuentes, coherencia, presupuesto y que no se haya inventado nada | Lectura de entregas, Python | ✅/❌ por comprobación | **Sí** |

---

## 2. El flujo de una jornada

```
           EXPEDIENTE COMÚN (partidos, modelo, reglas, trayectoria)
                                 │
   ┌───────────┬───────────┬───────────┼───────────┬───────────┬───────────┐
   ▼           ▼           ▼           ▼           ▼           ▼           ▼
INVESTIG.  MATEMÁTICO   FÍSICO    COMPILADOR   TRADER    CIENTÍFICO   RISK
(hechos)   (quant)     (incert.)  (cuotas)    (mercado)  (datos)      MANAGER
   └───────────┴───────────┴───────────┼───────────┴───────────┴───────────┘
                                       │      ← en paralelo, sin verse entre sí
                                 ▼                           │
                 DIRECTOR + Risk + Red Team + Pleno + Portfolio
                  (consejo: voto de cada agente por partido)
                                 │
                                 ▼
                     AUDITOR INDEPENDIENTE (veto)
                                 │
                                 ▼
          Boleto + 14 signos + Pleno + 5 sueltas → proyecto + panel
```

Los especialistas trabajan **en paralelo y sin verse**, como departamentos distintos. Así sus errores no se copian entre ellos. Cada uno entrega una tabla de 15 filas con su **dictamen**.

---

## 3. Cómo decide el Director (reglas escritas)

1. **Precio base:** el modelo oficial.
   - Solo se mezcla con el del Matemático si este demuestra un log-loss mejor fuera de muestra.
   - El peso es proporcional a la mejora, con un máximo del 50%.
2. **Hechos:** solo los A y B del Investigador mueven el precio, con los topes del v5 (±5%; hasta 10% por baja del portero o del delantero centro; tabla de cansancio por Copa).
3. **Dobles:** el Portfolio optimiza P(14) con el precio final.
   - Si el Físico marca un partido como **frágil** (robustez del signo <70%), ese partido tiene preferencia para el doble cuando la P(14) cae menos de un 5%.
4. **Valor:** el Compilador solo desempata.
   - Se elige el boleto de más valor entre los que conservan al menos el 90% de la P(14) máxima.
   - Nunca se cambia un signo con más de 10 puntos de ventaja.
5. **Vetos:**
   - Risk Analyst: nada <65% como fijo sin ⚠️.
   - Red Team: argumento contrario con evidencia A/B.
   - Auditor: cualquier error de cuentas o dato sin fuente → se corrige antes de publicar.
6. **Desacuerdo fuerte:** si 3 o más agentes dictaminan un signo distinto al del modelo en un partido, ese partido entra obligatoriamente entre los 7 dobles (sustituye al doble que menos P(14) aporte) y se anota como "decisión de la mesa".

---

## 4. Calendario y coste

| Momento | Quién trabaja | Coste |
|---|---|---|
| Primera pasada (miércoles o jueves) | Los 7 especialistas + Director + Auditor | Alto (una vez por jornada) |
| Revisión final (viernes, programada) | Investigador (Copa, bajas, %) + Compilador + Trader (movimientos) + Risk Manager + Director | Medio |
| Post-mortem (lunes) | Matemático (log-loss, Brier) + Científico de datos (actualizar datos) + Director | Bajo |

Para no gastar de más: el Matemático y el Físico solo se relanzan si cambian las probabilidades más de 3 puntos en algún partido.

---

## 5. Lo que la mesa NO hace (honestidad)

- No ve el futuro. El "físico cuántico" es una forma de hablar: en el fútbol no hay efectos cuánticos aprovechables. Lo que sí sirve de la física es la estadística: entropía, Monte Carlo, correlaciones.
- Ningún agente puede convertir un 40% en un 90%. Lo que hace la mesa es poner mejor los dobles, no fallar por errores de proceso y repartir el premio con menos gente cuando acertamos.
- Perplexity: el conector de Perplexity de este espacio solo importa paneles, no busca. El Investigador usa la búsqueda web propia de Claude, con las mismas fuentes.
