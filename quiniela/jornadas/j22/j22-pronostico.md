# Jornada 22 · 17-19/11/2026 · selecciones (repesca Mundial) + Champions femenina

> Jornada atípica: 6 partidos de selecciones + Pleno (modelo validado) y 8 de UEFA Women's Champions
> League (**modelo nuevo, confianza media**: `modelo/champions_f_modelo.py`, datos de Wikipedia,
> 90 partidos de 2025-26 y 2026-27). Cierre: martes 17/11 a las 20:45.

## Precios de los 15

| Nº | Partido | Competición | 1 | X | 2 | Signo | Confianza |
|---|---|---|---|---|---|---|---|
| 1 | Bosnia – Rumanía | Selección | 41,6 | 27,1 | 31,2 | 1 | Alta |
| 2 | Ucrania – Georgia | Selección | 53,1 | 24,4 | 22,4 | 1 | Alta |
| 3 | Gales – Portugal | Selección | 14,4 | 22,3 | **63,3** | 2 | Alta |
| 4 | Hungría – Irlanda del Norte | Selección | 44,5 | 30,7 | 24,8 | 1 | Alta |
| 5 | Polonia – Suecia | Selección | 42,1 | 23,4 | 34,5 | 1 | Alta |
| 6 | Eire – Kosovo | Selección | 43,2 | 29,8 | 27,0 | 1 | Alta |
| 7 | Real Madrid F – Inter F | Champions F | **80,0** | 12,9 | 7,2 | 1 | Media |
| 8 | Häcken F – Manchester City F | Champions F | 25,4 | 27,6 | **47,0** | 2 | Media |
| 9 | Chelsea F – PSG F | Champions F | **65,6** | 22,9 | 11,5 | 1 | Media |
| 10 | Juventus F – OH Leuven F | Champions F | **83,2** | 10,8 | 6,0 | 1 | Media |
| 11 | Austria Wien F – Bayern F | Champions F | 18,6 | 18,4 | **62,9** | 2 | Media |
| 12 | Arsenal F – Lyon F | Champions F | 23,4 | 24,5 | **52,1** | 2 | Media |
| 13 | Barcelona F – Servette F | Champions F | **99,3** | 0,5 | 0,2 | 1 | Media (lock) |
| 14 | Benfica F – Roma F | Champions F | **63,3** | 20,8 | 15,9 | 1 | Media |
| 15 | **Pleno: Dinamarca – Noruega** | Selección | 48,9 | 23,7 | 27,5 | **1-1** | Alta |

- **Fuerza del modelo femenino** (coherente con lo esperado): Lyon, Barcelona, Chelsea, Arsenal arriba; St. Pölten, OH Leuven, Servette, Roma abajo.
- El 99,3 % del Barcelona es el Poisson puro; en un partido suelto nadie gana tan seguro, pero la decisión (1 fijo) no cambia.

## Por qué esta jornada es favorable
- **Fallos esperados con los 14 signos: 5,6** (en una jornada de Segunda son 7+). Los partidos femeninos están muy desnivelados.
- Con un boleto de 18 € la P(14) es **1 entre 167** (en la J21 era 1 entre 1.224). P(≥13) 4,6 %.
- **Aviso honesto:** 8 de los 14 son de confianza media (modelo nuevo). Las repescas de selección también tienen más varianza (partido único, mucha presión).

## Empates (decide la mesa, sin regla fija)
- X esperadas: 2,96. P(ninguna X): 3,4 %.
- La mesa cubre la X donde más probable es: **Bosnia–Rumanía** (triple), **Hungría–Irlanda del Norte** y **Eire–Kosovo** (dobles 1X). Son las tres X más altas (27–31 %).

## Boleto recomendado · un boleto, 24 apuestas, 18 €

| Nº | Partido | Marca |
|---|---|---|
| 1 | Bosnia – Rumanía | **1 X 2** |
| 2 | Ucrania – Georgia | 1 |
| 3 | Gales – Portugal | 2 |
| 4 | Hungría – Irlanda del Norte | **1 X** |
| 5 | Polonia – Suecia | **1 2** |
| 6 | Eire – Kosovo | **1 X** |
| 7 | Real Madrid F – Inter F | 1 |
| 8 | Häcken F – Manchester City F | 2 |
| 9 | Chelsea F – PSG F | 1 |
| 10 | Juventus F – OH Leuven F | 1 |
| 11 | Austria Wien F – Bayern F | 2 |
| 12 | Arsenal F – Lyon F | 2 |
| 13 | Barcelona F – Servette F | 1 |
| 14 | Benfica F – Roma F | 1 |
| 15 | Pleno: Dinamarca – Noruega | 1-1 |

- **P(14) 1 entre 167 · P(≥13) 4,6 % · P(≥12) 16,5 % · P(≥10) 62,1 %.**
- Cubre la X en 3 partidos (Bosnia, Hungría, Eire).

## Informe del Auditor
- 24 apuestas, 18 € ≤ 20 €. ✅
- Selecciones (7 partidos): NatPoisson validado (log-loss 0,795 fuera de muestra). ✅
- Champions femenina (8 partidos): modelo nuevo, **confianza media**; fuerzas revisadas a ojo y coherentes. ⚠️ Anotado.
- Pleno 1-1 (más probable); el Pleno oficial del boleto se confirma al sellar. ⚠️
- 5 sueltas = los 5 signos más probables.
