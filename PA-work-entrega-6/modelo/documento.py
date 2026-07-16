import json
from pathlib import Path

from modelo.formas import FormaGeometrica


class DocumentoDesenho:
    def __init__(self, figuras=None):
        self.figuras = list(figuras or [])

    def adicionar(self, figura: FormaGeometrica) -> None:
        self.figuras.append(figura)

    def limpar(self) -> None:
        self.figuras.clear()

    def para_dicionario(self):
        return {
            "versao": 2,
            "figuras": [figura.para_dicionario() for figura in self.figuras],
        }

    @classmethod
    def de_dicionario(cls, dados):
        # Também aceita a lista usada pela versão anterior do controlador.
        if isinstance(dados, list):
            itens = dados
        else:
            itens = dados.get("figuras", [])
        return cls([FormaGeometrica.de_dicionario(item) for item in itens])

    def salvar(self, caminho) -> None:
        with Path(caminho).open("w", encoding="utf-8") as arquivo:
            json.dump(self.para_dicionario(), arquivo, ensure_ascii=False, indent=2)

    @classmethod
    def abrir(cls, caminho):
        with Path(caminho).open("r", encoding="utf-8") as arquivo:
            return cls.de_dicionario(json.load(arquivo))
