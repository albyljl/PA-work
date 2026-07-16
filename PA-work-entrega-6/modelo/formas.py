from __future__ import annotations

from abc import ABC, abstractmethod
from math import hypot
from typing import Any


class TipoFormaDesconhecido(ValueError):
    pass


class FormaGeometrica(ABC):
    """Contrato comum das figuras simples e compostas."""

    def __init__(self, tracejado: str, preenchimento: str = "", largura: int = 2):
        self.tracejado = tracejado
        self.preenchimento = preenchimento
        self.largura = largura
        self.selecionada = False

    @abstractmethod
    def renderizar(self, tela) -> None:
        pass

    @abstractmethod
    def contem_ponto(self, x: float, y: float) -> bool:
        pass

    @abstractmethod
    def mover(self, dx: float, dy: float) -> None:
        pass

    @abstractmethod
    def limites(self) -> tuple[float, float, float, float]:
        """Retorna xmin, ymin, xmax e ymax."""
        pass

    @abstractmethod
    def para_dicionario(self) -> dict[str, Any]:
        pass

    def definir_selecionada(self, valor: bool) -> None:
        self.selecionada = valor

    def definir_cor_contorno(self, cor: str) -> None:
        self.tracejado = cor

    def definir_cor_preenchimento(self, cor: str) -> None:
        self.preenchimento = cor

    def definir_largura(self, largura: int) -> None:
        self.largura = largura

    def _estilo_selecao(self) -> tuple[str, int]:
        if self.selecionada:
            return "blue", self.largura + 2
        return self.tracejado, self.largura

    @classmethod
    def de_dicionario(cls, dados: dict[str, Any]) -> FormaGeometrica:
        tipo = dados.get("tipo")
        construtores = {
            "Traco": Traco.de_dicionario,
            "Raspador": Raspador.de_dicionario,
            "Quadro": Quadro.de_dicionario,
            "Elipse": Elipse.de_dicionario,
            "FormatoMultiplo": FormatoMultiplo.de_dicionario,
            "FiguraComposta": FiguraComposta.de_dicionario,
        }
        try:
            return construtores[tipo](dados)
        except KeyError as erro:
            raise TipoFormaDesconhecido(f"Tipo de figura desconhecido: {tipo!r}") from erro


class Traco(FormaGeometrica):
    def __init__(self, xa, ya, xb, yb, tracejado, largura=2):
        super().__init__(tracejado, "", largura)
        self.xa, self.ya = xa, ya
        self.xb, self.yb = xb, yb

    def renderizar(self, tela) -> None:
        cor, largura = self._estilo_selecao()
        tela.create_line(
            self.xa,
            self.ya,
            self.xb,
            self.yb,
            fill=cor,
            width=largura,
            capstyle="round",
            joinstyle="round",
        )

    def contem_ponto(self, x, y) -> bool:
        margem = max(5, self.largura / 2 + 2)
        dx = self.xb - self.xa
        dy = self.yb - self.ya
        comprimento_quadrado = dx * dx + dy * dy
        if comprimento_quadrado == 0:
            return hypot(x - self.xa, y - self.ya) <= margem

        t = ((x - self.xa) * dx + (y - self.ya) * dy) / comprimento_quadrado
        t = max(0.0, min(1.0, t))
        px = self.xa + t * dx
        py = self.ya + t * dy
        return hypot(x - px, y - py) <= margem

    def mover(self, dx, dy) -> None:
        self.xa += dx
        self.ya += dy
        self.xb += dx
        self.yb += dy

    def limites(self):
        return min(self.xa, self.xb), min(self.ya, self.yb), max(self.xa, self.xb), max(self.ya, self.yb)

    def definir_cor_preenchimento(self, cor: str) -> None:
        # Linhas não possuem preenchimento.
        pass

    def para_dicionario(self):
        return {
            "tipo": "Traco",
            "xa": self.xa,
            "ya": self.ya,
            "xb": self.xb,
            "yb": self.yb,
            "tracejado": self.tracejado,
            "largura": self.largura,
        }

    @classmethod
    def de_dicionario(cls, dados):
        return cls(
            dados["xa"], dados["ya"], dados["xb"], dados["yb"],
            dados.get("tracejado", "black"), dados.get("largura", 2),
        )


class Raspador(Traco):
    def __init__(self, xa, ya, xb, yb, largura=10):
        super().__init__(xa, ya, xb, yb, "white", largura)

    def renderizar(self, tela) -> None:
        tela.create_line(
            self.xa,
            self.ya,
            self.xb,
            self.yb,
            fill="blue" if self.selecionada else "white",
            width=self.largura + 2 if self.selecionada else self.largura,
            capstyle="round",
            joinstyle="round",
        )

    def contem_ponto(self, x, y) -> bool:
        return super().contem_ponto(x, y)

    def definir_cor_contorno(self, cor: str) -> None:
        pass

    def para_dicionario(self):
        return {
            "tipo": "Raspador",
            "xa": self.xa,
            "ya": self.ya,
            "xb": self.xb,
            "yb": self.yb,
            "largura": self.largura,
        }

    @classmethod
    def de_dicionario(cls, dados):
        return cls(dados["xa"], dados["ya"], dados["xb"], dados["yb"], dados.get("largura", 10))


class Quadro(FormaGeometrica):
    def __init__(self, xa, ya, xb, yb, tracejado, preenchimento="", largura=2):
        super().__init__(tracejado, preenchimento, largura)
        self.xa, self.ya = xa, ya
        self.xb, self.yb = xb, yb

    def renderizar(self, tela) -> None:
        cor, largura = self._estilo_selecao()
        tela.create_rectangle(
            self.xa,
            self.ya,
            self.xb,
            self.yb,
            outline=cor,
            fill=self.preenchimento,
            width=largura,
        )

    def contem_ponto(self, x, y) -> bool:
        xmin, ymin, xmax, ymax = self.limites()
        return xmin <= x <= xmax and ymin <= y <= ymax

    def mover(self, dx, dy) -> None:
        self.xa += dx
        self.ya += dy
        self.xb += dx
        self.yb += dy

    def limites(self):
        return min(self.xa, self.xb), min(self.ya, self.yb), max(self.xa, self.xb), max(self.ya, self.yb)

    def para_dicionario(self):
        return {
            "tipo": "Quadro",
            "xa": self.xa,
            "ya": self.ya,
            "xb": self.xb,
            "yb": self.yb,
            "tracejado": self.tracejado,
            "preenchimento": self.preenchimento,
            "largura": self.largura,
        }

    @classmethod
    def de_dicionario(cls, dados):
        return cls(
            dados["xa"], dados["ya"], dados["xb"], dados["yb"],
            dados.get("tracejado", "black"), dados.get("preenchimento", ""),
            dados.get("largura", 2),
        )


class Elipse(Quadro):
    def renderizar(self, tela) -> None:
        cor, largura = self._estilo_selecao()
        tela.create_oval(
            self.xa,
            self.ya,
            self.xb,
            self.yb,
            outline=cor,
            fill=self.preenchimento,
            width=largura,
        )

    def contem_ponto(self, x, y) -> bool:
        xmin, ymin, xmax, ymax = self.limites()
        rx = (xmax - xmin) / 2
        ry = (ymax - ymin) / 2
        if rx == 0 or ry == 0:
            return False
        cx = (xmin + xmax) / 2
        cy = (ymin + ymax) / 2
        return ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1

    def para_dicionario(self):
        dados = super().para_dicionario()
        dados["tipo"] = "Elipse"
        return dados

    @classmethod
    def de_dicionario(cls, dados):
        return cls(
            dados["xa"], dados["ya"], dados["xb"], dados["yb"],
            dados.get("tracejado", "black"), dados.get("preenchimento", ""),
            dados.get("largura", 2),
        )


class FormatoMultiplo(FormaGeometrica):
    def __init__(self, vertices, tracejado, preenchimento="", largura=2):
        super().__init__(tracejado, preenchimento, largura)
        self.vertices = [tuple(ponto) for ponto in vertices]

    def renderizar(self, tela) -> None:
        if not self.vertices:
            return
        cor, largura = self._estilo_selecao()
        pontos = [coordenada for vertice in self.vertices for coordenada in vertice]
        tela.create_polygon(
            pontos,
            outline=cor,
            fill=self.preenchimento,
            width=largura,
        )

    def contem_ponto(self, x, y) -> bool:
        # Algoritmo ray casting para ponto dentro do polígono.
        dentro = False
        quantidade = len(self.vertices)
        if quantidade < 3:
            return False
        j = quantidade - 1
        for i in range(quantidade):
            xi, yi = self.vertices[i]
            xj, yj = self.vertices[j]
            cruza = (yi > y) != (yj > y)
            if cruza:
                x_intersecao = (xj - xi) * (y - yi) / (yj - yi) + xi
                if x < x_intersecao:
                    dentro = not dentro
            j = i
        return dentro

    def mover(self, dx, dy) -> None:
        self.vertices = [(x + dx, y + dy) for x, y in self.vertices]

    def limites(self):
        if not self.vertices:
            return 0, 0, 0, 0
        xs = [x for x, _ in self.vertices]
        ys = [y for _, y in self.vertices]
        return min(xs), min(ys), max(xs), max(ys)

    def para_dicionario(self):
        return {
            "tipo": "FormatoMultiplo",
            "vertices": [list(ponto) for ponto in self.vertices],
            "tracejado": self.tracejado,
            "preenchimento": self.preenchimento,
            "largura": self.largura,
        }

    @classmethod
    def de_dicionario(cls, dados):
        return cls(
            dados.get("vertices", []), dados.get("tracejado", "black"),
            dados.get("preenchimento", ""), dados.get("largura", 2),
        )


class FiguraComposta(FormaGeometrica):
    """Composite: contém figuras, mas pode ser tratada como uma única figura."""

    def __init__(self, figuras: list[FormaGeometrica]):
        if not figuras:
            raise ValueError("Uma figura composta precisa conter pelo menos uma figura.")
        super().__init__("black", "", 2)
        self.figuras = list(figuras)
        for figura in self.figuras:
            figura.definir_selecionada(False)

    def renderizar(self, tela) -> None:
        for figura in self.figuras:
            estado_anterior = figura.selecionada
            figura.definir_selecionada(False)
            figura.renderizar(tela)
            figura.definir_selecionada(estado_anterior)

        if self.selecionada:
            xmin, ymin, xmax, ymax = self.limites()
            tela.create_rectangle(
                xmin - 4,
                ymin - 4,
                xmax + 4,
                ymax + 4,
                outline="blue",
                width=2,
                dash=(5, 3),
            )

    def contem_ponto(self, x, y) -> bool:
        return any(figura.contem_ponto(x, y) for figura in reversed(self.figuras))

    def mover(self, dx, dy) -> None:
        for figura in self.figuras:
            figura.mover(dx, dy)

    def limites(self):
        limites = [figura.limites() for figura in self.figuras]
        return (
            min(limite[0] for limite in limites),
            min(limite[1] for limite in limites),
            max(limite[2] for limite in limites),
            max(limite[3] for limite in limites),
        )

    def definir_cor_contorno(self, cor: str) -> None:
        for figura in self.figuras:
            figura.definir_cor_contorno(cor)

    def definir_cor_preenchimento(self, cor: str) -> None:
        for figura in self.figuras:
            figura.definir_cor_preenchimento(cor)

    def definir_largura(self, largura: int) -> None:
        for figura in self.figuras:
            figura.definir_largura(largura)

    def para_dicionario(self):
        return {
            "tipo": "FiguraComposta",
            "figuras": [figura.para_dicionario() for figura in self.figuras],
        }

    @classmethod
    def de_dicionario(cls, dados):
        figuras = [FormaGeometrica.de_dicionario(item) for item in dados.get("figuras", [])]
        return cls(figuras)
