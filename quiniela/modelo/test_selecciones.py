"""Tests del modelo de selecciones. Ejecutar: python3 -m unittest modelo/test_selecciones.py (desde quiniela/)."""
import importlib.util, os, unittest
R = os.path.dirname(os.path.abspath(__file__))
s = importlib.util.spec_from_file_location("sm", os.path.join(R, "selecciones_modelo.py")); sm = importlib.util.module_from_spec(s); s.loader.exec_module(sm)

class TestSelecciones(unittest.TestCase):
    def test_probabilidades_validas(self):
        p = sm.uno_x_dos(sm.matriz(1.6, 1.0))
        self.assertAlmostEqual(sum(p), 1.0, places=6); self.assertGreater(p[0], p[2])
    def test_elo_simetrico_y_extremos(self):
        a, b = sm.uno_x_dos_elo(0), sm.uno_x_dos_elo(0)
        self.assertAlmostEqual(a[0], a[2], places=6)
        self.assertGreater(sm.uno_x_dos_elo(2000)[0], 0.85)  # no falla con diferencias enormes (con 2,4 goles el techo es ~0,91)
    def test_nombres_en_los_datos(self):
        equipos = {m["home"] for m in sm.cargar("2024-01-01")}
        for es, en in sm.NOMBRES.items():
            self.assertIn(en, equipos, es)
    def test_marcador_a_90(self):
        for m in sm.cargar("2020-01-01"):
            self.assertLessEqual(m["hg90"], m["hg"]); self.assertLessEqual(m["ag90"], m["ag"])

if __name__ == "__main__":
    unittest.main()
