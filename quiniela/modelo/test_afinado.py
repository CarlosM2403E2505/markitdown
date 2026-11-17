"""Tests del afinado por competición. python3 -m unittest modelo/test_afinado.py (desde quiniela/)."""
import importlib.util, os, unittest
R = os.path.dirname(os.path.abspath(__file__))
s = importlib.util.spec_from_file_location("af", os.path.join(R, "afinado.py")); af = importlib.util.module_from_spec(s); s.loader.exec_module(af)

class TestAfinado(unittest.TestCase):
    def test_suma_uno(self):
        for c in ("es.1", "es.2", None):
            self.assertAlmostEqual(sum(af.afinar_comp([0.5, 0.3, 0.2], c)), 1.0, places=9)
    def test_primera_afila_mas_que_segunda(self):
        p = [0.55, 0.25, 0.20]
        f1 = af.afinar_comp(p, "es.1:2026-27")[0]; f2 = af.afinar_comp(p, "es.2:2026-27")[0]
        self.assertGreater(f1, f2)  # Primera sube más al favorito
    def test_defecto_es_105(self):
        self.assertEqual(af.afinar_comp([0.4, 0.3, 0.3], "uefa.cl"), af.afinar_comp([0.4, 0.3, 0.3], None))

if __name__ == "__main__":
    unittest.main()
