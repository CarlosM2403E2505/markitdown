# J21 · Post-mortem (resultados oficiales del 15/11/2026)

| Nº | Partido | Resultado | Signo | Modelo | ¿Acertó el modelo? |
|---|---|---|---|---|---|
| 1 | Valladolid – Castellón | 0-1 | 2 | 2 (49 %) | Sí |
| 2 | Real Sociedad B – Sporting | 2-2 | **X** | 1 (39 %) | No |
| 3 | Almería – Andorra | 2-1 | 1 | 1 (61 %) | Sí |
| 4 | Mallorca – Córdoba | 3-3 | **X** | 1 (64 %) | No |
| 5 | Oviedo – Girona | 1-2 | 2 | 1 (37 %) | No (cubierto con doble) |
| 6 | Tenerife – Ceuta | 2-0 | 1 | 1 (49 %) | Sí |
| 7 | Granada – Las Palmas | 1-0 | 1 | 1 (43 %) | Sí |
| 8 | Eibar – Cádiz | 1-1 | **X** | 1 (54 %) | No |
| 9 | Eldense – Sabadell | 2-0 | 1 | 2 (36 %) | No (cubierto con triple) |
| 10 | Bélgica – Italia | 4-1 | 1 | 1 (50 %) | Sí |
| 11 | Alavés F – Eibar F | 2-1 | 1 | 1 (49 %) | Sí |
| 12 | Real Sociedad F – Athletic F | 1-4 | 2 | 1 (58 %) | No |
| 13 | Sevilla F – Atlético F | 1-2 | 2 | 2 (62 %) | Sí |
| 14 | Valencia F – Granada F | 0-0 | **X** | 2 (44 %) | No |
| 15 | **Pleno: España – Inglaterra** | **2-3** | 2 | 1-0 | **No** (España perdió) |

## Lo que pasó
- **Mejor columna: 9 aciertos** (boleto 1). Sin premio (hacían falta 10).
- **4 empates** (partidos 2, 4, 8, 14). **No cubrimos ninguno.** Es exactamente el patrón que preocupaba.
- El **Pleno se perdió**: España cayó 2-3 con Inglaterra. El modelo de selecciones daba a España un 53 %: una derrota entra dentro de lo posible, pero dolió.
- **Acierto de signo del modelo: 7 de 14 (50 %)**, en línea con la ventaja medida (`analisis/ventaja-de-la-mesa.md`).
- **Aun así batimos al público:** log-loss de la mesa 1,006 frente a 1,011 del % LAE. Mala semana, pero no por peor método que el público.

## Lecciones
1. Los empates: salieron 4 (sobre 3,4 esperados) y ninguno estaba cubierto. Con un presupuesto pequeño y un solo boleto, cubrir más de 1-2 X baja mucho la P(14). No hay arreglo gratis; se decide jornada a jornada (confirmado el 14/11).
2. El Pleno es de un solo partido: su varianza es irreducible. El modelo acierta a la larga, no cada semana.
3. **Premio oficial J21: pendiente** de añadir a `datos/premios.json`.
