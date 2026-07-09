from tkinter import colorchooser, filedialog

from controlador.estados import (
    EstadoBorracha,
    EstadoLivre,
    EstadoOval,
    EstadoPoligono,
    EstadoRetangulo,
)
from modelo.documento import DocumentoDesenho


class GerenteFluxo:
    def __init__(self):
        self.cor_linha = "black"
        self.cor_interna = ""
        self.grossura = 2

        self.documento = DocumentoDesenho()
        self.historico = self.documento.figuras

        self.x_start = None
        self.y_start = None
        self.objeto_guia = None

        self.nos_poligono = []
        self.graficos_apoio = []

        self.janela_view = None
        self.estados = {
            estado.chave: estado(self)
            for estado in (
                EstadoLivre,
                EstadoRetangulo,
                EstadoOval,
                EstadoPoligono,
                EstadoBorracha,
            )
        }
        self.estado_atual = self.estados["livre"]
        self.modo = self.estado_atual.chave

    def vincular_view(self, janela_view):
        self.janela_view = janela_view

    def iniciar_clique(self, event):
        self.estado_atual.iniciar_clique(event)

    def arrastar_mouse(self, event):
        self.estado_atual.arrastar_mouse(event)

    def soltar_mouse(self, event):
        self.estado_atual.soltar_mouse(event)

    def alternar_modo(self, novo_modo):
        estado_novo = self.estados[novo_modo]
        if estado_novo is self.estado_atual:
            return
        self.estado_atual.ao_sair()
        self.estado_atual = estado_novo
        self.modo = estado_novo.chave
        self.estado_atual.ao_entrar()

    def adicionar_figura(self, figura):
        figura.renderizar(self.janela_view.quadro_desenho)
        self.documento.adicionar(figura)

    def apagar_guia(self):
        if self.objeto_guia:
            self.janela_view.quadro_desenho.delete(self.objeto_guia)
            self.objeto_guia = None

    def inserir_no_poligono(self, x, y):
        tela = self.janela_view.quadro_desenho
        self.nos_poligono.append((x, y))
        d = 3

        marcador = tela.create_oval(
            x - d, y - d, x + d, y + d,
            fill=self.cor_linha, outline=self.cor_linha
        )
        self.graficos_apoio.append(marcador)

        if len(self.nos_poligono) > 1:
            xa, ya = self.nos_poligono[-2]
            xb, yb = self.nos_poligono[-1]
            linha_apoio = tela.create_line(xa, ya, xb, yb, fill=self.cor_linha, width=self.grossura)
            self.graficos_apoio.append(linha_apoio)

    def apagar_apoios_poligono(self):
        for item in self.graficos_apoio:
            self.janela_view.quadro_desenho.delete(item)
        self.graficos_apoio = []

    def fechar_poligono(self):
        estado = self.estados["poligono"]
        estado.fechar()

    def resetar_poligono_rascunho(self):
        self.apagar_guia()
        self.apagar_apoios_poligono()
        self.nos_poligono = []

    def mudar_cor_linha(self):
        paleta = colorchooser.askcolor(title="Cor Externa")
        if paleta and paleta[1]:
            self.cor_linha = paleta[1]
            self.janela_view.amostra_borda.config(bg=self.cor_linha)

    def mudar_cor_interna(self):
        paleta = colorchooser.askcolor(title="Cor Interna")
        if paleta and paleta[1]:
            self.cor_interna = paleta[1]
            self.janela_view.amostra_interna.config(bg=self.cor_interna)

    def remover_preenchimento(self):
        self.cor_interna = ""
        self.janela_view.amostra_interna.config(bg="white")

    def alterar_grossura(self, valor):
        self.grossura = int(valor)

    def resetar_painel(self):
        self.janela_view.quadro_desenho.delete("all")
        self.documento.limpar()
        self.nos_poligono = []
        self.graficos_apoio = []
        self.objeto_guia = None

    def redesenhar(self):
        tela = self.janela_view.quadro_desenho
        tela.delete("all")
        for figura in self.documento.figuras:
            figura.renderizar(tela)

    def salvar_desenho(self):
        caminho = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("Desenhos JSON", "*.json"), ("Todos os arquivos", "*.*")],
        )
        if caminho:
            self.documento.salvar(caminho)

    def abrir_desenho(self):
        caminho = filedialog.askopenfilename(
            filetypes=[("Desenhos JSON", "*.json"), ("Todos os arquivos", "*.*")]
        )
        if caminho:
            self.documento = DocumentoDesenho.abrir(caminho)
            self.historico = self.documento.figuras
            self.resetar_poligono_rascunho()
            self.redesenhar()
