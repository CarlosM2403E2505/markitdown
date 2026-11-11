# Estado del proyecto y del sistema
Copiado de la memoria de claude.ai el 11/11/2026.

## Objetivo
- Se describe como experto en la Quiniela española y la analiza jornada a jornada. El objetivo de todos los estudios es acertar el Pleno al 15.
- El 26/10/2026 unió todo el trabajo en el proyecto "F Almacén" de claude.ai. La entrada es `docs/00-indice.md` y la memoria anterior está en `docs/memoria-de-trabajo.md`.
- Su prompt maestro original y el análisis de la J13 se hicieron en otro chat y no están aquí.

## Sistema (lo que pidió recordar)
- **Modelo:** Poisson multi-liga jerárquico.
  - Parámetros: xi 0,0015; ridge 10/0,05; escala 1,05; mezcla del Pleno 0,20.
  - Empates: ×1,08 en ligas, ×1,0 en copas UEFA y ×0,85 en Liga F.
  - Campo en Primera: +0,07.
  - La Liga F va partido a partido, sin los partidos del Barça.
- **Riesgo:**
  - Nada por debajo del 65% es fijo.
  - Campo nórdico o dato no verificado: nunca fijo.
  - Tope del 5% por ajuste, salvo la baja del portero o del delantero centro.
  - El cansancio de Copa o Europa se aplica en ataque y en defensa.
  - El mismo Pleno en todas las columnas.
  - El Red Team no cambia signos con más de 10 puntos de ventaja.
- **Probados y descartados:** enfrentamientos directos, cambio de entrenador y árbitros no mejoran el 1X2; solo valen como aviso.
- **Con 12 €:** 4 dobles completos dan más P(14); la reducida de 7 dobles da más premios de 10–12.
- **xG:** solo en Primera, de statz.ai (datos Sportmonks). Ataque ×(xG/goles)^0,30 y defensa ×(xGA/encajados)^0,15, con tope de ±5%.

## Fuentes que pidió usar
- Sofascore, Transfermarkt, Understat, Football-Data y Flashscore. Estado comprobado el 27/10: Transfermarkt bloqueada; Understat y Football-Data no abren; Sofascore abre sin datos; de Flashscore solo sirven las noticias.
- bet365.es para cuotas y movimientos (solo control, en su navegador y con su aprobación).
- Para información de equipos: Marca, Sport, MD, L'Équipe, Le Figaro Sport, Sky Sports y The Sun Sport. Marca, Sport, MD y L'Équipe están bloqueadas por motivos legales y no se intentan.

## Historial de jornadas
| Jornada | Qué pasó |
|---|---|
| J13 (Champions/Europa) | Principal 7 de 11; Pleno fallado (1-2 frente a M-M); trampa nórdica |
| J14 | 5 columnas; mejor columna 11 (sin sellar); sueltas 5/5 |
| J15 | 5 columnas con Pleno M-1; mejor columna 9 |
| J16 | Primera reducida de 7 dobles; mejor columna 8 de 13; sueltas 4/5 |
| J17 | Descartada a petición suya |
| J18 | A-R a 18 € (dos boletos); la app rechazó el boleto el sábado a las 12:01 |
| J19 (europea) | 18 € (12 + 6); mejor columna 10, sin premio; sueltas 5/5 |
| J20 | 18 € (12 + 6), sellada el sábado por la mañana; mejor columna 8, sin premio; sueltas 3/5. P14 aplazado y decidido por sorteo |

- Selló la J19 y la J20 (18 € cada una); lo confirmó el 10/11/2026.
- Su administración de Loterías tiene horario continuo.
