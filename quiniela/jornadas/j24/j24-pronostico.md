# J24 · Champions (J5) + Europa League · 24-26/11/2026

## v1 · primer repaso · sáb 21/11/2026 22:30 (PROVISIONAL)

- Lista: quinielafutbol.info (21/11, clase C); los 13 de Champions coinciden en día y orden con prediball.com y dratings.com. Los 2 de Europa League, sin confirmar. Falta la lista oficial de SELAE.
- Primer partido: mar 24/11 21:00 → **definitivo mar 24/11 18:45**.
- Modelo: `modelo/j24_run.py` (Poisson multi-liga, UEFA empates ×1,0, T=1,05) con `datos/euro_j23.json` (hasta 15/11). **Huecos**: ligas extranjeras paradas ~1/11 (Eredivisie y Chequia 20/09); sin liga eslovaca, azerí ni ucraniana 2026/27 (Slovan, Sabah y Shakhtar solo con partidos UEFA). Este hilo no tiene acceso de red a las webs de §6 (entorno Default).

### Precios (mesa) y control (DRatings, modelo ajeno: solo control)

| # | Partido | Día | Mesa 1 / X / 2 | DRatings 1 / X / 2 | Signo |
|---|---|---|---|---|---|
| 1 | Arsenal – Dortmund | mar 24, 21:00 | 62 / 21 / 17 | 68 / 18 / 14 | 1 |
| 2 | Feyenoord – Oporto | mar 24, 21:00 | 32 / 23 / 45 | 35 / 28 / 37 | 2 |
| 3 | Man. City – Nápoles | mar 24, 21:00 | 68 / 18 / 14 | 65 / 20 / 15 | 1 |
| 4 | Real Madrid – PSV | mar 24, 21:00 | 69 / 15 / 16 | 74 / 16 / 10 | 1 |
| 5 | Slovan Bratislava – Betis | mar 24, 21:00 | 14 / 16 / 70 | — | 2 |
| 6 | Sabah – Barcelona | mié 25, 18:45 | 3 / 6 / 91 | — | 2 |
| 7 | Slavia Praga – Villarreal | mié 25, 18:45 | 31 / 22 / 47 | 25 / 25 / 49 | 2 |
| 8 | Brujas – Liverpool | mié 25, 21:00 | 28 / 21 / 52 | 15 / 20 / 64 | 2 |
| 9 | Inter – Stuttgart | mié 25, 21:00 | 65 / 18 / 18 | 74 / 16 / 10 | 1 |
| 10 | PSG – Roma | mié 25, 21:00 | 60 / 20 / 20 | 59 / 22 / 19 | 1 |
| 11 | Shakhtar – Fenerbahçe | mié 25, 21:00 | 31 / 23 / 46 | 22 / 24 / 54 | 2 |
| 12 | Sporting CP – Man. United | mié 25, 21:00 | 44 / 23 / 33 | 37 / 28 / 35 | 1 |
| 13 | Celta – Bournemouth | jue 26, 18:45 | 26 / 24 / 50 | — | 2 |
| 14 | Crystal Palace – Real Sociedad | jue 26, 21:00 | 53 / 22 / 25 | — | 1 |

**Pleno: Atlético – Viking** · mesa 73/14/12 · xG 2.84-1.18 · marcador más probable **M-1**

| Marcador | P |
|---|---|
| M-1 | 17.0 % |
| M-0 | 14.7 % |
| M-2 | 10.0 % |
| 2-1 | 8.6 % |
| 2-0 | 7.2 % |
| 1-1 | 7.1 % |

### Boleto (formato habitual: 18 € + 8 sencillas)

- 18 €: la herramienta (`boleto_unico.py`, objetivo P(≥13)) elige **24 columnas sencillas más probables** (P(14) 1/185, P(≥13) 3.86 %).
- 8 sencillas complementarias (las más probables fuera del boleto): 11112221112121, 11112222112111, 1211222211X221, 11112222112X21, 11112222111221, 121122221122X1, 1111222211X121, 12112221111121.
- Conjunto: 32 columnas, 24.00 € · P(14) 1/151 · P(≥13) 4.64 % · P(≥12) 15.8 % · P(≥10) 58.7 %.
- Empates: 2.71 X esperadas, P(ninguna X) 4.8 %, X cubiertas en el boleto: 0. En Europa la X sale menos de lo que da el modelo (ver abajo).

### Sueltas

| Partido | Apuesta | P |
|---|---|---|
| Sabah – Barcelona | Marca el Barcelona | 98.2 % |
| Real Madrid – PSV | Marca el Real Madrid | 94.5 % |
| Atlético – Viking | Marca el Atlético | 94.1 % |
| Slovan Bratislava – Betis | Marca el Betis | 91.8 % |
| Inter – Stuttgart | Marca el Inter | 91.5 % |

### ¿Se fía la mesa demasiado de los favoritos? (queja de Carlos tras Rayo 0-1 Valencia)

- **J23, Primera:** sí. Rayo 54 % en la mesa frente a 49 % en las casas: sobre T=1,15 se apilaron EURO_F ×1,12 (el Rayo juega la Conference) y bajas del Valencia ×1,03. Mismo patrón en Alavés (+16 sobre las casas) y Osasuna (+12), con la X por debajo. Pendiente: revalidar EURO_F y T=1,15 con los resultados de la J23 antes de la J25.
- **Europa (J24):** no. Prueba fuera de muestra (walk-forward mensual, 347 partidos UEFA 2025-26 y 2026-27):

| Favorito según la mesa | Partidos | Daba | Ganó |
|---|---|---|---|
| 33-45 % | 98 | 41,7 % | 45,9 % |
| 45-55 % | 105 | 50,3 % | 58,1 % |
| 55-65 % | 78 | 59,7 % | 64,1 % |
| 65-75 % | 32 | 69,3 % | 68,8 % |
| 75 %+ | 34 | 82,8 % | 88,2 % |

- Empates UEFA: daba 20,9 %, salieron 17,3 %. Aplanar (T<1) empeora el log-loss en las dos mitades (T=1,0: 0,9135; T=0,8: 0,9275). Se mantiene T=1,05.
- Control: las cuotas americanas de DRatings implican favoritos aún más fuertes que la mesa (Real Madrid ~84 %, Man City ~79 %).

### Pendiente

- Lista oficial SELAE; Europa League (Celta–Bournemouth, Palace–Real Sociedad) sin confirmar.
- Resultados del 7-9/11 y 21-23/11 de las ligas (necesita las webs de §6 o el entorno «markitdown»).
- Bajas A/B (Investigador), cuotas 1X2 de bet365 (Compilador), Risk Manager y Auditor antes del definitivo.

## v1.1 · dom 22/11/2026 02:20 · reglas nuevas tras la J23 (provisional)

- **Un solo boleto:** 24 sencillas no caben en un boleto (§1.5); el 18 € pasa a **directa 3 dobles + 1 triple** (P(14) 1/218, P(≥13) 3,65 %).
- **Fijos protegidos** (`proteccion.py`, regla del 22/11): fijos débiles Brujas–Liverpool (2, 52 %), Celta–Bournemouth (2, 50 %) y Palace–Real Sociedad (1, 53 %); su 2.º signo va en 2 sencillas y el 3.º en 1.
- **Pleno M-1 en todas las apuestas.** X templada: solo Primera, no aplica.

| # | Partido | Boleto 18 € |
|---|---|---|
| 1 | Arsenal – Dortmund | 1 |
| 2 | Feyenoord – Oporto | 1 X 2 |
| 3 | Man. City – Nápoles | 1 |
| 4 | Real Madrid – PSV | 1 |
| 5 | Slovan Bratislava – Betis | 2 |
| 6 | Sabah – Barcelona | 2 |
| 7 | Slavia Praga – Villarreal | 1 2 |
| 8 | Brujas – Liverpool | 2 |
| 9 | Inter – Stuttgart | 1 |
| 10 | PSG – Roma | 1 |
| 11 | Shakhtar – Fenerbahçe | 1 2 |
| 12 | Sporting CP – Man. United | 1 2 |
| 13 | Celta – Bournemouth | 2 |
| 14 | Crystal Palace – Real Sociedad | 1 |

Sencillas protegidas: 12112221112112, 121122211121X2, 1211222X11211X, 12112221112121, 12112222112111, 12112222112X21, 1211222211X121, 121122221121X1.
Conjunto: 32 columnas, 24.00 € · P(14) 1/173 · P(≥13) 4.43 % · P(≥12) 16.2 %. X cubiertas en el boleto: 1.
