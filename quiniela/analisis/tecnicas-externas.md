# Qué hacen las IA, los tipsters y las casas que la mesa no hace (22/11/2026)

Encargo de Carlos (22/11, 2:58): «Busca datos interesantes de IA o casas de apuestas que estén haciendo que nosotros no». Fuentes leídas (sin Marca, Sport, Mundo Deportivo ni L'Équipe), clase entre paréntesis.

## 1. Lo que hacen fuera y la mesa no

| Técnica | Quién la usa | ¿La mesa la tiene? | Dato |
|---|---|---|---|
| **Cuota de cierre (Pinnacle sin margen) como referencia** | Casas profesionales, tipsters serios, todos los proyectos de modelos serios | Solo como aviso (R3, `--mercado 0.08`); no entra en probabilidades (§1.3 y R5) | 45.629 partidos fuera de muestra: mercado log-loss **0,998**, mejor red neuronal 1,013, modelos de ratings 1,018 ([tracsj/match-predictor](https://github.com/tracsj/match-predictor), B). La mesa da 1,014 en Primera+Segunda (`ventaja-de-la-mesa.md`): está al nivel de un buen modelo, por debajo del mercado |
| **Valor esperado contra el público (juego de apuestas mutuas)** | Ochenta Veinte, V. Rodríguez-Doncel (UPM) | No: §1.12, el % LAE solo se informa | Elegir columnas con mayor premio esperado = probabilidad × premio / acertantes, con el % LAE ([Ochenta Veinte](https://ochentaveinte.substack.com/p/hackeando-la-quiniela), C; [El Español, 27/1/2026](https://www.elespanol.com/ciencia/20260127/victor-ingeniero-ganar-quiniela-apuestas-rentables-esperanza-beneficio-mayor/1003744104972_0.html), B). Ojo: en 51 semanas jugaron 153 € y cobraron 61,88 € |
| **Superordenador Opta / webs de IA (PrediBall, etc.)** | Medios, casas | No | Útil como control. PrediBall J24: Real Madrid–PSV 82 %, Man City–Nápoles 78 %, Atlético–Viking 88 % (mesa 69, 68, 73) ([PrediBall](https://www.prediball.com/champions-league/matchday-5/), D: no dice cómo calcula) |
| **xG o tiros a puerta en las fuerzas** | Opta, FiveThirtyEight (SPI), casi todas las IA | No: el modelo usa solo goles | El espejo de raw.githubusercontent.com (datasets/football-datasets) trae tiros y tiros a puerta de LaLiga 2024-26 (comprobado). Probable mejora en Primera; no aplica a UEFA |
| **Log-loss como métrica principal** | penaltyblog (M. Eastwood) | Sí | RPS puede ordenar mal dos pronósticos; log-loss es la buena ([pena.lt](https://pena.lt/y/2025/05/01/better-metrics-for-football-forecasts-moving-beyond-the-ranked-probability-score/), B). La mesa ya va bien |
| **CLV (valor frente a la cuota de cierre) para las apuestas** | Apostadores profesionales | No: el bank mide ROI, no CLV | Con 10-20 apuestas el ROI es ruido; el CLV dice antes si la mesa tiene ventaja |
| **Alineaciones confirmadas** | Casas (mueven la cuota 1 h antes) | Parcial: Flashscore por el navegador de Carlos | El definitivo sale 2 h 15 antes: no llega a los onces oficiales |

## 2. Prueba hecha hoy: ¿hay que afilar a los favoritos UEFA como hacen las webs de IA?

`modelo/calibracion_uefa.py`: walk-forward mensual, **864 partidos de Champions, Europa League y Conference** (sep. 2024 – nov. 2026), fuera de muestra. Elegir con 2024-25 y 2025-26 (702), validar con 2026-27 (162).

| Favorito según la mesa | Partidos | Mesa da | Gana de verdad |
|---|---|---|---|
| 33-45 % | 209 | 41,6 % | 43,1 % |
| 45-55 % | 238 | 49,9 % | 52,9 % |
| 55-66 % | 193 | 60,0 % | 58,0 % |
| **66-75 %** | 101 | 70,5 % | **56,4 %** |
| **75 %+** | 123 | 83,3 % | **76,4 %** |

- **No.** En Europa la mesa ya va algo pasada con los grandes favoritos, no corta. Las webs que dan 82-88 % a Madrid, City o Atlético exageran todavía más: seguirlas sería un error.
- Empates UEFA: salen 18,3 %, la mesa da 20,1 %. Diferencia dentro del ruido (±2,6).
- Temperatura y factor de X: el mejor al elegir (X 0,90, T 1,00) y el mejor al validar (T 1,15) se contradicen y las diferencias son de milésimas. **Se mantiene T 1,05 y X 1,0 en UEFA.** No cambia el boleto de la J24.

## 3. Propuestas (la mesa decide; nada choca con las reglas de Carlos)

**Para la J24 (antes del martes 18:45):**
1. **Control externo en el informe**: tabla mesa · casas (sin margen) · Opta · PrediBall en cada partido. Si la mesa se separa más de 8 puntos de las casas, ya actúa el aviso de R3. Solo informa; no mueve probabilidades (§1.3).
2. **Prudencia con los fijos del 66-75 %** (Arsenal, City, Madrid, Inter, PSG): en Europa ganan el 56 %, no el 70 %. R3 ya los deja sin tope desde el 65 %. El Auditor lo vigila en la J24 y, si vuelven a fallar, se estudia bajar el umbral sin tope en UEFA.
3. **CLV en el bank**: anotar la cuota de bet365 al apostar y la de cierre; `apuestas_valor.py` puede calcularlo. No cambia ninguna apuesta.

**Para las siguientes (Liga):**
4. **Tiros a puerta en el modelo de Primera** (prueba walk-forward como las anteriores; datos ya accesibles).
5. **Cuotas de cierre históricas** (football-data.co.uk, bloqueado desde el contenedor: abrir el dominio en Network access) para medir de verdad mesa frente a mercado en 1.800 partidos. Si el mercado gana, Carlos decide si se mezcla (hoy §1.3 lo prohíbe).
6. **Valor esperado contra el público**: solo como dato informativo (premio esperado de cada columna con el % LAE), porque §1.12 lo deja fuera de las decisiones.

## Informe del Auditor
- Fuentes citadas con URL, fecha y clase; ninguna excluida. ✅
- 864 partidos UEFA, todos fuera de muestra (reajuste mensual), sin previas. Datos en `datos/calibracion_uefa.json`. ✅
- Ninguna probabilidad, signo ni columna de la J24 cambia. ✅
- PrediBall es clase D (no explica su método): solo control. ✅
