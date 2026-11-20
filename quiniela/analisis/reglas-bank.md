# Apuestas sueltas en bet365 y bank de 500 € (desde el 20/11/2026)

**Encargo de Carlos (20/11/2026):** apuestas sueltas en bet365 sobre los partidos de la jornada, el mejor mercado que vea la mesa (no solo 1X2), todas las que tengan valor con **cuota mínima 1,80**, y un **bank de 500 €** con su gestión de ganancias y pérdidas. Las definitivas salen el día de la jornada junto con la quiniela definitiva.

## Reglas (herramientas/apuestas_valor.py)
| Regla | Valor | Por qué |
|---|---|---|
| Cuota mínima | 1,80 | Carlos |
| Valor mínimo | +5 % (prob. × cuota − 1) | Margen de error del modelo |
| Probabilidad que cuenta | 40 % mesa + 60 % mercado sin margen | J18-J19: log-loss del mercado 0,786/0,729 frente a 0,897/0,858 de la mesa. Sin mezclar, la mesa «vería valor» en cada desacuerdo, y casi siempre es el mercado quien acierta |
| Stake | ¼ de Kelly, tope 2 % del bank por apuesta | Kelly entero arruina con probabilidades inexactas |
| Exposición | máx. 10 % del bank por jornada | Evita una mala jornada catastrófica |
| Stake mínimo | 2 €, redondeo a 0,50 € | |
| Una por partido | La de más valor | Selecciones del mismo partido están correlacionadas |
| Sencillas, no combinadas | — | El margen de la casa se multiplica en cada pata |
| Parada | saldo < 375 € (75 %) | Se para y se revisa; nunca se sube el stake para recuperar |
| Prueba de ventaja | cuota tomada frente a cuota de cierre (CLV) | Con pocas apuestas el saldo es ruido; batir el cierre es la señal |

## Mercados que precia la mesa
1X2, doble oportunidad, empate no apuesta, más/menos 1,5-2,5-3,5 goles, ambos marcan y hándicap ±1,5. Los de 1X2 salen del precio final de la mesa; los de goles, de la matriz de Poisson del partido (xG de `jNN.json`, factor de empate de cada competición).

## Flujo de cada jornada
1. **Provisional (víspera):** `apuestas_valor.py proponer jNN.json --mercado=mercado.json` → lista «Vigilar» con cuota mínima y cuota estimada (mercado de comparadores + margen típico 5 %). Solo partidos con mercado conocido.
2. **Definitiva (día de la jornada, antes de las 10:45):** cuotas reales de bet365 (`navegador/encargo-bet365-apuestas.md`) → `proponer jNN.json cuotas.json` → estado «Propuesta». Siempre comprobar la cuota en bet365 antes de apostar.
3. **Carlos apuesta** (la mesa nunca apuesta): se marca «Apostada» con `cuota_tomada` en `app/apuestas.json`.
4. **Liquidar:** marcador `"marcador": "2-1"` en cada partido de `jNN.json` → `apuestas_valor.py liquidar jNN.json` → `app/bank.json` → `app_datos.py` y volcado a la app (§4).

## Aviso honesto
Las casas ajustan las cuotas con más información que la mesa. Un +5 % calculado no es dinero seguro: con 2-5 apuestas por jornada, el saldo puede bajar varias jornadas seguidas aunque el método tenga ventaja. Por eso los topes son pequeños.
