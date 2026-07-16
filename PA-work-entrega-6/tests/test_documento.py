import tempfile
import unittest
from pathlib import Path

from modelo.documento import DocumentoDesenho
from modelo.formas import Elipse, FiguraComposta, FormatoMultiplo, Quadro, Traco


class TestDocumentoDesenho(unittest.TestCase):
    def test_documento_round_trip_dicionario(self):
        documento = DocumentoDesenho([
            Traco(0, 0, 10, 10, "black", 2),
            Quadro(5, 5, 30, 40, "red", "blue", 3),
            Elipse(10, 10, 20, 30, "green", "", 4),
            FormatoMultiplo([(0, 0), (10, 0), (5, 10)], "purple", "yellow", 2),
        ])
        restaurado = DocumentoDesenho.de_dicionario(documento.para_dicionario())
        self.assertEqual(restaurado.para_dicionario(), documento.para_dicionario())

    def test_documento_salvar_e_abrir(self):
        with tempfile.TemporaryDirectory() as pasta:
            caminho = Path(pasta) / "desenho.json"
            documento = DocumentoDesenho([Quadro(1, 2, 3, 4, "red", "", 2)])
            documento.salvar(caminho)
            restaurado = DocumentoDesenho.abrir(caminho)
            self.assertEqual(restaurado.para_dicionario(), documento.para_dicionario())

    def test_documento_salva_figura_composta(self):
        with tempfile.TemporaryDirectory() as pasta:
            caminho = Path(pasta) / "grupo.json"
            grupo = FiguraComposta([
                Quadro(1, 2, 30, 40, "red", "blue", 2),
                Elipse(50, 60, 80, 90, "black", "yellow", 3),
            ])
            documento = DocumentoDesenho([grupo])
            documento.salvar(caminho)
            restaurado = DocumentoDesenho.abrir(caminho)

            self.assertIsInstance(restaurado.figuras[0], FiguraComposta)
            self.assertEqual(restaurado.para_dicionario(), documento.para_dicionario())


if __name__ == "__main__":
    unittest.main()
