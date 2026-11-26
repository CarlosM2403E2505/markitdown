import unittest
from puntuar_externo import puntuar


class T(unittest.TestCase):
    def test_basico(self):
        j = {"partidos": [
            {"n": 1, "p": [0.6, 0.25, 0.15], "mercado": [0.5, 0.3, 0.2], "resultado": "1"},
            {"n": 2, "p": [0.3, 0.3, 0.4], "mercado": [0.3, 0.3, 0.4], "resultado": ""},
        ]}
        x = {"partidos": [{"n": 1, "estudio_1x2": [80, 10, 10]}, {"n": 2, "estudio_1x2": None}]}
        r = puntuar(j, x)
        self.assertEqual(r["partidos"], 1)
        self.assertTrue(r["estudio_gana_al_mercado"])
        self.assertAlmostEqual(r["estudio"]["brier"], 0.06, places=4)


if __name__ == "__main__":
    unittest.main()
