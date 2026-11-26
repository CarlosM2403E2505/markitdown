# Jornadas europeas en el histórico oficial de LAE (23/11/2026)

Encargo de Carlos (23/11): qué se puede rescatar del histórico de partidos de Champions de loteriasyapuestas.es.
**Fuente (clase A):** buscador oficial de LAE (`/servicios/buscadorSorteos?game_id=LAQU`), leído con el navegador integrado. 612 jornadas de 2018 a nov. 2026 con los 15 partidos, marcadores, recaudación y escrutinio, en `datos/lae_historico.json`. Script: `herramientas/historico_europeo.py`.
**Muestra:** 91 jornadas europeas entre semana (Champions, Europa League y Conference; clasificadas a mano por fecha y partidos) y 433 de fin de semana como referencia. Se excluyen las de Liga entre semana, Copa, selecciones y Mundial de Clubes.

## 1. Signos
| | 1 | X | 2 | X por jornada |
|---|---|---|---|---|
| Jornadas europeas (91) | 46,6 % | **19,6 %** | **33,8 %** | 2,7 (mediana 3) |
| Fin de semana (433) | 44,3 % | 26,7 % | 29,0 % | 3,7 |
| Europeas desde 2024/25 (fase liga, 32) | 48 % | **17 %** | 35 % | 2,4 |

- En las europeas sale **una X menos por jornada** y más doses que el fin de semana.
- La mesa en la J24 da de media X 19,5 % y 2 39,6 % (las casas, 19,8 % y 36,8 %). La X está en línea con el histórico; no hay que tocarla. **No aplicar la X templada de Primera a la UEFA** (ya era así).

## 2. Grandes (Real Madrid, Barça, Bayern, City, Liverpool, PSG, Arsenal, Inter)
| Tipo de partido | n | 1 | X | 2 |
|---|---|---|---|---|
| Grande en casa contra no grande | 175 | **78 %** | 13 % | 9 % |
| Grande fuera contra no grande | 186 | 20 % | 17 % | **63 %** |
| Grande contra grande | 52 | 44 % | 13 % | 42 % |
| Sin grandes | 861 | 46 % | 22 % | 32 % |
| Equipo español en casa (sin otro español) | 185 | 56 % | 15 % | 29 % |
| Equipo español fuera | 193 | 35 % | 21 % | 44 % |

- Con la fase liga (desde 2024/25) los grandes ganan aún más: 83 % en casa (n=65) y 69 % fuera (n=67).
- Es una tasa base sin mirar al rival concreto. La prueba de calibración UEFA (864 partidos, `analisis/tecnicas-externas.md`) sigue mandando para los precios.

## 3. Dinero (dato informativo, no cambia signos)
| | Europeas | Fin de semana |
|---|---|---|
| Recaudación mediana | 1,11 M€ | 3,15 M€ |
| Premio de 14 (mediana, sin bote) | 20.479 € | 72.646 € |
| Premio de 13 (mediana) | 782 € | 2.805 € |
| Bote de 14 | 31 de 91 (34 %) | 139 de 433 (32 %) |
| Pleno desierto habiendo 14 | 30 de 60 (50 %) | 165 de 294 (56 %) |

- Bote según signos que no son 1: con 4-5, 0 de 12; con 7, 5 de 25; con **8 o más, 23 de 44 (52 %)**.
- En una europea se cobra unas 3,5 veces menos que un domingo con los mismos aciertos.

## 4. Pleno al 15 en europeas (91)
- Local en el Pleno: Real Madrid 14, Atlético 13, Barça 11, Sevilla 6.
- Con un grande en casa (56): 2-1 el 14 %, 1-0 11 %, M-1 11 %, M-0 9 %. El local mete 3 o más en 18 de 56 (32 %).
- El M-1 de la mesa para Atlético–Viking encaja con el histórico; no se cambia.

## 5. Reglas propuestas (solo lo medido)
1. **Control de la X en jornadas UEFA (Auditor):** la media de X de la mesa debe quedar entre el 16 % y el 23 % (histórico 19,6 %, fase liga 17 %). Si sale fuera, el Auditor lo avisa. No cambia precios.
2. **Alerta de grande (Auditor):** si la mesa da a un grande en casa contra un no grande menos del 63 % (78 % − 15), o fuera menos del 48 % (63 % − 15), y además las casas están por encima de la mesa, el partido se marca para la protección del fijo (regla de fijos protegidos). No cambia la probabilidad.
3. **Lo que no entra:** el % del público, la recaudación o los botes no cambian signos (§1.12).

## 6. J24
- X media de la mesa 19,5 %: dentro del control (regla 1).
- Grandes en casa: City 70, Madrid 68, Inter 65, Arsenal 62 (umbral 63 %, casas 68) y **PSG–Roma 55 % (casas 69 %)**. Arsenal y PSG quedan marcados para protección (regla 2). Liverpool fuera 53 % (≥ 48 %), Barça fuera 89 %.
