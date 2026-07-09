from abc import ABC, abstractmethod
import math


class TipoFormaDesconhecido(ValueError):
    pass

class FormaGeometrica(ABC):
    def __init__(self, tracejado, preenchimento="", largura=2):
        self.tracejado = tracejado
        self.preenchimento = preenchimento
        self.largura = largura

    @abstractmethod
    def renderizar(self, tela):
        pass

    @property
    @abstractmethod
    def tipo(self):
        pass

    @abstractmethod
    def mover(self, dx, dy):
        pass

    @abstractmethod
    def contem_ponto(self, x, y):
        pass

    def _atributos_estilo(self):
        return {
            "tracejado": self.tracejado,
            "preenchimento": self.preenchimento,
            "largura": self.largura,
        }

    @abstractmethod
    def para_dicionario(self):
        pass

    @classmethod
    def de_dicionario(cls, dados):
        tipo = dados.get("tipo")
        formas = {
            Traco.tipo: Traco,
            Raspador.tipo: Raspador,
            Quadro.tipo: Quadro,
            Elipse.tipo: Elipse,
            FormatoMultiplo.tipo: FormatoMultiplo,
        }
        try:
            forma_cls = formas[tipo]
        except KeyError as exc:
            raise TipoFormaDesconhecido(f"Tipo de forma desconhecido: {tipo}") from exc
        return forma_cls.de_dicionario(dados)


def _distancia_ponto_segmento(px, py, ax, ay, bx, by):
    dx = bx - ax
    dy = by - ay
    if dx == 0 and dy == 0:
        return math.hypot(px - ax, py - ay)

    t = ((px - ax) * dx + (py - ay) * dy) / (dx * dx + dy * dy)
    t = max(0, min(1, t))
    proj_x = ax + t * dx
    proj_y = ay + t * dy
    return math.hypot(px - proj_x, py - proj_y)


def _normalizar_retangulo(xa, ya, xb, yb):
    return min(xa, xb), min(ya, yb), max(xa, xb), max(ya, yb)


def _ponto_em_poligono(x, y, pontos):
    dentro = False
    total = len(pontos)
    j = total - 1
    for i in range(total):
        xi, yi = pontos[i]
        xj, yj = pontos[j]
        cruza = (yi > y) != (yj > y)
        if cruza:
            x_intersecao = (xj - xi) * (y - yi) / (yj - yi) + xi
            if x < x_intersecao:
                dentro = not dentro
        j = i
    return dentro

class Traco(FormaGeometrica):
    tipo = "traco"

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

    def mover(self, dx, dy):
        self.xa += dx
        self.ya += dy
        self.xb += dx
        self.yb += dy

    def contem_ponto(self, x, y):
        tolerancia = max(4, self.largura / 2)
        return _distancia_ponto_segmento(x, y, self.xa, self.ya, self.xb, self.yb) <= tolerancia

    def para_dicionario(self):
        dados = {
            "tipo": self.tipo,
            "xa": self.xa,
            "ya": self.ya,
            "xb": self.xb,
            "yb": self.yb,
        }
        dados.update(self._atributos_estilo())
        return dados

    @classmethod
    def de_dicionario(cls, dados):
        return cls(dados["xa"], dados["ya"], dados["xb"], dados["yb"], dados["tracejado"], dados.get("largura", 2))

class Raspador(FormaGeometrica):
    tipo = "raspador"

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

    def mover(self, dx, dy):
        self.xa += dx
        self.ya += dy
        self.xb += dx
        self.yb += dy

    def contem_ponto(self, x, y):
        return _distancia_ponto_segmento(x, y, self.xa, self.ya, self.xb, self.yb) <= self.largura / 2

    def para_dicionario(self):
        return {
            "tipo": self.tipo,
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
    tipo = "quadro"

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

    def mover(self, dx, dy):
        self.xa += dx
        self.ya += dy
        self.xb += dx
        self.yb += dy

    def contem_ponto(self, x, y):
        xa, ya, xb, yb = _normalizar_retangulo(self.xa, self.ya, self.xb, self.yb)
        return xa <= x <= xb and ya <= y <= yb

    def para_dicionario(self):
        dados = {
            "tipo": self.tipo,
            "xa": self.xa,
            "ya": self.ya,
            "xb": self.xb,
            "yb": self.yb,
        }
        dados.update(self._atributos_estilo())
        return dados

    @classmethod
    def de_dicionario(cls, dados):
        return cls(
            dados["xa"],
            dados["ya"],
            dados["xb"],
            dados["yb"],
            dados["tracejado"],
            dados.get("preenchimento", ""),
            dados.get("largura", 2),
        )

class Elipse(FormaGeometrica):
    tipo = "elipse"

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

    def mover(self, dx, dy):
        self.xa += dx
        self.ya += dy
        self.xb += dx
        self.yb += dy

    def contem_ponto(self, x, y):
        xa, ya, xb, yb = _normalizar_retangulo(self.xa, self.ya, self.xb, self.yb)
        raio_x = (xb - xa) / 2
        raio_y = (yb - ya) / 2
        if raio_x == 0 or raio_y == 0:
            return False
        centro_x = xa + raio_x
        centro_y = ya + raio_y
        return ((x - centro_x) ** 2) / (raio_x ** 2) + ((y - centro_y) ** 2) / (raio_y ** 2) <= 1

    def para_dicionario(self):
        dados = {
            "tipo": self.tipo,
            "xa": self.xa,
            "ya": self.ya,
            "xb": self.xb,
            "yb": self.yb,
        }
        dados.update(self._atributos_estilo())
        return dados

    @classmethod
    def de_dicionario(cls, dados):
        return cls(
            dados["xa"],
            dados["ya"],
            dados["xb"],
            dados["yb"],
            dados["tracejado"],
            dados.get("preenchimento", ""),
            dados.get("largura", 2),
        )

class FormatoMultiplo(FormaGeometrica):
    tipo = "formato_multiplo"

    def __init__(self, vertices, tracejado, preenchimento="", largura=2):
        super().__init__(tracejado, preenchimento, largura)
        self.vertices = [tuple(vertice) for vertice in vertices]

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

    def mover(self, dx, dy):
        self.vertices = [(x + dx, y + dy) for x, y in self.vertices]

    def contem_ponto(self, x, y):
        if len(self.vertices) < 3:
            return False
        return _ponto_em_poligono(x, y, self.vertices)

    def para_dicionario(self):
        dados = {
            "tipo": self.tipo,
            "vertices": [list(vertice) for vertice in self.vertices],
        }
        dados.update(self._atributos_estilo())
        return dados

    @classmethod
    def de_dicionario(cls, dados):
        return cls(
            dados["vertices"],
            dados["tracejado"],
            dados.get("preenchimento", ""),
            dados.get("largura", 2),
        )
