import tkinter as tk
from tkinter import colorchooser, messagebox

from figuras import Linha, Retangulo, Oval, Poligono, Borracha


ini_x = None
ini_y = None
item_temp = None

ferramenta = "livre"
cor_borda = "black"
cor_preenchimento = ""
espessura = 2

figuras = []

pontos_poligono = []
itens_temp_poligono = []


def marca_inicio(event):
    global ini_x, ini_y, item_temp

    if ferramenta == "poligono":
        adicionar_ponto_poligono(event)
        return

    ini_x = event.x
    ini_y = event.y
    item_temp = None


def atualiza_fim(event):
    global ini_x, ini_y, item_temp

    if ferramenta == "livre":
        linha = Linha(
            ini_x,
            ini_y,
            event.x,
            event.y,
            cor_borda,
            espessura
        )

        linha.desenhar(canvas)
        figuras.append(linha)

        ini_x = event.x
        ini_y = event.y

    elif ferramenta == "borracha":
        borracha = Borracha(
            ini_x,
            ini_y,
            event.x,
            event.y,
            espessura * 2
        )

        borracha.desenhar(canvas)
        figuras.append(borracha)

        ini_x = event.x
        ini_y = event.y        

    elif ferramenta == "retangulo":
        if item_temp:
            canvas.delete(item_temp)

        item_temp = canvas.create_rectangle(
            ini_x,
            ini_y,
            event.x,
            event.y,
            outline=cor_borda,
            fill=cor_preenchimento,
            width=espessura
        )

    elif ferramenta == "oval":
        if item_temp:
            canvas.delete(item_temp)

        item_temp = canvas.create_oval(
            ini_x,
            ini_y,
            event.x,
            event.y,
            outline=cor_borda,
            fill=cor_preenchimento,
            width=espessura
        )

    elif ferramenta == "poligono":
        if pontos_poligono:
            if item_temp:
                canvas.delete(item_temp)

            ultimo_x, ultimo_y = pontos_poligono[-1]

            item_temp = canvas.create_line(
                ultimo_x,
                ultimo_y,
                event.x,
                event.y,
                fill=cor_borda,
                width=espessura,
                dash=(4, 2)
            )


def finaliza(event):
    global item_temp

    if ferramenta == "retangulo":
        if item_temp:
            canvas.delete(item_temp)

        retangulo = Retangulo(
            ini_x,
            ini_y,
            event.x,
            event.y,
            cor_borda,
            cor_preenchimento,
            espessura
        )

        retangulo.desenhar(canvas)
        figuras.append(retangulo)

    elif ferramenta == "oval":
        if item_temp:
            canvas.delete(item_temp)

        oval = Oval(
            ini_x,
            ini_y,
            event.x,
            event.y,
            cor_borda,
            cor_preenchimento,
            espessura
        )

        oval.desenhar(canvas)
        figuras.append(oval)

    item_temp = None


def adicionar_ponto_poligono(event):
    pontos_poligono.append((event.x, event.y))

    raio = 3

    ponto = canvas.create_oval(
        event.x - raio,
        event.y - raio,
        event.x + raio,
        event.y + raio,
        fill=cor_borda,
        outline=cor_borda
    )

    itens_temp_poligono.append(ponto)

    if len(pontos_poligono) > 1:
        x1, y1 = pontos_poligono[-2]
        x2, y2 = pontos_poligono[-1]

        linha_temp = canvas.create_line(
            x1,
            y1,
            x2,
            y2,
            fill=cor_borda,
            width=espessura
        )

        itens_temp_poligono.append(linha_temp)


def finalizar_poligono():
    global pontos_poligono, itens_temp_poligono, item_temp

    if len(pontos_poligono) < 3:
        messagebox.showwarning(
            "Polígono",
            "Um polígono precisa de pelo menos 3 pontos."
        )
        return

    if item_temp:
        canvas.delete(item_temp)
        item_temp = None

    for item in itens_temp_poligono:
        canvas.delete(item)

    poligono = Poligono(
        pontos_poligono.copy(),
        cor_borda,
        cor_preenchimento,
        espessura
    )

    poligono.desenhar(canvas)
    figuras.append(poligono)

    pontos_poligono = []
    itens_temp_poligono = []


def limpar_poligono_temporario():
    global pontos_poligono, itens_temp_poligono, item_temp

    if item_temp:
        canvas.delete(item_temp)
        item_temp = None

    for item in itens_temp_poligono:
        canvas.delete(item)

    pontos_poligono = []
    itens_temp_poligono = []


def escolher_ferramenta(valor):
    global ferramenta

    if ferramenta == "poligono" and valor != "poligono":
        limpar_poligono_temporario()

    ferramenta = valor


def escolher_cor_borda():
    global cor_borda

    cor = colorchooser.askcolor(title="Cor da borda")

    if cor and cor[1]:
        cor_borda = cor[1]
        btn_borda.config(bg=cor_borda)


def escolher_cor_preenchimento():
    global cor_preenchimento

    cor = colorchooser.askcolor(title="Cor de preenchimento")

    if cor and cor[1]:
        cor_preenchimento = cor[1]
        btn_preenche.config(bg=cor_preenchimento)


def sem_preenchimento():
    global cor_preenchimento

    cor_preenchimento = ""
    btn_preenche.config(bg="white")


def atualiza_espessura(v):
    global espessura

    espessura = int(v)


def limpar_tudo():
    global pontos_poligono, itens_temp_poligono, item_temp

    canvas.delete("all")
    figuras.clear()

    pontos_poligono = []
    itens_temp_poligono = []
    item_temp = None


root = tk.Tk()
root.title("Desenho")

painel = tk.Frame(root, bg="#f0f0f0", padx=8, pady=8)
painel.pack(side=tk.LEFT, fill=tk.Y)

tk.Label(painel, text="Ferramenta", bg="#f0f0f0").pack(anchor=tk.W)

var = tk.StringVar(value="livre")

for texto, valor in [
    ("Mão livre", "livre"),
    ("Retângulo", "retangulo"),
    ("Oval", "oval"),
    ("Polígono", "poligono"),
    ("Borracha", "borracha")
]:
    tk.Radiobutton(
        painel,
        text=texto,
        variable=var,
        value=valor,
        bg="#f0f0f0",
        command=lambda v=valor: escolher_ferramenta(v)
    ).pack(anchor=tk.W)

tk.Button(
    painel,
    text="Finalizar polígono",
    command=finalizar_poligono
).pack(anchor=tk.W, pady=(5, 0))

tk.Button(
    painel,
    text="Apagar tudo",
    command=limpar_tudo
).pack(anchor=tk.W, pady=(5, 0))

tk.Label(painel, text="Borda", bg="#f0f0f0").pack(anchor=tk.W, pady=(10, 0))

btn_borda = tk.Button(
    painel,
    bg="black",
    width=4,
    command=escolher_cor_borda
)

btn_borda.pack(anchor=tk.W)

tk.Label(painel, text="Preenchimento", bg="#f0f0f0").pack(anchor=tk.W, pady=(10, 0))

btn_preenche = tk.Button(
    painel,
    bg="white",
    width=4,
    command=escolher_cor_preenchimento
)

btn_preenche.pack(anchor=tk.W)

tk.Button(
    painel,
    text="Sem preench.",
    command=sem_preenchimento
).pack(anchor=tk.W, pady=(2, 0))

tk.Label(painel, text="Espessura", bg="#f0f0f0").pack(anchor=tk.W, pady=(10, 0))

tk.Scale(
    painel,
    from_=1,
    to=20,
    orient=tk.HORIZONTAL,
    command=atualiza_espessura,
    bg="#f0f0f0"
).pack(anchor=tk.W)

canvas = tk.Canvas(root, bg="white", width=600, height=600)
canvas.pack(side=tk.LEFT)

canvas.bind("<ButtonPress-1>", marca_inicio)
canvas.bind("<B1-Motion>", atualiza_fim)
canvas.bind("<ButtonRelease-1>", finaliza)

root.mainloop()