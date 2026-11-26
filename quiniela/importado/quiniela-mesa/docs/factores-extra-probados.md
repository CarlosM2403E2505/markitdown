# FACTORES EXTRA PROBADOS: ENFRENTAMIENTOS DIRECTOS, ENTRENADORES Y ÁRBITROS

24/10/2026. Pregunta: ¿mejoran el pronóstico más allá de lo que el modelo ya sabe? Método: siempre fuera de muestra (el modelo solo ve el pasado de cada partido que predice).

## 1. Enfrentamientos directos (H2H) — NO aportan

Variable probada: cuánto rindió un equipo contra ese rival concreto por encima de lo que esperaba el modelo, encogido según el número de duelos previos.

| Peso del H2H | Log-loss (sep 25–ene 26, 2.626 partidos) | Log-loss (feb–oct 26, 1.948 partidos) |
|---|---|---|
| 0 (sin H2H) | 1.0332 | 1.0194 |
| 0.05 | 1.0330 | 1.0193 |
| 0.10 | 1.0330 | 1.0195 |
| 0.20 | 1.0335 | 1.0205 |
| 0.30 | 1.0345 | 1.0225 |

Mejora máxima: 0.0002 (despreciable). Con peso normal empeora. **El H2H ya está dentro de la fuerza actual de los equipos; lo que queda es ruido.** Se usa solo como aviso cualitativo.

"Entrenador contra ese rival" es un subconjunto aún más pequeño del H2H (3–6 partidos): misma conclusión, con más ruido.

## 2. Cambio de entrenador — NO hay efecto propio

49 ceses a mitad de temporada (Segunda 2024/25, Primera, Premier, Serie A, Bundesliga y Ligue 1 2025/26–2026/27). Para cada uno se ajustó el modelo con los datos hasta el día del cese y se midieron los puntos reales frente a los esperados.

| | Puntos por partido sobre lo esperado |
|---|---|
| 5 partidos ANTES del cese | **−0.60** (la mala racha que provoca el despido) |
| 5 partidos DESPUÉS del cese | **+0.03** (intervalo 95%: −0.12 a +0.19) |

La "reacción del entrenador nuevo" es **regresión a la media**: el equipo vuelve a su nivel real, que el modelo ya conocía. No hay que ajustar nada por un cambio de entrenador. Ejemplos de esta temporada: Valencia (Corberán cesado el 13/9; −0.96 antes, −0.08 después).

## 3. Árbitros — no medibles para el 1X2

- No hay fuente accesible con el árbitro de cada partido de varias temporadas. Solo 2026/27 (88 partidos, 20 árbitros, 3–5 partidos por árbitro).
- Aunque la hubiera: con ~20 partidos por árbitro y temporada, el error típico del porcentaje de victorias locales de un árbitro es de **±11 puntos**. Un sesgo arbitral real (pocos puntos) es indetectable.
- **Sí sirven para mercados de tarjetas y penaltis**, no para el 1X2. Ejemplo 2026/27: Martínez Munuera (Clásico) 3.0 amarillas y 0.6 penaltis por partido; Quintero González 1.0 rojas por partido.

## Conclusión

Los factores que mueven de verdad el pronóstico son los que ya están en el modelo: fuerza actual por goles, ventaja de campo, empates por competición, bajas y cansancio. H2H, entrenadores y árbitros quedan como **avisos**, no como números. Esto coincide con cómo trabajan las casas de apuestas: el precio sale del rating del equipo y las bajas, no del historial.
