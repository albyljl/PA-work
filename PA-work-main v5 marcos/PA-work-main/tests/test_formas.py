import unittest

from modelo.formas import (
    Elipse,
    FormaGeometrica,
    FormatoMultiplo,
    Quadro,
    Raspador,
    TipoFormaDesconhecido,
    Traco,
)


class TestFormas(unittest.TestCase):
    def test_figuras_detectam_clique(self):
        casos = [
            (Traco(0, 0, 10, 0, "black", 2), (5, 1), (5, 8)),
            (Raspador(0, 0, 10, 0, 10), (5, 4), (5, 8)),
            (Quadro(10, 10, 30, 30, "red", "blue", 3), (20, 20), (35, 20)),
            (Elipse(10, 10, 30, 30, "red", "", 3), (20, 20), (31, 20)),
            (FormatoMultiplo([(0, 0), (20, 0), (10, 20)], "green", "", 2), (10, 10), (30, 10)),
        ]

        for figura, ponto_dentro, ponto_fora in casos:
            with self.subTest(figura=type(figura).__name__):
                self.assertTrue(figura.contem_ponto(*ponto_dentro))
                self.assertFalse(figura.contem_ponto(*ponto_fora))

    def test_figuras_movem_coordenadas(self):
        figuras = [
            Traco(0, 0, 10, 10, "black", 2),
            Raspador(0, 0, 10, 10, 10),
            Quadro(0, 0, 10, 10, "black", "", 2),
            Elipse(0, 0, 10, 10, "black", "", 2),
        ]

        for figura in figuras:
            with self.subTest(figura=type(figura).__name__):
                figura.mover(3, 4)
                self.assertEqual(figura.xa, 3)
                self.assertEqual(figura.ya, 4)

    def test_poligono_move_vertices(self):
        poligono = FormatoMultiplo([(0, 0), (10, 0), (5, 5)], "black")
        poligono.mover(2, 3)

        self.assertEqual(poligono.vertices, [(2, 3), (12, 3), (7, 8)])

    def test_round_trip_dicionario(self):
        figuras = [
            Traco(1, 2, 3, 4, "black", 2),
            Raspador(1, 2, 3, 4, 10),
            Quadro(1, 2, 3, 4, "red", "yellow", 5),
            Elipse(1, 2, 3, 4, "blue", "", 6),
            FormatoMultiplo([(1, 2), (3, 4), (5, 6)], "green", "pink", 2),
        ]

        for figura in figuras:
            with self.subTest(figura=type(figura).__name__):
                dados = figura.para_dicionario()
                restaurada = FormaGeometrica.de_dicionario(dados)
                self.assertIs(type(restaurada), type(figura))
                self.assertEqual(restaurada.para_dicionario(), dados)

    def test_tipo_desconhecido_falha_com_erro_claro(self):
        with self.assertRaises(TipoFormaDesconhecido):
            FormaGeometrica.de_dicionario({"tipo": "estrela"})


if __name__ == "__main__":
    unittest.main()
