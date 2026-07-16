from abc import ABC, abstractmethod

class FormaGeometrica(ABC):
    def __init__(self, tracejado, preenchimento="", largura=2):
        self.tracejado = tracejado
        self.preenchimento = preenchimento
        self.largura = largura
        self.selecionada = False

    @abstractmethod
    def renderizar(self, tela):
        pass

    @abstractmethod
    def contem_ponto(self, x, y):
        pass

    @abstractmethod
    def mover(self, dx, dy):
        pass

class Traco(FormaGeometrica):
    def __init__(self, xa, ya, xb, yb, tracejado, largura=2):
        super().__init__(tracejado, "", largura)
        self.xa = xa
        self.ya = ya
        self.xb = xb
        self.yb = yb

    def renderizar(self, tela):
        cor = "blue" if self.selecionada else self.tracejado
        larg = self.largura + 2 if self.selecionada else self.largura
        tela.create_line(
            self.xa, self.ya, self.xb, self.yb,
            fill=cor,
            width=larg,
            capstyle="round",
            joinstyle="round"
        )

    def contem_ponto(self, x, y):
        margem = 5
        xmin, xmax = min(self.xa, self.xb) - margem, max(self.xa, self.xb) + margem
        ymin, ymax = min(self.ya, self.yb) - margem, max(self.ya, self.yb) + margem
        if not (xmin <= x <= xmax and ymin <= y <= ymax):
            return False
        dist = abs((self.yb - self.ya) * x - (self.xb - self.xa) * y + self.xb * self.ya - self.yb * self.xa) / (
            ((self.yb - self.ya) ** 2 + (self.xb - self.xa) ** 2) ** 0.5 or 1
        )
        return dist <= margem

    def mover(self, dx, dy):
        self.xa += dx
        self.ya += dy
        self.xb += dx
        self.yb += dy

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
            fill="white",
            width=self.largura,
            capstyle="round",
            joinstyle="round"
        )

    def contem_ponto(self, x, y):
        return False

    def mover(self, dx, dy):
        self.xa += dx
        self.ya += dy
        self.xb += dx
        self.yb += dy

class Quadro(FormaGeometrica):
    def __init__(self, xa, ya, xb, yb, tracejado, preenchimento="", largura=2):
        super().__init__(tracejado, preenchimento, largura)
        self.xa = xa
        self.ya = ya
        self.xb = xb
        self.yb = yb

    def renderizar(self, tela):
        cor_borda = "blue" if self.selecionada else self.tracejado
        larg = self.largura + 2 if self.selecionada else self.largura
        tela.create_rectangle(
            self.xa, self.ya, self.xb, self.yb,
            outline=cor_borda,
            fill=self.preenchimento,
            width=larg
        )

    def contem_ponto(self, x, y):
        xmin, xmax = min(self.xa, self.xb), max(self.xa, self.xb)
        ymin, ymax = min(self.ya, self.yb), max(self.ya, self.yb)
        return xmin <= x <= xmax and ymin <= y <= ymax

    def mover(self, dx, dy):
        self.xa += dx
        self.ya += dy
        self.xb += dx
        self.yb += dy

class Elipse(FormaGeometrica):
    def __init__(self, xa, ya, xb, yb, tracejado, preenchimento="", largura=2):
        super().__init__(tracejado, preenchimento, largura)
        self.xa = xa
        self.ya = ya
        self.xb = xb
        self.yb = yb

    def renderizar(self, tela):
        cor_borda = "blue" if self.selecionada else self.tracejado
        larg = self.largura + 2 if self.selecionada else self.largura
        tela.create_oval(
            self.xa, self.ya, self.xb, self.yb,
            outline=cor_borda,
            fill=self.preenchimento,
            width=larg
        )

    def contem_ponto(self, x, y):
        xmin, xmax = min(self.xa, self.xb), max(self.xa, self.xb)
        ymin, ymax = min(self.ya, self.yb), max(self.ya, self.yb)
        return xmin <= x <= xmax and ymin <= y <= ymax

    def mover(self, dx, dy):
        self.xa += dx
        self.ya += dy
        self.xb += dx
        self.yb += dy

class FormatoMultiplo(FormaGeometrica):
    def __init__(self, vertices, tracejado, preenchimento="", largura=2):
        super().__init__(tracejado, preenchimento, largura)
        self.vertices = vertices

    def renderizar(self, tela):
        cor_borda = "blue" if self.selecionada else self.tracejado
        larg = self.largura + 2 if self.selecionada else self.largura
        pontos = []
        for px, py in self.vertices:
            pontos.append(px)
            pontos.append(py)

        tela.create_polygon(
            pontos,
            outline=cor_borda,
            fill=self.preenchimento,
            width=larg
        )

    def contem_ponto(self, x, y):
        if not self.vertices:
            return False
        xs = [p[0] for p in self.vertices]
        ys = [p[1] for p in self.vertices]
        return min(xs) <= x <= max(xs) and min(ys) <= y <= max(ys)

    def mover(self, dx, dy):
        self.vertices = [(px + dx, py + dy) for px, py in self.vertices]