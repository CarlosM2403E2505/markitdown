"""Tests del importador del navegador. Ejecutar con: python3 -m unittest test_importar_navegador.py"""
import copy
import json
import os
import tempfile
import unittest

import importar_navegador as imp
import quiniela_calc as qc

JORNADA = {
    "jornada": 21,
    "partidos": [{"n": i, "partido": nombre, "p": [0.4, 0.3, 0.3]} for i, nombre in enumerate([
        "Valladolid – Castellón", "Real Sociedad B – Sporting", "Almería – Andorra", "Mallorca – Córdoba",
        "Oviedo – Girona", "Tenerife – Ceuta", "Granada – Las Palmas", "Eibar – Cádiz", "Eldense – Sabadell",
        "Bélgica – Italia", "Alavés F – Eibar F", "Real Sociedad F – Athletic F", "Sevilla F – Atlético F",
        "Valencia F – Granada F"], start=1)],
    "pleno": {"partido": "España – Inglaterra", "p": [0.7, 0.2, 0.1]},
}

# Como lo escribiría Loterías: abreviaturas, «(F)» y sin acentos en algunos nombres.
OFICIAL = [("Valladolid", "Castellón"), ("R. Sociedad B", "Sporting"), ("Almería", "Andorra"), ("Mallorca", "Córdoba"),
           ("R. Oviedo", "Girona"), ("Tenerife", "Ceuta"), ("Granada", "Las Palmas"), ("Eibar", "Cádiz"),
           ("Eldense", "Sabadell"), ("Bélgica", "Italia"), ("Alavés (F)", "Eibar (F)"),
           ("R. Sociedad (F)", "Athletic Club (F)"), ("Sevilla (F)", "At. Madrid (F)"), ("Valencia (F)", "Granada (F)")]


def leido(oficial=OFICIAL):
    return {
        "jornada": 21, "leido_el": "2026-11-14T09:30",
        "boleto_oficial": {"fuente": "loteriasyapuestas.es", "cierre": None,
                           "partidos": [{"n": i, "local": l, "visitante": v} for i, (l, v) in enumerate(oficial, 1)],
                           "pleno": {"local": "España", "visitante": "Inglaterra"}},
        "publico": {"fuente": "quiniela15.com", "pleno_mas_jugado": "1-0",
                    "partidos": [{"n": i, "lae": [50, 30, 20], "apu": None} for i in range(1, 15)]},
        "cuotas": {"fuente": "bet365.es", "partidos": [{"n": 10, "partido": "Bélgica – Italia", "c1": 2.2, "cx": 3.3, "c2": 3.4},
                                                     {"n": 1, "partido": "Valladolid – Castellón", "c1": None, "cx": 3.2, "c2": 2.1}]},
    }


class TestImportarNavegador(unittest.TestCase):
    def _preparar(self, datos_leidos, jornada=JORNADA):
        d = tempfile.mkdtemp()
        rj, rl = os.path.join(d, "j21.json"), os.path.join(d, "leido.json")
        with open(rj, "w", encoding="utf-8") as f:
            json.dump(jornada, f, ensure_ascii=False)
        with open(rl, "w", encoding="utf-8") as f:
            json.dump(datos_leidos, f, ensure_ascii=False)
        return d, rj, rl

    def test_boleto_bueno_se_carga(self):
        d, rj, rl = self._preparar(leido())
        dif, hecho = imp.importar(rj, rl)
        self.assertEqual(dif, [])
        j = json.load(open(rj, encoding="utf-8"))
        self.assertEqual(j["publico"]["columna"], "1" * 14)
        self.assertEqual(j["publico"]["pleno"], "1-0")
        self.assertTrue(any(f.startswith("bet365_") for f in os.listdir(d)))
        self.assertTrue(any(f.startswith("navegador_") for f in os.listdir(d)))

    def test_orden_de_la_j21_mal_se_para(self):
        """El error real de la J21: Bélgica–Italia en el 14 en vez de en el 10."""
        mal = copy.deepcopy(JORNADA)
        orden = mal["partidos"]
        bel = orden.pop(9)
        orden.append(bel)
        for i, x in enumerate(orden, 1):
            x["n"] = i
        d, rj, rl = self._preparar(leido(), mal)
        antes = open(rj, encoding="utf-8").read()
        dif, _ = imp.importar(rj, rl)
        self.assertTrue(any(x.startswith("Partido 10") for x in dif))
        self.assertTrue(any(x.startswith("Partido 14") for x in dif))
        self.assertEqual(open(rj, encoding="utf-8").read(), antes)  # no escribe nada
        self.assertEqual(os.listdir(d), ["j21.json", "leido.json"] if os.listdir(d)[0] == "j21.json" else ["leido.json", "j21.json"])

    def test_null_no_se_rellena(self):
        datos = leido()
        datos["publico"]["partidos"][3]["lae"] = None
        d, rj, rl = self._preparar(datos)
        dif, hecho = imp.importar(rj, rl)
        self.assertEqual(dif, [])
        j = json.load(open(rj, encoding="utf-8"))
        self.assertNotIn("4", j["publico"]["porcentajes"])
        self.assertNotIn("columna", j["publico"])  # sin los 14, no hay columna del público
        cuotas = json.load(open(os.path.join(d, [f for f in os.listdir(d) if f.startswith("bet365_")][0])))["cuotas"]
        self.assertEqual(list(cuotas), ["10"])  # la cuota con un null no entra

    def test_otra_jornada_se_rechaza(self):
        datos = leido()
        datos["jornada"] = 22
        _, rj, rl = self._preparar(datos)
        dif, _ = imp.importar(rj, rl)
        self.assertTrue(dif)

    def test_nombres_equivalentes(self):
        self.assertTrue(imp.mismo_equipo("Real Sociedad B", "R. Sociedad B"))
        self.assertTrue(imp.mismo_equipo("Atlético F", "At. Madrid (F)"))
        self.assertTrue(imp.mismo_equipo("Oviedo", "Real Oviedo"))
        self.assertFalse(imp.mismo_equipo("Real Sociedad B", "Real Sociedad"))
        self.assertFalse(imp.mismo_equipo("Bélgica", "Italia"))


class TestValorPublico(unittest.TestCase):
    def test_valor(self):
        v = qc.valor_publico([0.5, 0.3, 0.2], [40, 20, 40])
        self.assertAlmostEqual(v[0], 1.25)
        self.assertAlmostEqual(v[1], 1.5)
        self.assertAlmostEqual(v[2], 0.5)


if __name__ == "__main__":
    unittest.main()
