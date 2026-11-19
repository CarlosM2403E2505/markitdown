# J22 · Post-mortem (resultados del 17-19/11/2026)

> Fuente: quiniela15.com (resultados y % LAE, 19/11). Escrutinio oficial: **pendiente** (Loterías lo publica tras el último partido; su web bloquea los accesos automáticos).

| Nº | Partido | Resultado | Signo | Modelo | ¿Acertó el modelo? | Público (LAE) |
|---|---|---|---|---|---|---|
| 1 | Bosnia – Rumanía | 2-1 | **1** | 1 (42 %) | Sí | 54/24/22 |
| 2 | Ucrania – Georgia | 1-0 | **1** | 1 (53 %) | Sí | 59/25/16 |
| 3 | Gales – Portugal | 2-3 | **2** | 2 (63 %) | Sí | 13/15/72 |
| 4 | Hungría – Irlanda del Norte | 1-1 | **X** | 1 (44 %) | No | 53/28/19 |
| 5 | Polonia – Suecia | 1-1 | **X** | 1 (42 %) | No | 34/26/40 |
| 6 | Eire – Kosovo | 3-0 | **1** | 1 (43 %) | Sí | 59/25/16 |
| 7 | Real Madrid F – Inter F | 3-1 | **1** | 1 (80 %) | Sí | 79/12/9 |
| 8 | Häcken F – Manchester City F | 0-2 | **2** | 2 (47 %) | Sí | 9/12/79 |
| 9 | Chelsea F – PSG F | 1-0 | **1** | 1 (66 %) | Sí | 61/21/18 |
| 10 | Juventus F – OH Leuven F | 2-0 | **1** | 1 (83 %) | Sí | 83/11/6 |
| 11 | Austria Wien F – Bayern F | 0-4 | **2** | 2 (63 %) | Sí | 8/9/83 |
| 12 | Arsenal F – Lyon F | 0-2 | **2** | 2 (52 %) | Sí | 38/24/38 |
| 13 | Barcelona F – Servette F | 6-0 | **1** | 1 (99 %) | Sí | 89/6/5 |
| 14 | Benfica F – Roma F | 2-3 | **2** | 1 (63 %) | No | 47/28/25 |
| 15 | **Pleno: Dinamarca – Noruega** | **2-3** | 2-M | 1-1 (11,0 %) | **No** (el 2-M tenía un 3,4 %, puesto 14 de 16) | — |

## Cómo nos fue
- **Boleto de 18 € (24 apuestas): 2 columnas con 12 aciertos, 8 con 11 y 10 con 10.** Solo fallaron Polonia–Suecia (X, cubrimos 1 y 2) y Benfica–Roma (2-3, jugamos 1).
- **6 columnas individuales: la mejor hizo 12 aciertos** (la C4, la que llevaba la X en Hungría–Irlanda del Norte); otras dos hicieron 11.
- **Premio:** 12 y 11 aciertos son categorías con premio. El importe depende del escrutinio oficial, todavía no publicado. Fue una jornada de favoritos (la columna del público hizo 10), así que el premio por acertante será bajo.
- **Signo del modelo: 11 de 14.** Selecciones 4 de 6 (fallaron las dos X: Hungría y Polonia). **Champions femenina: 7 de 8**; el modelo nuevo, de confianza media, solo falló Benfica–Roma.
- **Empates:** salieron 2 (Hungría–Irlanda del Norte y Polonia–Suecia). El boleto de 18 € cubrió el de Hungría.
- **Pleno:** perdido. Dinamarca 2-3 Noruega (Haaland marcó). El 2-M era de los marcadores menos probables (3,4 %).
- **Frente al público:** esta vez el público predijo mejor (log-loss 0,602 frente a 0,713 de la mesa). En una jornada de favoritos claros, el público, que los carga, sale ganando; en la J21 ganó la mesa. Por eso se mide a la larga, no semana a semana.

## Lecciones
1. **El modelo femenino nuevo funcionó** (7 de 8 signos). Se mantiene para próximas jornadas con Champions femenina.
2. **Las X de selecciones** siguen siendo el punto débil: dos de los seis partidos de selección acabaron en empate.
3. **El Pleno, otra vez fallado:** van 3 de 3 verificables. Es lo esperado en un marcador exacto, pero se sigue registrando para medirlo a la larga.
4. **Premios pendientes:** añadir el escrutinio a `datos/premios.json` cuando salga.