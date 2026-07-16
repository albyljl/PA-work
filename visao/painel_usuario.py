import tkinter as tk


class PainelUsuario:
    def __init__(self, root, controlador):
        self.root = root
        self.controlador = controlador
        self.root.title("Editor Gráfico - MVC, State e Composite")

        self.barra_lateral = tk.Frame(self.root, bg="#f5f5f5", padx=10, pady=10)
        self.barra_lateral.pack(side=tk.LEFT, fill=tk.Y)

        tk.Label(self.barra_lateral, text="Ferramentas:", bg="#f5f5f5").pack(anchor=tk.W)
        self.seletor = tk.StringVar(value="livre")
        ferramentas = [
            ("Selecionar", "selecionar"),
            ("Livre", "livre"),
            ("Retângulo", "retangulo"),
            ("Oval", "oval"),
            ("Polígono", "poligono"),
            ("Borracha", "borracha"),
        ]
        for nome, chave in ferramentas:
            tk.Radiobutton(
                self.barra_lateral,
                text=nome,
                variable=self.seletor,
                value=chave,
                bg="#f5f5f5",
                command=lambda valor=chave: self.controlador.alternar_modo(valor),
            ).pack(anchor=tk.W)

        tk.Button(
            self.barra_lateral,
            text="Concluir Polígono",
            command=self.controlador.fechar_poligono,
        ).pack(anchor=tk.W, pady=(6, 0))

        tk.Label(self.barra_lateral, text="Agrupamento:", bg="#f5f5f5").pack(anchor=tk.W, pady=(12, 0))
        tk.Button(
            self.barra_lateral,
            text="Agrupar (Ctrl+G)",
            command=self.controlador.agrupar_selecionadas,
        ).pack(anchor=tk.W, pady=(3, 0))
        tk.Button(
            self.barra_lateral,
            text="Desagrupar (Ctrl+Shift+G)",
            command=self.controlador.desagrupar_selecionadas,
        ).pack(anchor=tk.W, pady=(3, 0))

        tk.Label(self.barra_lateral, text="Organizar:", bg="#f5f5f5").pack(anchor=tk.W, pady=(12, 0))
        tk.Button(
            self.barra_lateral,
            text="Trazer para Frente",
            command=self.controlador.trazer_para_frente,
        ).pack(anchor=tk.W, pady=(3, 0))
        tk.Button(
            self.barra_lateral,
            text="Mandar para Trás",
            command=self.controlador.mandar_para_tras,
        ).pack(anchor=tk.W, pady=(3, 0))

        tk.Label(self.barra_lateral, text="Contorno:", bg="#f5f5f5").pack(anchor=tk.W, pady=(12, 0))
        self.amostra_borda = tk.Button(
            self.barra_lateral,
            bg="black",
            width=4,
            command=self.controlador.mudar_cor_linha,
        )
        self.amostra_borda.pack(anchor=tk.W)

        tk.Label(self.barra_lateral, text="Preenchimento:", bg="#f5f5f5").pack(anchor=tk.W, pady=(12, 0))
        self.amostra_interna = tk.Button(
            self.barra_lateral,
            bg="white",
            width=4,
            command=self.controlador.mudar_cor_interna,
        )
        self.amostra_interna.pack(anchor=tk.W)
        tk.Button(
            self.barra_lateral,
            text="Fundo Invisível",
            command=self.controlador.remover_preenchimento,
        ).pack(anchor=tk.W, pady=(3, 0))

        tk.Label(self.barra_lateral, text="Espessura:", bg="#f5f5f5").pack(anchor=tk.W, pady=(12, 0))
        tk.Scale(
            self.barra_lateral,
            from_=1,
            to=20,
            orient=tk.HORIZONTAL,
            bg="#f5f5f5",
            command=self.controlador.alterar_grossura,
        ).pack(anchor=tk.W)

        tk.Label(self.barra_lateral, text="Arquivo:", bg="#f5f5f5").pack(anchor=tk.W, pady=(12, 0))
        tk.Button(self.barra_lateral, text="Salvar", command=self.controlador.salvar_desenho_json).pack(anchor=tk.W, pady=(3, 0))
        tk.Button(self.barra_lateral, text="Abrir", command=self.controlador.abrir_desenho_json).pack(anchor=tk.W, pady=(3, 0))
        tk.Button(self.barra_lateral, text="Limpar Tela", command=self.controlador.resetar_painel).pack(anchor=tk.W, pady=(8, 0))

        self.quadro_desenho = tk.Canvas(self.root, bg="white")
        self.quadro_desenho.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.quadro_desenho.bind("<Button-1>", self.controlador.iniciar_clique)
        self.quadro_desenho.bind("<B1-Motion>", self.controlador.arrastar_mouse)
        self.quadro_desenho.bind("<ButtonRelease-1>", self.controlador.soltar_mouse)
