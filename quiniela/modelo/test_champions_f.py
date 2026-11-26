"""Tests del modelo de Champions femenina. python3 -m unittest modelo/test_champions_f.py (desde quiniela/)."""
import importlib.util, os, unittest
R = os.path.dirname(os.path.abspath(__file__))
s = importlib.util.spec_from_file_location("cf", os.path.join(R, "champions_f_modelo.py")); cf = importlib.util.module_from_spec(s); s.loader.exec_module(cf)

class TestChampionsF(unittest.TestCase):
    def setUp(self):
        self.lf = cf.ajustar()
    def test_converge_y_equipos(self):
        self.assertTrue(self.lf["ok"])
        for t in ("Barcelona", "Lyon", "Chelsea", "Bayern", "Arsenal", "Juventus", "Roma", "Servette", "Häcken", "OH Leuven"):
            self.assertIn(t, self.lf["att"], t)
    def test_rates_positivas(self):
        l, u = cf.rates(self.lf, "Barcelona", "Servette")
        self.assertGreater(l, 0); self.assertGreater(l, u)  # Barça local y muy favorito
    def test_fuerza_coherente(self):
        f = {t: self.lf["att"][t] - self.lf["dfn"][t] for t in self.lf["teams"]}
        self.assertGreater(f["Lyon"], f["Servette"]); self.assertGreater(f["Barcelona"], f["OH Leuven"])

if __name__ == "__main__":
    unittest.main()
