import copy
import json
from tkinter import colorchooser, messagebox, filedialog
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
        self.pontos_livre = []
        
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
            tela.create_line(
                self.ultimo_x, self.ultimo_y, event.x, event.y,
                fill=self.cor_linha, width=self.grossura, capstyle="round", joinstyle="round"
            )
            self.pontos_livre.append((event.x, event.y))
            self.ultimo_x = event.x
            self.ultimo_y = event.y

        elif self.modo == "borracha":
            tela.create_line(
                self.ultimo_x, self.ultimo_y, event.x, event.y,
                fill="white", width=self.grossura * 2, capstyle="round", joinstyle="round"
            )
            self.pontos_livre.append((event.x, event.y))
            self.ultimo_x = event.x
            self.ultimo_y = event.y

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
        
        if self.modo == "livre" and len(self.pontos_livre) > 1:
            for i in range(len(self.pontos_livre) - 1):
                xa, ya = self.pontos_livre[i]
                xb, yb = self.pontos_livre[i+1]
                obj_traco = Traco(xa, ya, xb, yb, self.cor_linha, self.grossura)
                self.historico.append(obj_traco)
            self.pontos_livre = []

        elif self.modo == "borracha" and len(self.pontos_livre) > 1:
            for i in range(len(self.pontos_livre) - 1):
                xa, ya = self.pontos_livre[i]
                xb, yb = self.pontos_livre[i+1]
                obj_borracha = Raspador(xa, ya, xb, yb, self.grossura * 2)
                self.historico.append(obj_borracha)
            self.pontos_livre = []

        elif self.modo == "retangulo" and self.objeto_guia:
            tela.delete(self.objeto_guia)
            obj_quadro = Quadro(self.x_start, self.y_start, event.x, event.y, self.cor_linha, self.cor_interna, self.grossura)
            self.historico.append(obj_quadro)

        elif self.modo == "oval" and self.objeto_guia:
            tela.delete(self.objeto_guia)
            obj_elipse = Elipse(self.x_start, self.y_start, event.x, event.y, self.cor_linha, self.cor_interna, self.grossura)
            self.historico.append(obj_elipse)

        self.objeto_guia = None
        self.atualizar_tela()

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
        if len(self.nos_poligono) < 3:
            messagebox.showwarning("Aviso", "Mínimo de 3 pontos exigidos.")
            return
        self.resetar_poligono_rascunho()
        obj_multiplo = FormatoMultiplo(self.nos_poligono.copy(), self.cor_linha, self.cor_interna, self.grossura)
        self.historico.append(obj_multiplo)
        self.atualizar_tela()

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
            if self.selecionadas:
                for fig in self.selecionadas:
                    fig.tracejado = self.cor_linha
                self.atualizar_tela()

    def mudar_cor_interna(self):
        paleta = colorchooser.askcolor(title="Cor Interna")
        if paleta and paleta[1]:
            self.cor_interna = paleta[1]
            self.janela_view.amostra_interna.config(bg=self.cor_interna)
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
        self.historico.clear()
        self.selecionadas.clear()
        self.resetar_poligono_rascunho()
        self.atualizar_tela()

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
                nova_fig.mover(20, 20)
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

    # --- SALVAR O DESENHO EM ARQUIVO ---
    def salvar_desenho_json(self):
        caminho = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("Arquivos JSON", "*.json")])
        if not caminho:
            return
        
        dados = []
        for fig in self.historico:
            if isinstance(fig, Traco):
                dados.append({"tipo": "Traco", "xa": fig.xa, "ya": fig.ya, "xb": fig.xb, "yb": fig.yb, "tracejado": fig.tracejado, "largura": fig.largura})
            elif isinstance(fig, Raspador):
                dados.append({"tipo": "Raspador", "xa": fig.xa, "ya": fig.ya, "xb": fig.xb, "yb": fig.yb, "largura": fig.largura})
            elif isinstance(fig, Quadro):
                dados.append({"tipo": "Quadro", "xa": fig.xa, "ya": fig.ya, "xb": fig.xb, "yb": fig.yb, "tracejado": fig.tracejado, "preenchimento": fig.preenchimento, "largura": fig.largura})
            elif isinstance(fig, Elipse):
                dados.append({"tipo": "Elipse", "xa": fig.xa, "ya": fig.ya, "xb": fig.xb, "yb": fig.yb, "tracejado": fig.tracejado, "preenchimento": fig.preenchimento, "largura": fig.largura})
            elif isinstance(fig, FormatoMultiplo):
                dados.append({"tipo": "FormatoMultiplo", "vertices": fig.vertices, "tracejado": fig.tracejado, "preenchimento": fig.preenchimento, "largura": fig.largura})
        
        try:
            with open(caminho, 'w', encoding='utf-8') as f:
                json.dump(dados, f, indent=4)
            messagebox.showinfo("Sucesso", "Projeto salvo em JSON com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar arquivo JSON: {e}")

    # --- CARREGAR O DESENHO DO ARQUIVO E EXIBIR IMEDIATAMENTE ---
    def abrir_desenho_json(self):
        caminho = filedialog.askopenfilename(filetypes=[("Arquivos JSON", "*.json")])
        if not caminho:
            return
        
        try:
            with open(caminho, 'r', encoding='utf-8') as f:
                dados = json.load(f)
            
            # 1. Limpa o histórico atual e as seleções anteriores
            self.historico.clear()
            self.selecionadas.clear()
            
            # 2. Reconstrói os objetos geométricos reais na memória
            for d in dados:
                tipo = d["tipo"]
                if tipo == "Traco":
                    fig = Traco(d["xa"], d["ya"], d["xb"], d["yb"], d["tracejado"], d["largura"])
                elif tipo == "Raspador":
                    fig = Raspador(d["xa"], d["ya"], d["xb"], d["yb"], d["largura"])
                elif tipo == "Quadro":
                    fig = Quadro(d["xa"], d["ya"], d["xb"], d["yb"], d["tracejado"], d["preenchimento"], d["largura"])
                elif tipo == "Elipse":
                    fig = Elipse(d["xa"], d["ya"], d["xb"], d["yb"], d["tracejado"], d["preenchimento"], d["largura"])
                elif tipo == "FormatoMultiplo":
                    fig = FormatoMultiplo(d["vertices"], d["tracejado"], d["preenchimento"], d["largura"])
                
                self.historico.append(fig)
            
            # 3. Força a tela a ser limpa e redesenha todos os objetos lidos do arquivo
            self.atualizar_tela()
            messagebox.showinfo("Sucesso", "Projeto carregado com sucesso!")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar o arquivo JSON: {e}")

    def salvar_imagem_eps(self):
        caminho = filedialog.asksaveasfilename(defaultextension=".eps", filetypes=[("Encapsulated PostScript (Imagem)", "*.eps")])
        if not caminho:
            return
        try:
            self.janela_view.quadro_desenho.postscript(file=caminho, colormode='color')
            messagebox.showinfo("Sucesso", "Desenho salvo como Imagem (.eps) com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao exportar imagem: {e}")

    # Redesenha todo o histórico geométrico atual no quadro do Canvas
    def atualizar_tela(self):
        tela = self.janela_view.quadro_desenho
        tela.delete("all")
        for fig in self.historico:
            fig.renderizar(tela)