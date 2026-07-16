from __future__ import annotations

import copy
from tkinter import colorchooser, filedialog, messagebox

from controlador.estados import (
    EstadoBorracha,
    EstadoLivre,
    EstadoOval,
    EstadoPoligono,
    EstadoRetangulo,
    EstadoSelecionar,
)
from modelo.documento import DocumentoDesenho
from modelo.formas import FiguraComposta, FormaGeometrica


class GerenteFluxo:
    def __init__(self):
        self.cor_linha = "black"
        self.cor_interna = ""
        self.grossura = 2

        self.documento = DocumentoDesenho()
        self.selecionadas: list[FormaGeometrica] = []
        self.copiadas: list[FormaGeometrica] = []

        self.x_start = None
        self.y_start = None
        self.ultimo_x = None
        self.ultimo_y = None
        self.objeto_guia = None
        self.nos_poligono = []
        self.graficos_apoio = []
        self.janela_view = None

        estados = [
            EstadoSelecionar(self),
            EstadoLivre(self),
            EstadoRetangulo(self),
            EstadoOval(self),
            EstadoPoligono(self),
            EstadoBorracha(self),
        ]
        self.estados = {estado.chave: estado for estado in estados}
        self.estado_atual = self.estados["livre"]
        self.modo = self.estado_atual.chave

    @property
    def historico(self):
        """Compatibilidade com o nome usado nas entregas anteriores."""
        return self.documento.figuras

    def vincular_view(self, janela_view):
        self.janela_view = janela_view
        raiz = self.janela_view.root
        raiz.bind("<Delete>", lambda _e: self.apagar_selecionadas())
        raiz.bind("<Control-c>", lambda _e: self.copiar_selecionadas())
        raiz.bind("<Control-v>", lambda _e: self.colar_selecionadas())
        raiz.bind("<Control-g>", lambda _e: self.agrupar_selecionadas())
        raiz.bind("<Control-Shift-G>", lambda _e: self.desagrupar_selecionadas())
        raiz.bind("<Control-Shift-g>", lambda _e: self.desagrupar_selecionadas())

   
    def iniciar_clique(self, event):
        self.estado_atual.iniciar_clique(event)

    def arrastar_mouse(self, event):
        self.estado_atual.arrastar_mouse(event)

    def soltar_mouse(self, event):
        self.estado_atual.soltar_mouse(event)

    def alternar_modo(self, novo_modo):
        if novo_modo not in self.estados:
            raise ValueError(f"Ferramenta desconhecida: {novo_modo}")
        self.estado_atual.ao_sair()
        self.estado_atual = self.estados[novo_modo]
        self.modo = novo_modo
        self.estado_atual.ao_entrar()

    # Operações básicas do desenho.
    def adicionar_figura(self, figura):
        self.documento.adicionar(figura)
        self.atualizar_tela()

    def figura_no_ponto(self, x, y):
        for figura in reversed(self.historico):
            if figura.contem_ponto(x, y):
                return figura
        return None

    def selecionar_apenas(self, figura):
        self.limpar_selecao()
        figura.definir_selecionada(True)
        self.selecionadas = [figura]

    def alternar_selecao(self, figura):
        if figura in self.selecionadas:
            figura.definir_selecionada(False)
            self.selecionadas.remove(figura)
        else:
            figura.definir_selecionada(True)
            self.selecionadas.append(figura)

    def limpar_selecao(self):
        for figura in self.selecionadas:
            figura.definir_selecionada(False)
        self.selecionadas.clear()

    def apagar_selecionadas(self):
        selecionadas = set(self.selecionadas)
        self.documento.figuras[:] = [figura for figura in self.historico if figura not in selecionadas]
        self.limpar_selecao()
        self.atualizar_tela()

    def copiar_selecionadas(self):
        self.copiadas = [copy.deepcopy(figura) for figura in self.selecionadas]

    def colar_selecionadas(self):
        if not self.copiadas:
            return
        self.limpar_selecao()
        novas = []
        for figura_copiada in self.copiadas:
            nova = copy.deepcopy(figura_copiada)
            nova.mover(20, 20)
            nova.definir_selecionada(True)
            self.documento.adicionar(nova)
            novas.append(nova)
        self.selecionadas = novas
       
        self.copiadas = [copy.deepcopy(figura) for figura in novas]
        self.atualizar_tela()

    def trazer_para_frente(self):
        selecionadas = [figura for figura in self.historico if figura in self.selecionadas]
        restantes = [figura for figura in self.historico if figura not in self.selecionadas]
        self.documento.figuras[:] = restantes + selecionadas
        self.atualizar_tela()

    def mandar_para_tras(self):
        selecionadas = [figura for figura in self.historico if figura in self.selecionadas]
        restantes = [figura for figura in self.historico if figura not in self.selecionadas]
        self.documento.figuras[:] = selecionadas + restantes
        self.atualizar_tela()

    
    def agrupar_selecionadas(self):
        if len(self.selecionadas) < 2:
            messagebox.showwarning("Agrupar", "Selecione pelo menos duas figuras para agrupar.")
            return

        indices = [i for i, figura in enumerate(self.historico) if figura in self.selecionadas]
        figuras_do_grupo = [self.historico[i] for i in indices]
        indice_insercao = max(indices) - (len(indices) - 1)

        for figura in figuras_do_grupo:
            figura.definir_selecionada(False)
        restantes = [figura for figura in self.historico if figura not in figuras_do_grupo]
        grupo = FiguraComposta(figuras_do_grupo)
        grupo.definir_selecionada(True)
        restantes.insert(indice_insercao, grupo)

        self.documento.figuras[:] = restantes
        self.selecionadas = [grupo]
        self.atualizar_tela()

    def desagrupar_selecionadas(self):
        grupos = [figura for figura in self.selecionadas if isinstance(figura, FiguraComposta)]
        if not grupos:
            messagebox.showwarning("Desagrupar", "Selecione pelo menos uma figura composta.")
            return

        novas_selecionadas = []
        novo_historico = []
        grupos_set = set(grupos)
        for figura in self.historico:
            if figura not in grupos_set:
                novo_historico.append(figura)
                continue
            for componente in figura.figuras:
                componente.definir_selecionada(True)
                novo_historico.append(componente)
                novas_selecionadas.append(componente)

        for figura in self.selecionadas:
            if figura not in grupos_set:
                figura.definir_selecionada(True)
                novas_selecionadas.append(figura)

        self.documento.figuras[:] = novo_historico
        self.selecionadas = novas_selecionadas
        self.atualizar_tela()

  
    def mudar_cor_linha(self):
        paleta = colorchooser.askcolor(title="Cor do contorno")
        if not paleta or not paleta[1]:
            return
        self.cor_linha = paleta[1]
        self.janela_view.amostra_borda.config(bg=self.cor_linha)
        for figura in self.selecionadas:
            figura.definir_cor_contorno(self.cor_linha)
        self.atualizar_tela()

    def mudar_cor_interna(self):
        paleta = colorchooser.askcolor(title="Cor do preenchimento")
        if not paleta or not paleta[1]:
            return
        self.cor_interna = paleta[1]
        self.janela_view.amostra_interna.config(bg=self.cor_interna)
        for figura in self.selecionadas:
            figura.definir_cor_preenchimento(self.cor_interna)
        self.atualizar_tela()

    def remover_preenchimento(self):
        self.cor_interna = ""
        self.janela_view.amostra_interna.config(bg="white")
        for figura in self.selecionadas:
            figura.definir_cor_preenchimento("")
        self.atualizar_tela()

    def alterar_grossura(self, valor):
        self.grossura = int(float(valor))
        for figura in self.selecionadas:
            figura.definir_largura(self.grossura)
        self.atualizar_tela()

   
    def apagar_guia(self):
        if self.objeto_guia is not None and self.janela_view is not None:
            self.janela_view.quadro_desenho.delete(self.objeto_guia)
        self.objeto_guia = None

    def inserir_no_poligono(self, x, y):
        tela = self.janela_view.quadro_desenho
        self.nos_poligono.append((x, y))
        raio = 3
        marcador = tela.create_oval(
            x - raio,
            y - raio,
            x + raio,
            y + raio,
            fill=self.cor_linha,
            outline=self.cor_linha,
        )
        self.graficos_apoio.append(marcador)
        if len(self.nos_poligono) > 1:
            xa, ya = self.nos_poligono[-2]
            linha = tela.create_line(xa, ya, x, y, fill=self.cor_linha, width=self.grossura)
            self.graficos_apoio.append(linha)

    def fechar_poligono(self):
        estado = self.estados["poligono"]
        estado.fechar()

    def resetar_poligono_rascunho(self):
        if self.janela_view is None:
            self.nos_poligono = []
            self.graficos_apoio = []
            self.objeto_guia = None
            return
        tela = self.janela_view.quadro_desenho
        self.apagar_guia()
        for item in self.graficos_apoio:
            tela.delete(item)
        self.nos_poligono = []
        self.graficos_apoio = []

    def resetar_painel(self):
        self.documento.limpar()
        self.limpar_selecao()
        self.copiadas.clear()
        self.resetar_poligono_rascunho()
        self.atualizar_tela()

    
    def salvar_desenho_json(self):
        caminho = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("Arquivos JSON", "*.json")],
        )
        if not caminho:
            return
        try:
            self.documento.salvar(caminho)
            messagebox.showinfo("Sucesso", "Projeto salvo em JSON com sucesso!")
        except (OSError, TypeError, ValueError) as erro:
            messagebox.showerror("Erro", f"Erro ao salvar arquivo JSON: {erro}")

    def abrir_desenho_json(self):
        caminho = filedialog.askopenfilename(filetypes=[("Arquivos JSON", "*.json")])
        if not caminho:
            return
        try:
            self.documento = DocumentoDesenho.abrir(caminho)
            self.limpar_selecao()
            self.copiadas.clear()
            self.atualizar_tela()
            messagebox.showinfo("Sucesso", "Projeto carregado com sucesso!")
        except (OSError, KeyError, TypeError, ValueError) as erro:
            messagebox.showerror("Erro", f"Erro ao carregar o arquivo JSON: {erro}")


    def atualizar_tela(self):
        if self.janela_view is None:
            return
        tela = self.janela_view.quadro_desenho
        tela.delete("all")
        for figura in self.historico:
            figura.renderizar(tela)
