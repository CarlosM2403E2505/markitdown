# Mesa Quiniela · modelo y datos (J19, 2/11/2026)

## Contenido
| Carpeta / archivo | Qué es |
|---|---|
| `modelo/euro_model.py` | **Modelo oficial**: Poisson multi-liga jerárquico. log(goles) = c + ventaja de campo + ataque + defensa. Ponderación temporal exp(−xi·días), encogimiento ridge y niveles de liga enlazados por los partidos europeos |
| `modelo/j16_run.py` | Funciones compartidas: `finish()` pasa las lambdas a 1X2, marcadores y mercados. Incluye el modelo de Liga F de la J16 |
| `modelo/j18_run.py` | Jornada doméstica (Primera, Segunda y Liga F): empates ×1,08 en ligas, ×0,85 en Liga F y +0,07 de ventaja de campo en Primera |
| `modelo/j19_run.py` | Jornada europea (Champions, Europa League y Conference): empates ×1,0 |
| `modelo/lambdas_desde_1x2.py` | Saca las lambdas que reproducen un 1X2 dado (para precios con ajustes) |
| `modelo/reducida7.py` | Reducida de 7 dobles al 13 (código de Hamming [7,4]) y cálculo exacto de aciertos |
| `modelo/j19_director.py` | Boletos de 4 dobles y de reducida, con vetos |
| `modelo/eval18.py` | Boletos de 24 apuestas (1 triple + 3 dobles) frente al modelo, el mercado y una mezcla al 50% |
| `modelo/prueba_veto.py` | Prueba fuera de muestra del "favorito que viene de perder en Europa" |
| `datos/euro_j19.json` / `.csv` | **23.631 partidos** (2024 → 1/11/2026): unas 60 ligas europeas y las copas UEFA. Formato: fecha, competición, local, visitante, goles |
| `datos/j19_fx.json` | Los 15 partidos de la J19 con los nombres del dataset |
| `datos/j19_modelo_v1_sin_ajustes.json` | Salida del modelo sin ajustes (1X2, xG, marcadores y mercados) |
| `datos/j19_precio_final.json` | Precio final de la mesa (con bajas A/B y −4,5 puntos al favorito que viene de perder) |
| `datos/j19_lambdas_1x2.json` | El bloque JSON de lambdas, 1X2 y vetos |
| `datos/bet365_lunes_2nov_1300.json` | Foto de cuotas bet365 y OddsPortal (solo control; nunca entra en el modelo) |

## Requisitos y uso
Python 3.10 o superior, `numpy` y `scipy`.

```
cd modelo
python3 j19_run.py ../datos/euro_j19.json ../datos/j19_fx.json salida.json '{"15":[0.985,0.925]}'
python3 lambdas_desde_1x2.py ../datos/j19_precio_final.json 1.0
python3 eval18.py
python3 prueba_veto.py        # tarda varios minutos: ajusta el modelo dos veces
```

El tercer argumento de `j19_run.py` son los ajustes por partido, `{"n": [factor_lambda_local, factor_lambda_visitante]}`. El ejemplo aplica las bajas del Bayern en el Pleno. El ajuste dura unos 1–2 minutos.

## Parámetros
- xi = 0,0015; ridge = 10; escala = 1,05; mezcla = 0,2; jerárquico = sí.
- Empates: ×1,08 en ligas, ×1,0 en copas UEFA, ×0,85 en Liga F.
- Ventaja de campo extra en Primera: +0,07.
- Marcadores del Pleno: 80% Poisson + 20% distribución empírica.

## Fuentes de los datos y huecos conocidos
- **Fuentes:** openfootball (football.json, europe, champions-league) hasta el 20/09/2026. A partir de ahí, uefa.com, futboltotal.futbol, ESPN y thestatsapi, comprobados con 211 partidos que coincidían.
- **Huecos:**
  - Noruega 2026 a medias (80 de unos 200 partidos).
  - Chequia sin datos desde el 20/09.
  - Faltan las temporadas 2025-26 de Grecia, Turquía, Bélgica y Chequia.
  - Unos 25 partidos del 1/11 sin marcador.
  - Por eso, los precios de AEK, Fenerbahçe, Slavia y Union son los menos fiables.

## Avisos
- Las cuotas solo se usan como control.
- Los resultados históricos son datos públicos de partidos.
- El modelo no garantiza nada: en la J18 el público y el mercado predijeron mejor que él (log-loss 0,786 frente a 0,897). La prueba de confianza está para medirlo.
