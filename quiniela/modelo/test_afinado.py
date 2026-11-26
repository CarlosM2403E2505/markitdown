"""Tests del afinado por competición. python3 -m unittest modelo/test_afinado.py (desde quiniela/)."""
import importlib.util, os, unittest
R = os.path.dirname(os.path.abspath(__file__))
s = importlib.util.spec_from_file_location("af", os.path.join(R, "afinado.py")); af = importlib.util.module_from_spec(s); s.loader.exec_module(af)

class TestAfinado(unittest.TestCase):
    def test_suma_uno(self):
        for c in ("es.1", "es.2", None):
            self.assertAlmostEqual(sum(af.afinar_comp([0.5, 0.3, 0.2], c)), 1.0, places=9)
    def test_primera_afila_mas_que_segunda(self):
        p = [0.68, 0.20, 0.12]  # fuera del tramo de X templada (45-60 %)
        f1 = af.afinar_comp(p, "es.1:2026-27")[0]; f2 = af.afinar_comp(p, "es.2:2026-27")[0]
        self.assertGreater(f1, f2)  # Primera sube más al favorito
    def test_defecto_es_105(self):
        self.assertEqual(af.afinar_comp([0.4, 0.3, 0.3], "uefa.cl"), af.afinar_comp([0.4, 0.3, 0.3], None))

    def test_ligaf_aplana(self):
        p = [0.75, 0.15, 0.10]
        self.assertLess(af.afinar_comp(p, "ligaf")[0], 0.75)

    def test_x_templada_primera(self):
        p = [0.52, 0.26, 0.22]
        q = af.afinar_comp(p, "es.1")
        r = [v ** 1.15 for v in p]; r = [v / sum(r) for v in r]
        self.assertGreater(q[1], r[1])          # sube la X
        self.assertAlmostEqual(sum(q), 1.0, places=9)
    def test_x_templada_no_toca_claros_ni_segunda(self):
        p = [0.58, 0.24, 0.18]  # favorito entre 60 y 65 % tras T: ni templada ni claro
        r = [v ** 1.15 for v in p]; r = [v / sum(r) for v in r]
        self.assertTrue(0.60 <= max(r) < 0.65)
        self.assertEqual([round(v, 9) for v in af.afinar_comp(p, "es.1")], [round(v, 9) for v in r])
        p2 = [0.52, 0.26, 0.22]
        r2 = [v ** 1.05 for v in p2]; r2 = [v / sum(r2) for v in r2]
        self.assertEqual([round(v, 9) for v in af.afinar_comp(p2, "es.2")], [round(v, 9) for v in r2])

    def test_x_baja_con_favorito_claro_primera(self):
        p = [0.80, 0.12, 0.08]
        r = [v ** 1.15 for v in p]; r = [v / sum(r) for v in r]
        q = af.afinar_comp(p, "es.1")
        self.assertLess(q[1], r[1]); self.assertGreater(q[0], r[0])
        self.assertAlmostEqual(sum(q), 1.0, places=9)


if __name__ == "__main__":
    unittest.main()
