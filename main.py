import tkinter as tk

from controlador.gerente_fluxo import GerenteFluxo
from visao.painel_usuario import PainelUsuario


def principal():
    janela = tk.Tk()
    try:
        janela.state("zoomed")
    except tk.TclError:
        janela.geometry("1100x700")

    controlador = GerenteFluxo()
    visao = PainelUsuario(janela, controlador)
    controlador.vincular_view(visao)
    janela.mainloop()


if __name__ == "__main__":
    principal()
