"""Tests de la calculadora. Ejecutar con: python3 -m unittest test_quiniela_calc.py"""
import itertools
import random
import unittest

import quiniela_calc as qc


def _probs_aleatorias(semilla, n=14):
    rnd = random.Random(semilla)
    probs = []
    for _ in range(n):
        a, b, c = (rnd.random() + 0.1 for _ in range(3))
        s = a + b + c
        probs.append([a / s, b / s, c / s])
    return probs


def _fuerza_bruta(probs, columnas):
    """Distribución del mejor número de aciertos enumerando los 3^n resultados."""
    dist = [0.0] * (len(probs) + 1)
    for resultado in itertools.product(range(3), repeat=len(probs)):
        p = 1.0
        for pr, r in zip(probs, resultado):
            p *= pr[r]
        mejor = max(sum(qc.SIGNOS[r] == c[i] for i, r in enumerate(resultado)) for c in columnas)
        dist[mejor] += p
    return dist


class TestMarcadores(unittest.TestCase):
    def test_matriz_suma_uno_y_factor_x_sube_empates(self):
        m = qc.matriz_marcadores(1.4, 1.1)
        self.assertAlmostEqual(sum(map(sum, m)), 1.0)
        px = qc.uno_x_dos(m)[1]
        px_inflado = qc.uno_x_dos(qc.matriz_marcadores(1.4, 1.1, factor_x=1.08))[1]
        self.assertGreater(px_inflado, px)

    def test_categorias_pleno_suman_uno(self):
        p = qc.categorias_pleno(qc.matriz_marcadores(2.0, 0.8))
        self.assertEqual(len(p), 16)
        self.assertAlmostEqual(sum(p.values()), 1.0)

    def test_conservador_sigue_el_signo_del_partido(self):
        p = qc.categorias_pleno(qc.matriz_marcadores(1.55, 1.05, 1.08))
        self.assertEqual(qc.tres_plenos(p, "1")["conservador"], "1-0")
        self.assertEqual(qc.tres_plenos(p, "2")["conservador"], "0-1")


class TestBoletos(unittest.TestCase):
    def test_reducida_garantiza_13(self):
        """Si aciertan los 7 sencillos y los 7 dobles cubren, alguna columna hace 13 o 14."""
        probs = _probs_aleatorias(1)
        dobles = [0, 2, 4, 6, 8, 10, 12]
        for clase in qc.CLASES:
            cols = qc.columnas_reducida(probs, dobles, clase)
            self.assertEqual(len(set(cols)), 16)
            for bits in itertools.product((0, 1), repeat=7):
                resultado = [qc.SIGNOS[qc._orden(p)[0]] for p in probs]
                for d, b in zip(dobles, bits):
                    resultado[d] = qc.SIGNOS[qc._orden(probs[d])[b]]
                mejor = max(sum(a == b for a, b in zip(resultado, c)) for c in cols)
                self.assertGreaterEqual(mejor, 13)

    def test_evaluacion_exacta_coincide_con_fuerza_bruta(self):
        probs = _probs_aleatorias(2, n=8)
        cols = ["11X21X12", "1XX21X12", "11X2112X", "21X21X12"]
        exacta = qc.evaluar_columnas(probs, cols)
        bruta = _fuerza_bruta(probs, cols)
        for a, b in zip(exacta, bruta):
            self.assertAlmostEqual(a, b)

    def test_p14_rapida_coincide_con_evaluacion_exacta(self):
        probs = _probs_aleatorias(3)
        dobles = [1, 3, 5, 7, 9, 11, 13]
        ps = qc._sencillos(probs, dobles)
        for clase in qc.CLASES:
            rapida = qc._p14_reducida(probs, dobles, clase, ps)
            exacta = qc.evaluar_columnas(probs, qc.columnas_reducida(probs, dobles, clase))[14]
            self.assertAlmostEqual(rapida, exacta)

    def test_vetos_siempre_van_a_doble(self):
        probs = _probs_aleatorias(4)
        probs[0] = [0.9, 0.07, 0.03]
        dobles, _ = qc.mejor_boleto_a(probs, [0])
        self.assertIn(0, dobles)
        dobles, _, _ = qc.mejor_boleto_b(probs, [0])
        self.assertIn(0, dobles)

    def test_demasiados_vetos_es_error(self):
        with self.assertRaises(ValueError):
            qc.mejor_boleto_a(_probs_aleatorias(5), [0, 1, 2, 3, 4])


class TestColumnasMasProbables(unittest.TestCase):
    def _p_columna(self, probs, col):
        p = 1.0
        for pr, s in zip(probs, col):
            p *= pr[qc.SIGNOS.index(s)]
        return p

    def test_p14_es_la_suma_de_las_columnas(self):
        probs = _probs_aleatorias(6)
        cols = qc.columnas_mas_probables(probs, 16)
        self.assertEqual(len(set(cols)), 16)
        exacta = qc.simular_columnas(probs, cols)[14]
        self.assertAlmostEqual(exacta, sum(self._p_columna(probs, c) for c in cols))

    def test_son_las_mas_probables_de_todas(self):
        probs = _probs_aleatorias(7, n=6)
        todas = sorted(("".join(c) for c in itertools.product(qc.SIGNOS, repeat=6)),
                       key=lambda c: -self._p_columna(probs, c))
        cols = qc.columnas_mas_probables(probs, 16)
        self.assertAlmostEqual(sum(self._p_columna(probs, c) for c in cols),
                               sum(self._p_columna(probs, c) for c in todas[:16]))

    def test_supera_a_los_otros_sistemas_en_p14(self):
        for semilla in range(8, 13):
            probs = _probs_aleatorias(semilla)
            sistemas, _ = qc.comparar_sistemas(probs, [])
            c = [s for s in sistemas if s["nombre"].startswith("C")][0]
            for s in sistemas:
                self.assertGreaterEqual(c["p14"] + 1e-12, s["p14"])

    def test_cumple_los_vetos(self):
        probs = _probs_aleatorias(14)
        probs[0] = [0.85, 0.10, 0.05]  # muy favorito: sin veto saldría siempre 1
        cols = qc.columnas_mas_probables(probs, 16, forzados=[0])
        self.assertGreaterEqual(len({c[0] for c in cols}), 2)
        self.assertEqual(len(set(cols)), 16)


class TestVariantesConEmpate(unittest.TestCase):
    def test_se_comparan_cuando_c_no_lleva_x(self):
        probs = [[0.50 - 0.01 * i, 0.20, 0.30 + 0.01 * i] for i in range(14)]
        sistemas, _ = qc.comparar_sistemas(probs, [0, 1])
        variantes = [s for s in sistemas if s["nombre"].startswith("C+X")]
        self.assertTrue(variantes)
        for s in variantes:
            self.assertTrue(any("X" in c for c in s["columnas"]))
            self.assertEqual(len(set(s["columnas"])), 16)
            for f in (0, 1):
                self.assertGreaterEqual(len({c[f] for c in s["columnas"]}), 2)


class TestSimulacion(unittest.TestCase):
    def test_simulacion_se_parece_a_la_exacta(self):
        probs = _probs_aleatorias(15)
        cols = qc.columnas_mas_probables(probs, 16)
        sim = qc.simular_columnas(probs, cols)
        exacta = qc.evaluar_columnas(probs, cols)
        self.assertAlmostEqual(sim[14], exacta[14])
        for k in (13, 12, 10):
            self.assertAlmostEqual(qc.al_menos(sim, k), qc.al_menos(exacta, k), delta=0.01)


class TestPostmortem(unittest.TestCase):
    def test_puntuacion_de_un_acierto_y_un_fallo(self):
        partidos = [{"partido": "A", "p": [0.5, 0.3, 0.2], "resultado": "1"},
                    {"partido": "B", "p": [0.5, 0.3, 0.2], "resultado": "2"}]
        r = qc.puntuar(partidos)
        self.assertAlmostEqual(r["log_loss"], -(qc.math.log(0.5) + qc.math.log(0.2)) / 2)
        self.assertAlmostEqual(r["brier"], ((0.25 + 0.09 + 0.04) + (0.25 + 0.09 + 0.64)) / 2)
        self.assertEqual(r["fallos_reales"], 1)
        self.assertAlmostEqual(r["fallos_esperados"], 1.0)


class TestComprobaciones(unittest.TestCase):
    def test_detecta_probabilidades_que_no_suman_uno(self):
        datos = {"partidos": [{"partido": f"P{i}", "p": [0.5, 0.3, 0.3]} for i in range(14)]}
        errores, _, _ = qc.comprobar(datos)
        self.assertTrue(errores)

    def test_detecta_partidos_repetidos(self):
        datos = {"partidos": [{"partido": "P", "p": [0.5, 0.3, 0.2]} for _ in range(14)]}
        errores, _, _ = qc.comprobar(datos)
        self.assertIn("Hay partidos repetidos.", errores)


if __name__ == "__main__":
    unittest.main()
