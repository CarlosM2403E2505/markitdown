"""Tests de las reglas codificadas de la mesa. cd herramientas && python3 -m unittest test_reglas_mesa"""
import json, os, unittest
import reglas_mesa as rm
R = os.path.dirname(os.path.abspath(__file__))
PROBS = [x["p"] for x in json.load(open(os.path.join(R, "..", "jornadas", "j23", "j23.json"), encoding="utf-8"))["partidos"]]

class TestReglas(unittest.TestCase):
    def setUp(self):
        rm.N_OPT, rm.N_EXTRA, rm.N_CANDIDATAS, rm.TOPES_JORNADA = 1500, 300, 300, None
    def test_topes(self):
        self.assertEqual(rm.tope(0.40), 0.60); self.assertEqual(rm.tope(0.54), 0.75)
        self.assertEqual(rm.tope(0.60), 0.90); self.assertEqual(rm.tope(0.80), 1.0)
        self.assertEqual(rm.tope(0.60, ventaja=0.10), 0.75)   # aviso de las casas: tramo de abajo
    def test_mala_forma_endurece(self):
        self.assertEqual(rm.tope(0.54, forma=5), 0.60)   # Rayo J23: 54 % y 5 puntos de 15 → 60 %
        self.assertEqual(rm.tope(0.54, forma=9), 0.75)
        self.assertEqual(rm.tope(0.80, forma=0), 1.0)    # favorito claro: sin tope
    def test_r7_bloques(self):
        b, p13 = rm.presupuesto_r7(PROBS)
        self.assertIn(b, (6.0, 12.0, 18.0)); self.assertLess(p13[8], p13[16]); self.assertLess(p13[16], p13[24])
    def test_presupuesto(self):
        self.assertEqual(int(rm.PRESUPUESTO_MAX / rm.PRECIO), 24)
    def test_optimizadas_cumplen_r3_y_son_deterministas(self):
        Y = rm.muestras(PROBS, rm.N_OPT, semilla=7)
        a = rm.optimizadas(PROBS, 24, Y); b = rm.optimizadas(PROBS, 24, Y)
        self.assertEqual(len(a), 24); self.assertEqual(len(set(a)), 24); self.assertEqual(a, b)
        self.assertEqual(rm.diversidad(PROBS, a), [])
    def test_rayo_no_va_en_todas(self):
        Y = rm.muestras(PROBS, rm.N_OPT, semilla=7)
        a = rm.optimizadas(PROBS, 24, Y)
        self.assertLessEqual(sum(c[1] == "1" for c in a), 18)   # Rayo 54 % → como mucho el 75 %

if __name__ == "__main__":
    unittest.main()
