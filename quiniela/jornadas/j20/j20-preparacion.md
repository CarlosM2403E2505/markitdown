# Jornada 20 · preparación (antes de la primera pasada) · miércoles 4/11/2026

> Estado: **sin lista verificada**. Según el prompt v7 (fase 0), no se da precio hasta tener el boleto oficial.

## Lista provisional (búsqueda web del 4/11; sin verificar)

- **Fecha y cierre:** fin de semana del 7 y 8 de noviembre. Cierre el sábado 7 a las 14:00 (dato de un pronóstico publicado; confirmar).
- **Composición:** 7 de Primera + 3 de Segunda + 4 de Liga F. Pleno entre dos aspirantes al título.
- **Primera** (según las fuentes): Málaga – Racing (sáb 14:00), Osasuna – Athletic (sáb 18:30), Valencia – Real Madrid (sáb 21:00), Elche – Betis (dom 14:00), Real Sociedad – Rayo (dom 16:15), Celta – Levante (dom 18:30), Villarreal – Getafe (dom 18:30).
- **Segunda y Liga F:** las fuentes no coinciden (Eduardo Losilla cita Cádiz – Oviedo y Girona – Almería). Pendiente.
- **Pleno:** no identificado.

Fuentes: eduardolosilla.es (escrutinio de la jornada 20), quinielafutbol.info (próximas jornadas). Las dos con fechas de publicación que no cuadran: no se usan como lista oficial.

## Comprobación de datos (`datos/euro_j19.csv`)

- Los 14 equipos de Primera de la lista provisional están en `es.1:2026-27` (Málaga y Racing incluidos). En el dataset, el Athletic se llama `athletic bilbao`.
- **Huecos por cubrir antes del precio:**
  - Primera: faltan 3 partidos del fin de semana del 31/10 al 2/11 (el último de Osasuna es del 26/10; el de Valencia y Elche, del 24/10). Primera tiene 107 de 110 partidos hasta la jornada 11.
  - Segunda: el último partido del Cádiz es del 25/10.
  - UEFA: los datos terminan el 22/10. Faltan los partidos de esta semana (Champions del 3–4/11; Europa League y Conference del 5/11).
  - Liga F: la mesa la tiene escrita a mano en `modelo/j18_run.py`, solo hasta la jornada 8. Faltan las jornadas posteriores.
- **Calendario y fatiga (fase 3):** Villarreal, Real Madrid y Betis juegan Champions el martes o el miércoles (sin ajuste). Real Sociedad, Celta y Getafe juegan el jueves 5 en Europa League o Conference: −4 % en ataque y +2–3 % en goles encajados. Confirmar con los resultados y los minutos de los titulares.

## Plan (calendario del prompt)

1. **Jueves 5 por la noche o viernes 6 por la mañana · primera pasada:** con el boleto oficial, los huecos cubiertos y los europeos jugados.
2. **Sábado 7 por la mañana, antes de las 14:00 · revisión final:** bajas, alineaciones probables, cuotas y lo que juega el público.
3. **J19 · post-mortem:** cuando termine el jueves 5.

## Cambios del prompt v8 que afectan a la J20

- 1X2 del modelo elevado a T = 1,05 antes de los ajustes (`quiniela_calc.afinar`).
- Factor de empates: Primera 1,08 · **Segunda 1,00** · Liga F 0,85.
- Boleto congelado el sábado 7 a las 11:00 como tarde (3 horas antes del cierre de las 14:00).
