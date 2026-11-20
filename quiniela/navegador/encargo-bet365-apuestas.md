# Leer las cuotas de bet365 para las apuestas sueltas (Claude in Chrome)

Mismo montaje seguro que `encargo-claude-in-chrome.md`: perfil de Chrome aparte, bet365.es **sin iniciar sesión**, «Aprobar manualmente», solo bet365.es. Si la web pide datos, descargas o te lleva a otra web, para.

Hazlo el día de la jornada antes de las 10:15 (hora peninsular) y pega el bloque JSON en el hilo de las apuestas con la línea `Jornada NN · cuotas bet365`.

## Texto para pegar en Claude in Chrome
Cada jornada se genera con las candidatas de la lista provisional (solo sus mercados, con todas las selecciones para quitar el margen):

```bash
python3 herramientas/apuestas_valor.py encargo jornadas/jNN/jNN.json > navegador/encargo-bet365-jNN.md
```

J23: `navegador/encargo-bet365-j23.md`.

## Qué hace la mesa con el bloque
1. Lo guarda como `jornadas/jNN/cuotas_bet365_AAAAMMDD.json`.
2. `python3 herramientas/apuestas_valor.py proponer jornadas/jNN/jNN.json jornadas/jNN/cuotas_bet365_AAAAMMDD.json` (claves "mercado|selección")
3. Vuelca `app/apuestas.json` en la app (sección «Apuestas bet365») según §4 de `CLAUDE.md`.
