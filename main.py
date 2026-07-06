import tkinter as tk
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from controlador.gerente_fluxo import GerenteFluxo
from visao.painel_usuario import PainelUsuario

def principal():
    janela = tk.Tk()
    
    modulo_controle = GerenteFluxo()
    modulo_visao = PainelUsuario(janela, modulo_controle)
    modulo_controle.vincular_view(modulo_visao)
    
    janela.mainloop()

if __name__ == "__main__":
    principal()