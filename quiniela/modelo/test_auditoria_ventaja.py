"""Tests de la auditoría de ventaja. Ejecutar: python3 -m unittest modelo/test_auditoria_ventaja.py (desde quiniela/)."""
import importlib.util, math, os, unittest
import numpy as np
R = os.path.dirname(os.path.abspath(__file__))
s = importlib.util.spec_from_file_location("av", os.path.join(R, "auditoria_ventaja.py")); av = importlib.util.module_from_spec(s); s.loader.exec_module(av)

class TestAuditoriaVentaja(unittest.TestCase):
    def test_logloss_tasa_base(self):
        # Con una muestra de solo locales, la climatología [1,0,0] da log-loss 0.
        filas = [{"p": [0.5, 0.3, 0.2], "r": 0} for _ in range(10)]
        self.assertAlmostEqual(av.logloss(filas, lambda f: [1.0, 1e-12, 1e-12]), 0.0, places=5)
    def test_acierto(self):
        filas = [{"p": [0.5, 0.3, 0.2], "r": 0}, {"p": [0.2, 0.3, 0.5], "r": 2}]
        self.assertEqual(av.acierto(filas, lambda f: int(np.argmax(f["p"]))), 1.0)
    def test_dist_boleto_suma(self):
        filas = [{"p": [0.5, 0.3, 0.2], "r": 0} for _ in range(28)]
        nb, obs, esp = av.dist_boleto(filas)
        self.assertEqual(nb, 2)
        self.assertAlmostEqual(esp.sum(), 2.0, places=6)
        self.assertEqual(obs.sum(), 2)

if __name__ == "__main__":
    unittest.main()
