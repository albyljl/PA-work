import json

from modelo.formas import FormaGeometrica


class DocumentoDesenho:
    def __init__(self, figuras=None):
        self.figuras = list(figuras or [])

    def adicionar(self, figura):
        self.figuras.append(figura)

    def limpar(self):
        self.figuras.clear()

    def para_dicionario(self):
        return {
            "versao": 1,
            "figuras": [figura.para_dicionario() for figura in self.figuras],
        }

    @classmethod
    def de_dicionario(cls, dados):
        figuras = [
            FormaGeometrica.de_dicionario(figura)
            for figura in dados.get("figuras", [])
        ]
        return cls(figuras)

    def salvar(self, caminho):
        with open(caminho, "w", encoding="utf-8") as arquivo:
            json.dump(self.para_dicionario(), arquivo, ensure_ascii=False, indent=2)

    @classmethod
    def abrir(cls, caminho):
        with open(caminho, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
        return cls.de_dicionario(dados)
