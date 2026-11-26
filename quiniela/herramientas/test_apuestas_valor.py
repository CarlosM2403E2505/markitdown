import json
import os
import tempfile
import unittest

import apuestas_valor as av

J = os.path.join(av.RAIZ, "jornadas", "j23", "j23.json")


class TestApuestasValor(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        av.RUTA_APUESTAS = os.path.join(self.tmp, "apuestas.json")
        av.RUTA_BANK = os.path.join(self.tmp, "bank.json")

    def test_liquidacion(self):
        self.assertTrue(av.gana("Goles 2.5", "Más de 2,5", (2, 1), (0, 0)))
        self.assertFalse(av.gana("Ambos marcan", "Sí", (2, 0), (1, 0)))
        self.assertIsNone(av.gana("Empate no apuesta", "Local", (1, 1), (0, 0)))
        self.assertTrue(av.gana("Hándicap local -1.5", "Local -1,5", (3, 1), (1, 0)))
        self.assertTrue(av.gana("Hándicap local -1.5", "Visitante +1,5", (0, 1), (0, 0)))
        self.assertTrue(av.gana("Doble oportunidad", "X2", (0, 2), (0, 1)))
        self.assertTrue(av.gana("Descanso/Final", "X/1", (2, 1), (1, 1)))
        self.assertTrue(av.gana("Goles 2.ª parte 1.5", "2.ª parte más de 1,5", (3, 1), (1, 0)))

    def test_probabilidades(self):
        probs = av.probabilidades([0.5, 0.25, 0.25], 1.5, 1.0, "Primera")
        for m, sels in probs.items():
            if m in ("Empate no apuesta", "Doble oportunidad"):
                continue
            self.assertAlmostEqual(sum(g for g, _, _ in sels.values()), 1.0, places=6, msg=m)
        self.assertAlmostEqual(probs["1X2"]["1"][0], 0.5, places=6)  # cuadra con el 1X2 de la mesa
        self.assertAlmostEqual(probs["Empate no apuesta"]["Local"][1], 0.25, places=6)

    def test_coherente_con_la_quiniela(self):
        filas, _, _ = av.proponer(J)
        self.assertTrue(filas)
        for f in filas:
            if f["n"] == 7:  # Getafe – Atlético: la quiniela lleva X2
                self.assertNotIn(f["seleccion"], ("1", "Local", "1X", "Local gana a cero: sí"))
            self.assertEqual(f["estado"], "Vigilar")
            self.assertGreaterEqual(f["cuota_minima"], av.CUOTA_MIN)

    def test_con_cuotas_respeta_topes(self):
        c = {"partidos": [{"n": n, "cuotas": {"1X2|1": 2.6, "1X2|X": 3.4, "1X2|2": 2.9, "Goles 2.5|Más de 2,5": 2.1,
                                               "Goles 2.5|Menos de 2,5": 1.85}} for n in range(1, 16)]}
        ruta = os.path.join(self.tmp, "c.json")
        with open(ruta, "w") as f:
            json.dump(c, f)
        filas, bank, _ = av.proponer(J, ruta)
        self.assertTrue(filas)
        self.assertLessEqual(sum(f["stake"] for f in filas), av.TOPE_JORNADA * bank + 1e-9)
        for f in filas:
            self.assertGreaterEqual(f["cuota"], av.CUOTA_MIN)
            self.assertGreaterEqual(f["valor"], av.VALOR_MIN)
            self.assertLessEqual(f["stake"], av.TOPE_APUESTA * bank)
        self.assertEqual(len({f["n"] for f in filas}), len(filas))

    def test_bank(self):
        with open(av.RUTA_BANK, "w") as f:
            json.dump({"inicial": 500, "movimientos": [{"id": "a", "stake": 10, "importe": 9},
                                                       {"id": "b", "stake": 10, "importe": -10}]}, f)
        r = av.resumen_bank()
        self.assertEqual(r["saldo"], 499)
        self.assertAlmostEqual(r["yield"], -0.05)
        self.assertAlmostEqual(r["drawdown_max"], 10 / 509, places=4)

    def test_clv(self):
        with open(av.RUTA_APUESTAS, "w") as f:
            json.dump({"rows": [{"id": "x", "jornada": 23, "n": 1, "mercado": "1X2", "seleccion": "1",
                                 "estado": "Apostada", "cuota": 2.3, "cuota_tomada": 2.3, "stake": 10}]}, f)
        ruta = os.path.join(self.tmp, "cierre.json")
        with open(ruta, "w") as f:
            json.dump({"partidos": [{"n": 1, "cuotas": {"1X2|1": 2.1}}]}, f)
        av.cierre(J, ruta)
        self.assertAlmostEqual(av.clv_medio()[0], 2.3 / 2.1 - 1, places=4)


if __name__ == "__main__":
    unittest.main()
