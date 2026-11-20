# Leer las cuotas de bet365 para las apuestas sueltas (Claude in Chrome)

Mismo montaje seguro que `encargo-claude-in-chrome.md`: perfil de Chrome aparte, bet365.es **sin iniciar sesión**, «Aprobar manualmente», solo bet365.es. Si la web pide datos, descargas o te lleva a otra web, para.

Hazlo el día de la jornada antes de las 10:15 (hora peninsular) y pega el bloque JSON en el hilo de las apuestas con la línea `Jornada NN · cuotas bet365`.

## Texto para pegar en Claude in Chrome

```
Necesito que LEAS cuotas en bet365.es. Solo lectura.

Reglas:
- Abre solo bet365.es. No inicies sesión, no pulses «Apostar», «Acceder», «Registrarse» ni ningún boleto de apuesta. No descargues nada.
- Si una página te pide datos o te lleva a otra web, PARA y avísame.
- Copia solo lo que se ve. Si un mercado no aparece, déjalo fuera. No estimes nada.

Partidos (número y nombre):
[PEGAR AQUÍ LA LISTA DE LOS 15 PARTIDOS, P. EJ. «1 Alavés – Deportivo»]

Para cada partido abre su página y copia, en cuota decimal, estos mercados:
- "1X2": [1, X, 2]
- "DC" (doble oportunidad): [1X, X2, 12]
- "Empate no apuesta": [local, visitante]
- "Goles 1.5", "Goles 2.5", "Goles 3.5": [más de, menos de]
- "Ambos marcan": [sí, no]
- "Hándicap -1.5" (hándicap asiático o europeo -1,5 al local): [local -1,5, visitante +1,5]
- "Hándicap +1.5" (+1,5 al local): [local +1,5, visitante -1,5]

Devuélveme UN ÚNICO bloque JSON, sin texto alrededor:
{"fuente": "bet365.es", "leido_el": "AAAA-MM-DD HH:MM (hora de España)",
 "partidos": [{"n": 1, "partido": "Local – Visitante", "mercados": {"1X2": [2.20, 3.30, 3.40], "Goles 2.5": [1.90, 1.90]}}]}
```

## Qué hace la mesa con el bloque
1. Lo guarda como `jornadas/jNN/cuotas_bet365_AAAAMMDD.json`.
2. `python3 herramientas/apuestas_valor.py proponer jornadas/jNN/jNN.json jornadas/jNN/cuotas_bet365_AAAAMMDD.json`
3. Vuelca `app/apuestas.json` en la app (sección «Apuestas bet365») según §4 de `CLAUDE.md`.
