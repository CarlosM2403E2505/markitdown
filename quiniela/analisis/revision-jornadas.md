# Revisión de todas las jornadas jugadas (24/11/2026)

Petición de Carlos: no solo la J23, revisar todas para aprender. Script: `modelo/revision_jornadas.py`.
Datos: J19-J23 completas en `jornadas/jNN/jNN.json` (70 partidos con probabilidad de la mesa y resultado; 25 con cuota de las casas). J13-J18 solo tienen resúmenes en `importado/` (sin probabilidades completas): se usan para la mejor columna.

## 1. Jornada a jornada

| Jornada | Mejor columna | Favorito de la mesa acertó (esperado) | Mesa frente a casas/público (log-loss, menos es mejor) |
|---|---|---|---|
| J14 | 11 | — | — |
| J16 | 9 | — | — |
| J18 | 9 | 7 de 13 (6,6) | mesa 0,897 · público 0,786 |
| J19 (Champions) | 11 | 10 de 14 (7,1) | mesa 0,816 · casas 0,729 (11 partidos) |
| J20 | 7 | 6 de 14 (7,0) | — |
| J21 | 9 | 7 de 14 (6,9) | mesa 1,006 · público 1,011 |
| J22 (selecciones) | 12 | 11 de 14 (8,4) | — |
| J23 | 11 | 9 de 14 (8,2) | mesa 0,825 · casas 0,777 (14 partidos) |

Ninguna jornada ha llegado a 13. Media de la mejor columna: 9,9.

## 2. Qué se aprende (medido)

1. **La mesa no infla a sus favoritos; se queda corta.** En 70 partidos su favorito ganó 43 veces cuando esperaba 37,6. Los fijos acertaron 29 de 39 (esperados 23,3). Por tramos: favorito al 45-55 % ganó el 64 %, al 55-65 % el 72 %. Los fallos no vienen de probabilidades optimistas.
2. **Lo que tumba el boleto es el signo que no está en ninguna columna.** 14 partidos con el resultado en 0 columnas (2-4 por jornada). **8 de esos 14 fueron X.** De las 13 X que salieron, solo 2 estaban en alguna columna. Las columnas llevaban de 0,2 a 1,3 X cuando la mesa esperaba unas 3 por jornada. (La X no salió más de lo previsto: 13 frente a 16 esperadas. El problema es de cobertura, no de precio.)
3. **Las casas pronostican mejor que la mesa.** En los 25 partidos con cuota: casas 0,756 y mesa 0,821. Comprobado en grande: 1.372 partidos de Primera y Segunda 2024-26 con la probabilidad fuera de muestra de la mesa (`datos/auditoria_ventaja.json`) y la cuota de football-data (clase B): **casas 0,966 y mesa 1,014**. Diferencia −0,047 por partido (z ≈ 7,5), igual en 2024-25 y en 2025-26. Cualquier mezcla mesa-casas queda peor que las casas solas.
4. **Cuando la mesa da a su favorito 8 puntos más que las casas, aciertan las casas.** 268 casos: la mesa daba un 58,5 %, las casas un 42,9 %, y ganó el 50 %. Es lo que pasó en la J23 con Tenerife F–Madrid CFF (63 frente a 52, salió 2) y Tenerife–Mallorca (50 frente a 43, salió X).
5. Por competición (pocos partidos, solo vigilancia): Segunda (log-loss 1,07, favorito 6 de 15) y Liga F (1,01) son lo más flojo; Champions (9 de 11) y Champions F (7 de 8), lo mejor.

## 3. Regla nueva (R5b, en `herramientas/reglas_mesa.py`)

**Si el partido trae cuota de las casas (1X2 sin margen, campo `mercado`), el boleto se calcula con esa probabilidad.** Sin cuota (Liga F, Champions F) y en el Pleno manda la mesa. Los topes de diversidad (R3, R3b, mala forma) se siguen calculando también con la P de la mesa, así que la cobertura nunca baja. `--solo-mesa` vuelve al cálculo anterior. No sube ninguna probabilidad: usa la que mejor acierta medida fuera de muestra.

Sustituye, solo cuando hay cuota, a R5 («solo las de la mesa») y a la instrucción §1.3 de 12/11, en aplicación de la orden del 22/11: «todo dato positivo y medido lo ajusta la mesa».

**J24 (aplicada antes del definitivo):** con las cuotas bet365 del 24/11, el boleto anterior tenía P(≥13) 3,92 % medido con las casas; el nuevo, 4,54 % (mismos 18 €, 24 columnas que se sellan como 3 boletos de 8 sencillas). Cambia sobre todo Shakhtar–Fenerbahçe (mesa 25/23/53, casas 37/27/36), Sporting–United, PSG–Roma y Real Madrid–PSV. Pleno M-1 sin cambios.

No se propone ninguna regla más: la X y los fijos ya los cubren R3/R3b y no hay datos que pidan otra cosa.
