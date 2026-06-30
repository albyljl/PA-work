from abc import ABC, abstractmethod


class Figura(ABC):
    def __init__(self, cor_borda, cor_preenchimento="", espessura=2):
        self.cor_borda = cor_borda
        self.cor_preenchimento = cor_preenchimento
        self.espessura = espessura

    @abstractmethod
    def desenhar(self, canvas):
        pass


class Linha(Figura):
    def __init__(self, x1, y1, x2, y2, cor_borda, espessura=2):
        super().__init__(cor_borda, "", espessura)
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def desenhar(self, canvas):
        canvas.create_line(
            self.x1, self.y1, self.x2, self.y2,
            fill=self.cor_borda,
            width=self.espessura,
            capstyle="round",
            joinstyle="round"
        )


class Borracha(Figura):
    def __init__(self, x1, y1, x2, y2, espessura=10):
        super().__init__("white", "", espessura)
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def desenhar(self, canvas):
        canvas.create_line(
            self.x1,
            self.y1,
            self.x2,
            self.y2,
            fill=self.cor_borda,
            width=self.espessura,
            capstyle="round",
            joinstyle="round"
        )


class Retangulo(Figura):
    def __init__(self, x1, y1, x2, y2, cor_borda, cor_preenchimento="", espessura=2):
        super().__init__(cor_borda, cor_preenchimento, espessura)
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def desenhar(self, canvas):
        canvas.create_rectangle(
            self.x1, self.y1, self.x2, self.y2,
            outline=self.cor_borda,
            fill=self.cor_preenchimento,
            width=self.espessura
        )


class Oval(Figura):
    def __init__(self, x1, y1, x2, y2, cor_borda, cor_preenchimento="", espessura=2):
        super().__init__(cor_borda, cor_preenchimento, espessura)
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def desenhar(self, canvas):
        canvas.create_oval(
            self.x1, self.y1, self.x2, self.y2,
            outline=self.cor_borda,
            fill=self.cor_preenchimento,
            width=self.espessura
        )


class Poligono(Figura):
    def __init__(self, pontos, cor_borda, cor_preenchimento="", espessura=2):
        super().__init__(cor_borda, cor_preenchimento, espessura)
        self.pontos = pontos

    def desenhar(self, canvas):
        coordenadas = []

        for x, y in self.pontos:
            coordenadas.append(x)
            coordenadas.append(y)

        canvas.create_polygon(
            coordenadas,
            outline=self.cor_borda,
            fill=self.cor_preenchimento,
            width=self.espessura
        )