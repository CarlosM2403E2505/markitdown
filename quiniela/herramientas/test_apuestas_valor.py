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
        self.assertTrue(av.gana("Goles 2.5", 0, 2, 1))
        self.assertFalse(av.gana("Ambos marcan", 0, 2, 0))
        self.assertIsNone(av.gana("Empate no apuesta", 0, 1, 1))
        self.assertTrue(av.gana("Hándicap -1.5", 0, 3, 1))
        self.assertTrue(av.gana("Hándicap +1.5", 0, 0, 1))
        self.assertTrue(av.gana("DC", 1, 0, 2))

    def test_probabilidades_suman(self):
        probs, _ = av.probabilidades([0.5, 0.25, 0.25], 1.5, 1.0, "Primera")
        for m in ("Goles 2.5", "Ambos marcan", "Hándicap -1.5", "Hándicap +1.5"):
            self.assertAlmostEqual(sum(probs[m]), 1.0, places=6)

    def test_con_cuotas_respeta_topes(self):
        c = {"partidos": [{"n": n, "mercados": {"1X2": [2.6, 3.4, 2.9], "Goles 2.5": [2.1, 1.75]}} for n in range(1, 16)]}
        ruta = os.path.join(self.tmp, "c.json")
        json.dump(c, open(ruta, "w"))
        filas, bank = av.proponer(J, ruta)
        self.assertTrue(filas)
        self.assertLessEqual(sum(f["stake"] for f in filas), av.TOPE_JORNADA * bank + 1e-9)
        for f in filas:
            self.assertGreaterEqual(f["cuota"], av.CUOTA_MIN)
            self.assertGreaterEqual(f["valor"], av.VALOR_MIN)
            self.assertLessEqual(f["stake"], av.TOPE_APUESTA * bank)
        self.assertEqual(len({f["n"] for f in filas}), len(filas))

    def test_bank(self):
        json.dump({"inicial": 500, "movimientos": [{"id": "a", "stake": 10, "importe": 9}, {"id": "b", "stake": 10, "importe": -10}]},
                  open(av.RUTA_BANK, "w"))
        r = av.resumen_bank()
        self.assertEqual(r["saldo"], 499)
        self.assertAlmostEqual(r["yield"], -0.05)
        self.assertAlmostEqual(r["drawdown_max"], 10 / 509, places=4)


if __name__ == "__main__":
    unittest.main()
