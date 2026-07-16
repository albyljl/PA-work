import unittest

from controlador.gerente_fluxo import GerenteFluxo
from modelo.formas import Elipse, FiguraComposta, Quadro


class TestCompositeControlador(unittest.TestCase):
    def test_agrupar_e_desagrupar_preserva_componentes(self):
        controlador = GerenteFluxo()
        retangulo = Quadro(0, 0, 10, 10, "black")
        elipse = Elipse(20, 20, 40, 40, "red")
        controlador.historico.extend([retangulo, elipse])
        controlador.selecionadas = [retangulo, elipse]
        retangulo.definir_selecionada(True)
        elipse.definir_selecionada(True)

        controlador.agrupar_selecionadas()

        self.assertEqual(len(controlador.historico), 1)
        grupo = controlador.historico[0]
        self.assertIsInstance(grupo, FiguraComposta)
        self.assertEqual(grupo.figuras, [retangulo, elipse])
        self.assertEqual(controlador.selecionadas, [grupo])

        controlador.desagrupar_selecionadas()

        self.assertEqual(controlador.historico, [retangulo, elipse])
        self.assertEqual(controlador.selecionadas, [retangulo, elipse])

    def test_grupo_funciona_com_operacoes_da_entrega_5(self):
        controlador = GerenteFluxo()
        retangulo = Quadro(0, 0, 10, 10, "black")
        elipse = Elipse(20, 20, 40, 40, "red")
        grupo = FiguraComposta([retangulo, elipse])
        grupo.definir_selecionada(True)
        controlador.historico.append(grupo)
        controlador.selecionadas = [grupo]

        grupo.mover(5, 5)
        controlador.copiar_selecionadas()
        controlador.colar_selecionadas()

        self.assertEqual(len(controlador.historico), 2)
        self.assertIsInstance(controlador.historico[1], FiguraComposta)
        self.assertEqual(controlador.historico[1].limites(), (25, 25, 65, 65))

        controlador.apagar_selecionadas()
        self.assertEqual(controlador.historico, [grupo])


if __name__ == "__main__":
    unittest.main()
