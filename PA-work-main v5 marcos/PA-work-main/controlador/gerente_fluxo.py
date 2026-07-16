import copy
from tkinter import colorchooser, messagebox
from modelo.formas import Traco, Quadro, Elipse, FormatoMultiplo, Raspador

class GerenteFluxo:
    def __init__(self):
        self.modo = "livre"
        self.cor_linha = "black"
        self.cor_interna = ""
        self.grossura = 2
        
        self.historico = []
        self.selecionadas = []
        self.copiadas = []
        
        self.x_start = None
        self.y_start = None
        self.ultimo_x = None
        self.ultimo_y = None
        self.objeto_guia = None
        
        self.nos_poligono = []
        self.graficos_apoio = []
        
        self.janela_view = None

    def vincular_view(self, janela_view):
        self.janela_view = janela_view
        self.janela_view.root.bind("<Delete>", lambda e: self.apagar_selecionadas())
        self.janela_view.root.bind("<Control-c>", lambda e: self.copiar_selecionadas())
        self.janela_view.root.bind("<Control-v>", lambda e: self.colar_selecionadas())

    def iniciar_clique(self, event):
        self.x_start = event.x
        self.y_start = event.y
        self.ultimo_x = event.x
        self.ultimo_y = event.y

        if self.modo == "selecionar":
            figura_clicada = None
            for fig in reversed(self.historico):
                if fig.contem_ponto(event.x, event.y):
                    figura_clicada = fig
                    break
            
            # Seleção múltipla com a tecla Shift pressionada
            shift_pressionado = (event.state & 0x0001)
            
            if figura_clicada:
                if shift_pressionado:
                    if figura_clicada in self.selecionadas:
                        figura_clicada.selecionada = False
                        self.selecionadas.remove(figura_clicada)
                    else:
                        figura_clicada.selecionada = True
                        self.selecionadas.append(figura_clicada)
                else:
                    if figura_clicada not in self.selecionadas:
                        for f in self.selecionadas:
                            f.selecionada = False
                        figura_clicada.selecionada = True
                        self.selecionadas = [figura_clicada]
            else:
                if not shift_pressionado:
                    for f in self.selecionadas:
                        f.selecionada = False
                    self.selecionadas.clear()
            
            self.atualizar_tela()
            return

        if self.modo == "poligono":
            self.inserir_no(event)
            return

        self.objeto_guia = None

    def arrastar_mouse(self, event):
        tela = self.janela_view.quadro_desenho
        
        if self.modo == "selecionar" and self.selecionadas:
            dx = event.x - self.ultimo_x
            dy = event.y - self.ultimo_y
            for fig in self.selecionadas:
                fig.mover(dx, dy)
            self.ultimo_x = event.x
            self.ultimo_y = event.y
            self.atualizar_tela()
            return

        if self.modo == "livre":
            obj_traco = Traco(self.x_start, self.y_start, event.x, event.y, self.cor_linha, self.grossura)
            obj_traco.renderizar(tela)
            self.historico.append(obj_traco)
            self.x_start = event.x
            self.y_start = event.y

        elif self.modo == "borracha":
            obj_borracha = Raspador(self.x_start, self.y_start, event.x, event.y, self.grossura * 2)
            obj_borracha.renderizar(tela)
            self.historico.append(obj_borracha)
            self.x_start = event.x
            self.y_start = event.y        

        elif self.modo == "retangulo":
            if self.objeto_guia:
                tela.delete(self.objeto_guia)
            self.objeto_guia = tela.create_rectangle(
                self.x_start, self.y_start, event.x, event.y,
                outline=self.cor_linha, fill=self.cor_interna, width=self.grossura
            )

        elif self.modo == "oval":
            if self.objeto_guia:
                tela.delete(self.objeto_guia)
            self.objeto_guia = tela.create_oval(
                self.x_start, self.y_start, event.x, event.y,
                outline=self.cor_linha, fill=self.cor_interna, width=self.grossura
            )

        elif self.modo == "poligono" and self.nos_poligono:
            if self.objeto_guia:
                tela.delete(self.objeto_guia)
            ux, uy = self.nos_poligono[-1]
            self.objeto_guia = tela.create_line(
                ux, uy, event.x, event.y,
                fill=self.cor_linha, width=self.grossura, dash=(4, 2)
            )

    def soltar_mouse(self, event):
        tela = self.janela_view.quadro_desenho
        
        if self.modo == "retangulo" and self.objeto_guia:
            tela.delete(self.objeto_guia)
            obj_quadro = Quadro(self.x_start, self.y_start, event.x, event.y, self.cor_linha, self.cor_interna, self.grossura)
            obj_quadro.renderizar(tela)
            self.historico.append(obj_quadro)

        elif self.modo == "oval" and self.objeto_guia:
            tela.delete(self.objeto_guia)
            obj_elipse = Elipse(self.x_start, self.y_start, event.x, event.y, self.cor_linha, self.cor_interna, self.grossura)
            obj_elipse.renderizar(tela)
            self.historico.append(obj_elipse)

        self.objeto_guia = None

    def inserir_no(self, event):
        tela = self.janela_view.quadro_desenho
        self.nos_poligono.append((event.x, event.y))
        d = 3

        marcador = tela.create_oval(
            event.x - d, event.y - d, event.x + d, event.y + d,
            fill=self.cor_linha, outline=self.cor_linha
        )
        self.graficos_apoio.append(marcador)

        if len(self.nos_poligono) > 1:
            xa, ya = self.nos_poligono[-2]
            xb, yb = self.nos_poligono[-1]
            linha_apoio = tela.create_line(xa, ya, xb, yb, fill=self.cor_linha, width=self.grossura)
            self.graficos_apoio.append(linha_apoio)

    def fechar_poligono(self):
        tela = self.janela_view.quadro_desenho
        if len(self.nos_poligono) < 3:
            messagebox.showwarning("Aviso", "Mínimo de 3 pontos exigidos.")
            return

        if self.objeto_guia:
            tela.delete(self.objeto_guia)
            self.objeto_guia = None

        for item in self.graficos_apoio:
            tela.delete(item)

        obj_multiplo = FormatoMultiplo(self.nos_poligono.copy(), self.cor_linha, self.cor_interna, self.grossura)
        obj_multiplo.renderizar(tela)
        self.historico.append(obj_multiplo)

        self.nos_poligono = []
        self.graficos_apoio = []

    def resetar_poligono_rascunho(self):
        tela = self.janela_view.quadro_desenho
        if self.objeto_guia:
            tela.delete(self.objeto_guia)
            self.objeto_guia = None
        for item in self.graficos_apoio:
            tela.delete(item)
        self.nos_poligono = []
        self.graficos_apoio = []

    def alternar_modo(self, novo_modo):
        if self.modo == "poligono" and novo_modo != "poligono":
            self.resetar_poligono_rascunho()
        self.modo = novo_modo

    def mudar_cor_linha(self):
        paleta = colorchooser.askcolor(title="Cor Externa")
        if paleta and paleta[1]:
            self.cor_linha = paleta[1]
            self.janela_view.amostra_borda.config(bg=self.cor_linha)
            
            # Se houver figuras selecionadas, altera a cor delas imediatamente
            if self.selecionadas:
                for fig in self.selecionadas:
                    fig.tracejado = self.cor_linha
                self.atualizar_tela()

    def mudar_cor_interna(self):
        paleta = colorchooser.askcolor(title="Cor Interna")
        if paleta and paleta[1]:
            self.cor_interna = paleta[1]
            self.janela_view.amostra_interna.config(bg=self.cor_interna)
            
            # Se houver figuras selecionadas, altera o preenchimento delas imediatamente
            if self.selecionadas:
                for fig in self.selecionadas:
                    if hasattr(fig, "preenchimento"):
                        fig.preenchimento = self.cor_interna
                self.atualizar_tela()

    def remover_preenchimento(self):
        self.cor_interna = ""
        self.janela_view.amostra_interna.config(bg="white")
        if self.selecionadas:
            for fig in self.selecionadas:
                if hasattr(fig, "preenchimento"):
                    fig.preenchimento = ""
            self.atualizar_tela()

    def alterar_grossura(self, valor):
        self.grossura = int(valor)
        if self.selecionadas:
            for fig in self.selecionadas:
                fig.largura = self.grossura
            self.atualizar_tela()

    def resetar_painel(self):
        tela = self.janela_view.quadro_desenho
        tela.delete("all")
        self.historico.clear()
        self.selecionadas.clear()
        self.nos_poligono = []
        self.graficos_apoio = []
        self.objeto_guia = None

    def apagar_selecionadas(self):
        if self.selecionadas:
            for fig in self.selecionadas:
                if fig in self.historico:
                    self.historico.remove(fig)
            self.selecionadas.clear()
            self.atualizar_tela()

    def copiar_selecionadas(self):
        self.copiadas = [copy.deepcopy(fig) for fig in self.selecionadas]

    def colar_selecionadas(self):
        if self.copiadas:
            for f in self.selecionadas:
                f.selecionada = False
            self.selecionadas.clear()
            
            for fig in self.copiadas:
                nova_fig = copy.deepcopy(fig)
                nova_fig.mover(20, 20)  # Deslocamento para não colar por cima
                nova_fig.selecionada = True
                self.historico.append(nova_fig)
                self.selecionadas.append(nova_fig)
            
            self.copiadas = [copy.deepcopy(fig) for fig in self.selecionadas]
            self.atualizar_tela()

    def trazer_para_frente(self):
        for fig in self.selecionadas:
            if fig in self.historico:
                self.historico.remove(fig)
                self.historico.append(fig)
        self.atualizar_tela()

    def mandar_para_tras(self):
        for fig in reversed(self.selecionadas):
            if fig in self.historico:
                self.historico.remove(fig)
                self.historico.insert(0, fig)
        self.atualizar_tela()

    def atualizar_tela(self):
        tela = self.janela_view.quadro_desenho
        tela.delete("all")
        for fig in self.historico:
            fig.renderizar(tela)