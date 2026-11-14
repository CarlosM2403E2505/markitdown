"""Tests del criterio de elección del boleto único. Ejecutar: python3 -m unittest test_boleto_unico.py"""
import unittest
import boleto_unico as bu

C = [{"nombre": "A", "coste": 18.0, "p14": 1 / 1273, "p13": 0.0085, "p12": 0.043},
     {"nombre": "B", "coste": 19.5, "p14": 1 / 1136, "p13": 0.0093, "p12": 0.047},
     {"nombre": "C", "coste": 18.0, "p14": 1 / 2113, "p13": 0.0081, "p12": 0.049}]

class TestBoletoUnico(unittest.TestCase):
    def test_objetivo_p13(self):
        self.assertEqual(bu.elegir(C, "p13")["nombre"], "B")
    def test_criterio_fijo(self):
        # Fijo: P(14) ≥ 90 % de la máxima (solo B cumple) → B.
        self.assertEqual(bu.elegir(C, "fijo")["nombre"], "B")
    def test_un_solo_boleto_de_papel(self):
        # Sin las 26 sencillas (no caben en un boleto), gana la directa A por P(≥13).
        self.assertEqual(bu.elegir([C[0], C[2]], "p13")["nombre"], "A")

if __name__ == "__main__":
    unittest.main()
