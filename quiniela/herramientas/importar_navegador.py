#!/usr/bin/env python3
"""Carga en la jornada los datos leídos con Claude in Chrome (ver navegador/encargo-claude-in-chrome.md).

1. Comprueba el boleto oficial contra jornadas/jNN/jNN.json: mismo orden y mismos equipos.
   Si algo no coincide, no escribe nada y lista las diferencias (regla de oro 4).
2. Guarda una copia del JSON leído en jornadas/jNN/navegador_<fecha>.json.
3. Guarda las cuotas de bet365 como jornadas/jNN/bet365_<fecha>.json (formato que leen
   app_datos.py y exportar.py).
4. Guarda en jNN.json los porcentajes del público y, si están los 14, la columna del público.

No rellena nada: un dato que llega como null se queda sin escribir.

Uso: python3 herramientas/importar_navegador.py jornadas/j21/j21.json navegador.json
"""
import json
import os
import re
import sys
import unicodedata

SIGNOS = "1X2"
# Palabras que no distinguen a un equipo; se quitan antes de comparar.
VACIAS = {"real", "r", "club", "cf", "fc", "ud", "cd", "sd", "rcd", "ad", "deportivo", "de", "la", "el", "f",
          "femenino", "women", "balompie", "sad", "calcio"}
FILIALES = {"b", "c", "ii", "fortuna", "promesas", "atletic", "mirandilla", "castilla"}
ALIAS = {"at": "atletico", "atl": "atletico", "athletic": "athletic", "man": "manchester", "utd": "united",
         "betis": "betis", "rso": "sociedad", "sporting": "sporting", "gijon": "sporting"}


def normalizar(nombre):
    s = unicodedata.normalize("NFKD", nombre or "").encode("ascii", "ignore").decode().lower()
    s = re.sub(r"\((f|m)\)", " ", s)
    palabras = [ALIAS.get(p, p) for p in re.findall(r"[a-z0-9]+", s)]
    return [p for p in palabras if p not in VACIAS]


def mismo_equipo(a, b):
    """True si los dos nombres parecen el mismo equipo (prudente: ante la duda, False)."""
    pa, pb = normalizar(a), normalizar(b)
    if not pa or not pb:
        return False
    if pa == pb:
        return True
    # Un nombre corto contenido en el largo («Sociedad B» frente a «Sociedad B», «Valladolid»
    # frente a «Real Valladolid»), siempre que coincida la primera palabra significativa.
    corto, largo = (pa, pb) if len(pa) <= len(pb) else (pb, pa)
    sobrantes = set(largo) - set(corto)
    if sobrantes & FILIALES:  # «Real Sociedad B» no es «Real Sociedad»
        return False
    return corto[0] == largo[0] and all(p in largo for p in corto)


def _partes(partido):
    local, visitante = re.split(r"\s+[–-]\s+", partido.replace(" (Pleno)", ""), maxsplit=1)
    return local, visitante


def comprobar_boleto(jornada, boleto):
    """Lista de diferencias entre el boleto oficial leído y la lista de la jornada."""
    diferencias = []
    oficiales = {p["n"]: p for p in boleto.get("partidos", [])}
    for x in jornada["partidos"]:
        o = oficiales.get(x["n"])
        if o is None:
            diferencias.append(f"Partido {x['n']}: no aparece en el boleto leído")
            continue
        local, visitante = _partes(x["partido"])
        if not (mismo_equipo(local, o.get("local")) and mismo_equipo(visitante, o.get("visitante"))):
            diferencias.append(f"Partido {x['n']}: en la jornada «{x['partido']}», en el boleto oficial "
                               f"«{o.get('local')} – {o.get('visitante')}»")
    pleno = boleto.get("pleno") or {}
    if jornada.get("pleno") and pleno:
        local, visitante = _partes(jornada["pleno"]["partido"])
        if not (mismo_equipo(local, pleno.get("local")) and mismo_equipo(visitante, pleno.get("visitante"))):
            diferencias.append(f"Pleno: en la jornada «{jornada['pleno']['partido']}», en el boleto oficial "
                               f"«{pleno.get('local')} – {pleno.get('visitante')}»")
    return diferencias


def _valido(trio, maximo):
    return isinstance(trio, list) and len(trio) == 3 and all(isinstance(v, (int, float)) and 0 <= v <= maximo for v in trio)


def importar(ruta_jornada, ruta_leido, escribir=True):
    with open(ruta_jornada, encoding="utf-8") as f:
        jornada = json.load(f)
    with open(ruta_leido, encoding="utf-8") as f:
        leido = json.load(f)
    if leido.get("jornada") not in (None, jornada.get("jornada")):
        return [f"El JSON leído es de la jornada {leido.get('jornada')}, no de la {jornada.get('jornada')}"], {}

    boleto = leido.get("boleto_oficial")
    diferencias = comprobar_boleto(jornada, boleto) if boleto and boleto.get("partidos") else []
    if diferencias:
        return diferencias, {}

    carpeta = os.path.dirname(os.path.abspath(ruta_jornada))
    fecha = re.sub(r"[^0-9]", "", (leido.get("leido_el") or ""))[:12] or "sinfecha"
    hecho = {"boleto_comprobado": bool(boleto and boleto.get("partidos"))}

    # Cuotas de bet365, en el formato de bet365_*.json.
    cuotas = {}
    for c in (leido.get("cuotas") or {}).get("partidos", []):
        trio = [c.get("c1"), c.get("cx"), c.get("c2")]
        if c.get("n") and _valido(trio, 1000) and all(v > 1 for v in trio):
            cuotas[str(c["n"])] = trio
    hecho["cuotas"] = len(cuotas)

    # Porcentajes del público.
    publico = leido.get("publico") or {}
    porcentajes = {}
    for p in publico.get("partidos", []):
        entrada = {k: p[k] for k in ("lae", "apu") if _valido(p.get(k), 100)}
        if p.get("n") and entrada:
            porcentajes[str(p["n"])] = entrada
    hecho["porcentajes"] = len(porcentajes)

    if not escribir:
        return [], hecho
    with open(os.path.join(carpeta, f"navegador_{fecha}.json"), "w", encoding="utf-8") as f:
        json.dump(leido, f, ensure_ascii=False, indent=1)
    if cuotas:
        with open(os.path.join(carpeta, f"bet365_{fecha}.json"), "w", encoding="utf-8") as f:
            json.dump({"fuente": f"bet365.es leído con Claude in Chrome, {leido.get('leido_el')}", "cuotas": cuotas},
                      f, ensure_ascii=False, indent=1)
    if porcentajes or publico.get("pleno_mas_jugado"):
        pub = jornada.setdefault("publico", {})
        pub["porcentajes"] = porcentajes
        pub["fuente"] = f"{publico.get('fuente', 'quiniela15.com')} leído con Claude in Chrome, {leido.get('leido_el')}"
        lae = [porcentajes.get(str(x["n"]), {}).get("lae") for x in jornada["partidos"]]
        if all(lae):
            pub["columna"] = "".join(SIGNOS[t.index(max(t))] for t in lae)
        if publico.get("pleno_mas_jugado"):
            pub["pleno"] = publico["pleno_mas_jugado"]
        hecho["columna_publico"] = pub.get("columna")
    if boleto and boleto.get("partidos"):
        jornada["lista"] = f"Boleto oficial comprobado con loteriasyapuestas.es (Claude in Chrome, {leido.get('leido_el')})"
    with open(ruta_jornada, "w", encoding="utf-8") as f:
        json.dump(jornada, f, ensure_ascii=False, indent=1)
    return [], hecho


def main(argv=None):
    argv = argv or sys.argv[1:]
    if len(argv) != 2:
        print(__doc__)
        return 2
    diferencias, hecho = importar(argv[0], argv[1])
    if diferencias:
        print("NO SE HA CARGADO NADA. El boleto oficial no coincide con la lista de la jornada:")
        for d in diferencias:
            print("  - " + d)
        return 1
    print("Cargado:", json.dumps(hecho, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
