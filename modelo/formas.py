from abc import ABC, abstractmethod

class FormaGeometrica(ABC):
    def __init__(self, tracejado, preenchimento="", largura=2):
        self.tracejado = tracejado
        self.preenchimento = preenchimento
        self.largura = largura

    @abstractmethod
    def renderizar(self, tela):
        pass

class Traco(FormaGeometrica):
    def __init__(self, xa, ya, xb, yb, tracejado, largura=2):
        super().__init__(tracejado, "", largura)
        self.xa = xa
        self.ya = ya
        self.xb = xb
        self.yb = yb

    def renderizar(self, tela):
        tela.create_line(
            self.xa, self.ya, self.xb, self.yb,
            fill=self.tracejado,
            width=self.largura,
            capstyle="round",
            joinstyle="round"
        )

class Raspador(FormaGeometrica):
    def __init__(self, xa, ya, xb, yb, largura=10):
        super().__init__("white", "", largura)
        self.xa = xa
        self.ya = ya
        self.xb = xb
        self.yb = yb

    def renderizar(self, tela):
        tela.create_line(
            self.xa, self.ya, self.xb, self.yb,
            fill=self.tracejado,
            width=self.largura,
            capstyle="round",
            joinstyle="round"
        )

class Quadro(FormaGeometrica):
    def __init__(self, xa, ya, xb, yb, tracejado, preenchimento="", largura=2):
        super().__init__(tracejado, preenchimento, largura)
        self.xa = xa
        self.ya = ya
        self.xb = xb
        self.yb = yb

    def renderizar(self, tela):
        tela.create_rectangle(
            self.xa, self.ya, self.xb, self.yb,
            outline=self.tracejado,
            fill=self.preenchimento,
            width=self.largura
        )

class Elipse(FormaGeometrica):
    def __init__(self, xa, ya, xb, yb, tracejado, preenchimento="", largura=2):
        super().__init__(tracejado, preenchimento, largura)
        self.xa = xa
        self.ya = ya
        self.xb = xb
        self.yb = yb

    def renderizar(self, tela):
        tela.create_oval(
            self.xa, self.ya, self.xb, self.yb,
            outline=self.tracejado,
            fill=self.preenchimento,
            width=self.largura
        )

class FormatoMultiplo(FormaGeometrica):
    def __init__(self, vertices, tracejado, preenchimento="", largura=2):
        super().__init__(tracejado, preenchimento, largura)
        self.vertices = vertices

    def renderizar(self, tela):
        pontos = []
        for px, py in self.vertices:
            pontos.append(px)
            pontos.append(py)

        tela.create_polygon(
            pontos,
            outline=self.tracejado,
            fill=self.preenchimento,
            width=self.largura
        )