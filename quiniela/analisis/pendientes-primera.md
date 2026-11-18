# Pruebas pendientes de Primera (18/11/2026)

`modelo/pendientes_primera.py`: walk-forward mensual de Primera 2022-26. Se elige con 2022-24 (346 partidos) y se valida con 2025-26 (497 partidos), sobre el modelo actual (empates ×1,08, campo +0,07, T = 1,15).

| Prueba | Validación | Prueba | Decisión |
|---|---|---|---|
| Modelo actual | 0,9930 | 0,9600 | — |
| (a) Empates ×1,10 en igualados | 0,9969 | 0,9591 | ❌ Empeora la validación |
| (a) Empates ×1,20 en igualados | 1,0010 | 0,9588 | ❌ Empeora la validación |
| (b) EURO_F 1,04 | 0,9910 | 0,9582 | Mejora |
| (b) EURO_F 1,08 | 0,9896 | 0,9569 | Mejora |
| **(b) EURO_F 1,12** | **0,9887** | **0,9560** | ✅ **Aplicado** |

- **(a) Se rechaza.** Elegido con la validación, subir el empate en partidos igualados empeora. La pequeña mejora en la prueba no basta: se elige con la validación, no con la prueba.
- **(b) Se aplica EURO_F = 1,12.** Cuando en Primera solo uno de los dos equipos ha jugado competición UEFA en los últimos 120 días, sus goles esperados se multiplican por 1,12. Mejora la validación y la prueba (351 de 843 partidos tienen un solo equipo europeo). En `modelo/j23_run.py`.
- **Efecto en la J23:** se aplica a la Real Sociedad (en Santander) y al Betis (en el Pleno). En Real Madrid–Celta, Barcelona–Villarreal y Getafe–Atlético juegan Europa los dos, así que no cambia nada.
