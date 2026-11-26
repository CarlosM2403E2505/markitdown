# Calculadora de la Quiniela

Hace las cuentas del prompt maestro (v6). Solo necesita Python 3, sin dependencias.

```bash
# 1X2, marcadores y tres Plenos a partir de los goles esperados
python3 quiniela_calc.py marcador --local 1.55 --visitante 1.05 --factor-x 1.08

# Comprobaciones, boleto A, boleto B (reducida), Pleno y sueltas
python3 quiniela_calc.py boleto ejemplo-jornada.json            # maximiza P(14)
python3 quiniela_calc.py boleto ejemplo-jornada.json --objetivo p13

# Post-mortem: añadir "resultado": "1" | "X" | "2" a cada partido del JSON
python3 quiniela_calc.py postmortem j18.json j19.json

# Tests
python3 -m unittest test_quiniela_calc.py
```

El formato del JSON está en `ejemplo-jornada.json` (sus probabilidades son inventadas).
Un partido con `"veto_unico": true` va siempre a doble.

## Pleno con la mezcla del modelo oficial
```bash
python3 quiniela_calc.py empirica ../datos/euro_j19.csv   # pegar el resultado en pleno.empirica
```
Con `"empirica"` y `"mezcla": 0.2` en el Pleno, la calculadora da los mismos marcadores que el modelo oficial.

## Datos leídos con Claude in Chrome
```bash
python3 importar_navegador.py ../jornadas/j21/j21.json leido.json   # comprueba el boleto oficial y carga % y cuotas
python3 -m unittest test_importar_navegador.py
```
El formato del JSON está en `../navegador/encargo-claude-in-chrome.md`. Si el boleto oficial no coincide con la lista de la jornada, no se escribe nada.
