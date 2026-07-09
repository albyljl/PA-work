from abc import ABC
from tkinter import messagebox

from modelo.formas import Traco, Quadro, Elipse, FormatoMultiplo, Raspador


class EstadoFerramenta(ABC):
    chave = ""

    def __init__(self, controlador):
        self.controlador = controlador

    @property
    def tela(self):
        return self.controlador.janela_view.quadro_desenho

    def ao_entrar(self):
        pass

    def ao_sair(self):
        pass

    def iniciar_clique(self, event):
        self.controlador.x_start = event.x
        self.controlador.y_start = event.y
        self.controlador.objeto_guia = None

    def arrastar_mouse(self, event):
        pass

    def soltar_mouse(self, event):
        self.controlador.objeto_guia = None


class EstadoLivre(EstadoFerramenta):
    chave = "livre"

    def arrastar_mouse(self, event):
        figura = Traco(
            self.controlador.x_start,
            self.controlador.y_start,
            event.x,
            event.y,
            self.controlador.cor_linha,
            self.controlador.grossura,
        )
        self.controlador.adicionar_figura(figura)
        self.controlador.x_start = event.x
        self.controlador.y_start = event.y


class EstadoBorracha(EstadoFerramenta):
    chave = "borracha"

    def arrastar_mouse(self, event):
        figura = Raspador(
            self.controlador.x_start,
            self.controlador.y_start,
            event.x,
            event.y,
            self.controlador.grossura * 2,
        )
        self.controlador.adicionar_figura(figura)
        self.controlador.x_start = event.x
        self.controlador.y_start = event.y


class EstadoRetangulo(EstadoFerramenta):
    chave = "retangulo"

    def arrastar_mouse(self, event):
        self.controlador.apagar_guia()
        self.controlador.objeto_guia = self.tela.create_rectangle(
            self.controlador.x_start,
            self.controlador.y_start,
            event.x,
            event.y,
            outline=self.controlador.cor_linha,
            fill=self.controlador.cor_interna,
            width=self.controlador.grossura,
        )

    def soltar_mouse(self, event):
        if self.controlador.objeto_guia:
            self.controlador.apagar_guia()
            figura = Quadro(
                self.controlador.x_start,
                self.controlador.y_start,
                event.x,
                event.y,
                self.controlador.cor_linha,
                self.controlador.cor_interna,
                self.controlador.grossura,
            )
            self.controlador.adicionar_figura(figura)
        super().soltar_mouse(event)


class EstadoOval(EstadoFerramenta):
    chave = "oval"

    def arrastar_mouse(self, event):
        self.controlador.apagar_guia()
        self.controlador.objeto_guia = self.tela.create_oval(
            self.controlador.x_start,
            self.controlador.y_start,
            event.x,
            event.y,
            outline=self.controlador.cor_linha,
            fill=self.controlador.cor_interna,
            width=self.controlador.grossura,
        )

    def soltar_mouse(self, event):
        if self.controlador.objeto_guia:
            self.controlador.apagar_guia()
            figura = Elipse(
                self.controlador.x_start,
                self.controlador.y_start,
                event.x,
                event.y,
                self.controlador.cor_linha,
                self.controlador.cor_interna,
                self.controlador.grossura,
            )
            self.controlador.adicionar_figura(figura)
        super().soltar_mouse(event)


class EstadoPoligono(EstadoFerramenta):
    chave = "poligono"

    def iniciar_clique(self, event):
        self.controlador.inserir_no_poligono(event.x, event.y)

    def arrastar_mouse(self, event):
        if not self.controlador.nos_poligono:
            return
        self.controlador.apagar_guia()
        ux, uy = self.controlador.nos_poligono[-1]
        self.controlador.objeto_guia = self.tela.create_line(
            ux,
            uy,
            event.x,
            event.y,
            fill=self.controlador.cor_linha,
            width=self.controlador.grossura,
            dash=(4, 2),
        )

    def ao_sair(self):
        self.controlador.resetar_poligono_rascunho()

    def fechar(self):
        if len(self.controlador.nos_poligono) < 3:
            messagebox.showwarning("Aviso", "Minimo de 3 pontos exigidos.")
            return

        self.controlador.apagar_guia()
        self.controlador.apagar_apoios_poligono()

        figura = FormatoMultiplo(
            self.controlador.nos_poligono.copy(),
            self.controlador.cor_linha,
            self.controlador.cor_interna,
            self.controlador.grossura,
        )
        self.controlador.adicionar_figura(figura)
        self.controlador.nos_poligono = []
