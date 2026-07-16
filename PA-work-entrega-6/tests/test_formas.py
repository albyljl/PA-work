import unittest

from modelo.formas import (
    Elipse,
    FiguraComposta,
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

    def test_composta_move_todos_componentes(self):
        retangulo = Quadro(0, 0, 10, 10, "black")
        elipse = Elipse(20, 20, 40, 40, "red")
        grupo = FiguraComposta([retangulo, elipse])

        grupo.mover(5, -2)

        self.assertEqual(retangulo.limites(), (5, -2, 15, 8))
        self.assertEqual(elipse.limites(), (25, 18, 45, 38))
        self.assertEqual(grupo.limites(), (5, -2, 45, 38))

    def test_composta_detecta_clique_nos_componentes(self):
        grupo = FiguraComposta([
            Quadro(0, 0, 10, 10, "black"),
            Elipse(20, 20, 40, 40, "red"),
        ])
        self.assertTrue(grupo.contem_ponto(5, 5))
        self.assertTrue(grupo.contem_ponto(30, 30))
        self.assertFalse(grupo.contem_ponto(15, 15))

    def test_composta_propaga_estilo(self):
        retangulo = Quadro(0, 0, 10, 10, "black", "white", 2)
        elipse = Elipse(20, 20, 40, 40, "red", "yellow", 3)
        grupo = FiguraComposta([retangulo, elipse])

        grupo.definir_cor_contorno("purple")
        grupo.definir_cor_preenchimento("pink")
        grupo.definir_largura(7)

        for figura in grupo.figuras:
            self.assertEqual(figura.tracejado, "purple")
            self.assertEqual(figura.preenchimento, "pink")
            self.assertEqual(figura.largura, 7)

    def test_composta_round_trip_recursivo(self):
        grupo = FiguraComposta([
            Quadro(0, 0, 10, 10, "black", "white", 2),
            FiguraComposta([
                Traco(20, 20, 30, 30, "red", 3),
                Elipse(40, 40, 60, 60, "blue", "yellow", 4),
            ]),
        ])
        dados = grupo.para_dicionario()
        restaurada = FormaGeometrica.de_dicionario(dados)
        self.assertIsInstance(restaurada, FiguraComposta)
        self.assertEqual(restaurada.para_dicionario(), dados)


if __name__ == "__main__":
    unittest.main()
