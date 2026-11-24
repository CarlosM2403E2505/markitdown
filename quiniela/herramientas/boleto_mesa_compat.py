"""Compatibilidad con `boleto_mesa` (reglas_mesa.py, desde la J24): lo traduce a las claves que leen
pronosticos_definitivos.py, archivar_definitivos.py y app_datos.py (boleto_provisional + columnas)."""
S = "1X2"


def desde_boleto_mesa(d):
    """Devuelve (boleto, columnas, solo_sencillas). boleto: tipo, apuestas, coste, signos (cobertura por partido), pleno."""
    b = d.get("boleto_mesa")
    if not b:
        return None
    cols = list(b["columnas"])
    signos = {str(i + 1): " ".join(s for s in S if any(c[i] == s for c in cols)) for i in range(14)}
    boleto = {"tipo": b["formato"], "apuestas": b["apuestas"], "coste": b["coste"], "signos": signos, "pleno": b["pleno"],
              "p14": b.get("p14"), "p13": b.get("p13")}
    # Cualquier formato con sencillas se puede sellar como columnas sencillas (mismas columnas, mismo coste)
    return boleto, cols, b.get("sellar") == "sencillas" or ("sencillas" in b["formato"] and "+" not in b["formato"])
