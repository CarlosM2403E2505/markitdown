import unittest
import analista_lae as al


class TestAnalistaLAE(unittest.TestCase):
    def test_sorteo_total_es_el_publico(self):
        self.assertEqual(al.mezcla_sorteo([0.6, 0.2, 0.2], [0.5, 0.3, 0.2], 1.0), [0.5, 0.3, 0.2])

    def test_sorteo_nulo_es_la_mesa(self):
        self.assertEqual(al.mezcla_sorteo([0.6, 0.2, 0.2], [0.5, 0.3, 0.2], 0.0), [0.6, 0.2, 0.2])

    def test_premio_j21(self):
        # J21 real: recaudación 1.586.225 €, 4 acertantes de 14 a 63.449 €; producto del público 7,09e-7
        n = al.acertantes_14(1586225.25, 7.0866e-7)
        self.assertTrue(2 <= n <= 6)
        self.assertAlmostEqual(al.FONDO_14 * 1586225.25 / 4, 63449.01, delta=1)

    def test_columnas_directa(self):
        d = {"boleto_provisional": {"signos": {str(i): ("1 2" if i == 2 else "1") for i in range(1, 15)}}}
        self.assertEqual(len(al.columnas(d)), 2)


if __name__ == "__main__":
    unittest.main()
