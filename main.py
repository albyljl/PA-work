import tkinter as tk
from tkinter import colorchooser

ini_x = None
ini_y = None
item_temp = None
ferramenta = "livre"
cor_borda = "black"
cor_preenchimento = ""
espessura = 2


def marca_inicio(event):
    global ini_x, ini_y, item_temp
    ini_x = event.x
    ini_y = event.y
    item_temp = None


def atualiza_fim(event):
    global ini_x, ini_y, item_temp

    if ferramenta == "livre":
        canvas.create_line(ini_x, ini_y, event.x, event.y,
                           fill=cor_borda, width=espessura,
                           capstyle=tk.ROUND, joinstyle=tk.ROUND)
        ini_x = event.x
        ini_y = event.y

    elif ferramenta == "retangulo":
        if item_temp:
            canvas.delete(item_temp)
        item_temp = canvas.create_rectangle(ini_x, ini_y, event.x, event.y,
                                            outline=cor_borda, fill=cor_preenchimento,
                                            width=espessura)

    elif ferramenta == "oval":
        if item_temp:
            canvas.delete(item_temp)
        item_temp = canvas.create_oval(ini_x, ini_y, event.x, event.y,
                                       outline=cor_borda, fill=cor_preenchimento,
                                       width=espessura)


def finaliza(event):
    global item_temp

    if ferramenta == "retangulo":
        if item_temp:
            canvas.delete(item_temp)
        canvas.create_rectangle(ini_x, ini_y, event.x, event.y,
                                 outline=cor_borda, fill=cor_preenchimento,
                                 width=espessura)

    elif ferramenta == "oval":
        if item_temp:
            canvas.delete(item_temp)
        canvas.create_oval(ini_x, ini_y, event.x, event.y,
                            outline=cor_borda, fill=cor_preenchimento,
                            width=espessura)

    item_temp = None


def escolher_ferramenta(valor):
    global ferramenta
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


# janela
root = tk.Tk()
root.title("Desenho")

painel = tk.Frame(root, bg="#f0f0f0", padx=8, pady=8)
painel.pack(side=tk.LEFT, fill=tk.Y)

tk.Label(painel, text="Ferramenta", bg="#f0f0f0").pack(anchor=tk.W)
var = tk.StringVar(value="livre")
for texto, valor in [("Mão livre", "livre"), ("Retângulo", "retangulo"), ("Oval", "oval")]:
    tk.Radiobutton(painel, text=texto, variable=var, value=valor,
                   bg="#f0f0f0", command=lambda v=valor: escolher_ferramenta(v)).pack(anchor=tk.W)

tk.Label(painel, text="Borda", bg="#f0f0f0").pack(anchor=tk.W, pady=(10, 0))
btn_borda = tk.Button(painel, bg="black", width=4, command=escolher_cor_borda)
btn_borda.pack(anchor=tk.W)

tk.Label(painel, text="Preenchimento", bg="#f0f0f0").pack(anchor=tk.W, pady=(10, 0))
btn_preenche = tk.Button(painel, bg="white", width=4, command=escolher_cor_preenchimento)
btn_preenche.pack(anchor=tk.W)
tk.Button(painel, text="Sem preench.", command=sem_preenchimento).pack(anchor=tk.W, pady=(2, 0))

tk.Label(painel, text="Espessura", bg="#f0f0f0").pack(anchor=tk.W, pady=(10, 0))
def atualiza_espessura(v):
    global espessura
    espessura = int(v)
tk.Scale(painel, from_=1, to=20, orient=tk.HORIZONTAL,
         command=atualiza_espessura, bg="#f0f0f0").pack(anchor=tk.W)

# canvas
canvas = tk.Canvas(root, bg='white', width=600, height=600)
canvas.pack(side=tk.LEFT)

canvas.bind('<ButtonPress-1>', marca_inicio)
canvas.bind('<B1-Motion>', atualiza_fim)
canvas.bind('<ButtonRelease-1>', finaliza)

root.mainloop()
