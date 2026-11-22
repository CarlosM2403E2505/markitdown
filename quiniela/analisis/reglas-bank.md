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
| Coherencia (Carlos, 20/11) | Solo lo que la mesa espera: la selección más probable de su mercado, y nunca a favor de un signo que la quiniela descarta | Nada de «Getafe empate no apuesta» con la quiniela en X2 |
| Una por partido | La de más valor | Selecciones del mismo partido están correlacionadas |
| Sencillas, no combinadas | — | El margen de la casa se multiplica en cada pata |
| Parada | saldo < 375 € (75 %) | Se para y se revisa; nunca se sube el stake para recuperar |
| Prueba de ventaja | cuota tomada frente a cuota de cierre (CLV) | Con pocas apuestas el saldo es ruido; batir el cierre es la señal |

## Mercados que precia la mesa (29 por partido)
1X2, doble oportunidad, empate no apuesta, goles 0,5 a 4,5, goles del local y del visitante (0,5-1,5-2,5), ambos marcan, hándicaps ±1,5 y ±2,5 a cada equipo, gana a cero (local y visitante), resultado y ambos marcan, resultado y goles 2,5, descanso 1X2, goles de la 1.ª parte (0,5 y 1,5), goles de la 2.ª parte (1,5), mitad con más goles y descanso/final.
Salen de un Poisson por partes (45 % de los goles antes del descanso) con los xG de `jNN.json`, el factor de empate de cada competición y los signos reescalados al 1X2 final de la mesa, para que todo cuadre con la quiniela.
**Sin modelo, no se apuestan todavía:** córners, tarjetas, goleadores y resultado exacto (salvo el Pleno). Haría falta un histórico por equipo y árbitro; la mesa no inventa precios.

## Flujo de cada jornada
1. **Provisional (víspera):** `apuestas_valor.py proponer jNN.json` → hasta 3 candidatas por partido (estado «Vigilar») con su **cuota mínima** = cuota justa de la mesa × 1,10 (y nunca menos de 1,80). Se descarta lo que la mesa ve tan seguro que la casa no pagará 1,80 (cuota justa < 1,60) y lo muy improbable (cuota mínima > 3,50). Después, `encargo jNN.json` genera el texto para leer esas cuotas en bet365.
2. **Definitiva (día de la jornada, antes de las 10:45):** cuotas reales de bet365 (`navegador/encargo-bet365-apuestas.md`) → `proponer jNN.json cuotas.json` → estado «Propuesta». Siempre comprobar la cuota en bet365 antes de apostar.
3. **Carlos apuesta** (la mesa nunca apuesta): se marca «Apostada» con `cuota_tomada` en `app/apuestas.json`.
4. **Liquidar:** marcador `"marcador": "2-1"` en cada partido de `jNN.json` → `apuestas_valor.py liquidar jNN.json` → `app/bank.json` → `app_datos.py` y volcado a la app (§4).
5. **CLV:** al apostar se anota `cuota_tomada`; justo antes del partido se leen las cuotas de cierre de bet365 (mismo formato que las de la definitiva) → `apuestas_valor.py cierre jNN.json cierre.json`. CLV = tomada / cierre − 1; sale por apuesta y de media en «Bank». Con pocas apuestas el saldo es ruido: un CLV medio positivo es la señal de ventaja.

## Aviso honesto
Las casas ajustan las cuotas con más información que la mesa. Un +5 % calculado no es dinero seguro: con 2-5 apuestas por jornada, el saldo puede bajar varias jornadas seguidas aunque el método tenga ventaja. Por eso los topes son pequeños.
